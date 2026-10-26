"""
Microsoft RD-Agent Quant Autonomous Evolutionary Research Loop Module.

Based on:
- Microsoft RD-Agent (RD-Agent Quant, arXiv:2505.15155):
  * HypothesisGenerator: Formulates structured hypotheses about market micro-structure.
  * FactorEvolver: Generates symbolic mathematical factor variants via genetic crossover
    and prompt/heuristic mutation on Qlib base factors.
  * BacktestEvaluator: Evaluates mutated factors on in-sample (IS) and out-of-sample (OOS) data
    with transaction costs (Maker 2 bps, Taker 5 bps, Slippage 5 bps).
  * FeedbackPruner: Computes Information Coefficient (IC), Information Ratio (IR), and
    Credal Epistemic Vacuity u (Subjective Logic Dirichlet model).
    Prunes/discards factors with IC < 0.02 or u > 0.35.
- Implements:
  `run_rd_agent_iteration(df: pd.DataFrame, num_generations: int = 3) -> dict`
  returning the best evolved factor combination, hypothesis log, and convergence report.
"""

from __future__ import annotations

import copy
import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

import numpy as np
import pandas as pd

from src.alphagpt_factor_miner import (
    FactorScore,
    FactorStackVM,
    compute_alphagpt_factors,
    compute_wilder_atr,
)
from src.credal_transformer_auditor import CredalEvidenceModel, CredalEvidenceState


# ---------------------------------------------------------------------------
# Data Models & Structures
# ---------------------------------------------------------------------------

@dataclass
class Hypothesis:
    """Structured research hypothesis about market micro-structure."""
    id: str
    statement: str
    rationale: str
    target_microstructure: str  # e.g., "OFI_FVG_ABSORPTION", "SWEEP_MOMENTUM", etc.
    regime_condition: str      # e.g., "high_volatility", "mean_reverting", "trending"
    expected_alpha_mechanism: str
    generation: int = 0
    status: str = "active"     # "active", "validated", "pruned"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "rationale": self.rationale,
            "target_microstructure": self.target_microstructure,
            "regime_condition": self.regime_condition,
            "expected_alpha_mechanism": self.expected_alpha_mechanism,
            "generation": self.generation,
            "status": self.status,
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass
class EvolvedFactor:
    """Symbolic mathematical factor entity within genetic evolutionary loop."""
    id: str
    name: str
    expression: str  # Symbolic expression in FactorStackVM RPN tokens
    hypothesis_id: str
    generation: int
    parent_ids: List[str] = field(default_factory=list)
    mutation_type: str = "init"  # "init", "crossover", "mutation", "prompt_mutation"
    score: Optional[FactorScore] = None
    backtest_metrics: Dict[str, float] = field(default_factory=dict)
    credal_state: Optional[CredalEvidenceState] = None
    vacuity_u: float = 1.0
    pruned: bool = False
    prune_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "expression": self.expression,
            "hypothesis_id": self.hypothesis_id,
            "generation": self.generation,
            "parent_ids": list(self.parent_ids),
            "mutation_type": self.mutation_type,
            "ic": self.score.ic_mean if self.score else 0.0,
            "rank_ic": self.score.rank_ic_mean if self.score else 0.0,
            "ic_ir": self.score.ic_ir if self.score else 0.0,
            "vacuity_u": self.vacuity_u,
            "pruned": self.pruned,
            "prune_reason": self.prune_reason,
            "backtest_metrics": copy.deepcopy(self.backtest_metrics),
        }


# ---------------------------------------------------------------------------
# Component 1: HypothesisGenerator
# ---------------------------------------------------------------------------

