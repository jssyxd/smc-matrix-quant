"""
Comprehensive Regression & Boundary Condition Test Suite for NautilusTrader SMC Strategy.
Target: Validate bug conditions and fixes for:
1. Ghost Position Bug: Entry position flag setting immediately on order submission vs on_order_filled.
2. Ghost Exit Trigger: When limit order is unfilled and price moves away, verify whether fake exit order triggers.
3. Balance & Circuit Breaker: Integration with real portfolio balance_free vs hardcoded accumulator.
4. Order Timeout / Rejection: Handling of unfilled stale limit orders.
"""

import os
import sys
from decimal import Decimal
import pytest
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import nautilus_trader
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.model.data import Bar, BarType, BarSpecification
from nautilus_trader.model.enums import BarAggregation, PriceType, OrderSide, TimeInForce
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.identifiers import InstrumentId, Venue, Symbol
from nautilus_trader.model.objects import Price, Quantity, Money, Currency

from src.nautilus_smc_strategy import NautilusSMCHighFreqStrategy, NautilusSMCConfig


def create_test_setup(trader_id="TESTER-REG", starting_balance=1000.0):
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
        ts_init=0,
    )
    engine = BacktestEngine(config=BacktestEngineConfig(trader_id=trader_id, logging=LoggingConfig(log_level="ERROR")))
    engine.add_venue(
        venue=Venue("BINANCE"),
        oms_type=nautilus_trader.model.enums.OmsType.NETTING,
        account_type=nautilus_trader.model.enums.AccountType.MARGIN,
        base_currency=Currency.from_str("USDT"),
        starting_balances=[Money(starting_balance, Currency.from_str("USDT"))],
    )
    engine.add_instrument(instrument)

    bar_spec = BarSpecification(15, BarAggregation.MINUTE, PriceType.LAST)
    bar_type = BarType(instrument_id, bar_spec)

    return engine, instrument_id, bar_type


def test_ghost_position_flag_immediate_mutation():
    """
    Boundary Test 1: Verify whether active_position_side is prematurely set before fill.
    In the un-refactored code, active_position_side is set in _execute_entry() right after
    order creation, even before the order is filled by the matching engine!
    """
    engine, instrument_id, bar_type = create_test_setup("TEST-GHOST-FLAG")

    t_base = 1704067200000000000
    bars = []
    # Bar 0: Signal triggered at close 42000. Limit BUY submitted at 42000.
    bars.append(Bar(
        bar_type=bar_type,
        open=Price(42000.0, 2),
        high=Price(42050.0, 2),
        low=Price(41950.0, 2),
        close=Price(42000.0, 2),
        volume=Quantity(10.0, 6),
        ts_event=t_base,
        ts_init=t_base,
    ))
    # Bar 1: Price gaps way UP (low is 43000), so limit buy at 42000 CANNOT fill!
    bars.append(Bar(
        bar_type=bar_type,
        open=Price(43000.0, 2),
        high=Price(43500.0, 2),
        low=Price(42900.0, 2),
        close=Price(43200.0, 2),
        volume=Quantity(10.0, 6),
        ts_event=t_base + 15 * 60 * 1_000_000_000,
        ts_init=t_base + 15 * 60 * 1_000_000_000,
    ))

    engine.add_data(bars)

    signals_feed = {
        bars[0].ts_event: {"signal": 1, "atr": 200.0, "credal_u": 0.10}
    }

    strat_cfg = NautilusSMCConfig(
        instrument_id=instrument_id,
        bar_type=bar_type,
        maker_limit_entry=True,
    )
    strategy = NautilusSMCHighFreqStrategy(strat_cfg, signals_feed=signals_feed)
    engine.add_strategy(strategy)
    engine.run()

    fills_report = engine.trader.generate_order_fills_report()
    # Check if the limit order actually filled
    fill_count = len(fills_report)

    # In a correct event-driven design:
    # If the limit order at 42000 never fills because Bar 1 low is 42900,
    # fill_count must be 0, and strategy.active_position_side must be None!
    # In the flawed implementation, active_position_side was set to BUY upon submission,
    # and in Bar 1, since high is 43500 >= take_profit_price (42000 + 300*2 = 42600),
    # it triggers a TAKE_PROFIT exit market order, closing a position that NEVER existed!
    print(f"\n[Test 1 Diagnostic] Fills count: {fill_count}")
    print(f"[Test 1 Diagnostic] Total orders submitted: {strategy.total_orders_submitted}")
    print(f"[Test 1 Diagnostic] Executed round trips: {strategy.executed_trades_count}")
    print(f"[Test 1 Diagnostic] Trade logs: {strategy.trade_logs}")

    # Document the exact manifestation of the Ghost Position Bug
    ghost_exit_triggered = any(log.get("action") == "EXIT" for log in strategy.trade_logs)
    print(f"[Test 1 Diagnostic] Ghost Exit Triggered without Fill: {ghost_exit_triggered}")

    engine.dispose()
    return {
        "fill_count": fill_count,
        "total_orders_submitted": strategy.total_orders_submitted,
        "executed_trades_count": strategy.executed_trades_count,
        "ghost_exit_triggered": ghost_exit_triggered,
        "active_position_side": strategy.active_position_side,
    }


