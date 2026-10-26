"""
Round 3 Compound SMC Execution Engine.

Specification:
1. Maker Limit Order Entry:
   - Places order at 50% retracement of OB/FVG zone (limit_entry_px).
   - Requires price penetration: LimitPrice ± 0.05 * ATR (no touch-fills).
     * BUY: Low <= LimitPrice - 0.05 * ATR.
     * SELL: High >= LimitPrice + 0.05 * ATR.
   - Maker fee: 0.02% (0.0002), 0.00% slippage.
   - Order expiry: cancelled if not filled within expiry_bars (default: 3).
2. Taker Stop Loss & Early BE:
   - Dynamic slippage: 0.05% + fee 0.05%.
   - Early BE: when MFE >= 0.7R, moves SL to Entry ± 0.15 * ATR.
   - Intra-bar sequence pessimism: if both SL and TP are touched in the same bar, SL wins!
3. TP1 & TP2 Double-Entry Accounting:
   - TP1 at 1.5R: closes 50% of initial position with Maker fee 0.02%.
   - TP2 at 3.0R: closes remaining 50% position with Maker fee 0.02%.
   - Strict balance conservation: Total PnL == Realized TP1 PnL + Realized Remaining PnL.
4. Compound Capital Model:
   - Size dynamically calculated from accumulated equity:
     Size = (Equity * Risk%) / StopDistance
   - Bounded by max notional leverage (default: 4.0x).
5. AlphaGPT Features & Credal Uncertainty Gate:
   - Evaluates Credal evidence & epistemic uncertainty (u <= u_max, non-conflicting).
   - Integrates AlphaGPT micro-structure factors (OFI_Impulse, FVG_Absorption_Rate,
     Liquidity_Sweep_Intensity, Vol_Displacement_Ratio).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from src.credal_engine import CredalSMCEngine, CredalSignal, CredalDecision
from src.alphagpt_factor_miner import compute_alphagpt_factors


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PositionSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class PendingLimitOrder:
    order_id: str
    side: OrderSide
    limit_price: float
    size: float
    stop_loss: float
    tp1: float
    tp2: float
    placed_idx: int
    placed_time: Any
    expiry_bars: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, current_idx: int) -> bool:
        return (current_idx - self.placed_idx) > self.expiry_bars


@dataclass
class ActivePosition:
    position_id: str
    side: PositionSide
    entry_price: float
    entry_time: Any
    entry_idx: int
    initial_size: float
    remaining_size: float
    stop_loss: float
    tp1: float
    tp2: float
    tp1_hit: bool = False
    realized_tp1_pnl: float = 0.0
    early_be_triggered: bool = False
    total_entry_fee: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TradeRecord:
    trade_id: str
    direction: str
    entry_time: Any
    exit_time: Any
    entry_price: float
    exit_price: float
    initial_size: float
    exit_size: float
    pnl: float
    pnl_pct: float
    exit_reason: str
    tp1_hit: bool
    tp1_pnl: float
    remaining_pnl: float
    total_fees: float
    total_slippage: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "direction": self.direction,
            "entry_time": str(self.entry_time),
            "exit_time": str(self.exit_time),
            "entry_price": float(self.entry_price),
            "exit_price": float(self.exit_price),
            "size": float(self.initial_size),
            "initial_size": float(self.initial_size),
            "exit_size": float(self.exit_size),
            "pnl": float(self.pnl),
            "pnl_pct": float(self.pnl_pct),
            "exit_reason": self.exit_reason,
            "tp1_hit": bool(self.tp1_hit),
            "tp1_pnl": float(self.tp1_pnl),
            "remaining_pnl": float(self.remaining_pnl),
            "total_fees": float(self.total_fees),
            "total_slippage": float(self.total_slippage),
            "metadata": self.metadata,
        }


class SMCRound3ExecutionEngine:
    """Round 3 Execution Engine adhering to strict quant invariants and contract."""

    def __init__(
        self,
        initial_cash: float = 1000.0,
        maker_fee: float = 0.0002,         # 0.02% Maker fee
        taker_fee: float = 0.0005,         # 0.05% Taker fee
        taker_slippage: float = 0.0005,    # 0.05% Dynamic slippage base
        risk_pct: float = 1.0,             # 1.0% Risk per trade
        use_compound: bool = True,         # Compound capital sizing
        max_leverage: float = 4.0,         # Maximum 4.0x leverage cap
        penetration_atr_mult: float = 0.05,# 0.05 * ATR penetration requirement
        rr_tp1: float = 1.5,               # 1.5R partial TP1 (closes 50%)
        rr_tp2: float = 3.0,               # 3.0R final TP2 (closes remaining 50%)
        early_be_mfe_r: float = 0.7,       # MFE >= 0.7R triggers early BE
        early_be_buffer_atr: float = 0.15, # Entry ± 0.15 * ATR
        limit_order_expiry_bars: int = 3,  # 3 bars time-in-force
        use_credal: bool = True,           # Credal uncertainty gate
        credal_u_max: float = 0.35,        # Maximum allowable vacuity
        credal_delta: float = 0.15,        # Evidence margin conflict threshold
        pessimistic_intra_bar: bool = True,# Same-bar TP/SL conflict strictly hits SL
    ) -> None:
        self.initial_cash = float(initial_cash)
        self.maker_fee = float(maker_fee)
        self.taker_fee = float(taker_fee)
        self.taker_slippage = float(taker_slippage)
        self.risk_pct = float(risk_pct)
        self.use_compound = bool(use_compound)
        self.max_leverage = float(max_leverage)
        self.penetration_atr_mult = float(penetration_atr_mult)
        self.rr_tp1 = float(rr_tp1)
        self.rr_tp2 = float(rr_tp2)
        self.early_be_mfe_r = float(early_be_mfe_r)
        self.early_be_buffer_atr = float(early_be_buffer_atr)
        self.limit_order_expiry_bars = int(limit_order_expiry_bars)
        self.use_credal = bool(use_credal)
        self.credal_u_max = float(credal_u_max)
        self.credal_delta = float(credal_delta)
        self.pessimistic_intra_bar = bool(pessimistic_intra_bar)

        self.credal_engine = (
            CredalSMCEngine(u_max=self.credal_u_max, delta=self.credal_delta)
            if self.use_credal
            else None
        )

    def calculate_position_size(
        self,
        equity: float,
        entry_price: float,
        stop_loss_price: float,
    ) -> float:
        """
        Compound Capital Model:
        Size = (Equity * Risk%) / StopDistance
        Bounded by max notional leverage:
        MaxNotional = (Equity * max_leverage) / entry_price
        """
        stop_distance = abs(entry_price - stop_loss_price)
        if stop_distance <= 0.0 or entry_price <= 0.0:
            return 0.0

        base_capital = max(equity, 10.0) if self.use_compound else self.initial_cash
        risk_budget = base_capital * (self.risk_pct / 100.0)
        size_by_risk = risk_budget / stop_distance

        max_allowed_size = (base_capital * self.max_leverage) / entry_price
        final_size = min(size_by_risk, max_allowed_size)
        return float(final_size)

    def evaluate_credal_gate(
        self,
        row: Union[pd.Series, Dict[str, Any]],
    ) -> Tuple[bool, Optional[CredalDecision]]:
        """Evaluate Credal uncertainty gate."""
        if not self.use_credal or self.credal_engine is None:
            return True, None

        if isinstance(row, pd.Series):
            indicators = row.to_dict()
        elif isinstance(row, dict):
            indicators = dict(row)
        else:
            indicators = vars(row)

        # If the incoming row already evaluated credal uncertainty and should_abstain
        if "credal_uncertainty" in indicators and "should_abstain" in indicators:
            u_val = float(indicators["credal_uncertainty"])
            abstain_val = bool(indicators["should_abstain"])
            if abstain_val or u_val > self.credal_u_max:
                return False, None
            return True, None
        decision = self.credal_engine.evaluate(**indicators)
        if decision.should_abstain or decision.uncertainty > self.credal_u_max:
            return False, decision

        return True, decision

    def run(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Execute backtest on provided DataFrame."""
        if len(df) == 0:
            return {
                "trades": [],
                "equity_curve": [self.initial_cash],
                "metrics": self._empty_metrics(),
            }

        data = df.copy()
        col_rename = {
            "open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"
        }
        data = data.rename(columns={k: v for k, v in col_rename.items() if k in data.columns and v not in data.columns})

        # Ensure ATR exists
        if "ATR" not in data.columns and "atr" not in data.columns:
            high_low = data["High"] - data["Low"]
            high_prev = (data["High"] - data["Close"].shift(1)).abs()
            low_prev = (data["Low"] - data["Close"].shift(1)).abs()
            tr = pd.concat([high_low, high_prev, low_prev], axis=1).max(axis=1)
            data["ATR"] = tr.rolling(window=14, min_periods=1).mean().bfill()
        elif "atr" in data.columns and "ATR" not in data.columns:
            data["ATR"] = data["atr"]

        # If AlphaGPT factors are missing, automatically compute them
        agpt_cols = ["OFI_Impulse", "FVG_Absorption_Rate", "Liquidity_Sweep_Intensity", "Vol_Displacement_Ratio"]
        if not all(col in data.columns for col in agpt_cols):
            try:
                agpt_df = compute_alphagpt_factors(data)
                for c in agpt_cols:
                    if c in agpt_df.columns and c not in data.columns:
                        data[c] = agpt_df[c]
            except Exception:
                pass

        # Cache NumPy arrays for fast vectorized access
        close_arr = data["Close"].values.astype(float)
        high_arr = data["High"].values.astype(float)
        low_arr = data["Low"].values.astype(float)
        open_arr = data["Open"].values.astype(float)
        atr_arr = data["ATR"].values.astype(float)
        timestamps = data.index if hasattr(data, "index") else np.arange(len(data))
        n = len(data)

        # Standardize Signal column
        signal_series = None
        for col in ["Signal", "signal"]:
            if col in data.columns:
                signal_series = data[col].values
                break

        limit_entry_series = None
        for col in ["limit_entry_px", "LimitEntryPx", "limit_entry", "LimitEntry"]:
            if col in data.columns:
                limit_entry_series = data[col].values
                break

        sl_series = None
        for col in ["stop_loss", "StopLoss", "sl", "SL"]:
            if col in data.columns:
                sl_series = data[col].values
                break

        tp1_series = None
        for col in ["tp1", "TP1"]:
            if col in data.columns:
                tp1_series = data[col].values
                break

        tp2_series = None
        for col in ["tp2", "TP2"]:
            if col in data.columns:
                tp2_series = data[col].values
                break

        # State tracking
        cash = self.initial_cash
        equity = self.initial_cash
        equity_curve: List[float] = [equity]
        trades: List[Dict[str, Any]] = []

        total_fees = 0.0
        total_slippage = 0.0
        order_counter = 0

        pending_order: Optional[PendingLimitOrder] = None
        active_position: Optional[ActivePosition] = None
        just_entered = False

        for idx in range(n):
            current_time = timestamps[idx]
            close = close_arr[idx]
            high = high_arr[idx]
            low = low_arr[idx]
            atr = atr_arr[idx]
            bar_range = high - low

            # -------------------------------------------------------------
            # STEP 1: Process Pending Limit Order (Strict Penetration Fill)
            # -------------------------------------------------------------
            if pending_order is not None and active_position is None:
                if pending_order.is_expired(idx):
                    pending_order = None
                else:
                    # Strict penetration requirement: LimitPrice ± 0.05 * ATR
                    penetration = self.penetration_atr_mult * atr
                    filled = False
                    if pending_order.side == OrderSide.BUY:
                        if low <= (pending_order.limit_price - penetration):
                            filled = True
                    elif pending_order.side == OrderSide.SELL:
                        if high >= (pending_order.limit_price + penetration):
                            filled = True

                    if filled:
                        exec_price = pending_order.limit_price
                        # Maker fill: 0.02% fee, 0.00% slippage
                        entry_fee = pending_order.size * exec_price * self.maker_fee
                        total_fees += entry_fee
                        cash -= entry_fee
                        equity -= entry_fee
                        just_entered = True
                        active_position = ActivePosition(
                            position_id=pending_order.order_id,
                            side=PositionSide.LONG if pending_order.side == OrderSide.BUY else PositionSide.SHORT,
                            entry_price=exec_price,
                            entry_time=current_time,
                            entry_idx=idx,
                            initial_size=pending_order.size,
                            remaining_size=pending_order.size,
                            stop_loss=pending_order.stop_loss,
                            tp1=pending_order.tp1,
                            tp2=pending_order.tp2,
                            tp1_hit=False,
                            realized_tp1_pnl=0.0,
                            early_be_triggered=False,
                            total_entry_fee=entry_fee,
                            metadata=pending_order.metadata,
                        )
                        pending_order = None

            # -------------------------------------------------------------
            # STEP 2: Manage Active Position (Double-Entry, Early BE, Intra-bar Pessimism)
            # -------------------------------------------------------------
            if active_position is not None and not just_entered:
                pos = active_position
                closed = False

                sl_touched = False
                if pos.side == PositionSide.LONG and low <= pos.stop_loss:
                    sl_touched = True
                elif pos.side == PositionSide.SHORT and high >= pos.stop_loss:
                    sl_touched = True

                tp1_touched = False
                if not pos.tp1_hit:
                    if pos.side == PositionSide.LONG and high >= pos.tp1:
                        tp1_touched = True
                    elif pos.side == PositionSide.SHORT and low <= pos.tp1:
                        tp1_touched = True

                tp2_touched = False
                if pos.tp1_hit:
                    if pos.side == PositionSide.LONG and high >= pos.tp2:
                        tp2_touched = True
                    elif pos.side == PositionSide.SHORT and low <= pos.tp2:
                        tp2_touched = True

                # Pessimistic Intra-Bar Sequence Conflict Resolution:
                # If both SL and TP are touched in the same bar, SL wins!
                if sl_touched and (tp1_touched or tp2_touched) and self.pessimistic_intra_bar:
                    # Execute Taker SL immediately on current remaining position
                    dyn_slip = self.taker_slippage + 0.10 * (bar_range / max(atr, 1e-6)) * self.taker_slippage
                    if pos.side == PositionSide.LONG:
                        exit_px = pos.stop_loss * (1.0 - dyn_slip)
                        pnl_rem = pos.remaining_size * (exit_px - pos.entry_price)
                        slip_loss = pos.remaining_size * (pos.stop_loss - exit_px)
                    else:
                        exit_px = pos.stop_loss * (1.0 + dyn_slip)
                        pnl_rem = pos.remaining_size * (pos.entry_price - exit_px)
                        slip_loss = pos.remaining_size * (exit_px - pos.stop_loss)

                    fee_sl = pos.remaining_size * exit_px * self.taker_fee
                    total_fees += fee_sl
                    total_slippage += slip_loss
                    pnl_rem -= fee_sl
                    cash += pnl_rem
                    equity += pnl_rem

                    total_trade_pnl = (pos.realized_tp1_pnl if pos.tp1_hit else 0.0) + pnl_rem
                    total_trade_fees = pos.total_entry_fee + (
                        pos.initial_size * 0.5 * pos.tp1 * self.maker_fee if pos.tp1_hit else 0.0
                    ) + fee_sl

                    exit_label = "BE_SL" if pos.early_be_triggered else "INTRA_BAR_SL_CONFLICT"
                    trades.append(
                        TradeRecord(
                            trade_id=pos.position_id,
                            direction=pos.side.value,
                            entry_time=pos.entry_time,
                            exit_time=current_time,
                            entry_price=pos.entry_price,
                            exit_price=exit_px,
                            initial_size=pos.initial_size,
                            exit_size=pos.remaining_size,
                            pnl=total_trade_pnl,
                            pnl_pct=(total_trade_pnl / (pos.initial_size * pos.entry_price)) * 100.0,
                            exit_reason=exit_label,
                            tp1_hit=pos.tp1_hit,
                            tp1_pnl=pos.realized_tp1_pnl,
                            remaining_pnl=pnl_rem,
                            total_fees=total_trade_fees,
                            total_slippage=slip_loss,
                            metadata=pos.metadata,
                        ).to_dict()
                    )
                    active_position = None
                    closed = True

                # Normal sequential execution when no intra-bar conflict
                if not closed and active_position is not None:
                    # 2A. TP1 check (1.5R): closes 50% with Maker fee 0.02%
                    if tp1_touched and not pos.tp1_hit:
                        exit_px = pos.tp1
                        close_size = pos.initial_size * 0.5
                        fee_tp1 = close_size * exit_px * self.maker_fee
                        total_fees += fee_tp1

                        if pos.side == PositionSide.LONG:
                            tp1_pnl = close_size * (exit_px - pos.entry_price) - fee_tp1
                            be_sl = pos.entry_price + self.early_be_buffer_atr * atr
                        else:
                            tp1_pnl = close_size * (pos.entry_price - exit_px) - fee_tp1
                            be_sl = pos.entry_price - self.early_be_buffer_atr * atr

                        cash += tp1_pnl
                        equity += tp1_pnl
                        pos.realized_tp1_pnl = tp1_pnl
                        pos.remaining_size = pos.initial_size - close_size
                        pos.tp1_hit = True
                        pos.stop_loss = be_sl
                        pos.early_be_triggered = True
                        tp1_just_hit_on_this_bar = True
                    else:
                        tp1_just_hit_on_this_bar = False

                    # 2B. TP2 check (3.0R): closes remaining 50% with Maker fee 0.02%
                    if tp2_touched and pos.tp1_hit:
                        exit_px = pos.tp2
                        fee_rem = pos.remaining_size * exit_px * self.maker_fee
                        total_fees += fee_rem

                        if pos.side == PositionSide.LONG:
                            pnl_rem = pos.remaining_size * (exit_px - pos.entry_price) - fee_rem
                        else:
                            pnl_rem = pos.remaining_size * (pos.entry_price - exit_px) - fee_rem

                        cash += pnl_rem
                        equity += pnl_rem

                        total_trade_pnl = pos.realized_tp1_pnl + pnl_rem
                        total_trade_fees = pos.total_entry_fee + (
                            pos.initial_size * 0.5 * pos.tp1 * self.maker_fee
                        ) + fee_rem

                        trades.append(
                            TradeRecord(
                                trade_id=pos.position_id,
                                direction=pos.side.value,
                                entry_time=pos.entry_time,
                                exit_time=current_time,
                                entry_price=pos.entry_price,
                                exit_price=exit_px,
                                initial_size=pos.initial_size,
                                exit_size=pos.remaining_size,
                                pnl=total_trade_pnl,
                                pnl_pct=(total_trade_pnl / (pos.initial_size * pos.entry_price)) * 100.0,
                                exit_reason="TP2",
                                tp1_hit=pos.tp1_hit,
                                tp1_pnl=pos.realized_tp1_pnl,
                                remaining_pnl=pnl_rem,
                                total_fees=total_trade_fees,
                                total_slippage=0.0,
                                metadata=pos.metadata,
                            ).to_dict()
                        )
                        active_position = None
                        closed = True

                    # 2C. Stop Loss check: Taker fee 0.05% + dynamic slippage
                    if not closed and active_position is not None and not tp1_just_hit_on_this_bar and sl_touched:
                        dyn_slip = self.taker_slippage + 0.10 * (bar_range / max(atr, 1e-6)) * self.taker_slippage
                        if pos.side == PositionSide.LONG:
                            exit_px = pos.stop_loss * (1.0 - dyn_slip)
                            slip = pos.remaining_size * (pos.stop_loss - exit_px)
                            pnl_rem = pos.remaining_size * (exit_px - pos.entry_price)
                        else:
                            exit_px = pos.stop_loss * (1.0 + dyn_slip)
                            slip = pos.remaining_size * (exit_px - pos.stop_loss)
                            pnl_rem = pos.remaining_size * (pos.entry_price - exit_px)

                        fee_sl = pos.remaining_size * exit_px * self.taker_fee
                        total_fees += fee_sl
                        total_slippage += slip
                        pnl_rem -= fee_sl

                        cash += pnl_rem
                        equity += pnl_rem

                        total_trade_pnl = (pos.realized_tp1_pnl if pos.tp1_hit else 0.0) + pnl_rem
                        total_trade_fees = pos.total_entry_fee + (
                            pos.initial_size * 0.5 * pos.tp1 * self.maker_fee if pos.tp1_hit else 0.0
                        ) + fee_sl

                        exit_label = "BE_SL" if pos.early_be_triggered else "STOP_LOSS"
                        trades.append(
                            TradeRecord(
                                trade_id=pos.position_id,
                                direction=pos.side.value,
                                entry_time=pos.entry_time,
                                exit_time=current_time,
                                entry_price=pos.entry_price,
                                exit_price=exit_px,
                                initial_size=pos.initial_size,
                                exit_size=pos.remaining_size,
                                pnl=total_trade_pnl,
                                pnl_pct=(total_trade_pnl / (pos.initial_size * pos.entry_price)) * 100.0,
                                exit_reason=exit_label,
                                tp1_hit=pos.tp1_hit,
                                tp1_pnl=pos.realized_tp1_pnl,
                                remaining_pnl=pnl_rem,
                                total_fees=total_trade_fees,
                                total_slippage=slip,
                                metadata=pos.metadata,
                            ).to_dict()
                        )
                        active_position = None
                        closed = True

                    # 2D. Early BE Check: when MFE >= 0.7R, move SL to Entry ± 0.15 ATR
                    if not closed and active_position is not None and not pos.early_be_triggered:
                        stop_dist = abs(pos.entry_price - pos.stop_loss)
                        mfe_threshold = self.early_be_mfe_r * stop_dist
                        if pos.side == PositionSide.LONG and (high - pos.entry_price) >= mfe_threshold:
                            pos.stop_loss = pos.entry_price + self.early_be_buffer_atr * atr
                            pos.early_be_triggered = True
                        elif pos.side == PositionSide.SHORT and (pos.entry_price - low) >= mfe_threshold:
                            pos.stop_loss = pos.entry_price - self.early_be_buffer_atr * atr
                            pos.early_be_triggered = True

            # -------------------------------------------------------------
            # STEP 3: Signal Generation & Pending Limit Order Placement
            # -------------------------------------------------------------
            if active_position is None and pending_order is None:
                sig = signal_series[idx] if signal_series is not None else None
                if sig in ("LONG", "SHORT", 1, -1, CredalSignal.BULLISH, CredalSignal.BEARISH):
                    is_long = sig in ("LONG", 1, CredalSignal.BULLISH)

                    # 3A. Credal Uncertainty Gate Check
                    credal_allowed, credal_decision = self.evaluate_credal_gate(data.iloc[idx])
                    if not credal_allowed:
                        pass
                    else:
                        # 3B. Maker Limit Order at 50% retracement of OB/FVG zone
                        if limit_entry_series is not None and not np.isnan(limit_entry_series[idx]):
                            limit_px = float(limit_entry_series[idx])
                        else:
                            if "Equilibrium" in data.columns and not np.isnan(data["Equilibrium"].iloc[idx]):
                                limit_px = float(data["Equilibrium"].iloc[idx])
                            elif "equilibrium" in data.columns and not np.isnan(data["equilibrium"].iloc[idx]):
                                limit_px = float(data["equilibrium"].iloc[idx])
                            else:
                                limit_px = (close - 0.2 * atr) if is_long else (close + 0.2 * atr)

                        # 3C. SL and TP levels (TP1 at 1.5R, TP2 at 3.0R)
                        if sl_series is not None and not np.isnan(sl_series[idx]):
                            sl_val = float(sl_series[idx])
                        else:
                            sl_val = (limit_px - 1.5 * atr) if is_long else (limit_px + 1.5 * atr)

                        stop_dist = abs(limit_px - sl_val)

                        if tp1_series is not None and not np.isnan(tp1_series[idx]):
                            tp1_val = float(tp1_series[idx])
                        else:
                            tp1_val = (limit_px + self.rr_tp1 * stop_dist) if is_long else (limit_px - self.rr_tp1 * stop_dist)

                        if tp2_series is not None and not np.isnan(tp2_series[idx]):
                            tp2_val = float(tp2_series[idx])
                        else:
                            tp2_val = (limit_px + self.rr_tp2 * stop_dist) if is_long else (limit_px - self.rr_tp2 * stop_dist)

                        # Compound Capital Model Position Sizing: Size = (Equity * Risk%) / StopDist
                        if stop_dist > 0.0 and stop_dist <= limit_px * 0.15:
                            order_size = self.calculate_position_size(
                                equity=cash,
                                entry_price=limit_px,
                                stop_loss_price=sl_val,
                            )

                            if order_size > 0.0:
                                order_counter += 1
                                meta = {}
                                if credal_decision is not None:
                                    meta["credal_uncertainty"] = float(credal_decision.uncertainty)
                                    meta["credal_signal"] = credal_decision.credal_signal.value

                                pending_order = PendingLimitOrder(
                                    order_id=f"ORD_R3_{order_counter:05d}",
                                    side=OrderSide.BUY if is_long else OrderSide.SELL,
                                    limit_price=limit_px,
                                    size=order_size,
                                    stop_loss=sl_val,
                                    tp1=tp1_val,
                                    tp2=tp2_val,
                                    placed_idx=idx,
                                    placed_time=current_time,
                                    expiry_bars=self.limit_order_expiry_bars,
                                    metadata=meta,
                                )

            # -------------------------------------------------------------
            # STEP 4: Mark to Market Equity Tracking
            # -------------------------------------------------------------
            if active_position is not None:
                pos = active_position
                if pos.side == PositionSide.LONG:
                    unrealized = pos.remaining_size * (close - pos.entry_price) - (
                        pos.remaining_size * close * self.taker_fee
                    )
                else:
                    unrealized = pos.remaining_size * (pos.entry_price - close) - (
                        pos.remaining_size * close * self.taker_fee
                    )
                current_equity = cash + unrealized
                equity_curve.append(current_equity)
            else:
                equity_curve.append(cash)

            just_entered = False

        # Close any lingering open position on final bar
        if active_position is not None:
            pos = active_position
            final_close = close_arr[-1]
            fee_last = pos.remaining_size * final_close * self.taker_fee
            slip_last = pos.remaining_size * final_close * self.taker_slippage
            if pos.side == PositionSide.LONG:
                pnl_rem = pos.remaining_size * (final_close * (1.0 - self.taker_slippage) - pos.entry_price) - fee_last
            else:
                pnl_rem = pos.remaining_size * (pos.entry_price - final_close * (1.0 + self.taker_slippage)) - fee_last

            cash += pnl_rem
            equity = cash
            total_fees += fee_last
            total_slippage += slip_last
            total_trade_pnl = (pos.realized_tp1_pnl if pos.tp1_hit else 0.0) + pnl_rem
            total_trade_fees = pos.total_entry_fee + (
                pos.initial_size * 0.5 * pos.tp1 * self.maker_fee if pos.tp1_hit else 0.0
            ) + fee_last

            trades.append(
                TradeRecord(
                    trade_id=pos.position_id,
                    direction=pos.side.value,
                    entry_time=pos.entry_time,
                    exit_time=timestamps[-1],
                    entry_price=pos.entry_price,
                    exit_price=final_close,
                    initial_size=pos.initial_size,
                    exit_size=pos.remaining_size,
                    pnl=total_trade_pnl,
                    pnl_pct=(total_trade_pnl / (pos.initial_size * pos.entry_price)) * 100.0,
                    exit_reason="END_OF_DATA",
                    tp1_hit=pos.tp1_hit,
                    tp1_pnl=pos.realized_tp1_pnl,
                    remaining_pnl=pnl_rem,
                    total_fees=total_trade_fees,
                    total_slippage=slip_last,
                    metadata=pos.metadata,
                ).to_dict()
            )

        metrics = self._calculate_metrics(
            trades=trades,
            equity_curve=equity_curve,
            final_cash=cash,
            total_fees=total_fees,
            total_slippage=total_slippage,
        )

        return {
            "trades": trades,
            "metrics": metrics,
            "equity_curve": equity_curve,
        }

    def _calculate_metrics(
        self,
        trades: List[Dict[str, Any]],
        equity_curve: List[float],
        final_cash: float,
        total_fees: float,
        total_slippage: float,
    ) -> Dict[str, Any]:
        """Compute performance metrics."""
        total_trades = len(trades)
        if total_trades == 0:
            return self._empty_metrics()

        pnls = [t["pnl"] for t in trades]
        winning_trades = [p for p in pnls if p > 0]
        losing_trades = [p for p in pnls if p < 0]

        win_rate = (len(winning_trades) / total_trades) * 100.0
        total_profit = sum(winning_trades)
        total_loss = abs(sum(losing_trades))

        if total_loss > 0:
            profit_factor = total_profit / total_loss
        elif total_profit > 0:
            profit_factor = float("inf")
        else:
            profit_factor = 0.0

        total_return_pct = ((final_cash - self.initial_cash) / self.initial_cash) * 100.0

        # Maximum Drawdown
        eq = np.array(equity_curve)
        cummax = np.maximum.accumulate(eq)
        drawdowns = (cummax - eq) / np.maximum(cummax, 1e-6)
        max_drawdown_pct = float(np.max(drawdowns)) * 100.0 if len(drawdowns) > 0 else 0.0

        # Sharpe ratio
        trade_returns = [t["pnl_pct"] / 100.0 for t in trades]
        if len(trade_returns) > 1:
            mean_ret = np.mean(trade_returns)
            std_ret = np.std(trade_returns, ddof=1)
            sharpe = float((mean_ret / std_ret) * np.sqrt(252)) if std_ret > 0 else 0.0
        else:
            sharpe = 0.0

        # Maker fill count
        maker_trades = sum(1 for t in trades if t.get("exit_reason") in ("TP1", "TP2"))
        maker_fill_ratio = (maker_trades / total_trades) if total_trades > 0 else 0.0

        return {
            "total_trades": total_trades,
            "win_rate_pct": round(win_rate, 2),
            "total_return_pct": round(total_return_pct, 2),
            "profit_factor": round(profit_factor, 3) if not math.isinf(profit_factor) else 999.0,
            "max_drawdown_pct": round(max_drawdown_pct, 2),
            "sharpe_ratio": round(sharpe, 3),
            "total_profit": round(total_profit, 2),
            "total_loss": round(total_loss, 2),
            "total_fees": round(total_fees, 4),
            "total_slippage_cost": round(total_slippage, 4),
            "final_cash": round(final_cash, 4),
            "maker_fill_ratio": round(maker_fill_ratio, 3),
        }

    def _empty_metrics(self) -> Dict[str, Any]:
        return {
            "total_trades": 0,
            "win_rate_pct": 0.0,
            "total_return_pct": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 0.0,
            "sharpe_ratio": 0.0,
            "total_profit": 0.0,
            "total_loss": 0.0,
            "total_fees": 0.0,
            "total_slippage_cost": 0.0,
            "final_cash": self.initial_cash,
            "maker_fill_ratio": 0.0,
        }
