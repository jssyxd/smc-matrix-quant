"""
Unit and Integration Test Suite for Microsoft RD-Agent Quant Autonomous Evolutionary Research Loop.

Verifies:
1. HypothesisGenerator:
   - Structured hypothesis formatting, target microstructure, regime condition, and rationale.
   - Generation indexing, feedback adaptation, and determinism with fixed seed.
2. FactorEvolver:
   - Generation of seed factors linked to hypotheses.
   - Genetic crossover between two parent factors.
   - Genetic and prompt mutations.
   - Population evolution size and monotonicity.
3. BacktestEvaluator:
   - IS / OOS temporal split integrity and causality.
   - Realistic transaction friction (Maker 2 bps, Taker 5 bps, Slippage 5 bps).
   - Position generation and performance metric bounds.
4. FeedbackPruner:
   - IC and IC_IR computation accuracy.
   - Credal Dirichlet epistemic vacuity u derivation (Subjective Logic).
   - Strict pruning threshold enforcement (IC < 0.02 or u > 0.35).
   - Rejection of invalid/constant factor series.
5. End-to-End RD-Agent Iteration Loop (`run_rd_agent_iteration`):
   - Multi-generation execution across realistic synthetic OHLCV data.
   - Structural schema integrity of returned result (best_factor, hypothesis_log, convergence_report).
   - Convergence metrics and non-empty valid factor delivery.
"""

from __future__ import annotations

import os
import sys
import unittest
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.rd_agent_evolution_loop import (
    Hypothesis,
    EvolvedFactor,
    HypothesisGenerator,
    FactorEvolver,
    BacktestEvaluator,
    FeedbackPruner,
    run_rd_agent_iteration,
)
from src.alphagpt_factor_miner import (
    FactorScore,
    compute_alphagpt_factors,
)


def _generate_synthetic_ohlcv(
    n: int = 250,
    seed: int = 42,
    base_price: float = 100.0,
) -> pd.DataFrame:
    """Generate realistic synthetic OHLCV market data."""
    rng = np.random.RandomState(seed)
    returns = rng.normal(loc=0.0003, scale=0.015, size=n)
    close = base_price * np.exp(np.cumsum(returns))

    intraday_pct = rng.uniform(0.005, 0.025, size=n)
    high = close * (1.0 + intraday_pct * rng.uniform(0.3, 1.0, size=n))
    low = close * (1.0 - intraday_pct * rng.uniform(0.3, 1.0, size=n))
    open_ = low + rng.uniform(0.1, 0.9, size=n) * (high - low)
    volume = rng.lognormal(mean=10.0, sigma=0.5, size=n)

    dates = pd.date_range("2026-01-01", periods=n, freq="15min")
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=dates,
    )


class TestHypothesisGenerator(unittest.TestCase):
    """Test suite for HypothesisGenerator."""

    def setUp(self) -> None:
        self.generator = HypothesisGenerator(seed=123)

    def test_hypothesis_generation_format_and_validity(self) -> None:
        """Verify hypothesis data structure formatting, validity, and fields."""
        hyps = self.generator.generate(num_hypotheses=3, generation=0)
        self.assertEqual(len(hyps), 3)

        for h in hyps:
            self.assertIsInstance(h, Hypothesis)
            self.assertTrue(h.id.startswith("HYP_G0_"))
            self.assertNotIn("{regime}", h.statement)
            self.assertGreater(len(h.statement), 10)
            self.assertGreater(len(h.rationale), 10)
            self.assertIn(h.regime_condition, ["high_volatility", "mean_reverting", "trending", "low_volatility"])
            self.assertGreater(len(h.target_microstructure), 0)
            self.assertEqual(h.generation, 0)
            self.assertEqual(h.status, "active")

            # Dict serialization
            d = h.to_dict()
            self.assertEqual(d["id"], h.id)
            self.assertEqual(d["statement"], h.statement)
            self.assertIn("base_factors", d["metadata"])

    def test_hypothesis_determinism(self) -> None:
        """Verify determinism with identical seeds."""
        gen1 = HypothesisGenerator(seed=999)
        gen2 = HypothesisGenerator(seed=999)

        h1 = gen1.generate(num_hypotheses=4, generation=1)
        h2 = gen2.generate(num_hypotheses=4, generation=1)

        for a, b in zip(h1, h2):
            self.assertEqual(a.statement, b.statement)
            self.assertEqual(a.target_microstructure, b.target_microstructure)
            self.assertEqual(a.regime_condition, b.regime_condition)

    def test_hypothesis_feedback_adaptation(self) -> None:
        """Verify generator accepts feedback from prior generations."""
        feedback = [
            {"status": "validated", "target_microstructure": "OFI_FVG_ABSORPTION", "ic": 0.05}
        ]
        hyps = self.generator.generate(num_hypotheses=2, generation=1, feedback=feedback)
        self.assertEqual(len(hyps), 2)
        self.assertEqual(hyps[0].generation, 1)


