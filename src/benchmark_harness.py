#!/usr/bin/env python3
"""
Canonical Autoresearch Benchmark Harness.
Executes the Research Director Strategy Verification & Anti-Overfitting Suite.
Outputs METRIC lines in canonical autoresearch format.
"""

from __future__ import annotations

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.research_director_audit import run_full_research_director_audit


def main() -> int:
    try:
        report = run_full_research_director_audit(
            trades_log_path="results/ross_momentum_backtests/ross_alpaca_trades_log.json",
            yahoo_bars_dir="data/yahoo_bars",
        )

        # Primary metric (higher is better, 0.0 - 100.0)
        print(f"METRIC anti_overfitting_score={report.anti_overfitting_score:.4f}")

        # Secondary metrics
        print(f"METRIC fillability_rate={report.fillability_rate:.4f}")
        print(f"METRIC walk_forward_efficiency={report.walk_forward_efficiency:.4f}")
        print(f"METRIC pbo={report.pbo:.4f}")
        print(f"METRIC deflated_sharpe={report.deflated_sharpe:.4f}")
        print(f"METRIC lookahead_pass_rate={report.lookahead_pass_rate:.4f}")
        print(f"METRIC max_drawdown_95={report.max_drawdown_95:.4f}")
        print(f"METRIC ruin_probability={report.ruin_probability:.4f}")

        # Additional summary output for logging
        print(f"ASI summary_verdict={report.summary_verdict}")
        print(f"ASI total_trades={report.market_fillability.total_trades_audited}")
        print(f"ASI matched_timestamps={report.market_fillability.matched_timestamps}")
        print(f"ASI price_valid_count={report.market_fillability.price_valid_count}")
        print(f"ASI volume_valid_count={report.market_fillability.volume_depth_valid_count}")
        print(f"ASI phantom_price_count={report.market_fillability.phantom_price_count}")

        return 0
    except Exception as e:
        sys.stderr.write(f"Benchmark error: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
