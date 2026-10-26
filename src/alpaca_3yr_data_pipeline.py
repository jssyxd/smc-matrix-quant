"""
Alpaca 3-Year Data Pipeline (2021-2023) for Ross Cameron Momentum Day-Trading.
Provides data acquisition, pagination, and local Parquet/CSV caching for:
1. Daily bars for universe stocks (MARA, RIOT, GME, SOUN, PLTR, CVNA, LCID, AFRM) from 2021-01-01 to 2023-12-31.
2. Intraday (1-minute and 5-minute) bars for candidate momentum stocks on identified breakout days.
3. Disk caching in `data/alpaca_cache/` ensuring zero redundant API calls.
"""

import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
import pandas as pd
import numpy as np

# Alpaca API configuration & credentials
ALPACA_DATA_URL = "https://data.alpaca.markets/v2/stocks/bars"
API_KEY = os.environ.get("APCA_API_KEY_ID", "PKP5X2XV6XX3CQJZIH3XNIUJUC")
SECRET_KEY = os.environ.get("APCA_API_SECRET_KEY", "FeSjzoYJBizCbfJ9tCnjCcTmGuDVZZGpNZdBZaqSuTxN")
DEFAULT_FEED = "iex"

# Target universe for 3-year momentum screening
DEFAULT_UNIVERSE = ["MARA", "RIOT", "GME", "SOUN", "PLTR", "CVNA", "LCID", "AFRM"]
DEFAULT_START_DATE = "2021-01-01"
DEFAULT_END_DATE = "2023-12-31"
DEFAULT_CACHE_DIR = "data/alpaca_cache"


def get_cache_filepath(
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
    cache_dir: str = DEFAULT_CACHE_DIR,
    file_format: str = "parquet",
) -> Path:
    """Generate deterministic cache file path for given symbol and date range."""
    # Sanitize dates for filename
    s_clean = start_date.split("T")[0].replace("-", "")
    e_clean = end_date.split("T")[0].replace("-", "")
    tf_clean = timeframe.lower().replace(" ", "")
    filename = f"{symbol.upper()}_{tf_clean}_{s_clean}_{e_clean}.{file_format}"
    return Path(cache_dir) / filename


def save_to_cache(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    file_format: str = "parquet",
) -> Path:
    """Save DataFrame to cache (Parquet preferred, CSV supported)."""
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    
    if df.empty:
        # Create empty DataFrame with expected columns and datetime index
        df = pd.DataFrame(
            columns=["open", "high", "low", "close", "volume", "vwap", "trades_count"],
            index=pd.DatetimeIndex([], name="timestamp")
        )

    if file_format == "parquet":
        try:
            df.to_parquet(p)
            return p
        except Exception as e:
            # Fallback to CSV if parquet engine error
            csv_path = p.with_suffix(".csv")
            df.to_csv(csv_path)
            return csv_path
    else:
        csv_path = p.with_suffix(".csv")
        df.to_csv(csv_path)
        return csv_path


def load_from_cache(filepath: Union[str, Path]) -> Optional[pd.DataFrame]:
    """Load DataFrame from cache file, restoring DatetimeIndex."""
    p = Path(filepath)
    if not p.exists():
        # Check alternative formats
        if p.suffix == ".parquet" and p.with_suffix(".csv").exists():
            p = p.with_suffix(".csv")
        elif p.suffix == ".csv" and p.with_suffix(".parquet").exists():
            p = p.with_suffix(".parquet")
        else:
            return None

    try:
        if p.suffix == ".parquet":
            df = pd.read_parquet(p)
        else:
            df = pd.read_csv(p, index_col=0, parse_dates=True)
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index)
            df.index.name = "timestamp"
            
        if not df.empty and isinstance(df.index, pd.DatetimeIndex):
            df = df.sort_index()
        return df
    except Exception:
        return None