class HypothesisGenerator:
    """Formulates hypotheses about market micro-structure.

    Example hypothesis:
    'Combining OFI with FVG absorption reduces false breakout losses in high-volatility regimes'
    """

    CORE_TEMPLATES = [
        {
            "template": "Combining OFI with FVG absorption reduces false breakout losses in {regime} regimes.",
            "target": "OFI_FVG_ABSORPTION",
            "mechanism": "OFI order flow pressure confirms FVG retest before liquidity exhaustion.",
            "preferred_regime": "high_volatility",
            "base_factors": ["OFI_Impulse", "FVG_Absorption_Rate", "Vol_Displacement_Ratio"],
        },
        {
            "template": "Penetration depth of liquidity sweeps against ATR predicts directional mean-reversion in {regime} regimes.",
            "target": "SWEEP_REVERSION",
            "mechanism": "Exhausted stop-runs beyond swing levels lead to sharp order-book snapbacks.",
            "preferred_regime": "mean_reverting",
            "base_factors": ["Liquidity_Sweep_Intensity", "OFI_Impulse"],
        },
        {
            "template": "Volatility displacement ratio scaling trend momentum filters noise during {regime} regimes.",
            "target": "VOLATILITY_SCALED_MOMENTUM",
            "mechanism": "Garman-Klass volatility normalization prevents over-trading during chop while riding expansions.",
            "preferred_regime": "trending",
            "base_factors": ["Vol_Displacement_Ratio", "ret_1", "ret_5"],
        },
        {
            "template": "Asymmetric order book imbalance coupled with volume surges accelerates breakout velocity in {regime} regimes.",
            "target": "IMBALANCE_ACCELERATION",
            "mechanism": "Bid/Ask volume divergence triggers cascading stop orders in low-resistance zones.",
            "preferred_regime": "high_volatility",
            "base_factors": ["OFI_Impulse", "volume_surge"],
        },
        {
            "template": "Counter-trend FVG absorption divergence signals regime transition in {regime} regimes.",
            "target": "FVG_REGIME_TRANSITION",
            "mechanism": "Persistent non-fill of large FVGs reveals latent institutional inventory absorption.",
            "preferred_regime": "mean_reverting",
            "base_factors": ["FVG_Absorption_Rate", "Vol_Displacement_Ratio"],
        },
    ]

    def __init__(self, seed: Optional[int] = 42) -> None:
        self.rng = random.Random(seed)
        self.hypothesis_counter = 0

    def generate(
        self,
        num_hypotheses: int = 3,
        generation: int = 0,
        feedback: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Hypothesis]:
        """Generate hypotheses for the current evolutionary cycle."""
        hypotheses: List[Hypothesis] = []
        regimes = ["high_volatility", "mean_reverting", "trending", "low_volatility"]

        # Adapt based on feedback if provided
        favored_targets: Set[str] = set()
        if feedback:
            for fb in feedback:
                if fb.get("status") == "validated":
                    favored_targets.add(fb.get("target_microstructure", ""))

        for i in range(num_hypotheses):
            self.hypothesis_counter += 1
            h_id = f"HYP_G{generation}_{self.hypothesis_counter:03d}"

            # Select template
            tmpl_idx = (self.hypothesis_counter - 1) % len(self.CORE_TEMPLATES)
            tmpl_info = self.CORE_TEMPLATES[tmpl_idx]

            # Regime selection
            regime = tmpl_info["preferred_regime"]
            if feedback and self.rng.random() > 0.7:
                regime = self.rng.choice(regimes)

            statement = tmpl_info["template"].format(regime=regime)
            rationale = (
                f"Micro-structural causal hypothesis for {tmpl_info['target']} under {regime}: "
                f"{tmpl_info['mechanism']}"
            )

            hypo = Hypothesis(
                id=h_id,
                statement=statement,
                rationale=rationale,
                target_microstructure=tmpl_info["target"],
                regime_condition=regime,
                expected_alpha_mechanism=tmpl_info["mechanism"],
                generation=generation,
                metadata={"base_factors": list(tmpl_info["base_factors"])},
            )
            hypotheses.append(hypo)

        return hypotheses


# ---------------------------------------------------------------------------
# Component 2: FactorEvolver
# ---------------------------------------------------------------------------

