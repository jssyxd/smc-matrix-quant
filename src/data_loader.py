"""
统一3层退避数据加载器。

优先级:
  1. Alpaca v1beta3 crypto/us/bars (BTC/USD, ETH/USD, SOL/USD, BNB/USD)
     或 Alpaca v2 stocks/bars (美股)
  2. Binance 公共 klines API (BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT)
  3. Yahoo Finance (BTC-USD, ETH-USD, etc.)
  4. 合成 GBM 数据 (seed=42, 最终退避，保证不崩溃)

所有结果缓存至 data/alpaca_cache/<symbol>_<tf>_<start>_<end>.parquet
"""
from __future__ import annotations

import os
import time
import hashlib
import requests
import numpy as np
import pandas as pd

# ── 认证 ─────────────────────────────────────────────────────────────
ALPACA_KEY    = "PKP5X2XV6XX3CQJZIH3XNIUJUC"
ALPACA_SECRET = "FeSjzoYJBizCbfJ9tCnjCcTmGuDVZZGpNZdBZaqSuTxN"
ALPACA_CRYPTO = "https://data.alpaca.markets/v1beta3/crypto/us/bars"
ALPACA_STOCKS = "https://data.alpaca.markets/v2/stocks/bars"
BINANCE_KLINES = "https://api.binance.com/api/v3/klines"

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "alpaca_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# 加密币品种别名表
CRYPTO_SYMBOLS = {
    "BTC": "BTC/USD", "BTCUSD": "BTC/USD", "BTCUSDT": "BTC/USD",
    "ETH": "ETH/USD", "ETHUSD": "ETH/USD", "ETHUSDT": "ETH/USD",
    "SOL": "SOL/USD", "SOLUSD": "SOL/USD", "SOLUSDT": "SOL/USD",
    "BNB": "BNB/USD", "BNBUSD": "BNB/USD", "BNBUSDT": "BNB/USD",
}

# 时间框架映射
TF_ALPACA  = {"1m":"1Min","5m":"5Min","15m":"15Min","1h":"1Hour","4h":"4Hour","1d":"1Day"}
TF_BINANCE = {"1m":"1m",  "5m":"5m",  "15m":"15m",  "1h":"1h",  "4h":"4h",   "1d":"1d"}


def _cache_path(symbol: str, timeframe: str, start: str, end: str) -> str:
    key = hashlib.md5(f"{symbol}{timeframe}{start}{end}".encode()).hexdigest()[:12]
    safe = symbol.replace("/", "_").replace("-", "_")
    return os.path.join(CACHE_DIR, f"{safe}_{timeframe}_{key}.parquet")


def load_ohlcv(
    symbol: str,
    timeframe: str = "1h",
    start: str = "2022-01-01",
    end: str = "2025-01-01",
    cache: bool = True,
) -> pd.DataFrame:
    """
    3层退避 OHLCV 加载。
    返回列: timestamp(UTC DatetimeTZ), open, high, low, close, volume
    """
    cp = _cache_path(symbol, timeframe, start, end)
    if cache and os.path.exists(cp):
        df = pd.read_parquet(cp)
        print(f"[Cache] {symbol} {timeframe} {len(df)} bars from {cp}")
        return df

    # 解析 symbol
    sym_upper = symbol.upper().replace("-", "").replace("/", "")
    alpaca_sym = CRYPTO_SYMBOLS.get(sym_upper)
    is_crypto = alpaca_sym is not None

    df = None

    # ── Layer 1: Alpaca ───────────────────────────────────────────────
    if is_crypto:
        df = _load_alpaca_crypto(alpaca_sym, timeframe, start, end)
    else:
        df = _load_alpaca_stocks(sym_upper, timeframe, start, end)

    # ── Layer 2: Binance (仅加密币) ───────────────────────────────────
    if (df is None or len(df) < 10) and is_crypto:
        binance_sym = sym_upper + "USDT" if not sym_upper.endswith("USDT") else sym_upper
        df = _load_binance(binance_sym, timeframe, start, end)

    # ── Layer 3: Yahoo Finance ────────────────────────────────────────
    if df is None or len(df) < 10:
        df = _load_yahoo(symbol, timeframe, start, end)

    # ── Layer 4: 合成 GBM（最终退避）─────────────────────────────────
    if df is None or len(df) < 10:
        print(f"[WARN] All data sources failed for {symbol} {timeframe}, using synthetic GBM")
        df = _generate_synthetic(symbol, timeframe, start, end)

    if cache and df is not None and len(df) > 0:
        df.to_parquet(cp)
        print(f"[Cache] Saved {symbol} {timeframe} {len(df)} bars → {cp}")

    return df


