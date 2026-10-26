"""
Extended Qlib Alpha101 / Alpha158 Micro-Structure Factor Extraction.

Implements high-dimensional micro-structure features inspired by Microsoft Qlib
(Alpha101 / Alpha158) with strict mathematical causality (zero lookahead):
1. Volume Impulses:
   - Volume SMA ratios (5, 10, 20, 60), volume surge z-scores, force index,
     order flow imbalance pressure, VWAP price deviations, and rolling volume-return correlations.
2. Trend Consistency:
   - Multi-scale EMA spreads (10/30, 20/50, 50/200), directional consistency fractions,
     Kaufman Efficiency Ratios, normalized MACD / MACD histograms, normalized RSI, and momentum ROCs.
3. Micro Price Displacements:
   - Candle body/wick displacements, relative range, upper/lower shadow ratios,
     close location value, Parkinson and Garman-Klass micro-volatility, and normalized true range.
4. Classical Qlib / WorldQuant 101 Microstructure Alphas:
   - Alpha006, Alpha012, Alpha053, Alpha054, Alpha101, Qlib K-Line descriptors (KLOW, KHIGH, KSFT).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd


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


def compute_true_range(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
) -> pd.Series:
    """Compute causal True Range series."""
    prev_close = close.shift(1).fillna(close)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr


def compute_wilder_rma(series: pd.Series, period: int) -> pd.Series:
    """Compute Wilder's Running Moving Average (causal EWM with alpha=1/period)."""
    if len(series) == 0:
        return series
    return series.ewm(alpha=1.0 / float(period), adjust=False).mean()