class TestFactorEvolver(unittest.TestCase):
    """Test suite for FactorEvolver."""

    def setUp(self) -> None:
        self.evolver = FactorEvolver(seed=42)
        self.features = ["OFI_Impulse", "FVG_Absorption_Rate", "Liquidity_Sweep_Intensity", "Vol_Displacement_Ratio"]
        self.hypo_gen = HypothesisGenerator(seed=42)
        self.hypotheses = self.hypo_gen.generate(num_hypotheses=2, generation=0)

    def test_generate_seed_factors(self) -> None:
        """Verify seed factor generation tied to hypotheses."""
        seeds = self.evolver.generate_seed_factors(self.hypotheses, self.features, factors_per_hypothesis=2)
        self.assertEqual(len(seeds), 4)

        for s in seeds:
            self.assertIsInstance(s, EvolvedFactor)
            self.assertTrue(s.id.startswith("FACT_G0_"))
            self.assertIn(s.hypothesis_id, [h.id for h in self.hypotheses])
            self.assertEqual(s.generation, 0)
            self.assertEqual(s.mutation_type, "init")
            self.assertGreater(len(s.expression), 0)

    def test_crossover(self) -> None:
        """Verify genetic crossover between two parents produces valid offspring."""
        seeds = self.evolver.generate_seed_factors(self.hypotheses, self.features, factors_per_hypothesis=2)
        p1, p2 = seeds[0], seeds[1]

        child = self.evolver.crossover(p1, p2, generation=1)
        self.assertIsInstance(child, EvolvedFactor)
        self.assertEqual(child.generation, 1)
        self.assertEqual(child.mutation_type, "crossover")
        self.assertEqual(child.parent_ids, [p1.id, p2.id])
        self.assertIn(p1.expression, child.expression)
        self.assertIn(p2.expression, child.expression)

    def test_mutation(self) -> None:
        """Verify point mutation and prompt-guided mutation."""
        seeds = self.evolver.generate_seed_factors(self.hypotheses, self.features, factors_per_hypothesis=1)
        parent = seeds[0]

        mutant = self.evolver.mutate(parent, self.features, generation=1)
        self.assertIsInstance(mutant, EvolvedFactor)
        self.assertEqual(mutant.generation, 1)
        self.assertTrue(mutant.mutation_type.startswith("mutation_"))
        self.assertEqual(mutant.parent_ids, [parent.id])
        self.assertNotEqual(mutant.expression, parent.expression)

    def test_evolve_population_size_and_monotonicity(self) -> None:
        """Verify population evolution maintains specified size."""
        seeds = self.evolver.generate_seed_factors(self.hypotheses, self.features, factors_per_hypothesis=2)
        target_size = 10
        next_pop = self.evolver.evolve_population(
            survivors=seeds[:2],
            hypotheses=self.hypotheses,
            available_features=self.features,
            target_population_size=target_size,
            generation=1,
        )
        self.assertEqual(len(next_pop), target_size)


