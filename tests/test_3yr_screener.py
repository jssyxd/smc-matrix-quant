import unittest
import pandas as pd
import numpy as np
from src.ross_3yr_daily_screener import (
    Ross3YrDailyScreener,
    compute_rolling_50d_avg_volume,
    enrich_daily_indicators,
)

class Test3YrScreener(unittest.TestCase):
    def setUp(self):
        self.screener = Ross3YrDailyScreener()

    def test_rolling_50d_volume_zero_lookahead(self):
        """Verify 50-day average volume uses strictly prior days t-1...t-50 with shift(1)."""
        vols = pd.Series([1000.0] * 60)
        vols.iloc[50] = 50000.0  # huge spike on day 50
        
        avg_vols = compute_rolling_50d_avg_volume(vols, window=50)
        # On day 50, avg_vol should NOT know about day 50's volume
        self.assertEqual(avg_vols.iloc[50], 1000.0)
        # On day 51, avg_vol should incorporate day 50
        expected_avg_51 = (1000.0 * 49 + 50000.0) / 50.0
        self.assertAlmostEqual(avg_vols.iloc[51], expected_avg_51, places=4)

    def test_screener_candidate_qualification(self):
        """Test candidate with >10% gain and >5x RVol qualifies."""
        c = self.screener.screen_stock_record(
            date_str="2023-01-10",
            symbol="MARA",
            current_price=12.0,
            prev_close=10.0,
            current_volume=10_000_000,
            avg_volume_50d=1_000_000,
            high_price=13.0,
            float_shares=15_000_000,
            has_catalyst=True,
        )
        self.assertTrue(c.qualified)
        self.assertGreaterEqual(c.passed_rules_count, 4)
        self.assertGreaterEqual(c.relative_volume, 5.0)

if __name__ == "__main__":
    unittest.main()