class FactorEvolver:
    """Generates symbolic mathematical factor variants via genetic crossover
    and prompt mutation on Qlib base factors.
    """

    UNARY_OPS = ["abs", "neg", "sign", "log", "inv", "sqrt"]
    BINARY_OPS = ["add", "sub", "mul", "div", "max", "min"]
    TS_OPS = ["ts_mean", "ts_std", "ts_rank", "ts_delta", "ts_delay", "ts_max", "ts_min", "ts_zscore"]
    TIME_WINDOWS = [3, 5, 10, 20]

    def __init__(self, seed: Optional[int] = 42) -> None:
        self.rng = random.Random(seed)
        self.factor_counter = 0

    def generate_seed_factors(
        self,
        hypotheses: Sequence[Hypothesis],
        available_features: Sequence[str],
        factors_per_hypothesis: int = 2,
    ) -> List[EvolvedFactor]:
        """Generate initial seed factors directly tied to hypotheses."""
        factors: List[EvolvedFactor] = []
        features = list(available_features)

        for hypo in hypotheses:
            base_targets = hypo.metadata.get("base_factors", [])
            valid_bases = [b for b in base_targets if b in features]
            if not valid_bases:
                valid_bases = features[:2]

            for k in range(factors_per_hypothesis):
                self.factor_counter += 1
                fid = f"FACT_G{hypo.generation}_{self.factor_counter:03d}"

                if len(valid_bases) >= 2 and k == 0:
                    f1 = valid_bases[0]
                    f2 = valid_bases[1]
                    # Stack VM RPN: f1 f2 mul or f1 f2 sub
                    op = "mul" if "absorption" in hypo.statement.lower() or "scale" in hypo.statement.lower() else "sub"
                    expr = f"{f1} {f2} {op}"
                elif len(valid_bases) >= 1:
                    f1 = valid_bases[0]
                    expr = f"{f1} 5 ts_rank"
                else:
                    f1 = features[0]
                    expr = f"{f1} 10 ts_zscore"

                factor = EvolvedFactor(
                    id=fid,
                    name=f"Alpha_{hypo.target_microstructure}_{self.factor_counter}",
                    expression=expr,
                    hypothesis_id=hypo.id,
                    generation=hypo.generation,
                    mutation_type="init",
                )
                factors.append(factor)

        return factors

    def crossover(self, parent1: EvolvedFactor, parent2: EvolvedFactor, generation: int) -> EvolvedFactor:
        """Genetic crossover combining symbolic AST/RPN sub-expressions from two parent factors."""
        self.factor_counter += 1
        fid = f"FACT_G{generation}_{self.factor_counter:03d}"

        # Combine via binary operator in valid RPN
        op = self.rng.choice(["add", "sub", "mul"])
        combined = f"{parent1.expression} {parent2.expression} {op}"

        return EvolvedFactor(
            id=fid,
            name=f"Crossover_{parent1.name[:10]}_{parent2.name[:10]}",
            expression=combined,
            hypothesis_id=parent1.hypothesis_id,
            generation=generation,
            parent_ids=[parent1.id, parent2.id],
            mutation_type="crossover",
        )

    def mutate(
        self,
        factor: EvolvedFactor,
        available_features: Sequence[str],
        generation: int,
    ) -> EvolvedFactor:
        """Symbolic genetic mutation (point mutation, operator mutation, or terminal insertion)."""
        self.factor_counter += 1
        fid = f"FACT_G{generation}_{self.factor_counter:03d}"

        mutation_types = ["wrap_unary", "append_feature", "time_window_shift", "prompt_guided"]
        chosen_mut = self.rng.choice(mutation_types)

        new_expr = factor.expression
        if chosen_mut == "wrap_unary":
            unary = self.rng.choice(self.UNARY_OPS)
            new_expr = f"{factor.expression} {unary}"
        elif chosen_mut == "append_feature":
            feat = self.rng.choice(list(available_features))
            op = self.rng.choice(self.BINARY_OPS)
            new_expr = f"{factor.expression} {feat} {op}"
        elif chosen_mut == "time_window_shift":
            window = self.rng.choice(self.TIME_WINDOWS)
            op = self.rng.choice(self.TS_OPS)
            new_expr = f"{factor.expression} {window} {op}"
        else:
            # Prompt-guided mutation mimicking LLM prompt mutation
            new_expr = f"{factor.expression} OFI_Impulse mul"

        return EvolvedFactor(
            id=fid,
            name=f"Mutant_{factor.name[:12]}",
            expression=new_expr,
            hypothesis_id=factor.hypothesis_id,
            generation=generation,
            parent_ids=[factor.id],
            mutation_type=f"mutation_{chosen_mut}",
        )

    def evolve_population(
        self,
        survivors: Sequence[EvolvedFactor],
        hypotheses: Sequence[Hypothesis],
        available_features: Sequence[str],
        target_population_size: int,
        generation: int,
    ) -> List[EvolvedFactor]:
        """Evolve the survivor population to create the next generation."""
        new_pop: List[EvolvedFactor] = list(survivors)
        if not survivors:
            return self.generate_seed_factors(hypotheses, available_features, factors_per_hypothesis=2)

        while len(new_pop) < target_population_size:
            roll = self.rng.random()
            if roll < 0.4 and len(survivors) >= 2:
                # Crossover
                p1, p2 = self.rng.sample(list(survivors), 2)
                child = self.crossover(p1, p2, generation)
                new_pop.append(child)
            elif roll < 0.8:
                # Mutation
                p = self.rng.choice(list(survivors))
                child = self.mutate(p, available_features, generation)
                new_pop.append(child)
            else:
                # Fresh seed from hypothesis
                h = self.rng.choice(list(hypotheses))
                seeds = self.generate_seed_factors([h], available_features, factors_per_hypothesis=1)
                new_pop.extend(seeds)

        return new_pop[:target_population_size]


