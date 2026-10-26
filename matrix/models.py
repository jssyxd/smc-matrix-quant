"""
Domain models for the SMC Multi-Asset Rolling Machine Learning & Backtest Matrix.
Enforces domain discipline: explicit typed structures, immutable contracts, and clear boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import pandas as pd

class TimeFrame(str, Enum):
    TF_5M = "5m"
    TF_15M = "15m"
    TF_30M = "30m"
    TF_1H = "1h"
    TF_2H = "2h"
    TF_3H = "3h"
    TF_4H = "4h"


class SubstrategyType(str, Enum):
    SINGLE_COIN = "single_coin"
    BTC_EXOGENOUS = "btc_exogenous"
    CMC20_BASKET = "cmc20_basket"


class TriggerType(str, Enum):
    SCHEDULED = "scheduled"
    VOLATILITY_EVENT = "volatility_event"


@dataclass(frozen=True)
class MatrixConfig:
    train_tf: TimeFrame = TimeFrame.TF_15M
    trade_tf: TimeFrame = TimeFrame.TF_15M
    window_size: int = 5000
    is_size: int = 2500
    oos_size: int = 2500
    risk_pct: float = 0.05          # 5% capital risk per trade
    leverage: float = 20.0          # 20x leverage
    initial_capital: float = 120.0   # 120 USDT initial capital
    maker_fee: float = 0.0002       # 0.02% Maker fee
    taker_fee: float = 0.0005       # 0.05% Taker fee
    slippage_bps: float = 0.0002    # 2 bps dynamic execution slippage
    min_generalization_score: float = 0.60
    vol_trigger_threshold: float = 1.80
    scheduled_step_bars: int = 288   # ~3 days in 15m bars


@dataclass
class TradeRecord:
    trade_id: int
    timestamp: str
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    size_nominal: float
    leverage: float
    pnl_net: float
    fees: float
    exit_reason: str
    return_pct: float
    balance_after: float
    slice_idx: int
    substrategy: str


@dataclass
class GeneralizationGateResult:
    passed: bool
    g_score: float
    is_sharpe: float
    oos_sharpe: float
    wfe: float
    is_win_rate: float
    oos_win_rate: float
    precision_oos: float
    rejection_reason: Optional[str] = None


@dataclass
class MonteCarloResult:
    n_simulations: int
    var_95_dd: float
    var_99_dd: float
    ruin_probability: float
    max_consecutive_losses: int
    worst_drawdown_simulated: float


@dataclass
class BacktestSummaryReport:
    substrategy: str
    train_tf: str
    trade_tf: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_net_pnl: float
    total_return_pct: float
    cagr: float
    max_drawdown_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate_pct: float
    profit_factor: float
    avg_win: float
    avg_loss: float
    generalization_pass_rate: float
    monte_carlo: Optional[MonteCarloResult] = None
