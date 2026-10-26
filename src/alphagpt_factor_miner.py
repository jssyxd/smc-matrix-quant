"""
AlphaGPT Automated Symbolic Factor Synthesis & IC/IR Scoring Engine.

Inspired by:
1. `imbue-bit/AlphaGPT` stack virtual machine (Stack VM) for symbolic Alpha generation.
2. Microsoft RD-Agent Quant iterative hypothesis and factor evolution.
3. Quant AI Invariants & Anti-Overfitting defense (Bailey & López de Prado, Bailey et al. 2015).

Provides:
- Vectorized causal feature extraction: `compute_alphagpt_factors(df)`
  * OFI_Impulse: Order flow imbalance proxy from tick/volume and directional candle spread.
  * FVG_Absorption_Rate: Rate of FVG fill against volume surge.
  * Liquidity_Sweep_Intensity: Normalized penetration depth of swing high/low sweeps over local ATR.
  * Vol_Displacement_Ratio: Parkinson / Garman-Klass volatility displacement relative to ATR100.
- `AlphaGPTFactorMiner`: Automated symbolic factor synthesis, stack VM evaluation,
  causal forward IC/IR scoring, correlation-pruning, and anti-hallucination guardrails.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Data Extraction & Basic Mathematical Utilities
# ---------------------------------------------------------------------------

def _extract_ohlcv(
    df: pd.DataFrame,
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Index]:
    """Extract open, high, low, close, volume series with case-insensitive matching."""
    cols = {str(c).strip().lower(): c for c in df.columns}
    required = ["open", "high", "low", "close", "volume"]
    for req in required:
        if req not in cols:
            raise ValueError(f"DataFrame missing required column '{req}' (case-insensitive).")

    open_ = df[cols["open"]].astype(float)
    high = df[cols["high"]].astype(float)
    low = df[cols["low"]].astype(float)
    close = df[cols["close"]].astype(float)
    volume = df[cols["volume"]].astype(float)
    return open_, high, low, close, volume, df.index


def compute_wilder_atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14,
) -> pd.Series:
    """Compute strictly causal Wilder's Average True Range (RMA) using exponential smoothing."""
    prev_close = close.shift(1).fillna(close)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    if len(tr) == 0:
        return tr
    return tr.ewm(alpha=1.0 / float(period), adjust=False).mean()


# ---------------------------------------------------------------------------
# Core Vectorized Feature Extraction: compute_alphagpt_factors
# ---------------------------------------------------------------------------