def test_ghost_position_fake_market_order_generation():
    """
    Boundary Test 2: Unfilled limit order + price movement triggering fake market exit.
    Simulate price plunging below stop loss without limit buy having filled.
    """
    engine, instrument_id, bar_type = create_test_setup("TEST-GHOST-EXIT")

    t_base = 1704067200000000000
    bars = []
    # Bar 0: Signal triggered at close 42000. Limit BUY at 41000 (well below market).
    # Since current_close is 42000, strategy puts limit at 42000.
    # To ensure it doesn't fill on bar 0, bar 0 low is 42000.
    # On bar 1, price drops straight from open 41000 down to 40000 (gapping down).
    bars.append(Bar(
        bar_type=bar_type,
        open=Price(42050.0, 2),
        high=Price(42100.0, 2),
        low=Price(42000.0, 2),
        close=Price(42000.0, 2),
        volume=Quantity(1.0, 6),
        ts_event=t_base,
        ts_init=t_base,
    ))
    bars.append(Bar(
        bar_type=bar_type,
        open=Price(41000.0, 2),
        high=Price(41100.0, 2),
        low=Price(40000.0, 2),
        close=Price(40500.0, 2),
        volume=Quantity(1.0, 6),
        ts_event=t_base + 15 * 60 * 1_000_000_000,
        ts_init=t_base + 15 * 60 * 1_000_000_000,
    ))

    engine.add_data(bars)

    signals_feed = {
        bars[0].ts_event: {"signal": 1, "atr": 200.0, "credal_u": 0.10}
    }

    strat_cfg = NautilusSMCConfig(
        instrument_id=instrument_id,
        bar_type=bar_type,
        maker_limit_entry=True,
    )
    strategy = NautilusSMCHighFreqStrategy(strat_cfg, signals_feed=signals_feed)
    engine.add_strategy(strategy)
    engine.run()

    fills_report = engine.trader.generate_order_fills_report()
    engine.dispose()

    exit_logs = [log for log in strategy.trade_logs if log.get("action") == "EXIT"]
    return {
        "fills_count": len(fills_report),
        "exit_logs_count": len(exit_logs),
        "exit_logs": exit_logs,
        "total_orders_submitted": strategy.total_orders_submitted,
    }


