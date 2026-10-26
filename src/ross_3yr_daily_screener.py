"""
Ross Cameron 3-Year Daily Screener (2021-2023) for US Equities.
Applies Ross Cameron's 5 Momentum Rules across all trading days in 2021-2023:
1. Day Change / Gap-Up >= +10% (sweet spot >= +30%).
2. Relative Volume (RVol) >= 5x (compared to rolling 50-day average volume up to day t-1).
3. Share Price $2.00 - $20.00 (sweet spot $5.00 - $10.00).
4. Low Float < 20M shares (sweet spot < 10M shares).
5. Catalyst / News / Heavy Short Squeeze.

Enforces zero lookahead bias:
Rolling 50-day average volume at day t is strictly computed from days t-50 through t-1.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any, Tuple
import pandas as pd
import numpy as np

from src.ross_momentum_screener import ScreenerCandidate


@dataclass
class DailyScreenerCandidate(ScreenerCandidate):
    """
    Extends ScreenerCandidate with trading date and volume diagnostics.
    """
    date: str = ""
    volume: float = 0.0
    avg_volume_50d: float = 0.0
    prev_close: float = 0.0


# Default metadata for universe stocks
DEFAULT_STOCK_METADATA: Dict[str, Dict[str, Any]] = {
    "MARA": {
        "float_shares": 18_500_000,
        "has_catalyst": True,
        "is_short_squeeze": True,
        "sector": "Crypto/Mining",
    },
    "RIOT": {
        "float_shares": 22_000_000,
        "has_catalyst": True,
        "is_short_squeeze": True,
        "sector": "Crypto/Mining",
    },
    "GME": {
        "float_shares": 46_000_000,
        "has_catalyst": True,
        "is_short_squeeze": True,
        "sector": "Gaming/Meme",
    },
    "SOUN": {
        "float_shares": 25_000_000,
        "has_catalyst": True,
        "is_short_squeeze": False,
        "sector": "AI Technology",
    },
    "PLTR": {
        "float_shares": 1_800_000_000,
        "has_catalyst": True,
        "is_short_squeeze": False,
        "sector": "AI/Defense Enterprise",
    },
    "CVNA": {
        "float_shares": 65_000_000,
        "has_catalyst": True,
        "is_short_squeeze": True,
        "sector": "Auto Retail/Short Squeeze",
    },
    "LCID": {
        "float_shares": 80_000_000,
        "has_catalyst": True,
        "is_short_squeeze": False,
        "sector": "EV/Automotive",
    },
    "AFRM": {
        "float_shares": 120_000_000,
        "has_catalyst": True,
        "is_short_squeeze": False,
        "sector": "Fintech/BNPL",
    },
}


def compute_rolling_50d_avg_volume(
    volume_series: pd.Series,
    window: int = 50,
    min_periods: int = 1,
) -> pd.Series:
    """
    Calculate rolling 50-day average volume strictly up to day t-1.
    Zero-lookahead guarantee:
    Volume at day t is NEVER included in day t's rolling 50-day average volume.
    """
    return volume_series.shift(1).rolling(window=window, min_periods=min_periods).mean()


def enrich_daily_indicators(
    df: pd.DataFrame,
    window: int = 50,
    min_periods: int = 1,
) -> pd.DataFrame:
    """
    Enrich daily price bars with zero-lookahead momentum indicators:
    - prev_close: close[t-1]
    - day_change_pct: ((close[t] - prev_close) / prev_close) * 100
    - gap_pct: ((open[t] - prev_close) / prev_close) * 100
    - max_gain_pct: ((high[t] - prev_close) / prev_close) * 100
    - avg_volume_50d: rolling 50-day mean of volume[t-50..t-1]
    - rvol: volume[t] / avg_volume_50d
    """
    if df.empty:
        return df

    res = df.copy()
    if not isinstance(res.index, pd.DatetimeIndex):
        res.index = pd.to_datetime(res.index)
    res = res.sort_index()

    res["prev_close"] = res["close"].shift(1)
    res["day_change_pct"] = ((res["close"] - res["prev_close"]) / res["prev_close"].replace(0, np.nan)) * 100.0
    res["gap_pct"] = ((res["open"] - res["prev_close"]) / res["prev_close"].replace(0, np.nan)) * 100.0
    res["max_gain_pct"] = ((res["high"] - res["prev_close"]) / res["prev_close"].replace(0, np.nan)) * 100.0

    res["avg_volume_50d"] = compute_rolling_50d_avg_volume(
        res["volume"], window=window, min_periods=min_periods
    )
    res["rvol"] = res["volume"] / res["avg_volume_50d"].replace(0, np.nan)
    res["date_str"] = res.index.strftime("%Y-%m-%d")
    return res


class Ross3YrDailyScreener:
    """
    Ross Cameron 5-Rule Daily Screener for multi-year US equities universes.
    """
    def __init__(
        self,
        min_gap_pct: float = 10.0,
        min_rvol: float = 5.0,
        min_price: float = 2.0,
        max_price: float = 20.0,
        max_float: float = 20_000_000,
        strict_sweet_spot: bool = False,
        require_mandatory_rvol: bool = True,
        require_mandatory_gain: bool = True,
        min_passed_rules: int = 4,
        volume_window: int = 50,
        volume_min_periods: int = 1,
        stock_metadata: Optional[Dict[str, Dict[str, Any]]] = None,
        use_high_for_gain: bool = False,
    ):
        self.min_gap_pct = 30.0 if strict_sweet_spot else min_gap_pct
        self.min_rvol = min_rvol
        self.min_price = 5.0 if strict_sweet_spot else min_price
        self.max_price = 10.0 if strict_sweet_spot else max_price
        self.max_float = 10_000_000 if strict_sweet_spot else max_float
        self.strict_sweet_spot = strict_sweet_spot
        self.require_mandatory_rvol = require_mandatory_rvol
        self.require_mandatory_gain = require_mandatory_gain
        self.min_passed_rules = min_passed_rules
        self.volume_window = volume_window
        self.volume_min_periods = volume_min_periods
        self.stock_metadata = stock_metadata or DEFAULT_STOCK_METADATA
        self.use_high_for_gain = use_high_for_gain

    def screen_stock_record(
        self,
        symbol: str,
        date_str: str,
        current_price: float,
        prev_close: float,
        current_volume: float,
        avg_volume_50d: float,
        high_price: Optional[float] = None,
        open_price: Optional[float] = None,
        float_shares: Optional[float] = None,
        has_catalyst: Optional[bool] = None,
        is_short_squeeze: Optional[bool] = None,
    ) -> DailyScreenerCandidate:
        """
        Evaluate a single stock on a given date against Ross Cameron's 5 momentum rules.
        """
        sym_meta = self.stock_metadata.get(symbol.upper(), {})
        f_shares = float_shares if float_shares is not None else sym_meta.get("float_shares", 15_000_000)
        h_catalyst = has_catalyst if has_catalyst is not None else sym_meta.get("has_catalyst", False)
        s_squeeze = is_short_squeeze if is_short_squeeze is not None else sym_meta.get("is_short_squeeze", False)

        # Day change calculation
        if prev_close <= 0 or np.isnan(prev_close):
            gain_pct = 0.0
        else:
            if self.use_high_for_gain and high_price is not None and not np.isnan(high_price):
                gain_pct = ((high_price - prev_close) / prev_close) * 100.0
            else:
                gain_pct = ((current_price - prev_close) / prev_close) * 100.0

        # Relative volume
        if avg_volume_50d <= 0 or np.isnan(avg_volume_50d):
            rvol = 0.0
        else:
            rvol = current_volume / avg_volume_50d

        # Rule 1: Gain / Gap >= 10%
        r1 = gain_pct >= self.min_gap_pct

        # Rule 2: RVol >= 5x (compared to rolling 50-day average volume)
        r2 = rvol >= self.min_rvol

        # Rule 3: Share price in $2 - $20
        r3 = (self.min_price <= current_price <= self.max_price)

        # Rule 4: Low float < 20M shares
        r4 = (f_shares <= self.max_float)

        # Rule 5: Catalyst / Squeeze
        r5 = bool(h_catalyst or s_squeeze)

        passed_rules = sum([r1, r2, r3, r4, r5])

        # Ross Cameron rule logic:
        # Mandatory RVol >= 5x, mandatory positive gain >= min_gap_pct,
        # and at least min_passed_rules (default 4 of 5 rules).
        qualified = True
        if self.require_mandatory_rvol and not r2:
            qualified = False
        if self.require_mandatory_gain and not r1:
            qualified = False
        if passed_rules < self.min_passed_rules:
            qualified = False

        # Ranking score (Ross Cameron momentum composite score)
        score = (
            min(max(gain_pct, 0.0), 100.0) * 0.35 +
            min(max(rvol, 0.0) * 5.0, 50.0) * 0.35 +
            (10.0 if (5.0 <= current_price <= 10.0) else 5.0) +
            (20.0 if f_shares <= 10_000_000 else 10.0) +
            (10.0 if r5 else 0.0)
        )

        return DailyScreenerCandidate(
            symbol=symbol.upper(),
            price=float(current_price),
            gap_percent=float(gain_pct),
            relative_volume=float(rvol),
            float_shares=float(f_shares),
            has_catalyst=h_catalyst,
            is_short_squeeze=s_squeeze,
            passed_rules_count=int(passed_rules),
            qualified=bool(qualified),
            score=float(score),
            date=date_str,
            volume=float(current_volume),
            avg_volume_50d=float(avg_volume_50d) if not np.isnan(avg_volume_50d) else 0.0,
            prev_close=float(prev_close) if not np.isnan(prev_close) else 0.0,
        )

    def screen_day(
        self,
        date: Union[str, pd.Timestamp],
        universe_enriched_data: Dict[str, pd.DataFrame],
        filter_qualified_only: bool = True,
    ) -> List[DailyScreenerCandidate]:
        """
        Screen all universe stocks on a specific trading day.
        Returns candidates for that day, sorted and ranked by composite score.
        """
        date_str = str(date).split("T")[0].split(" ")[0]
        day_candidates: List[DailyScreenerCandidate] = []

        for symbol, df in universe_enriched_data.items():
            if df.empty:
                continue

            # Direct lookup if 'date_str' column is present
            if "date_str" in df.columns:
                matching_rows = df[df["date_str"] == date_str]
            else:
                matching_rows = df[df.index.strftime("%Y-%m-%d") == date_str]

            if matching_rows.empty:
                continue

            row = matching_rows.iloc[0]
            prev_c = row.get("prev_close", np.nan)
            avg_v = row.get("avg_volume_50d", np.nan)
            
            # Skip if no previous history
            if pd.isna(prev_c) or pd.isna(avg_v) or prev_c <= 0 or avg_v <= 0:
                continue

            cand = self.screen_stock_record(
                symbol=symbol,
                date_str=date_str,
                current_price=row["close"],
                prev_close=prev_c,
                current_volume=row["volume"],
                avg_volume_50d=avg_v,
                high_price=row.get("high"),
                open_price=row.get("open"),
            )

            if not filter_qualified_only or cand.qualified:
                day_candidates.append(cand)

        # Sort by score descending and assign rank
        day_candidates.sort(key=lambda x: x.score, reverse=True)
        for idx, c in enumerate(day_candidates):
            c.rank = idx + 1

        return day_candidates

    def run_3yr_screening(
        self,
        universe_daily_data: Dict[str, pd.DataFrame],
        start_date: str = "2021-01-01",
        end_date: str = "2023-12-31",
        filter_qualified_only: bool = True,
    ) -> Dict[str, List[DailyScreenerCandidate]]:
        """
        Execute daily screening loop across all trading days in the multi-year range.
        Calculates rolling 50-day average volume up to day t-1 for zero lookahead.
        Pre-indexes dates for millisecond-level execution across 3 years.
        Returns mapping: {date_str: [DailyScreenerCandidate, ...]}
        """
        # Step 1: Pre-calculate zero-lookahead rolling 50d volume and indicators per stock
        start_clean = start_date.split("T")[0]
        end_clean = end_date.split("T")[0]

        # Pre-group records by date_str for fast lookup
        date_records: Dict[str, Dict[str, Any]] = {}
        for sym, raw_df in universe_daily_data.items():
            if raw_df.empty:
                continue
            df_enriched = enrich_daily_indicators(
                raw_df, window=self.volume_window, min_periods=self.volume_min_periods
            )
            # Filter date range
            mask = (df_enriched["date_str"] >= start_clean) & (df_enriched["date_str"] <= end_clean)
            for dt_str, row in df_enriched[mask].iterrows():
                d_str = row["date_str"]
                if d_str not in date_records:
                    date_records[d_str] = {}
                date_records[d_str][sym.upper()] = row

        sorted_dates = sorted(list(date_records.keys()))
        results: Dict[str, List[DailyScreenerCandidate]] = {}

        # Step 2: Screen each trading day in chronological order
        for d_str in sorted_dates:
            day_candidates: List[DailyScreenerCandidate] = []
            sym_dict = date_records[d_str]

            for symbol, row in sym_dict.items():
                prev_c = row.get("prev_close", np.nan)
                avg_v = row.get("avg_volume_50d", np.nan)

                if pd.isna(prev_c) or pd.isna(avg_v) or prev_c <= 0 or avg_v <= 0:
                    continue

                cand = self.screen_stock_record(
                    symbol=symbol,
                    date_str=d_str,
                    current_price=row["close"],
                    prev_close=prev_c,
                    current_volume=row["volume"],
                    avg_volume_50d=avg_v,
                    high_price=row.get("high"),
                    open_price=row.get("open"),
                )

                if not filter_qualified_only or cand.qualified:
                    day_candidates.append(cand)

            if day_candidates or not filter_qualified_only:
                day_candidates.sort(key=lambda x: x.score, reverse=True)
                for idx, c in enumerate(day_candidates):
                    c.rank = idx + 1
                results[d_str] = day_candidates

        return results

    def get_candidates_summary_df(
        self,
        screening_results: Dict[str, List[DailyScreenerCandidate]],
    ) -> pd.DataFrame:
        """
        Convert screening results mapping into a consolidated summary DataFrame.
        """
        records = []
        for d_str, cands in screening_results.items():
            for c in cands:
                records.append({
                    "date": c.date,
                    "symbol": c.symbol,
                    "price": c.price,
                    "prev_close": c.prev_close,
                    "gap_percent": c.gap_percent,
                    "relative_volume": c.relative_volume,
                    "volume": c.volume,
                    "avg_volume_50d": c.avg_volume_50d,
                    "float_shares": c.float_shares,
                    "has_catalyst": c.has_catalyst,
                    "is_short_squeeze": c.is_short_squeeze,
                    "passed_rules_count": c.passed_rules_count,
                    "qualified": c.qualified,
                    "score": c.score,
                    "rank": c.rank,
                })

        if not records:
            return pd.DataFrame(
                columns=[
                    "date", "symbol", "price", "prev_close", "gap_percent",
                    "relative_volume", "volume", "avg_volume_50d", "float_shares",
                    "has_catalyst", "is_short_squeeze", "passed_rules_count",
                    "qualified", "score", "rank",
                ]
            )

        df = pd.DataFrame(records)
        return df.sort_values(by=["date", "rank"]).reset_index(drop=True)

    def get_active_momentum_days(
        self,
        screening_results: Dict[str, List[DailyScreenerCandidate]],
    ) -> List[Dict[str, Any]]:
        """
        Extract qualified active momentum days in dictionary form suitable for
        feeding directly into intraday data pipelines.
        """
        active_days = []
        for d_str, cands in screening_results.items():
            for c in cands:
                if c.qualified:
                    active_days.append({
                        "symbol": c.symbol,
                        "date": c.date,
                        "price": c.price,
                        "gap_percent": c.gap_percent,
                        "relative_volume": c.relative_volume,
                        "score": c.score,
                        "rank": c.rank,
                    })
        return active_days
