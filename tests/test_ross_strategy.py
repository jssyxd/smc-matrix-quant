"""
Unit Tests for Ross Cameron Momentum Strategy and Execution Engine.
Verifies all 5 required specifications:
1. First pullback entry trigger, sizing, and R/R check.
2. Stop loss placement and 50% TP1 halving at HOD with Early BE buffer.
3. 5 Exit signal triggers (Ask Wall, Iceberg, Tape Selling, Topping Tail, Volume Divergence).
4. 5 Walk-Away Rules enforcement.
5. Double-entry balance conservation and pessimistic intra-bar execution.
"""

import unittest
import math
import datetime
from typing import Tuple, List, Dict, Optional, Any
import pandas as pd
import numpy as np

from src.ross_momentum_strategy import (
    RossMomentumStrategy,
    StrategyConfig,
    RossPosition,
    ExitSignalType,
    WalkAwayReason,
    enrich_ross_indicators,
)
from src.ross_execution_engine import (
    RossExecutionEngine,
    ExecutionConfig,
    TradeExecutionRecord,
)


class TestRossMomentumStrategy(unittest.TestCase):
    """Unit tests for Ross Momentum Strategy logic."""

    def setUp(self):
        self.config = StrategyConfig(
            risk_per_trade_pct=0.01,
            min_rr_ratio=1.0,
            ideal_rr_ratio=2.0,
            early_be_atr_buffer=0.15,
            min_pullback_bars=1,
            max_pullback_bars=5,
            daily_max_loss=200.0,
            peak_profit_retrace_pct=0.50,
            trading_cutoff_time="10:00:00",
        )
        self.strategy = RossMomentumStrategy(self.config)

    def _create_sample_spike_and_pullback(
        self,
        pullback_count: int = 2,
        hod_price: float = 12.00,
        pullback_low: float = 11.00,
        prev_bar_high: float = 11.40,
        breakout_high: float = 11.70,
        support_price: float = 10.80,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
        """Helper to create synthetic spike and pullback price action."""
        records = []
        # Bar 0: Base
        records.append({
            "timestamp": "09:30:00", "open": 10.00, "high": 10.50, "low": 9.90, "close": 10.40, "volume": 100000
        })
        # Bar 1: Vertical Surge / Spike to HOD
        records.append({
            "timestamp": "09:31:00", "open": 10.40, "high": hod_price, "low": 10.30, "close": 11.80, "volume": 500000
        })

        # Pullback bars
        for i in range(pullback_count):
            bar_high = hod_price - 0.20 - (i * 0.15)
            bar_low = pullback_low + (i * 0.05)
            records.append({
                "timestamp": f"09:3{2+i}:00",
                "open": bar_high,
                "high": bar_high,
                "low": bar_low,
                "close": bar_low + 0.10,
                "volume": 80000,
            })

        # Ensure last pullback bar has prev_bar_high
        records[-1]["high"] = prev_bar_high

        df = pd.DataFrame(records)
        df = enrich_ross_indicators(df)
        # Override support for controlled testing
        df['ema9'] = support_price
        df['vwap'] = support_price
        df['atr'] = 0.50

        # Trigger bar (breaks above prev_bar_high)
        trigger_bar = pd.Series({
            "timestamp": f"09:3{2+pullback_count}:00",
            "open": prev_bar_high - 0.05,
            "high": breakout_high,
            "low": prev_bar_high - 0.10,
            "close": breakout_high - 0.05,
            "volume": 200000,
            "ema9": support_price,
            "vwap": support_price,
            "atr": 0.50,
            "hod": hod_price,
        })
        prev_bar = df.iloc[-1]
        return df, trigger_bar, prev_bar

    # =========================================================================
    # 1. First Pullback Entry Trigger & Sizing
    # =========================================================================
    def test_first_pullback_entry_trigger(self):
        """Verify first pullback entry triggers immediately upon breaking previous candle high."""
        df_history, trigger_bar, prev_bar = self._create_sample_spike_and_pullback(
            pullback_count=2,
            hod_price=12.00,
            pullback_low=11.00,
            prev_bar_high=11.40,
            breakout_high=11.60,
            support_price=10.80,
        )

        signal = self.strategy.evaluate_first_pullback_entry(
            df_history=df_history,
            current_bar=trigger_bar,
            prev_bar=prev_bar,
            account_equity=2000.0,
            available_cash=2000.0,
            current_time="09:34:00",
        )

        self.assertIsNotNone(signal, "First pullback entry should have triggered")
        # Trigger price: prev_bar.high + 0.01 = 11.41
        self.assertEqual(signal["trigger_price"], 11.41)
        # Stop loss at pullback low - 0.01 = 10.99
        self.assertEqual(signal["stop_loss"], 10.99)
        # Target at HOD = 12.00
        self.assertEqual(signal["hod_target"], 12.00)
        # Risk per share = 11.41 - 10.99 = 0.42
        # Reward per share = 12.00 - 11.41 = 0.59
        # R/R = 0.59 / 0.42 = 1.405 >= 1.0
        self.assertGreaterEqual(signal["rr_ratio"], 1.0)

        # Position Sizing: Risk = $2,000 * 1% = $20. Shares = floor(20 / 0.42) = 47 shares
        expected_shares = math.floor(20.0 / 0.42)
        self.assertEqual(signal["shares"], expected_shares)

    def test_first_pullback_rejection_low_rr(self):
        """Verify entry is rejected when R/R to HOD is less than 1:1."""
        # Set HOD price very close to entry, so Reward < Risk
        df_history, trigger_bar, prev_bar = self._create_sample_spike_and_pullback(
            pullback_count=2,
            hod_price=11.50, # Low HOD target
            pullback_low=11.00,
            prev_bar_high=11.40, # Entry at 11.41 -> Reward = 11.50 - 11.41 = 0.09, Risk = 0.42 -> R/R = 0.21
            breakout_high=11.55,
            support_price=10.80,
        )

        signal = self.strategy.evaluate_first_pullback_entry(
            df_history=df_history,
            current_bar=trigger_bar,
            prev_bar=prev_bar,
            account_equity=2000.0,
            available_cash=2000.0,
            current_time="09:34:00",
        )
        self.assertIsNone(signal, "Trade must be rejected when R/R < 1:1")

    def test_first_pullback_support_break_rejection(self):
        """Verify entry is rejected when pullback breaks below key support (9EMA/VWAP)."""
        df_history, trigger_bar, prev_bar = self._create_sample_spike_and_pullback(
            pullback_count=2,
            hod_price=12.00,
            pullback_low=10.50, # Broke below support
            prev_bar_high=11.40,
            breakout_high=11.60,
            support_price=11.00, # Support is 11.00, but low reached 10.50
        )

        signal = self.strategy.evaluate_first_pullback_entry(
            df_history=df_history,
            current_bar=trigger_bar,
            prev_bar=prev_bar,
            account_equity=2000.0,
            available_cash=2000.0,
            current_time="09:34:00",
        )
        self.assertIsNone(signal, "Trade must be rejected when pullback breaks below support")

    # =========================================================================
    # 2. Stop Loss Placement and 50% TP1 Halving at HOD
    # =========================================================================
    def test_stop_loss_placement_and_tp1_halving(self):
        """Verify initial SL, 50% TP1 halving at HOD, and Early BE adjustment."""
        engine = RossExecutionEngine(strategy=self.strategy)

        # Place initial position
        pos = engine.execute_buy(
            symbol="MOMO",
            shares=100,
            trigger_price=11.40,
            stop_loss=11.00,
            hod_target=12.00,
            atr=0.50,
            timestamp="09:35:00",
        )
        self.assertIsNotNone(pos)
        self.assertEqual(pos.remaining_shares, 100)
        self.assertEqual(pos.stop_loss, 11.00)

        # Bar reaches HOD target (TP1 = 12.00)
        current_bar = pd.Series({
            "open": 11.80,
            "high": 12.10, # Touches HOD
            "low": 11.70,  # Does not touch SL
            "close": 12.05,
            "volume": 300000,
            "vol_sma20": 150000,
            "atr": 0.50,
        })
        engine.process_bar(
            df_history=pd.DataFrame([current_bar]),
            current_bar=current_bar,
            prev_bar=None,
            symbol="MOMO",
        )

        # 50% must be sold
        self.assertTrue(pos.tp1_hit)
        self.assertEqual(pos.remaining_shares, 50)
        # Stop loss moved to early BE: Entry (11.415 with slippage) + 0.15 * ATR (0.50)
        expected_be = round(pos.entry_price + (0.15 * 0.50), 2)
        self.assertAlmostEqual(pos.stop_loss, expected_be, places=2)
        self.assertGreater(pos.stop_loss, 11.00, "SL must move up to protect profit after TP1")

    # =========================================================================
    # 3. Five Exit Signals Triggers
    # =========================================================================
    def test_exit_signal_1_big_ask_wall(self):
        """Verify Exit Signal 1: Big Ask Wall (Level 2 resistance wall)."""
        pos = RossPosition(
            position_id="POS_TEST",
            symbol="MOMO",
            entry_price=10.00,
            entry_time="09:35:00",
            initial_shares=100,
            remaining_shares=50,
            stop_loss=9.80,
            hod_target=11.00,
            atr_at_entry=0.40,
            tp1_hit=True,
        )
        bar = pd.Series({
            "open": 10.80, "high": 10.90, "low": 10.75, "close": 10.85, "volume": 100000, "vol_sma20": 100000
        })
        l2 = {"ask_wall_ratio": 4.5, "ask_wall_detected": True} # Ask depth 4.5x bid

        sig_type, sig_px, sig_msg = self.strategy.check_exit_signals(
            current_bar=bar,
            prev_bar=None,
            position=pos,
            level2_data=l2,
        )
        self.assertEqual(sig_type, ExitSignalType.BIG_ASK_WALL)
        self.assertIn("Big Ask Wall", sig_msg)

    def test_exit_signal_2_hidden_iceberg(self):
        """Verify Exit Signal 2: Hidden Iceberg Seller (Heavy volume absorption with no progress)."""
        pos = RossPosition(
            position_id="POS_TEST",
            symbol="MOMO",
            entry_price=10.00,
            entry_time="09:35:00",
            initial_shares=100,
            remaining_shares=50,
            stop_loss=9.80,
            hod_target=11.00,
            atr_at_entry=0.50,
            tp1_hit=True,
        )
        # Volume 3x average, but tiny range (0.05 vs 0.50 ATR) and red close
        bar = pd.Series({
            "open": 10.90,
            "high": 10.92,
            "low": 10.88,
            "close": 10.89,
            "volume": 600000,
            "vol_sma20": 200000,
            "range": 0.04,
        })

        sig_type, sig_px, sig_msg = self.strategy.check_exit_signals(
            current_bar=bar,
            prev_bar=None,
            position=pos,
        )
        self.assertEqual(sig_type, ExitSignalType.HIDDEN_ICEBERG)
        self.assertIn("Hidden Iceberg", sig_msg)

    def test_exit_signal_3_tape_selling(self):
        """Verify Exit Signal 3: Tape Selling (Aggressive hitting bid, bid stepping down)."""
        pos = RossPosition(
            position_id="POS_TEST",
            symbol="MOMO",
            entry_price=10.00,
            entry_time="09:35:00",
            initial_shares=100,
            remaining_shares=50,
            stop_loss=9.80,
            hod_target=11.00,
            atr_at_entry=0.40,
            tp1_hit=True,
        )
        bar = pd.Series({
            "open": 10.80, "high": 10.85, "low": 10.75, "close": 10.78, "volume": 100000, "vol_sma20": 100000
        })
        tape = {"tape_sell_ratio": 0.75, "bid_stepping_down": True}

        sig_type, sig_px, sig_msg = self.strategy.check_exit_signals(
            current_bar=bar,
            prev_bar=None,
            position=pos,
            tape_data=tape,
        )
        self.assertEqual(sig_type, ExitSignalType.TAPE_SELLING)
        self.assertIn("Tape selling", sig_msg)

    def test_exit_signal_4_topping_tail(self):
        """Verify Exit Signal 4: Candlestick topping tail / long upper wick exhaustion."""
        pos = RossPosition(
            position_id="POS_TEST",
            symbol="MOMO",
            entry_price=10.00,
            entry_time="09:35:00",
            initial_shares=100,
            remaining_shares=50,
            stop_loss=9.80,
            hod_target=11.00,
            atr_at_entry=0.40,
            tp1_hit=True,
        )
        # Bar spikes to 11.20 but closes at 10.75 (upper wick = 11.20 - 10.80 = 0.40 out of 0.50 range = 80%)
        bar = pd.Series({
            "open": 10.70,
            "high": 11.20,
            "low": 10.70,
            "close": 10.75,
            "volume": 200000,
            "vol_sma20": 100000,
        })

        sig_type, sig_px, sig_msg = self.strategy.check_exit_signals(
            current_bar=bar,
            prev_bar=None,
            position=pos,
        )
        self.assertEqual(sig_type, ExitSignalType.TOPPING_TAIL)
        self.assertIn("Topping tail", sig_msg)

    def test_exit_signal_5_volume_divergence(self):
        """Verify Exit Signal 5: Volume divergence (higher high on fading volume)."""
        pos = RossPosition(
            position_id="POS_TEST",
            symbol="MOMO",
            entry_price=10.00,
            entry_time="09:35:00",
            initial_shares=100,
            remaining_shares=50,
            stop_loss=9.80,
            hod_target=11.00,
            atr_at_entry=0.40,
            tp1_hit=True,
        )
        prev_bar = pd.Series({
            "high": 10.80, "low": 10.50, "close": 10.75, "volume": 500000, "vol_sma20": 200000
        })
        # Current bar prints higher high (10.95 > 10.80) on only 200,000 volume (40% of prior 500k)
        curr_bar = pd.Series({
            "open": 10.75,
            "high": 10.95,
            "low": 10.70,
            "close": 10.90,
            "volume": 200000,
            "vol_sma20": 200000,
        })

        sig_type, sig_px, sig_msg = self.strategy.check_exit_signals(
            current_bar=curr_bar,
            prev_bar=prev_bar,
            position=pos,
        )
        self.assertEqual(sig_type, ExitSignalType.VOLUME_DIVERGENCE)
        self.assertIn("Volume divergence", sig_msg)

    # =========================================================================
    # 4. Five Walk-Away Rules Enforcement
    # =========================================================================
    def test_walk_away_rule_1_peak_profit_retraced_50_pct(self):
        """Rule 1: Peak profit retraced by 50% -> halt for the day."""
        self.strategy.peak_daily_profit = 400.0 # Peak profit $400
        self.strategy.daily_realized_pnl = 190.0 # Retraced to $190 (< 50% of $400 = $200)

        halted, reason = self.strategy.check_walk_away_rules(current_time="09:45:00")
        self.assertTrue(halted)
        self.assertEqual(reason, WalkAwayReason.PEAK_PROFIT_RETRACED)

    def test_walk_away_rule_2_daily_max_loss_hit(self):
        """Rule 2: Daily max loss hit -> halt for the day."""
        self.strategy.daily_realized_pnl = -205.0 # Max loss is $200

        halted, reason = self.strategy.check_walk_away_rules(current_time="09:45:00")
        self.assertTrue(halted)
        self.assertEqual(reason, WalkAwayReason.DAILY_MAX_LOSS_HIT)

    def test_walk_away_rule_3_passed_10am_est(self):
        """Rule 3: Passed 10:00 AM EST -> halt for the day."""
        halted, reason = self.strategy.check_walk_away_rules(current_time="10:01:00")
        self.assertTrue(halted)
        self.assertEqual(reason, WalkAwayReason.TIME_WINDOW_PASSED)

        # Ensure before 10:00 AM does not halt
        self.strategy.is_halted = False
        self.strategy.halt_reason = None
        halted, reason = self.strategy.check_walk_away_rules(current_time="09:45:00")
        self.assertFalse(halted)

    def test_walk_away_rule_4_screener_no_valid_stocks(self):
        """Rule 4: Screener has no valid stocks -> stay in cash."""
        halted, reason = self.strategy.check_walk_away_rules(
            current_time="09:40:00",
            screener_has_valid_stocks=False,
        )
        self.assertTrue(halted)
        self.assertEqual(reason, WalkAwayReason.SCREENER_NO_VALID_STOCKS)

    def test_walk_away_rule_5_market_momentum_exhausted(self):
        """Rule 5: Overall market momentum exhausted -> stop."""
        halted, reason = self.strategy.check_walk_away_rules(
            current_time="09:40:00",
            market_momentum_exhausted=True,
        )
        self.assertTrue(halted)
        self.assertEqual(reason, WalkAwayReason.MARKET_MOMENTUM_EXHAUSTED)


class TestRossExecutionEngine(unittest.TestCase):
    """Unit tests for Ross Execution Engine, Balance Conservation, and Pessimistic Defense."""

    def setUp(self):
        self.strat_config = StrategyConfig(
            risk_per_trade_pct=0.01,
            daily_max_loss=200.0,
            trading_cutoff_time="10:00:00",
        )
        self.exec_config = ExecutionConfig(
            initial_capital=2000.0,
            base_slippage_per_share=0.015, # $0.015 slippage
            sec_fee_rate=0.0000278,
            finra_taf_per_share=0.000166,
            pessimistic_intra_bar_sl=True,
            enable_compounding=True,
        )
        self.strategy = RossMomentumStrategy(self.strat_config)
        self.engine = RossExecutionEngine(strategy=self.strategy, exec_config=self.exec_config)

    # =========================================================================
    # 5. Double-Entry Balance Conservation & Pessimistic Intra-Bar Execution
    # =========================================================================
    def test_pessimistic_intra_bar_sl_conflict(self):
        """
        Verify Pessimistic Intra-Bar Execution:
        When High >= TP1 and Low <= SL in the same bar, Stop Loss triggers FIRST!
        """
        pos = self.engine.execute_buy(
            symbol="ROSS",
            shares=100,
            trigger_price=10.00,
            stop_loss=9.50,
            hod_target=11.00,
            atr=0.50,
            timestamp="09:32:00",
        )
        self.assertIsNotNone(pos)

        # Bar touches BOTH TP1 (High >= 11.00) and SL (Low <= 9.50)
        conflict_bar = pd.Series({
            "timestamp": "09:33:00",
            "open": 10.20,
            "high": 11.20, # Touches TP1
            "low": 9.40,   # Touches SL
            "close": 10.50,
            "volume": 500000,
            "vol_sma20": 200000,
            "atr": 0.50,
        })

        self.engine.process_bar(
            df_history=pd.DataFrame([conflict_bar]),
            current_bar=conflict_bar,
            prev_bar=None,
            symbol="ROSS",
        )

        # Position must be completely closed via STOP LOSS, NOT TP1!
        self.assertIsNone(self.engine.active_position, "Position must be closed")
        last_trade = self.engine.trade_history[-1]
        self.assertEqual(last_trade.exit_reason, "SL_PESSIMISTIC_CONFLICT")
        self.assertEqual(last_trade.side, "STOP_LOSS")
        # Realized PnL must be negative (loss, not profit)
        self.assertLess(last_trade.realized_pnl, 0.0)

    def test_double_entry_balance_conservation_invariant(self):
        """
        Verify Double-Entry Balance Conservation:
        1. At every bar: Cash + (Shares * Current_Price) == Total Equity.
        2. Across round-trip trades: Initial_Capital + Realized_PnL == Cash.
        3. All slippage and SEC/FINRA regulatory fees audited with zero leakage.
        """
        self.assertEqual(self.engine.cash, 2000.0)
        self.assertEqual(self.engine.equity, 2000.0)

        # Execute Buy
        pos = self.engine.execute_buy(
            symbol="ABC",
            shares=100,
            trigger_price=10.00,
            stop_loss=9.50,
            hod_target=11.00,
            atr=0.40,
            timestamp="09:31:00",
        )
        self.assertIsNotNone(pos)
        # Fill price: 10.00 + 0.015 slippage = 10.015
        expected_fill = 10.015
        expected_outflow = 100 * 10.015 # 1001.50
        self.assertAlmostEqual(self.engine.cash, 2000.0 - expected_outflow, places=3)
        self.assertAlmostEqual(self.engine.equity, 2000.0, places=3) # At fill price

        # Bar 1: Price rises
        bar1 = pd.Series({
            "timestamp": "09:32:00", "open": 10.20, "high": 10.60, "low": 10.10, "close": 10.50, "volume": 100000
        })
        self.engine.process_bar(
            df_history=pd.DataFrame([bar1]), current_bar=bar1, prev_bar=None, symbol="ABC"
        )
        # Conservation check at bar close
        expected_stock_val = 100 * 10.50
        self.assertAlmostEqual(self.engine.equity, self.engine.cash + expected_stock_val, places=3)

        # Bar 2: TP1 hit at HOD (11.00)
        bar2 = pd.Series({
            "timestamp": "09:33:00", "open": 10.60, "high": 11.05, "low": 10.50, "close": 10.95, "volume": 200000
        })
        self.engine.process_bar(
            df_history=pd.DataFrame([bar1, bar2]), current_bar=bar2, prev_bar=bar1, symbol="ABC"
        )
        # 50 shares sold at 11.00 - 0.015 slippage = 10.985
        self.assertEqual(pos.remaining_shares, 50)
        self.assertAlmostEqual(self.engine.equity, self.engine.cash + (50 * 10.95), places=3)

        # Bar 3: Exit remaining shares on Topping Tail
        bar3 = pd.Series({
            "timestamp": "09:34:00", "open": 10.90, "high": 11.40, "low": 10.85, "close": 10.90, "volume": 300000
        })
        self.engine.process_bar(
            df_history=pd.DataFrame([bar1, bar2, bar3]), current_bar=bar3, prev_bar=bar2, symbol="ABC"
        )
        # Remaining 50 shares closed on topping tail
        self.assertIsNone(self.engine.active_position)
        self.assertEqual(self.engine.equity, self.engine.cash)

        # Final Double-Entry Invariant:
        # Cash == Initial_Capital + Total_Realized_PnL
        audit = self.engine.get_audit_summary()
        self.assertTrue(audit["double_entry_balance_conservation_verified"])
        self.assertAlmostEqual(self.engine.cash, 2000.0 + self.engine.cumulative_realized_pnl, places=3)
        self.assertGreater(self.engine.total_slippage_cost, 0.0)
        self.assertGreater(self.engine.total_sec_fees, 0.0)
        self.assertGreater(self.engine.total_finra_fees, 0.0)

    def test_compounding_equity_reinvestment(self):
        """Verify compounding increases position sizing as account grows."""
        # Initial sizing at $2,000 equity, risk 1% = $20, risk distance $0.50 -> 40 shares
        sig1 = self.strategy.evaluate_first_pullback_entry(
            df_history=pd.DataFrame([
                {"timestamp": "09:30:00", "open": 10.0, "high": 12.0, "low": 9.9, "close": 11.8, "volume": 100000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0},
                {"timestamp": "09:31:00", "open": 10.8, "high": 10.49, "low": 10.01, "close": 10.2, "volume": 50000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0},
            ]),
            current_bar=pd.Series({"timestamp": "09:32:00", "open": 10.40, "high": 10.60, "low": 10.20, "close": 10.55, "volume": 80000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0}),
            prev_bar=pd.Series({"timestamp": "09:31:00", "open": 10.8, "high": 10.49, "low": 10.01, "close": 10.2, "volume": 50000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0}),
            account_equity=2000.0,
            available_cash=2000.0,
            current_time="09:32:00",
        )
        self.assertIsNotNone(sig1)
        shares_initial = sig1["shares"]

        # Sizing at $4,000 compounded equity
        sig2 = self.strategy.evaluate_first_pullback_entry(
            df_history=pd.DataFrame([
                {"timestamp": "09:30:00", "open": 10.0, "high": 12.0, "low": 9.9, "close": 11.8, "volume": 100000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0},
                {"timestamp": "09:31:00", "open": 10.8, "high": 10.49, "low": 10.01, "close": 10.2, "volume": 50000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0},
            ]),
            current_bar=pd.Series({"timestamp": "09:32:00", "open": 10.40, "high": 10.60, "low": 10.20, "close": 10.55, "volume": 80000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0}),
            prev_bar=pd.Series({"timestamp": "09:31:00", "open": 10.8, "high": 10.49, "low": 10.01, "close": 10.2, "volume": 50000, "ema9": 10.0, "vwap": 10.0, "atr": 0.5, "hod": 12.0}),
            account_equity=4000.0,
            available_cash=4000.0,
            current_time="09:32:00",
        )
        self.assertIsNotNone(sig2)
        shares_compounded = sig2["shares"]

        # Compounding reinvestment should scale shares proportionally with account equity
        self.assertGreater(shares_compounded, shares_initial)
        self.assertEqual(shares_compounded, shares_initial * 2)

    def test_pullback_bar_count_boundary(self):
        """Verify 1-5 pullback candles trigger, while > 5 pullback candles is rejected."""
        # Test 1 pullback candle
        df_1, trig_1, prev_1 = TestRossMomentumStrategy()._create_sample_spike_and_pullback(
            pullback_count=1, hod_price=12.00, pullback_low=11.00, prev_bar_high=11.40, breakout_high=11.60
        )
        sig_1 = self.strategy.evaluate_first_pullback_entry(
            df_history=df_1, current_bar=trig_1, prev_bar=prev_1,
            account_equity=2000.0, available_cash=2000.0, current_time="09:33:00"
        )
        self.assertIsNotNone(sig_1, "1 pullback candle should be accepted")

        # Test 5 pullback candles
        df_5, trig_5, prev_5 = TestRossMomentumStrategy()._create_sample_spike_and_pullback(
            pullback_count=5, hod_price=12.00, pullback_low=11.00, prev_bar_high=11.40, breakout_high=11.60
        )
        sig_5 = self.strategy.evaluate_first_pullback_entry(
            df_history=df_5, current_bar=trig_5, prev_bar=prev_5,
            account_equity=2000.0, available_cash=2000.0, current_time="09:37:00"
        )
        self.assertIsNotNone(sig_5, "5 pullback candles should be accepted")

        # Test 6 pullback candles (> 5 max pullback candles)
        df_6, trig_6, prev_6 = TestRossMomentumStrategy()._create_sample_spike_and_pullback(
            pullback_count=6, hod_price=12.00, pullback_low=11.00, prev_bar_high=11.40, breakout_high=11.60
        )
        sig_6 = self.strategy.evaluate_first_pullback_entry(
            df_history=df_6, current_bar=trig_6, prev_bar=prev_6,
            account_equity=2000.0, available_cash=2000.0, current_time="09:38:00"
        )
        self.assertIsNone(sig_6, "6 pullback candles must be rejected as outside 1-5 pullback limit")

    def test_complete_chronological_backtest_lifecycle(self):
        """
        Verify end-to-end backtest lifecycle:
        - Entry on first pullback breakout.
        - Take profit 50% at HOD.
        - Exit runner on Level 2 Ask Wall.
        - Verify strict double-entry balance conservation at every bar.
        """
        bars = [
            # 09:30 - Initial Base
            {"timestamp": "09:30:00", "open": 10.00, "high": 10.20, "low": 9.95, "close": 10.15, "volume": 100000},
            # 09:31 - Surge to HOD 12.00
            {"timestamp": "09:31:00", "open": 10.20, "high": 12.00, "low": 10.15, "close": 11.90, "volume": 600000},
            # 09:32 - Pullback Bar 1
            {"timestamp": "09:32:00", "open": 11.85, "high": 11.80, "low": 11.10, "close": 11.20, "volume": 80000},
            # 09:33 - Pullback Bar 2 (consolidating above 9EMA/VWAP ~ 10.80)
            {"timestamp": "09:33:00", "open": 11.20, "high": 11.35, "low": 11.05, "close": 11.15, "volume": 70000},
            # 09:34 - Breakout trigger above 11.35 (reaches 11.60)
            {"timestamp": "09:34:00", "open": 11.30, "high": 11.60, "low": 11.25, "close": 11.55, "volume": 250000},
            # 09:35 - Continues upward (11.85)
            {"timestamp": "09:35:00", "open": 11.55, "high": 11.90, "low": 11.50, "close": 11.85, "volume": 300000},
            # 09:36 - Hits HOD 12.05 (TP1 triggered, sells 50%)
            {"timestamp": "09:36:00", "open": 11.85, "high": 12.10, "low": 11.80, "close": 12.05, "volume": 400000},
            # 09:37 - Runner encounters Big Ask Wall at 12.00 (Exits remainder)
            {"timestamp": "09:37:00", "open": 12.05, "high": 12.15, "low": 11.95, "close": 12.00, "volume": 200000},
            # 09:38 - Post-trade bar
            {"timestamp": "09:38:00", "open": 12.00, "high": 12.05, "low": 11.90, "close": 11.95, "volume": 100000},
        ]
        df = pd.DataFrame(bars)
        l2_feed = {
            6: {"ask_wall_ratio": 4.0, "ask_wall_detected": True} # Ask wall at index 6 (bar 09:37)
        }

        engine = RossExecutionEngine(strategy=self.strategy, exec_config=self.exec_config)
        summary = engine.run_backtest(df=df, symbol="MOMO", level2_feed=l2_feed)

        # Assertions
        self.assertTrue(summary["double_entry_balance_conservation_verified"])
        self.assertGreater(summary["total_trades"], 0)
        self.assertGreater(summary["final_equity"], 2000.0, "Strategy should be profitable on clean pullback")
        self.assertEqual(summary["winning_trades"], 2, "TP1 and Ask Wall exit should both be wins")
        self.assertEqual(summary["losing_trades"], 0)
        self.assertEqual(summary["win_rate"], 1.0)

        # Verify trades
        trades = engine.trade_history
        self.assertEqual(trades[0].side, "BUY")
        self.assertEqual(trades[1].side, "SELL_HALF")
        self.assertEqual(trades[1].exit_reason, "TAKE_PROFIT_1_HOD")
        self.assertEqual(trades[2].side, "SELL_ALL")
        self.assertEqual(trades[2].exit_reason, ExitSignalType.BIG_ASK_WALL.value)

        # Audit fees & slippage
        self.assertGreater(summary["total_slippage_cost"], 0.0)
        self.assertGreater(summary["total_sec_fees"], 0.0)
        self.assertGreater(summary["total_finra_fees"], 0.0)

        # Balance conservation: Cash + Realized PnL == Final Cash
        self.assertAlmostEqual(summary["final_cash"], 2000.0 + summary["total_realized_pnl"], places=3)


if __name__ == "__main__":
    unittest.main()
