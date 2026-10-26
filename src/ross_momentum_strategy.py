"""
Ross Cameron 20-Year Day Trading Strategy Implementation.
Based on Warrior Trading / Ross Cameron 20-Year Momentum Strategy (UD4XwSs_0r8).

Key Components:
- Step 2: First Pullback Entry (首波回调突破):
  - Never chase initial vertical spike.
  - Wait for 1-5 pullback candles consolidating above key support (9EMA / 20EMA / VWAP).
  - Pullback low establishes initial Stop Loss (SL).
  - Trigger: The instant a candle breaks above the HIGH of the previous candle, enter immediately.
  - Risk/Reward check: Target is Day High (HOD). Must verify R/R >= 1:1, ideally >= 2:1.
  - Position Sizing: Risk amount = Account * Risk%, Shares = floor(Risk / (Entry - SL)).
- Step 3: Exit & 5 Exit Signals:
  - At Day High (HOD): Conservatively sell 50% (TP1), move Stop Loss to breakeven buffer (Entry + 0.15 ATR).
  - Exit remainder on any of the 5 Exit Signals:
    1. Big Ask Wall (Level 2 resistance wall).
    2. Hidden Iceberg seller (Heavy volume absorption without upward movement).
    3. Tape selling (Time & Sales aggressive hitting bid, bid stepping down).
    4. Candlestick topping tail / long upper wick (exhaustion candle).
    5. Volume divergence (price prints higher high on fading volume).
- Step 4: 5 Walk-Away Rules (Risk Control):
  1. Peak profit retraced by 50% -> halt for the day.
  2. Daily max loss hit -> halt for the day.
  3. Passed 10:00 AM EST -> halt for the day.
  4. Screener has no valid stocks -> stay in cash.
  5. Overall market momentum exhausted -> stop.
"""

from dataclasses import dataclass, field
from enum import Enum
import math
from typing import Dict, List, Optional, Tuple, Any, Union
import datetime
import numpy as np
import pandas as pd


class ExitSignalType(str, Enum):
    NONE = "NONE"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT_1 = "TAKE_PROFIT_1"
    BIG_ASK_WALL = "BIG_ASK_WALL"
    HIDDEN_ICEBERG = "HIDDEN_ICEBERG"
    TAPE_SELLING = "TAPE_SELLING"
    TOPPING_TAIL = "TOPPING_TAIL"
    VOLUME_DIVERGENCE = "VOLUME_DIVERGENCE"
    WALK_AWAY_HALT = "WALK_AWAY_HALT"


class WalkAwayReason(str, Enum):
    PEAK_PROFIT_RETRACED = "PEAK_PROFIT_RETRACED"
    DAILY_MAX_LOSS_HIT = "DAILY_MAX_LOSS_HIT"
    TIME_WINDOW_PASSED = "TIME_WINDOW_PASSED"
    SCREENER_NO_VALID_STOCKS = "SCREENER_NO_VALID_STOCKS"
    MARKET_MOMENTUM_EXHAUSTED = "MARKET_MOMENTUM_EXHAUSTED"


@dataclass
class StrategyConfig:
    risk_per_trade_pct: float = 0.01          # 1% risk per trade
    min_rr_ratio: float = 1.0                 # Minimum 1:1 risk/reward to HOD
    ideal_rr_ratio: float = 2.0               # Ideal 2:1 risk/reward
    early_be_atr_buffer: float = 0.15         # Entry + 0.15 * ATR
    min_pullback_bars: int = 1                # 1-5 pullback candles
    max_pullback_bars: int = 5
    daily_max_loss: float = 200.0             # Daily maximum loss in dollars ($200 on $2,000 account)
    peak_profit_retrace_pct: float = 0.50     # 50% retrace from peak daily profit
    trading_cutoff_time: str = "10:00:00"     # Halt passed 10:00 AM EST
    topping_tail_wick_ratio: float = 0.50     # Upper wick >= 50% of bar range
    volume_divergence_ratio: float = 0.70     # Volume < 70% of prior volume on higher high
    ask_wall_ratio_threshold: float = 3.0     # Ask depth >= 3x bid depth
    iceberg_vol_mult: float = 2.0             # Volume >= 2x 20-bar avg with small displacement
    tape_selling_ratio_threshold: float = 0.65# Tape sell volume / total tape volume >= 65%
    support_tolerance_pct: float = 0.005      # 0.5% tolerance around EMA/VWAP support


