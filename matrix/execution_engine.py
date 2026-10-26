"""
Realistic Execution Engine for SMC Matrix Backtesting.
Adheres strictly to the transaction friction requirements:
- Initial capital: 120 USDT
- Leverage: 20x nominal position scaling
- Risk per trade: 5% of free balance
- Fees: Maker 0.02% (limit entry), Taker 0.05% (stop loss/market exit) on nominal value
- Intra-bar pessimism: same-bar conflict strictly executes stop loss first.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any, Optional
from matrix.models import TradeRecord, MatrixConfig


class RealisticExecutionEngine:
    def __init__(self, config: MatrixConfig = MatrixConfig()):
        self.config = config
        self.reset()

    def reset(self, initial_capital: Optional[float] = None) -> None:
        self.capital = initial_capital if initial_capital is not None else self.config.initial_capital
        self.initial_capital = self.capital
        self.trades: List[TradeRecord] = []
        self.trade_counter = 0

    def simulate_trades(
        self,
        df: pd.DataFrame,
        symbol: str,
        slice_idx: int = 0,
        substrategy: str = "single_coin",
        dynamic_risk_multiplier: float = 1.0,
    ) -> List[TradeRecord]:
        """
        Simulates bar-by-bar execution.
        Entries are Maker Limit Orders at discount/premium zone (Maker 0.02%).
        Exits are Stop Loss (Taker 0.05% + dynamic slippage) or Take Profit (Maker 0.02%).
        """
        n = len(df)
        if n < 50:
            return []

        close = df['close'].values.astype(float)
        high = df['high'].values.astype(float)
        low = df['low'].values.astype(float)
        open_p = df['open'].values.astype(float)
        atr14 = df['atr14'].values.astype(float) if 'atr14' in df.columns else np.full(n, 1.0)
        signal = df['signal'].values.astype(int) if 'signal' in df.columns else np.zeros(n, dtype=int)
        timestamps = df.index.astype(str) if isinstance(df.index, pd.DatetimeIndex) else df.get('timestamp', np.arange(n)).astype(str).values

        position = 0  # 1 = LONG, -1 = SHORT, 0 = FLAT
        entry_price = 0.0
        stop_loss = 0.0
        take_profit = 0.0
        pos_size_contracts = 0.0  # nominal value in crypto units
        nominal_exposure = 0.0
        entry_ts = ""

        slice_trades = []

        for i in range(1, n):
            c_price = close[i]
            h_price = high[i]
            l_price = low[i]
            o_price = open_p[i]
            cur_atr = max(atr14[i], c_price * 0.002)

            # Check open position exit first (Bar execution)
            if position != 0:
                hit_sl = False
                hit_tp = False

                if position == 1:
                    hit_sl = l_price <= stop_loss
                    hit_tp = h_price >= take_profit
                    
                    # Intra-bar pessimism: same-bar conflict prioritizes Stop Loss
                    if hit_sl:
                        exit_price = min(o_price, stop_loss) * (1.0 - self.config.slippage_bps)
                        exit_fee = nominal_exposure * self.config.taker_fee
                        raw_pnl = pos_size_contracts * (exit_price - entry_price)
                        net_pnl = raw_pnl - exit_fee
                        reason = "STOP_LOSS"
                    elif hit_tp:
                        exit_price = take_profit
                        exit_fee = nominal_exposure * self.config.maker_fee
                        raw_pnl = pos_size_contracts * (exit_price - entry_price)
                        net_pnl = raw_pnl - exit_fee
                        reason = "TAKE_PROFIT"
                    else:
                        continue

                elif position == -1:
                    hit_sl = h_price >= stop_loss
                    hit_tp = l_price <= take_profit

                    if hit_sl:
                        exit_price = max(o_price, stop_loss) * (1.0 + self.config.slippage_bps)
                        exit_fee = nominal_exposure * self.config.taker_fee
                        raw_pnl = pos_size_contracts * (entry_price - exit_price)
                        net_pnl = raw_pnl - exit_fee
                        reason = "STOP_LOSS"
                    elif hit_tp:
                        exit_price = take_profit
                        exit_fee = nominal_exposure * self.config.maker_fee
                        raw_pnl = pos_size_contracts * (entry_price - exit_price)
                        net_pnl = raw_pnl - exit_fee
                        reason = "TAKE_PROFIT"
                    else:
                        continue

                # Close position & update capital
                self.capital += net_pnl
                self.trade_counter += 1
                ret_pct = (net_pnl / max(self.capital - net_pnl, 1.0)) * 100.0

                record = TradeRecord(
                    trade_id=self.trade_counter,
                    timestamp=timestamps[i],
                    symbol=symbol,
                    side="LONG" if position == 1 else "SHORT",
                    entry_price=entry_price,
                    exit_price=exit_price,
                    size_nominal=nominal_exposure,
                    leverage=self.config.leverage,
                    pnl_net=net_pnl,
                    fees=exit_fee + (nominal_exposure * self.config.maker_fee),
                    exit_reason=reason,
                    return_pct=ret_pct,
                    balance_after=max(self.capital, 0.0),
                    slice_idx=slice_idx,
                    substrategy=substrategy,
                )
                slice_trades.append(record)
                self.trades.append(record)
                position = 0

                # If capital drops below minimal threshold, break
                if self.capital <= 10.0:
                    break

            # If FLAT, look for new entry signal from previous bar
            if position == 0 and self.capital > 10.0:
                sig = signal[i - 1]
                if sig != 0:
                    effective_risk_pct = self.config.risk_pct * dynamic_risk_multiplier
                    risk_budget = self.capital * effective_risk_pct
                    sl_dist = cur_atr * 1.5

                    if sig == 1:  # LONG
                        entry_price = o_price
                        stop_loss = entry_price - sl_dist
                        take_profit = entry_price + sl_dist * 2.0  # 1:2 R/R target

                        # Position sizing: risk_budget = pos_size_contracts * sl_dist
                        # Capped by maximum leverage nominal: capital * leverage
                        desired_contracts = risk_budget / max(sl_dist, 1e-9)
                        max_contracts = (self.capital * self.config.leverage) / entry_price
                        pos_size_contracts = min(desired_contracts, max_contracts)
                        nominal_exposure = pos_size_contracts * entry_price

                        # Entry fee (Maker limit entry)
                        entry_fee = nominal_exposure * self.config.maker_fee
                        self.capital -= entry_fee
                        position = 1
                        entry_ts = timestamps[i]

                    elif sig == -1:  # SHORT
                        entry_price = o_price
                        stop_loss = entry_price + sl_dist
                        take_profit = entry_price - sl_dist * 2.0

                        desired_contracts = risk_budget / max(sl_dist, 1e-9)
                        max_contracts = (self.capital * self.config.leverage) / entry_price
                        pos_size_contracts = min(desired_contracts, max_contracts)
                        nominal_exposure = pos_size_contracts * entry_price

                        entry_fee = nominal_exposure * self.config.maker_fee
                        self.capital -= entry_fee
                        position = -1
                        entry_ts = timestamps[i]

        return slice_trades
