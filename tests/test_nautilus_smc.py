"""
Test NautilusTrader SMC Strategy on Binance BTCUSDT 15m.
"""

import os
import sys
from decimal import Decimal

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import pandas as pd
import numpy as np

import nautilus_trader
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.model.data import Bar, BarType, BarSpecification
from nautilus_trader.model.enums import BarAggregation, PriceType, OrderSide, TimeInForce
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.identifiers import InstrumentId, Venue, Symbol
from nautilus_trader.model.objects import Price, Quantity, Money, Currency

from src.qlib_smc_alpha import QlibSMCConfig, compute_qlib_smc_alpha
from src.nautilus_smc_strategy import NautilusSMCHighFreqStrategy, NautilusSMCConfig


def run_test():
    print("=" * 70)
    print("Testing NautilusTrader SMC Strategy Integration (Fast Feed)...")
    print("=" * 70)

    instrument_id = InstrumentId(Symbol('BTCUSDT'), Venue('BINANCE'))
    instrument = CurrencyPair(
        instrument_id=instrument_id,
        raw_symbol=Symbol('BTCUSDT'),
        base_currency=Currency.from_str('BTC'),
        quote_currency=Currency.from_str('USDT'),
        price_precision=2,
        size_precision=6,
        price_increment=Price.from_str('0.01'),
        size_increment=Quantity.from_str('0.000001'),
        lot_size=Quantity.from_str('0.000001'),
        max_quantity=Quantity.from_str('10000.0'),
        min_quantity=Quantity.from_str('0.000001'),
        max_price=Price.from_str('1000000.0'),
        min_price=Price.from_str('0.01'),
        margin_init=Decimal('0'),
        margin_maint=Decimal('0'),
        maker_fee=Decimal('0.0002'),
        taker_fee=Decimal('0.0005'),
        ts_event=0,
        ts_init=0
    )

    engine_config = BacktestEngineConfig(
        trader_id="TESTER-001",
        logging=LoggingConfig(log_level="ERROR"),
    )
    engine = BacktestEngine(config=engine_config)
    engine.add_venue(
        venue=Venue("BINANCE"),
        oms_type=nautilus_trader.model.enums.OmsType.NETTING,
        account_type=nautilus_trader.model.enums.AccountType.MARGIN,
        base_currency=Currency.from_str("USDT"),
        starting_balances=[Money(1000.0, Currency.from_str("USDT"))],
    )
    engine.add_instrument(instrument)

    bar_spec = BarSpecification(15, BarAggregation.MINUTE, PriceType.LAST)
    bar_type = BarType(instrument_id, bar_spec)

    # Load 1 month of BTC 15m
    df = pd.read_parquet('data/raw_extracted/BTC/BTCUSDT_15m_ohlcv_2024-01.parquet')
    print(f"Loaded data: {len(df)} bars from {df.index.min()} to {df.index.max()}")

    # Pre-compute signals using Qlib + AlphaGPT factor engine
    qlib_cfg = QlibSMCConfig(
        swing_len=3,
        min_score_threshold=60.0,
        vol_spike_threshold=1.1,
    )
    print("Computing Qlib SMC Alpha factors...")
    res_df = compute_qlib_smc_alpha(df, qlib_cfg)

    signals_feed = {}
    bars = []
    for ts, row in df.iterrows():
        ts_ns = int(ts.timestamp() * 1_000_000_000)
        bar = Bar(
            bar_type=bar_type,
            open=Price(row['open'], precision=2),
            high=Price(row['high'], precision=2),
            low=Price(row['low'], precision=2),
            close=Price(row['close'], precision=2),
            volume=Quantity(row['volume'], precision=6),
            ts_event=ts_ns,
            ts_init=ts_ns,
        )
        bars.append(bar)

        sig = int(res_df.loc[ts, "signal"]) if ts in res_df.index else 0
        atr = float(res_df.loc[ts, "atr"]) if (ts in res_df.index and "atr" in res_df.columns) else (row['high'] - row['low'])
        credal_u = float(res_df.loc[ts, "credal_uncertainty"]) if (ts in res_df.index and "credal_uncertainty" in res_df.columns) else 0.0
        credal_abstain = bool(res_df.loc[ts, "should_abstain"]) if (ts in res_df.index and "should_abstain" in res_df.columns) else False
        if sig != 0:
            signals_feed[ts_ns] = {
                "signal": sig,
                "atr": atr,
                "credal_u": credal_u,
                "credal_abstain": credal_abstain,
            }
    print(f"Generated {len(signals_feed)} entry signals in feed.")
    engine.add_data(bars)

    strat_cfg = NautilusSMCConfig(
        instrument_id=instrument_id,
        bar_type=bar_type,
        min_confluence_score=60.0,
        risk_per_trade_pct=0.015,
        ideal_rr_ratio=2.0,
    )
    strategy = NautilusSMCHighFreqStrategy(strat_cfg, signals_feed=signals_feed)
    engine.add_strategy(strategy)

    print("\nRunning NautilusTrader Engine...")
    import time
    t0 = time.time()
    engine.run()
    el = time.time() - t0
    print(f"NautilusTrader Engine Run Complete in {el:.3f}s!")

    print("\n=== Strategy Execution Metrics ===")
    print(f"Total Signals Generated:    {strategy.total_signals}")
    print(f"Total Orders Submitted:     {strategy.total_orders_submitted}")
    print(f"Executed Round-Trips:       {strategy.executed_trades_count}")
    print(f"Winning Trades:             {strategy.winning_trades_count}")
    print(f"Losing Trades:              {strategy.losing_trades_count}")
    win_rate = (strategy.winning_trades_count / max(strategy.executed_trades_count, 1)) * 100.0
    print(f"Win Rate:                   {win_rate:.1f}%")
    print(f"Cumulative Realized PnL:    ${strategy.realized_pnl_accumulator:+.2f}")
    
    days = (df.index.max() - df.index.min()).total_seconds() / 86400.0
    daily_freq = strategy.executed_trades_count / max(days, 1.0)
    print(f"Daily Trading Frequency:    {daily_freq:.2f} trades/day")

    fills = engine.trader.generate_order_fills_report()
    print(f"Nautilus Order Fills Count: {len(fills)}")
    print("=" * 70)

    results = {
        "total_signals": strategy.total_signals,
        "total_orders_submitted": strategy.total_orders_submitted,
        "executed_trades_count": strategy.executed_trades_count,
        "winning_trades_count": strategy.winning_trades_count,
        "losing_trades_count": strategy.losing_trades_count,
        "win_rate": win_rate,
        "realized_pnl": strategy.realized_pnl_accumulator,
        "daily_trading_frequency": daily_freq,
        "fills_count": len(fills),
        "credal_rejections_count": strategy.credal_rejections_count,
    }
    engine.dispose()
    return results


