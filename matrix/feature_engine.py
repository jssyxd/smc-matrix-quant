"""
Feature engineering engine for the SMC Matrix.
Computes causal micro-structure indicators, Qlib-inspired orderflow features,
Garman-Klass volatility, and Dirichlet Credal Uncertainty adhering strictly to smc_live_trader.py.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, Tuple


def compute_wilder_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    n = len(close)
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
    
    atr = np.zeros(n)
    if n < period:
        return tr
    atr[period - 1] = np.mean(tr[:period])
    alpha = 1.0 / period
    for i in range(period, n):
        atr[i] = (1.0 - alpha) * atr[i - 1] + alpha * tr[i]
    return atr


def compute_garman_klass_volatility(high: np.ndarray, low: np.ndarray, open_p: np.ndarray, close: np.ndarray, window: int = 20) -> np.ndarray:
    n = len(close)
    log_hl = np.log(np.maximum(high, 1e-9) / np.maximum(low, 1e-9))
    log_co = np.log(np.maximum(close, 1e-9) / np.maximum(open_p, 1e-9))
    rs = 0.5 * (log_hl ** 2) - (2.0 * np.log(2.0) - 1.0) * (log_co ** 2)
    
    gk_vol = pd.Series(rs).rolling(window=window, min_periods=5).mean().values
    return np.sqrt(np.maximum(gk_vol, 0.0))


def compute_causal_swings(high: np.ndarray, low: np.ndarray, swing_len: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """Causal swing high and low detection strictly evaluated at t - swing_len."""
    n = len(high)
    hh = np.full(n, high[0])
    ll = np.full(n, low[0])
    
    curr_hh = high[0]
    curr_ll = low[0]
    
    for t in range(2 * swing_len, n):
        p = t - swing_len
        if high[p] == np.max(high[p - swing_len : t + 1]):
            curr_hh = high[p]
        if low[p] == np.min(low[p - swing_len : t + 1]):
            curr_ll = low[p]
        hh[t] = curr_hh
        ll[t] = curr_ll
        
    return hh, ll


def compute_dirichlet_credal_metrics(
    score_long: np.ndarray,
    score_short: np.ndarray,
    u_max: float = 0.35,
    c_max: float = 0.40,
    base_neutral: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Implements Dirichlet Evidential Gate strictly identical to smc_live_trader.py:
    alpha_bull = max(bull_ev, 0.0) + 1.0
    alpha_bear = max(bear_ev, 0.0) + 1.0
    alpha_neutral = base_neutral + 1.0
    S = alpha_bull + alpha_bear + alpha_neutral
    b_bull = (alpha_bull - 1.0) / S
    b_bear = (alpha_bear - 1.0) / S
    u = K / S (K=3.0)
    C = (2.0 * min(b_bull, b_bear) / (b_bull + b_bear)) if (b_bull + b_bear) > 1e-6 else 0.0
    passed = (u <= u_max) and (C <= c_max + 1e-5)
    """
    bull_ev = np.maximum(score_long / 10.0, 0.0)
    bear_ev = np.maximum(score_short / 10.0, 0.0)
    
    alpha_bull = bull_ev + 1.0
    alpha_bear = bear_ev + 1.0
    alpha_neutral = base_neutral + 1.0
    
    S = alpha_bull + alpha_bear + alpha_neutral
    b_bull = bull_ev / S
    b_bear = bear_ev / S
    u = 3.0 / S
    
    tot_dir = b_bull + b_bear
    c_conflict = np.where(tot_dir > 1e-6, 2.0 * np.minimum(b_bull, b_bear) / np.maximum(tot_dir, 1e-9), 0.0)
    passed = (u <= u_max) & (c_conflict <= (c_max + 1e-5))
    return b_bull, b_bear, u, c_conflict, passed