@dataclass
class RossPosition:
    position_id: str
    symbol: str
    entry_price: float
    entry_time: Any
    initial_shares: int
    remaining_shares: int
    stop_loss: float
    hod_target: float
    atr_at_entry: float
    tp1_hit: bool = False
    realized_tp1_pnl: float = 0.0
    early_be_sl: float = 0.0
    closed: bool = False
    exit_time: Optional[Any] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None
    trades: List[Dict[str, Any]] = field(default_factory=list)


def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    """Calculate Exponential Moving Average."""
    return series.ewm(span=span, adjust=False).mean()


def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """Calculate Volume Weighted Average Price."""
    cum_vol = df['volume'].cumsum()
    cum_pv = (df['close'] * df['volume']).cumsum()
    # Avoid zero division
    return np.where(cum_vol > 0, cum_pv / cum_vol, df['close'])


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Average True Range (ATR)."""
    high = df['high']
    low = df['low']
    prev_close = df['close'].shift(1).fillna(df['open'])
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(window=period, min_periods=1).mean()


def enrich_ross_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich OHLCV dataframe with indicators needed for Ross Cameron strategy:
    - EMA9, EMA20, VWAP
    - ATR (14)
    - HOD (High of Day running maximum)
    - Candlestick body, upper wick, lower wick, and range
    """
    data = df.copy()
    data['ema9'] = calculate_ema(data['close'], 9)
    data['ema20'] = calculate_ema(data['close'], 20)
    data['vwap'] = calculate_vwap(data)
    data['atr'] = calculate_atr(data, 14)
    data['hod'] = data['high'].cummax()
    
    data['range'] = (data['high'] - data['low']).clip(lower=1e-5)
    data['upper_wick'] = data['high'] - data[['open', 'close']].max(axis=1)
    data['lower_wick'] = data[['open', 'close']].min(axis=1) - data['low']
    data['body'] = (data['close'] - data['open']).abs()
    data['vol_sma20'] = data['volume'].rolling(window=20, min_periods=1).mean()
    return data


def parse_time_to_time_obj(t_val: Any) -> datetime.time:
    """Parse string, Timestamp, or datetime to datetime.time."""
    if isinstance(t_val, datetime.time):
        return t_val
    if isinstance(t_val, (pd.Timestamp, datetime.datetime)):
        return t_val.time()
    if isinstance(t_val, str):
        # Handle formats like "10:00:00" or "2026-09-29 09:35:00"
        if " " in t_val:
            t_val = t_val.split(" ")[-1]
        parts = t_val.split(":")
        return datetime.time(int(parts[0]), int(parts[1]), int(float(parts[2])) if len(parts) > 2 else 0)
    raise ValueError(f"Cannot parse time from {t_val}")