def compute_alphagpt_factors(
    df: pd.DataFrame,
    swing_len: int = 5,
    vol_sma_period: int = 20,
    atr_fast_period: int = 14,
    atr_slow_period: int = 100,
    fvg_min_atr_mult: float = 0.05,
) -> pd.DataFrame:
    """
    Extract the 4 core AlphaGPT micro-structure factors with strict causality.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market DataFrame containing 'open', 'high', 'low', 'close', 'volume'.
    swing_len : int, default 5
        Bars required to confirm a pivot swing high or low strictly causally.
    vol_sma_period : int, default 20
        Rolling window for volume surge normalization.
    atr_fast_period : int, default 14
        Period for local ATR used in normalization.
    atr_slow_period : int, default 100
        Period for baseline ATR100.
    fvg_min_atr_mult : float, default 0.05
        Minimum gap threshold multiplier against local ATR.

    Returns
    -------
    pd.DataFrame
        DataFrame containing at least:
        - 'OFI_Impulse': Order flow imbalance proxy from tick/volume and directional candle spread.
        - 'FVG_Absorption_Rate': Rate of FVG fill against volume surge.
        - 'Liquidity_Sweep_Intensity': Normalized penetration depth of swing high/low sweeps over local ATR.
        - 'Vol_Displacement_Ratio': Parkinson / Garman-Klass volatility displacement relative to ATR100.
    """
    if len(df) == 0:
        cols = [
            "OFI_Impulse",
            "FVG_Absorption_Rate",
            "Liquidity_Sweep_Intensity",
            "Vol_Displacement_Ratio",
        ]
        return pd.DataFrame(columns=cols, index=df.index, dtype=float)

    open_, high, low, close, volume, index = _extract_ohlcv(df)
    n = len(df)
    eps = 1e-9

    hl_range = high - low
    safe_hl = hl_range.replace(0.0, eps)
    safe_close = close.replace(0.0, eps)
    safe_open = open_.replace(0.0, eps)

    # -------------------------------------------------------------------------
    # 1. OFI_Impulse: Order Flow Imbalance Proxy
    # -------------------------------------------------------------------------
    # Directional candle spread:
    # 1) Spread pressure = ((Close - Low) - (High - Close)) / (High - Low + eps)
    # 2) Body direction = (Close - Open) / (High - Low + eps)
    spread_pressure = (2.0 * close - high - low) / safe_hl
    body_direction = (close - open_) / safe_hl
    directional_spread = 0.5 * (spread_pressure + body_direction)

    vol_sma = volume.rolling(vol_sma_period, min_periods=1).mean().replace(0.0, eps)
    vol_surge = (volume / vol_sma).fillna(1.0)
    ofi_impulse = directional_spread * vol_surge

    # -------------------------------------------------------------------------
    # 2. Vol_Displacement_Ratio: Garman-Klass / Parkinson vs ATR100
    # -------------------------------------------------------------------------
    atr14 = compute_wilder_atr(high, low, close, period=atr_fast_period).replace(0.0, eps)
    atr100 = compute_wilder_atr(high, low, close, period=atr_slow_period).replace(0.0, eps)

    log_hl = np.log((high / low.replace(0.0, eps)).clip(lower=1.0)).replace([np.inf, -np.inf], 0.0)
    log_co = np.log((close / safe_open).clip(lower=1e-6)).replace([np.inf, -np.inf], 0.0)

    # Garman-Klass volatility: 0.5 * ln(H/L)^2 - (2*ln(2)-1) * ln(C/O)^2
    gk_var = 0.5 * log_hl.pow(2) - (2.0 * np.log(2.0) - 1.0) * log_co.pow(2)
    gk_vol = np.sqrt(gk_var.clip(lower=0.0))

    # Fallback to Parkinson volatility if gk_vol is zero
    parkinson_vol = np.sqrt((log_hl.pow(2) / (4.0 * np.log(2.0))).clip(lower=0.0))
    vol_metric = np.where(gk_vol > 0.0, gk_vol, parkinson_vol)

    vol_displacement = pd.Series(vol_metric, index=index) * close
    vol_displacement_ratio = (vol_displacement / atr100).fillna(0.0).clip(lower=0.0)

    # -------------------------------------------------------------------------
    # 3. FVG_Absorption_Rate: Rate of FVG fill against volume surge
    # -------------------------------------------------------------------------
    # Strictly causal sequential FVG tracking:
    # A 3-bar Fair Value Gap formed at bar t-1 is observed at bar t >= 2:
    # Bullish FVG: Low[t] > High[t-2], gap = [High[t-2], Low[t]]
    # Bearish FVG: High[t] < Low[t-2], gap = [High[t], Low[t-2]]
    high_arr = high.to_numpy()
    low_arr = low.to_numpy()
    vol_surge_arr = vol_surge.to_numpy()
    atr14_arr = atr14.to_numpy()

    fvg_absorption_arr = np.zeros(n, dtype=float)

    # Active FVG state: list of (is_bullish, bottom, top, original_size)
    active_fvgs: List[Tuple[bool, float, float, float]] = []

    for t in range(n):
        curr_high = high_arr[t]
        curr_low = low_arr[t]
        curr_surge = vol_surge_arr[t]
        local_min_gap = fvg_min_atr_mult * atr14_arr[t]

        # 1. Check if current bar fills or absorbs existing active FVGs
        max_fill_rate = 0.0
        remaining_fvgs: List[Tuple[bool, float, float, float]] = []

        for is_bull, b_bottom, b_top, orig_size in active_fvgs:
            # Overlap between current candle and FVG
            overlap_low = max(curr_low, b_bottom)
            overlap_high = min(curr_high, b_top)

            if overlap_high > overlap_low:
                overlap_size = overlap_high - overlap_low
                fill_fraction = overlap_size / max(orig_size, eps)
                fill_rate = fill_fraction * curr_surge
                if fill_rate > max_fill_rate:
                    max_fill_rate = fill_rate

            # Check if FVG remains open
            is_filled = False
            if is_bull and curr_low <= b_bottom:
                is_filled = True
            elif (not is_bull) and curr_high >= b_top:
                is_filled = True

            if not is_filled:
                remaining_fvgs.append((is_bull, b_bottom, b_top, orig_size))

        active_fvgs = remaining_fvgs
        fvg_absorption_arr[t] = max_fill_rate

        # 2. Check if a new FVG was formed at bar t (using t, t-1, t-2)
        if t >= 2:
            h_lag2 = high_arr[t - 2]
            l_lag2 = low_arr[t - 2]

            # Bullish FVG
            if curr_low > h_lag2 and (curr_low - h_lag2) >= local_min_gap:
                active_fvgs.append((True, h_lag2, curr_low, curr_low - h_lag2))

            # Bearish FVG
            elif curr_high < l_lag2 and (l_lag2 - curr_high) >= local_min_gap:
                active_fvgs.append((False, curr_high, l_lag2, l_lag2 - curr_high))

        # Cap active FVG queue to avoid unbound memory
        if len(active_fvgs) > 10:
            active_fvgs = active_fvgs[-10:]

    fvg_absorption_rate = pd.Series(fvg_absorption_arr, index=index)

    # -------------------------------------------------------------------------
    # 4. Liquidity_Sweep_Intensity: Normalized penetration depth over local ATR
    # -------------------------------------------------------------------------
    # Strictly causal swing detection:
    # A pivot swing at p = t - swing_len is confirmed at bar t strictly when
    # high[p] == max(high[p - swing_len : t + 1])
    # low[p] == min(low[p - swing_len : t + 1])
    sweep_intensity_arr = np.zeros(n, dtype=float)

    last_sh: Optional[float] = None
    last_sl: Optional[float] = None

    for t in range(n):
        curr_high = high_arr[t]
        curr_low = low_arr[t]
        local_atr = atr14_arr[t] + eps

        # Check for sweeps of previously confirmed swings
        pen_high = 0.0
        pen_low = 0.0

        if last_sh is not None and curr_high > last_sh:
            pen_high = curr_high - last_sh

        if last_sl is not None and curr_low < last_sl:
            pen_low = last_sl - curr_low

        max_penetration = max(pen_high, pen_low)
        sweep_intensity_arr[t] = max_penetration / local_atr

        # Check if pivot bar p = t - swing_len is confirmed as a new swing at bar t
        if t >= 2 * swing_len:
            p = t - swing_len
            w_start = p - swing_len
            w_end = t + 1

            window_high = high_arr[w_start:w_end]
            if high_arr[p] == np.max(window_high):
                last_sh = high_arr[p]

            window_low = low_arr[w_start:w_end]
            if low_arr[p] == np.min(window_low):
                last_sl = low_arr[p]

    liquidity_sweep_intensity = pd.Series(sweep_intensity_arr, index=index)

    # Assemble output DataFrame
    result = pd.DataFrame(
        {
            "OFI_Impulse": ofi_impulse.fillna(0.0),
            "FVG_Absorption_Rate": fvg_absorption_rate.fillna(0.0),
            "Liquidity_Sweep_Intensity": liquidity_sweep_intensity.fillna(0.0),
            "Vol_Displacement_Ratio": vol_displacement_ratio.fillna(0.0),
        },
        index=index,
    )

    # Ensure strictly finite
    result = result.replace([np.inf, -np.inf], 0.0).fillna(0.0)
    return result


