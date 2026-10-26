"""
Tests for Research Director Strategy & Anti-Overfitting Audit Suite.
Verifies all 5 auditing dimensions:
1. Real Market Fillability Auditor (Yahoo Finance matching).
2. Rolling Window Walk-Forward Auditor.
3. Anti-Lookahead Rearview Auditor.
4. Statistical Overfit Auditor (CSCV, PBO, DSR, Monte Carlo).
5. Composite Anti-Overfitting Score Invariant.
"""

from __future__ import annotations

import os
import sys
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.research_director_audit import (
    YahooMarketFeasibilityAuditor,
    RollingWindowWalkForwardAuditor,
    AntiLookaheadRearviewAuditor,
    StatisticalOverfitAuditor,
    compute_composite_anti_overfitting_score,
    run_full_research_director_audit,
)


class TestResearchDirectorAudit(unittest.TestCase):
    def setUp(self) -> None:
        np.random.seed(42)

    def test_market_fillability_auditor(self) -> None:
        auditor = YahooMarketFeasibilityAuditor(bars_dir="data/yahoo_bars")
        self.assertGreater(len(auditor.cached_bars), 0)
        res = auditor.audit_trades_log("results/ross_momentum_backtests/ross_alpaca_trades_log.json")
        self.assertGreater(res.total_trades_audited, 0)
        self.assertGreater(res.matched_timestamps, 0)
        self.assertGreaterEqual(res.fillability_rate, 0.0)
        self.assertLessEqual(res.fillability_rate, 1.0)
        self.assertIn("ZTG", res.details_per_symbol)

    def test_rolling_window_walk_forward(self) -> None:
        auditor = RollingWindowWalkForwardAuditor(num_folds=3, is_ratio=0.60)
        # Load ZTG bars
        df = pd.read_parquet("data/yahoo_bars/ZTG_1m.parquet")
        df.columns = [c.lower() for c in df.columns]
        res = auditor.run_walk_forward(df.iloc[:300], symbol="ZTG")
        self.assertEqual(res.num_folds, 3)
        self.assertGreaterEqual(res.walk_forward_efficiency, 0.0)

    def test_anti_lookahead_auditor(self) -> None:
        auditor = AntiLookaheadRearviewAuditor()
        df = pd.read_parquet("data/yahoo_bars/ZTG_1m.parquet")
        df.columns = [c.lower() for c in df.columns]
        res = auditor.audit_strategy_causality(df.iloc[:200], symbol="ZTG")
        self.assertGreaterEqual(res.lookahead_pass_rate, 0.80)
        self.assertEqual(res.pessimistic_intra_bar_tests_passed, 3)

    def test_statistical_overfit_auditor(self) -> None:
        auditor = StatisticalOverfitAuditor()
        rng = np.random.RandomState(42)
        returns = rng.normal(0.001, 0.02, size=100)
        res = auditor.audit_statistics(returns, num_trials=20)
        self.assertGreaterEqual(res.pbo, 0.0)
        self.assertLessEqual(res.pbo, 1.0)
        self.assertGreaterEqual(res.deflated_sharpe_ratio, 0.0)
        self.assertLessEqual(res.deflated_sharpe_ratio, 1.0)
        self.assertLessEqual(res.ruin_probability, 0.05)

    def test_composite_score_bounds(self) -> None:
        score = compute_composite_anti_overfitting_score(
            fillability_rate=1.0,
            walk_forward_efficiency=1.0,
            pbo=0.10,
            deflated_sharpe=0.95,
            lookahead_pass_rate=1.0,
            max_drawdown_95=0.10,
            ruin_probability=0.0,
        )
        self.assertGreaterEqual(score, 90.0)
        self.assertLessEqual(score, 100.0)

    def test_full_audit_execution(self) -> None:
        report = run_full_research_director_audit()
        self.assertIsNotNone(report.anti_overfitting_score)
        self.assertIn(report.summary_verdict, ["PASSED", "FAILED_OVERFITTING_RISK"])


if __name__ == "__main__":
    unittest.main()
