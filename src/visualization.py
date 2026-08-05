from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _safe_number(
    value,
    decimals: int = 2,
) -> str:
    """
    安全格式化数值。
    """

    if pd.isna(value):
        return "N/A"

    return f"{float(value):.{decimals}f}"


def _safe_date(
    value,
) -> str:
    """
    安全格式化日期。
    """

    if pd.isna(value):
        return "N/A"

    return pd.Timestamp(value).strftime(
        "%Y-%m-%d"
    )


def build_summary_table(
    attribution: pd.DataFrame,
) -> pd.DataFrame:
    """
    生成报告摘要统计。
    """

    total_events = len(attribution)

    matched_events = int(
        attribution[
            "related_event_found"
        ].fillna(False).sum()
    )

    matched_rate = (
        matched_events / total_events * 100
        if total_events > 0
        else np.nan
    )

    average_abs_z = (
        attribution["z_score"]
        .abs()
        .mean()
    )

    largest_abs_z = (
        attribution["z_score"]
        .abs()
        .max()
    )

    largest_basis_change = (
        attribution["basis_change"]
        .abs()
        .max()
    )

    summary = pd.DataFrame(
        {
            "Metric": [
                "Total abnormal events",
                "Matched calendar events",
                "Event matching rate",
                "Average absolute Z-score",
                "Largest absolute Z-score",
                "Largest absolute basis change",
            ],
            "Value": [
                total_events,
                matched_events,
                (
                    f"{matched_rate:.2f}%"
                    if pd.notna(matched_rate)
                    else "N/A"
                ),
                _safe_number(
                    average_abs_z,
                    2,
                ),
                _safe_number(
                    largest_abs_z,
                    2,
                ),
                _safe_number(
                    largest_basis_change,
                    2,
                ),
            ],
        }
    )

    return summary


def build_reason_summary(
    attribution: pd.DataFrame,
) -> pd.DataFrame:
    """
    统计主要归因原因。
    """

    if "primary_reason" not in attribution.columns:
        return pd.DataFrame(
            columns=[
                "Primary Reason",
                "Event Count",
                "Percentage",
            ]
        )

    reason_summary = (
        attribution[
            "primary_reason"
        ]
        .fillna("Unknown")
        .value_counts()
        .rename_axis(
            "Primary Reason"
        )
        .reset_index(
            name="Event Count"
        )
    )

    total = reason_summary[
        "Event Count"
    ].sum()

    reason_summary[
        "Percentage"
    ] = (
        reason_summary[
            "Event Count"
        ]
        / total
        * 100
    )

    reason_summary[
        "Percentage"
    ] = reason_summary[
        "Percentage"
    ].map(
        lambda value: f"{value:.2f}%"
    )

    return reason_summary


def build_event_type_summary(
    attribution: pd.DataFrame,
) -> pd.DataFrame:
    """
    统计匹配到的事件类型。
    """

    matched = attribution.loc[
        attribution[
            "related_event_found"
        ].fillna(False)
    ].copy()

    if matched.empty:
        return pd.DataFrame(
            columns=[
                "Event Type",
                "Event Count",
                "Percentage",
            ]
        )

    event_summary = (
        matched[
            "related_event_type"
        ]
        .replace(
            "",
            "Unknown",
        )
        .fillna(
            "Unknown"
        )
        .value_counts()
        .rename_axis(
            "Event Type"
        )
        .reset_index(
            name="Event Count"
        )
    )

    total = event_summary[
        "Event Count"
    ].sum()

    event_summary[
        "Percentage"
    ] = (
        event_summary[
            "Event Count"
        ]
        / total
        * 100
    )

    event_summary[
        "Percentage"
    ] = event_summary[
        "Percentage"
    ].map(
        lambda value: f"{value:.2f}%"
    )

    return event_summary


def dataframe_to_markdown(
    data: pd.DataFrame,
) -> str:
    """
    将DataFrame转换为Markdown表格。
    """

    if data.empty:
        return "_No records available._"

    return data.to_markdown(
        index=False
    )