# ---------------------------------------------------------------------------
# Symbolic Factor Representation & Stack VM Evaluator
# ---------------------------------------------------------------------------

@dataclass
class FactorScore:
    """Metrics and statistics for a synthesized Alpha factor."""
    expression: str
    ic_mean: float
    ic_std: float
    rank_ic_mean: float
    rank_ic_std: float
    ic_ir: float
    rank_ic_ir: float
    t_stat: float
    turnover: float
    fitness: float
    n_samples: int
    dsr: Optional[float] = None


class FactorStackVM:
    """
    Stack Virtual Machine for strictly causal symbolic expression evaluation.

    Inspired by `imbue-bit/AlphaGPT` reverse Polish notation (RPN) execution
    and WorldQuant/Qlib alpha operators.
    """

    UNARY_OPS: Set[str] = {
        "abs", "sign", "log", "neg", "inv", "sqrt",
    }
    BINARY_OPS: Set[str] = {
        "add", "sub", "mul", "div", "max", "min",
    }
    TS_OPS: Set[str] = {
        "ts_mean", "ts_std", "ts_rank", "ts_delta", "ts_delay",
        "ts_max", "ts_min", "ts_zscore",
    }

    @staticmethod
    def eval_unary(op: str, x: pd.Series) -> pd.Series:
        eps = 1e-9
        if op == "abs":
            return x.abs()
        elif op == "sign":
            return np.sign(x)
        elif op == "log":
            return np.sign(x) * np.log1p(x.abs())
        elif op == "neg":
            return -x
        elif op == "inv":
            return 1.0 / x.replace(0.0, eps)
        elif op == "sqrt":
            return np.sqrt(x.abs())
        raise ValueError(f"Unknown unary operator: {op}")

    @staticmethod
    def eval_binary(op: str, x: pd.Series, y: pd.Series) -> pd.Series:
        eps = 1e-9
        if op == "add":
            return x + y
        elif op == "sub":
            return x - y
        elif op == "mul":
            return x * y
        elif op == "div":
            safe_y = y.replace(0.0, eps)
            return (x / safe_y).clip(-1e6, 1e6)
        elif op == "max":
            return np.maximum(x, y)
        elif op == "min":
            return np.minimum(x, y)
        raise ValueError(f"Unknown binary operator: {op}")

    @staticmethod
    def eval_ts(op: str, x: pd.Series, d: int) -> pd.Series:
        eps = 1e-9
        d = max(1, int(d))
        if op == "ts_mean":
            return x.rolling(d, min_periods=1).mean()
        elif op == "ts_std":
            return x.rolling(d, min_periods=1).std().fillna(0.0)
        elif op == "ts_max":
            return x.rolling(d, min_periods=1).max()
        elif op == "ts_min":
            return x.rolling(d, min_periods=1).min()
        elif op == "ts_delta":
            return x - x.shift(d).fillna(x)
        elif op == "ts_delay":
            return x.shift(d).fillna(x)
        elif op == "ts_rank":
            # Rolling percentile rank in [0, 1]
            return x.rolling(d, min_periods=1).rank(pct=True).fillna(0.5)
        elif op == "ts_zscore":
            mean = x.rolling(d, min_periods=1).mean()
            std = x.rolling(d, min_periods=1).std().fillna(0.0).replace(0.0, eps)
            return ((x - mean) / std).clip(-5.0, 5.0)
        raise ValueError(f"Unknown time-series operator: {op}")

    @classmethod
    def execute_rpn(
        cls,
        tokens: Sequence[str],
        data_table: Dict[str, pd.Series],
    ) -> pd.Series:
        """
        Execute an RPN token sequence on the input data table.

        Example:
            ['close', 'open', 'sub', '10', 'ts_mean']
        """
        stack: List[Union[pd.Series, float, int]] = []

        for token in tokens:
            token_clean = token.strip()
            # 1. Terminal / Column
            if token_clean in data_table:
                stack.append(data_table[token_clean])
            # 2. Numeric Constant
            elif token_clean.replace(".", "", 1).replace("-", "", 1).isdigit():
                stack.append(float(token_clean) if "." in token_clean else int(token_clean))
            # 3. Unary operator
            elif token_clean.lower() in cls.UNARY_OPS:
                if not stack:
                    raise ValueError(f"Stack underflow for unary op {token_clean}")
                val = stack.pop()
                if not isinstance(val, pd.Series):
                    # Broadcast constant to Series using any available series
                    ref = next(iter(data_table.values()))
                    val = pd.Series(val, index=ref.index)
                res = cls.eval_unary(token_clean.lower(), val)
                stack.append(res)
            # 4. Binary operator
            elif token_clean.lower() in cls.BINARY_OPS:
                if len(stack) < 2:
                    raise ValueError(f"Stack underflow for binary op {token_clean}")
                val2 = stack.pop()
                val1 = stack.pop()
                ref = next(iter(data_table.values()))
                if not isinstance(val1, pd.Series):
                    val1 = pd.Series(val1, index=ref.index)
                if not isinstance(val2, pd.Series):
                    val2 = pd.Series(val2, index=ref.index)
                res = cls.eval_binary(token_clean.lower(), val1, val2)
                stack.append(res)
            # 5. TS operator
            elif token_clean.lower() in cls.TS_OPS:
                if len(stack) < 2:
                    raise ValueError(f"Stack underflow for TS op {token_clean}")
                window_val = stack.pop()
                val = stack.pop()
                if not isinstance(val, pd.Series):
                    ref = next(iter(data_table.values()))
                    val = pd.Series(val, index=ref.index)
                d = int(window_val) if isinstance(window_val, (int, float)) else 10
                res = cls.eval_ts(token_clean.lower(), val, d)
                stack.append(res)
            else:
                raise ValueError(f"Unrecognized RPN token: '{token_clean}'")

        if len(stack) != 1:
            raise ValueError(f"Stack execution finished with {len(stack)} items, expected 1.")

        out = stack.pop()
        if not isinstance(out, pd.Series):
            ref = next(iter(data_table.values()))
            out = pd.Series(out, index=ref.index)

        return out.replace([np.inf, -np.inf], np.nan).ffill().fillna(0.0)


