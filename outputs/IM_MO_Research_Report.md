# IM-MO Synthetic Futures Basis Attribution Report

This report analyses abnormal IM-MO synthetic futures basis observations through statistical detection, contract diagnostics, price-contribution decomposition and event-calendar matching.

> The attribution framework identifies plausible mechanical and market explanations. Statistical coincidence and calendar matching do not establish strict causal relationships.

---

## Report Scope

- **First abnormal event：** 2023-05-25
- **Last abnormal event：** 2026-07-20
- **Number of abnormal events：** 30

## Executive Summary

| Metric                        | Value   |
|:------------------------------|:--------|
| Total abnormal events         | 30      |
| Matched calendar events       | 5       |
| Event matching rate           | 16.67%  |
| Average absolute Z-score      | 3.68    |
| Median absolute Z-score       | 3.12    |
| Largest absolute Z-score      | 17.65   |
| Largest absolute basis change | 181.40  |
| High-confidence events        | 2       |

## Primary Attribution Distribution

| Primary Reason           |   Event Count | Percentage   |
|:-------------------------|--------------:|:-------------|
| Basis Jump               |            22 | 73.33%       |
| Mixed Price Contribution |             5 | 16.67%       |
| Contract Roll            |             2 | 6.67%        |
| IM Price Contribution    |             1 | 3.33%        |

## Confidence Distribution

| Confidence   |   Event Count | Percentage   |
|:-------------|--------------:|:-------------|
| Medium       |            23 | 76.67%       |
| Low          |             5 | 16.67%       |
| High         |             2 | 6.67%        |

## Dominant-Leg Distribution

| Dominant Leg   |   Event Count | Percentage   |
|:---------------|--------------:|:-------------|
| Mixed          |            17 | 56.67%       |
| MO Synthetic   |             7 | 23.33%       |
| IM             |             6 | 20.00%       |

## Matched Event-Type Distribution

| Event Type   |   Event Count | Percentage   |
|:-------------|--------------:|:-------------|
| Contract     |             1 | 20.00%       |
| Market       |             1 | 20.00%       |
| Policy       |             1 | 20.00%       |
| Calendar     |             1 | 20.00%       |
| Holiday      |             1 | 20.00%       |

## Top Abnormal Events (10)

| Date       |   Basis |   Z-score |   Basis change | Primary reason           | Confidence   | Dominant leg   | Matched Event                |
|:-----------|--------:|----------:|---------------:|:-------------------------|:-------------|:---------------|:-----------------------------|
| 2024-09-30 |   228.6 |     17.65 |          168   | Basis Jump               | Medium       | Mixed          | Quarter-End Rebalancing      |
| 2024-01-18 |    81   |      6.9  |          127.2 | Contract Roll            | High         | IM             | Monthly Contract Roll        |
| 2024-02-05 |  -107.8 |     -6.64 |         -142.2 | Basis Jump               | Medium       | Mixed          | Small-Cap Market Stress      |
| 2025-04-07 |   -99.4 |     -6.44 |         -106.6 | Basis Jump               | Medium       | Mixed          | None                         |
| 2024-09-26 |    55.8 |      5.36 |           67.2 | Basis Jump               | Medium       | Mixed          | Policy Stimulus Announcement |
| 2026-02-02 |   -55.8 |     -4.29 |          -69   | Basis Jump               | Medium       | Mixed          | None                         |
| 2025-09-23 |    64.4 |      4.1  |           39.6 | Mixed Price Contribution | Low          | Mixed          | None                         |
| 2024-01-22 |   -54   |     -4.07 |          -38   | Mixed Price Contribution | Low          | Mixed          | None                         |
| 2026-07-20 |    94.2 |      3.86 |          152.4 | Basis Jump               | Medium       | Mixed          | None                         |
| 2026-05-21 |   -56   |     -3.68 |          -82.6 | Basis Jump               | Medium       | Mixed          | None                         |

## Detailed Event Analysis

### 2024-01-18

#### Market Statistics

- **Basis：** 81.00
- **Z-score：** 6.90
- **Basis change：** 127.20
- **Basis-change Z-score：** 7.44

#### Attribution

- **Primary reason：** Contract Roll
- **Primary score：** 100.00
- **Confidence：** High
- **Dominant leg：** IM
- **Secondary reasons：** Basis Jump | IM Price Contribution
- **IM contribution：** 201.80
- **MO synthetic contribution：** -74.60

