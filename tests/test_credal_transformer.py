"""
Unit tests for Credal Transformer & Subjective Logic Auditing Module.

Verifies:
1. Mathematical invariant: sum(b_k) + u == 1.0 (Strict Subjective Logic conservation law).
2. Epistemic uncertainty monotonicity: as evidence increases, u -> 0.
3. Zero evidence state: u = 1.0, b_k = 0.
4. Abstention behavior on conflicting/noisy inputs (vacuity > 0.35 or conflict > 0.40).
5. High conviction approval behavior.
6. Empirical PnL distribution auditing against vacuous priors (overfitting detection).
"""

from __future__ import annotations

import os
import sys
import unittest
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.credal_transformer_auditor import (
    CredalEvidenceModel,
    CredalAuditGate,
    CredalEvidenceState,
)


class TestCredalTransformerAuditor(unittest.TestCase):
    """Test suite validating CredalEvidenceModel and CredalAuditGate."""

    def setUp(self) -> None:
        self.model = CredalEvidenceModel(K=3, eps=1e-9)
        self.gate = CredalAuditGate(K=3, threshold_conflict=0.40, eps=1e-9)

    def test_mathematical_invariant_conservation_law(self) -> None:
        """1. Mathematical invariant: sum(b_k) + u == 1.0 (Strict Subjective Logic conservation law)."""
        test_vectors = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [5.0, 2.0, 1.0],
            [10.5, 0.2, 3.8],
            [100.0, 50.0, 25.0],
            [0.001, 0.001, 0.001],
            [1e-6, 0.0, 0.0],
        ]

        for e_vec in test_vectors:
            state = self.model.evaluate_evidence(e_vec)
            total_mass = float(np.sum(state.beliefs) + state.vacuity)
            self.assertAlmostEqual(
                total_mass,
                1.0,
                places=9,
                msg=f"Conservation law violated for e={e_vec}: sum(b_k) + u = {total_mass}",
            )
            # Probability conservation: sum(p_k) == 1.0
            sum_p = float(np.sum(state.expected_probs))
            self.assertAlmostEqual(
                sum_p,
                1.0,
                places=9,
                msg=f"Probability law violated for e={e_vec}: sum(p_k) = {sum_p}",
            )

    def test_epistemic_uncertainty_monotonicity(self) -> None:
        """2. Epistemic uncertainty monotonicity: as evidence increases, u -> 0."""
        evidence_magnitudes = [0.0, 1.0, 5.0, 10.0, 50.0, 200.0, 1000.0]
        vacuities = []

        for mag in evidence_magnitudes:
            state = self.model.evaluate_evidence([mag, 0.0, 0.0])
            vacuities.append(state.vacuity)

        # Ensure strict decreasing order: u_1 > u_2 > ... > u_N
        for i in range(len(vacuities) - 1):
            self.assertGreater(
                vacuities[i],
                vacuities[i + 1],
                f"Monotonicity failed between mag {evidence_magnitudes[i]} and {evidence_magnitudes[i+1]}",
            )

        # As evidence -> large, u -> 0
        self.assertLess(vacuities[-1], 0.01)

    def test_zero_evidence_state(self) -> None:
        """3. Zero evidence state: u = 1.0, b_k = 0."""
        state = self.model.evaluate_evidence([0.0, 0.0, 0.0])

        self.assertAlmostEqual(state.vacuity, 1.0, places=9)
        for b in state.beliefs:
            self.assertAlmostEqual(b, 0.0, places=9)

        # Dirichlet strength S = K
        self.assertAlmostEqual(state.strength, float(self.model.K), places=9)

        # Alphas should all be 1.0 (uninformative uniform Dirichlet prior)
        for alpha in state.alphas:
            self.assertAlmostEqual(alpha, 1.0, places=9)

        # Expected probabilities should be uniform (1/K)
        for p in state.expected_probs:
            self.assertAlmostEqual(p, 1.0 / self.model.K, places=9)

        # Conflict is 0 in absence of belief
        self.assertAlmostEqual(state.pairwise_conflict, 0.0, places=9)

    def test_abstention_on_high_vacuity(self) -> None:
        """4a. Abstention behavior on high vacuity (sparse / weak evidence)."""
        # Weak evidence: S = 0.5 + 3 = 3.5, u = 3 / 3.5 = 0.857 > 0.35
        weak_evidence = {"evidence": [0.5, 0.0, 0.0]}
        passed, res = self.gate.audit_trade_signal(weak_evidence, threshold_u=0.35)

        self.assertFalse(passed)
        self.assertEqual(res["status"], "ABSTAIN")
        self.assertEqual(res["reason"], "HIGH_EPISTEMIC_VACUITY")
        self.assertGreater(res["u"], 0.35)
        self.assertEqual(res["confidence"], 0.0)

    def test_abstention_on_high_conflict(self) -> None:
        """4b. Abstention behavior on conflicting inputs."""
        # Strong but opposing evidence: e_bull = 15.0, e_bear = 15.0, e_neutral = 0.0
        # S = 33, b_bull = 15/33 = 0.4545, b_bear = 0.4545, u = 3/33 = 0.0909 < 0.35
        # Conflict = 2 * 0.4545 * 0.4545 = 0.4132 > 0.40
        conflicting_evidence = {"evidence": [15.0, 15.0, 0.0]}
        passed, res = self.gate.audit_trade_signal(conflicting_evidence, threshold_u=0.35)

        self.assertFalse(passed)
        self.assertEqual(res["status"], "ABSTAIN")
        self.assertEqual(res["reason"], "HIGH_SIGNAL_CONFLICT")
        self.assertLess(res["u"], 0.35)
        self.assertGreater(res["conflict"], 0.40)
        self.assertEqual(res["confidence"], 0.0)

    def test_high_conviction_approval(self) -> None:
        """5. Approval behavior on high-conviction, low-conflict evidence."""
        # Strong bullish evidence: e_bull = 10.0, e_bear = 0.0, e_neutral = 0.0
        # S = 13, u = 3/13 = 0.2307 < 0.35, conflict = 0.0
        strong_evidence = {"evidence": [10.0, 0.0, 0.0]}
        passed, res = self.gate.audit_trade_signal(strong_evidence, threshold_u=0.35)

        self.assertTrue(passed)
        self.assertEqual(res["status"], "APPROVED")
        self.assertLess(res["u"], 0.35)
        self.assertAlmostEqual(res["conflict"], 0.0, places=6)
        self.assertAlmostEqual(res["confidence"], 1.0 - res["u"], places=6)
        self.assertGreater(res["confidence"], 0.65)

    def test_multi_factor_evidence_combination(self) -> None:
        """6. Multi-factor evidence combination from technical, microstructure, and sentiment."""
        tech = [3.0, 0.0, 0.0]
        micro = [4.0, 0.0, 0.0]
        sent = [3.0, 0.0, 0.0]

        fused = self.model.combine_factor_evidence(tech, micro, sent, weights=(1.0, 1.0, 1.0))
        # Total e = [10.0, 0.0, 0.0]
        self.assertAlmostEqual(fused.evidence[0], 10.0, places=9)
        self.assertAlmostEqual(fused.vacuity, 3.0 / 13.0, places=9)

    def test_audit_strategy_pnl_distribution_synthetic_valid(self) -> None:
        """7a. PnL distribution audit on statistically solid, non-overfitted returns."""
        np.random.seed(42)
        # 100 trades with positive mean and 60% win rate
        positive_trades = np.random.normal(loc=0.005, scale=0.015, size=100)
        report = self.gate.audit_strategy_pnl_distribution(positive_trades)

        self.assertEqual(report["status"], "APPROVED")
        self.assertTrue(report["passes_audit"])
        self.assertFalse(report["is_overfitted"])
        self.assertGreater(report["win_rate"], 0.50)
        self.assertLess(report["evidential_vacuity_u"], 0.10)
        self.assertGreater(report["sharpe_ratio"], 0.0)

    def test_audit_strategy_pnl_distribution_sparse_or_losing(self) -> None:
        """7b. PnL distribution audit flags sparse or losing strategies."""
        # 1. Very few trades (N=5) -> high vacuity u = 3 / 8 = 0.375 > 0.10
        sparse_returns = np.array([0.01, 0.02, -0.01, 0.015, 0.005])
        sparse_report = self.gate.audit_strategy_pnl_distribution(sparse_returns)
        self.assertTrue(sparse_report["is_overfitted"])
        self.assertFalse(sparse_report["passes_audit"])
        self.assertTrue(sparse_report["insufficient_sample"])

        # 2. Consistent losing trades
        losing_returns = np.array([-0.01] * 50)
        losing_report = self.gate.audit_strategy_pnl_distribution(losing_returns)
        self.assertTrue(losing_report["is_overfitted"])
        self.assertFalse(losing_report["passes_audit"])
        self.assertLess(losing_report["sharpe_ratio"], 0.0)

        # 3. Empty trades
        empty_report = self.gate.audit_strategy_pnl_distribution([])
        self.assertEqual(empty_report["status"], "REJECTED")
        self.assertTrue(empty_report["is_overfitted"])


if __name__ == "__main__":
    unittest.main()