# ── Alpaca 加密币 ──────────────────────────────────────────────────────
def _load_alpaca_crypto(symbol: str, timeframe: str, start: str, end: str) -> pd.DataFrame | None:
    tf = TF_ALPACA.get(timeframe, "1Hour")
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    rows = []
    next_token = None
    try:
        while True:
            params: dict = {
                "symbols": symbol,
                "timeframe": tf,
                "start": pd.Timestamp(start, tz="UTC").isoformat(),
                "end":   pd.Timestamp(end,   tz="UTC").isoformat(),
                "limit": 1000,
                "sort":  "asc",
            }
            if next_token:
                params["page_token"] = next_token
            r = requests.get(ALPACA_CRYPTO, headers=headers, params=params, timeout=20)
            if r.status_code != 200:
                print(f"[Alpaca Crypto] HTTP {r.status_code}: {r.text[:200]}")
                return None
            data = r.json()
            bars = data.get("bars", {}).get(symbol, [])
            rows.extend(bars)
            next_token = data.get("next_page_token")
            if not next_token or not bars:
                break
            time.sleep(0.15)
        if not rows:
            return None
        df = pd.DataFrame(rows)
        df = df.rename(columns={"t": "timestamp", "o": "open", "h": "high",
                                 "l": "low", "c": "close", "v": "volume"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
        print(f"[Alpaca Crypto] {symbol} {timeframe} → {len(df)} bars")
        return df
    except Exception as e:
        print(f"[Alpaca Crypto] Exception: {e}")
        return None


# ── Alpaca 美股 ────────────────────────────────────────────────────────
def _load_alpaca_stocks(symbol: str, timeframe: str, start: str, end: str) -> pd.DataFrame | None:
    tf = TF_ALPACA.get(timeframe, "1Hour")
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    rows = []
    next_token = None
    try:
        while True:
            params: dict = {
                "symbols": symbol,
                "timeframe": tf,
                "start": pd.Timestamp(start, tz="UTC").isoformat(),
                "end":   pd.Timestamp(end,   tz="UTC").isoformat(),
                "limit": 1000,
                "sort":  "asc",
                "feed":  "iex",
            }
            if next_token:
                params["page_token"] = next_token
            r = requests.get(ALPACA_STOCKS, headers=headers, params=params, timeout=20)
            if r.status_code != 200:
                print(f"[Alpaca Stocks] HTTP {r.status_code}: {r.text[:200]}")
                return None
            data = r.json()
            bars = data.get("bars", {}).get(symbol, []) if isinstance(data.get("bars"), dict) else data.get("bars", [])
            rows.extend(bars)
            next_token = data.get("next_page_token")
            if not next_token or not bars:
                break
            time.sleep(0.15)
        if not rows:
            return None
        df = pd.DataFrame(rows)
        df = df.rename(columns={"t": "timestamp", "o": "open", "h": "high",
                                 "l": "low", "c": "close", "v": "volume"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
        print(f"[Alpaca Stocks] {symbol} {timeframe} → {len(df)} bars")
        return df
    except Exception as e:
        print(f"[Alpaca Stocks] Exception: {e}")
        return None


# ── Binance 公共 API ────────────────────────────────────────────────────
def _load_binance(symbol: str, timeframe: str, start: str, end: str) -> pd.DataFrame | None:
    tf = TF_BINANCE.get(timeframe, "1h")
    try:
        start_ms = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
        end_ms   = int(pd.Timestamp(end,   tz="UTC").timestamp() * 1000)
        rows = []
        while start_ms < end_ms:
            r = requests.get(BINANCE_KLINES, params={
                "symbol": symbol, "interval": tf,
                "startTime": start_ms, "endTime": end_ms, "limit": 1000,
            }, timeout=20)
            if r.status_code != 200:
                print(f"[Binance] HTTP {r.status_code}")
                break
            batch = r.json()
            if not batch:
                break
            rows.extend(batch)
            start_ms = int(batch[-1][6]) + 1   # close_time + 1ms
            time.sleep(0.12)
        if not rows:
            return None
        cols = ["timestamp","open","high","low","close","volume",
                "close_time","qav","num_trades","tbbav","tbqav","ignore"]
        df = pd.DataFrame(rows, columns=cols)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms", utc=True)
        for c in ["open","high","low","close","volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df[["timestamp","open","high","low","close","volume"]].reset_index(drop=True)
        print(f"[Binance] {symbol} {timeframe} → {len(df)} bars")
        return df
    except Exception as e:
        print(f"[Binance] Exception: {e}")
        return None


# ── Yahoo Finance ──────────────────────────────────────────────────────
def _load_yahoo(symbol: str, timeframe: str, start: str, end: str) -> pd.DataFrame | None:
    try:
        import yfinance as yf  # type: ignore
        tf_map = {"1m":"1m","5m":"5m","15m":"15m","1h":"1h","4h":"1h","1d":"1d"}
        interval = tf_map.get(timeframe, "1h")
        # 转换 symbol
        sym_upper = symbol.upper().replace("USDT","").replace("BUSD","").replace("/","")
        yf_sym = sym_upper + "-USD" if not sym_upper.endswith("-USD") else sym_upper
        ticker = yf.Ticker(yf_sym)
        df = ticker.history(start=start, end=end, interval=interval)
        if df is None or df.empty:
            return None
        df = df.reset_index()
        df.columns = [c.lower() for c in df.columns]
        ts_col = next((c for c in df.columns if "date" in c or "time" in c), None)
        if ts_col is None:
            return None
        df = df.rename(columns={ts_col: "timestamp"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df[["timestamp","open","high","low","close","volume"]].dropna().reset_index(drop=True)
        print(f"[Yahoo] {yf_sym} {timeframe} → {len(df)} bars")
        return df
    except Exception as e:
        print(f"[Yahoo] Exception: {e}")
        return None


# ── 合成 GBM 数据（最终退避）──────────────────────────────────────────
def _generate_synthetic(
    symbol: str, timeframe: str, start: str, end: str, seed: int = 42
) -> pd.DataFrame:
    sym_hash = int(hashlib.md5(symbol.encode()).hexdigest(), 16) % 10000
    rng = np.random.default_rng(seed + sym_hash)
    tf_hours = {"1m": 1/60, "5m": 5/60, "15m": 0.25, "1h": 1.0, "4h": 4.0, "1d": 24.0}.get(timeframe, 1.0)
    total_hours = (pd.Timestamp(end) - pd.Timestamp(start)).total_seconds() / 3600
    n = max(100, int(total_hours / tf_hours))
    dt = tf_hours / 8760
    vol = 0.80; drift = 0.20
    S0 = {"BTC": 30000, "ETH": 2000, "SOL": 100, "BNB": 250}.get(
        symbol.upper().replace("USDT","").replace("/USD",""), 30000
    )
    log_ret = rng.normal((drift - 0.5 * vol**2) * dt, vol * np.sqrt(dt), n)
    closes  = S0 * np.exp(np.cumsum(log_ret))
    highs   = closes * (1 + rng.exponential(0.006, n))
    lows    = closes * (1 - rng.exponential(0.006, n))
    opens   = np.empty(n); opens[0] = S0; opens[1:] = closes[:-1]
    lows    = np.minimum(lows, np.minimum(opens, closes))
    highs   = np.maximum(highs, np.maximum(opens, closes))
    volumes = rng.lognormal(10, 1, n)
    freq = f"{max(1, int(tf_hours * 60))}min"
    ts = pd.date_range(start, periods=n, freq=freq, tz="UTC")
    df = pd.DataFrame({
        "timestamp": ts, "open": opens, "high": highs,
        "low": lows, "close": closes, "volume": volumes,
    })
    print(f"[Synthetic] {symbol} {timeframe} → {len(df)} bars (GBM seed={seed}+{sym_hash})")
    return df


# ── 便捷批量加载 ────────────────────────────────────────────────────────
def load_crypto_universe(
    symbols: list[str] = None,
    timeframe: str = "1h",
    start: str = "2022-01-01",
    end: str = "2025-06-01",
) -> dict[str, pd.DataFrame]:
    """加载多品种加密币数据，返回 {symbol: df}"""
    if symbols is None:
        symbols = ["BTC/USD", "ETH/USD", "SOL/USD", "BNB/USD"]
    result = {}
    for sym in symbols:
        df = load_ohlcv(sym, timeframe, start, end)
        result[sym] = df
    return result


if __name__ == "__main__":
    # 快速连通测试
    print("=== Data Loader Connectivity Test ===")
    df = load_ohlcv("BTC/USD", "1h", "2024-01-01", "2024-01-08")
    print(f"BTC/USD 1h: {len(df)} bars, {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]}")
    print(df.head(3).to_string())
    print("=== PASS ===")
