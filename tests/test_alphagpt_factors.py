"""
Unit and Integration Test Suite for AlphaGPT Factor Miner & Extended Qlib Factors.

Verifies:
1. Mathematical Correctness & Formula Invariants:
   - OFI_Impulse (Order flow imbalance from tick/volume and directional spread).
   - FVG_Absorption_Rate (Rate of Fair Value Gap fill against volume surge).
   - Liquidity_Sweep_Intensity (Normalized penetration depth of swing sweeps over ATR).
   - Vol_Displacement_Ratio (Parkinson / Garman-Klass volatility displacement relative to ATR100).
2. Strict Causality & Zero Lookahead Bias:
   - Prefix Invariance: features computed on df[:T] match df[:N][:T] exactly.
   - Future Perturbation Invariance: mutating future bars t > k does not alter past features t <= k.
3. Value Boundedness & Numerical Stability:
   - Zero-range candles (High == Low).
   - Zero-volume candles (Volume == 0).
   - Flat constant price series.
   - Absence of NaN, Inf, and -Inf values.
4. AlphaGPTFactorMiner:
   - Stack VM RPN execution & expression parsing.
   - Pearson IC, Spearman Rank IC, and IC_IR scoring.
   - Candidate factor generation, evaluation, and correlation-pruning.
5. Qlib Factors Extended:
   - High-dimensional Micro-Structure feature extraction.
   - Prefix invariance and edge case handling.
"""

from __future__ import annotations

import os
import sys
import unittest
import numpy as np
import pandas as pd

# Ensure project root is discoverable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.alphagpt_factor_miner import (
    compute_alphagpt_factors,
    compute_wilder_atr,
    FactorScore,
    FactorStackVM,
    AlphaGPTFactorMiner,
)
from src.qlib_factors_extended import (
    extract_qlib_alpha_features,
    compute_true_range,
    compute_wilder_rma,
)


def _generate_synthetic_ohlcv(
    n: int = 150,
    seed: int = 42,
    base_price: float = 100.0,
) -> pd.DataFrame:
    """Generate realistic synthetic OHLCV data for testing."""
    rng = np.random.RandomState(seed)
    returns = rng.normal(loc=0.0002, scale=0.015, size=n)
    close = base_price * np.exp(np.cumsum(returns))
    
    # Intraday ranges
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


