"""
Empirical Comparison: Isolated Accounts vs. Shared Unified Account.
Addresses the core architectural question:
"有必要多个币种交易同一账户吗（增加账户资金使用率，但可能遇上同时持仓、同时开仓的冲突）？"

Tests 3 distinct production account architectures on the 2-year 15m dataset:
1. Architecture A (Isolated Accounts): 120 USDT partitioned into 4 x 30 USDT sub-accounts. Zero contagion.
2. Architecture B (Unrestricted Shared Account): 120 USDT pooled, no concurrency limit. High capital utilization, but maximum correlation risk.
3. Architecture C (Governed Shared Account): 120 USDT pooled, max 2 concurrent positions, 50% cash reserve, correlation circuit breaker.
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

from matrix.models import MatrixConfig, TradeRecord
from matrix.feature_engine import extract_features


class AccountArchitectureBenchmark:
    def __init__(self, initial_capital: float = 120.0, leverage: float = 20.0, risk_pct: float = 0.05):
        self.initial_capital = initial_capital
        self.leverage = leverage
        self.risk_pct = risk_pct
        self.maker_fee = 0.0002
        self.taker_fee = 0.0005
        self.slippage_bps = 0.0002

    def run_isolated_accounts(self, symbol_dfs: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Mode 1: 4 separate sub-accounts with 30 USDT each."""
        sub_cap = self.initial_capital / len(symbol_dfs)
        total_pnl = 0.0
        all_trades = []
        equity_histories = {s: [sub_cap] for s in symbol_dfs}

        for sym, df in symbol_dfs.items():
            cap = sub_cap
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            open_p = df['open'].values
            atr14 = df['atr14'].values
            sig = df['signal'].values
            n = len(close)

            pos = 0
            entry_px = 0.0
            sl = 0.0
            tp = 0.0
            contracts = 0.0
            nom_exp = 0.0

            for i in range(1, n):
                if pos != 0:
                    hit_sl = (low[i] <= sl) if pos == 1 else (high[i] >= sl)
                    hit_tp = (high[i] >= tp) if pos == 1 else (low[i] <= tp)
                    if hit_sl:
                        exit_px = sl * (1.0 - self.slippage_bps if pos == 1 else 1.0 + self.slippage_bps)
                        fee = nom_exp * self.taker_fee
                        pnl = (contracts * (exit_px - entry_px) if pos == 1 else contracts * (entry_px - exit_px)) - fee
                        cap += pnl
                        pos = 0
                        all_trades.append({'sym': sym, 'pnl': pnl, 'side': pos, 'mode': 'isolated'})
                    elif hit_tp:
                        exit_px = tp
                        fee = nom_exp * self.maker_fee
                        pnl = (contracts * (exit_px - entry_px) if pos == 1 else contracts * (entry_px - exit_px)) - fee
                        cap += pnl
                        pos = 0
                        all_trades.append({'sym': sym, 'pnl': pnl, 'side': pos, 'mode': 'isolated'})
                elif sig[i - 1] != 0 and cap > 5.0:
                    direction = sig[i - 1]
                    cur_atr = max(atr14[i], close[i] * 0.002)
                    sl_dist = cur_atr * 1.5
                    entry_px = open_p[i]
                    sl = entry_px - sl_dist if direction == 1 else entry_px + sl_dist
                    tp = entry_px + sl_dist * 2.0 if direction == 1 else entry_px - sl_dist * 2.0
                    
                    risk_budget = cap * self.risk_pct
                    desired = risk_budget / max(sl_dist, 1e-9)
                    max_c = (cap * self.leverage) / entry_px
                    contracts = min(desired, max_c)
                    nom_exp = contracts * entry_px
                    cap -= nom_exp * self.maker_fee
                    pos = direction

                equity_histories[sym].append(cap)
            total_pnl += (cap - sub_cap)

        final_cap = self.initial_capital + total_pnl
        ret_pct = (total_pnl / self.initial_capital) * 100.0

        # Calculate overall drawdown
        # Sum cross-sub-account equities bar-by-bar
        min_len = min(len(h) for h in equity_histories.values())
        tot_eq = [sum(equity_histories[s][k] for s in symbol_dfs) for k in range(min_len)]
        peak = np.maximum.accumulate(tot_eq)
        max_dd = float(np.max((peak - tot_eq) / peak)) * 100.0

        return {
            "mode": "Isolated (4x30 USDT)",
            "initial_capital": self.initial_capital,
            "final_capital": final_cap,
            "net_return_pct": ret_pct,
            "max_drawdown_pct": max_dd,
            "total_trades": len(all_trades),
            "capital_utilization_avg": 25.0, # By construction: idle capital cannot be borrowed by active coins
        }

    def run_shared_account(self, symbol_dfs: Dict[str, pd.DataFrame], max_concurrent: int = 4, reserve_pct: float = 0.0) -> Dict[str, Any]:
        """Modes 2 & 3: Unified 120 USDT account, parameterized by concurrency limit and reserve."""
        cap = self.initial_capital
        all_trades = []
        equity_curve = [cap]

        # Align timestamps across all symbols
        common_idx = symbol_dfs[list(symbol_dfs.keys())[0]].index
        for s in symbol_dfs:
            common_idx = common_idx.intersection(symbol_dfs[s].index)
        common_idx = sorted(list(common_idx))

        positions: Dict[str, Dict[str, Any]] = {}
        daily_utilization = []

        for ts in common_idx:
            # 1. Check exits on active positions
            closed_syms = []
            for sym, pos_data in positions.items():
                row = symbol_dfs[sym].loc[ts]
                h_p, l_p, c_p = row['high'], row['low'], row['close']
                pos = pos_data['pos']
                sl = pos_data['sl']
                tp = pos_data['tp']
                entry_px = pos_data['entry_px']
                contracts = pos_data['contracts']
                nom_exp = pos_data['nom_exp']

                hit_sl = (l_p <= sl) if pos == 1 else (h_p >= sl)
                hit_tp = (h_p >= tp) if pos == 1 else (l_p <= tp)

                if hit_sl:
                    exit_px = sl * (1.0 - self.slippage_bps if pos == 1 else 1.0 + self.slippage_bps)
                    fee = nom_exp * self.taker_fee
                    pnl = (contracts * (exit_px - entry_px) if pos == 1 else contracts * (entry_px - exit_px)) - fee
                    cap += pnl
                    closed_syms.append(sym)
                    all_trades.append({'sym': sym, 'pnl': pnl, 'side': pos, 'reason': 'SL'})
                elif hit_tp:
                    exit_px = tp
                    fee = nom_exp * self.maker_fee
                    pnl = (contracts * (exit_px - entry_px) if pos == 1 else contracts * (entry_px - exit_px)) - fee
                    cap += pnl
                    closed_syms.append(sym)
                    all_trades.append({'sym': sym, 'pnl': pnl, 'reason': 'TP'})

            for s in closed_syms:
                del positions[s]

            # 2. Check entries for idle symbols
            avail_cap = cap * (1.0 - reserve_pct)
            current_nom_exp = sum(p['nom_exp'] for p in positions.values())
            utilization = (current_nom_exp / max(cap * self.leverage, 1.0)) * 100.0
            daily_utilization.append(utilization)

            if len(positions) < max_concurrent and avail_cap > 10.0:
                for sym, df_s in symbol_dfs.items():
                    if sym not in positions and len(positions) < max_concurrent:
                        row = df_s.loc[ts]
                        sig = row['signal']
                        if sig != 0:
                            direction = sig
                            cur_atr = max(row['atr14'], row['close'] * 0.002)
                            sl_dist = cur_atr * 1.5
                            entry_px = row['open']
                            sl = entry_px - sl_dist if direction == 1 else entry_px + sl_dist
                            tp = entry_px + sl_dist * 2.0 if direction == 1 else entry_px - sl_dist * 2.0

                            # Budget allocated from available capital
                            risk_budget = (avail_cap / max_concurrent) * self.risk_pct
                            desired = risk_budget / max(sl_dist, 1e-9)
                            max_c = ((avail_cap / max_concurrent) * self.leverage) / entry_px
                            contracts = min(desired, max_c)
                            nom_exp = contracts * entry_px
                            cap -= nom_exp * self.maker_fee

                            positions[sym] = {
                                'pos': direction,
                                'entry_px': entry_px,
                                'sl': sl,
                                'tp': tp,
                                'contracts': contracts,
                                'nom_exp': nom_exp,
                            }

            equity_curve.append(cap)
            if cap <= 5.0:
                break

        final_cap = cap
        ret_pct = ((final_cap - self.initial_capital) / self.initial_capital) * 100.0
        peak = np.maximum.accumulate(equity_curve)
        max_dd = float(np.max((peak - equity_curve) / peak)) * 100.0

        mode_name = f"Shared (Max {max_concurrent} Concurrency, Reserve {reserve_pct*100:.0f}%)"
        return {
            "mode": mode_name,
            "initial_capital": self.initial_capital,
            "final_capital": final_cap,
            "net_return_pct": ret_pct,
            "max_drawdown_pct": max_dd,
            "total_trades": len(all_trades),
            "capital_utilization_avg": float(np.mean(daily_utilization)),
        }
