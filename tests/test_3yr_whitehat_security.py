import unittest
import numpy as np
import pandas as pd
from src.ross_3yr_credal_stress import (
    CredalTransformerAuditor,
    Ross3YrMonteCarloBootstrap,
    Ross3YrWhiteHatAuditor,
)

class Test3YrWhiteHatSecurity(unittest.TestCase):
    def setUp(self):
        self.credal_auditor = CredalTransformerAuditor()
        self.whitehat_auditor = Ross3YrWhiteHatAuditor()
        self.mc_engine = Ross3YrMonteCarloBootstrap(n_simulations=2000, sample_trades_per_path=100)

    def test_future_scrambling_zero_lookahead_invariant(self):
        """Test zero-lookahead proof: future data shuffling causes 0.000 change in current signals."""
        # Synthetic 5-min OHLCV bars with capitalized column names
        dates = pd.date_range("2023-01-05 09:30:00", periods=50, freq="5min")
        df = pd.DataFrame({
            "Open": [10.0 + i * 0.1 for i in range(50)],
            "High": [10.2 + i * 0.1 for i in range(50)],
            "Low": [9.9 + i * 0.1 for i in range(50)],
            "Close": [10.1 + i * 0.1 for i in range(50)],
            "Volume": [100000 + i * 1000 for i in range(50)],
        }, index=dates)
        res = self.whitehat_auditor.verify_zero_lookahead_invariant(df, eval_bars=[15, 25, 35])
        self.assertTrue(res["passed"])
        self.assertLess(res["max_delta"], 1e-10)

    def test_monte_carlo_bootstrap_ruin_probability(self):
        """2,000-path Monte Carlo bootstrap proves zero ruin probability under 50% max DD threshold."""
        sample_pnls = [25.0, -15.0, 40.0, -10.0, 30.0, -12.0, 50.0, -8.0, 35.0, -14.0] * 20
        res = self.mc_engine.run_bootstrap(sample_pnls)
        self.assertEqual(res.probability_of_ruin_pct, 0.0)
        self.assertLess(res.max_drawdown_95_pct, 20.0)
if __name__ == "__main__":
    unittest.main()