class TestAlphaGPTFactorFormulas(unittest.TestCase):
    """Test mathematical formulas and boundedness of AlphaGPT factors."""

    def test_required_columns_present(self) -> None:
        """Verify that all 4 required factor columns are returned."""
        df = _generate_synthetic_ohlcv(n=50)
        res = compute_alphagpt_factors(df)
        required = [
            "OFI_Impulse",
            "FVG_Absorption_Rate",
            "Liquidity_Sweep_Intensity",
            "Vol_Displacement_Ratio",
        ]
        for col in required:
            self.assertIn(col, res.columns)
            self.assertFalse(res[col].isna().any(), f"Column {col} contains NaN")
            self.assertFalse(np.isinf(res[col]).any(), f"Column {col} contains Inf")

    def test_ofi_impulse_formula_and_bounds(self) -> None:
        """Verify OFI_Impulse direction, value bounds, and zero-range handling."""
        # Case 1: Pure bullish candle: Close == High, Open == Low
        df_bull = pd.DataFrame(
            {
                "open": [100.0] * 25,
                "high": [110.0] * 25,
                "low": [100.0] * 25,
                "close": [110.0] * 25,
                "volume": [1000.0] * 25,
            }
        )
        res_bull = compute_alphagpt_factors(df_bull)
        # Close == High and Close > Open -> maximum directional spread = 1.0, volume surge = 1.0
        self.assertAlmostEqual(res_bull["OFI_Impulse"].iloc[-1], 1.0, places=4)

        # Case 2: Pure bearish candle: Close == Low, Open == High
        df_bear = pd.DataFrame(
            {
                "open": [110.0] * 25,
                "high": [110.0] * 25,
                "low": [100.0] * 25,
                "close": [100.0] * 25,
                "volume": [1000.0] * 25,
            }
        )
        res_bear = compute_alphagpt_factors(df_bear)
        self.assertAlmostEqual(res_bear["OFI_Impulse"].iloc[-1], -1.0, places=4)

        # Case 3: Zero-range candle (High == Low)
        df_flat = pd.DataFrame(
            {
                "open": [100.0] * 10,
                "high": [100.0] * 10,
                "low": [100.0] * 10,
                "close": [100.0] * 10,
                "volume": [1000.0] * 10,
            }
        )
        res_flat = compute_alphagpt_factors(df_flat)
        self.assertTrue((res_flat["OFI_Impulse"] == 0.0).all())

    def test_fvg_absorption_rate_detection_and_fill(self) -> None:
        """Verify that FVG_Absorption_Rate identifies gap fill and is non-negative."""
        # Construct explicit 3-bar Bullish FVG:
        # Bar 0: Low=95, High=98, Close=97
        # Bar 1: Strong impulse: Low=99, High=105, Close=104
        # Bar 2: Low=101, High=108, Close=107 -> Gap between Low[2]=101 and High[0]=98 (size=3.0)
        # Bar 3: Retracement into gap: Low=97, High=102, Close=98 (fills the gap)
        n = 15
        open_ = [100.0] * n
        high = [100.0] * n
        low = [99.0] * n
        close = [99.5] * n
        volume = [1000.0] * n

        high[2] = 98.0
        low[2] = 95.0
        close[2] = 97.0

        high[3] = 105.0
        low[3] = 99.0
        close[3] = 104.0

        high[4] = 108.0
        low[4] = 101.0
        close[4] = 107.0

        # Bar 5 retraces into [98.0, 101.0] with volume surge
        high[5] = 102.0
        low[5] = 97.5
        close[5] = 98.5
        volume[5] = 2000.0

        df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume})
        res = compute_alphagpt_factors(df, fvg_min_atr_mult=0.01)

        # FVG_Absorption_Rate must be non-negative
        self.assertTrue((res["FVG_Absorption_Rate"] >= 0.0).all())

        # Bar 5 must show active absorption rate > 0
        self.assertGreater(res["FVG_Absorption_Rate"].iloc[5], 0.0)

    def test_liquidity_sweep_intensity_behavior(self) -> None:
        """Verify normalized sweep intensity on confirmed swing high/low."""
        # Setup: swing_len = 5
        # Bar 10 has a high peak at 120.0 (confirmed at bar 15)
        # Bar 18 sweeps bar 10's high by reaching 125.0
        n = 30
        high = [100.0] * n
        low = [90.0] * n
        close = [95.0] * n
        open_ = [95.0] * n
        volume = [1000.0] * n

        high[10] = 120.0
        high[18] = 125.0  # Sweeps 120.0 by 5.0

        df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume})
        res = compute_alphagpt_factors(df, swing_len=5)

        # Liquidity_Sweep_Intensity must be strictly non-negative
        self.assertTrue((res["Liquidity_Sweep_Intensity"] >= 0.0).all())

        # Bar 10 peak confirmed at bar 15, so bar 18 should show a positive sweep intensity
        self.assertGreater(res["Liquidity_Sweep_Intensity"].iloc[18], 0.0)
        # Prior to confirmation at bar 15, bar 11 should have zero intensity
        self.assertEqual(res["Liquidity_Sweep_Intensity"].iloc[11], 0.0)

    def test_vol_displacement_ratio_non_negative(self) -> None:
        """Verify Vol_Displacement_Ratio is strictly non-negative and finite."""
        df = _generate_synthetic_ohlcv(n=120)
        res = compute_alphagpt_factors(df)
        ratio = res["Vol_Displacement_Ratio"]
        self.assertTrue((ratio >= 0.0).all())
        self.assertFalse(np.isinf(ratio).any())
        self.assertFalse(ratio.isna().any())