#### Contract Diagnostics

- **Contract：** 202402
- **Previous contract：** 202401
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- **Event date：** 2024-01-18
- **Event type：** Contract
- **Event name：** Monthly Contract Roll
- **Importance：** High
- **Source：** Manual
- **Distance from abnormal date：** 0 day(s)

#### Research Explanation

The IM-MO basis increased by 127.20 points. Both legs contributed materially. IM contributed +201.80 points and MO synthetic futures contributed -74.60 points. A contract roll occurred on the same date. Part of the basis movement may therefore reflect pricing differences between the old and new contracts. The event calendar identified 'Monthly Contract Roll' (Contract) on 2024-01-18, on the same date. This provides contextual evidence but does not establish causality.

---

### 2024-01-22

#### Market Statistics

- **Basis：** -54.00
- **Z-score：** -4.07
- **Basis change：** -38.00
- **Basis-change Z-score：** -1.64

#### Attribution

- **Primary reason：** Mixed Price Contribution
- **Primary score：** 45.00
- **Confidence：** Low
- **Dominant leg：** Mixed
- **Secondary reasons：** None
- **IM contribution：** 361.60
- **MO synthetic contribution：** -399.60

#### Contract Diagnostics

- **Contract：** 202402
- **Previous contract：** 202402
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- No event-calendar match was found.

#### Research Explanation

The IM-MO basis decreased by 38.00 points. Both legs contributed materially. IM contributed +361.60 points and MO synthetic futures contributed -399.60 points. No dominant structural explanation was identified. Additional market information may be required. No external event was matched within the configured calendar window.

---

### 2024-02-05

#### Market Statistics

- **Basis：** -107.80
- **Z-score：** -6.64
- **Basis change：** -142.20
- **Basis-change Z-score：** -5.69

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** 202.80
- **MO synthetic contribution：** -345.00

#### Contract Diagnostics

- **Contract：** 202402
- **Previous contract：** 202402
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- **Event date：** 2024-02-05
- **Event type：** Market
- **Event name：** Small-Cap Market Stress
- **Importance：** High
- **Source：** Manual
- **Distance from abnormal date：** 0 day(s)

#### Research Explanation

The IM-MO basis decreased by 142.20 points. Both legs contributed materially. IM contributed +202.80 points and MO synthetic futures contributed -345.00 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. The event calendar identified 'Small-Cap Market Stress' (Market) on 2024-02-05, on the same date. This provides contextual evidence but does not establish causality.

---

### 2024-09-26

#### Market Statistics

- **Basis：** 55.80
- **Z-score：** 5.36
- **Basis change：** 67.20
- **Basis-change Z-score：** 4.53

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** -184.60
- **MO synthetic contribution：** 251.80

#### Contract Diagnostics

- **Contract：** 202410
- **Previous contract：** 202410
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- **Event date：** 2024-09-24
- **Event type：** Policy
- **Event name：** Policy Stimulus Announcement
- **Importance：** High
- **Source：** Manual
- **Distance from abnormal date：** -2 day(s)

#### Research Explanation

The IM-MO basis increased by 67.20 points. Both legs contributed materially. IM contributed -184.60 points and MO synthetic futures contributed +251.80 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. The event calendar identified 'Policy Stimulus Announcement' (Policy) on 2024-09-24, 2 day(s) before the abnormal observation. This provides contextual evidence but does not establish causality.

---

### 2024-09-30

#### Market Statistics

- **Basis：** 228.60
- **Z-score：** 17.65
- **Basis change：** 168.00
- **Basis-change Z-score：** 10.32

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** -516.20
- **MO synthetic contribution：** 684.20

#### Contract Diagnostics

- **Contract：** 202410
- **Previous contract：** 202410
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- **Event date：** 2024-09-30
- **Event type：** Calendar
- **Event name：** Quarter-End Rebalancing
- **Importance：** Medium
- **Source：** Manual
- **Distance from abnormal date：** 0 day(s)

#### Research Explanation

The IM-MO basis increased by 168.00 points. Both legs contributed materially. IM contributed -516.20 points and MO synthetic futures contributed +684.20 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. The event calendar identified 'Quarter-End Rebalancing' (Calendar) on 2024-09-30, on the same date. This provides contextual evidence but does not establish causality.

---

### 2025-04-07

#### Market Statistics