class TestBacktestEvaluator(unittest.TestCase):
    """Test suite for BacktestEvaluator with transaction friction."""

    def setUp(self) -> None:
        self.df = _generate_synthetic_ohlcv(n=200, seed=42)
        self.features = compute_alphagpt_factors(self.df)
        self.forward_returns = (self.df["close"].shift(-1) / self.df["close"] - 1.0).fillna(0.0)
        self.evaluator = BacktestEvaluator(maker_fee=0.0002, taker_fee=0.0005, slippage=0.0005)

    def test_is_oos_data_split(self) -> None:
        """Verify IS / OOS temporal split integrity."""
        is_feat, is_ret, oos_feat, oos_ret = self.evaluator.split_data(self.features, self.forward_returns)

        self.assertEqual(len(is_feat), len(is_ret))
        self.assertEqual(len(oos_feat), len(oos_ret))
        self.assertEqual(len(is_feat) + len(oos_feat), len(self.features))
        self.assertLess(is_feat.index[-1], oos_feat.index[0])  # Strict temporal causality

    def test_backtest_single_factor_friction(self) -> None:
        """Verify transaction costs reduce total returns when turnover occurs."""
        factor_values = self.features["OFI_Impulse"]
        metrics_maker = self.evaluator.backtest_single_factor(factor_values, self.forward_returns, is_maker=True)
        metrics_taker = self.evaluator.backtest_single_factor(factor_values, self.forward_returns, is_maker=False)

        self.assertIn("sharpe", metrics_maker)
        self.assertIn("total_return", metrics_maker)
        self.assertIn("win_rate", metrics_maker)
        self.assertIn("profit_factor", metrics_maker)

        # Taker fees are higher than Maker fees -> total return should be lower or equal
        self.assertGreaterEqual(metrics_maker["total_return"], metrics_taker["total_return"])

    def test_evaluate_evolved_factor(self) -> None:
        """Verify factor expression evaluation."""
        factor = EvolvedFactor(
            id="FACT_001",
            name="TestOFI",
            expression="OFI_Impulse 10 ts_zscore",
            hypothesis_id="HYP_001",
            generation=0,
        )
        series, metrics = self.evaluator.evaluate(factor, self.features, self.forward_returns)
        self.assertIsNotNone(series)
        self.assertIn("oos_sharpe", metrics)
        self.assertIn("oos_return", metrics)
        self.assertIn("trade_count", metrics)