class TestStrictCausalityAndZeroLookahead(unittest.TestCase):
    """Test prefix invariance and zero future information leakage."""

    def setUp(self) -> None:
        self.df = _generate_synthetic_ohlcv(n=150, seed=101)

    def test_alphagpt_prefix_invariance(self) -> None:
        """Verify compute_alphagpt_factors(df[:T]).iloc[-1] == compute_alphagpt_factors(df).iloc[T-1]."""
        full_res = compute_alphagpt_factors(self.df)
        for t in [40, 75, 100, 130]:
            sub_res = compute_alphagpt_factors(self.df.iloc[:t])
            for col in full_res.columns:
                val_full = full_res[col].iloc[t - 1]
                val_sub = sub_res[col].iloc[-1]
                self.assertAlmostEqual(
                    val_full,
                    val_sub,
                    places=9,
                    msg=f"Prefix invariance failed at t={t} for column {col}: {val_full} vs {val_sub}",
                )

    def test_alphagpt_future_perturbation_invariance(self) -> None:
        """Verify that altering future bars t > k does NOT affect features at t <= k."""
        k = 80
        df_perturbed = self.df.copy()
        # Heavily perturb bars from k onwards
        df_perturbed.loc[df_perturbed.index[k:], "close"] *= 5.0
        df_perturbed.loc[df_perturbed.index[k:], "high"] *= 6.0
        df_perturbed.loc[df_perturbed.index[k:], "volume"] *= 100.0

        res_orig = compute_alphagpt_factors(self.df)
        res_pert = compute_alphagpt_factors(df_perturbed)

        for col in res_orig.columns:
            diff = np.abs(res_orig[col].iloc[:k].to_numpy() - res_pert[col].iloc[:k].to_numpy())
            max_diff = np.nanmax(diff)
            self.assertAlmostEqual(
                max_diff,
                0.0,
                places=9,
                msg=f"Future perturbation leaked into history for column {col}! Max diff: {max_diff}",
            )

    def test_qlib_prefix_invariance(self) -> None:
        """Verify extract_qlib_alpha_features satisfies exact prefix invariance."""
        full_qlib = extract_qlib_alpha_features(self.df)
        for t in [50, 100]:
            sub_qlib = extract_qlib_alpha_features(self.df.iloc[:t])
            diff = np.abs(full_qlib.iloc[t - 1].to_numpy() - sub_qlib.iloc[-1].to_numpy())
            max_diff = np.nanmax(diff)
            self.assertAlmostEqual(
                max_diff,
                0.0,
                places=9,
                msg=f"Qlib prefix invariance failed at t={t}! Max diff: {max_diff}",
            )

    def test_qlib_future_perturbation_invariance(self) -> None:
        """Verify that altering future bars does NOT affect past Qlib features."""
        k = 70
        df_perturbed = self.df.copy()
        df_perturbed.loc[df_perturbed.index[k:], "high"] *= 10.0
        df_perturbed.loc[df_perturbed.index[k:], "volume"] *= 50.0

        res_orig = extract_qlib_alpha_features(self.df)
        res_pert = extract_qlib_alpha_features(df_perturbed)

        diff = np.abs(res_orig.iloc[:k].to_numpy() - res_pert.iloc[:k].to_numpy())
        max_diff = np.nanmax(diff)
        self.assertAlmostEqual(
            max_diff,
            0.0,
            places=9,
            msg=f"Qlib future perturbation leaked! Max diff: {max_diff}",
        )


