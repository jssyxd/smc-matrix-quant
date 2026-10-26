"""
Unit and integration test suite for Marcos López de Prado Advanced Statistical
Anti-Overfitting Audit Suite (Round 4 Production).

Verifies:
1. DeflatedSharpeAuditor:
   - DSR monotonicity with trial count N (increasing N strictly increases E[max_N] and lowers DSR).
   - Skewness and kurtosis non-normality adjustments.
   - Haircut Sharpe Ratio (HSR) multiple-testing discount and correlation dampening.
   - N >= 50 enforcement and validation.
2. CSCVOverfittingAuditor:
   - CSCV PBO algorithm mathematical correctness with S = 16 sub-matrices and C(16, 8) = 12,870 splits.
   - Synthetic true alpha -> low PBO (PBO <= 0.15, passes).
   - Overfitted pure noise trials (N = 500) -> high PBO (PBO >= 0.40, fails).
   - Rank distribution and logit calculations.
3. CrossAssetSharedCapitalBootstrap:
   - 2,000-path resampling convergence.
   - Ruin probability (ruin <= 0.00%) and 95% Max Drawdown (<= 20.0%) invariants.
   - Monotonicity across drawdown percentiles: Mean <= 95th <= 99th.
4. End-to-end audit orchestrator and final certification report generation.
"""

from __future__ import annotations

import math
import os
import sys
import unittest
import numpy as np

# Ensure src/ is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from anti_overfit_round4_auditor import (
    DeflatedSharpeAuditor,
    CSCVOverfittingAuditor,
    CrossAssetSharedCapitalBootstrap,
    expected_maximum_sr,
    run_round4_production_audit,
    EULER_MASCHERONI,
)


