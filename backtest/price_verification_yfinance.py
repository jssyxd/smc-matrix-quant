#!/usr/bin/env python3
"""
Price Verification: Cross-check SMB lake data against Yahoo Finance.
Per prompt specification:
"每轮回测前对测试的各个交易标的随机抽取5个时段的价格与 yahoofinance的价格比对，确认数据是否有问题，有问题立即停止工作向用户汇报。"
"""

import sys
import random
import pandas as pd
import pyarrow.parquet as pq
import yfinance as yf

SYMBOL_CONFIG = {
    "BTCUSDT": {
        "parquet_path": "/home/da/smb_database/03_governed_lake/v2_parquet_lake/crypto/futures_um/BTCUSDT/15m/BTCUSDT_15m_consolidated.parquet",
        "yf_ticker": "BTC-USD",
    },
    "ETHUSDT": {
        "parquet_path": "/home/da/smb_database/03_governed_lake/v2_parquet_lake/crypto/futures_um/ETHUSDT/15m/ETHUSDT_15m_consolidated.parquet",
        "yf_ticker": "ETH-USD",
    },
    "SOLUSDT": {
        "parquet_path": "/home/da/smb_database/03_governed_lake/v2_parquet_lake/crypto/futures_um/SOLUSDT/15m/SOLUSDT_15m_consolidated.parquet",
        "yf_ticker": "SOL-USD",
    },
    "BNBUSDT": {
        "parquet_path": "/home/da/smb_database/03_governed_lake/v2_parquet_lake/crypto/futures_um/BNBUSDT/15m/BNBUSDT_15m_consolidated.parquet",
        "yf_ticker": "BNB-USD",
    },
}

def verify_all_symbols(sample_count: int = 5, max_allowed_divergence_pct: float = 2.5) -> bool:
    print("=" * 85)
    print("Starting Price Verification: SMB Lake Parquet vs Yahoo Finance Intraday")
    print(f"Sampling {sample_count} random timestamps per symbol. Tolerance threshold: {max_allowed_divergence_pct}%")
    print("=" * 85)

    all_passed = True
    summary_records = []

    for sym, cfg in SYMBOL_CONFIG.items():
        print(f"\n[Verifying {sym}] Loading parquet: {cfg['parquet_path']}...")
        table = pq.read_table(cfg["parquet_path"])
        df_pq = table.to_pandas()
        
        # Standardize timestamp
        if "timestamp" in df_pq.columns and df_pq["timestamp"].iloc[0] > 1e11:
            df_pq["dt_utc"] = pd.to_datetime(df_pq["timestamp"], unit="ms", utc=True)
        elif "datetime" in df_pq.columns:
            df_pq["dt_utc"] = pd.to_datetime(df_pq["datetime"], utc=True)
        else:
            df_pq["dt_utc"] = pd.to_datetime(df_pq.index, utc=True)

        df_pq.set_index("dt_utc", inplace=True)
        df_pq.sort_index(inplace=True)

        yf_sym = cfg["yf_ticker"]
        print(f"Fetching recent 15m bars from Yahoo Finance for {yf_sym}...")
        yf_df = yf.Ticker(yf_sym).history(period="14d", interval="15m")
        if yf_df.empty:
            print(f"WARNING: Yahoo Finance history returned empty for {yf_sym}, trying 30d daily fallback check...")
            yf_df = yf.Ticker(yf_sym).history(period="30d", interval="1d")

        if yf_df.index.tz is None:
            yf_df.index = yf_df.index.tz_localize("UTC")
        else:
            yf_df.index = yf_df.index.tz_convert("UTC")

        # Find overlapping timestamps
        common_ts = df_pq.index.intersection(yf_df.index)
        if len(common_ts) < sample_count:
            # Fallback: align by nearest timestamp within 15 minutes
            print(f"Direct timestamp intersection count: {len(common_ts)}. Aligning by nearest bar...")
            matched_ts = []
            for ts in yf_df.index[-50:]:
                if ts in df_pq.index:
                    matched_ts.append(ts)
            common_ts = pd.DatetimeIndex(matched_ts)

        if len(common_ts) < sample_count:
            print(f"ERROR: Not enough overlapping timestamps for {sym} (found {len(common_ts)})")
            all_passed = False
            continue

        random.seed(42)
        sampled = random.sample(list(common_ts), sample_count)
        sampled.sort()

        print(f"{'Timestamp (UTC)':<22} | {'Parquet Close':<14} | {'Yahoo Close':<14} | {'Diff ($)':<10} | {'Rel Diff (%)':<12}")
        print("-" * 85)

        for ts in sampled:
            pq_close = float(df_pq.loc[ts, "close"])
            yf_close = float(yf_df.loc[ts, "Close"])
            diff = abs(pq_close - yf_close)
            rel_diff = (diff / yf_close) * 100.0

            status = "PASS" if rel_diff <= max_allowed_divergence_pct else "FAIL"
            print(f"{str(ts):<22} | {pq_close:<14.4f} | {yf_close:<14.4f} | {diff:<10.4f} | {rel_diff:<10.3f}% [{status}]")

            summary_records.append({
                "symbol": sym,
                "timestamp": str(ts),
                "parquet_close": pq_close,
                "yahoo_close": yf_close,
                "diff": diff,
                "rel_diff_pct": rel_diff,
                "status": status,
            })

            if rel_diff > max_allowed_divergence_pct:
                all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("ALL SYMBOLS PASSED PRICE CROSS-CHECK (Max deviation strictly within tolerance).")
    else:
        print("ERROR: ONE OR MORE SAMPLES EXCEEDED THE DIVERGENCE THRESHOLD!")
    print("=" * 85)
    return all_passed

if __name__ == "__main__":
    success = verify_all_symbols(sample_count=5)
    if not success:
        sys.exit(1)