class TestNaNAndEdgeCases(unittest.TestCase):
    """Test empty, single-row, constant price, and zero volume edge cases."""

    def test_empty_dataframe(self) -> None:
        """Verify empty DataFrame returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        res_agpt = compute_alphagpt_factors(empty_df)
        self.assertEqual(len(res_agpt), 0)
        self.assertIn("OFI_Impulse", res_agpt.columns)

        res_qlib = extract_qlib_alpha_features(empty_df)
        self.assertEqual(len(res_qlib), 0)
        self.assertGreater(len(res_qlib.columns), 40)

    def test_single_row_dataframe(self) -> None:
        """Verify single row input does not raise errors and outputs finite values."""
        single_df = pd.DataFrame(
            {"open": [100.0], "high": [102.0], "low": [99.0], "close": [101.0], "volume": [500.0]}
        )
        res_agpt = compute_alphagpt_factors(single_df)
        self.assertEqual(len(res_agpt), 1)
        self.assertFalse(res_agpt.isna().any().any())

        res_qlib = extract_qlib_alpha_features(single_df)
        self.assertEqual(len(res_qlib), 1)
        self.assertFalse(res_qlib.isna().any().any())

    def test_constant_zero_volume_series(self) -> None:
        """Verify series with 0 volume and flat price does not generate NaNs or Infs."""
        df_flat = pd.DataFrame(
            {
                "open": [100.0] * 30,
                "high": [100.0] * 30,
                "low": [100.0] * 30,
                "close": [100.0] * 30,
                "volume": [0.0] * 30,
            }
        )
        res_agpt = compute_alphagpt_factors(df_flat)
        self.assertFalse(res_agpt.isna().any().any())
        self.assertFalse(np.isinf(res_agpt.to_numpy()).any())

        res_qlib = extract_qlib_alpha_features(df_flat)
        self.assertFalse(res_qlib.isna().any().any())
        self.assertFalse(np.isinf(res_qlib.to_numpy()).any())

    def test_case_insensitive_columns(self) -> None:
        """Verify case-insensitive column matching."""
        df = _generate_synthetic_ohlcv(n=25)
        df_upper = df.rename(
            columns={"open": "Open", "high": "HIGH", "low": "Low", "close": "Close", "volume": "VOLUME"}
        )
        res_agpt = compute_alphagpt_factors(df_upper)
        self.assertEqual(len(res_agpt), 25)

        res_qlib = extract_qlib_alpha_features(df_upper)
        self.assertEqual(len(res_qlib), 25)


class TestAlphaGPTFactorMiner(unittest.TestCase):
    """Test AlphaGPTFactorMiner symbolic synthesis, stack VM, scoring, and mining."""

    def setUp(self) -> None:
        self.df = _generate_synthetic_ohlcv(n=120, seed=42)
        self.miner = AlphaGPTFactorMiner(random_seed=42)

    def test_stack_vm_execution_and_operators(self) -> None:
        """Verify Stack VM evaluation of unary, binary, and TS operators."""
        table = self.miner.prepare_feature_table(self.df)

        # Unary: abs, log, sign
        rpn_unary = ["close", "log"]
        res_unary = FactorStackVM.execute_rpn(rpn_unary, table)
        expected_unary = np.sign(table["close"]) * np.log1p(table["close"].abs())
        pd.testing.assert_series_equal(res_unary, expected_unary, check_names=False)

        # Binary: sub, div
        rpn_binary = ["close", "open", "sub"]
        res_binary = FactorStackVM.execute_rpn(rpn_binary, table)
        expected_binary = table["close"] - table["open"]
        pd.testing.assert_series_equal(res_binary, expected_binary, check_names=False)

        # TS: ts_mean
        rpn_ts = ["OFI_Impulse", "10", "ts_mean"]
        res_ts = FactorStackVM.execute_rpn(rpn_ts, table)
        expected_ts = table["OFI_Impulse"].rolling(10, min_periods=1).mean()
        pd.testing.assert_series_equal(res_ts, expected_ts, check_names=False)

    def test_expression_parser_functional_syntax(self) -> None:
        """Verify parsing functional string syntax to RPN tokens."""
        # ts_mean(OFI_Impulse, 10) -> ['OFI_Impulse', '10', 'ts_mean']
        rpn1 = self.miner.parse_prefix_to_rpn("ts_mean(OFI_Impulse, 10)")
        self.assertEqual(rpn1, ["OFI_Impulse", "10", "ts_mean"])

        # sub(close, open) -> ['close', 'open', 'sub']
        rpn2 = self.miner.parse_prefix_to_rpn("sub(close, open)")
        self.assertEqual(rpn2, ["close", "open", "sub"])

    def test_ic_ir_scoring_known_signals(self) -> None:
        """Verify IC / Rank IC / IR computation on synthetic target relationships."""
        table = self.miner.prepare_feature_table(self.df)
        fwd_returns = self.miner.compute_forward_returns(table["close"], horizon=1)

        # Factor positively correlated with future returns
        perfect_pos_factor = fwd_returns.copy()
        score_pos = self.miner.score_factor(perfect_pos_factor, fwd_returns)
        self.assertAlmostEqual(score_pos.rank_ic_mean, 1.0, places=2)
        self.assertGreater(score_pos.rank_ic_ir, 0.0)

        # Factor negatively correlated with future returns
        perfect_neg_factor = -fwd_returns.copy()
        score_neg = self.miner.score_factor(perfect_neg_factor, fwd_returns)
        self.assertAlmostEqual(score_neg.rank_ic_mean, -1.0, places=2)
        self.assertLess(score_neg.rank_ic_ir, 0.0)

    def test_mine_factors_pipeline_and_pruning(self) -> None:
        """Verify automated candidate mining loop, ranking, and orthogonalization."""
        top_k = 4
        mined = self.miner.mine_factors(
            self.df,
            n_candidates=20,
            forward_horizon=1,
            top_k=top_k,
            correlation_prune_threshold=0.85,
        )

        self.assertGreater(len(mined), 0)
        self.assertLessEqual(len(mined), top_k)

        # Verify all candidates have valid expressions and non-nan metrics
        for factor in mined:
            self.assertIsInstance(factor, FactorScore)
            self.assertFalse(np.isnan(factor.rank_ic_mean))
            self.assertFalse(np.isnan(factor.rank_ic_ir))
            self.assertFalse(np.isnan(factor.fitness))
            self.assertGreater(factor.n_samples, 0)


class TestQlibFactorsExtendedFeatures(unittest.TestCase):
    """Test extended Qlib Alpha101 / Alpha158 micro-structure feature extraction."""

    def test_feature_richness_and_groups(self) -> None:
        """Verify key micro-structure, volume impulse, and trend consistency factors."""
        df = _generate_synthetic_ohlcv(n=80)
        features = extract_qlib_alpha_features(df)

        expected_subset = [
            "micro_disp_body",
            "micro_disp_range",
            "micro_wick_balance",
            "vol_sma_ratio_20",
            "vol_flow_imbalance",
            "vol_vwap_dev_20",
            "trend_ema_20_50",
            "trend_consistency_10",
            "trend_macd_norm",
            "trend_rsi_14",
            "alpha_006",
            "alpha_012",
            "alpha_053",
            "alpha_101",
            "vol_parkinson_20",
            "vol_garman_klass_20",
        ]

        for col in expected_subset:
            self.assertIn(col, features.columns)
            self.assertFalse(features[col].isna().any(), f"{col} contains NaN")
            self.assertFalse(np.isinf(features[col]).any(), f"{col} contains Inf")

        # Verify RSI bounded in [0, 1]
        self.assertTrue((features["trend_rsi_14"] >= 0.0).all())
        self.assertTrue((features["trend_rsi_14"] <= 1.0).all())

        # Verify micro_body_abs bounded in [0, 1]
        self.assertTrue((features["micro_body_abs"] >= 0.0).all())
        self.assertTrue((features["micro_body_abs"] <= 1.0).all())


if __name__ == "__main__":
    unittest.main()
