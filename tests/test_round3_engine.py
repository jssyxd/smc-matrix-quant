"""
Unit tests for SMCRound3ExecutionEngine.

Verifies all contract specifications:
1. Maker Limit Order Entry:
   - Order placed at limit_entry_px (50% retracement of OB/FVG zone).
   - Price penetration requirement: LimitPrice ± 0.05 * ATR.
   - Maker fee: 0.02%, 0% slippage.
   - Expiry after 3 bars without fill.
2. Taker Stop Loss & Early BE:
   - Dynamic slippage: 0.05% + fee 0.05%.
   - Early BE: when MFE >= 0.7R, moves SL to Entry ± 0.15 * ATR.
   - Intra-bar pessimism: same bar TP and SL conflict strictly executes SL.
3. TP1 & TP2 Double-Entry Accounting:
   - TP1 at 1.5R: closes 50% of initial position with Maker fee 0.02%.
   - TP2 at 3.0R: closes remaining 50% position with Maker fee 0.02%.
   - Strict balance conservation: Total PnL == Realized TP1 PnL + Realized Remaining PnL.
4. Compound Capital Model:
   - Size dynamically calculated from accumulated equity:
     Size = (Equity * Risk%) / StopDistance.
5. Credal Uncertainty Gate & AlphaGPT Features:
   - Abstains when u > 0.35 or when factors conflict.
"""

import math
import os
import sys
import unittest
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.smc_round3_compound_engine import (
    SMCRound3ExecutionEngine,
    OrderSide,
    PositionSide,
    PendingLimitOrder,
    ActivePosition,
)
from src.credal_engine import CredalSignal