def test_nautilus_smc_strategy_execution():
    """Verify end-to-end NautilusTrader execution with SMC alpha signals."""
    metrics = run_test()
    assert metrics["executed_trades_count"] > 0, "No trades were executed"
    assert metrics["total_orders_submitted"] > 0, "No orders were submitted"
    assert metrics["fills_count"] > 0, "No order fills recorded"


def test_nautilus_credal_gate_rejection():
    """Verify that Credal gate rejects high epistemic uncertainty signals."""
    instrument_id = InstrumentId(Symbol('BTCUSDT'), Venue('BINANCE'))
    instrument = CurrencyPair(
        instrument_id=instrument_id,
        raw_symbol=Symbol('BTCUSDT'),
        base_currency=Currency.from_str('BTC'),
        quote_currency=Currency.from_str('USDT'),
        price_precision=2,
        size_precision=6,
        price_increment=Price.from_str('0.01'),
        size_increment=Quantity.from_str('0.000001'),
        lot_size=Quantity.from_str('0.000001'),
        max_quantity=Quantity.from_str('10000.0'),
        min_quantity=Quantity.from_str('0.000001'),
        max_price=Price.from_str('1000000.0'),
        min_price=Price.from_str('0.01'),
        margin_init=Decimal('0'),
        margin_maint=Decimal('0'),
        maker_fee=Decimal('0.0002'),
        taker_fee=Decimal('0.0005'),
        ts_event=0,
        ts_init=0
    )
    engine = BacktestEngine(config=BacktestEngineConfig(trader_id="TESTER-CREDAL", logging=LoggingConfig(log_level="ERROR")))
    engine.add_venue(
        venue=Venue("BINANCE"),
        oms_type=nautilus_trader.model.enums.OmsType.NETTING,
        account_type=nautilus_trader.model.enums.AccountType.MARGIN,
        base_currency=Currency.from_str("USDT"),
        starting_balances=[Money(1000.0, Currency.from_str("USDT"))],
    )
    engine.add_instrument(instrument)

    bar_spec = BarSpecification(15, BarAggregation.MINUTE, PriceType.LAST)
    bar_type = BarType(instrument_id, bar_spec)

    # Create 3 synthetic bars
    bars = []
    t_base = 1704067200000000000  # 2024-01-01
    for i in range(3):
        t_ns = t_base + i * 15 * 60 * 1_000_000_000
        bar = Bar(
            bar_type=bar_type,
            open=Price(42000.0 + i * 10, precision=2),
            high=Price(42100.0 + i * 10, precision=2),
            low=Price(41950.0 + i * 10, precision=2),
            close=Price(42050.0 + i * 10, precision=2),
            volume=Quantity(10.0, precision=6),
            ts_event=t_ns,
            ts_init=t_ns,
        )
        bars.append(bar)
    engine.add_data(bars)

    # Feed: bar 0 has high epistemic uncertainty u=0.60 (> 0.35 threshold) -> REJECT
    # Feed: bar 1 has low uncertainty u=0.10 -> APPROVE
    signals_feed = {
        bars[0].ts_event: {"signal": 1, "atr": 100.0, "credal_u": 0.60},
        bars[1].ts_event: {"signal": 1, "atr": 100.0, "credal_u": 0.10},
    }

    strat_cfg = NautilusSMCConfig(
        instrument_id=instrument_id,
        bar_type=bar_type,
        credal_u_max=0.35,
        use_credal_gate=True,
    )
    strategy = NautilusSMCHighFreqStrategy(strat_cfg, signals_feed=signals_feed)
    engine.add_strategy(strategy)
    engine.run()

    assert strategy.credal_rejections_count == 1, f"Expected 1 credal rejection, got {strategy.credal_rejections_count}"
    assert strategy.total_orders_submitted == 1, f"Expected 1 order submitted, got {strategy.total_orders_submitted}"
    engine.dispose()


if __name__ == "__main__":
    run_test()