def fetch_alpaca_raw_page(
    symbol: str,
    timeframe: str,
    start: str,
    end: str,
    limit: int = 10000,
    feed: str = DEFAULT_FEED,
    page_token: Optional[str] = None,
    api_key: str = API_KEY,
    secret_key: str = SECRET_KEY,
    timeout: int = 15,
) -> Dict[str, Any]:
    """Fetch single page of raw bars from Alpaca Data API v2."""
    params = [
        f"symbols={symbol.upper()}",
        f"timeframe={timeframe}",
        f"start={start}",
        f"end={end}",
        f"limit={limit}",
        f"feed={feed}",
    ]
    if page_token:
        params.append(f"page_token={page_token}")
        
    url = f"{ALPACA_DATA_URL}?{'&'.join(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key,
            "User-Agent": "Alpaca3YrDataPipeline/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_alpaca_bars_to_df(bars: List[Dict[str, Any]]) -> pd.DataFrame:
    """Parse raw Alpaca bar dictionaries into standardized DatetimeIndex DataFrame."""
    if not bars:
        return pd.DataFrame(
            columns=["open", "high", "low", "close", "volume", "vwap", "trades_count"],
            index=pd.DatetimeIndex([], name="timestamp")
        )
    df = pd.DataFrame(bars)
    df = df.rename(
        columns={
            "t": "timestamp",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
            "vw": "vwap",
            "n": "trades_count",
        }
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()
    # Ensure standard numeric types
    for col in ["open", "high", "low", "close", "volume", "vwap", "trades_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def fetch_alpaca_bars_with_pagination(
    symbol: str,
    timeframe: str,
    start: str,
    end: str,
    feed: str = DEFAULT_FEED,
    api_key: str = API_KEY,
    secret_key: str = SECRET_KEY,
    max_retries: int = 3,
    retry_delay: float = 1.0,
) -> pd.DataFrame:
    """
    Fetch all historical bars for symbol across date range, following page_tokens.
    """
    all_bars = []
    page_token = None
    
    # Format ISO 8601 timestamps
    start_iso = start if "T" in start else f"{start}T00:00:00Z"
    end_iso = end if "T" in end else f"{end}T23:59:59Z"

    while True:
        data = None
        for attempt in range(max_retries):
            try:
                data = fetch_alpaca_raw_page(
                    symbol=symbol,
                    timeframe=timeframe,
                    start=start_iso,
                    end=end_iso,
                    feed=feed,
                    page_token=page_token,
                    api_key=api_key,
                    secret_key=secret_key,
                )
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:  # Rate limit
                    time.sleep(retry_delay * (2 ** attempt))
                else:
                    if attempt == max_retries - 1:
                        data = {}
                    else:
                        time.sleep(retry_delay)
            except Exception:
                if attempt == max_retries - 1:
                    data = {}
                else:
                    time.sleep(retry_delay)

        if not data:
            break

        bars = data.get("bars", {}).get(symbol.upper(), [])
        if bars:
            all_bars.extend(bars)

        page_token = data.get("next_page_token")
        if not page_token:
            break

    return parse_alpaca_bars_to_df(all_bars)


def fetch_daily_bars(
    symbol: str,
    start_date: str = DEFAULT_START_DATE,
    end_date: str = DEFAULT_END_DATE,
    cache_dir: str = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
    force_refresh: bool = False,
    file_format: str = "parquet",
    feed: str = DEFAULT_FEED,
    api_key: str = API_KEY,
    secret_key: str = SECRET_KEY,
) -> pd.DataFrame:
    """
    Fetch and cache daily bars for a given symbol from start_date to end_date.
    Checks disk cache first. If cache miss or force_refresh, fetches from Alpaca API.
    """
    cache_path = get_cache_filepath(
        symbol=symbol,
        timeframe="1Day",
        start_date=start_date,
        end_date=end_date,
        cache_dir=cache_dir,
        file_format=file_format,
    )

    if use_cache and not force_refresh:
        cached_df = load_from_cache(cache_path)
        if cached_df is not None and not cached_df.empty:
            return cached_df

    # Fetch from API
    df = fetch_alpaca_bars_with_pagination(
        symbol=symbol,
        timeframe="1Day",
        start=start_date,
        end=end_date,
        feed=feed,
        api_key=api_key,
        secret_key=secret_key,
    )

    # Save to disk cache
    if not df.empty and use_cache:
        save_to_cache(df, cache_path, file_format=file_format)

    return df


def fetch_universe_daily_bars(
    symbols: List[str] = DEFAULT_UNIVERSE,
    start_date: str = DEFAULT_START_DATE,
    end_date: str = DEFAULT_END_DATE,
    cache_dir: str = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
    force_refresh: bool = False,
    file_format: str = "parquet",
    feed: str = DEFAULT_FEED,
    api_key: str = API_KEY,
    secret_key: str = SECRET_KEY,
) -> Dict[str, pd.DataFrame]:
    """
    Fetch and cache daily bars for all universe stocks from start_date to end_date.
    Returns dictionary mapping symbol -> daily DataFrame.
    """
    universe_data = {}
    for sym in symbols:
        df = fetch_daily_bars(
            symbol=sym,
            start_date=start_date,
            end_date=end_date,
            cache_dir=cache_dir,
            use_cache=use_cache,
            force_refresh=force_refresh,
            file_format=file_format,
            feed=feed,
            api_key=api_key,
            secret_key=secret_key,
        )
        universe_data[sym.upper()] = df
    return universe_data


def fetch_intraday_bars(
    symbol: str,
    date: str,
    timeframe: str = "5Min",
    cache_dir: str = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
    force_refresh: bool = False,
    file_format: str = "parquet",
    feed: str = DEFAULT_FEED,
    api_key: str = API_KEY,
    secret_key: str = SECRET_KEY,
) -> pd.DataFrame:
    """
    Fetch and cache intraday (5-minute or 1-minute) bars for candidate symbol on a specific date.
    Checks disk cache in `data/alpaca_cache/` first to eliminate redundant API calls.
    """
    # Extract date string YYYY-MM-DD
    date_str = date.split("T")[0]
    start_iso = f"{date_str}T00:00:00Z"
    end_iso = f"{date_str}T23:59:59Z"

    cache_path = get_cache_filepath(
        symbol=symbol,
        timeframe=timeframe,
        start_date=date_str,
        end_date=date_str,
        cache_dir=cache_dir,
        file_format=file_format,
    )

    if use_cache and not force_refresh:
        cached_df = load_from_cache(cache_path)
        if cached_df is not None and not cached_df.empty:
            return cached_df

    # Fetch from Alpaca
    df = fetch_alpaca_bars_with_pagination(
        symbol=symbol,
        timeframe=timeframe,
        start=start_iso,
        end=end_iso,
        feed=feed,
        api_key=api_key,
        secret_key=secret_key,
    )

    if not df.empty and use_cache:
        save_to_cache(df, cache_path, file_format=file_format)

    return df


def fetch_candidate_intraday_data(
    candidates: List[Dict[str, Any]],
    timeframe: str = "5Min",
    cache_dir: str = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
    force_refresh: bool = False,
    file_format: str = "parquet",
) -> Dict[str, pd.DataFrame]:
    """
    Batch fetch intraday bars for all screened candidate breakout days.
    candidates list contains elements with 'symbol' and 'date'.
    Returns mapping of "{symbol}_{date}" -> intraday DataFrame.
    """
    intraday_data = {}
    for cand in candidates:
        symbol = cand.get("symbol", "").upper()
        date = cand.get("date", "")
        if not symbol or not date:
            continue
        date_str = str(date).split("T")[0].split(" ")[0]
        key = f"{symbol}_{date_str}"
        df = fetch_intraday_bars(
            symbol=symbol,
            date=date_str,
            timeframe=timeframe,
            cache_dir=cache_dir,
            use_cache=use_cache,
            force_refresh=force_refresh,
            file_format=file_format,
        )
        intraday_data[key] = df
    return intraday_data


class Alpaca3YrDataPipeline:
    """
    Object-oriented harness for 3-year Alpaca data fetching, caching, and retrieval.
    """
    def __init__(
        self,
        symbols: List[str] = DEFAULT_UNIVERSE,
        start_date: str = DEFAULT_START_DATE,
        end_date: str = DEFAULT_END_DATE,
        cache_dir: str = DEFAULT_CACHE_DIR,
        file_format: str = "parquet",
        feed: str = DEFAULT_FEED,
        api_key: str = API_KEY,
        secret_key: str = SECRET_KEY,
    ):
        self.symbols = [s.upper() for s in symbols]
        self.start_date = start_date
        self.end_date = end_date
        self.cache_dir = cache_dir
        self.file_format = file_format
        self.feed = feed
        self.api_key = api_key
        self.secret_key = secret_key
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

    def fetch_all_daily(self, force_refresh: bool = False) -> Dict[str, pd.DataFrame]:
        """Fetch and cache daily bars for all configured universe symbols."""
        return fetch_universe_daily_bars(
            symbols=self.symbols,
            start_date=self.start_date,
            end_date=self.end_date,
            cache_dir=self.cache_dir,
            use_cache=True,
            force_refresh=force_refresh,
            file_format=self.file_format,
            feed=self.feed,
            api_key=self.api_key,
            secret_key=self.secret_key,
        )

    def fetch_candidate_intraday(
        self,
        candidates: List[Dict[str, Any]],
        timeframe: str = "5Min",
        force_refresh: bool = False,
    ) -> Dict[str, pd.DataFrame]:
        """Fetch and cache intraday bars for screened momentum candidate days."""
        return fetch_candidate_intraday_data(
            candidates=candidates,
            timeframe=timeframe,
            cache_dir=self.cache_dir,
            use_cache=True,
            force_refresh=force_refresh,
            file_format=self.file_format,
        )
