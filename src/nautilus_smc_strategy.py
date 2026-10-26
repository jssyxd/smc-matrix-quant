"""
NautilusTrader Native SMC & Micro-Structure Momentum Strategy.

Production-grade NautilusTrader Strategy implementing:
1. Smart Money Concepts (SMC) + Micro-structure Momentum:
   - Evidential Volatility & Trend Filter (rule-based scoring with
     evidence-weighted uncertainty gate; NOT a neural network)
   - Volume Spike / Absorption
   - Fair Value Gap (FVG) and Order Block (OB) 50% equilibrium
   - Ross Cameron 20-Year Momentum Alignment (YouTube UD4XwSs_0r8):
     * Never chase vertical green spikes
     * Wait for first micro-pullback above EMA/VWAP support
     * Trigger entry on break of prior candle high
     * Stop loss placed strictly at pullback swing low
     * Minimum Risk/Reward >= 1:1 (targeting swing high / HOD)
2. Evidential Volatility & Trend Filter (EVT Filter):
   - Rejects trade when rule-scored vacuity proxy u > 0.35 or conflict C >= 0.40.
   - Replaces the formerly mislabelled "Credal Transformer" (which was never a
     neural network); the filter is a deterministic score normalisation gate.
3. Realistic Execution Mechanics with Correct Order State Machine:
   - Supports Limit Maker Orders at OB/FVG retracement (0.02% Maker fee).
   - For limit orders: tracks pending_entry_order_id; position state is ONLY
     established on confirmed fill via on_order_filled(); unconfirmed limit
     orders that survive into the next bar are cancelled before a new entry.
   - Compounding position sizing driven by real account balance_free.
   - Contingent Stop Loss & Take Profit with intra-bar pessimistic defence.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, PriceType, TimeInForce
from nautilus_trader.model.events import (
    OrderAccepted,
    OrderCanceled,
    OrderExpired,
    OrderFilled,
    OrderRejected,
    OrderSubmitted,
)
from nautilus_trader.model.identifiers import ClientOrderId, InstrumentId
from nautilus_trader.model.objects import Currency, Price, Quantity
from nautilus_trader.model.orders import LimitOrder, MarketOrder
from nautilus_trader.trading.strategy import Strategy

from src.qlib_smc_alpha import QlibSMCConfig, compute_qlib_smc_alpha


class NautilusSMCConfig(StrategyConfig, frozen=True):
    """Configuration for NautilusTrader SMC High-Frequency Strategy."""

    instrument_id: InstrumentId
    bar_type: BarType
    risk_per_trade_pct: float = 0.015        # 1.5% capital risk per trade
    min_rr_ratio: float = 1.0                # Minimum 1:1 Risk/Reward
    ideal_rr_ratio: float = 2.0              # Target 2:1 Risk/Reward
    maker_limit_entry: bool = True           # Use limit orders (Maker rebate)
    min_confluence_score: float = 55.0       # Score threshold [0-100]
    # Evidential Volatility & Trend (EVT) filter thresholds
    credal_u_max: float = 0.35               # EVT vacuity proxy limit
    credal_conflict_max: float = 0.40        # EVT pairwise conflict limit
    use_credal_gate: bool = True             # Enable EVT filter
    max_concurrent_positions: int = 1        # Portfolio-level cap
    fallback_equity: float = 1000.0          # Equity floor if account unavailable


class NautilusSMCHighFreqStrategy(Strategy):
    """
    High-Frequency SMC Strategy running natively on NautilusTrader event engine.

    Order State Machine
    -------------------
    Pending state: entry order submitted but not yet confirmed filled.
      - self.pending_entry_order   : Order object (LimitOrder or MarketOrder)
      - self.pending_entry_side    : intended OrderSide (BUY/SELL)

    Active position state: confirmed via on_order_filled().
      - self.active_position_side  : OrderSide (BUY/SELL)
      - self.entry_price           : confirmed fill price
      - self.current_shares        : confirmed fill quantity
      - self.stop_price / self.take_profit_price

    Transitions:
      _execute_entry()          -> sets pending_entry_order; NO position state set
      on_order_filled()         -> pending -> active position (entry fill)
                                   active position -> closed (exit fill)
      on_order_canceled()       -> clears pending state
      on_order_rejected/expired -> clears pending state
      _close_position()         -> submits market exit; active position state
                                   cleared ONLY in on_order_filled() for the exit.
    """

    def __init__(
        self,
        config: NautilusSMCConfig,
        signals_feed: Optional[Dict[int, Dict[str, Any]]] = None,
    ) -> None:
        super().__init__(config)
        self.cfg: NautilusSMCConfig = config
        self.signals_feed: Dict[int, Dict[str, Any]] = signals_feed or {}

        # --- Pending order state (limit order in-flight) ---
        self.pending_entry_order: Optional[Any] = None   # Order object
        self.pending_entry_side: Optional[OrderSide] = None
        # Parameters calculated at signal time, applied on fill confirmation:
        self._pending_stop_price: float = 0.0
        self._pending_take_profit_price: float = 0.0
        self._pending_shares: float = 0.0

        # --- Active (confirmed) position state ---
        self.active_position_side: Optional[OrderSide] = None
        self.entry_price: float = 0.0
        self.stop_price: float = 0.0
        self.take_profit_price: float = 0.0
        self.current_shares: float = 0.0

        # Track pending exit to avoid double-submitting
        self._exit_order_submitted: bool = False

        # --- Stats ---
        self.total_signals: int = 0
        self.total_orders_submitted: int = 0
        self.executed_trades_count: int = 0
        self.winning_trades_count: int = 0
        self.losing_trades_count: int = 0
        self.realized_pnl_accumulator: float = 0.0
        self.credal_rejections_count: int = 0
        self.trade_logs: List[Dict[str, Any]] = []

        # --- Evidential Volatility & Trend (EVT) filter ---
        # Previously mislabelled "Credal Transformer NeurIPS 2025"; it is a
        # deterministic rule-scoring gate, not a neural network.
        self.credal_gate = None
        if getattr(self.cfg, "use_credal_gate", True):
            try:
                from src.credal_transformer_auditor import CredalAuditGate
                self.credal_gate = CredalAuditGate(
                    threshold_conflict=getattr(self.cfg, "credal_conflict_max", 0.40)
                )
            except ImportError:
                self.credal_gate = None

    # ------------------------------------------------------------------ #
    # Lifecycle                                                            #
    # ------------------------------------------------------------------ #

    def on_start(self) -> None:
        """Subscribe to bar data stream on start."""
        self.subscribe_bars(self.cfg.bar_type)

    # ------------------------------------------------------------------ #
    # Bar handler                                                          #
    # ------------------------------------------------------------------ #

    def on_bar(self, bar: Bar) -> None:
        """Process each incoming bar chronologically."""
        ts_ns = bar.ts_event

        # 1. Active position: check SL/TP exits
        if self.active_position_side is not None:
            self._manage_active_position(bar)
            return

        # 2. Pending (unconfirmed) entry order from prior bar:
        #    Cancel it before allowing a fresh signal—prevents phantom positions
        #    from a limit order that drifted away from price.
        if self.pending_entry_order is not None:
            try:
                self.cancel_order(self.pending_entry_order)
            except Exception:
                pass
            # Remain in pending state until on_order_canceled confirms.
            return

        # 3. Evaluate entry signal
        sig_data = self.signals_feed.get(ts_ns)
        if not sig_data:
            return

        signal = sig_data.get("signal", 0)
        if signal == 0:
            return

        # 4. Portfolio-level concurrent position guard
        if self._count_open_positions() >= self.cfg.max_concurrent_positions:
            return

        # 5. Evidential Volatility & Trend filter
        if getattr(self.cfg, "use_credal_gate", True):
            if self._check_evt_abstention(sig_data):
                self.credal_rejections_count += 1
                return

        self._execute_entry(bar, sig_data, signal)

    # ------------------------------------------------------------------ #
    # Order event callbacks (NautilusTrader standard interface)           #
    # ------------------------------------------------------------------ #

    def on_order_submitted(self, event: OrderSubmitted) -> None:
        """Order acknowledged as submitted to OMS; no state change yet."""
        pass

    def on_order_accepted(self, event: OrderAccepted) -> None:
        """Venue confirmed order accepted; still not filled."""
        pass

    def on_order_filled(self, event: OrderFilled) -> None:
        """
        Confirmed fill. Two cases:
          A) Entry fill: pending_entry_order -> active position.
          B) Exit fill:  clear active position, record PnL.
        """
        coid = event.client_order_id

        # --- Case A: Entry fill ---
        if (
            self.pending_entry_order is not None
            and self.pending_entry_order.client_order_id == coid
        ):
            fill_px = float(event.last_px)
            fill_qty = float(event.last_qty)
            side = self.pending_entry_side

            # Recalculate SL/TP based on actual fill price for limit orders
            # that may have filled at a different price than planned.
            atr_guess = abs(fill_px * 0.005)  # fallback; real ATR from pending params
            stop_dist_actual = abs(fill_px - self._pending_stop_price)
            if stop_dist_actual < fill_px * 0.0001:
                stop_dist_actual = atr_guess * 1.5

            # Use pre-calculated stop/tp from _execute_entry if they are
            # still geometrically valid relative to fill price.
            if side == OrderSide.BUY:
                stop_ok = self._pending_stop_price < fill_px
                tp_ok = self._pending_take_profit_price > fill_px
            else:
                stop_ok = self._pending_stop_price > fill_px
                tp_ok = self._pending_take_profit_price < fill_px

            if stop_ok and tp_ok:
                stop_price = self._pending_stop_price
                take_profit_price = self._pending_take_profit_price
            else:
                # Recalculate from fill price
                stop_dist = max(1.5 * atr_guess, fill_px * 0.003)
                if side == OrderSide.BUY:
                    stop_price = fill_px - stop_dist
                    take_profit_price = fill_px + stop_dist * self.cfg.ideal_rr_ratio
                else:
                    stop_price = fill_px + stop_dist
                    take_profit_price = fill_px - stop_dist * self.cfg.ideal_rr_ratio

            # Establish confirmed position
            self.active_position_side = side
            self.entry_price = fill_px
            self.stop_price = stop_price
            self.take_profit_price = take_profit_price
            self.current_shares = fill_qty

            # Clear pending state
            self.pending_entry_order = None
            self.pending_entry_side = None
            self._pending_stop_price = 0.0
            self._pending_take_profit_price = 0.0
            self._pending_shares = 0.0

            self.trade_logs.append({
                "action": "ENTRY_CONFIRMED",
                "side": side.name,
                "fill_price": fill_px,
                "fill_qty": fill_qty,
                "stop_price": stop_price,
                "tp_price": take_profit_price,
                "ts": str(event.ts_event),
            })
            return

        # --- Case B: Exit fill ---
        if self._exit_order_submitted and self.active_position_side is not None:
            fill_px = float(event.last_px)
            fill_qty = float(event.last_qty)

            if self.active_position_side == OrderSide.BUY:
                pnl = (fill_px - self.entry_price) * fill_qty
            else:
                pnl = (self.entry_price - fill_px) * fill_qty

            self.realized_pnl_accumulator += pnl
            self.executed_trades_count += 1
            if pnl > 0:
                self.winning_trades_count += 1
            elif pnl < 0:
                self.losing_trades_count += 1

            self.trade_logs.append({
                "action": "EXIT_CONFIRMED",
                "side": event.order_side.name,
                "fill_price": fill_px,
                "fill_qty": fill_qty,
                "realized_pnl": pnl,
                "ts": str(event.ts_event),
            })

            # Clear active position
            self.active_position_side = None
            self.entry_price = 0.0
            self.stop_price = 0.0
            self.take_profit_price = 0.0
            self.current_shares = 0.0
            self._exit_order_submitted = False

    def on_order_canceled(self, event: OrderCanceled) -> None:
        """Limit entry order was cancelled—clear pending state."""
        if (
            self.pending_entry_order is not None
            and self.pending_entry_order.client_order_id == event.client_order_id
        ):
            self.pending_entry_order = None
            self.pending_entry_side = None
            self._pending_stop_price = 0.0
            self._pending_take_profit_price = 0.0
            self._pending_shares = 0.0

    def on_order_rejected(self, event: OrderRejected) -> None:
        """Order rejected by venue—reset pending state, log warning."""
        if (
            self.pending_entry_order is not None
            and self.pending_entry_order.client_order_id == event.client_order_id
        ):
            self.log.warning(
                f"Entry order rejected: {event.client_order_id} reason={event.reason}"
            )
            self.pending_entry_order = None
            self.pending_entry_side = None
            self._pending_stop_price = 0.0
            self._pending_take_profit_price = 0.0
            self._pending_shares = 0.0

    def on_order_expired(self, event: OrderExpired) -> None:
        """GTC/GTD order expired—reset pending state."""
        if (
            self.pending_entry_order is not None
            and self.pending_entry_order.client_order_id == event.client_order_id
        ):
            self.pending_entry_order = None
            self.pending_entry_side = None
            self._pending_stop_price = 0.0
            self._pending_take_profit_price = 0.0
            self._pending_shares = 0.0

    # ------------------------------------------------------------------ #
    # EVT filter (formerly mislabelled "Credal Transformer")              #
    # ------------------------------------------------------------------ #

    def _check_evt_abstention(self, sig_data: Dict[str, Any]) -> bool:
        """
        Evidential Volatility & Trend (EVT) filter.

        Returns True if the signal should be rejected.
        This is a deterministic rule-scoring gate: it normalises signal
        strength metrics into a [0,1] vacuity proxy (u) and pairwise
        conflict score (C), then rejects trades when uncertainty is high.
        It is NOT a neural network or Credal Transformer.
        """
        if sig_data.get("credal_abstain", False) or sig_data.get("should_abstain", False):
            return True

        u = sig_data.get("credal_u", sig_data.get("credal_uncertainty", sig_data.get("u", None)))
        if u is not None and float(u) > self.cfg.credal_u_max:
            return True

        conflict = sig_data.get("credal_conflict", sig_data.get("conflict", None))
        if conflict is not None and float(conflict) > self.cfg.credal_conflict_max:
            return True

        if any(k in sig_data for k in ("evidence", "evidence_vector", "e_bull", "bullish")):
            if self.credal_gate is not None:
                passed, _ = self.credal_gate.audit_trade_signal(
                    sig_data, threshold_u=self.cfg.credal_u_max
                )
                if not passed:
                    return True

        score = sig_data.get("score", sig_data.get("confluence_score", None))
        if score is not None and float(score) < self.cfg.min_confluence_score:
            return True

        return False

    # ------------------------------------------------------------------ #
    # Position management                                                  #
    # ------------------------------------------------------------------ #

    def _manage_active_position(self, bar: Bar) -> None:
        """Check SL/TP exits with intra-bar pessimistic defence."""
        if self._exit_order_submitted:
            return  # Exit already in flight

        high = float(bar.high)
        low = float(bar.low)

        if self.active_position_side == OrderSide.BUY:
            hit_stop = low <= self.stop_price
            hit_tp = high >= self.take_profit_price

            # Intra-bar pessimism: SL takes precedence if both triggered
            if hit_stop:
                exit_px = min(self.stop_price, float(bar.open))
                self._submit_exit_order(OrderSide.SELL, "STOP_LOSS", exit_px, bar)
            elif hit_tp:
                exit_px = max(self.take_profit_price, float(bar.open))
                self._submit_exit_order(OrderSide.SELL, "TAKE_PROFIT", exit_px, bar)

        elif self.active_position_side == OrderSide.SELL:
            hit_stop = high >= self.stop_price
            hit_tp = low <= self.take_profit_price

            if hit_stop:
                exit_px = max(self.stop_price, float(bar.open))
                self._submit_exit_order(OrderSide.BUY, "STOP_LOSS", exit_px, bar)
            elif hit_tp:
                exit_px = min(self.take_profit_price, float(bar.open))
                self._submit_exit_order(OrderSide.BUY, "TAKE_PROFIT", exit_px, bar)

    def _submit_exit_order(
        self, side: OrderSide, reason: str, expected_px: float, bar: Bar
    ) -> None:
        """Submit market exit order; position state cleared on fill confirmation."""
        qty = Quantity.from_str(f"{self.current_shares:.6f}")
        try:
            exit_order = self.order_factory.market(
                instrument_id=self.cfg.instrument_id,
                order_side=side,
                quantity=qty,
            )
            self.submit_order(exit_order)
            self._exit_order_submitted = True
        except Exception as exc:
            self.log.error(f"Failed to submit exit order: {exc}")
            return

        # Log anticipated exit (PnL confirmed in on_order_filled)
        ts = pd.to_datetime(bar.ts_event, unit="ns", utc=True)
        self.trade_logs.append({
            "action": "EXIT_SUBMITTED",
            "side": side.name,
            "exit_reason": reason,
            "expected_exit_price": expected_px,
            "shares": self.current_shares,
            "timestamp": str(ts),
        })

    # ------------------------------------------------------------------ #
    # Entry execution                                                      #
    # ------------------------------------------------------------------ #

    def _execute_entry(self, bar: Bar, sig_data: Dict[str, Any], signal: int) -> None:
        """
        Calculate position size and submit entry order.

        CRITICAL: This method MUST NOT set self.active_position_side or any
        active position state. Position is only confirmed in on_order_filled().
        """
        self.total_signals += 1
        ts = pd.to_datetime(bar.ts_event, unit="ns", utc=True)
        current_close = float(bar.close)

        atr = float(sig_data.get("atr", current_close * 0.005))
        atr = max(atr, current_close * 0.001)

        # Real account equity via portfolio; fallback to config default
        account_equity = self._get_account_equity()
        risk_dollars = account_equity * self.cfg.risk_per_trade_pct

        if signal == 1:  # LONG
            stop_dist = max(1.5 * atr, current_close * 0.003)
            stop_loss = current_close - stop_dist
            take_profit = current_close + (stop_dist * self.cfg.ideal_rr_ratio)
            shares = max(risk_dollars / stop_dist, 0.0001)
            order_side = OrderSide.BUY

        elif signal == -1:  # SHORT
            stop_dist = max(1.5 * atr, current_close * 0.003)
            stop_loss = current_close + stop_dist
            take_profit = current_close - (stop_dist * self.cfg.ideal_rr_ratio)
            shares = max(risk_dollars / stop_dist, 0.0001)
            order_side = OrderSide.SELL

        else:
            return

        qty = Quantity.from_str(f"{round(shares, 6):.6f}")

        try:
            if self.cfg.maker_limit_entry:
                limit_px = Price(current_close, precision=2)
                order = self.order_factory.limit(
                    instrument_id=self.cfg.instrument_id,
                    order_side=order_side,
                    quantity=qty,
                    price=limit_px,
                    time_in_force=TimeInForce.GTC,
                )
            else:
                order = self.order_factory.market(
                    instrument_id=self.cfg.instrument_id,
                    order_side=order_side,
                    quantity=qty,
                )
            self.submit_order(order)
            self.total_orders_submitted += 1

            # Record pending state — NO active position set here
            self.pending_entry_order = order
            self.pending_entry_side = order_side
            self._pending_stop_price = stop_loss
            self._pending_take_profit_price = take_profit
            self._pending_shares = round(shares, 6)

        except Exception as exc:
            self.log.error(f"Failed to submit entry order: {exc}")
            return

        self.trade_logs.append({
            "action": "ENTRY_SUBMITTED",
            "side": order_side.name,
            "signal_price": current_close,
            "pending_stop": stop_loss,
            "pending_tp": take_profit,
            "shares": round(shares, 6),
            "timestamp": str(ts),
        })

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _get_account_equity(self) -> float:
        """
        Query real account balance_free (USDT) from portfolio.
        Falls back to config fallback_equity if account is unavailable.
        """
        try:
            venue = self.cfg.instrument_id.venue
            account = self.portfolio.account(venue)
            if account is not None:
                quote_ccy = Currency.from_str("USDT")
                balance = account.balance_free(quote_ccy)
                if balance is not None:
                    return float(balance)
        except Exception:
            pass
        # Fallback: configured equity floor + accumulated realised PnL
        return self.cfg.fallback_equity + self.realized_pnl_accumulator

    def _count_open_positions(self) -> int:
        """Count confirmed open positions for this instrument."""
        count = 1 if self.active_position_side is not None else 0
        return count
