"""
Unit and Integration Test Suite for SMCSharedPortfolioEngine (Round 4).

Verifies all contract specifications:
1. Hard concurrency cap: asserts concurrent positions never exceed 2.
2. Cash non-negativity and reservation: cash never drops below 0 and liquidity reserve is preserved.
3. Accounting conservation across multi-asset shared pool: strict double-entry balance conservation.
4. Priority dispatch mechanism: (1 - u) * AlphaGPT_Confluence_Score determines precedence.
5. Maker limit penetration requirement (LimitPrice ± 0.05 * ATR).
6. TP1 (50% reduction) + Early BE buffer + TP2 terminal liquidation.
7. Pessimistic intra-bar execution: same bar TP/SL conflict strictly hits SL.
"""

from __future__ import annotations

import math
import os
import sys
import unittest
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.smc_round4_portfolio_engine import (
    SMCSharedPortfolioEngine,
    OrderSide,
    PositionSide,
    PendingLimitOrder,
    ActivePosition,
    TradeRecord,
)
from src.whitehat_round3_penetration import verify_accounting_conservation_invariant


class TestSMCSharedPortfolioEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = SMCSharedPortfolioEngine(
            initial_cash=10000.0,
            max_concurrent_positions=2,
            liquidity_reserve_pct=0.50,
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
            use_credal=False,  # disabled for explicit mechanical testing
            pessimistic_intra_bar=True,
        )

    def test_hard_concurrency_cap(self) -> None:
        """Asserts concurrent active positions never exceed max_concurrent_positions (2)."""
        # Create simultaneous signals across 4 symbols (BTC, ETH, SOL, BNB)
        # All 4 symbols signal LONG at bar 0, penetrate at bar 1, and remain open
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=5, freq="15min")
        symbols = ["BTC", "ETH", "SOL", "BNB"]
        dfs = {}

        for sym in symbols:
            dfs[sym] = pd.DataFrame([
                # Bar 0: Signal generated
                {"Open": 100.0, "High": 101.0, "Low": 99.5, "Close": 100.0, "ATR": 1.0,
                 "Signal": "LONG", "limit_entry_px": 99.0, "stop_loss": 97.0,
                 "confluence_score": 80.0, "credal_uncertainty": 0.10},
                # Bar 1: Low penetrates (98.90 <= 99.0 - 0.05*1.0)
                {"Open": 99.5, "High": 100.0, "Low": 98.80, "Close": 99.5, "ATR": 1.0,
                 "Signal": "NEUTRAL", "limit_entry_px": 99.0, "stop_loss": 97.0},
                # Bars 2-4: Remain open
                {"Open": 99.5, "High": 100.0, "Low": 99.1, "Close": 99.6, "ATR": 1.0, "Signal": "NEUTRAL"},
                {"Open": 99.6, "High": 100.2, "Low": 99.2, "Close": 99.8, "ATR": 1.0, "Signal": "NEUTRAL"},
                {"Open": 99.8, "High": 100.5, "Low": 99.4, "Close": 100.0, "ATR": 1.0, "Signal": "NEUTRAL"},
            ], index=timestamps)

        res = self.engine.run(dfs)

        # Invariant 1: Peak active positions observed must be <= 2
        self.assertLessEqual(
            res["metrics"]["max_concurrent_positions_observed"],
            2,
            f"Observed {res['metrics']['max_concurrent_positions_observed']} active positions, expected <= 2",
        )
        self.assertLessEqual(max(res["active_positions_history"]), 2)

        # Invariant 2: Capacity skips recorded for lower priority assets
        self.assertGreater(
            res["metrics"]["skipped_due_to_capacity"],
            0,
            "Should have skipped excess signals due to global concurrency capacity",
        )

        # Invariant 3: Total closed trades at end of data must equal 2
        self.assertEqual(len(res["trades"]), 2)

    def test_priority_dispatch_mechanism(self) -> None:
        """
        Tests Priority = (1.0 - u) * AlphaGPT_Confluence_Score.
        When 3 symbols signal at the same bar:
        - BTC: u = 0.20, Score = 80.0 -> Priority = 64.0
        - ETH: u = 0.10, Score = 90.0 -> Priority = 81.0 (Highest)
        - SOL: u = 0.30, Score = 70.0 -> Priority = 49.0 (Lowest)
        With max_concurrent = 2, ETH and BTC must be accepted; SOL must be skipped.
        """
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=4, freq="15min")

        btc_df = pd.DataFrame([
            {"Open": 100.0, "High": 101.0, "Low": 99.5, "Close": 100.0, "ATR": 1.0,
             "Signal": "LONG", "limit_entry_px": 99.0, "stop_loss": 97.0,
             "AlphaGPT_Confluence_Score": 80.0, "credal_uncertainty": 0.20},
            {"Open": 99.5, "High": 100.0, "Low": 98.80, "Close": 99.5, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 99.5, "High": 100.0, "Low": 99.0, "Close": 99.6, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 99.6, "High": 100.5, "Low": 99.2, "Close": 100.0, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        eth_df = pd.DataFrame([
            {"Open": 100.0, "High": 101.0, "Low": 99.5, "Close": 100.0, "ATR": 1.0,
             "Signal": "LONG", "limit_entry_px": 99.0, "stop_loss": 97.0,
             "AlphaGPT_Confluence_Score": 90.0, "credal_uncertainty": 0.10},
            {"Open": 99.5, "High": 100.0, "Low": 98.80, "Close": 99.5, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 99.5, "High": 100.0, "Low": 99.0, "Close": 99.6, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 99.6, "High": 100.5, "Low": 99.2, "Close": 100.0, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        sol_df = pd.DataFrame([
            {"Open": 100.0, "High": 101.0, "Low": 99.5, "Close": 100.0, "ATR": 1.0,
             "Signal": "LONG", "limit_entry_px": 99.0, "stop_loss": 97.0,
             "AlphaGPT_Confluence_Score": 70.0, "credal_uncertainty": 0.30},
            {"Open": 99.5, "High": 100.0, "Low": 98.80, "Close": 99.5, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 99.5, "High": 100.0, "Low": 99.0, "Close": 99.6, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 99.6, "High": 100.5, "Low": 99.2, "Close": 100.0, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        dfs = {"BTC": btc_df, "ETH": eth_df, "SOL": sol_df}
        res = self.engine.run(dfs)

        trades = res["trades"]
        self.assertEqual(len(trades), 2, "Exactly 2 positions should be executed")
        executed_symbols = {t["symbol"] for t in trades}

        # ETH (priority 81.0) and BTC (priority 64.0) must be executed
        self.assertIn("ETH", executed_symbols)
        self.assertIn("BTC", executed_symbols)
        # SOL (priority 49.0) must be skipped due to capacity
        self.assertNotIn("SOL", executed_symbols)
        self.assertEqual(res["metrics"]["skipped_due_to_capacity"], 1)

        # Check recorded trade priorities
        eth_trade = next(t for t in trades if t["symbol"] == "ETH")
        btc_trade = next(t for t in trades if t["symbol"] == "BTC")
        self.assertAlmostEqual(eth_trade["priority"], 81.0, places=2)
        self.assertAlmostEqual(btc_trade["priority"], 64.0, places=2)

    def test_cash_non_negativity_and_reservation(self) -> None:
        """Cash never drops below 0 and liquidity reserve is preserved."""
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=6, freq="15min")

        # Two assets experience stop-losses
        btc_df = pd.DataFrame([
            {"Open": 100.0, "High": 101.0, "Low": 99.5, "Close": 100.0, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 99.0, "stop_loss": 97.0},
            {"Open": 99.5, "High": 100.0, "Low": 98.80, "Close": 99.5, "ATR": 1.0, "Signal": "NEUTRAL"},
            # Drops and hits SL at 97.0
            {"Open": 99.5, "High": 99.6, "Low": 96.50, "Close": 96.8, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 96.8, "High": 97.0, "Low": 96.5, "Close": 96.9, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 96.9, "High": 97.2, "Low": 96.7, "Close": 97.0, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 97.0, "High": 97.5, "Low": 96.8, "Close": 97.2, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        eth_df = pd.DataFrame([
            {"Open": 200.0, "High": 202.0, "Low": 199.0, "Close": 200.0, "ATR": 2.0, "Signal": "LONG", "limit_entry_px": 198.0, "stop_loss": 194.0},
            {"Open": 199.0, "High": 200.0, "Low": 197.80, "Close": 199.0, "ATR": 2.0, "Signal": "NEUTRAL"},
            # Drops and hits SL at 194.0
            {"Open": 199.0, "High": 199.2, "Low": 193.00, "Close": 193.5, "ATR": 2.0, "Signal": "NEUTRAL"},
            {"Open": 193.5, "High": 194.0, "Low": 193.0, "Close": 193.8, "ATR": 2.0, "Signal": "NEUTRAL"},
            {"Open": 193.8, "High": 194.2, "Low": 193.5, "Close": 194.0, "ATR": 2.0, "Signal": "NEUTRAL"},
            {"Open": 194.0, "High": 194.5, "Low": 193.8, "Close": 194.2, "ATR": 2.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        res = self.engine.run({"BTC": btc_df, "ETH": eth_df})

        # Cash non-negativity
        self.assertGreater(res["metrics"]["min_cash_observed"], 0.0)
        self.assertGreater(min(res["cash_curve"]), 0.0)
        self.assertGreater(min(res["equity_curve"]), 0.0)

        # Liquidity reserve: check that sizing did not over-allocate capital
        # Initial cash is $10,000, max capital allocated <= 50% = $5,000
        for t in res["trades"]:
            notional = t["initial_size"] * t["entry_price"]
            self.assertLessEqual(notional, 10000.0 * 0.50 + 1e-4)

    def test_accounting_conservation_across_multi_asset_shared_pool(self) -> None:
        """
        Validates double-entry accounting conservation:
        1. Terminal Cash - Initial Cash == sum(Trade PnLs) - sum(Entry Fees).
        2. For every trade: Trade PnL == Realized TP1 PnL + Realized Remaining PnL.
        3. Passed via official White-Hat Penetration Test audit runner.
        """
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=7, freq="15min")

        # BTC hits TP1 (1.5R) and TP2 (3.0R)
        # Entry = 100.0, SL = 98.0 -> Stop dist = 2.0. TP1 = 103.0, TP2 = 106.0
        btc_df = pd.DataFrame([
            {"Open": 100.5, "High": 101.0, "Low": 100.0, "Close": 100.5, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 100.5, "High": 100.8, "Low": 99.90, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL"},
            # Hits TP1 at 103.0
            {"Open": 100.2, "High": 103.5, "Low": 100.1, "Close": 103.2, "ATR": 1.0, "Signal": "NEUTRAL"},
            # Hits TP2 at 106.0
            {"Open": 103.2, "High": 106.5, "Low": 103.0, "Close": 106.2, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 106.2, "High": 106.5, "Low": 105.8, "Close": 106.0, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 106.0, "High": 106.3, "Low": 105.9, "Close": 106.1, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 106.1, "High": 106.4, "Low": 105.8, "Close": 106.2, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        # ETH hits TP1 at 206.0 then BE_SL at 200.30
        # Entry = 200.0, SL = 196.0 -> Stop dist = 4.0. TP1 = 206.0. Early BE = 200 + 0.15*2.0 = 200.30
        eth_df = pd.DataFrame([
            {"Open": 201.0, "High": 202.0, "Low": 200.0, "Close": 201.0, "ATR": 2.0, "Signal": "LONG", "limit_entry_px": 200.0, "stop_loss": 196.0},
            {"Open": 201.0, "High": 201.5, "Low": 199.80, "Close": 200.5, "ATR": 2.0, "Signal": "NEUTRAL"},
            # Hits TP1 at 206.0
            {"Open": 200.5, "High": 207.0, "Low": 200.4, "Close": 206.5, "ATR": 2.0, "Signal": "NEUTRAL"},
            # Pulls back and hits BE_SL at 200.30
            {"Open": 206.5, "High": 206.8, "Low": 199.5, "Close": 199.8, "ATR": 2.0, "Signal": "NEUTRAL"},
            {"Open": 199.8, "High": 200.0, "Low": 199.0, "Close": 199.5, "ATR": 2.0, "Signal": "NEUTRAL"},
            {"Open": 199.5, "High": 200.0, "Low": 199.2, "Close": 199.7, "ATR": 2.0, "Signal": "NEUTRAL"},
            {"Open": 199.7, "High": 200.2, "Low": 199.4, "Close": 200.0, "ATR": 2.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        res = self.engine.run({"BTC": btc_df, "ETH": eth_df})
        trades = res["trades"]
        self.assertEqual(len(trades), 2)

        # 1. Trade-level double-entry consistency
        for t in trades:
            self.assertTrue(t["tp1_hit"])
            expected_pnl = t["tp1_pnl"] + t["remaining_pnl"]
            self.assertAlmostEqual(t["pnl"], expected_pnl, places=5)
            self.assertAlmostEqual(t["total_fees"], t["entry_fee"] + t["tp1_fee"] + t["exit_fee"], places=5)

        # 2. Portfolio-level cash change consistency
        initial_cash = 10000.0
        final_cash = res["metrics"]["final_cash"]
        total_pnl = sum(t["pnl"] for t in trades)
        total_entry_fees = sum(t["entry_fee"] for t in trades)
        expected_cash_change = total_pnl - total_entry_fees
        actual_cash_change = final_cash - initial_cash

        self.assertAlmostEqual(actual_cash_change, expected_cash_change, places=4)

        # 3. White-hat penetration test runner verification
        audit_res = verify_accounting_conservation_invariant(
            engine_result=res,
            initial_cash=initial_cash,
            maker_fee=0.0002,
            tolerance=1e-5,
        )
        self.assertTrue(audit_res["passed"], f"White-hat accounting audit failed: {audit_res}")
        self.assertAlmostEqual(audit_res["discrepancy"], 0.0, places=5)

    def test_maker_penetration_requirement(self) -> None:
        """Penetration fill: LimitPrice ± 0.05 * ATR required to fill."""
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=4, freq="15min")

        # Bar 1 touches 100.0 (Low = 100.0) -> Not penetrated (Low must be <= 99.95) -> NO fill
        # Bar 2 Low drops to 99.90 (<= 99.95) -> Fills as Maker at exactly 100.0
        df = pd.DataFrame([
            {"Open": 101.0, "High": 102.0, "Low": 100.5, "Close": 101.0, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 101.0, "High": 101.5, "Low": 100.0, "Close": 100.5, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 100.5, "High": 101.0, "Low": 99.90, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 100.2, "High": 100.5, "Low": 100.0, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        res = self.engine.run({"BTC": df})
        trades = res["trades"]
        self.assertEqual(len(trades), 1)
        t = trades[0]
        self.assertEqual(t["entry_price"], 100.0)

    def test_intra_bar_pessimism_sl_resolution(self) -> None:
        """When TP and SL are touched in the same bar, SL wins!"""
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=4, freq="15min")

        df = pd.DataFrame([
            {"Open": 100.5, "High": 101.0, "Low": 100.0, "Close": 100.5, "ATR": 1.0, "Signal": "LONG", "limit_entry_px": 100.0, "stop_loss": 98.0},
            {"Open": 100.5, "High": 100.8, "Low": 99.90, "Close": 100.2, "ATR": 1.0, "Signal": "NEUTRAL"},
            # Bar 2 touches BOTH 103.5 (TP1) and 97.0 (SL)
            {"Open": 100.2, "High": 104.0, "Low": 97.0, "Close": 101.0, "ATR": 1.0, "Signal": "NEUTRAL"},
            {"Open": 101.0, "High": 101.5, "Low": 100.5, "Close": 101.0, "ATR": 1.0, "Signal": "NEUTRAL"},
        ], index=timestamps)

        res = self.engine.run({"BTC": df})
        trades = res["trades"]
        self.assertEqual(len(trades), 1)
        t = trades[0]
        self.assertIn("SL", t["exit_reason"])
        self.assertFalse(t["tp1_hit"])

    def test_equity_compounding_formula(self) -> None:
        """Position size scales dynamically: Size = (Equity * Risk%) / StopDist."""
        size1 = self.engine.calculate_position_size(equity=10000.0, entry_price=100.0, stop_loss_price=98.0)
        # With 2 concurrent positions sharing 50% reserve, each position gets max 25% notional = 2,500 / 100 = 25.0
        self.assertAlmostEqual(size1, 25.0, places=4)

        size2 = self.engine.calculate_position_size(equity=20000.0, entry_price=100.0, stop_loss_price=98.0)
        # Scaled linearly with 2x equity compounding: 5,000 / 100 = 50.0
        self.assertAlmostEqual(size2, 50.0, places=4)


if __name__ == "__main__":
    unittest.main()
