"""
Automated Test Runner and Safety Invariant Verification Suite for Round 3.

Executes the full white-hat penetration test suite and asserts all safety invariants pass:
1. 2,000-Path Monte Carlo Bootstrap Engine:
   - Resamples Out-of-Sample trade sequence over 2,000 synthetic market paths (200 trades per path).
   - Computes Probability of Ruin (drawdown >= 50%), VaR 95%, CVaR 95%, and 95%/99% Max Drawdown.
2. White-Hat Penetration Tests:
   - Zero lookahead bias proof: shifts future prices and proves current signals remain identical.
   - Accounting conservation invariant: validates total cash change equals sum of trade net PnL minus fees
     and slippage across all trades.
   - Pessimistic intra-bar execution check: validates that when high >= TP and low <= SL in the same bar,
     the engine always resolves as a Stop Loss hit.
"""

from __future__ import annotations

import json
import math
import os
import sys
import unittest
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.whitehat_round3_penetration import (
    MonteCarloStressResult,
    run_monte_carlo_bootstrap,
    verify_zero_lookahead_invariant,
    verify_accounting_conservation_invariant,
    verify_intra_bar_pessimism_invariant,
    generate_adversarial_synthetic_bars,
)
from src.qlib_smc_alpha import QlibSMCAlphaPipeline, QlibSMCConfig
from src.smc_round2_engine import Round2SMCEngine
from src.smc_pessimistic_engine import PessimisticExecutionEngine