# ---------------------------------------------------------------------------
# Component 3: BacktestEvaluator
# ---------------------------------------------------------------------------

class BacktestEvaluator:
    """Evaluates mutated factors on in-sample and out-of-sample data with transaction costs.

    Transaction costs adherence:
    - Maker: 0.0002 (2 bps)
    - Taker: 0.0005 (5 bps)
    - Slippage: 0.0005 (5 bps)
    """

    def __init__(
        self,
        maker_fee: float = 0.0002,
        taker_fee: float = 0.0005,
        slippage: float = 0.0005,
        split_ratio: float = 0.8,
        warmup_bars: int = 50,
    ) -> None:
        self.maker_fee = float(maker_fee)
        self.taker_fee = float(taker_fee)
        self.slippage = float(slippage)
        self.split_ratio = float(split_ratio)
        self.warmup_bars = int(warmup_bars)

    def split_data(
        self,
        features_df: pd.DataFrame,
        returns: pd.Series,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """Split into in-sample (IS) and out-of-sample (OOS) data."""
        n = len(features_df)
        split_idx = int(n * self.split_ratio)
        split_idx = max(self.warmup_bars + 10, min(split_idx, n - 10))

        is_feat = features_df.iloc[:split_idx]
        is_ret = returns.iloc[:split_idx]
        oos_feat = features_df.iloc[split_idx:]
        oos_ret = returns.iloc[split_idx:]
        return is_feat, is_ret, oos_feat, oos_ret

    def evaluate_factor_series(
        self,
        expression: str,
        features_df: pd.DataFrame,
    ) -> Optional[pd.Series]:
        """Evaluate symbolic factor expression via FactorStackVM."""
        try:
            tokens = expression.split()
            data_table = {col: features_df[col] for col in features_df.columns}
            return FactorStackVM.execute_rpn(tokens, data_table)
        except Exception:
            return None

    def backtest_single_factor(
        self,
        factor_values: pd.Series,
        forward_returns: pd.Series,
        is_maker: bool = True,
    ) -> Dict[str, float]:
        """Run realistic friction-aware vectorized backtest on a single factor signal.

        Signal logic:
        - Long when standardized factor > 0.5
        - Short when standardized factor < -0.5
        - Friction deducted on every position switch.
        """
        valid_idx = factor_values.dropna().index.intersection(forward_returns.dropna().index)
        if len(valid_idx) < 10:
            return {
                "sharpe": 0.0,
                "total_return": 0.0,
                "max_drawdown": 0.0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "trade_count": 0,
            }

        s_vals = factor_values.loc[valid_idx]
        ret = forward_returns.loc[valid_idx]

        # Standardize factor to avoid extreme scaling
        std = s_vals.std()
        if std == 0 or np.isnan(std):
            norm_s = s_vals - s_vals.mean()
        else:
            norm_s = (s_vals - s_vals.mean()) / std

        # Generate target positions: +1, 0, -1
        pos = pd.Series(0.0, index=valid_idx)
        pos[norm_s > 0.5] = 1.0
        pos[norm_s < -0.5] = -1.0

        # Position changes incur trading friction
        pos_change = pos.diff().abs().fillna(0.0)
        fee_rate = (self.maker_fee if is_maker else self.taker_fee) + self.slippage
        friction = pos_change * fee_rate

        # Strategy returns: position * next_bar_return - friction
        strat_ret = pos * ret - friction

        # Metrics calculation
        total_pnl = float(strat_ret.sum())
        mean_r = strat_ret.mean()
        std_r = strat_ret.std()
        sharpe = float((mean_r / (std_r + 1e-8)) * math.sqrt(252 * 96)) if std_r > 0 else 0.0

        # Drawdown
        cum_ret = strat_ret.cumsum()
        running_max = np.maximum.accumulate(cum_ret)
        dd = cum_ret - running_max
        max_dd = float(dd.min()) if len(dd) > 0 else 0.0

        # Trade stats
        win_rate = float((strat_ret > 0).mean()) if len(strat_ret) > 0 else 0.0
        pos_wins = strat_ret[strat_ret > 0].sum()
        neg_losses = abs(strat_ret[strat_ret < 0].sum())
        profit_factor = float(pos_wins / (neg_losses + 1e-8))

        return {
            "sharpe": sharpe,
            "total_return": total_pnl,
            "max_drawdown": max_dd,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "trade_count": int(pos_change.sum()),
        }

    def evaluate(
        self,
        factor: EvolvedFactor,
        features_df: pd.DataFrame,
        forward_returns: pd.Series,
    ) -> Tuple[Optional[pd.Series], Dict[str, float]]:
        """Evaluate factor expression, backtest IS and OOS, and compute metrics."""
        f_series = self.evaluate_factor_series(factor.expression, features_df)
        if f_series is None or f_series.isna().all() or f_series.std() == 0:
            return None, {"is_sharpe": 0.0, "oos_sharpe": 0.0, "oos_return": 0.0}

        is_feat, is_ret, oos_feat, oos_ret = self.split_data(features_df, forward_returns)

        is_s = f_series.reindex(is_feat.index)
        oos_s = f_series.reindex(oos_feat.index)

        is_metrics = self.backtest_single_factor(is_s, is_ret, is_maker=True)
        oos_metrics = self.backtest_single_factor(oos_s, oos_ret, is_maker=True)

        combined_metrics = {
            "is_sharpe": is_metrics["sharpe"],
            "is_return": is_metrics["total_return"],
            "is_win_rate": is_metrics["win_rate"],
            "oos_sharpe": oos_metrics["sharpe"],
            "oos_return": oos_metrics["total_return"],
            "oos_win_rate": oos_metrics["win_rate"],
            "oos_max_dd": oos_metrics["max_drawdown"],
            "oos_profit_factor": oos_metrics["profit_factor"],
            "trade_count": oos_metrics["trade_count"],
        }
        return f_series, combined_metrics


# ---------------------------------------------------------------------------
# Component 4: FeedbackPruner
# ---------------------------------------------------------------------------

class FeedbackPruner:
    """Computes Information Coefficient (IC), Information Ratio (IR),
    and Credal Epistemic Vacuity u (Subjective Logic Dirichlet model).

    Discards factors with:
    - Pearson IC < ic_threshold (default 0.02)
    - Credal epistemic vacuity u > vacuity_threshold (default 0.35)
    """

    def __init__(
        self,
        ic_threshold: float = 0.02,
        vacuity_threshold: float = 0.35,
        min_trade_count: int = 5,
    ) -> None:
        self.ic_threshold = float(ic_threshold)
        self.vacuity_threshold = float(vacuity_threshold)
        self.min_trade_count = int(min_trade_count)
        self.credal_model = CredalEvidenceModel(K=3)

    def compute_ic_ir(
        self,
        factor_values: pd.Series,
        forward_returns: pd.Series,
    ) -> Tuple[float, float, float, float]:
        """Compute Pearson IC, Spearman Rank IC, IC std, and IC_IR."""
        valid_idx = factor_values.dropna().index.intersection(forward_returns.dropna().index)
        if len(valid_idx) < 10:
            return 0.0, 0.0, 0.0, 0.0

        f = factor_values.loc[valid_idx].astype(float)
        r = forward_returns.loc[valid_idx].astype(float)

        if f.std() == 0 or r.std() == 0 or f.isna().all() or r.isna().all():
            return 0.0, 0.0, 0.0, 0.0

        # Pearson correlation
        pearson_ic = float(f.corr(r, method="pearson"))
        if np.isnan(pearson_ic):
            pearson_ic = 0.0

        # Spearman rank correlation
        spearman_ic = float(f.corr(r, method="spearman"))
        if np.isnan(spearman_ic):
            spearman_ic = 0.0

        # Rolling window IC for IC_IR
        roll_window = min(30, max(5, len(valid_idx) // 5))
        roll_ic = f.rolling(roll_window).corr(r).dropna()
        ic_std = float(roll_ic.std()) if len(roll_ic) > 1 else 0.0
        if np.isnan(ic_std) or ic_std == 0:
            ic_std = 0.05
        ic_ir = float(pearson_ic / ic_std) if ic_std > 0 else 0.0

        return pearson_ic, spearman_ic, ic_std, ic_ir

    def compute_credal_vacuity(
        self,
        factor_score: FactorScore,
        backtest_metrics: Dict[str, float],
    ) -> Tuple[float, CredalEvidenceState]:
        """Map empirical factor metrics into Subjective Logic Dirichlet evidence vector e.

        Evidence formulation:
        - Class 0 (Alpha predictive signal strength): derived from abs(IC) / 0.02 and IC_IR
        - Class 1 (Out-of-sample stability): derived from max(0, OOS Sharpe) and win_rate
        - Class 2 (Market resistance / friction resilience): derived from profit_factor > 1.0
        Total evidence S = sum(e_k) + K
        Vacuity u = K / S.
        """
        # Evidence k=0: IC evidence
        ic_mag = abs(factor_score.ic_mean)
        e0 = max(0.0, (ic_mag / max(1e-4, self.ic_threshold)) - 0.5) * 2.0

        # Evidence k=1: OOS Sharpe / stability
        oos_sharpe = backtest_metrics.get("oos_sharpe", 0.0)
        e1 = max(0.0, oos_sharpe * 1.5)

        # Evidence k=2: Profit factor / trade quality
        pf = backtest_metrics.get("oos_profit_factor", 0.0)
        e2 = max(0.0, (pf - 1.0) * 2.0)

        evidence_vec = np.array([e0, e1, e2], dtype=np.float64)
        c_state = self.credal_model.evaluate_evidence(evidence_vec)
        return float(c_state.vacuity), c_state

    def prune(
        self,
        factor: EvolvedFactor,
        factor_series: Optional[pd.Series],
        forward_returns: pd.Series,
    ) -> EvolvedFactor:
        """Prune factor if IC < 0.02 or vacuity u > 0.35 or evaluation failed."""
        if factor_series is None:
            factor.pruned = True
            factor.prune_reason = "EVALUATION_FAILED_OR_CONSTANT"
            factor.vacuity_u = 1.0
            return factor

        # Compute IC / IR
        p_ic, s_ic, ic_std, ic_ir = self.compute_ic_ir(factor_series, forward_returns)
        factor.score = FactorScore(
            expression=factor.expression,
            ic_mean=p_ic,
            ic_std=ic_std,
            rank_ic_mean=s_ic,
            rank_ic_std=ic_std,
            ic_ir=ic_ir,
            rank_ic_ir=s_ic / (ic_std + 1e-9),
            t_stat=p_ic / (ic_std + 1e-9) * math.sqrt(max(1, len(factor_series.dropna()))),
            turnover=0.1,
            fitness=abs(p_ic) * ic_ir,
            n_samples=len(factor_series.dropna()),
        )

        # Compute Credal Epistemic Vacuity u
        vacuity_u, credal_state = self.compute_credal_vacuity(factor.score, factor.backtest_metrics)
        factor.vacuity_u = vacuity_u
        factor.credal_state = credal_state

        # Pruning decisions
        reasons: List[str] = []
        if abs(p_ic) < self.ic_threshold:
            reasons.append(f"IC_BELOW_THRESHOLD (abs_ic={abs(p_ic):.4f} < {self.ic_threshold:.4f})")

        if vacuity_u > self.vacuity_threshold:
            reasons.append(f"HIGH_EPISTEMIC_VACUITY (u={vacuity_u:.4f} > {self.vacuity_threshold:.4f})")

        if factor.backtest_metrics.get("trade_count", 0) < self.min_trade_count:
            reasons.append(f"INSUFFICIENT_TRADES ({factor.backtest_metrics.get('trade_count', 0)} < {self.min_trade_count})")

        if reasons:
            factor.pruned = True
            factor.prune_reason = "; ".join(reasons)
        else:
            factor.pruned = False
            factor.prune_reason = None

        return factor


# ---------------------------------------------------------------------------
# Master Workflow: run_rd_agent_iteration
# ---------------------------------------------------------------------------

def run_rd_agent_iteration(
    df: pd.DataFrame,
    num_generations: int = 3,
    population_size: int = 8,
    ic_threshold: float = 0.02,
    vacuity_threshold: float = 0.35,
    seed: int = 42,
) -> Dict[str, Any]:
    """Execute complete Microsoft RD-Agent Quant autonomous evolutionary research loop.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market price series (open, high, low, close, volume).
    num_generations : int, default=3
        Number of evolutionary generations.
    population_size : int, default=8
        Number of factor individuals per generation.
    ic_threshold : float, default=0.02
        Minimum acceptable Pearson Information Coefficient.
    vacuity_threshold : float, default=0.35
        Maximum acceptable Credal Epistemic Vacuity u.
    seed : int, default=42
        Reproducibility seed.

    Returns
    -------
    dict
        Dictionary containing:
        - "best_factor": dict representation of the top evolved factor.
        - "hypothesis_log": list of all formulated hypotheses.
        - "convergence_report": generation-by-generation convergence metrics.
        - "generation_history": factors evolved per generation.
    """
    # 1. Feature Extraction: Qlib and AlphaGPT micro-structure primitives
    alpha_features = compute_alphagpt_factors(df)

    # Calculate causal 1-bar forward return for IC evaluation
    close_col = "close" if "close" in df.columns else [c for c in df.columns if "close" in str(c).lower()][0]
    close = df[close_col].astype(float)
    forward_returns = (close.shift(-1) / close - 1.0).fillna(0.0)

    # Setup components
    hypo_gen = HypothesisGenerator(seed=seed)
    factor_evolver = FactorEvolver(seed=seed)
    evaluator = BacktestEvaluator(maker_fee=0.0002, taker_fee=0.0005, slippage=0.0005, split_ratio=0.8)
    pruner = FeedbackPruner(ic_threshold=ic_threshold, vacuity_threshold=vacuity_threshold)

    available_features = list(alpha_features.columns)

    hypothesis_log: List[Dict[str, Any]] = []
    generation_history: List[List[Dict[str, Any]]] = []
    convergence_report: List[Dict[str, Any]] = []

    current_population: List[EvolvedFactor] = []
    survivors: List[EvolvedFactor] = []
    feedback: List[Dict[str, Any]] = []

    for gen in range(num_generations):
        # 1. Generate / Adapt Hypotheses
        active_hypotheses = hypo_gen.generate(
            num_hypotheses=max(2, population_size // 3),
            generation=gen,
            feedback=feedback,
        )
        for h in active_hypotheses:
            hypothesis_log.append(h.to_dict())

        # 2. Factor Evolution (Symbolic crossover, mutation, prompt-mutation)
        if gen == 0:
            current_population = factor_evolver.generate_seed_factors(
                active_hypotheses,
                available_features,
                factors_per_hypothesis=max(2, population_size // len(active_hypotheses)),
            )
            # Ensure population size
            while len(current_population) < population_size:
                extra = factor_evolver.generate_seed_factors(
                    [active_hypotheses[0]],
                    available_features,
                    factors_per_hypothesis=1,
                )
                current_population.extend(extra)
            current_population = current_population[:population_size]
        else:
            current_population = factor_evolver.evolve_population(
                survivors=survivors,
                hypotheses=active_hypotheses,
                available_features=available_features,
                target_population_size=population_size,
                generation=gen,
            )

        # 3. Backtest Evaluation & Feedback Pruning
        evaluated_generation: List[EvolvedFactor] = []
        gen_survivors: List[EvolvedFactor] = []

        for factor in current_population:
            f_series, b_metrics = evaluator.evaluate(factor, alpha_features, forward_returns)
            factor.backtest_metrics = b_metrics
            pruned_factor = pruner.prune(factor, f_series, forward_returns)
            evaluated_generation.append(pruned_factor)

            if not pruned_factor.pruned:
                gen_survivors.append(pruned_factor)

        # Record generation history
        generation_history.append([f.to_dict() for f in evaluated_generation])

        # Update survivors for next cycle
        if gen_survivors:
            # Sort survivors by combination of IC and OOS Sharpe
            gen_survivors.sort(
                key=lambda f: (
                    (abs(f.score.ic_mean) if f.score else 0.0) * 0.5
                    + f.backtest_metrics.get("oos_sharpe", 0.0) * 0.5
                    - f.vacuity_u * 0.2
                ),
                reverse=True,
            )
            survivors = gen_survivors[:max(2, population_size // 2)]
        else:
            # If all pruned, carry over top ranked from evaluated to prevent complete collapse
            ranked = sorted(
                evaluated_generation,
                key=lambda f: (abs(f.score.ic_mean) if f.score else 0.0),
                reverse=True,
            )
            survivors = ranked[:2]

        # Prepare feedback for next hypothesis generation
        feedback = []
        for s in survivors:
            feedback.append({
                "status": "validated" if not s.pruned else "candidate",
                "hypothesis_id": s.hypothesis_id,
                "ic": s.score.ic_mean if s.score else 0.0,
                "vacuity_u": s.vacuity_u,
            })

        # Convergence report for this generation
        valid_ics = [abs(f.score.ic_mean) for f in evaluated_generation if f.score]
        valid_vacuities = [f.vacuity_u for f in evaluated_generation]
        convergence_report.append({
            "generation": gen,
            "population_count": len(evaluated_generation),
            "survivor_count": len(gen_survivors),
            "pruned_count": len(evaluated_generation) - len(gen_survivors),
            "mean_abs_ic": float(np.mean(valid_ics)) if valid_ics else 0.0,
            "max_abs_ic": float(np.max(valid_ics)) if valid_ics else 0.0,
            "mean_vacuity_u": float(np.mean(valid_vacuities)) if valid_vacuities else 1.0,
            "min_vacuity_u": float(np.min(valid_vacuities)) if valid_vacuities else 1.0,
        })

    # Find the globally best factor across all generations
    all_factors: List[Dict[str, Any]] = [
        f_dict for gen_list in generation_history for f_dict in gen_list
    ]

    # Best factor prioritizes unpruned, highest rank IC, lowest vacuity
    def score_factor(f_dict: Dict[str, Any]) -> float:
        unpruned_bonus = 10.0 if not f_dict["pruned"] else 0.0
        ic_part = abs(f_dict.get("ic", 0.0)) * 5.0
        vacuity_penalty = -f_dict.get("vacuity_u", 1.0) * 2.0
        sharpe_part = max(-2.0, min(5.0, f_dict.get("backtest_metrics", {}).get("oos_sharpe", 0.0)))
        return unpruned_bonus + ic_part + vacuity_penalty + sharpe_part

    best_factor = max(all_factors, key=score_factor) if all_factors else {}

    return {
        "best_factor": best_factor,
        "hypothesis_log": hypothesis_log,
        "convergence_report": convergence_report,
        "generation_history": generation_history,
    }