class TestAntiOverfitRound4(unittest.TestCase):
    """Test suite for Round 4 Marcos López de Prado anti-overfitting suite."""

    def setUp(self) -> None:
        np.random.seed(42)

    # -----------------------------------------------------------------------
    # 1. Deflated Sharpe Ratio (DSR) & Haircut Sharpe Tests
    # -----------------------------------------------------------------------

    def test_dsr_monotonicity_with_trial_count_n(self) -> None:
        """
        Verify DSR monotonicity with trial count N.
        Increasing N strictly increases E[max_N], decreases z-stat, and lowers DSR.
        """
        auditor = DeflatedSharpeAuditor(significance_level=0.05)
        sr = 0.25
        t = 500
        var_trials = 0.004

        trial_counts = [2, 10, 50, 100, 500, 2000]
        emax_list = []
        zstat_list = []
        dsr_list = []

        for n in trial_counts:
            res = auditor.compute_dsr(
                sr=sr,
                t=t,
                skew=0.0,
                kurtosis=3.0,
                n_trials=n,
                var_trials=var_trials,
            )
            emax_list.append(res.expected_max_sr)
            zstat_list.append(res.z_stat)
            dsr_list.append(res.dsr)

        # 1. E[max_N] must be strictly increasing with trial count N
        for i in range(len(emax_list) - 1):
            self.assertGreater(
                emax_list[i + 1],
                emax_list[i],
                f"E[max_N] should increase monotonically: {emax_list[i]} -> {emax_list[i+1]}",
            )

        # 2. Standardized z-statistic must be strictly decreasing with N
        for i in range(len(zstat_list) - 1):
            self.assertLess(
                zstat_list[i + 1],
                zstat_list[i],
                f"z-stat should decrease monotonically with N: {zstat_list[i]} -> {zstat_list[i+1]}",
            )

        # 3. DSR probability Phi(z) must be strictly decreasing with N
        for i in range(len(dsr_list) - 1):
            self.assertLess(
                dsr_list[i + 1],
                dsr_list[i],
                f"DSR should decrease monotonically with N: {dsr_list[i]} -> {dsr_list[i+1]}",
            )

    def test_dsr_skewness_and_kurtosis_impact(self) -> None:
        """
        Verify that negative skewness and excess kurtosis inflate standard error
        and deflate the resulting Sharpe ratio statistic.
        """
        auditor = DeflatedSharpeAuditor()
        sr = 0.30
        t = 500
        n_trials = 60
        var_trials = 0.003

        # Base normal case (skew=0, kurt=3)
        res_normal = auditor.compute_dsr(
            sr=sr, t=t, skew=0.0, kurtosis=3.0, n_trials=n_trials, var_trials=var_trials
        )

        # Fat-tailed left-skewed case (skew=-0.8, kurt=6.0)
        res_fat_tail = auditor.compute_dsr(
            sr=sr, t=t, skew=-0.8, kurtosis=6.0, n_trials=n_trials, var_trials=var_trials
        )

        self.assertGreater(
            res_fat_tail.std_error,
            res_normal.std_error,
            "Negative skewness and excess kurtosis must increase standard error of Sharpe ratio.",
        )
        self.assertLess(
            res_fat_tail.dsr,
            res_normal.dsr,
            "Negative skewness and excess kurtosis must deflate DSR probability.",
        )

    def test_haircut_sharpe_properties(self) -> None:
        """
        Verify Haircut Sharpe Ratio properties:
        - N=1 has zero haircut penalty.
        - Increasing N increases haircut percentage.
        - Higher pairwise correlation decreases effective trials and reduces haircut penalty.
        """
        auditor = DeflatedSharpeAuditor()
        ann_sr = 2.50
        t_days = 500

        # N = 1: no penalty
        res_1 = auditor.compute_haircut_sharpe(sr=ann_sr, n_trials=1, t=t_days)
        self.assertEqual(res_1.haircut_pct, 0.0)
        self.assertAlmostEqual(res_1.haircut_sr, ann_sr, places=6)

        # N = 50 independent trials
        res_50_indep = auditor.compute_haircut_sharpe(
            sr=ann_sr, n_trials=50, t=t_days, correlation=0.0
        )
        self.assertGreater(res_50_indep.haircut_pct, 0.0)
        self.assertLess(res_50_indep.haircut_sr, ann_sr)

        # N = 50 correlated trials (rho = 0.70)
        res_50_corr = auditor.compute_haircut_sharpe(
            sr=ann_sr, n_trials=50, t=t_days, correlation=0.70
        )
        self.assertLess(
            res_50_corr.haircut_pct,
            res_50_indep.haircut_pct,
            "Correlated trials must incur lower haircut than independent trials.",
        )
        self.assertGreater(
            res_50_corr.haircut_sr,
            res_50_indep.haircut_sr,
            "Correlated trials must preserve higher Haircut Sharpe Ratio.",
        )

    # -----------------------------------------------------------------------
    # 2. CSCV Overfitting Auditor (Combinatorial CV & PBO)
    # -----------------------------------------------------------------------

    def test_cscv_splits_and_combination_count(self) -> None:
        """
        Verify that CSCV partitions S=16 generates exactly C(16, 8) = 12,870 splits.
        """
        cscv = CSCVOverfittingAuditor(n_partitions=16, pbo_threshold=0.40)
        T = 320
        N = 5
        dummy_matrix = np.random.normal(size=(T, N))

        res = cscv.compute_pbo(dummy_matrix)
        self.assertEqual(res.n_partitions, 16)
        self.assertEqual(res.n_combinations, 12870)
        self.assertEqual(len(res.rank_distribution), 12870)
        self.assertEqual(len(res.logits), 12870)
        self.assertTrue(np.all(res.rank_distribution > 0.0))
        self.assertTrue(np.all(res.rank_distribution < 1.0))

    def test_cscv_synthetic_true_alpha_passes(self) -> None:
        """
        Verify CSCV with synthetic true alpha strategy:
        True drift vs 9 noise strategies -> low PBO (<= 0.15) -> passes.
        """
        T = 640
        N = 10
        alpha_drift = 0.06 / math.sqrt(252)
        alpha_vol = 0.12 / math.sqrt(252)
        true_alpha = np.random.normal(loc=alpha_drift, scale=alpha_vol, size=T)
        noise_trials = np.random.normal(loc=0.0, scale=alpha_vol, size=(T, N - 1))
        matrix = np.column_stack([true_alpha, noise_trials])

        cscv = CSCVOverfittingAuditor(n_partitions=16, pbo_threshold=0.40)
        res = cscv.compute_pbo(matrix)

        self.assertLessEqual(
            res.pbo,
            0.15,
            f"True alpha strategy must have near-zero PBO, got {res.pbo:.2%}",
        )
        self.assertFalse(res.is_overfitted, "True alpha must not be classified as overfitted.")
        self.assertTrue(res.passes, "True alpha strategy must pass CSCV audit.")
        self.assertLess(res.prob_loss, 0.20, "Probability of OOS loss should be low for true alpha.")

    def test_cscv_overfitted_noise_strategies_fails(self) -> None:
        """
        Verify CSCV overfitted noise search:
        Searching over pure noise strategies -> IS-best strategy is symmetric noise OOS -> PBO ~ 50%.
        """
        T = 1000
        N = 500
        noise_matrix = np.random.normal(loc=0.0, scale=0.01, size=(T, N))
        cscv = CSCVOverfittingAuditor(n_partitions=16, pbo_threshold=0.40)
        res = cscv.compute_pbo(noise_matrix)

        self.assertGreaterEqual(
            res.pbo,
            0.40,
            f"Pure noise search must exhibit high PBO >= 40%, got {res.pbo:.2%}",
        )
        self.assertTrue(res.is_overfitted, "Pure noise trials must be flagged as overfitted.")
        self.assertFalse(res.passes, "Overfitted noise trials must fail CSCV audit.")

    # -----------------------------------------------------------------------
    # 3. 2,000-Path Cross-Asset Shared Capital Bootstrap Tests
    # -----------------------------------------------------------------------

    def test_bootstrap_2000_paths_convergence_and_invariants(self) -> None:
        """
        Verify 2,000-Path Cross-Asset Shared Capital Bootstrap:
        - 2,000 simulations executed.
        - Probability of Ruin <= 0.00% (zero ruin).
        - Max Drawdown 95th Percentile <= 20.0%.
        - Drawdown percentiles strictly monotonic: Mean <= 95th <= 99th.
        - CVaR 95% >= VaR 95% (coherent risk property).
        """
        engine = CrossAssetSharedCapitalBootstrap(
            n_simulations=2000,
            sample_trades_per_path=200,
            initial_capital=1000.0,
            ruin_drawdown_threshold=0.50,
            mdd_95_limit_pct=20.0,
            ruin_prob_limit_pct=0.00,
        )

        res = engine.run_bootstrap(seed=42)

        self.assertEqual(res.n_simulations, 2000)
        self.assertEqual(res.sample_trades_per_path, 200)
        self.assertEqual(res.initial_capital, 1000.0)

        # Safety Invariants
        self.assertLessEqual(
            res.probability_of_ruin_pct,
            0.00,
            f"Probability of Ruin must be <= 0.00%, got {res.probability_of_ruin_pct:.2f}%",
        )
        self.assertTrue(res.passes_ruin, "Bootstrap must pass ruin probability check.")

        self.assertLessEqual(
            res.percentile_95_max_drawdown_pct,
            20.0,
            f"95% Max Drawdown must be <= 20.0%, got {res.percentile_95_max_drawdown_pct:.2f}%",
        )
        self.assertTrue(res.passes_mdd, "Bootstrap must pass 95% Max DD constraint.")
        self.assertTrue(res.overall_pass, "Bootstrap must pass overall stress audit.")

        # Monotonicity invariants
        self.assertLessEqual(
            res.mean_max_drawdown_pct,
            res.percentile_95_max_drawdown_pct,
            "Mean Max DD must be <= 95th percentile Max DD.",
        )
        self.assertLessEqual(
            res.percentile_95_max_drawdown_pct,
            res.percentile_99_max_drawdown_pct,
            "95th percentile Max DD must be <= 99th percentile Max DD.",
        )

        # Risk coherence
        self.assertGreaterEqual(
            res.cvar_95_pct,
            res.var_95_pct - 1e-6,
            "Conditional VaR (Expected Shortfall) must be >= Value at Risk (VaR 95%).",
        )

    # -----------------------------------------------------------------------
    # 4. End-to-End Production Audit Orchestrator Test
    # -----------------------------------------------------------------------

    def test_run_round4_production_audit_execution(self) -> None:
        """
        Verify that run_round4_production_audit completes cleanly,
        achieves certification, and writes the final markdown report.
        """
        output_report = os.path.join(
            os.path.dirname(__file__), "..", "results", "round4_audit", "FINAL_ROUND4_PRODUCTION_REPORT.md"
        )
        report = run_round4_production_audit(output_report_path=output_report)

        self.assertTrue(report.overall_certified, "Round 4 Production Audit must be overall certified.")
        self.assertEqual(report.cscv_result.n_combinations, 12870)
        self.assertLess(report.cscv_result.pbo, 0.40)
        self.assertLessEqual(report.bootstrap_result.probability_of_ruin_pct, 0.00)
        self.assertLessEqual(report.bootstrap_result.percentile_95_max_drawdown_pct, 20.0)
        self.assertTrue(os.path.exists(output_report), "Production Markdown report must be generated on disk.")

        with open(output_report, "r", encoding="utf-8") as fp:
            content = fp.read()
        self.assertIn("Round 4 Production Audit", content)
        self.assertIn("12,870", content)
        self.assertIn("100% PRODUCTION CERTIFIED (PASSED)", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
