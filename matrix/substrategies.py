"""
Implementation of the Three Sub-strategies for the SMC Matrix:
1. Substrategy 1: Single-coin isolated dynamic walk-forward training & forward execution.
2. Substrategy 2: Exogenous BTC regime driver (BTC trains and gates, Altcoins BNB/SOL/ETH trade).
3. Substrategy 3: CMC20 synthetic index basket with concurrent synchronous fills.
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from matrix.models import MatrixConfig, TradeRecord, SubstrategyType, BacktestSummaryReport
from matrix.feature_engine import extract_features
from matrix.execution_engine import RealisticExecutionEngine
from matrix.rolling_trainer import RollingWalkForwardTrainer


def calculate_summary_metrics(
    trades: List[TradeRecord],
    initial_capital: float,
    final_capital: float,
    substrategy: str,
    train_tf: str,
    trade_tf: str,
    start_date: str,
    end_date: str,
    gen_pass_rate: float,
) -> BacktestSummaryReport:
    """Calculates standardized benchmark metrics including CAGR, Sharpe, Sortino, Calmar, Win Rate, and Profit Factor."""
    total_trades = len(trades)
    if total_trades == 0:
        return BacktestSummaryReport(
            substrategy=substrategy,
            train_tf=train_tf,
            trade_tf=trade_tf,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_net_pnl=0.0,
            total_return_pct=0.0,
            cagr=0.0,
            max_drawdown_pct=0.0,
            sharpe_ratio=0.0,
            sortino_ratio=0.0,
            calmar_ratio=0.0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate_pct=0.0,
            profit_factor=0.0,
            avg_win=0.0,
            avg_loss=0.0,
            generalization_pass_rate=gen_pass_rate,
        )

    winning_trades = [t for t in trades if t.pnl_net > 0]
    losing_trades = [t for t in trades if t.pnl_net <= 0]
    n_wins = len(winning_trades)
    n_losses = len(losing_trades)
    win_rate = (n_wins / total_trades) * 100.0

    gross_profit = sum(t.pnl_net for t in winning_trades)
    gross_loss = abs(sum(t.pnl_net for t in losing_trades))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 1e-6 else 99.0
    avg_win = (gross_profit / n_wins) if n_wins > 0 else 0.0
    avg_loss = (gross_loss / n_losses) if n_losses > 0 else 0.0

    total_net_pnl = final_capital - initial_capital
    total_return_pct = (total_net_pnl / initial_capital) * 100.0

    # Compounding equity curve
    equity_curve = [initial_capital]
    for t in trades:
        equity_curve.append(t.balance_after)
    eq_series = pd.Series(equity_curve)
    peak = eq_series.cummax()
    dd = (eq_series - peak) / peak
    max_dd_pct = abs(float(dd.min())) * 100.0

    # Returns statistics
    returns = np.array([t.return_pct / 100.0 for t in trades])
    mean_ret = np.mean(returns)
    std_ret = np.std(returns) + 1e-9
    neg_returns = returns[returns < 0]
    std_downside = np.std(neg_returns) + 1e-9 if len(neg_returns) > 1 else std_ret

    annual_factor = np.sqrt(max(total_trades / 2.0, 50.0))
    sharpe = float((mean_ret / std_ret) * annual_factor)
    sortino = float((mean_ret / std_downside) * annual_factor)

    years = 2.0
    cagr = float(((final_capital / max(initial_capital, 1e-3)) ** (1.0 / years) - 1.0) * 100.0)
    calmar = (cagr / max_dd_pct) if max_dd_pct > 0.01 else 0.0

    return BacktestSummaryReport(
        substrategy=substrategy,
        train_tf=train_tf,
        trade_tf=trade_tf,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        final_capital=final_capital,
        total_net_pnl=total_net_pnl,
        total_return_pct=total_return_pct,
        cagr=cagr,
        max_drawdown_pct=max_dd_pct,
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        calmar_ratio=calmar,
        total_trades=total_trades,
        winning_trades=n_wins,
        losing_trades=n_losses,
        win_rate_pct=win_rate,
        profit_factor=profit_factor,
        avg_win=avg_win,
        avg_loss=avg_loss,
        generalization_pass_rate=gen_pass_rate,
    )


class SubstrategyRunner:
    def __init__(self, config: MatrixConfig = MatrixConfig()):
        self.config = config
        self.trainer = RollingWalkForwardTrainer(config)

    def run_single_coin(self, df: pd.DataFrame, symbol: str) -> Tuple[List[TradeRecord], BacktestSummaryReport]:
        """Sub-strategy 1: Single coin isolated dynamic rolling train and forward backtest."""
        df_feat = extract_features(df)
        engine = RealisticExecutionEngine(self.config)
        all_trades: List[TradeRecord] = []
        gen_passes = 0
        total_slices = 0

        for slice_idx, is_df, oos_eval_df, forward_live_df, trigger in self.trainer.generate_rolling_slices(df_feat):
            total_slices += 1
            gate_res, risk_mult = self.trainer.evaluate_slice_generalization(is_df, oos_eval_df, symbol, slice_idx)
            
            if gate_res.passed:
                gen_passes += 1
                trades = engine.simulate_trades(
                    forward_live_df,
                    symbol=symbol,
                    slice_idx=slice_idx,
                    substrategy="sub1_single_coin",
                    dynamic_risk_multiplier=risk_mult,
                )
                all_trades.extend(trades)

        pass_rate = (gen_passes / total_slices * 100.0) if total_slices > 0 else 0.0
        start_date = str(df.index[0])[:10]
        end_date = str(df.index[-1])[:10]

        summary = calculate_summary_metrics(
            trades=all_trades,
            initial_capital=self.config.initial_capital,
            final_capital=engine.capital,
            substrategy=f"Sub1-SingleCoin({symbol})",
            train_tf=self.config.train_tf.value,
            trade_tf=self.config.trade_tf.value,
            start_date=start_date,
            end_date=end_date,
            gen_pass_rate=pass_rate,
        )
        return all_trades, summary

    def run_btc_exogenous_altcoins(
        self,
        btc_df: pd.DataFrame,
        alt_dfs: Dict[str, pd.DataFrame],
    ) -> Tuple[List[TradeRecord], BacktestSummaryReport]:
        """
        Sub-strategy 2: BTC provides exogenous market regime features and anti-hallucination gating.
        BTC itself is NOT traded; trades are distributed across altcoins (BNB, SOL, ETH).
        """
        btc_feat = extract_features(btc_df)
        alt_feats = {sym: extract_features(df) for sym, df in alt_dfs.items()}

        engine = RealisticExecutionEngine(self.config)
        all_trades: List[TradeRecord] = []
        gen_passes = 0
        total_slices = 0

        for slice_idx, is_btc, oos_eval_btc, forward_live_btc, trigger in self.trainer.generate_rolling_slices(btc_feat):
            total_slices += 1
            gate_res, risk_mult = self.trainer.evaluate_slice_generalization(is_btc, oos_eval_btc, "BTCUSDT", slice_idx)

            if gate_res.passed:
                gen_passes += 1
                start_ts = forward_live_btc.index[0]
                end_ts = forward_live_btc.index[-1]
                
                # Trade altcoins in this forward window
                for sym, a_feat in alt_feats.items():
                    oos_alt = a_feat.loc[start_ts:end_ts]
                    if len(oos_alt) > 5:
                        trades = engine.simulate_trades(
                            oos_alt,
                            symbol=sym,
                            slice_idx=slice_idx,
                            substrategy="sub2_btc_exogenous",
                            dynamic_risk_multiplier=risk_mult * 0.80,
                        )
                        all_trades.extend(trades)

        pass_rate = (gen_passes / total_slices * 100.0) if total_slices > 0 else 0.0
        start_date = str(btc_df.index[0])[:10]
        end_date = str(btc_df.index[-1])[:10]

        summary = calculate_summary_metrics(
            trades=all_trades,
            initial_capital=self.config.initial_capital,
            final_capital=engine.capital,
            substrategy="Sub2-BTC_Exogenous_Altcoins(BNB/SOL/ETH)",
            train_tf=self.config.train_tf.value,
            trade_tf=self.config.trade_tf.value,
            start_date=start_date,
            end_date=end_date,
            gen_pass_rate=pass_rate,
        )
        return all_trades, summary

    def run_cmc20_basket(self, cmc_df: pd.DataFrame) -> Tuple[List[TradeRecord], BacktestSummaryReport]:
        """Sub-strategy 3: CMC20 synthetic index basket tracking with synchronized fills."""
        val = cmc_df['value'].values
        ret = np.abs(pd.Series(val).pct_change().fillna(0.001).values)
        df_basket = pd.DataFrame(index=cmc_df.index)
        df_basket['open'] = val * (1.0 - ret * 0.25)
        df_basket['high'] = val * (1.0 + ret * 0.75)
        df_basket['low'] = val * (1.0 - ret * 0.75)
        df_basket['close'] = val
        df_basket['volume'] = ret * 1e7 + 1000.0

        df_feat = extract_features(df_basket)
        engine = RealisticExecutionEngine(self.config)
        all_trades: List[TradeRecord] = []
        gen_passes = 0
        total_slices = 0

        for slice_idx, is_df, oos_eval_df, forward_live_df, trigger in self.trainer.generate_rolling_slices(df_feat):
            total_slices += 1
            gate_res, risk_mult = self.trainer.evaluate_slice_generalization(is_df, oos_eval_df, "CMC20", slice_idx)

            if gate_res.passed:
                gen_passes += 1
                trades = engine.simulate_trades(
                    forward_live_df,
                    symbol="CMC20_INDEX",
                    slice_idx=slice_idx,
                    substrategy="sub3_cmc20_basket",
                    dynamic_risk_multiplier=risk_mult,
                )
                all_trades.extend(trades)

        pass_rate = (gen_passes / total_slices * 100.0) if total_slices > 0 else 0.0
        start_date = str(cmc_df.index[0])[:10]
        end_date = str(cmc_df.index[-1])[:10]

        summary = calculate_summary_metrics(
            trades=all_trades,
            initial_capital=self.config.initial_capital,
            final_capital=engine.capital,
            substrategy="Sub3-CMC20_Basket_Index",
            train_tf=self.config.train_tf.value,
            trade_tf=self.config.trade_tf.value,
            start_date=start_date,
            end_date=end_date,
            gen_pass_rate=pass_rate,
        )
        return all_trades, summary
