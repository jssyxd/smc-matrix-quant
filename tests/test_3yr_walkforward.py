import unittest
import pandas as pd
from src.ross_3yr_walkforward_engine import Ross3YrWalkForwardEngine

class Test3YrWalkForward(unittest.TestCase):
    def setUp(self):
        self.engine = Ross3YrWalkForwardEngine(initial_capital=2000.0)

    def test_walk_forward_execution_and_summary(self):
        """Verify 80/20 walk-forward backtest runs across 2021-2023 with non-zero trades and valid summary."""
        res = self.engine.run_walk_forward_backtest()
        df = res["summary_df"]
        self.assertEqual(len(df), 6)  # 3 years * (1 IS + 1 OOS) = 6 rows
        self.assertTrue(all(col in df.columns for col in ["year", "sample_type", "total_trades", "win_rate_pct", "period_pnl"]))
        self.assertGreater(df["total_trades"].sum(), 20)
        self.assertGreater(res["final_capital"], 1000.0)

if __name__ == "__main__":
    unittest.main()
