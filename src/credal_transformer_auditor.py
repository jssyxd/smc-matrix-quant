"""
Mathematical Evidential Deep-Dive Module: Credal Transformer & Subjective Logic.

Based on NeurIPS 2025 Credal Transformer (arXiv:2510.12137) and
Subjective Logic (Audun Jøsang, 2016).

This module quantifies epistemic uncertainty (vacuity) and pairwise conflict
across multi-factor evidence vectors (technical, micro-structure, sentiment/trend),
enforcing strict belief conservation laws and abstaining from high-uncertainty or
conflicting regimes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union
import numpy as np


@dataclass(frozen=True)
class CredalEvidenceState:
    """State of evidential evaluation under Subjective Logic.

    Invariants:
        S = sum(alpha_k) = sum(e_k) + K
        b_k = e_k / S
        u = K / S
        sum(b_k) + u == 1.0
    """
    evidence: np.ndarray
    alphas: np.ndarray
    beliefs: np.ndarray
    vacuity: float
    strength: float
    pairwise_conflict: float
    expected_probs: np.ndarray


class CredalEvidenceModel:
    """Multi-factor Evidential Deep Learning Model based on Subjective Logic & Credal Transformer.

    Takes multi-factor evidence vectors e = [e_1, e_2, ..., e_K] from technical,
    micro-structure, sentiment, or trend factors.

    Formulation:
        alpha_k = e_k + 1
        S = sum_{k=1}^K alpha_k = sum_{k=1}^K e_k + K
        b_k = e_k / S
        u = K / S
        p_k = alpha_k / S = b_k + u / K
        Conservation Law: sum_{k=1}^K b_k + u = 1.0

    Pairwise signal conflict mass (Dempster-Shafer / Subjective Logic fusion conflict):
        conflict = sum_{i != j} (b_i * b_j) / (1 - sum_i b_i^2) or normalized cross-belief product.
        Specifically, for singleton orthogonal hypotheses:
        C = sum_{i < j} 2 * b_i * b_j = (sum b_i)^2 - sum b_i^2 = (1 - u)^2 - sum b_i^2.
    """

    def __init__(self, K: int = 3, eps: float = 1e-9) -> None:
        """Initialize CredalEvidenceModel.

        Parameters
        ----------
        K : int, default=3
            Number of classes/hypotheses (e.g. [BULLISH, BEARISH, NEUTRAL] or K factors).
        eps : float, default=1e-9
            Numerical stability constant to avoid zero-division.
        """
        if K < 2:
            raise ValueError(f"K must be at least 2, got {K}")
        self.K = int(K)
        self.eps = float(eps)

    def compute_conflict(self, beliefs: np.ndarray) -> float:
        """Compute pairwise signal conflict across classes.

        For orthogonal belief assignments in Subjective Logic:
            Conflict C = sum_{i != j} b_i * b_j = 2 * sum_{i < j} b_i * b_j
                       = (sum b_i)^2 - sum(b_i^2)
        Normalized relative to maximum possible conflict between opposing directional beliefs:
            If two opposing beliefs b_1 = 0.5, b_2 = 0.5 (with u = 0), C = 2 * 0.5 * 0.5 = 0.5.
            We report pairwise conflict mass C in [0, 1].
        """
        b = np.asarray(beliefs, dtype=np.float64)
        sum_b = float(np.sum(b))
        sum_sq = float(np.sum(b ** 2))
        conflict = max(0.0, float(sum_b ** 2 - sum_sq))
        return min(1.0, conflict)

    def evaluate_evidence(self, evidence: Sequence[float] | np.ndarray) -> CredalEvidenceState:
        """Evaluate evidence vector and compute Dirichlet parameters, beliefs, vacuity, and conflict.

        Parameters
        ----------
        evidence : Sequence[float] or np.ndarray
            Non-negative evidence vector e of length K.

        Returns
        -------
        CredalEvidenceState
            Container with alphas, beliefs, vacuity u, strength S, and conflict.
        """
        e = np.asarray(evidence, dtype=np.float64)
        if e.ndim != 1 or len(e) != self.K:
            raise ValueError(f"Evidence must be 1D array of length K={self.K}, got shape {e.shape}")

        # Evidence must be non-negative
        e = np.maximum(0.0, e)

        # Dirichlet parameters alpha_k = e_k + 1
        alphas = e + 1.0

        # Dirichlet strength S = sum(alpha_k)
        S = float(np.sum(alphas))
        if S < self.eps:
            S = float(self.K)

        # Beliefs b_k = e_k / S
        beliefs = e / S

        # Vacuity (Epistemic Uncertainty) u = K / S
        vacuity = float(self.K / S)

        # Expected Dirichlet probability p_k = alpha_k / S = b_k + u / K
        expected_probs = alphas / S

        # Pairwise signal conflict
        conflict = self.compute_conflict(beliefs)

        return CredalEvidenceState(
            evidence=e,
            alphas=alphas,
            beliefs=beliefs,
            vacuity=vacuity,
            strength=S,
            pairwise_conflict=conflict,
            expected_probs=expected_probs,
        )

    def combine_factor_evidence(
        self,
        technical_evidence: Sequence[float] | np.ndarray,
        microstructure_evidence: Sequence[float] | np.ndarray,
        sentiment_evidence: Sequence[float] | np.ndarray,
        weights: Optional[Tuple[float, float, float]] = None,
    ) -> CredalEvidenceState:
        """Combine multi-factor evidence vectors from technical, micro-structure, and sentiment.

        Parameters
        ----------
        technical_evidence : array-like of shape (K,)
        microstructure_evidence : array-like of shape (K,)
        sentiment_evidence : array-like of shape (K,)
        weights : Optional[Tuple[float, float, float]]
            Weights for each source. Defaults to equal weighting (1.0, 1.0, 1.0).

        Returns
        -------
        CredalEvidenceState
            Fused evidential state.
        """
        w = weights if weights is not None else (1.0, 1.0, 1.0)
        e_tech = np.maximum(0.0, np.asarray(technical_evidence, dtype=np.float64))
        e_micro = np.maximum(0.0, np.asarray(microstructure_evidence, dtype=np.float64))
        e_sent = np.maximum(0.0, np.asarray(sentiment_evidence, dtype=np.float64))

        fused_e = w[0] * e_tech + w[1] * e_micro + w[2] * e_sent
        return self.evaluate_evidence(fused_e)


class CredalAuditGate:
    """Auditing gate for trade signals and empirical PnL distributions.

    Adheres strictly to the contract:
    - `audit_trade_signal(evidence_dict: dict, threshold_u: float = 0.35) -> Tuple[bool, dict]`:
      If vacuity u > threshold_u or conflict > 0.40:
          output (False, {"status": "ABSTAIN", "reason": "HIGH_EPISTEMIC_VACUITY" or "HIGH_SIGNAL_CONFLICT", "u": u, ...})
      Else:
          output (True, {"status": "APPROVED", "u": u, "confidence": 1.0 - u, ...})
    - `audit_strategy_pnl_distribution(trade_returns: np.ndarray) -> dict`:
      Evaluates empirical distribution vs vacuous prior to detect overfitting/data snooping.
    """

    def __init__(self, K: int = 3, threshold_conflict: float = 0.40, eps: float = 1e-9) -> None:
        """Initialize CredalAuditGate.

        Parameters
        ----------
        K : int, default=3
            Number of hypotheses classes (typically 3: Bullish, Bearish, Neutral).
        threshold_conflict : float, default=0.40
            Pairwise conflict threshold above which trade is abstained.
        eps : float, default=1e-9
            Numerical stability floor.
        """
        self.K = K
        self.threshold_conflict = threshold_conflict
        self.eps = eps
        self.evidence_model = CredalEvidenceModel(K=K, eps=eps)

    def parse_evidence_dict(self, evidence_dict: Mapping[str, Any]) -> np.ndarray:
        """Extract evidence vector from various dictionary structures.

        Accepts:
        - {"evidence": [e1, e2, e3]} or {"evidence_vector": [...]}
        - {"e_bull": float, "e_bear": float, "e_neutral": float}
        - {"bullish": float, "bearish": float, "neutral": float}
        - Multi-factor breakdown: {"technical": [...], "microstructure": [...], "sentiment": [...]}
        - Factor signals: list of positive indicator weights.
        """
        if "evidence" in evidence_dict:
            return np.asarray(evidence_dict["evidence"], dtype=np.float64)
        if "evidence_vector" in evidence_dict:
            return np.asarray(evidence_dict["evidence_vector"], dtype=np.float64)

        if "e_bull" in evidence_dict or "e_bear" in evidence_dict:
            e_bull = float(evidence_dict.get("e_bull", 0.0))
            e_bear = float(evidence_dict.get("e_bear", 0.0))
            e_neutral = float(evidence_dict.get("e_neutral", 0.0))
            return np.array([e_bull, e_bear, e_neutral], dtype=np.float64)

        if "bullish" in evidence_dict or "bearish" in evidence_dict:
            e_bull = float(evidence_dict.get("bullish", 0.0))
            e_bear = float(evidence_dict.get("bearish", 0.0))
            e_neutral = float(evidence_dict.get("neutral", 0.0))
            return np.array([e_bull, e_bear, e_neutral], dtype=np.float64)

        # Multi-factor composition if provided
        if any(k in evidence_dict for k in ("technical", "microstructure", "sentiment")):
            tech = np.asarray(evidence_dict.get("technical", np.zeros(self.K)), dtype=np.float64)
            micro = np.asarray(evidence_dict.get("microstructure", np.zeros(self.K)), dtype=np.float64)
            sent = np.asarray(evidence_dict.get("sentiment", np.zeros(self.K)), dtype=np.float64)
            return tech + micro + sent

        # If indicators mapping is provided
        e_bull = 0.0
        e_bear = 0.0
        for k, v in evidence_dict.items():
            val = float(v) if isinstance(v, (int, float, np.number, bool)) else 0.0
            kl = k.lower()
            if "bull" in kl or "up" in kl or "long" in kl:
                e_bull += val
            elif "bear" in kl or "down" in kl or "short" in kl:
                e_bear += val

        return np.array([e_bull, e_bear, 0.0], dtype=np.float64)

    def audit_trade_signal(
        self,
        evidence_dict: Mapping[str, Any],
        threshold_u: float = 0.35,
    ) -> Tuple[bool, Dict[str, Any]]:
        """Audit trade signal using evidential vacuity and pairwise signal conflict.

        Parameters
        ----------
        evidence_dict : dict
            Multi-factor evidence input.
        threshold_u : float, default=0.35
            Maximum permitted epistemic vacuity.

        Returns
        -------
        Tuple[bool, dict]
            (passed, audit_metadata)
            If vacuity u > threshold_u or conflict > 0.40:
                (False, {"status": "ABSTAIN", "reason": ..., "u": u, ...})
            Else:
                (True, {"status": "APPROVED", "u": u, "confidence": 1.0 - u, ...})
        """
        e_vec = self.parse_evidence_dict(evidence_dict)
        state = self.evidence_model.evaluate_evidence(e_vec)

        u = state.vacuity
        conflict = state.pairwise_conflict

        # Check conditions
        high_vacuity = u > threshold_u
        high_conflict = conflict > self.threshold_conflict

        if high_vacuity and high_conflict:
            reason = "HIGH_EPISTEMIC_VACUITY_AND_CONFLICT"
            return (
                False,
                {
                    "status": "ABSTAIN",
                    "reason": reason,
                    "u": float(u),
                    "conflict": float(conflict),
                    "beliefs": state.beliefs.tolist(),
                    "alphas": state.alphas.tolist(),
                    "confidence": 0.0,
                },
            )
        elif high_vacuity:
            reason = "HIGH_EPISTEMIC_VACUITY"
            return (
                False,
                {
                    "status": "ABSTAIN",
                    "reason": reason,
                    "u": float(u),
                    "conflict": float(conflict),
                    "beliefs": state.beliefs.tolist(),
                    "alphas": state.alphas.tolist(),
                    "confidence": 0.0,
                },
            )
        elif high_conflict:
            reason = "HIGH_SIGNAL_CONFLICT"
            return (
                False,
                {
                    "status": "ABSTAIN",
                    "reason": reason,
                    "u": float(u),
                    "conflict": float(conflict),
                    "beliefs": state.beliefs.tolist(),
                    "alphas": state.alphas.tolist(),
                    "confidence": 0.0,
                },
            )
        else:
            confidence = float(max(0.0, 1.0 - u))
            return (
                True,
                {
                    "status": "APPROVED",
                    "u": float(u),
                    "conflict": float(conflict),
                    "confidence": confidence,
                    "beliefs": state.beliefs.tolist(),
                    "alphas": state.alphas.tolist(),
                    "expected_probs": state.expected_probs.tolist(),
                },
            )

    def audit_strategy_pnl_distribution(
        self,
        trade_returns: Sequence[float] | np.ndarray,
        null_sharpe: float = 0.0,
        significance_level: float = 0.05,
    ) -> Dict[str, Any]:
        """Audit empirical PnL distribution against a vacuous / uninformative prior.

        Detects overfitting, data-snooping, and lack of genuine statistical edge
        by evaluating:
        1. Sample size sufficiency and evidentiary strength.
        2. Win/loss evidence mapping to Dirichlet posterior:
           - positive return count -> e_win
           - negative return count -> e_loss
           - zero return count -> e_neutral
        3. Vacuity of empirical performance: u_pnl = K / (N + K)
        4. Evidential p-value / posterior probability that true win rate > 50%.
        5. Moments (mean, standard deviation, Sharpe ratio, skewness, kurtosis).

        Parameters
        ----------
        trade_returns : Sequence[float] or np.ndarray
            Array of per-trade returns (percentage or decimal).
        null_sharpe : float, default=0.0
            Sharpe ratio under the null hypothesis of no alpha.
        significance_level : float, default=0.05
            Significance threshold.

        Returns
        -------
        dict
            Audit report with overfitting flags, evidential vacuity, win-rate beliefs,
            and pass/fail verdict.
        """
        arr = np.asarray(trade_returns, dtype=np.float64)
        n_trades = len(arr)

        if n_trades == 0:
            return {
                "status": "REJECTED",
                "reason": "NO_TRADE_DATA",
                "n_trades": 0,
                "u_pnl": 1.0,
                "is_overfitted": True,
                "passes_audit": False,
            }

        # Count win, loss, neutral trades
        wins = int(np.sum(arr > self.eps))
        losses = int(np.sum(arr < -self.eps))
        neutral = int(n_trades - wins - losses)

        # Subjective Logic evidence representation of trade outcomes
        # K = 3 (Win, Loss, Neutral)
        pnl_evidence = np.array([float(wins), float(losses), float(neutral)], dtype=np.float64)
        pnl_state = self.evidence_model.evaluate_evidence(pnl_evidence)

        # Distributional moments
        mean_ret = float(np.mean(arr))
        std_ret = float(np.std(arr, ddof=1)) if n_trades > 1 else 0.0
        # Handle standard deviation zero or constant returns
        if std_ret > self.eps:
            sharpe = float(mean_ret / std_ret * np.sqrt(252))
        elif mean_ret < 0:
            sharpe = -float("inf")
        elif mean_ret > 0:
            sharpe = float("inf")
        else:
            sharpe = 0.0

        # Skewness and Kurtosis
        if n_trades >= 3 and std_ret > 0:
            skew = float(np.mean(((arr - mean_ret) / std_ret) ** 3))
        else:
            skew = 0.0

        if n_trades >= 4 and std_ret > 0:
            kurt = float(np.mean(((arr - mean_ret) / std_ret) ** 4) - 3.0)
        else:
            kurt = 0.0

        # Epistemic vacuity of PnL: u = 3 / (N + 3)
        u_pnl = pnl_state.vacuity

        # Posterior win belief and probability
        b_win = float(pnl_state.beliefs[0])
        b_loss = float(pnl_state.beliefs[1])
        p_win = float(pnl_state.expected_probs[0])

        # Overfitting / snooping checks:
        # 1. High vacuity in PnL (insufficient trade count to reject prior ignorance, e.g. N < 30)
        insufficient_sample = bool(u_pnl > 0.10 or n_trades < 30)

        # 2. Asymmetric loss tail / negative skewness hiding catastrophic tail risk
        tail_risk_anomaly = bool(skew < -1.5 and kurt > 3.0)

        # 3. Win rate indistinguishable from random flip under evidential vacuity
        edge_uncertain = bool(b_win <= b_loss or p_win < 0.50)

        # 4. Statistical significance of positive return (t-test)
        if n_trades > 1 and std_ret > 0:
            se = std_ret / np.sqrt(n_trades)
            t_stat = mean_ret / (se + self.eps)
        else:
            t_stat = 0.0

        # Overfitted verdict
        is_overfitted = bool(insufficient_sample or edge_uncertain or (sharpe < 0.0))
        passes_audit = bool(not is_overfitted and not tail_risk_anomaly)

        verdict_status = "APPROVED" if passes_audit else "FLAGGED_FOR_OVERFITTING"

        return {
            "status": verdict_status,
            "passes_audit": passes_audit,
            "is_overfitted": is_overfitted,
            "n_trades": n_trades,
            "win_rate": float(wins / n_trades),
            "loss_rate": float(losses / n_trades),
            "evidential_vacuity_u": float(u_pnl),
            "dirichlet_strength": float(pnl_state.strength),
            "belief_win": b_win,
            "belief_loss": b_loss,
            "posterior_win_prob": p_win,
            "mean_return": mean_ret,
            "std_return": std_ret,
            "sharpe_ratio": sharpe,
            "skewness": skew,
            "excess_kurtosis": kurt,
            "t_statistic": float(t_stat),
            "tail_risk_anomaly": tail_risk_anomaly,
            "insufficient_sample": insufficient_sample,
        }