class RossMomentumStrategy:
    """
    Implements Ross Cameron's 20-Year Momentum Strategy rules:
    - First Pullback Entry after vertical spike.
    - Sizing via Risk% and Stop Loss distance.
    - 50% TP1 halving at HOD with Early BE buffer.
    - 5 Level-2/Tape/Price Action Exit Signals.
    - 5 Walk-Away Rules.
    """

    def __init__(self, config: Optional[StrategyConfig] = None):
        self.config = config or StrategyConfig()
        self.daily_realized_pnl: float = 0.0
        self.peak_daily_profit: float = 0.0
        self.is_halted: bool = False
        self.halt_reason: Optional[WalkAwayReason] = None
        self.active_position: Optional[RossPosition] = None

    def reset_day(self):
        """Reset daily tracking state for a new trading session."""
        self.daily_realized_pnl = 0.0
        self.peak_daily_profit = 0.0
        self.is_halted = False
        self.halt_reason = None
        self.active_position = None

    def update_daily_pnl(self, realized_pnl_delta: float):
        """Update realized daily PnL and track peak profit."""
        self.daily_realized_pnl += realized_pnl_delta
        if self.daily_realized_pnl > self.peak_daily_profit:
            self.peak_daily_profit = self.daily_realized_pnl

    def check_walk_away_rules(
        self,
        current_time: Any,
        screener_has_valid_stocks: bool = True,
        market_momentum_exhausted: bool = False,
    ) -> Tuple[bool, Optional[WalkAwayReason]]:
        """
        Step 4: Check 5 Walk-Away Rules (Risk Control):
        1. Peak profit retraced by >= 50% -> halt for the day.
        2. Daily max loss hit -> halt for the day.
        3. Passed 10:00 AM EST -> halt for the day.
        4. Screener has no valid stocks -> stay in cash.
        5. Overall market momentum exhausted -> stop.
        """
        if self.is_halted:
            return True, self.halt_reason

        # Rule 1: Peak profit retraced by 50%
        if self.peak_daily_profit > 0.0:
            retrace_threshold = self.peak_daily_profit * (1.0 - self.config.peak_profit_retrace_pct)
            if self.daily_realized_pnl <= retrace_threshold:
                self.is_halted = True
                self.halt_reason = WalkAwayReason.PEAK_PROFIT_RETRACED
                return True, self.halt_reason

        # Rule 2: Daily max loss hit
        if self.daily_realized_pnl <= -abs(self.config.daily_max_loss):
            self.is_halted = True
            self.halt_reason = WalkAwayReason.DAILY_MAX_LOSS_HIT
            return True, self.halt_reason

        # Rule 3: Passed 10:00 AM EST
        try:
            curr_t = parse_time_to_time_obj(current_time)
            cutoff_t = parse_time_to_time_obj(self.config.trading_cutoff_time)
            if curr_t >= cutoff_t:
                self.is_halted = True
                self.halt_reason = WalkAwayReason.TIME_WINDOW_PASSED
                return True, self.halt_reason
        except Exception:
            pass

        # Rule 4: Screener has no valid stocks
        if not screener_has_valid_stocks:
            return True, WalkAwayReason.SCREENER_NO_VALID_STOCKS

        # Rule 5: Overall market momentum exhausted
        if market_momentum_exhausted:
            self.is_halted = True
            self.halt_reason = WalkAwayReason.MARKET_MOMENTUM_EXHAUSTED
            return True, self.halt_reason

        return False, None

    def evaluate_first_pullback_entry(
        self,
        df_history: pd.DataFrame,
        current_bar: pd.Series,
        prev_bar: pd.Series,
        account_equity: float,
        available_cash: float,
        current_time: Any,
        screener_has_valid_stocks: bool = True,
        market_momentum_exhausted: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Step 2: First Pullback Entry (首波回调突破):
        - Never chase initial vertical spike.
        - Wait for 1-5 pullback candles consolidating above key support (9EMA / 20EMA / VWAP).
        - Pullback low establishes initial Stop Loss (SL).
        - Trigger: The instant a candle breaks above the HIGH of the previous candle, enter immediately.
        - Risk/Reward check: Target is Day High (HOD). Must verify R/R >= 1:1, ideally >= 2:1.
        - Position Sizing: Risk = Account * Risk%, Shares = floor(Risk / (Entry - SL)).
        """
        # First check walk-away rules
        halted, reason = self.check_walk_away_rules(
            current_time=current_time,
            screener_has_valid_stocks=screener_has_valid_stocks,
            market_momentum_exhausted=market_momentum_exhausted,
        )
        if halted:
            return None

        # Already in position? One position at a time for Ross strategy
        if self.active_position is not None and not self.active_position.closed:
            return None

        # Check breakout of previous candle high: instant trigger
        # If current_bar['high'] <= prev_bar['high'], breakout hasn't triggered yet
        if current_bar['high'] <= prev_bar['high']:
            return None

        # Determine pullback sequence prior to the trigger
        # We look back 1 to 5 bars from prev_bar
        if len(df_history) < 2:
            return None

        # Look back from prev_bar to find the pullback consolidation
        # We need at least min_pullback_bars (1) and up to max_pullback_bars (5)
        # Pullback bars are consecutive bars before current_bar that pulled back after a spike
        pullback_bars = []
        spike_found = False
        spike_high = 0.0

        history_len = len(df_history)
        # Look for the surge/spike peak in recent history (up to max_pullback_bars + 3 bars back)
        lookback_window = min(self.config.max_pullback_bars + 3, history_len)
        recent_slice = df_history.iloc[-lookback_window:]
        
        # Find the index of the highest high in the recent window
        spike_rel_idx = recent_slice['high'].values.argmax()
        spike_abs_idx = history_len - lookback_window + spike_rel_idx

        # Number of pullback bars between spike candle and prev_bar
        # (spike_abs_idx is the spike candle; prev_bar is at history_len - 1)
        pullback_count = (history_len - 1) - spike_abs_idx

        if pullback_count < self.config.min_pullback_bars or pullback_count > self.config.max_pullback_bars:
            # Pullback candle count must be strictly between 1 and 5
            return None

        pullback_bars = df_history.iloc[spike_abs_idx + 1:]
        spike_candle = df_history.iloc[spike_abs_idx]
        spike_high = float(spike_candle['high'])

        # Verify that all pullback bars have highs below or equal to the spike high
        if pullback_bars['high'].max() > spike_high:
            return None

        # Verify pullback consolidation above key support (9EMA / 20EMA / VWAP)
        # Check against support values on the pullback bars
        ema9 = prev_bar.get('ema9')
        ema20 = prev_bar.get('ema20')
        vwap = prev_bar.get('vwap')
        key_supports = [s for s in [ema9, ema20, vwap] if pd.notnull(s) and s > 0]
        if not key_supports:
            key_supports = [prev_bar['close'] * 0.95]

        # Support level is the lowest of the key supports (as long as it's a realistic base)
        support_level = min(key_supports)

        # Pullback low must be consolidating above support (or within support tolerance)
        pullback_low = float(pullback_bars['low'].min())
        tolerance = support_level * self.config.support_tolerance_pct
        if pullback_low < (support_level - tolerance):
            # Broke support, invalid pullback
            return None

        # Trigger price: instant breakout above prev_bar high
        # In live market, fill is prev_bar.high + 0.01 (tick) or current open if gapped
        entry_price = round(float(prev_bar['high'] + 0.01), 2)
        if current_bar['open'] > entry_price:
            entry_price = round(float(current_bar['open']), 2)

        # Pullback low establishes initial Stop Loss (SL)
        stop_loss = round(pullback_low - 0.01, 2)
        per_share_risk = entry_price - stop_loss

        if per_share_risk <= 0.005:
            # Invalid SL (too tight or inverted)
            return None

        # Target is Day High (HOD)
        hist_hod = df_history['hod'].iloc[-1] if 'hod' in df_history.columns else df_history['high'].max()
        hod_target = round(float(max(spike_high, hist_hod)), 2)
        reward = hod_target - entry_price

        # Risk/Reward check: R/R >= min_rr_ratio (1:1)
        rr_ratio = reward / per_share_risk
        if rr_ratio < self.config.min_rr_ratio:
            # Reject trade: insufficient R/R to HOD
            return None

        # Position Sizing: Risk = Account * Risk%, Shares = floor(Risk / (Entry - SL))
        risk_dollar = account_equity * self.config.risk_per_trade_pct
        shares_by_risk = math.floor(risk_dollar / per_share_risk)

        # Constrain by cash buying power
        shares_by_cash = math.floor(available_cash / entry_price) if entry_price > 0 else 0
        shares = min(shares_by_risk, shares_by_cash)

        if shares < 1:
            return None

        atr = float(prev_bar.get('atr', per_share_risk))

        return {
            "trigger_price": entry_price,
            "stop_loss": stop_loss,
            "hod_target": hod_target,
            "shares": shares,
            "rr_ratio": rr_ratio,
            "atr": atr,
            "per_share_risk": per_share_risk,
            "pullback_low": pullback_low,
            "pullback_bars_count": len(pullback_bars),
            "support_level": support_level,
        }

    def check_exit_signals(
        self,
        current_bar: pd.Series,
        prev_bar: Optional[pd.Series],
        position: RossPosition,
        level2_data: Optional[Dict[str, Any]] = None,
        tape_data: Optional[Dict[str, Any]] = None,
    ) -> Tuple[ExitSignalType, float, str]:
        """
        Step 3: Exit & 5 Exit Signals:
        - At Day High (HOD): Conservatively sell 50% (TP1), move Stop Loss to breakeven buffer (Entry + 0.15 ATR).
        - Exit remainder on any of the 5 Exit Signals:
          1. Big Ask Wall (Level 2 resistance wall).
          2. Hidden Iceberg seller (Heavy volume absorption without upward movement).
          3. Tape selling (Time & Sales aggressive hitting bid, bid stepping down).
          4. Candlestick topping tail / long upper wick (exhaustion candle).
          5. Volume divergence (price prints higher high on fading volume).
        - Full stop loss if price <= position.stop_loss.
        """
        high = float(current_bar['high'])
        low = float(current_bar['low'])
        close = float(current_bar['close'])
        open_px = float(current_bar['open'])
        volume = float(current_bar['volume'])

        # 0. Check Stop Loss first (or trailing BE stop)
        if low <= position.stop_loss:
            return ExitSignalType.STOP_LOSS, position.stop_loss, f"Hit Stop Loss at {position.stop_loss}"

        # 0. Check TP1 at HOD (if not hit yet)
        if not position.tp1_hit and high >= position.hod_target:
            return ExitSignalType.TAKE_PROFIT_1, position.hod_target, f"Hit TP1 (HOD) at {position.hod_target}"

        # Check the 5 Exit Signals (for the runner position after TP1, or prior if severe exhaustion)
        # Signal 1: Big Ask Wall (Level 2 resistance wall)
        if level2_data:
            ask_wall_ratio = level2_data.get('ask_wall_ratio', 1.0)
            ask_wall_detected = level2_data.get('ask_wall_detected', False)
            if ask_wall_detected or ask_wall_ratio >= self.config.ask_wall_ratio_threshold:
                return ExitSignalType.BIG_ASK_WALL, close, f"Big Ask Wall detected (ratio={ask_wall_ratio:.2f})"

        # Signal 2: Hidden Iceberg seller (Heavy volume absorption without upward movement)
        vol_sma20 = float(current_bar.get('vol_sma20', volume))
        bar_range = max(1e-5, high - low)
        atr = position.atr_at_entry
        iceberg_flag = False
        if level2_data and level2_data.get('iceberg_detected', False):
            iceberg_flag = True
        elif volume >= (self.config.iceberg_vol_mult * vol_sma20) and bar_range <= (0.30 * atr) and close <= open_px:
            iceberg_flag = True

        if iceberg_flag:
            return ExitSignalType.HIDDEN_ICEBERG, close, f"Hidden Iceberg seller detected (vol={volume:.0f} vs avg={vol_sma20:.0f})"

        # Signal 3: Tape selling (Time & Sales aggressive hitting bid, bid stepping down)
        if tape_data:
            tape_sell_ratio = tape_data.get('tape_sell_ratio', 0.0)
            bid_stepping_down = tape_data.get('bid_stepping_down', False)
            if bid_stepping_down or tape_sell_ratio >= self.config.tape_selling_ratio_threshold:
                return ExitSignalType.TAPE_SELLING, close, f"Tape selling detected (sell_ratio={tape_sell_ratio:.2f})"

        # Signal 4: Candlestick topping tail / long upper wick (exhaustion candle)
        upper_wick = high - max(open_px, close)
        if bar_range >= (0.40 * atr) and (upper_wick / bar_range) >= self.config.topping_tail_wick_ratio:
            return ExitSignalType.TOPPING_TAIL, close, f"Topping tail exhaustion candle (wick_ratio={upper_wick / bar_range:.2f})"

        # Signal 5: Volume divergence (price prints higher high on fading volume)
        if prev_bar is not None:
            prev_high = float(prev_bar['high'])
            prev_vol = float(prev_bar['volume'])
            if high > prev_high and prev_vol > 0:
                if volume < (prev_vol * self.config.volume_divergence_ratio):
                    return ExitSignalType.VOLUME_DIVERGENCE, close, f"Volume divergence (vol={volume:.0f} vs prev_vol={prev_vol:.0f})"

        return ExitSignalType.NONE, 0.0, ""
