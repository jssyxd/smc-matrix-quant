"""
Alpaca US Equities Data Loader for Ross Cameron Momentum Strategy.
Fetches and caches 1-minute and 5-minute historical bars from Alpaca Market Data API.
Filters trading windows specifically for US pre-market (07:00-09:30 EST) and regular hours (09:30-16:00 EST).
"""

import os
import json
import urllib.request
import pandas as pd
import numpy as np
from datetime import datetime, time, timezone
from typing import Dict, List, Optional, Union

ALPACA_DATA_URL = "https://data.alpaca.markets/v2/stocks/bars"
API_KEY = os.environ.get("APCA_API_KEY_ID", "PKP5X2XV6XX3CQJZIH3XNIUJUC")
SECRET_KEY = os.environ.get("APCA_API_SECRET_KEY", "FeSjzoYJBizCbfJ9tCnjCcTmGuDVZZGpNZdBZaqSuTxN")


def fetch_alpaca_bars(
    symbol: str,
    timeframe: str = "1Min",
    start: str = "2026-09-18T07:00:00Z",
    end: str = "2026-09-18T16:00:00Z",
    limit: int = 1000,
    feed: str = "iex",
) -> pd.DataFrame:
    """Fetch raw bars from Alpaca Data API."""
    url = f"{ALPACA_DATA_URL}?symbols={symbol}&timeframe={timeframe}&start={start}&end={end}&limit={limit}&feed={feed}"
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY,
        "User-Agent": "AlpacaRossDataLoader/1.0"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return pd.DataFrame()

    bars = data.get("bars", {}).get(symbol, [])
    if not bars:
        return pd.DataFrame()

    df = pd.DataFrame(bars)
    df = df.rename(columns={
        "t": "timestamp",
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "v": "volume",
        "vw": "vwap",
        "n": "trades_count"
    })
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()
    return df


def filter_trading_window(
    df: pd.DataFrame,
    start_time: str = "07:00:00",
    end_time: str = "10:00:00",
    tz_convert: str = "America/New_York",
) -> pd.DataFrame:
    """
    Filter DataFrame for Ross Cameron's golden morning trading window (07:00 - 10:00 AM EST).
    """
    if df.empty:
        return df
    
    # Ensure localized
    if df.index.tz is None:
        df = df.tz_localize("UTC")
    df_ny = df.tz_convert(tz_convert)
    
    start_t = datetime.strptime(start_time, "%H:%M:%S").time()
    end_t = datetime.strptime(end_time, "%H:%M:%S").time()
    
    mask = (df_ny.index.time >= start_t) & (df_ny.index.time <= end_t)
    return df_ny[mask]
