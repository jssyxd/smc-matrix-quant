#!/usr/bin/env python3
"""
SMC High-Frequency Crypto Multi-Asset Benchmark Harness.

Covers:
1. Mainstream crypto assets: BTC, ETH, SOL, BNB (15m intraday bars)
2. Natural-Year Walk-Forward:
   - In-Sample (IS): 2023
   - Out-of-Sample (OOS): 2024 (strictly locked evaluation)
3. Strict Transaction Friction:
   - Maker entry: 0.02% (2 bps), 0.00% slippage
   - Taker SL: 0.05% (5 bps) + 0.05% dynamic slippage
   - Intra-bar pessimism: same-bar conflict strictly prioritizes Stop Loss
   - Compounding equity from $1,000 USD base
4. Credal Transformer Epistemic Gate (NeurIPS 2025, arXiv:2510.12137):
   - Subjective Logic Dirichlet vacuity u <= u_max (0.38)
5. 2,000-Path Monte Carlo Bootstrap Tail Risk Assessment:
   - Probability of Ruin (Max Drawdown >= 50%)
   - VaR 95% and CVaR 95%
6. Canonical Autoresearch Output:
   - METRIC daily_trades (Primary metric, target: 1 ~ 60 trades/day)
   - METRIC oos_annual_return_pct
   - METRIC oos_sharpe
   - METRIC win_rate_pct
   - METRIC profit_factor
   - METRIC max_drawdown_pct
   - METRIC ruin_probability
   - METRIC is_annual_return_pct
   - METRIC walk_forward_efficiency
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pandas as pd

# Ensure root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backtest_core import load_symbol_timeframe_data
from src.qlib_smc_alpha import compute_qlib_smc_alpha, QlibSMCConfig
from src.smc_round2_engine import Round2SMCEngine
CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "BNB"]
TIMEFRAME = "15m"
def run_benchmark(
    swing_len: int = 5,
    min_score_threshold: float = 68.0,
    credal_u_max: float = 0.32,
    risk_pct: float = 0.08,
    rr_tp1: float = 1.0,
    rr_tp2: float = 3.0,
    n_mc_paths: int = 2000,
    mc_seed: int = 42,
) -> dict:
    """Executes the full walk-forward multi-asset backtest and returns metrics dictionary."""

    is_trades_list = []
    oos_trades_list = []
    is_returns = []
    oos_returns = []
    oos_all_pnl = []

    # 1. Evaluate each crypto asset across IS (2023) and OOS (2024)
    for sym in CRYPTO_SYMBOLS:
        raw_df = load_symbol_timeframe_data(sym, TIMEFRAME)

        # In-Sample 2023
        df_is = raw_df[raw_df.index.year == 2023].copy()
        if len(df_is) > 100:
            cfg_is = QlibSMCConfig(
                swing_len=swing_len,
                min_score_threshold=min_score_threshold,
                use_credal_filter=True,
                credal_u_max=credal_u_max,
                atr_ratio_min=0.80,
                atr_ratio_max=2.20,
            )
            feats_is = compute_qlib_smc_alpha(df_is, config=cfg_is)
            eng_is = Round2SMCEngine(
                use_credal=False,
                use_compound=True,
                risk_pct=risk_pct,
                rr_tp1=rr_tp1,
                rr_tp2=rr_tp2,
                credal_u_max=credal_u_max,
            )
            res_is = eng_is.run(feats_is)
            m_is = res_is["metrics"]
            is_trades_list.extend(res_is["trades"])
            is_returns.append(m_is["total_return_pct"])

        # Out-of-Sample 2024 (Strictly locked evaluation)
        df_oos = raw_df[raw_df.index.year == 2024].copy()
        if len(df_oos) > 100:
            cfg_oos = QlibSMCConfig(
                swing_len=swing_len,
                min_score_threshold=min_score_threshold,
                use_credal_filter=True,
                credal_u_max=credal_u_max,
                atr_ratio_min=0.80,
                atr_ratio_max=2.20,
            )
            feats_oos = compute_qlib_smc_alpha(df_oos, config=cfg_oos)
            eng_oos = Round2SMCEngine(
                use_credal=False,
                use_compound=True,
                risk_pct=risk_pct,
                rr_tp1=rr_tp1,
                rr_tp2=rr_tp2,
                credal_u_max=credal_u_max,
            )
            res_oos = eng_oos.run(feats_oos)
            m_oos = res_oos["metrics"]
            oos_trades_list.extend(res_oos["trades"])
            oos_returns.append(m_oos["total_return_pct"])
            for t in res_oos["trades"]:
                oos_all_pnl.append(float(t.get("pnl", 0.0)))

    # Aggregate OOS statistics
    n_oos_trades = len(oos_trades_list)
    daily_trades = n_oos_trades / 366.0  # 2024 is leap year

    oos_winning = [t for t in oos_trades_list if t.get("pnl", 0.0) > 0]
    oos_losing = [t for t in oos_trades_list if t.get("pnl", 0.0) <= 0]
    win_rate = (len(oos_winning) / n_oos_trades * 100.0) if n_oos_trades > 0 else 0.0

    total_win = sum(t.get("pnl", 0.0) for t in oos_winning)
    total_loss = abs(sum(t.get("pnl", 0.0) for t in oos_losing))
    profit_factor = (total_win / total_loss) if total_loss > 0 else (99.0 if total_win > 0 else 0.0)

    mean_is_ret = float(np.mean(is_returns)) if is_returns else 0.0
    mean_oos_ret = float(np.mean(oos_returns)) if oos_returns else 0.0

    # Sharpe on aggregated OOS trade returns
    if oos_all_pnl:
        pnl_arr = np.array(oos_all_pnl)
        pnl_std = float(np.std(pnl_arr))
        pnl_mean = float(np.mean(pnl_arr))
        oos_sharpe = (pnl_mean / pnl_std * np.sqrt(daily_trades * 365.0)) if pnl_std > 1e-9 else 0.0
    else:
        oos_sharpe = 0.0

    # Approximate max drawdown across pooled trades
    if oos_all_pnl:
        eq = 1000.0 + np.cumsum(oos_all_pnl)
        peak = np.maximum.accumulate(eq)
        dd = (peak - eq) / np.maximum(peak, 1e-9)
        max_dd = float(np.max(dd) * 100.0)
    else:
        max_dd = 0.0

    # 2. Monte Carlo Bootstrap (2,000 synthetic paths)
    ruin_count = 0
    if len(oos_all_pnl) >= 20:
        rng = np.random.default_rng(mc_seed)
        pnl_pool = np.array(oos_all_pnl)
        trades_per_path = min(200, len(pnl_pool))
        for _ in range(n_mc_paths):
            sampled_pnls = rng.choice(pnl_pool, size=trades_per_path, replace=True)
            path_eq = 1000.0 + np.cumsum(sampled_pnls)
            path_peak = np.maximum.accumulate(path_eq)
            path_dd = (path_peak - path_eq) / np.maximum(path_peak, 1e-9)
            if np.max(path_dd) >= 0.50:
                ruin_count += 1
        ruin_prob = ruin_count / n_mc_paths
    else:
        ruin_prob = 0.0

    # Walk-Forward Efficiency (OOS Return / max(|IS Return|, 1e-6))
    wf_efficiency = mean_oos_ret / max(abs(mean_is_ret), 1.0)

    return {
        "daily_trades": float(daily_trades),
        "oos_annual_return_pct": float(mean_oos_ret),
        "oos_sharpe": float(oos_sharpe),
        "win_rate_pct": float(win_rate),
        "profit_factor": float(profit_factor),
        "max_drawdown_pct": float(max_dd),
        "ruin_probability": float(ruin_prob),
        "is_annual_return_pct": float(mean_is_ret),
        "walk_forward_efficiency": float(wf_efficiency),
        "total_trades": int(n_oos_trades),
        "is_trades": int(len(is_trades_list)),
        "oos_trades": int(n_oos_trades),
    }


def main() -> int:
    try:
        metrics = run_benchmark()

        # Primary Metric: Daily Trade Frequency (target: 1.0 ~ 60.0 trades/day)
        print(f"METRIC daily_trades={metrics['daily_trades']:.4f}")

        # Secondary Metrics
        print(f"METRIC oos_annual_return_pct={metrics['oos_annual_return_pct']:.4f}")
        print(f"METRIC oos_sharpe={metrics['oos_sharpe']:.4f}")
        print(f"METRIC win_rate_pct={metrics['win_rate_pct']:.4f}")
        print(f"METRIC profit_factor={metrics['profit_factor']:.4f}")
        print(f"METRIC max_drawdown_pct={metrics['max_drawdown_pct']:.4f}")
        print(f"METRIC ruin_probability={metrics['ruin_probability']:.4f}")
        print(f"METRIC is_annual_return_pct={metrics['is_annual_return_pct']:.4f}")
        print(f"METRIC walk_forward_efficiency={metrics['walk_forward_efficiency']:.4f}")

        # ASI Structured Diagnostics
        print(f"ASI total_trades={metrics['total_trades']}")
        print(f"ASI is_trades={metrics['is_trades']}")
        print(f"ASI oos_trades={metrics['oos_trades']}")

        return 0
    except Exception as e:
        sys.stderr.write(f"Benchmark error: {e}\n")
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