def extract_qlib_alpha_features(
    df: pd.DataFrame,
    fill_na: bool = True,
) -> pd.DataFrame:
    """
    Extract high-dimensional Qlib Alpha101 / Alpha158 micro-structure factors.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV market DataFrame containing 'open', 'high', 'low', 'close', 'volume'.
    fill_na : bool, default True
        If True, causally replaces initial warmup NaNs and infinite values with 0.0.

    Returns
    -------
    pd.DataFrame
        DataFrame of high-dimensional micro-structure features with index aligned to df.
    """
    if len(df) == 0:
        empty_cols = [
            "micro_disp_body", "micro_disp_range", "micro_upper_wick", "micro_lower_wick",
            "micro_wick_balance", "micro_close_loc", "micro_body_abs", "micro_ret_1",
            "micro_ret_3", "micro_ret_5", "micro_ret_10", "micro_true_range_pct",
            "micro_zscore_20", "vol_sma_ratio_5", "vol_sma_ratio_10", "vol_sma_ratio_20",
            "vol_sma_ratio_60", "vol_std_ratio_20", "vol_zscore_20", "vol_force",
            "vol_flow_imbalance", "vol_vwap_dev_20", "vol_price_corr_10", "vol_price_corr_20",
            "trend_ema_10_30", "trend_ema_20_50", "trend_ema_50_200", "trend_consistency_5",
            "trend_consistency_10", "trend_consistency_20", "trend_efficiency_10",
            "trend_efficiency_20", "trend_macd_norm", "trend_macd_hist_norm", "trend_rsi_14",
            "trend_roc_5", "trend_roc_10", "trend_roc_20", "alpha_006", "alpha_012",
            "alpha_053", "alpha_054", "alpha_101", "qlib_klow", "qlib_khigh", "qlib_kclose",
            "qlib_kopen", "qlib_ksft", "vol_parkinson_20", "vol_garman_klass_20",
        ]
        return pd.DataFrame(columns=empty_cols, index=df.index, dtype=float)

    open_, high, low, close, volume, index = _extract_ohlcv(df)
    eps = 1e-9

    features: Dict[str, pd.Series] = {}

    # Basic spans
    hl_range = high - low
    safe_hl = hl_range.replace(0.0, eps)
    safe_close = close.replace(0.0, eps)
    safe_open = open_.replace(0.0, eps)

    # -------------------------------------------------------------------------
    # 1. Micro Price Displacements
    # -------------------------------------------------------------------------
    # Directional body dominance in [-1, 1]
    features["micro_disp_body"] = (close - open_) / safe_hl

    # Candle range normalized by price
    features["micro_disp_range"] = hl_range / safe_close

    # Upper and lower wicks
    max_oc = np.maximum(open_, close)
    min_oc = np.minimum(open_, close)
    features["micro_upper_wick"] = (high - max_oc) / safe_hl
    features["micro_lower_wick"] = (min_oc - low) / safe_hl
    features["micro_wick_balance"] = features["micro_upper_wick"] - features["micro_lower_wick"]

    # Close location value in [0, 1]
    features["micro_close_loc"] = (close - low) / safe_hl

    # Absolute body fraction in [0, 1]
    features["micro_body_abs"] = (close - open_).abs() / safe_hl

    # Multi-period causal returns
    features["micro_ret_1"] = (close - close.shift(1)) / safe_close.shift(1).fillna(safe_close)
    features["micro_ret_3"] = (close - close.shift(3)) / safe_close.shift(3).fillna(safe_close)
    features["micro_ret_5"] = (close - close.shift(5)) / safe_close.shift(5).fillna(safe_close)
    features["micro_ret_10"] = (close - close.shift(10)) / safe_close.shift(10).fillna(safe_close)

    # True range normalized
    tr = compute_true_range(high, low, close)
    features["micro_true_range_pct"] = tr / safe_close

    # Rolling Z-score of close (20 bars)
    sma_close_20 = close.rolling(20, min_periods=1).mean()
    std_close_20 = close.rolling(20, min_periods=1).std().fillna(0.0).replace(0.0, eps)
    features["micro_zscore_20"] = (close - sma_close_20) / std_close_20

    # -------------------------------------------------------------------------
    # 2. Volume Impulses & Flow
    # -------------------------------------------------------------------------
    vol_sma_5 = volume.rolling(5, min_periods=1).mean().replace(0.0, eps)
    vol_sma_10 = volume.rolling(10, min_periods=1).mean().replace(0.0, eps)
    vol_sma_20 = volume.rolling(20, min_periods=1).mean().replace(0.0, eps)
    vol_sma_60 = volume.rolling(60, min_periods=1).mean().replace(0.0, eps)
    vol_std_20 = volume.rolling(20, min_periods=1).std().fillna(0.0)

    features["vol_sma_ratio_5"] = volume / vol_sma_5
    features["vol_sma_ratio_10"] = volume / vol_sma_10
    features["vol_sma_ratio_20"] = volume / vol_sma_20
    features["vol_sma_ratio_60"] = volume / vol_sma_60
    features["vol_std_ratio_20"] = vol_std_20 / vol_sma_20
    features["vol_zscore_20"] = (volume - vol_sma_20) / vol_std_20.replace(0.0, eps)

    # Force index / volume pressure
    features["vol_force"] = features["micro_disp_body"] * features["vol_sma_ratio_20"]

    # Order flow imbalance proxy
    features["vol_flow_imbalance"] = (
        (2.0 * close - high - low) / safe_hl
    ) * features["vol_sma_ratio_20"]

    # Rolling 20-bar VWAP price deviation
    typical_price = (high + low + close) / 3.0
    cum_pv_20 = (typical_price * volume).rolling(20, min_periods=1).sum()
    cum_v_20 = volume.rolling(20, min_periods=1).sum().replace(0.0, eps)
    vwap_20 = cum_pv_20 / cum_v_20
    features["vol_vwap_dev_20"] = (close - vwap_20) / vwap_20.replace(0.0, eps)

    # Rolling price-volume correlation
    ret_1 = features["micro_ret_1"]
    vol_chg_1 = (volume - volume.shift(1)) / volume.shift(1).replace(0.0, eps).fillna(1.0)
    features["vol_price_corr_10"] = ret_1.rolling(10, min_periods=2).corr(vol_chg_1).fillna(0.0)
    features["vol_price_corr_20"] = ret_1.rolling(20, min_periods=2).corr(vol_chg_1).fillna(0.0)

    # -------------------------------------------------------------------------
    # 3. Trend Consistency & Directional Strength
    # -------------------------------------------------------------------------
    ema_10 = close.ewm(span=10, adjust=False).mean()
    ema_20 = close.ewm(span=20, adjust=False).mean()
    ema_30 = close.ewm(span=30, adjust=False).mean()
    ema_50 = close.ewm(span=50, adjust=False).mean()
    ema_200 = close.ewm(span=200, adjust=False).mean()

    features["trend_ema_10_30"] = (ema_10 - ema_30) / safe_close
    features["trend_ema_20_50"] = (ema_20 - ema_50) / safe_close
    features["trend_ema_50_200"] = (ema_50 - ema_200) / safe_close

    # Directional consistency: fraction of positive return bars
    pos_ret = (ret_1 > 0.0).astype(float)
    features["trend_consistency_5"] = pos_ret.rolling(5, min_periods=1).mean()
    features["trend_consistency_10"] = pos_ret.rolling(10, min_periods=1).mean()
    features["trend_consistency_20"] = pos_ret.rolling(20, min_periods=1).mean()

    # Kaufman Efficiency Ratio = net displacement / total path
    abs_ret_1 = (close - close.shift(1)).abs()
    path_10 = abs_ret_1.rolling(10, min_periods=1).sum().replace(0.0, eps)
    path_20 = abs_ret_1.rolling(20, min_periods=1).sum().replace(0.0, eps)
    features["trend_efficiency_10"] = (close - close.shift(10)).abs().fillna(0.0) / path_10
    features["trend_efficiency_20"] = (close - close.shift(20)).abs().fillna(0.0) / path_20

    # Normalized MACD and MACD Histogram over ATR(14)
    atr_14 = compute_wilder_rma(tr, 14).replace(0.0, eps)
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    macd_raw = ema_12 - ema_26
    macd_signal = macd_raw.ewm(span=9, adjust=False).mean()
    features["trend_macd_norm"] = macd_raw / atr_14
    features["trend_macd_hist_norm"] = (macd_raw - macd_signal) / atr_14

    # Wilder RSI(14) normalized to [0, 1]
    delta_c = close - close.shift(1).fillna(close)
    gain = delta_c.clip(lower=0.0)
    loss = (-delta_c).clip(lower=0.0)
    avg_gain = compute_wilder_rma(gain, 14)
    avg_loss = compute_wilder_rma(loss, 14)
    rs = avg_gain / avg_loss.replace(0.0, eps)
    rsi_14 = 100.0 - (100.0 / (1.0 + rs))
    features["trend_rsi_14"] = (rsi_14 / 100.0).clip(0.0, 1.0)

    # Momentum Rate-of-Change (ROC)
    features["trend_roc_5"] = (close - close.shift(5)) / safe_close.shift(5).fillna(safe_close)
    features["trend_roc_10"] = (close - close.shift(10)) / safe_close.shift(10).fillna(safe_close)
    features["trend_roc_20"] = (close - close.shift(20)) / safe_close.shift(20).fillna(safe_close)

    # -------------------------------------------------------------------------
    # 4. Classic Qlib / WorldQuant 101 Microstructure Alphas
    # -------------------------------------------------------------------------
    # Alpha006: -1 * correlation(open, volume, 10)
    features["alpha_006"] = (
        -1.0 * open_.rolling(10, min_periods=2).corr(volume).fillna(0.0)
    )

    # Alpha012: sign(delta(volume, 1)) * (-1 * delta(close, 1))
    d_vol_1 = np.sign(volume - volume.shift(1).fillna(volume))
    d_close_1 = -1.0 * (close - close.shift(1).fillna(close)) / safe_close
    features["alpha_012"] = d_vol_1 * d_close_1

    # Alpha053: -1 * delta(((close - low) - (high - close)) / (high - low + eps), 9)
    spread_press = (2.0 * close - high - low) / safe_hl
    features["alpha_053"] = -1.0 * (spread_press - spread_press.shift(9).fillna(spread_press))

    # Alpha054: -1 * (low - close) * (open^5) / ((low - high) * (close^5) + eps)
    o_pow5 = (open_ / safe_close).pow(5).clip(-1e6, 1e6)
    denom_54 = (low - high).replace(0.0, -eps)
    features["alpha_054"] = -1.0 * (low - close) * o_pow5 / denom_54

    # Alpha101: (close - open) / (high - low + 0.001)
    features["alpha_101"] = (close - open_) / (hl_range + 0.001)

    # Qlib K-Line Descriptors
    features["qlib_klow"] = (low - low.shift(1)) / low.shift(1).replace(0.0, eps).fillna(safe_close)
    features["qlib_khigh"] = (high - high.shift(1)) / high.shift(1).replace(0.0, eps).fillna(safe_close)
    features["qlib_kclose"] = features["micro_ret_1"]
    features["qlib_kopen"] = (open_ - open_.shift(1)) / open_.shift(1).replace(0.0, eps).fillna(safe_open)
    features["qlib_ksft"] = spread_press

    # Parkinson Volatility (rolling 20 bars)
    log_hl = np.log(high / low.replace(0.0, eps)).replace([np.inf, -np.inf], 0.0)
    parkinson_inst = (log_hl.pow(2) / (4.0 * np.log(2.0))).clip(lower=0.0)
    features["vol_parkinson_20"] = np.sqrt(
        parkinson_inst.rolling(20, min_periods=1).mean().clip(lower=0.0)
    )

    # Garman-Klass Volatility (rolling 20 bars)
    log_co = np.log(close / open_.replace(0.0, eps)).replace([np.inf, -np.inf], 0.0)
    gk_inst = (
        0.5 * log_hl.pow(2) - (2.0 * np.log(2.0) - 1.0) * log_co.pow(2)
    ).clip(lower=0.0)
    features["vol_garman_klass_20"] = np.sqrt(
        gk_inst.rolling(20, min_periods=1).mean().clip(lower=0.0)
    )

    # Assemble result DataFrame
    res = pd.DataFrame(features, index=index)

    if fill_na:
        res = res.replace([np.inf, -np.inf], np.nan)
        res = res.ffill().fillna(0.0)
    return res


__all__ = [
    "extract_qlib_alpha_features",
    "compute_true_range",
    "compute_wilder_rma",
]
