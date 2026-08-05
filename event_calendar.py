from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "event_type",
    "event_name",
    "importance",
    "source",
]


def load_event_calendar(
    file_path: str | Path = "data/event_calendar.csv",
) -> pd.DataFrame:
    """
    读取并清洗事件日历。
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"找不到事件日历文件：{file_path}"
        )

    calendar = pd.read_csv(file_path)

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in calendar.columns
    ]

    if missing_columns:
        raise KeyError(
            f"事件日历缺少字段：{missing_columns}"
        )

    calendar["date"] = pd.to_datetime(
        calendar["date"],
        errors="coerce",
    )

    calendar = (
        calendar
        .dropna(subset=["date"])
        .sort_values("date")
        .reset_index(drop=True)
    )

    for col in [
        "event_type",
        "event_name",
        "importance",
        "source",
    ]:
        calendar[col] = (
            calendar[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return calendar


def _importance_score(
    importance: str,
) -> int:
    """
    将重要性转换成数值，便于排序。
    """

    mapping = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    return mapping.get(
        str(importance).strip().lower(),
        0,
    )


def match_one_date(
    abnormal_date: pd.Timestamp,
    event_calendar: pd.DataFrame,
    window_days: int = 2,
) -> dict:
    """
    为单个异常日期匹配附近事件。
    """

    abnormal_date = pd.Timestamp(
        abnormal_date
    )

    start_date = (
        abnormal_date
        - pd.Timedelta(days=window_days)
    )

    end_date = (
        abnormal_date
        + pd.Timedelta(days=window_days)
    )

    matched = event_calendar.loc[
        event_calendar["date"].between(
            start_date,
            end_date,
        )
    ].copy()

    if matched.empty:
        return {
            "related_event_found": False,
            "related_event_date": pd.NaT,
            "related_event_type": "",
            "related_event_name": "",
            "related_event_importance": "",
            "related_event_source": "",
            "event_day_distance": pd.NA,
            "all_related_events": "",
        }

    matched["day_distance"] = (
        matched["date"]
        - abnormal_date
    ).dt.days

    matched["abs_day_distance"] = (
        matched["day_distance"].abs()
    )

    matched["importance_score"] = (
        matched["importance"]
        .apply(_importance_score)
    )

    matched = matched.sort_values(
        [
            "abs_day_distance",
            "importance_score",
        ],
        ascending=[
            True,
            False,
        ],
    )

    primary = matched.iloc[0]

    all_related_events = " | ".join(
        matched["date"].dt.strftime(
            "%Y-%m-%d"
        )
        + ": "
        + matched["event_name"]
        + " ["
        + matched["event_type"]
        + "]"
    )

    return {
        "related_event_found": True,
        "related_event_date": primary["date"],
        "related_event_type": primary["event_type"],
        "related_event_name": primary["event_name"],
        "related_event_importance": primary["importance"],
        "related_event_source": primary["source"],
        "event_day_distance": int(
            primary["day_distance"]
        ),
        "all_related_events": all_related_events,
    }


def attach_event_calendar(
    attribution_results: pd.DataFrame,
    event_calendar: pd.DataFrame,
    date_col: str = "date",
    window_days: int = 2,
) -> pd.DataFrame:
    """
    将事件日历信息附加到归因结果。
    """

    result = attribution_results.copy()

    result[date_col] = pd.to_datetime(
        result[date_col],
        errors="coerce",
    )

    matched_records = []

    for _, row in result.iterrows():
        record = match_one_date(
            abnormal_date=row[date_col],
            event_calendar=event_calendar,
            window_days=window_days,
        )

        matched_records.append(record)

    matched_df = pd.DataFrame(
        matched_records
    )

    return pd.concat(
        [
            result.reset_index(drop=True),
            matched_df.reset_index(drop=True),
        ],
        axis=1,
    )


def add_event_context(
    matched_results: pd.DataFrame,
) -> pd.DataFrame:
    """
    在已有解释后面补充事件背景。
    """

    result = matched_results.copy()

    if "research_explanation" in result.columns:
        base_col = "research_explanation"
    elif "explanation" in result.columns:
        base_col = "explanation"
    else:
        base_col = None

    def build_text(row: pd.Series) -> str:
        base_text = (
            str(row.get(base_col, "")).strip()
            if base_col is not None
            else ""
        )

        if not bool(
            row.get(
                "related_event_found",
                False,
            )
        ):
            event_text = (
                "No event was found within the configured "
                "event-calendar window."
            )

        else:
            event_date = pd.Timestamp(
                row["related_event_date"]
            ).strftime("%Y-%m-%d")

            distance = row[
                "event_day_distance"
            ]

            if distance == 0:
                timing_text = "on the same date"
            elif distance > 0:
                timing_text = (
                    f"{distance} day(s) after "
                    "the abnormal observation"
                )
            else:
                timing_text = (
                    f"{abs(distance)} day(s) before "
                    "the abnormal observation"
                )

            event_text = (
                f"The event calendar identified "
                f"'{row['related_event_name']}' "
                f"({row['related_event_type']}, "
                f"{row['related_event_importance']}) "
                f"on {event_date}, {timing_text}. "
                "This is contextual evidence only and "
                "does not establish causality."
            )

        return (
            base_text
            + " "
            + event_text
        ).strip()

    result["event_context_explanation"] = (
        result.apply(
            build_text,
            axis=1,
        )
    )

    return result


def run_event_calendar_matching(
    attribution_results: pd.DataFrame,
    calendar_path: str | Path = (
        "data/event_calendar.csv"
    ),
    window_days: int = 2,
    output_path: str | Path = (
        "outputs/attribution_with_events.csv"
    ),
) -> pd.DataFrame:
    """
    一键完成读取、匹配、补充解释和导出。
    """

    calendar = load_event_calendar(
        file_path=calendar_path
    )

    matched = attach_event_calendar(
        attribution_results=attribution_results,
        event_calendar=calendar,
        date_col="date",
        window_days=window_days,
    )

    enriched = add_event_context(
        matched_results=matched
    )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    enriched.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )

    print("=" * 70)
    print("Event Calendar Matching")
    print("=" * 70)
    print(
        "异常事件数量：",
        len(enriched),
    )
    print(
        "成功匹配数量：",
        int(
            enriched[
                "related_event_found"
            ].sum()
        ),
    )
    print(
        "输出文件：",
        output_path,
    )

    return enriched