"""
Round 4 Unified Cross-Asset Portfolio Execution Engine.

Specification:
1. Shared Multi-Asset Capital Pool:
   - Initial Capital: $10,000 USD shared across all assets (BTC, ETH, SOL, BNB, NEAR, AAPL).
   - Global Concurrency Control: at most max_concurrent_positions = 2 concurrent active positions.
   - Liquidity Reserve: never allocates more than 50% of current equity at any single time,
     preserving cash for higher-conviction opportunities across other symbols.
   - Cash non-negativity: cash balance never drops below 0.
2. Cross-Asset Opportunistic Priority:
   - When multiple symbols signal entry in the same bar, priority is given to the highest composite score:
     Priority = (1.0 - u) * AlphaGPT_Confluence_Score
   - Higher-conviction opportunities take precedence when concurrency capacity is bounded.
3. Maker Limit Order Entries:
   - Places orders at 50% retracement of OB/FVG zone (limit_entry_px).
   - Requires pessimistic penetration: LimitPrice ± 0.05 * ATR (no touch-fills).
     * BUY: Low <= LimitPrice - 0.05 * ATR.
     * SELL: High >= LimitPrice + 0.05 * ATR.
   - Maker fee: 0.02% (0.0002), 0.00% slippage.
   - Order expiry: cancelled if not filled within expiry_bars (default: 3 bars for that symbol).
4. TP1 (50% reduction) + Early BE Buffer + TP2 Terminal Liquidation:
   - TP1 at 1.5R: closes 50% of initial position with Maker fee 0.02%.
   - Early BE buffer: when MFE >= 0.7R or upon TP1 hit, moves SL to Entry ± 0.15 * ATR.
   - TP2 at 3.0R: closes remaining 50% position with Maker fee 0.02%.
   - Pessimistic intra-bar conflict: same-bar TP and SL conflict strictly hits SL.
   - Stop Loss: Taker fee 0.05% + dynamic slippage base 0.05% + volatility scaling.
5. Equity Compounding & Accounting Conservation:
   - Position sizes dynamically scale with net portfolio wealth:
     Size = (Equity * Risk%) / StopDistance.
   - Bounded by liquidity reserve and max leverage.
   - Strict balance conservation: Total PnL == Realized TP1 PnL + Realized Remaining PnL.
   - Final Cash - Initial Cash == Total Trade PnL - Total Entry Fees.
6. Deliverables:
   - Output: trade history JSONs and results/round4_portfolio/shared_portfolio_summary.csv.
"""

from __future__ import annotations

import gc
import json
import logging
import math
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

from src.credal_engine import CredalDecision, CredalSMCEngine, CredalSignal

logger = logging.getLogger("smc_round4_portfolio")


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PositionSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class PendingLimitOrder:
    order_id: str
    symbol: str
    side: OrderSide
    limit_price: float
    size: float
    allocated_margin: float
    stop_loss: float
    tp1: float
    tp2: float
    placed_idx: int
    placed_time: Any
    expiry_bars: int = 3
    priority: float = 0.0
    bars_elapsed: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        return self.bars_elapsed > self.expiry_bars


@dataclass
class ActivePosition:
    position_id: str
    symbol: str
    side: PositionSide
    entry_price: float
    entry_time: Any
    entry_idx: int
    initial_size: float
    remaining_size: float
    allocated_margin: float
    stop_loss: float
    tp1: float
    tp2: float
    tp1_hit: bool = False
    realized_tp1_pnl: float = 0.0
    early_be_triggered: bool = False
    total_entry_fee: float = 0.0
    tp1_fee: float = 0.0
    priority: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TradeRecord:
    trade_id: str
    symbol: str
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
    entry_fee: float
    tp1_fee: float
    exit_fee: float
    total_fees: float
    total_slippage: float
    priority: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "direction": self.direction,
            "entry_time": str(self.entry_time),
            "exit_time": str(self.exit_time),
            "entry_price": round(self.entry_price, 6),
            "exit_price": round(self.exit_price, 6),
            "initial_size": round(self.initial_size, 6),
            "exit_size": round(self.exit_size, 6),
            "pnl": round(self.pnl, 6),
            "pnl_pct": round(self.pnl_pct, 4),
            "exit_reason": self.exit_reason,
            "tp1_hit": self.tp1_hit,
            "tp1_pnl": round(self.tp1_pnl, 6),
            "remaining_pnl": round(self.remaining_pnl, 6),
            "entry_fee": round(self.entry_fee, 6),
            "tp1_fee": round(self.tp1_fee, 6),
            "exit_fee": round(self.exit_fee, 6),
            "total_fees": round(self.total_fees, 6),
            "total_slippage": round(self.total_slippage, 6),
            "priority": round(self.priority, 4),
            "metadata": self.metadata,
        }