def build_event_section(
    row: pd.Series,
) -> list[str]:
    """
    生成单个异常事件的Markdown内容。
    """

    lines = []

    event_date = _safe_date(
        row.get("date")
    )

    lines.extend(
        [
            f"### {event_date}",
            "",
            (
                f"- **Basis:** "
                f"{_safe_number(row.get('basis'))}"
            ),
            (
                f"- **Z-score:** "
                f"{_safe_number(row.get('z_score'))}"
            ),
            (
                f"- **Basis change:** "
                f"{_safe_number(row.get('basis_change'))}"
            ),
            (
                f"- **Primary reason:** "
                f"{row.get('primary_reason', 'Unknown')}"
            ),
            (
                f"- **Confidence:** "
                f"{row.get('confidence', 'Unknown')}"
            ),
            (
                f"- **Dominant leg:** "
                f"{row.get('dominant_leg', 'Unknown')}"
            ),
        ]
    )

    if "IM_contribution" in row.index:
        lines.append(
            (
                f"- **IM contribution:** "
                f"{_safe_number(row.get('IM_contribution'))}"
            )
        )

    if "MO_contribution" in row.index:
        lines.append(
            (
                f"- **MO synthetic contribution:** "
                f"{_safe_number(row.get('MO_contribution'))}"
            )
        )

    if "days_to_expiry" in row.index:
        lines.append(
            (
                f"- **Days to expiry:** "
                f"{_safe_number(row.get('days_to_expiry'), 0)}"
            )
        )

    related_event_found = bool(
        row.get(
            "related_event_found",
            False,
        )
    )

    lines.extend(
        [
            "",
            "#### Event Calendar Match",
            "",
        ]
    )

    if related_event_found:
        lines.extend(
            [
                (
                    f"- **Event date:** "
                    f"{_safe_date(row.get('related_event_date'))}"
                ),
                (
                    f"- **Event type:** "
                    f"{row.get('related_event_type', '')}"
                ),
                (
                    f"- **Event name:** "
                    f"{row.get('related_event_name', '')}"
                ),
                (
                    f"- **Importance:** "
                    f"{row.get('related_event_importance', '')}"
                ),
                (
                    f"- **Source:** "
                    f"{row.get('related_event_source', '')}"
                ),
                (
                    f"- **Distance from abnormal date:** "
                    f"{row.get('event_day_distance', 'N/A')} day(s)"
                ),
            ]
        )
    else:
        lines.append(
            "- No event-calendar match was found."
        )

    lines.extend(
        [
            "",
            "#### Explanation",
            "",
        ]
    )

    explanation = row.get(
        "event_context_explanation",
        row.get(
            "research_explanation",
            row.get(
                "explanation",
                "",
            ),
        ),
    )

    lines.extend(
        [
            str(explanation),
            "",
            "---",
            "",
        ]
    )

    return lines


def generate_research_report(
    attribution: pd.DataFrame,
    output_path: str | Path = (
        "outputs/IM_MO_Research_Report.md"
    ),
    project_title: str = (
        "IM-MO Basis Attribution Research Report"
    ),
    top_events: int | None = None,
) -> Path:
    """
    自动生成Markdown研究报告。

    Parameters
    ----------
    attribution:
        attribution_with_events结果。

    output_path:
        Markdown输出路径。

    project_title:
        报告标题。

    top_events:
        只展示绝对z-score最大的前N个事件。
        None表示展示全部。
    """

    required_columns = [
        "date",
        "basis",
        "z_score",
        "primary_reason",
        "related_event_found",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in attribution.columns
    ]

    if missing_columns:
        raise KeyError(
            f"归因结果缺少字段：{missing_columns}"
        )

    data = attribution.copy()

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce",
    )

    data = (
        data
        .dropna(subset=["date"])
        .sort_values("date")
        .reset_index(drop=True)
    )

    summary_table = build_summary_table(
        data
    )

    reason_summary = build_reason_summary(
        data
    )

    event_type_summary = (
        build_event_type_summary(
            data
        )
    )

    event_details = data.copy()

    if top_events is not None:
        event_details = (
            event_details
            .assign(
                abs_z_score=event_details[
                    "z_score"
                ].abs()
            )
            .sort_values(
                "abs_z_score",
                ascending=False,
            )
            .head(top_events)
            .sort_values("date")
        )

    lines = [
        f"# {project_title}",
        "",
        (
            "This report summarises abnormal IM-MO basis "
            "observations, structural attribution, price "
            "contribution analysis and event-calendar matching."
        ),
        "",
        (
            "> Event-calendar matches provide contextual "
            "evidence only and do not establish causality."
        ),
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        dataframe_to_markdown(
            summary_table
        ),
        "",
        "## Primary Attribution Summary",
        "",
        dataframe_to_markdown(
            reason_summary
        ),
        "",
        "## Matched Event-Type Summary",
        "",
        dataframe_to_markdown(
            event_type_summary
        ),
        "",
        "## Event Details",
        "",
    ]

    for _, row in event_details.iterrows():
        lines.extend(
            build_event_section(
                row
            )
        )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("=" * 70)
    print("Research Report Generator")
    print("=" * 70)
    print(
        "报告事件数量：",
        len(event_details),
    )
    print(
        "输出文件：",
        output_path,
    )

    return output_path