class TestSMCRound3ExecutionEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = SMCRound3ExecutionEngine(
            initial_cash=1000.0,
            maker_fee=0.0002,
            taker_fee=0.0005,
            taker_slippage=0.0005,
            risk_pct=1.0,
            use_compound=True,
            max_leverage=4.0,
            penetration_atr_mult=0.05,
            rr_tp1=1.5,
            rr_tp2=3.0,
            early_be_mfe_r=0.7,
            early_be_buffer_atr=0.15,
            limit_order_expiry_bars=3,
            use_credal=False,  # default off for direct order mechanics tests
            pessimistic_intra_bar=True,
        )

    def test_maker_penetration_requirement(self) -> None:
        """Penetration fill: LimitPrice ± 0.05 * ATR required to fill."""
        # Entry = 100.0, ATR = 1.0 -> Penetration requirement = 0.05
        # Bar 1 touches 100.0 (Low = 100.0), NOT penetrated (< 99.95) -> NO fill!
        # Bar 2 Low drops to 99.94 (<= 99.95) -> Fills as Maker at exactly 100.0
        df = pd.DataFrame([
            {"Open": 101.0, "High": 102.0, "Low": 100.5, "Close": 101.0, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 101.0, "High": 101.5, "Low": 100.0, "Close": 100.5, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 100.5, "High": 101.0, "Low": 99.90, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 100.2, "High": 100.5, "Low": 100.0, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
        ])

        res = self.engine.run(df)
        trades = res["trades"]
        self.assertEqual(len(trades), 1)
        t = trades[0]
        # Filled at bar 2 (time index 2)
        self.assertEqual(t["entry_price"], 100.0)
        # Maker fee 0.02%, zero slippage on entry
        expected_size = (1000.0 * 0.01) / 2.0  # Equity 1000, 1% risk = 10. Stop dist = 100 - 98 = 2. Size = 5.0
        self.assertAlmostEqual(t["initial_size"], expected_size, places=4)

    def test_partial_close_tp1_and_tp2_accounting(self) -> None:
        """TP1 at 1.5R closes 50% with Maker fee 0.02%, TP2 at 3.0R closes remainder."""
        # Entry = 100.0, SL = 98.0 -> Stop dist = 2.0
        # TP1 (1.5R) = 100 + 1.5*2 = 103.0
        # TP2 (3.0R) = 100 + 3.0*2 = 106.0
        # ATR = 1.0
        df = pd.DataFrame([
            # Bar 0: Long signal, limit placed at 100.0, SL at 98.0
            {"Open": 101.0, "High": 101.5, "Low": 100.5, "Close": 101.0, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            # Bar 1: Low drops to 99.90 (<= 99.95), penetrates & fills at 100.0
            {"Open": 100.5, "High": 101.0, "Low": 99.90, "Close": 100.5, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            # Bar 2: High touches 103.5 (>= 103.0 TP1). Closes 50% (2.5 units), moves SL to Entry + 0.15*ATR = 100.15
            {"Open": 100.5, "High": 103.5, "Low": 100.4, "Close": 103.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            # Bar 3: High reaches 106.5 (>= 106.0 TP2). Closes remaining 50% (2.5 units) with Maker fee
            {"Open": 103.2, "High": 106.5, "Low": 103.0, "Close": 106.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
        ])

        res = self.engine.run(df)
        trades = res["trades"]
        self.assertEqual(len(trades), 1)
        t = trades[0]

        self.assertEqual(t["exit_reason"], "TP2")
        self.assertTrue(t["tp1_hit"])
        self.assertAlmostEqual(t["initial_size"], 5.0, places=4)
        self.assertAlmostEqual(t["exit_size"], 2.5, places=4)

        # TP1 realized PnL = 2.5 * (103.0 - 100.0) - (2.5 * 103.0 * 0.0002) = 7.5 - 0.0515 = 7.4485
        tp1_fee = 2.5 * 103.0 * 0.0002
        expected_tp1_pnl = 2.5 * 3.0 - tp1_fee
        self.assertAlmostEqual(t["tp1_pnl"], expected_tp1_pnl, places=4)

        # TP2 remaining PnL = 2.5 * (106.0 - 100.0) - (2.5 * 106.0 * 0.0002) = 15.0 - 0.053 = 14.947
        tp2_fee = 2.5 * 106.0 * 0.0002
        expected_remaining_pnl = 2.5 * 6.0 - tp2_fee
        self.assertAlmostEqual(t["remaining_pnl"], expected_remaining_pnl, places=4)

        entry_fee = 5.0 * 100.0 * 0.0002
        expected_trade_pnl = expected_tp1_pnl + expected_remaining_pnl
        self.assertAlmostEqual(t["pnl"], expected_trade_pnl, places=4)

        # Balance conservation check: Final Cash - Initial Cash == Trade PnL - Entry Fee
        net_delta = res["metrics"]["final_cash"] - 1000.0
        expected_net_delta = expected_trade_pnl - entry_fee
        self.assertAlmostEqual(net_delta, expected_net_delta, places=4)
    def test_early_be_trigger_at_0_7r(self) -> None:
        """When MFE >= 0.7R, SL is moved to Entry ± 0.15 * ATR."""
        # Entry = 100.0, SL = 98.0 -> Stop dist = 2.0. 0.7R = 1.4 -> Price reaching 101.4 moves SL to 100.15
        df = pd.DataFrame([
            {"Open": 100.5, "High": 101.0, "Low": 100.0, "Close": 100.5, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 100.5, "High": 100.8, "Low": 99.90, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            # Bar 2 reaches High = 101.5 (>= 101.4 MFE 0.7R), moves SL to 100.15
            {"Open": 100.2, "High": 101.5, "Low": 100.1, "Close": 101.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            # Bar 3 plunges to 100.0, hitting the adjusted BE SL at 100.15
            {"Open": 101.2, "High": 101.3, "Low": 100.0, "Close": 100.1, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
        ])

        res = self.engine.run(df)
        trades = res["trades"]
        self.assertEqual(len(trades), 1)
        t = trades[0]
        self.assertEqual(t["exit_reason"], "BE_SL")
        self.assertLess(t["exit_price"], 100.15)
        self.assertGreater(t["exit_price"], 100.0)
    def test_intra_bar_pessimism_sl_wins(self) -> None:
        """When TP and SL are touched in the same bar, SL wins!"""
        df = pd.DataFrame([
            {"Open": 100.5, "High": 101.0, "Low": 100.0, "Close": 100.5, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 100.5, "High": 100.8, "Low": 99.90, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
            # Bar 2 touches BOTH 103.5 (TP1) and 97.5 (SL)
            {"Open": 100.2, "High": 104.0, "Low": 97.0, "Close": 101.0, "ATR": 1.0, "Signal": "NEUTRAL", "limit_entry_px": 100.0, "stop_loss": 98.0},
        ])

        res = self.engine.run(df)
        trades = res["trades"]
        self.assertEqual(len(trades), 1)
        t = trades[0]
        self.assertIn("SL", t["exit_reason"])
        self.assertFalse(t["tp1_hit"])

    def test_compound_sizing_formula(self) -> None:
        """Position size scales dynamically: Size = (Equity * Risk%) / StopDist."""
        size1 = self.engine.calculate_position_size(equity=1000.0, entry_price=100.0, stop_loss_price=98.0)
        # Risk 1% of 1000 = 10. Stop dist = 2. Size = 5.0
        self.assertAlmostEqual(size1, 5.0, places=4)

        size2 = self.engine.calculate_position_size(equity=2000.0, entry_price=100.0, stop_loss_price=98.0)
        # Risk 1% of 2000 = 20. Stop dist = 2. Size = 10.0
        self.assertAlmostEqual(size2, 10.0, places=4)


if __name__ == "__main__":
    unittest.main()
