# IM-MO Synthetic Futures Statistical Arbitrage Backtest

## Overview

This project implements a statistical arbitrage backtest between CSI 1000 Index Futures (IM) and CSI 1000 Index Options (MO) synthetic futures.

The synthetic futures price is constructed using the put-call parity relationship:

Synthetic Future = Call − Put + Strike

The strategy investigates whether the spread between the listed index futures and synthetic futures exhibits mean reversion, and evaluates the profitability after incorporating realistic transaction costs.

The project is inspired by the statistical arbitrage framework discussed in the CITIC Futures research report, while the complete backtesting framework, contract selection logic and implementation are independently developed.
# Results

The framework generates:

- Net value curve
- Basis movement analysis
- Abnormal event detection
- Automated attribution report
## Visualization

### Net Value Curve

![Net Value Curve](outputs/figures/MO-IM%20Arbitrage%20Net%20Value%20Curve.png)


### Basis Attribution Analysis

![Basis Attribution](outputs/figures/IM_MO_Basis_Attribution_Summary.png)


### Synthetic Futures Backtest

![Synthetic Futures Backtest](outputs/figures/MO%20synthetic%20future%20-%20IM%20arbitrage%20backtest.png)

## Backtest Performance

### Net Value Curve

![Net Value Curve](outputs/figures/MO-IM%20Arbitrage%20Net%20Value%20Curve.png)


### Basis Attribution Analysis

![Basis Attribution](outputs/figures/IM_MO_Basis_Attribution_Summary.png)


### Synthetic Futures Backtest

![Synthetic Futures Backtest](outputs/figures/MO%20synthetic%20future%20-%20IM%20arbitrage%20backtest.png)
---

## Strategy

### 1. Contract Selection

For each trading day:

- Select the active IM futures contract
- Filter MO options satisfying

```
ATM_distance = |Strike − Spot| / Spot < 5%
```

- Choose the strike with the highest trading volume
- Construct synthetic futures

```
Synthetic = Call − Put + Strike
```

---

### 2. Spread Construction

```
Basis = IM Futures − Synthetic Futures
```

A positive basis indicates that futures are relatively expensive.

A negative basis indicates that synthetic futures are relatively expensive.

---

### 3. Signal Generation

Rolling statistics are computed using historical information only.

```
Window = 100 days

Rolling Mean

Rolling Standard Deviation
```

Trading bands:

```
Upper = Mean + Std

Lower = Mean − Std
```

Entry rules:

- Basis > Upper
    → Short Basis

- Basis < Lower
    → Long Basis

---

### 4. Exit Rules

The position is closed when

- Basis reverts to the rolling mean

or

- Contract expiration

or

- Contract rollover

---

## Transaction Cost Model

The backtest considers

- IM futures trading fee
- IM delivery fee
- MO option trading fee
- MO exercise fee
- Market impact
- Position scaling

Both gross profit and net profit are reported.

---

## Backtesting Framework

```
Market Data

↓

Contract Selection

↓

Synthetic Futures Construction

↓

Basis Calculation

↓

Rolling Statistics

↓

Trading Signal

↓

Position Management

↓

PnL Calculation

↓

Transaction Cost

↓

Performance Evaluation
```

---

## Performance Metrics

The backtest reports

- Total Gross Profit
- Total Net Profit
- Annualized Return
- Win Rate
- Sharpe Ratio
- Profit Factor
- Maximum Drawdown
- Average Holding Period

---

## Project Structure

```
.
├── notebooks/
│   └── IM_MO_Mean_Reversion_Backtest.ipynb
│
├── figures/
│   ├── basis.png
│   ├── equity_curve.png
│   └── drawdown.png
│
├── README.md
└── requirements.txt
```

---

## Future Improvements

- Lock option contracts after opening positions
- Introduce bid-ask spread using tick data
- Dynamic market impact estimation
- Walk-forward parameter validation
- Portfolio-level capital allocation
- Multi-contract statistical arbitrage

---

## Disclaimer

This project is intended solely for educational and research purposes.

It does not constitute investment advice.