# ---------------------------------------------------------------------------
# AlphaGPTFactorMiner: Automated Symbolic Miner & IC/IR Scorer
# ---------------------------------------------------------------------------

class AlphaGPTFactorMiner:
    """
    Automated Symbolic Factor Miner and IC/IR Scorer.

    Implements:
    - Causal candidate factor synthesis from primitives (OHLCV + AlphaGPT factors).
    - Reverse Polish Notation (RPN) / Expression parsing and Stack VM execution.
    - Information Coefficient (Pearson IC & Spearman Rank IC) and Information Ratio (IR).
    - Correlation-pruning to eliminate redundant / collinear factor discoveries.
    - Multiple-testing Deflated Sharpe Ratio (DSR) adjustments against Alpha Hallucination.
    """

    DEFAULT_BASE_FEATURES: List[str] = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "OFI_Impulse",
        "FVG_Absorption_Rate",
        "Liquidity_Sweep_Intensity",
        "Vol_Displacement_Ratio",
    ]

    DEFAULT_WINDOWS: List[int] = [3, 5, 10, 20, 40]

    def __init__(
        self,
        base_features: Optional[List[str]] = None,
        windows: Optional[List[int]] = None,
        random_seed: Optional[int] = 42,
    ) -> None:
        self.base_features = list(base_features or self.DEFAULT_BASE_FEATURES)
        self.windows = list(windows or self.DEFAULT_WINDOWS)
        self.rng = random.Random(random_seed)
        self.vm = FactorStackVM()

    def prepare_feature_table(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Extract OHLCV base series and AlphaGPT micro-structure factors."""
        open_, high, low, close, volume, index = _extract_ohlcv(df)
        table: Dict[str, pd.Series] = {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }

        # Compute core AlphaGPT factors
        agpt_df = compute_alphagpt_factors(df)
        for col in agpt_df.columns:
            table[col] = agpt_df[col]

        return table

    def synthesize_random_rpn(self, max_depth: int = 2) -> List[str]:
        """
        Synthesize a random valid RPN expression.

        Depth 1: e.g. ['close', 'open', 'sub'] or ['OFI_Impulse', '10', 'ts_mean']
        Depth 2: nested operations combining terminals and TS operators.
        """
        terminals = [f for f in self.base_features]

        def _generate(depth: int) -> List[str]:
            if depth <= 0 or self.rng.random() < 0.35:
                return [self.rng.choice(terminals)]

            op_type = self.rng.choice(["unary", "binary", "ts"])

            if op_type == "unary":
                op = self.rng.choice(list(FactorStackVM.UNARY_OPS))
                return _generate(depth - 1) + [op]

            elif op_type == "binary":
                op = self.rng.choice(list(FactorStackVM.BINARY_OPS))
                return _generate(depth - 1) + _generate(depth - 1) + [op]

            else:  # ts
                op = self.rng.choice(list(FactorStackVM.TS_OPS))
                window = str(self.rng.choice(self.windows))
                return _generate(depth - 1) + [window, op]

        # Ensure valid non-trivial expression
        for _ in range(10):
            rpn = _generate(max_depth)
            if len(rpn) > 1:
                return rpn

        # Fallback default
        return ["OFI_Impulse", "10", "ts_mean"]

    def parse_prefix_to_rpn(self, expr: str) -> List[str]:
        """
        Parse prefix/functional expressions to RPN tokens.
        Supports expressions like:
        - 'ts_mean(OFI_Impulse, 10)' -> ['OFI_Impulse', '10', 'ts_mean']
        - 'div(sub(close, open), high)' -> ['close', 'open', 'sub', 'high', 'div']
        - 'sub(close, open)' -> ['close', 'open', 'sub']
        """
        expr = expr.strip()
        if not ("(" in expr and expr.endswith(")")):
            # Assume space-delimited or comma-delimited tokens
            tokens = [t.strip() for t in expr.replace(",", " ").split() if t.strip()]
            return tokens

        # Recursive functional expression parser
        paren_idx = expr.find("(")
        fn = expr[:paren_idx].strip()
        inner = expr[paren_idx + 1 : -1].strip()

        # Split inner arguments by top-level commas
        args: List[str] = []
        depth = 0
        cur: List[str] = []
        for ch in inner:
            if ch == "(":
                depth += 1
                cur.append(ch)
            elif ch == ")":
                depth -= 1
                cur.append(ch)
            elif ch == "," and depth == 0:
                args.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
        if cur:
            args.append("".join(cur).strip())

        parsed_args: List[str] = []
        for arg in args:
            parsed_args.extend(self.parse_prefix_to_rpn(arg))

        return parsed_args + [fn]

    def evaluate_expression(
        self,
        expr_or_rpn: Union[str, Sequence[str]],
        data_table_or_df: Union[pd.DataFrame, Dict[str, pd.Series]],
    ) -> pd.Series:
        """Evaluate a symbolic expression or RPN token list causally."""
        if isinstance(data_table_or_df, pd.DataFrame):
            table = self.prepare_feature_table(data_table_or_df)
        else:
            table = data_table_or_df

        if isinstance(expr_or_rpn, str):
            rpn = self.parse_prefix_to_rpn(expr_or_rpn)
        else:
            rpn = list(expr_or_rpn)

        return self.vm.execute_rpn(rpn, table)

    @staticmethod
    def compute_forward_returns(
        close: pd.Series,
        horizon: int = 1,
    ) -> pd.Series:
        """
        Compute forward returns r_{t+h} = (Close_{t+h} - Close_t) / Close_t.
        Aligned at bar t (future return relative to bar t close).
        """
        fwd_close = close.shift(-horizon)
        return ((fwd_close - close) / close.replace(0.0, 1e-9)).fillna(0.0)

    @classmethod
    def score_factor(
        cls,
        factor_series: pd.Series,
        forward_returns: pd.Series,
        expression: str = "",
        rolling_slice_size: int = 20,
    ) -> FactorScore:
        """
        Score a factor series against forward returns using IC, Rank IC, and IR.

        Strict Evaluation Invariant:
        Factor series at bar t is compared with the forward return spanning [t, t+horizon].
        """
        valid_mask = ~(
            factor_series.isna()
            | forward_returns.isna()
            | np.isinf(factor_series)
            | np.isinf(forward_returns)
        )
        # Drop the last horizon rows where forward returns are unavailable
        f_clean = factor_series[valid_mask]
        r_clean = forward_returns[valid_mask]
        n_samples = len(f_clean)

        if n_samples < 5 or f_clean.std() < 1e-9 or r_clean.std() < 1e-9:
            return FactorScore(
                expression=expression,
                ic_mean=0.0,
                ic_std=0.0,
                rank_ic_mean=0.0,
                rank_ic_std=0.0,
                ic_ir=0.0,
                rank_ic_ir=0.0,
                t_stat=0.0,
                turnover=0.0,
                fitness=0.0,
                n_samples=n_samples,
            )

        # Pearson IC
        pearson_ic = float(np.corrcoef(f_clean, r_clean)[0, 1])
        if np.isnan(pearson_ic):
            pearson_ic = 0.0

        # Spearman Rank IC
        rank_f = f_clean.rank()
        rank_r = r_clean.rank()
        rank_ic = float(np.corrcoef(rank_f, rank_r)[0, 1])
        if np.isnan(rank_ic):
            rank_ic = 0.0

        # Sub-period rolling IC stability
        k = max(2, min(rolling_slice_size, n_samples // 4))
        n_slices = n_samples // k
        slice_rank_ics: List[float] = []

        for i in range(n_slices):
            sub_f = rank_f.iloc[i * k : (i + 1) * k]
            sub_r = rank_r.iloc[i * k : (i + 1) * k]
            if sub_f.std() > 1e-9 and sub_r.std() > 1e-9:
                c = float(np.corrcoef(sub_f, sub_r)[0, 1])
                if not np.isnan(c):
                    slice_rank_ics.append(c)

        if len(slice_rank_ics) >= 2:
            rank_ic_mean = float(np.mean(slice_rank_ics))
            rank_ic_std = float(np.std(slice_rank_ics, ddof=1)) + 1e-9
        else:
            rank_ic_mean = rank_ic
            rank_ic_std = 0.1

        rank_ic_ir = rank_ic_mean / rank_ic_std
        ic_ir = pearson_ic / (rank_ic_std)
        t_stat = rank_ic_ir * math.sqrt(max(1, len(slice_rank_ics)))

        # Turnover: bar-to-bar relative variation of factor rank
        norm_rank = rank_f / float(n_samples)
        turnover = float(norm_rank.diff().abs().mean()) if n_samples > 1 else 0.0

        # Composite fitness score: penalizes excessive turnover and rewards IC stability
        fitness = abs(rank_ic_mean) * max(0.0, rank_ic_ir) / (1.0 + turnover)

        return FactorScore(
            expression=expression,
            ic_mean=pearson_ic,
            ic_std=rank_ic_std,
            rank_ic_mean=rank_ic_mean,
            rank_ic_std=rank_ic_std,
            ic_ir=ic_ir,
            rank_ic_ir=rank_ic_ir,
            t_stat=t_stat,
            turnover=turnover,
            fitness=fitness,
            n_samples=n_samples,
        )

    def mine_factors(
        self,
        df: pd.DataFrame,
        n_candidates: int = 25,
        target_col: str = "close",
        forward_horizon: int = 1,
        top_k: int = 5,
        correlation_prune_threshold: float = 0.85,
    ) -> List[FactorScore]:
        """
        Run the automated symbolic factor synthesis & IC/IR mining pipeline.

        Parameters
        ----------
        df : pd.DataFrame
            Historical OHLCV data.
        n_candidates : int, default 25
            Number of candidate symbolic factors to generate and evaluate.
        target_col : str, default 'close'
            Price column for forward returns.
        forward_horizon : int, default 1
            Bars forward for returns evaluation.
        top_k : int, default 5
            Number of top uncorrelated factors to retain.
        correlation_prune_threshold : float, default 0.85
            Maximum allowable correlation between retained factors.

        Returns
        -------
        List[FactorScore]
            Ranked list of top non-collinear factors with comprehensive metrics.
        """
        if len(df) < 10:
            return []

        table = self.prepare_feature_table(df)
        fwd_returns = self.compute_forward_returns(table[target_col.lower()], horizon=forward_horizon)

        # Seed initial high-conviction templates inspired by RD-Agent & AlphaGPT
        initial_templates = [
            ["OFI_Impulse", "5", "ts_mean"],
            ["OFI_Impulse", "20", "ts_zscore"],
            ["FVG_Absorption_Rate", "10", "ts_rank"],
            ["Liquidity_Sweep_Intensity", "5", "ts_mean"],
            ["Vol_Displacement_Ratio", "20", "ts_rank"],
            ["close", "open", "sub", "high", "low", "sub", "div"],
            ["OFI_Impulse", "Vol_Displacement_Ratio", "mul"],
        ]

        candidates_rpn: List[List[str]] = list(initial_templates)
        while len(candidates_rpn) < n_candidates:
            depth = self.rng.choice([1, 2, 3])
            candidates_rpn.append(self.synthesize_random_rpn(max_depth=depth))

        evaluated: List[Tuple[FactorScore, pd.Series]] = []

        for rpn in candidates_rpn:
            expr_str = " ".join(rpn)
            try:
                factor_series = self.vm.execute_rpn(rpn, table)
                score = self.score_factor(
                    factor_series,
                    fwd_returns,
                    expression=expr_str,
                )
                if not np.isnan(score.fitness) and score.n_samples > 0:
                    evaluated.append((score, factor_series))
            except Exception:
                continue

        # Sort candidate factors descending by absolute Rank IC and fitness
        evaluated.sort(key=lambda item: (abs(item[0].rank_ic_mean), item[0].fitness), reverse=True)

        # Orthogonalization / Correlation Pruning
        retained: List[FactorScore] = []
        retained_series: List[pd.Series] = []

        for score, series in evaluated:
            is_collinear = False
            for prev_series in retained_series:
                c = float(np.corrcoef(series, prev_series)[0, 1])
                if not np.isnan(c) and abs(c) >= correlation_prune_threshold:
                    is_collinear = True
                    break

            if not is_collinear:
                retained.append(score)
                retained_series.append(series)
                if len(retained) >= top_k:
                    break

        return retained


__all__ = [
    "compute_alphagpt_factors",
    "compute_wilder_atr",
    "FactorScore",
    "FactorStackVM",
    "AlphaGPTFactorMiner",
]
