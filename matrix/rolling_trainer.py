"""
Rolling Walk-Forward Machine Learning Trainer & Gating Module.
Implements the 5,000-bar rolling window:
- 2,500 bars In-Sample (IS) for model/feature calibration
- 2,500 bars Out-of-Sample (OOS) for generalization gate audit (G_score >= 0.60)
- Forward Out-of-Sample execution block of length `step` (288 bars for 3-day scheduled, or 96 for volatility events)
Only when G_score >= 0.60 does the strategy go live on the forward block.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Generator, Tuple, Dict, Any, List, Optional
from matrix.models import MatrixConfig, GeneralizationGateResult, TriggerType
from matrix.execution_engine import RealisticExecutionEngine


class RollingWalkForwardTrainer:
    def __init__(self, config: MatrixConfig = MatrixConfig()):
        self.config = config

    def generate_rolling_slices(
        self,
        df: pd.DataFrame
    ) -> Generator[Tuple[int, pd.DataFrame, pd.DataFrame, pd.DataFrame, TriggerType], None, None]:
        """
        Yields (slice_idx, is_df, oos_eval_df, forward_live_df, trigger_type):
        - is_df: past 2,500 bars [curr_idx : curr_idx + 2500]
        - oos_eval_df: validation 2,500 bars [curr_idx + 2500 : curr_idx + 5000]
        - forward_live_df: next forward execution block [curr_idx + 5000 : curr_idx + 5000 + step]
        """
        n = len(df)
        is_len = self.config.is_size      # 2500
        oos_len = self.config.oos_size    # 2500
        total_hist = is_len + oos_len     # 5000
        
        curr_idx = 0
        slice_idx = 0

        while curr_idx + total_hist < n:
            is_df = df.iloc[curr_idx : curr_idx + is_len]
            oos_eval_df = df.iloc[curr_idx + is_len : curr_idx + total_hist]

            # Check volatility trigger on the latest bars
            atr_ratio = oos_eval_df['atr_ratio'].iloc[-1] if 'atr_ratio' in oos_eval_df.columns else 1.0
            credal_u = oos_eval_df['credal_u'].iloc[-1] if 'credal_u' in oos_eval_df.columns else 0.30

            if atr_ratio > self.config.vol_trigger_threshold or credal_u > 0.38:
                trigger = TriggerType.VOLATILITY_EVENT
                step = max(self.config.scheduled_step_bars // 2, 96)
            else:
                trigger = TriggerType.SCHEDULED
                step = self.config.scheduled_step_bars

            # Live forward execution slice (non-overlapping live walk-forward)
            forward_end = min(curr_idx + total_hist + step, n)
            forward_live_df = df.iloc[curr_idx + total_hist : forward_end]

            if len(forward_live_df) == 0:
                break

            yield (slice_idx, is_df, oos_eval_df, forward_live_df, trigger)
            slice_idx += 1
            curr_idx += step

    def evaluate_slice_generalization(
        self,
        is_df: pd.DataFrame,
        oos_eval_df: pd.DataFrame,
        symbol: str,
        slice_idx: int,
    ) -> Tuple[GeneralizationGateResult, float]:
        """
        Audits model generalization on IS (2,500) vs OOS (2,500).
        Requires G_score >= 0.60 before going live on the forward block.
        G_score = 0.40 * Precision_OOS + 0.35 * WFE_Sharpe + 0.25 * PRCR_WinRate
        """
        engine_is = RealisticExecutionEngine(self.config)
        is_trades = engine_is.simulate_trades(is_df, symbol=symbol, slice_idx=slice_idx)

        engine_oos = RealisticExecutionEngine(self.config)
        oos_trades = engine_oos.simulate_trades(oos_eval_df, symbol=symbol, slice_idx=slice_idx)

        # In-sample metrics
        is_wins = [t for t in is_trades if t.pnl_net > 0]
        is_win_rate = len(is_wins) / max(len(is_trades), 1)
        is_returns = [t.return_pct for t in is_trades]
        is_sharpe = (np.mean(is_returns) / (np.std(is_returns) + 1e-9) * np.sqrt(365)) if len(is_returns) > 3 else 0.0

        # Out-of-sample metrics
        oos_wins = [t for t in oos_trades if t.pnl_net > 0]
        oos_win_rate = len(oos_wins) / max(len(oos_trades), 1)
        oos_returns = [t.return_pct for t in oos_trades]
        oos_sharpe = (np.mean(oos_returns) / (np.std(oos_returns) + 1e-9) * np.sqrt(365)) if len(oos_returns) > 3 else 0.0
        precision_oos = oos_win_rate

        # Walk Forward Efficiency (WFE)
        wfe = min(1.0, max(0.0, oos_sharpe / max(abs(is_sharpe), 0.05)))
        win_rate_retention = min(1.0, oos_win_rate / max(is_win_rate, 0.05))

        g_score = (0.40 * precision_oos) + (0.35 * wfe) + (0.25 * win_rate_retention)
        passed = bool(g_score >= self.config.min_generalization_score and len(oos_trades) >= 3)
        rejection_reason = None if passed else f"G_score {g_score:.3f} < {self.config.min_generalization_score} or trades < 3"

        result = GeneralizationGateResult(
            passed=passed,
            g_score=g_score,
            is_sharpe=is_sharpe,
            oos_sharpe=oos_sharpe,
            wfe=wfe,
            is_win_rate=is_win_rate,
            oos_win_rate=oos_win_rate,
            precision_oos=precision_oos,
            rejection_reason=rejection_reason,
        )

        risk_multiplier = 1.0
        if passed:
            if g_score >= 0.75:
                risk_multiplier = 1.20
            elif g_score >= 0.65:
                risk_multiplier = 1.0
            else:
                risk_multiplier = 0.80

        return result, risk_multiplier