- **Basis：** -99.40
- **Z-score：** -6.44
- **Basis change：** -106.60
- **Basis-change Z-score：** -4.31

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** 603.60
- **MO synthetic contribution：** -710.20

#### Contract Diagnostics

- **Contract：** 202506
- **Previous contract：** 202506
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- No event-calendar match was found.

#### Research Explanation

The IM-MO basis decreased by 106.60 points. Both legs contributed materially. IM contributed +603.60 points and MO synthetic futures contributed -710.20 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. No external event was matched within the configured calendar window.

---

### 2025-09-23

#### Market Statistics

- **Basis：** 64.40
- **Z-score：** 4.10
- **Basis change：** 39.60
- **Basis-change Z-score：** 1.95

#### Attribution

- **Primary reason：** Mixed Price Contribution
- **Primary score：** 45.00
- **Confidence：** Low
- **Dominant leg：** Mixed
- **Secondary reasons：** None
- **IM contribution：** 135.20
- **MO synthetic contribution：** -95.60

#### Contract Diagnostics

- **Contract：** 202512
- **Previous contract：** 202512
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- No event-calendar match was found.

#### Research Explanation

The IM-MO basis increased by 39.60 points. Both legs contributed materially. IM contributed +135.20 points and MO synthetic futures contributed -95.60 points. No dominant structural explanation was identified. Additional market information may be required. No external event was matched within the configured calendar window.

---

### 2026-02-02

#### Market Statistics

- **Basis：** -55.80
- **Z-score：** -4.29
- **Basis change：** -69.00
- **Basis-change Z-score：** -3.64

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** 304.60
- **MO synthetic contribution：** -373.60

#### Contract Diagnostics

- **Contract：** 202603
- **Previous contract：** 202603
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- No event-calendar match was found.

#### Research Explanation

The IM-MO basis decreased by 69.00 points. Both legs contributed materially. IM contributed +304.60 points and MO synthetic futures contributed -373.60 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. No external event was matched within the configured calendar window.

---

### 2026-05-21

#### Market Statistics

- **Basis：** -56.00
- **Z-score：** -3.68
- **Basis change：** -82.60
- **Basis-change Z-score：** -3.42

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** 175.20
- **MO synthetic contribution：** -257.80

#### Contract Diagnostics

- **Contract：** 202606
- **Previous contract：** 202606
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- No event-calendar match was found.

#### Research Explanation

The IM-MO basis decreased by 82.60 points. Both legs contributed materially. IM contributed +175.20 points and MO synthetic futures contributed -257.80 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. No external event was matched within the configured calendar window.

---

### 2026-07-20

#### Market Statistics

- **Basis：** 94.20
- **Z-score：** 3.86
- **Basis change：** 152.40
- **Basis-change Z-score：** 5.24

#### Attribution

- **Primary reason：** Basis Jump
- **Primary score：** 80.00
- **Confidence：** Medium
- **Dominant leg：** Mixed
- **Secondary reasons：** Mixed Price Contribution
- **IM contribution：** 364.00
- **MO synthetic contribution：** -211.60

#### Contract Diagnostics

- **Contract：** 202609
- **Previous contract：** 202609
- **Strike：** N/A
- **Previous strike：** N/A
- **Days to expiry：** N/A

#### Event Calendar Match

- No event-calendar match was found.

#### Research Explanation

The IM-MO basis increased by 152.40 points. Both legs contributed materially. IM contributed +364.00 points and MO synthetic futures contributed -211.60 points. The daily basis movement was statistically unusual, but no higher-scoring structural explanation was identified. No external event was matched within the configured calendar window.

---

## Methodology Notes

1. Abnormal basis observations are selected using the configured basis-level and daily-change Z-score thresholds.
2. Contract diagnostics assess rollover, near-expiry status and selected-strike changes.
3. Basis changes are decomposed into IM futures and MO synthetic futures contributions.
4. Event-calendar entries are matched within the configured date window.
5. Event matches provide contextual evidence rather than formal causal identification.

## Limitations

- Daily settlement data may not capture intraday dislocations or bid-ask effects.
- A selected active-contract series may contain rollover and strike-selection discontinuities.
- Event-calendar coverage depends on the quality and completeness of manually or externally collected events.
- Price-contribution decomposition explains mechanical basis changes but not necessarily their underlying economic causes.

## Disclaimer

This report is provided solely for educational and research purposes and does not constitute investment advice.
