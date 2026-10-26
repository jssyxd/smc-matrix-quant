import unittest
import pandas as pd
from src.ross_momentum_screener import RossMomentumScreener, ScreenerCandidate
from src.alpaca_ross_data_loader import filter_trading_window

class TestRossMomentumScreener(unittest.TestCase):
    def setUp(self):
        self.screener = RossMomentumScreener()

    def test_ideal_ross_candidate_passes_all_rules(self):
        """Test ideal candidate like ZTG: +150% gain, 8x RVol, $6 price, 7.19M float, with catalyst."""
        cand = self.screener.screen_stock(
            symbol="ZTG",
            current_price=6.50,
            prev_close=2.60,
            current_volume=4_000_000,
            avg_volume_50d=500_000,
            float_shares=7_190_000,
            has_catalyst=True,
        )
        self.assertTrue(cand.qualified)
        self.assertEqual(cand.passed_rules_count, 5)
        self.assertGreater(cand.score, 60.0)

    def test_four_out_of_five_rules_passes_with_no_news(self):
        """Test candidate with no news but huge momentum/squeeze passes (Ross ZTG case)."""
        cand = self.screener.screen_stock(
            symbol="ZTG_NO_NEWS",
            current_price=1.60,  # slightly below $2
            prev_close=0.70,
            current_volume=5_000_000,
            avg_volume_50d=500_000,
            float_shares=7_190_000,
            has_catalyst=False,
            is_short_squeeze=True,
        )
        # R2 (RVol 10x) is true, gap +128% is true, float < 20M is true, squeeze is true -> 4 rules
        self.assertTrue(cand.qualified)

    def test_rvol_under_five_fails_mandatory(self):
        """Ross: RVol >= 5x is mandatory; without high volume, stock is rejected."""
        cand = self.screener.screen_stock(
            symbol="LOW_VOL",
            current_price=8.00,
            prev_close=5.00,
            current_volume=1_000_000,
            avg_volume_50d=500_000,  # only 2x RVol
            float_shares=5_000_000,
            has_catalyst=True,
        )
        self.assertFalse(cand.qualified)

    def test_filter_trading_window(self):
        """Verify pre-market & morning trading window filter (07:00 - 10:00 EST)."""
        idx = pd.date_range("2026-09-29 11:00:00", periods=8, freq="30min", tz="UTC") # 07:00 to 10:30 EST
        df = pd.DataFrame({"close": range(8)}, index=idx)
        filtered = filter_trading_window(df, start_time="07:00:00", end_time="10:00:00")
        self.assertEqual(len(filtered), 7)  # 10:30 EST is filtered out

if __name__ == "__main__":
    unittest.main()
