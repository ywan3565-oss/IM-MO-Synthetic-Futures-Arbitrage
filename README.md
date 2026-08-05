# IM-MO Synthetic Futures Arbitrage Research

A quantitative research framework for identifying and explaining abnormal basis movements between the CSI 1000 Index Futures (IM) and synthetic futures constructed from CSI 1000 Index Options (MO).

The project provides an end-to-end workflow including:

- Synthetic futures construction
- Basis calculation
- Statistical anomaly detection
- Attribution analysis
- Event calendar matching
- Automatic bilingual research report generation

---

# Workflow

```
Raw Market Data
        │
        ▼
Synthetic Futures Construction
        │
        ▼
Basis Calculation
        │
        ▼
Rolling Statistics
        │
        ▼
Abnormal Event Detection
        │
        ▼
Basis Attribution Engine
        │
        ▼
Event Calendar Matching
        │
        ▼
Automatic Research Report
```

---

# Features

## 1. Synthetic Futures Construction

Construct synthetic futures using

```
Synthetic Future
=
Call
− Put
+ Strike
```

and compare against IM futures settlement prices.

---

## 2. Basis Analysis

Calculate

```
Basis
=
Synthetic Future
− IM Futures
```

or

```
Basis
=
IM Futures
− Synthetic Future
```

depending on research definition.

Rolling statistics include

- Rolling Mean
- Rolling Standard Deviation
- Z-score
- Basis Change

---

## 3. Automatic Abnormal Event Detection

Detect statistically significant basis movements using

- Rolling Z-score
- Daily Basis Change
- Minimum event spacing

Output:

- abnormal_basis_events.csv

---

## 4. Basis Attribution Engine

For every abnormal event the engine evaluates

- Contract Roll
- Strike Change
- Near Expiry
- IM Contribution
- MO Contribution
- Dominant Leg
- Confidence Score

Automatically identifies the primary reason for each abnormal basis movement.

---

## 5. Event Calendar Matching

Abnormal events are matched with an external event calendar.

Examples include

- Contract Roll
- Holiday
- Economic Release
- Policy Announcement
- Exchange Adjustment

Outputs

- matched event
- event importance
- event distance

---

## 6. Automatic Research Report

Generate

- English Markdown Report
- Chinese Markdown Report

Each report contains

- abnormal event summary
- attribution result
- matched event
- confidence
- research explanation

---

# Project Structure

```
src/
    attribution.py
    event_calendar.py
    report_generator.py
    visualization.py

data/
    event_calendar.csv

outputs/
    attribution_results.csv
    attribution_with_events.csv
    IM_MO_Research_Report.md
    IM_MO_研究报告.md

MO-IM synthetic future arbitrage backtest.ipynb
README.md
```

---

# Example Output

For every abnormal event

| Date | Basis | Primary Reason | Dominant Leg | Event |
|------|------:|---------------|-------------|-------|
|2024-01-18|81.0|Contract Roll|IM|Monthly Contract Roll|
|2024-09-30|228.6|Basis Jump|Mixed|National Day Holiday|

---

# Future Development

Planned improvements include

- Automatic financial news collection
- LLM-assisted event explanation
- PDF report generation
- Interactive dashboard
- Real-time monitoring
- Multi-asset support

---

# Disclaimer

This repository is intended for quantitative research and educational purposes only.

No investment advice is provided.

Market data are not included in this repository.