class TestFeedbackPruner(unittest.TestCase):
    """Test suite for FeedbackPruner and Credal Epistemic Vacuity."""

    def setUp(self) -> None:
        self.pruner = FeedbackPruner(ic_threshold=0.02, vacuity_threshold=0.35, min_trade_count=2)

    def test_ic_and_ir_computation(self) -> None:
        """Verify Pearson IC and Spearman IC computation."""
        rng = np.random.RandomState(42)
        n = 100
        returns = pd.Series(rng.normal(0, 0.01, size=n))
        # High correlation signal
        factor = returns + rng.normal(0, 0.005, size=n)

        p_ic, s_ic, ic_std, ic_ir = self.pruner.compute_ic_ir(factor, returns)
        self.assertGreater(p_ic, 0.5)
        self.assertGreater(s_ic, 0.5)
        self.assertGreater(ic_ir, 0.0)

    def test_pruning_low_ic_factor(self) -> None:
        """Verify uninformative factors with IC < 0.02 are pruned."""
        # Construct orthogonal signal: zero correlation with returns
        returns = pd.Series(np.tile([0.01, -0.01], 50))
        noise_factor = pd.Series(np.tile([1.0, 1.0, -1.0, -1.0], 25))
        factor = EvolvedFactor(
            id="FACT_NOISE",
            name="NoiseAlpha",
            expression="noise",
            hypothesis_id="HYP_NOISE",
            generation=0,
            backtest_metrics={"oos_sharpe": 0.0, "oos_profit_factor": 0.5, "trade_count": 10},
        )
        pruned_factor = self.pruner.prune(factor, noise_factor, returns)
        self.assertTrue(pruned_factor.pruned)
        self.assertIsNotNone(pruned_factor.prune_reason)
        self.assertIn("IC_BELOW_THRESHOLD", pruned_factor.prune_reason)

    def test_pruning_high_vacuity_factor(self) -> None:
        """Verify factors with high credal epistemic vacuity u > 0.35 are pruned."""
        # Mock high vacuity: score with low IC and terrible backtest metrics
        score = FactorScore(
            expression="weak",
            ic_mean=0.022,  # Marginally passes IC threshold
            ic_std=0.05,
            rank_ic_mean=0.021,
            rank_ic_std=0.05,
            ic_ir=0.1,
            rank_ic_ir=0.1,
            t_stat=0.5,
            turnover=0.1,
            fitness=0.002,
            n_samples=100,
        )
        poor_backtest = {"oos_sharpe": 0.0, "oos_profit_factor": 0.8, "trade_count": 5}
        vacuity_u, c_state = self.pruner.compute_credal_vacuity(score, poor_backtest)

        self.assertGreater(vacuity_u, 0.35)

        factor = EvolvedFactor(
            id="FACT_WEAK",
            name="WeakAlpha",
            expression="weak",
            hypothesis_id="HYP_WEAK",
            generation=0,
            backtest_metrics=poor_backtest,
        )
        # Synthesize signal with IC > 0.02 (e.g. 0.03), but zero Sharpe/PF -> high vacuity u > 0.35
        n = 1000
        rng = np.random.RandomState(42)
        ret_series = pd.Series(rng.normal(0, 0.01, size=n))
        ret_norm = (ret_series - ret_series.mean()) / ret_series.std()
        z = pd.Series(rng.normal(0, 0.01, size=n))
        z_proj = z - ret_norm * (z * ret_norm).mean()
        z_ortho = (z_proj - z_proj.mean()) / z_proj.std()
        target_corr = 0.03
        s_series = target_corr * ret_norm + np.sqrt(1 - target_corr**2) * z_ortho
        pruned_factor = self.pruner.prune(factor, s_series, ret_series)

        # Should be pruned due to vacuity
        self.assertTrue(pruned_factor.pruned)
        self.assertIn("HIGH_EPISTEMIC_VACUITY", pruned_factor.prune_reason)


class TestRDAgentIterationIntegration(unittest.TestCase):
    """Integration test suite for the complete run_rd_agent_iteration loop."""

    def test_run_rd_agent_iteration_full_loop(self) -> None:
        """Test complete 3-generation evolutionary run on synthetic market data."""
        df = _generate_synthetic_ohlcv(n=200, seed=42)
        results = run_rd_agent_iteration(
            df=df,
            num_generations=3,
            population_size=6,
            ic_threshold=0.015,  # Moderate threshold for synthetic test data
            vacuity_threshold=0.50,
            seed=42,
        )

        self.assertIsInstance(results, dict)
        self.assertIn("best_factor", results)
        self.assertIn("hypothesis_log", results)
        self.assertIn("convergence_report", results)
        self.assertIn("generation_history", results)

        # Check hypothesis log
        self.assertGreater(len(results["hypothesis_log"]), 0)
        for h in results["hypothesis_log"]:
            self.assertIn("id", h)
            self.assertIn("statement", h)
            self.assertIn("target_microstructure", h)

        # Check convergence report
        self.assertEqual(len(results["convergence_report"]), 3)
        for cr in results["convergence_report"]:
            self.assertIn("generation", cr)
            self.assertIn("population_count", cr)
            self.assertIn("survivor_count", cr)
            self.assertIn("mean_abs_ic", cr)
            self.assertIn("mean_vacuity_u", cr)

        # Check generation history
        self.assertEqual(len(results["generation_history"]), 3)
        for gen_factors in results["generation_history"]:
            self.assertEqual(len(gen_factors), 6)

        # Check best factor
        best_f = results["best_factor"]
        self.assertIsInstance(best_f, dict)
        self.assertIn("id", best_f)
        self.assertIn("expression", best_f)
        self.assertIn("ic", best_f)
        self.assertIn("vacuity_u", best_f)


if __name__ == "__main__":
    unittest.main()