def extract_features(df: pd.DataFrame, swing_len: int = 5) -> pd.DataFrame:
    """Computes causal features and composite scores matching smc_live_trader.py."""
    res = df.copy()
    high = res['high'].values.astype(float)
    low = res['low'].values.astype(float)
    close = res['close'].values.astype(float)
    open_p = res['open'].values.astype(float)
    volume = res['volume'].values.astype(float) if 'volume' in res.columns else np.ones(len(close))
    n = len(close)

    # 1. Swings (zero-lookahead)
    hh, ll = compute_causal_swings(high, low, swing_len)
    res['swing_high'] = hh
    res['swing_low'] = ll
    
    # 2. Volatilities
    atr14 = compute_wilder_atr(high, low, close, 14)
    atr100 = compute_wilder_atr(high, low, close, 100)
    res['atr14'] = atr14
    res['atr100'] = atr100
    res['atr_ratio'] = atr14 / np.maximum(atr100, 1e-9)
    res['gk_vol'] = compute_garman_klass_volatility(high, low, open_p, close, window=20)
    
    # 3. Orderflow and Microstructure Proxies
    hl_range = np.maximum(high - low, 1e-9)
    res['clv'] = ((close - low) - (high - close)) / hl_range  # CLV in [-1, 1]
    
    vol_sma20 = pd.Series(volume).rolling(window=20, min_periods=1).mean().values
    res['vol_spike'] = (volume / np.maximum(vol_sma20, 1e-9)) > 1.25
    
    # 4. EMAs
    res['ema20'] = pd.Series(close).ewm(span=20, adjust=False).mean().values
    res['ema50'] = pd.Series(close).ewm(span=50, adjust=False).mean().values
    
    # 5. Composite Scoring exactly per smc_live_trader.py
    is_bull_candle = close > open_p
    score_long = np.zeros(n)
    score_short = np.zeros(n)

    # Trend (30 pts)
    score_long += np.where((close > res['ema20']) & (res['ema20'] > res['ema50']), 30.0, 0.0)
    score_short += np.where((close < res['ema20']) & (res['ema20'] < res['ema50']), 30.0, 0.0)

    # Volume spike (25 pts)
    score_long += np.where(res['vol_spike'] & is_bull_candle, 25.0, 0.0)
    score_short += np.where(res['vol_spike'] & (~is_bull_candle), 25.0, 0.0)

    # CLV pressure (15 pts)
    score_long += np.where(res['clv'] > 0.40, 15.0, 0.0)
    score_short += np.where(res['clv'] < -0.40, 15.0, 0.0)

    # Volatility health channel (15 pts)
    in_atr_channel = (res['atr_ratio'] >= 0.55) & (res['atr_ratio'] <= 1.80)
    score_long += np.where(in_atr_channel, 15.0, 0.0)
    score_short += np.where(in_atr_channel, 15.0, 0.0)

    # Pullback to EMA20 (15 pts)
    pullback_long = is_bull_candle & (np.abs(low - res['ema20']) / np.maximum(atr14, 1e-9) < 0.8)
    pullback_short = (~is_bull_candle) & (np.abs(high - res['ema20']) / np.maximum(atr14, 1e-9) < 0.8)
    score_long += np.where(pullback_long, 15.0, 0.0)
    score_short += np.where(pullback_short, 15.0, 0.0)

    res['score_long'] = np.clip(score_long, 0.0, 100.0)
    res['score_short'] = np.clip(score_short, 0.0, 100.0)

    # 6. Credal Evidential Filtering
    b_bull, b_bear, u, c_conf, passed = compute_dirichlet_credal_metrics(res['score_long'].values, res['score_short'].values)
    res['b_bull'] = b_bull
    res['b_bear'] = b_bear
    res['credal_u'] = u
    res['credal_conflict'] = c_conf
    res['credal_passed'] = passed

    # 7. Signal Generation (score >= 60.0 & credal_passed)
    signal = np.zeros(n, dtype=int)
    sig_long = (res['score_long'] >= 60.0) & (res['score_long'] > res['score_short']) & passed
    sig_short = (res['score_short'] >= 60.0) & (res['score_short'] > res['score_long']) & passed

    signal[sig_long] = 1
    signal[sig_short] = -1
    res['signal'] = signal

    return res
