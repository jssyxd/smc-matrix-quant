"""
Ross Cameron 5-Rule Momentum Screener (YouTube UD4XwSs_0r8).
Rules:
1. Day Change / Gap-Up >= +10% (sweet spot >= +30%).
2. Relative Volume (RVol) >= 5x (compared to 50-day average volume).
3. Share Price $2.00 - $20.00 (sweet spot $5.00 - $10.00).
4. Low Float < 20M shares (sweet spot < 10M shares).
5. Catalyst / News / Heavy Short Squeeze.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np


@dataclass
class ScreenerCandidate:
    symbol: str
    price: float
    gap_percent: float
    relative_volume: float
    float_shares: float
    has_catalyst: bool
    is_short_squeeze: bool
    passed_rules_count: int
    qualified: bool
    score: float
    rank: int = 0


class RossMomentumScreener:
    def __init__(
        self,
        min_gap_pct: float = 10.0,
        min_rvol: float = 5.0,
        min_price: float = 2.0,
        max_price: float = 20.0,
        max_float: float = 20_000_000,
        strict_sweet_spot: bool = False,
    ):
        self.min_gap_pct = 30.0 if strict_sweet_spot else min_gap_pct
        self.min_rvol = min_rvol
        self.min_price = 5.0 if strict_sweet_spot else min_price
        self.max_price = 10.0 if strict_sweet_spot else max_price
        self.max_float = 10_000_000 if strict_sweet_spot else max_float

    def screen_stock(
        self,
        symbol: str,
        current_price: float,
        prev_close: float,
        current_volume: float,
        avg_volume_50d: float,
        float_shares: float,
        has_catalyst: bool = False,
        is_short_squeeze: bool = False,
    ) -> ScreenerCandidate:
        """Screen a single US stock against Ross Cameron's 5 rules."""
        gap_pct = ((current_price - prev_close) / max(prev_close, 1e-4)) * 100.0
        rvol = current_volume / max(avg_volume_50d, 1.0)
        
        # Rule 1: Gap / Day change >= 10%
        r1 = gap_pct >= self.min_gap_pct
        
        # Rule 2: RVol >= 5x
        r2 = rvol >= self.min_rvol
        
        # Rule 3: Price in $2 - $20
        r3 = (self.min_price <= current_price <= self.max_price)
        
        # Rule 4: Float < 20M
        r4 = (float_shares <= self.max_float)
        
        # Rule 5: Catalyst / Squeeze
        r5 = has_catalyst or is_short_squeeze
        
        passed_rules = sum([r1, r2, r3, r4, r5])
        
        # Ross: RVol >= 5x is mandatory; if no news, 4 out of 5 rules allows trading with reduced size
        qualified = r2 and (passed_rules >= 4)
        
        # Score calculation for ranking
        score = (
            min(gap_pct, 100.0) * 0.35 +
            min(rvol * 5.0, 50.0) * 0.35 +
            (10.0 if (5.0 <= current_price <= 10.0) else 5.0) +
            (20.0 if float_shares <= 10_000_000 else 10.0) +
            (10.0 if r5 else 0.0)
        )
        
        return ScreenerCandidate(
            symbol=symbol,
            price=current_price,
            gap_percent=gap_pct,
            relative_volume=rvol,
            float_shares=float_shares,
            has_catalyst=has_catalyst,
            is_short_squeeze=is_short_squeeze,
            passed_rules_count=passed_rules,
            qualified=qualified,
            score=score,
        )

    def screen_universe(self, stocks_data: List[Dict[str, Any]]) -> List[ScreenerCandidate]:
        """Screen and rank a universe of candidates."""
        candidates = [self.screen_stock(**s) for s in stocks_data]
        # Filter qualified
        qualified = [c for c in candidates if c.qualified]
        # Sort by score descending
        qualified.sort(key=lambda x: x.score, reverse=True)
        for idx, c in enumerate(qualified):
            c.rank = idx + 1
        return qualified