class SMCSharedPortfolioEngine:
    """Production Unified Cross-Asset Portfolio Engine with Shared Capital & Concurrency Control."""

    def __init__(
        self,
        initial_cash: float = 10000.0,
        max_concurrent_positions: int = 2,
        liquidity_reserve_pct: float = 0.50,
        maker_fee: float = 0.0002,          # 0.02% Maker fee
        taker_fee: float = 0.0005,          # 0.05% Taker fee
        taker_slippage: float = 0.0005,     # 0.05% Base dynamic slippage
        risk_pct: float = 1.0,              # 1.0% Risk budget per trade
        use_compound: bool = True,          # Reinvest equity dynamically
        max_leverage: float = 4.0,          # 4.0x leverage bound
        penetration_atr_mult: float = 0.05, # 0.05 * ATR penetration requirement
        rr_tp1: float = 1.5,                # 1.5R partial TP1 (50% reduction)
        rr_tp2: float = 3.0,                # 3.0R final TP2 (terminal liquidation)
        early_be_mfe_r: float = 0.7,        # MFE >= 0.7R triggers early BE
        early_be_buffer_atr: float = 0.15,  # Entry ± 0.15 * ATR
        limit_order_expiry_bars: int = 3,   # 3 bars time-in-force per symbol
        use_credal: bool = True,            # Credal Dirichlet uncertainty filter
        credal_u_max: float = 0.35,         # Vacuity threshold
        credal_delta: float = 0.15,         # Conflict threshold
        pessimistic_intra_bar: bool = True, # SL wins intra-bar conflict
    ) -> None:
        self.initial_cash = float(initial_cash)
        self.max_concurrent_positions = int(max_concurrent_positions)
        self.liquidity_reserve_pct = float(liquidity_reserve_pct)
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
        current_allocated: float = 0.0,
    ) -> float:
        """
        Calculates position size adhering to:
        1. Compounding: Size = (Equity * Risk%) / StopDistance.
        2. Liquidity Reserve: never allocates more than 50% of current equity total,
           preserving cash for opportunities across other symbols.
        3. Cash non-negativity and maximum leverage bounds.
        """
        stop_distance = abs(entry_price - stop_loss_price)
        if stop_distance <= 0.0 or entry_price <= 0.0:
            return 0.0

        base_capital = max(equity, 10.0) if self.use_compound else self.initial_cash
        risk_budget = base_capital * (self.risk_pct / 100.0)
        size_by_risk = risk_budget / stop_distance

        # Liquidity reserve cap: total capital allocated across positions cannot exceed 50% of equity
        max_allowed_allocation = base_capital * self.liquidity_reserve_pct
        available_allocation = max(0.0, max_allowed_allocation - current_allocated)

        if available_allocation <= 0.0:
            return 0.0

        # Maximum notional allowed for this single position (fair share across concurrent slots)
        max_single_position_allocation = max_allowed_allocation / max(1, self.max_concurrent_positions)
        max_notional_per_pos = min(available_allocation, max_single_position_allocation)
        max_size_by_reserve = max_notional_per_pos / entry_price

        # Bound by leverage
        max_size_by_leverage = (base_capital * self.max_leverage) / entry_price

        final_size = min(size_by_risk, max_size_by_reserve, max_size_by_leverage)
        return float(max(0.0, final_size))

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

    def calculate_priority(
        self,
        row: Union[pd.Series, Dict[str, Any]],
        signal_val: Any,
        credal_decision: Optional[CredalDecision] = None,
    ) -> Tuple[float, float, float]:
        """
        Cross-Asset Opportunistic Priority Formula:
            Priority = (1.0 - u) * AlphaGPT_Confluence_Score
        Returns:
            (priority, u, confluence_score)
        """
        if isinstance(row, pd.Series):
            row_dict = row.to_dict()
        elif isinstance(row, dict):
            row_dict = row
        else:
            row_dict = vars(row)

        # 1. Uncertainty u
        if "priority" in row_dict and not np.isnan(row_dict["priority"]):
            u_val = float(row_dict.get("credal_uncertainty", row_dict.get("u", 0.0)))
            conf_score = float(row_dict.get("AlphaGPT_Confluence_Score", row_dict.get("score_long", 50.0)))
            return float(row_dict["priority"]), u_val, conf_score

        if "credal_uncertainty" in row_dict and not np.isnan(row_dict["credal_uncertainty"]):
            u_val = float(row_dict["credal_uncertainty"])
        elif "uncertainty" in row_dict and not np.isnan(row_dict["uncertainty"]):
            u_val = float(row_dict["uncertainty"])
        elif "u" in row_dict and not np.isnan(row_dict["u"]):
            u_val = float(row_dict["u"])
        elif credal_decision is not None:
            u_val = float(credal_decision.uncertainty)
        else:
            u_val = 0.0

        u_val = np.clip(u_val, 0.0, 1.0)

        # 2. Confluence Score
        if "AlphaGPT_Confluence_Score" in row_dict and not np.isnan(row_dict["AlphaGPT_Confluence_Score"]):
            conf_score = float(row_dict["AlphaGPT_Confluence_Score"])
        elif "alphagpt_confluence_score" in row_dict and not np.isnan(row_dict["alphagpt_confluence_score"]):
            conf_score = float(row_dict["alphagpt_confluence_score"])
        elif "confluence_score" in row_dict and not np.isnan(row_dict["confluence_score"]):
            conf_score = float(row_dict["confluence_score"])
        else:
            is_long = signal_val in ("LONG", 1, CredalSignal.BULLISH)
            if is_long and "score_long" in row_dict and not np.isnan(row_dict["score_long"]):
                conf_score = float(row_dict["score_long"])
            elif (not is_long) and "score_short" in row_dict and not np.isnan(row_dict["score_short"]):
                conf_score = float(row_dict["score_short"])
            elif "score" in row_dict and not np.isnan(row_dict["score"]):
                conf_score = float(row_dict["score"])
            else:
                conf_score = 50.0

        conf_score = np.clip(conf_score, 0.0, 100.0)
        priority = (1.0 - u_val) * conf_score
        return float(priority), float(u_val), float(conf_score)

    def _prepare_symbol_arrays(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Normalize columns and extract NumPy arrays for C-speed access."""
        data = df.copy()
        col_rename = {
            "open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"
        }
        data = data.rename(columns={k: v for k, v in col_rename.items() if k in data.columns and v not in data.columns})

        if "ATR" not in data.columns and "atr" not in data.columns:
            high_low = data["High"] - data["Low"]
            high_prev = (data["High"] - data["Close"].shift(1)).abs()
            low_prev = (data["Low"] - data["Close"].shift(1)).abs()
            tr = pd.concat([high_low, high_prev, low_prev], axis=1).max(axis=1)
            data["ATR"] = tr.rolling(window=14, min_periods=1).mean().bfill()
        elif "atr" in data.columns and "ATR" not in data.columns:
            data["ATR"] = data["atr"]

        signal_series = None
        for col in ["Signal", "signal"]:
            if col in data.columns:
                signal_series = data[col].values
                break

        limit_entry_series = None
        for col in ["limit_entry_px", "LimitEntryPx", "limit_entry", "LimitEntry", "Equilibrium", "equilibrium"]:
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

        # Uncertainty series
        u_series = None
        for col in ["credal_uncertainty", "uncertainty", "u"]:
            if col in data.columns:
                u_series = data[col].values
                break

        abstain_series = None
        if "should_abstain" in data.columns:
            abstain_series = data["should_abstain"].values

        # Confluence score series
        score_long_series = data["score_long"].values if "score_long" in data.columns else None
        score_short_series = data["score_short"].values if "score_short" in data.columns else None
        conf_series = None
        for col in ["AlphaGPT_Confluence_Score", "alphagpt_confluence_score", "confluence_score"]:
            if col in data.columns:
                conf_series = data[col].values
                break

        priority_series = None
        if "priority" in data.columns:
            priority_series = data["priority"].values
        elif "Priority" in data.columns:
            priority_series = data["Priority"].values

        return {
            "df": data,
            "close": data["Close"].values.astype(float),
            "high": data["High"].values.astype(float),
            "low": data["Low"].values.astype(float),
            "open": data["Open"].values.astype(float),
            "atr": data["ATR"].values.astype(float),
            "timestamps": data.index,
            "signal": signal_series,
            "limit_entry_px": limit_entry_series,
            "stop_loss": sl_series,
            "tp1": tp1_series,
            "tp2": tp2_series,
            "u": u_series,
            "should_abstain": abstain_series,
            "score_long": score_long_series,
            "score_short": score_short_series,
            "confluence_score": conf_series,
            "priority": priority_series,
        }

    def run(
        self,
        dfs: Dict[str, pd.DataFrame],
        eval_start_time: Optional[pd.Timestamp] = None,
    ) -> Dict[str, Any]:
        """
        Execute unified cross-asset portfolio simulation across all symbols.

        Parameters
        ----------
        dfs : Dict[str, pd.DataFrame]
            Dictionary mapping symbol name to its OHLCV / alpha DataFrame.
        eval_start_time : Optional[pd.Timestamp]
            If provided, only bars at or after eval_start_time can trigger new orders (for OOS warmup).
        """
        if not dfs:
            return self._empty_result()

        # 1. Pre-process and extract NumPy arrays for all symbols
        arrays: Dict[str, Dict[str, Any]] = {}
        all_timestamps_set = set()
        for sym, df in dfs.items():
            if len(df) == 0:
                continue
            arr_data = self._prepare_symbol_arrays(df)
            arrays[sym] = arr_data
            all_timestamps_set.update(df.index)

        if not arrays or not all_timestamps_set:
            return self._empty_result()

        # Unified chronological timeline
        all_timestamps = pd.DatetimeIndex(sorted(all_timestamps_set))
        n_timeline = len(all_timestamps)

        # Build indexer map for O(1) bar lookups: symbol -> row index in symbol DataFrame (-1 if no bar)
        idx_maps = {sym: arr["df"].index.get_indexer(all_timestamps) for sym, arr in arrays.items()}

        # 2. Portfolio State Tracking
        cash = self.initial_cash
        equity = self.initial_cash
        equity_curve: List[float] = [equity]
        cash_curve: List[float] = [cash]
        active_positions_history: List[int] = [0]
        trades: List[Dict[str, Any]] = []

        total_fees = 0.0
        total_slippage = 0.0
        order_counter = 0

        # Concurrency & reservation tracking
        active_positions: Dict[str, ActivePosition] = {}
        pending_orders: Dict[str, PendingLimitOrder] = {}
        just_entered_symbols: set = set()

        skipped_due_to_capacity = 0
        skipped_due_to_liquidity = 0
        skipped_due_to_credal = 0
        max_concurrent_observed = 0
        min_cash_observed = cash
        min_equity_observed = equity

        # 3. Chronological Simulation Loop
        for t_idx in range(n_timeline):
            current_time = all_timestamps[t_idx]
            just_entered_symbols.clear()

            # -----------------------------------------------------------------
            # STEP 1: Manage Active Positions (Double-Entry, Early BE, Intra-Bar Pessimism)
            # -----------------------------------------------------------------
            closed_symbols = []
            for sym, pos in list(active_positions.items()):
                sym_row_idx = idx_maps[sym][t_idx]
                if sym_row_idx == -1:
                    continue  # Asset not trading on this timestamp

                sym_arr = arrays[sym]
                close = sym_arr["close"][sym_row_idx]
                high = sym_arr["high"][sym_row_idx]
                low = sym_arr["low"][sym_row_idx]
                atr = max(sym_arr["atr"][sym_row_idx], 1e-6)
                bar_range = high - low

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

                # Pessimistic Intra-Bar Sequence Conflict: If both SL and TP touched, SL wins!
                if sl_touched and (tp1_touched or tp2_touched) and self.pessimistic_intra_bar:
                    dyn_slip = self.taker_slippage + 0.10 * (bar_range / atr) * self.taker_slippage
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
                    total_trade_fees = pos.total_entry_fee + pos.tp1_fee + fee_sl
                    exit_label = "BE_SL" if pos.early_be_triggered else "INTRA_BAR_SL_CONFLICT"

                    trades.append(
                        TradeRecord(
                            trade_id=pos.position_id,
                            symbol=pos.symbol,
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
                            entry_fee=pos.total_entry_fee,
                            tp1_fee=pos.tp1_fee,
                            exit_fee=fee_sl,
                            total_fees=total_trade_fees,
                            total_slippage=slip_loss,
                            priority=pos.priority,
                            metadata=pos.metadata,
                        ).to_dict()
                    )
                    closed_symbols.append(sym)
                    closed = True

                # Normal Sequential Execution
                if not closed:
                    tp1_just_hit_on_this_bar = False
                    # 1A. TP1 check (1.5R): closes 50% with Maker fee 0.02%
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
                        pos.tp1_fee = fee_tp1
                        pos.remaining_size = pos.initial_size - close_size
                        pos.allocated_margin = pos.remaining_size * pos.entry_price
                        pos.tp1_hit = True
                        pos.stop_loss = be_sl
                        pos.early_be_triggered = True
                        tp1_just_hit_on_this_bar = True

                    # 1B. TP2 check (3.0R): closes remaining 50% with Maker fee 0.02%
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
                        total_trade_fees = pos.total_entry_fee + pos.tp1_fee + fee_rem

                        trades.append(
                            TradeRecord(
                                trade_id=pos.position_id,
                                symbol=pos.symbol,
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
                                entry_fee=pos.total_entry_fee,
                                tp1_fee=pos.tp1_fee,
                                exit_fee=fee_rem,
                                total_fees=total_trade_fees,
                                total_slippage=0.0,
                                priority=pos.priority,
                                metadata=pos.metadata,
                            ).to_dict()
                        )
                        closed_symbols.append(sym)
                        closed = True

                    # 1C. Stop Loss check: Taker fee 0.05% + dynamic slippage
                    if not closed and not tp1_just_hit_on_this_bar and sl_touched:
                        dyn_slip = self.taker_slippage + 0.10 * (bar_range / atr) * self.taker_slippage
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
                        total_trade_fees = pos.total_entry_fee + pos.tp1_fee + fee_sl
                        exit_label = "BE_SL" if pos.early_be_triggered else "STOP_LOSS"

                        trades.append(
                            TradeRecord(
                                trade_id=pos.position_id,
                                symbol=pos.symbol,
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
                                entry_fee=pos.total_entry_fee,
                                tp1_fee=pos.tp1_fee,
                                exit_fee=fee_sl,
                                total_fees=total_trade_fees,
                                total_slippage=slip,
                                priority=pos.priority,
                                metadata=pos.metadata,
                            ).to_dict()
                        )
                        closed_symbols.append(sym)
                        closed = True

                    # 1D. Early BE Check: when MFE >= 0.7R, move SL to Entry ± 0.15 * ATR
                    if not closed and not pos.early_be_triggered:
                        stop_dist = abs(pos.entry_price - pos.stop_loss)
                        mfe_threshold = self.early_be_mfe_r * stop_dist
                        if pos.side == PositionSide.LONG and (high - pos.entry_price) >= mfe_threshold:
                            pos.stop_loss = pos.entry_price + self.early_be_buffer_atr * atr
                            pos.early_be_triggered = True
                        elif pos.side == PositionSide.SHORT and (pos.entry_price - low) >= mfe_threshold:
                            pos.stop_loss = pos.entry_price - self.early_be_buffer_atr * atr
                            pos.early_be_triggered = True

            # Release closed positions
            for sym in closed_symbols:
                if sym in active_positions:
                    del active_positions[sym]

            # -----------------------------------------------------------------
            # STEP 2: Process Pending Limit Orders (Pessimistic Penetration Check)
            # -----------------------------------------------------------------
            filled_pending = []
            expired_pending = []
            for sym, pending in list(pending_orders.items()):
                sym_row_idx = idx_maps[sym][t_idx]
                if sym_row_idx == -1:
                    continue  # Asset not active on this timestamp

                pending.bars_elapsed += 1
                if pending.is_expired():
                    expired_pending.append(sym)
                    continue

                # Concurrency check before fill: active positions cannot exceed max_concurrent_positions
                if len(active_positions) >= self.max_concurrent_positions:
                    # Concurrency is full, cannot fill this bar
                    continue

                sym_arr = arrays[sym]
                high = sym_arr["high"][sym_row_idx]
                low = sym_arr["low"][sym_row_idx]
                atr = max(sym_arr["atr"][sym_row_idx], 1e-6)

                penetration = self.penetration_atr_mult * atr
                filled = False
                if pending.side == OrderSide.BUY:
                    if low <= (pending.limit_price - penetration):
                        filled = True
                elif pending.side == OrderSide.SELL:
                    if high >= (pending.limit_price + penetration):
                        filled = True

                if filled:
                    exec_price = pending.limit_price
                    # Maker fee: 0.02%, 0.00% slippage
                    entry_fee = pending.size * exec_price * self.maker_fee
                    total_fees += entry_fee
                    cash -= entry_fee
                    equity -= entry_fee

                    just_entered_symbols.add(sym)
                    active_positions[sym] = ActivePosition(
                        position_id=pending.order_id,
                        symbol=sym,
                        side=PositionSide.LONG if pending.side == OrderSide.BUY else PositionSide.SHORT,
                        entry_price=exec_price,
                        entry_time=current_time,
                        entry_idx=t_idx,
                        initial_size=pending.size,
                        remaining_size=pending.size,
                        allocated_margin=pending.allocated_margin,
                        stop_loss=pending.stop_loss,
                        tp1=pending.tp1,
                        tp2=pending.tp2,
                        tp1_hit=False,
                        realized_tp1_pnl=0.0,
                        early_be_triggered=False,
                        total_entry_fee=entry_fee,
                        tp1_fee=0.0,
                        priority=pending.priority,
                        metadata=pending.metadata,
                    )
                    filled_pending.append(sym)

            for sym in filled_pending:
                del pending_orders[sym]
            for sym in expired_pending:
                del pending_orders[sym]

            # -----------------------------------------------------------------
            # STEP 3: Multi-Asset Opportunistic Priority Signal Dispatch
            # -----------------------------------------------------------------
            # Candidate signals collection across all symbols on bar t
            candidate_signals = []

            # Check if this bar satisfies eval_start_time
            allow_new_entries = eval_start_time is None or current_time >= eval_start_time

            if allow_new_entries:
                for sym, sym_arr in arrays.items():
                    # Skip if symbol already has active position or pending limit order
                    if sym in active_positions or sym in pending_orders:
                        continue

                    sym_row_idx = idx_maps[sym][t_idx]
                    if sym_row_idx == -1:
                        continue

                    sig = sym_arr["signal"][sym_row_idx] if sym_arr["signal"] is not None else None
                    if sig in ("LONG", "SHORT", 1, -1, CredalSignal.BULLISH, CredalSignal.BEARISH):
                        is_long = sig in ("LONG", 1, CredalSignal.BULLISH)

                        # Credal gate check
                        row_series = sym_arr["df"].iloc[sym_row_idx]
                        credal_allowed, credal_decision = self.evaluate_credal_gate(row_series)
                        if not credal_allowed:
                            skipped_due_to_credal += 1
                            continue

                        # Limit price at 50% retracement of OB/FVG zone
                        close_px = sym_arr["close"][sym_row_idx]
                        high_px = sym_arr["high"][sym_row_idx]
                        low_px = sym_arr["low"][sym_row_idx]
                        atr_val = max(sym_arr["atr"][sym_row_idx], 1e-6)

                        if sym_arr["limit_entry_px"] is not None and not np.isnan(sym_arr["limit_entry_px"][sym_row_idx]):
                            limit_px = float(sym_arr["limit_entry_px"][sym_row_idx])
                        else:
                            limit_px = (close_px - 0.2 * atr_val) if is_long else (close_px + 0.2 * atr_val)

                        # Enforce resting limit order
                        if is_long:
                            limit_px = min(close_px, limit_px)
                        else:
                            limit_px = max(close_px, limit_px)

                        # Stop loss & TP levels
                        if sym_arr["stop_loss"] is not None and not np.isnan(sym_arr["stop_loss"][sym_row_idx]):
                            sl_val = float(sym_arr["stop_loss"][sym_row_idx])
                        else:
                            sl_val = (limit_px - 1.5 * atr_val) if is_long else (limit_px + 1.5 * atr_val)

                        stop_dist = abs(limit_px - sl_val)
                        if stop_dist <= 0.0 or stop_dist > limit_px * 0.20:
                            continue

                        if sym_arr["tp1"] is not None and not np.isnan(sym_arr["tp1"][sym_row_idx]):
                            tp1_val = float(sym_arr["tp1"][sym_row_idx])
                        else:
                            tp1_val = (limit_px + self.rr_tp1 * stop_dist) if is_long else (limit_px - self.rr_tp1 * stop_dist)

                        if sym_arr["tp2"] is not None and not np.isnan(sym_arr["tp2"][sym_row_idx]):
                            tp2_val = float(sym_arr["tp2"][sym_row_idx])
                        else:
                            tp2_val = (limit_px + self.rr_tp2 * stop_dist) if is_long else (limit_px - self.rr_tp2 * stop_dist)

                        # Calculate Priority = (1.0 - u) * AlphaGPT_Confluence_Score
                        priority_val, u_val, conf_score = self.calculate_priority(
                            row=row_series,
                            signal_val=sig,
                            credal_decision=credal_decision,
                        )

                        candidate_signals.append({
                            "symbol": sym,
                            "side": OrderSide.BUY if is_long else OrderSide.SELL,
                            "limit_px": limit_px,
                            "sl_val": sl_val,
                            "tp1_val": tp1_val,
                            "tp2_val": tp2_val,
                            "stop_dist": stop_dist,
                            "priority": priority_val,
                            "u": u_val,
                            "confluence_score": conf_score,
                            "credal_decision": credal_decision,
                        })

            # Sort candidate signals by priority descending
            if candidate_signals:
                candidate_signals.sort(key=lambda x: x["priority"], reverse=True)

                # Available concurrency capacity
                available_slots = max(0, self.max_concurrent_positions - len(active_positions) - len(pending_orders))

                for i, cand in enumerate(candidate_signals):
                    if available_slots <= 0:
                        skipped_due_to_capacity += 1
                        continue

                    sym = cand["symbol"]
                    limit_px = cand["limit_px"]
                    sl_val = cand["sl_val"]

                    # Compute currently allocated capital across active + pending
                    current_allocated = sum(
                        p.remaining_size * p.entry_price for p in active_positions.values()
                    ) + sum(o.size * o.limit_price for o in pending_orders.values())

                    # Calculate position size with compounding and liquidity reserve
                    order_size = self.calculate_position_size(
                        equity=max(cash, 10.0),
                        entry_price=limit_px,
                        stop_loss_price=sl_val,
                        current_allocated=current_allocated,
                    )

                    if order_size <= 0.0:
                        skipped_due_to_liquidity += 1
                        continue

                    # Place pending limit order
                    order_counter += 1
                    available_slots -= 1

                    meta = {
                        "priority": cand["priority"],
                        "credal_uncertainty": cand["u"],
                        "confluence_score": cand["confluence_score"],
                    }

                    pending_orders[sym] = PendingLimitOrder(
                        order_id=f"ORD_R4_{sym}_{order_counter:06d}",
                        symbol=sym,
                        side=cand["side"],
                        limit_price=limit_px,
                        size=order_size,
                        allocated_margin=order_size * limit_px,
                        stop_loss=sl_val,
                        tp1=cand["tp1_val"],
                        tp2=cand["tp2_val"],
                        placed_idx=t_idx,
                        placed_time=current_time,
                        expiry_bars=self.limit_order_expiry_bars,
                        priority=cand["priority"],
                        bars_elapsed=0,
                        metadata=meta,
                    )

            # -----------------------------------------------------------------
            # STEP 4: Mark to Market Equity Tracking & Concurrency Recording
            # -----------------------------------------------------------------
            unrealized_total = 0.0
            for sym, pos in active_positions.items():
                sym_row_idx = idx_maps[sym][t_idx]
                if sym_row_idx != -1:
                    close_p = arrays[sym]["close"][sym_row_idx]
                else:
                    close_p = pos.entry_price

                if pos.side == PositionSide.LONG:
                    unrealized = pos.remaining_size * (close_p - pos.entry_price) - (
                        pos.remaining_size * close_p * self.taker_fee
                    )
                else:
                    unrealized = pos.remaining_size * (pos.entry_price - close_p) - (
                        pos.remaining_size * close_p * self.taker_fee
                    )
                unrealized_total += unrealized

            current_equity = cash + unrealized_total
            equity_curve.append(current_equity)
            cash_curve.append(cash)

            cur_concurrent = len(active_positions)
            active_positions_history.append(cur_concurrent)
            max_concurrent_observed = max(max_concurrent_observed, cur_concurrent)
            min_cash_observed = min(min_cash_observed, cash)
            min_equity_observed = min(min_equity_observed, current_equity)

        # ---------------------------------------------------------------------
        # STEP 5: Liquidation on Final Bar (Close remaining active positions)
        # ---------------------------------------------------------------------
        for sym, pos in list(active_positions.items()):
            final_close = arrays[sym]["close"][-1]
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
            total_trade_fees = pos.total_entry_fee + pos.tp1_fee + fee_last

            trades.append(
                TradeRecord(
                    trade_id=pos.position_id,
                    symbol=pos.symbol,
                    direction=pos.side.value,
                    entry_time=pos.entry_time,
                    exit_time=all_timestamps[-1],
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
                    entry_fee=pos.total_entry_fee,
                    tp1_fee=pos.tp1_fee,
                    exit_fee=fee_last,
                    total_fees=total_trade_fees,
                    total_slippage=slip_last,
                    priority=pos.priority,
                    metadata=pos.metadata,
                ).to_dict()
            )

        active_positions.clear()
        pending_orders.clear()

        metrics = self._calculate_metrics(
            trades=trades,
            equity_curve=equity_curve,
            final_cash=cash,
            total_fees=total_fees,
            total_slippage=total_slippage,
            skipped_due_to_capacity=skipped_due_to_capacity,
            skipped_due_to_liquidity=skipped_due_to_liquidity,
            skipped_due_to_credal=skipped_due_to_credal,
            max_concurrent_observed=max_concurrent_observed,
            min_cash_observed=min_cash_observed,
            min_equity_observed=min_equity_observed,
        )

        return {
            "trades": trades,
            "metrics": metrics,
            "equity_curve": equity_curve,
            "cash_curve": cash_curve,
            "active_positions_history": active_positions_history,
        }

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "trades": [],
            "metrics": {
                "initial_cash": self.initial_cash,
                "final_cash": self.initial_cash,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate_pct": 0.0,
                "total_return_pct": 0.0,
                "profit_factor": 0.0,
                "max_drawdown_pct": 0.0,
                "sharpe_ratio": 0.0,
                "total_fees": 0.0,
                "total_slippage": 0.0,
                "maker_fill_ratio": 0.0,
                "skipped_due_to_capacity": 0,
                "skipped_due_to_liquidity": 0,
                "skipped_due_to_credal": 0,
                "max_concurrent_positions_observed": 0,
                "min_cash_observed": self.initial_cash,
                "min_equity_observed": self.initial_cash,
            },
            "equity_curve": [self.initial_cash],
            "cash_curve": [self.initial_cash],
            "active_positions_history": [0],
        }

    def _calculate_metrics(
        self,
        trades: List[Dict[str, Any]],
        equity_curve: List[float],
        final_cash: float,
        total_fees: float,
        total_slippage: float,
        skipped_due_to_capacity: int,
        skipped_due_to_liquidity: int,
        skipped_due_to_credal: int,
        max_concurrent_observed: int,
        min_cash_observed: float,
        min_equity_observed: float,
    ) -> Dict[str, Any]:
        total_trades = len(trades)
        if total_trades == 0:
            res = self._empty_result()["metrics"]
            res["final_cash"] = final_cash
            res["skipped_due_to_capacity"] = skipped_due_to_capacity
            res["skipped_due_to_liquidity"] = skipped_due_to_liquidity
            res["skipped_due_to_credal"] = skipped_due_to_credal
            res["max_concurrent_positions_observed"] = max_concurrent_observed
            res["min_cash_observed"] = min_cash_observed
            res["min_equity_observed"] = min_equity_observed
            return res

        pnls = [t["pnl"] for t in trades]
        winning = [p for p in pnls if p > 0]
        losing = [p for p in pnls if p < 0]

        win_rate = (len(winning) / total_trades) * 100.0
        tot_profit = sum(winning)
        tot_loss = abs(sum(losing))

        if tot_loss > 0:
            profit_factor = tot_profit / tot_loss
        elif tot_profit > 0:
            profit_factor = 999.0
        else:
            profit_factor = 0.0

        total_return_pct = ((final_cash - self.initial_cash) / self.initial_cash) * 100.0

        # Max drawdown
        eq = np.array(equity_curve)
        cummax = np.maximum.accumulate(eq)
        drawdowns = (cummax - eq) / np.maximum(cummax, 1e-6)
        max_dd_pct = float(np.max(drawdowns)) * 100.0 if len(drawdowns) > 0 else 0.0

        # Sharpe ratio
        trade_returns = [t["pnl_pct"] / 100.0 for t in trades]
        if len(trade_returns) > 1:
            mean_ret = np.mean(trade_returns)
            std_ret = np.std(trade_returns, ddof=1)
            sharpe = float((mean_ret / std_ret) * np.sqrt(252)) if std_ret > 0 else 0.0
        else:
            sharpe = 0.0

        maker_count = sum(1 for t in trades if t.get("exit_reason") in ("TP1", "TP2"))
        maker_ratio = maker_count / total_trades if total_trades > 0 else 0.0

        return {
            "initial_cash": round(self.initial_cash, 2),
            "final_cash": float(final_cash),
            "total_trades": total_trades,
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "win_rate_pct": round(win_rate, 2),
            "total_return_pct": round(total_return_pct, 2),
            "profit_factor": round(profit_factor, 3),
            "max_drawdown_pct": round(max_dd_pct, 2),
            "sharpe_ratio": round(sharpe, 3),
            "total_fees": round(total_fees, 4),
            "total_slippage": round(total_slippage, 4),
            "maker_fill_ratio": round(maker_ratio, 3),
            "skipped_due_to_capacity": skipped_due_to_capacity,
            "skipped_due_to_liquidity": skipped_due_to_liquidity,
            "skipped_due_to_credal": skipped_due_to_credal,
            "max_concurrent_positions_observed": max_concurrent_observed,
            "min_cash_observed": round(min_cash_observed, 4),
            "min_equity_observed": round(min_equity_observed, 4),
        }


def run_round4_portfolio_simulation(
    symbols: Sequence[str] = ("BTC", "ETH", "SOL", "BNB", "NEAR", "AAPL"),
    years: Sequence[int] = (2021, 2022, 2023, 2024, 2025),
    timeframes: Sequence[str] = ("15m", "1h"),
    initial_cash: float = 10000.0,
    output_dir: str = "results/round4_portfolio",
) -> pd.DataFrame:
    """
    Run full industrial cross-asset portfolio walk-forward backtests across all assets.
    Saves trade history JSONs and shared_portfolio_summary.csv.
    """
    from backtest_core import load_symbol_timeframe_data
    from src.qlib_smc_alpha import compute_qlib_smc_alpha
    from src.alphagpt_factor_miner import compute_alphagpt_factors

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    trades_dir = out_path / "trades"
    trades_dir.mkdir(parents=True, exist_ok=True)

    summary_records = []
    all_trades_corpus = []

    for tf in timeframes:
        # Load raw data for all symbols
        raw_dfs: Dict[str, pd.DataFrame] = {}
        for sym in symbols:
            try:
                raw_dfs[sym] = load_symbol_timeframe_data(sym, tf)
                logger.info(f"Loaded {sym} {tf} ({len(raw_dfs[sym])} bars)")
            except Exception as e:
                logger.warning(f"Could not load data for {sym} {tf}: {e}")

        for year in years:
            # Prepare pre-computed alpha for In-Sample and Out-of-Sample per symbol
            is_dfs: Dict[str, pd.DataFrame] = {}
            oos_dfs: Dict[str, pd.DataFrame] = {}
            oos_eval_start_times: Dict[str, pd.Timestamp] = {}

            # Calculate calendar natural-year 80/20 split
            start_year = pd.Timestamp(f"{year}-01-01 00:00:00")
            end_year = pd.Timestamp(f"{year}-12-31 23:59:59")
            split_ts = start_year + pd.Timedelta(days=int(365.25 * 0.8))

            for sym, full_df in raw_dfs.items():
                ydf = full_df[(full_df.index >= start_year) & (full_df.index <= end_year)]
                if len(ydf) < 20:
                    continue

                # 1. In-Sample slice: bars < split_ts
                is_raw = ydf[ydf.index < split_ts]
                if len(is_raw) >= 10:
                    try:
                        alpha_is = compute_qlib_smc_alpha(is_raw)
                        agpt_is = compute_alphagpt_factors(is_raw)
                        for c in ["OFI_Impulse", "FVG_Absorption_Rate", "Liquidity_Sweep_Intensity", "Vol_Displacement_Ratio"]:
                            if c in agpt_is.columns:
                                alpha_is[c] = agpt_is[c]
                        is_dfs[sym] = alpha_is
                    except Exception as e:
                        logger.warning(f"Error computing IS alpha for {sym} {year}: {e}")

                # 2. Out-of-Sample slice with 200-bar warmup prior to split_ts
                # Locate split_ts index in full_df
                prior_bars = full_df[full_df.index < split_ts]
                warmup_bars = 200
                warmup_start_idx = max(0, len(prior_bars) - warmup_bars)
                warmup_start_ts = prior_bars.index[warmup_start_idx] if len(prior_bars) > 0 else split_ts

                oos_raw = full_df[(full_df.index >= warmup_start_ts) & (full_df.index <= end_year)]
                if len(oos_raw) > 20:
                    try:
                        alpha_oos = compute_qlib_smc_alpha(oos_raw)
                        agpt_oos = compute_alphagpt_factors(oos_raw)
                        for c in ["OFI_Impulse", "FVG_Absorption_Rate", "Liquidity_Sweep_Intensity", "Vol_Displacement_Ratio"]:
                            if c in agpt_oos.columns:
                                alpha_oos[c] = agpt_oos[c]
                        oos_dfs[sym] = alpha_oos
                        oos_eval_start_times[sym] = split_ts
                    except Exception as e:
                        logger.warning(f"Error computing OOS alpha for {sym} {year}: {e}")

            # Run In-Sample and Out-of-Sample simulations
            for sample_type, sample_dfs, eval_start in [
                ("In-Sample", is_dfs, None),
                ("Out-of-Sample", oos_dfs, split_ts),
            ]:
                if not sample_dfs:
                    continue

                engine = SMCSharedPortfolioEngine(
                    initial_cash=initial_cash,
                    max_concurrent_positions=2,
                    liquidity_reserve_pct=0.50,
                    risk_pct=1.0,
                    use_compound=True,
                    use_credal=True,
                    credal_u_max=0.35,
                    pessimistic_intra_bar=True,
                )

                res = engine.run(sample_dfs, eval_start_time=eval_start)
                m = res["metrics"]
                trades_list = res["trades"]

                # Save trade JSON
                trade_filename = f"shared_portfolio_{tf}_{year}_{sample_type.lower().replace('-', '_')}_trades.json"
                trade_path = trades_dir / trade_filename
                with open(trade_path, "w") as fp:
                    json.dump(trades_list, fp, indent=2)

                all_trades_corpus.extend(trades_list)

                record = {
                    "capital_model": "Shared_Portfolio_Capital",
                    "timeframe": tf,
                    "year": year,
                    "sample_type": sample_type,
                    "symbols": "+".join(sorted(sample_dfs.keys())),
                    "initial_capital": initial_cash,
                    "final_equity": m["final_cash"],
                    "total_trades": m["total_trades"],
                    "winning_trades": m["winning_trades"],
                    "losing_trades": m["losing_trades"],
                    "win_rate_pct": m["win_rate_pct"],
                    "total_return_pct": m["total_return_pct"],
                    "profit_factor": m["profit_factor"],
                    "max_drawdown_pct": m["max_drawdown_pct"],
                    "sharpe_ratio": m["sharpe_ratio"],
                    "total_fees": m["total_fees"],
                    "total_slippage": m["total_slippage"],
                    "skipped_due_to_capacity": m["skipped_due_to_capacity"],
                    "skipped_due_to_liquidity": m["skipped_due_to_liquidity"],
                    "skipped_due_to_credal": m["skipped_due_to_credal"],
                    "max_concurrent_positions": m["max_concurrent_positions_observed"],
                    "min_cash_observed": m["min_cash_observed"],
                    "min_equity_observed": m["min_equity_observed"],
                    "trade_file": str(trade_path),
                }
                summary_records.append(record)
                logger.info(
                    f"[{sample_type} {tf} {year}] Trades: {m['total_trades']}, "
                    f"WinRate: {m['win_rate_pct']}%, Ret: {m['total_return_pct']:+.2f}%, "
                    f"MDD: {m['max_drawdown_pct']}%, SkippedCap: {m['skipped_due_to_capacity']}"
                )

        gc.collect()

    summary_df = pd.DataFrame(summary_records)
    summary_csv_path = out_path / "shared_portfolio_summary.csv"
    summary_df.to_csv(summary_csv_path, index=False)
    logger.info(f"Saved shared portfolio summary to {summary_csv_path}")

    # Save complete trade corpus
    with open(out_path / "shared_portfolio_all_trades.json", "w") as fp:
        json.dump(all_trades_corpus, fp, indent=2)

    return summary_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    run_round4_portfolio_simulation()