class TestWhitehatRound3Penetration(unittest.TestCase):
    """Test suite executing the full penetration testing and safety invariant verification."""

    def setUp(self) -> None:
        self.initial_capital = 1000.0
        self.bars = generate_adversarial_synthetic_bars(n_bars=250, seed=42)

    def test_monte_carlo_bootstrap_2000_paths(self) -> None:
        """1. Verify 2,000-path Monte Carlo bootstrap simulation and risk metrics."""
        # Test with realistic OOS trade distribution
        mc_result = run_monte_carlo_bootstrap(
            n_simulations=2000,
            sample_trades_per_path=200,
            initial_capital=self.initial_capital,
            seed=42,
        )

        self.assertIsInstance(mc_result, MonteCarloStressResult)
        self.assertEqual(mc_result.n_simulations, 2000)
        self.assertEqual(mc_result.sample_trades_per_path, 200)
        self.assertEqual(mc_result.initial_capital, 1000.0)

        # Invariant checks on Monte Carlo statistical distributions
        self.assertGreater(mc_result.mean_terminal_wealth, 0.0)
        self.assertGreater(mc_result.median_terminal_wealth, 0.0)
        self.assertGreaterEqual(mc_result.probability_of_ruin_pct, 0.0)
        self.assertLessEqual(mc_result.probability_of_ruin_pct, 100.0)

        # Drawdown invariants: Percentile 99 DD >= Percentile 95 DD >= Mean DD
        self.assertGreaterEqual(
            mc_result.percentile_99_max_drawdown_pct,
            mc_result.percentile_95_max_drawdown_pct - 1e-6,
            "99th percentile Max DD should be >= 95th percentile Max DD",
        )
        self.assertGreaterEqual(
            mc_result.percentile_95_max_drawdown_pct,
            mc_result.mean_max_drawdown_pct - 1e-6,
            "95th percentile Max DD should be >= Mean Max DD",
        )

        # VaR and CVaR invariants: CVaR (expected shortfall) >= VaR
        self.assertGreaterEqual(
            mc_result.cvar_95_pct,
            mc_result.var_95_pct - 1e-6,
            "CVaR 95% must be greater than or equal to VaR 95%",
        )

        # Verify export to dictionary
        d = mc_result.to_dict()
        self.assertIn("probability_of_ruin_pct", d)
        self.assertIn("var_95_pct", d)
        self.assertIn("cvar_95_pct", d)
        self.assertIn("percentile_95_max_drawdown_pct", d)
        self.assertIn("percentile_99_max_drawdown_pct", d)

    def test_zero_lookahead_future_scramble_invariant(self) -> None:
        """2. Verify mathematical proof of zero lookahead bias."""
        config = QlibSMCConfig(swing_len=5, use_credal_filter=False)
        audit_res = verify_zero_lookahead_invariant(
            df=self.bars,
            config=config,
            scramble_modes=["random_shuffle", "extreme_adversarial_shock", "future_reversal"],
        )

        self.assertTrue(
            audit_res["passed"],
            f"Zero lookahead invariant violated! Violations: {audit_res.get('violations')}",
        )
        self.assertGreater(audit_res["checked_points"], 0)
        self.assertEqual(len(audit_res["violations"]), 0)

    def test_accounting_conservation_invariant_round2(self) -> None:
        """3. Verify accounting balance conservation on Round2 execution engine."""
        engine = Round2SMCEngine(
            initial_cash=1000.0,
            maker_fee=0.0002,
            taker_fee=0.0005,
            slippage=0.0005,
            risk_pct=1.5,
            use_compound=True,
            use_credal=False,
        )

        # Generate signals on synthetic data
        alpha_engine = QlibSMCAlphaPipeline(config=QlibSMCConfig(swing_len=5, use_credal_filter=False))
        df_with_signals = alpha_engine.generate_signals(self.bars)

        # Map signal column to Round2 engine expectation if needed
        # Round2 engine recognizes "Signal", "limit_entry_px", "stop_loss", "tp1", "tp2"
        # In QlibSMCAlphaEngine, signal is 1, -1, 0. Let's map to LONG, SHORT, NEUTRAL
        df_run = df_with_signals.copy()
        if "signal" in df_run.columns:
            df_run["Signal"] = df_run["signal"].map({1: "LONG", -1: "SHORT", 0: "NEUTRAL"}).fillna("NEUTRAL")

        # Set limit prices and stops if not present
        if "limit_entry_px" not in df_run.columns or df_run["limit_entry_px"].isna().all():
            df_run["limit_entry_px"] = df_run["Close"]
        if "stop_loss" not in df_run.columns or df_run["stop_loss"].isna().all():
            df_run["stop_loss"] = np.where(df_run["Signal"] == "LONG", df_run["Close"] * 0.98, df_run["Close"] * 1.02)
        if "tp1" not in df_run.columns or df_run["tp1"].isna().all():
            df_run["tp1"] = np.where(df_run["Signal"] == "LONG", df_run["Close"] * 1.02, df_run["Close"] * 0.98)
        if "tp2" not in df_run.columns or df_run["tp2"].isna().all():
            df_run["tp2"] = np.where(df_run["Signal"] == "LONG", df_run["Close"] * 1.04, df_run["Close"] * 0.96)

        res = engine.run(df_run)

        # Check balance conservation invariant
        audit_res = verify_accounting_conservation_invariant(
            engine_result=res,
            initial_cash=1000.0,
            tolerance=1e-5,
        )

        self.assertTrue(
            audit_res["passed"],
            f"Accounting conservation invariant failed! Discrepancy: {audit_res['discrepancy']}, "
            f"trade discrepancies: {audit_res['trade_discrepancies']}",
        )
        self.assertAlmostEqual(audit_res["discrepancy"], 0.0, places=5)

    def test_intra_bar_pessimism_stop_loss_resolution(self) -> None:
        """4. Verify pessimistic intra-bar execution check (TP & SL on same bar -> SL hit)."""
        audit_res = verify_intra_bar_pessimism_invariant(PessimisticExecutionEngine)

        self.assertTrue(
            audit_res["passed"],
            f"Pessimistic intra-bar invariant failed! Long passed: {audit_res['long_passed']} "
            f"({audit_res['long_exit_reason']}), Short passed: {audit_res['short_passed']} "
            f"({audit_res['short_exit_reason']})",
        )
        self.assertTrue(audit_res["long_passed"])
        self.assertTrue(audit_res["short_passed"])


if __name__ == "__main__":
    unittest.main()