def test_balance_free_and_risk_sizing_verification():
    """
    Boundary Test 3: Verify capital sizing dependence.
    Un-refactored: account_equity = 1000.0 + self.realized_pnl_accumulator
    Target: portfolio.account(venue).balance_free (or portfolio.equity).
    """
    engine, instrument_id, bar_type = create_test_setup("TEST-BALANCE", starting_balance=50000.0)

    t_base = 1704067200000000000
    bars = []
    bars.append(Bar(
        bar_type=bar_type,
        open=Price(42000.0, 2),
        high=Price(42100.0, 2),
        low=Price(41900.0, 2),
        close=Price(42000.0, 2),
        volume=Quantity(10.0, 6),
        ts_event=t_base,
        ts_init=t_base,
    ))
    engine.add_data(bars)

    signals_feed = {
        bars[0].ts_event: {"signal": 1, "atr": 200.0, "credal_u": 0.10}
    }

    strat_cfg = NautilusSMCConfig(
        instrument_id=instrument_id,
        bar_type=bar_type,
        risk_per_trade_pct=0.015,  # 1.5%
        maker_limit_entry=False,   # Market order to ensure immediate fill
    )
    strategy = NautilusSMCHighFreqStrategy(strat_cfg, signals_feed=signals_feed)
    engine.add_strategy(strategy)
    engine.run()

    # If starting balance is 50,000, 1.5% risk is $750.
    # stop_dist = 1.5 * 200 = 300.
    # Expected shares = 750 / 300 = 2.5 BTC.
    # But in the flawed version, it uses hardcoded 1000.0 + realized_pnl, so risk is $15 -> 0.05 BTC!
    actual_shares = strategy.current_shares if strategy.current_shares > 0 else (
        strategy.trade_logs[0]["shares"] if strategy.trade_logs else 0.0
    )
    engine.dispose()
    return {
        "actual_shares": actual_shares,
        "is_hardcoded_1000": abs(actual_shares - 0.05) < 0.01,
        "is_linked_to_50k": abs(actual_shares - 2.5) < 0.01,
    }


def test_timeout_cancellation_unfilled_order():
    """
    Boundary Test 4: Stale limit order cancellation.
    When a limit order is submitted and remains unfilled for N bars,
    verify whether the strategy cancels the order or leaves it hanging forever.
    """
    engine, instrument_id, bar_type = create_test_setup("TEST-TIMEOUT")

    t_base = 1704067200000000000
    bars = []
    # Bar 0: Signal at 40000. Limit BUY at 40000.
    bars.append(Bar(
        bar_type=bar_type,
        open=Price(40000.0, 2),
        high=Price(40050.0, 2),
        low=Price(40000.0, 2),
        close=Price(40000.0, 2),
        volume=Quantity(1.0, 6),
        ts_event=t_base,
        ts_init=t_base,
    ))
    # Bars 1 to 10: Price rallies away to 45000+. The limit order at 40000 is left behind.
    for i in range(1, 10):
        t_ns = t_base + i * 15 * 60 * 1_000_000_000
        bars.append(Bar(
            bar_type=bar_type,
            open=Price(44000.0 + i * 100, 2),
            high=Price(44500.0 + i * 100, 2),
            low=Price(43900.0 + i * 100, 2),
            close=Price(44200.0 + i * 100, 2),
            volume=Quantity(5.0, 6),
            ts_event=t_ns,
            ts_init=t_ns,
        ))

    engine.add_data(bars)
    signals_feed = {
        bars[0].ts_event: {"signal": 1, "atr": 200.0, "credal_u": 0.10}
    }

    strat_cfg = NautilusSMCConfig(
        instrument_id=instrument_id,
        bar_type=bar_type,
        maker_limit_entry=True,
    )
    strategy = NautilusSMCHighFreqStrategy(strat_cfg, signals_feed=signals_feed)
    engine.add_strategy(strategy)
    engine.run()

    # Check whether any cancel order was issued
    # In un-refactored strategy, there is no cancel_order logic or timeout mechanism
    orders_report = engine.trader.generate_orders_report()
    open_orders = [o for o in engine.cache.orders() if o.is_open]
    cancelled_orders = [o for o in engine.cache.orders() if o.is_canceled]

    engine.dispose()
    return {
        "total_orders": len(orders_report),
        "open_orders": len(open_orders),
        "cancelled_orders": len(cancelled_orders),
    }


if __name__ == "__main__":
    res1 = test_ghost_position_flag_immediate_mutation()
    print("Test 1 Result (Ghost Position Flag Mutation):", res1)

    res2 = test_ghost_position_fake_market_order_generation()
    print("Test 2 Result (Ghost Exit Trigger):", res2)

    res3 = test_balance_free_and_risk_sizing_verification()
    print("Test 3 Result (Balance Free Integration):", res3)

    res4 = test_timeout_cancellation_unfilled_order()
    print("Test 4 Result (Timeout Cancellation):", res4)
