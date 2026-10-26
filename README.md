# SMC Multi-Asset Matrix Quant: Rolling ML Walk-Forward & High-Frequency Suite

Production-grade quantitative research, machine learning rolling walk-forward training, and realistic event-driven backtesting suite for Smart Money Concepts (SMC) multi-asset trading.

---

## 🚀 Core Architecture & Matrix Innovations

1. **5,000-Bar Rolling Walk-Forward Window**:
   - **In-Sample (IS)**: 2,500 bars for feature calibration and regime estimation.
   - **Out-of-Sample (OOS Validation)**: 2,500 bars for $G_{\text{score}} \ge 60\%$ Generalization Gate audit.
   - **Forward Execution**: 288-bar (3-day in 15m) or 144-bar (3-day in 30m) non-overlapping live execution.
2. **Dual-Trigger Re-training Mechanism**:
   - **Scheduled Step**: Every 3 days (288 15m bars).
   - **Volatility/Credal Event**: Dynamic interruption when Garman-Klass / ATR ratio $> 1.80$ or Dirichlet Vacuity $u > 0.38$.
3. **Sub-strategy Matrix**:
   - **Sub-strategy 1**: Single-coin isolated dynamic walk-forward (BTC, ETH, SOL, BNB across 15m and 30m).
   - **Sub-strategy 2**: Exogenous BTC regime driver (BTC trains and gates; Altcoins BNB/SOL/ETH trade).
   - **Sub-strategy 3**: CMC20 synthetic index basket tracking with synchronized execution.
4. **Realistic Transaction Friction**:
   - Initial Capital: 120.00 USDT
   - Leverage: 20x nominal exposure
   - Risk per trade: 5% of free equity
   - Fees: Maker 0.02% (Limit Order entry) / Taker 0.05% (Stop Loss) + 2 bps dynamic slippage
   - Intra-bar pessimism: same-bar conflict strictly executes stop loss first.
5. **Monte Carlo & Noise Perturbation**:
   - 10,000 bootstrap reshuffled paths for Value-at-Risk and Risk of Ruin (> 50% DD).
   - Gaussian price noise ($\pm 0.15\%$) and 3x slippage sensitivity analysis.

---

## 📁 Repository Structure

```
smc-matrix-quant/
├── 001_smc_matrix_20260930/          # Production OKX live trading engine (smc_live_trader.py)
├── matrix/
│   ├── models.py                     # Typed domain models & matrix data structures
│   ├── feature_engine.py             # Causal micro-structure & Dirichlet Credal filter (NeurIPS 2025)
│   ├── execution_engine.py           # Realistic transaction friction execution simulator
│   ├── rolling_trainer.py            # 5,000-bar walk-forward trainer & G_score >= 60% gating
│   ├── substrategies.py              # Sub-strategies 1, 2, and 3 implementation
│   └── kaggle_notebook_generator.py  # Standalone Kaggle Jupyter Notebook generator
├── backtest/
│   ├── price_verification_yfinance.py # Yahoo Finance 5-timestamp cross-verification
│   └── monte_carlo_stress_test.py    # 10,000-path Monte Carlo & noise perturbation engine
├── notebooks/                        # Self-contained Kaggle Jupyter Notebooks (.ipynb)
├── results/                          # Trade ledgers (.csv) and comprehensive audit report (.md)
├── run_full_matrix_simulation.py     # Master orchestrator script
└── docs/                             # Academic & architectural audit reports
```

---

## 📊 Summary Results Table (2024 - 2026)

| Sub-strategy | Train TF | Trade TF | Initial | Final | Net Return | Sharpe | Win Rate | Trades | Gen Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sub1-SingleCoin (ETHUSDT)** | 15m | 15m | $120.00 | $2,338.57 | **+1,848.81%** | **3.24** | 39.7% | 4,299 | 65.0% |
| **Sub1-SingleCoin (SOLUSDT)** | 30m | 30m | $120.00 | $4,040.68 | **+3,267.24%** | **2.43** | 38.8% | 2,259 | 72.2% |
| **Sub1-SingleCoin (BTCUSDT)** | 15m | 15m | $120.00 | $9.98 | -91.68% | 1.89 | 39.7% | 2,287 | 44.5% |
| **Sub1-SingleCoin (BNBUSDT)** | 15m | 15m | $120.00 | $9.90 | -91.75% | 1.29 | 38.9% | 1,516 | 55.0% |
| **Sub2-BTC_Exogenous (Altcoins)** | 15m | 15m | $120.00 | $55.46 | -53.78% | 3.51 | 38.8% | 9,014 | 44.5% |
| **Sub3-CMC20_Basket** | 15m | 15m | $120.00 | $9.50 | -92.08% | -1.13 | 34.8% | 135 | 8.1% |

*Detailed ledgers and analysis available in `results/COMPREHENSIVE_ROLLING_AUDIT_REPORT.md`.*
