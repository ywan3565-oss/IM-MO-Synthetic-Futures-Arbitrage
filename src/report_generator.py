from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# IM-MO Bilingual Research Report Generator
# ============================================================


DEFAULT_TITLES = {
    "EN": "IM-MO Synthetic Futures Basis Attribution Report",
    "CN": "IM-MO 合成期货基差异常归因研究报告",
}


TEXT = {
    "EN": {
        "report_description": (
            "This report analyses abnormal IM-MO synthetic futures basis "
            "observations through statistical detection, contract diagnostics, "
            "price-contribution decomposition and event-calendar matching."
        ),
        "causality_warning": (
            "The attribution framework identifies plausible mechanical and "
            "market explanations. Statistical coincidence and calendar matching "
            "do not establish strict causal relationships."
        ),
        "report_scope": "Report Scope",
        "first_event": "First abnormal event",
        "last_event": "Last abnormal event",
        "event_number": "Number of abnormal events",
        "executive_summary": "Executive Summary",
        "primary_reason_distribution": "Primary Attribution Distribution",
        "confidence_distribution": "Confidence Distribution",
        "dominant_leg_distribution": "Dominant-Leg Distribution",
        "event_type_distribution": "Matched Event-Type Distribution",
        "top_events": "Top Abnormal Events",
        "detailed_analysis": "Detailed Event Analysis",
        "market_statistics": "Market Statistics",
        "attribution": "Attribution",
        "contract_diagnostics": "Contract Diagnostics",
        "calendar_match": "Event Calendar Match",
        "research_explanation": "Research Explanation",
        "methodology": "Methodology Notes",
        "limitations": "Limitations",
        "disclaimer": "Disclaimer",
        "basis": "Basis",
        "z_score": "Z-score",
        "basis_change": "Basis change",
        "basis_change_z": "Basis-change Z-score",
        "primary_reason": "Primary reason",
        "primary_score": "Primary score",
        "confidence": "Confidence",
        "dominant_leg": "Dominant leg",
        "secondary_reasons": "Secondary reasons",
        "im_contribution": "IM contribution",
        "mo_contribution": "MO synthetic contribution",
        "im_share": "IM contribution share",
        "mo_share": "MO contribution share",
        "contract": "Contract",
        "previous_contract": "Previous contract",
        "strike": "Strike",
        "previous_strike": "Previous strike",
        "days_to_expiry": "Days to expiry",
        "event_date": "Event date",
        "event_type": "Event type",
        "event_name": "Event name",
        "importance": "Importance",
        "source": "Source",
        "event_distance": "Distance from abnormal date",
        "no_event": "No event-calendar match was found.",
        "days": "day(s)",
        "total_events": "Total abnormal events",
        "matched_events": "Matched calendar events",
        "matching_rate": "Event matching rate",
        "average_abs_z": "Average absolute Z-score",
        "median_abs_z": "Median absolute Z-score",
        "largest_abs_z": "Largest absolute Z-score",
        "largest_basis_change": "Largest absolute basis change",
        "high_confidence_events": "High-confidence events",
        "metric": "Metric",
        "value": "Value",
        "reason": "Primary Reason",
        "event_count": "Event Count",
        "percentage": "Percentage",
        "event_type_column": "Event Type",
        "confidence_column": "Confidence",
        "dominant_leg_column": "Dominant Leg",
        "date_column": "Date",
        "matched_event_column": "Matched Event",
        "none": "None",
        "unknown": "Unknown",
        "not_available": "N/A",
        "method_1": (
            "Abnormal basis observations are selected using the configured "
            "basis-level and daily-change Z-score thresholds."
        ),
        "method_2": (
            "Contract diagnostics assess rollover, near-expiry status and "
            "selected-strike changes."
        ),
        "method_3": (
            "Basis changes are decomposed into IM futures and MO synthetic "
            "futures contributions."
        ),
        "method_4": (
            "Event-calendar entries are matched within the configured date window."
        ),
        "method_5": (
            "Event matches provide contextual evidence rather than formal "
            "causal identification."
        ),
        "limitation_1": (
            "Daily settlement data may not capture intraday dislocations "
            "or bid-ask effects."
        ),
        "limitation_2": (
            "A selected active-contract series may contain rollover and "
            "strike-selection discontinuities."
        ),
        "limitation_3": (
            "Event-calendar coverage depends on the quality and completeness "
            "of manually or externally collected events."
        ),
        "limitation_4": (
            "Price-contribution decomposition explains mechanical basis changes "
            "but not necessarily their underlying economic causes."
        ),
        "disclaimer_text": (
            "This report is provided solely for educational and research purposes "
            "and does not constitute investment advice."
        ),
    },

    "CN": {
        "report_description": (
            "本报告对 IM 股指期货与 MO 期权合成期货之间的异常基差进行分析，"
            "涵盖统计异常检测、合约结构诊断、价格贡献分解以及事件日历匹配。"
        ),
        "causality_warning": (
            "本归因框架仅用于识别可能的机械性因素及市场背景。统计上的同期出现、"
            "价格贡献分解和事件日历匹配均不能单独证明严格的因果关系。"
        ),
        "report_scope": "报告范围",
        "first_event": "首个异常事件",
        "last_event": "最后一个异常事件",
        "event_number": "异常事件数量",
        "executive_summary": "核心摘要",
        "primary_reason_distribution": "主要归因原因分布",
        "confidence_distribution": "归因可信度分布",
        "dominant_leg_distribution": "主要驱动端分布",
        "event_type_distribution": "匹配事件类型分布",
        "top_events": "主要异常事件",
        "detailed_analysis": "异常事件详细分析",
        "market_statistics": "市场统计",
        "attribution": "归因分析",
        "contract_diagnostics": "合约结构诊断",
        "calendar_match": "事件日历匹配",
        "research_explanation": "研究解释",
        "methodology": "方法说明",
        "limitations": "研究局限",
        "disclaimer": "免责声明",
        "basis": "基差",
        "z_score": "Z-score",
        "basis_change": "基差变化",
        "basis_change_z": "基差变化 Z-score",
        "primary_reason": "主要原因",
        "primary_score": "主要原因评分",
        "confidence": "可信度",
        "dominant_leg": "主要驱动端",
        "secondary_reasons": "次要原因",
        "im_contribution": "IM 期货贡献",
        "mo_contribution": "MO 合成期货贡献",
        "im_share": "IM 贡献占比",
        "mo_share": "MO 贡献占比",
        "contract": "当前合约",
        "previous_contract": "前一合约",
        "strike": "当前行权价",
        "previous_strike": "前一行权价",
        "days_to_expiry": "距离到期天数",
        "event_date": "事件日期",
        "event_type": "事件类型",
        "event_name": "事件名称",
        "importance": "重要程度",
        "source": "来源",
        "event_distance": "与异常日期的距离",
        "no_event": "未在设定窗口内匹配到事件日历记录。",
        "days": "天",
        "total_events": "异常事件总数",
        "matched_events": "匹配到事件日历的数量",
        "matching_rate": "事件匹配率",
        "average_abs_z": "平均绝对 Z-score",
        "median_abs_z": "绝对 Z-score 中位数",
        "largest_abs_z": "最大绝对 Z-score",
        "largest_basis_change": "最大绝对基差变化",
        "high_confidence_events": "高可信度事件数量",
        "metric": "指标",
        "value": "结果",
        "reason": "主要归因原因",
        "event_count": "事件数量",
        "percentage": "占比",
        "event_type_column": "事件类型",
        "confidence_column": "可信度",
        "dominant_leg_column": "主要驱动端",
        "date_column": "日期",
        "matched_event_column": "匹配事件",
        "none": "无",
        "unknown": "未知",
        "not_available": "无数据",
        "method_1": (
            "异常事件根据基差水平 Z-score 和基差单日变化 Z-score 的设定阈值进行筛选。"
        ),
        "method_2": (
            "合约结构诊断包括主力合约切换、临近到期以及选取行权价变化等因素。"
        ),
        "method_3": (
            "基差变化被分解为 IM 期货价格变化贡献和 MO 合成期货价格变化贡献。"
        ),
        "method_4": (
            "事件日历按照设定的日期窗口与异常事件进行匹配。"
        ),
        "method_5": (
            "事件匹配仅用于补充市场背景，不代表完成了正式的因果识别。"
        ),
        "limitation_1": (
            "日度结算价无法完整反映盘中基差波动、买卖价差和成交冲击。"
        ),
        "limitation_2": (
            "最活跃合约和行权价的每日重新筛选可能引入换月或选券不连续。"
        ),
        "limitation_3": (
            "事件日历的覆盖范围取决于人工整理或外部数据源的完整性与准确性。"
        ),
        "limitation_4": (
            "价格贡献分解能够解释基差在计算上的变化来源，但不能直接说明其深层经济原因。"
        ),
        "disclaimer_text": (
            "本报告仅供教育和研究用途，不构成任何投资建议。"
        ),
    },
}


# ============================================================
# 1. 基础工具函数
# ============================================================

def _normalise_language(language: str) -> str:
    language = str(language).strip().upper()

    aliases = {
        "ENGLISH": "EN",
        "ENG": "EN",
        "中文": "CN",
        "CHINESE": "CN",
        "ZH": "CN",
        "ZH-CN": "CN",
    }

    language = aliases.get(language, language)

    if language not in TEXT:
        raise ValueError(
            "language 只能设置为 'EN' 或 'CN'。"
        )

    return language


def _safe_number(
    value,
    decimals: int = 2,
    missing_text: str = "N/A",
) -> str:
    if value is None or pd.isna(value):
        return missing_text

    return f"{float(value):.{decimals}f}"


def _safe_integer(
    value,
    missing_text: str = "N/A",
) -> str:
    if value is None or pd.isna(value):
        return missing_text

    return str(int(round(float(value))))


def _safe_percent(
    value,
    decimals: int = 2,
    missing_text: str = "N/A",
) -> str:
    if value is None or pd.isna(value):
        return missing_text

    return f"{float(value):.{decimals}f}%"


def _safe_date(
    value,
    missing_text: str = "N/A",
) -> str:
    if value is None or pd.isna(value):
        return missing_text

    return pd.Timestamp(value).strftime("%Y-%m-%d")


def _safe_text(
    value,
    default: str = "N/A",
) -> str:
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    text = str(value).strip()

    return text if text else default


def _bool_value(value) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "1",
            "yes",
            "y",
        }

    if value is None:
        return False

    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass

    return bool(value)


def dataframe_to_markdown(
    data: pd.DataFrame,
    empty_message: str,
) -> str:
    if data is None or data.empty:
        return empty_message

    return data.to_markdown(index=False)


# ============================================================
# 2. 数据校验与准备
# ============================================================

def validate_attribution_data(
    attribution: pd.DataFrame,
) -> None:
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
            f"归因结果缺少必要字段：{missing_columns}"
        )


def prepare_report_data(
    attribution: pd.DataFrame,
) -> pd.DataFrame:
    validate_attribution_data(attribution)

    data = attribution.copy()

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce",
    )

    date_columns = [
        "related_event_date",
    ]

    for column in date_columns:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column],
                errors="coerce",
            )

    numeric_columns = [
        "basis",
        "z_score",
        "basis_change",
        "basis_change_z",
        "IM_contribution",
        "MO_contribution",
        "IM_contribution_pct",
        "MO_contribution_pct",
        "days_to_expiry",
        "primary_score",
        "event_day_distance",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    data = (
        data
        .dropna(subset=["date"])
        .sort_values("date")
        .reset_index(drop=True)
    )

    data["abs_z_score"] = data["z_score"].abs()

    if "basis_change" in data.columns:
        data["abs_basis_change"] = (
            data["basis_change"].abs()
        )
    else:
        data["abs_basis_change"] = np.nan

    return data


# ============================================================
# 3. 中文字段翻译
# ============================================================

def _translate_reason(
    value,
    language: str,
) -> str:
    value = _safe_text(value, "Unknown")

    if language == "EN":
        return value

    mapping = {
        "Contract Roll": "合约换月",
        "Near Expiry": "临近到期",
        "ATM Strike Change": "行权价切换",
        "Basis Jump": "基差异常跳变",
        "Statistical Basis Shock": "统计性基差冲击",
        "Unexplained Basis Jump": "未解释的基差跳变",
        "Unexplained Market Movement": "未解释的市场变化",
        "IM Price Contribution": "IM 期货价格主导",
        "MO Synthetic Price Contribution": "MO 合成期货价格主导",
        "Mixed Price Contribution": "IM 与 MO 共同驱动",
        "Unknown": "未知",
    }

    return mapping.get(value, value)


def _translate_confidence(
    value,
    language: str,
) -> str:
    value = _safe_text(value, "Unknown")

    if language == "EN":
        return value

    mapping = {
        "High": "高",
        "Medium": "中",
        "Low": "低",
        "Unknown": "未知",
    }

    return mapping.get(value, value)


def _translate_dominant_leg(
    value,
    language: str,
) -> str:
    value = _safe_text(value, "Unknown")

    if language == "EN":
        return value

    mapping = {
        "IM": "IM 期货",
        "MO": "MO 合成期货",
        "MO Synthetic": "MO 合成期货",
        "Mixed": "IM 与 MO 共同驱动",
        "Unknown": "未知",
    }

    return mapping.get(value, value)


def _translate_event_type(
    value,
    language: str,
) -> str:
    value = _safe_text(value, "Unknown")

    if language == "EN":
        return value

    mapping = {
        "Contract": "合约事件",
        "Market": "市场事件",
        "Policy": "政策事件",
        "Calendar": "日历效应",
        "Holiday": "节假日事件",
        "Macro": "宏观事件",
        "Liquidity": "流动性事件",
        "Expiry": "到期事件",
        "Unknown": "未知",
    }

    return mapping.get(value, value)


# ============================================================
# 4. 统计摘要
# ============================================================

def build_executive_summary(
    data: pd.DataFrame,
    language: str,
) -> pd.DataFrame:
    txt = TEXT[language]

    total_events = len(data)

    matched_mask = (
        data["related_event_found"]
        .apply(_bool_value)
    )

    matched_events = int(matched_mask.sum())

    matching_rate = (
        matched_events / total_events * 100
        if total_events > 0
        else np.nan
    )

    average_abs_z = data["abs_z_score"].mean()
    median_abs_z = data["abs_z_score"].median()
    largest_abs_z = data["abs_z_score"].max()

    largest_basis_change = (
        data["abs_basis_change"].max()
        if "abs_basis_change" in data.columns
        else np.nan
    )

    high_confidence_events = (
        int(
            data["confidence"]
            .astype(str)
            .str.lower()
            .eq("high")
            .sum()
        )
        if "confidence" in data.columns
        else 0
    )

    return pd.DataFrame(
        {
            txt["metric"]: [
                txt["total_events"],
                txt["matched_events"],
                txt["matching_rate"],
                txt["average_abs_z"],
                txt["median_abs_z"],
                txt["largest_abs_z"],
                txt["largest_basis_change"],
                txt["high_confidence_events"],
            ],
            txt["value"]: [
                total_events,
                matched_events,
                _safe_percent(
                    matching_rate,
                    missing_text=txt["not_available"],
                ),
                _safe_number(
                    average_abs_z,
                    missing_text=txt["not_available"],
                ),
                _safe_number(
                    median_abs_z,
                    missing_text=txt["not_available"],
                ),
                _safe_number(
                    largest_abs_z,
                    missing_text=txt["not_available"],
                ),
                _safe_number(
                    largest_basis_change,
                    missing_text=txt["not_available"],
                ),
                high_confidence_events,
            ],
        }
    )


def build_reason_summary(
    data: pd.DataFrame,
    language: str,
) -> pd.DataFrame:
    txt = TEXT[language]

    summary = (
        data["primary_reason"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .rename_axis("reason")
        .reset_index(name="event_count")
    )

    total = summary["event_count"].sum()

    summary["percentage"] = (
        summary["event_count"] / total * 100
    )

    summary["reason"] = summary["reason"].apply(
        lambda value: _translate_reason(
            value,
            language,
        )
    )

    summary["percentage"] = summary["percentage"].map(
        lambda value: _safe_percent(value)
    )

    return summary.rename(
        columns={
            "reason": txt["reason"],
            "event_count": txt["event_count"],
            "percentage": txt["percentage"],
        }
    )


def build_confidence_summary(
    data: pd.DataFrame,
    language: str,
) -> pd.DataFrame:
    txt = TEXT[language]

    if "confidence" not in data.columns:
        return pd.DataFrame()

    summary = (
        data["confidence"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .rename_axis("confidence")
        .reset_index(name="event_count")
    )

    total = summary["event_count"].sum()

    summary["percentage"] = (
        summary["event_count"] / total * 100
    )

    summary["confidence"] = summary["confidence"].apply(
        lambda value: _translate_confidence(
            value,
            language,
        )
    )

    summary["percentage"] = summary["percentage"].map(
        lambda value: _safe_percent(value)
    )

    return summary.rename(
        columns={
            "confidence": txt["confidence_column"],
            "event_count": txt["event_count"],
            "percentage": txt["percentage"],
        }
    )


def build_dominant_leg_summary(
    data: pd.DataFrame,
    language: str,
) -> pd.DataFrame:
    txt = TEXT[language]

    if "dominant_leg" not in data.columns:
        return pd.DataFrame()

    summary = (
        data["dominant_leg"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .rename_axis("dominant_leg")
        .reset_index(name="event_count")
    )

    total = summary["event_count"].sum()

    summary["percentage"] = (
        summary["event_count"] / total * 100
    )

    summary["dominant_leg"] = summary["dominant_leg"].apply(
        lambda value: _translate_dominant_leg(
            value,
            language,
        )
    )

    summary["percentage"] = summary["percentage"].map(
        lambda value: _safe_percent(value)
    )

    return summary.rename(
        columns={
            "dominant_leg": txt["dominant_leg_column"],
            "event_count": txt["event_count"],
            "percentage": txt["percentage"],
        }
    )


def build_event_type_summary(
    data: pd.DataFrame,
    language: str,
) -> pd.DataFrame:
    txt = TEXT[language]

    matched = data.loc[
        data["related_event_found"].apply(_bool_value)
    ].copy()

    if (
        matched.empty
        or "related_event_type" not in matched.columns
    ):
        return pd.DataFrame()

    summary = (
        matched["related_event_type"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .rename_axis("event_type")
        .reset_index(name="event_count")
    )

    total = summary["event_count"].sum()

    summary["percentage"] = (
        summary["event_count"] / total * 100
    )

    summary["event_type"] = summary["event_type"].apply(
        lambda value: _translate_event_type(
            value,
            language,
        )
    )

    summary["percentage"] = summary["percentage"].map(
        lambda value: _safe_percent(value)
    )

    return summary.rename(
        columns={
            "event_type": txt["event_type_column"],
            "event_count": txt["event_count"],
            "percentage": txt["percentage"],
        }
    )


# ============================================================
# 5. Top Event 表格
# ============================================================

def build_top_event_table(
    data: pd.DataFrame,
    language: str,
    top_n: int,
) -> pd.DataFrame:
    txt = TEXT[language]

    desired_columns = [
        "date",
        "basis",
        "z_score",
        "basis_change",
        "primary_reason",
        "confidence",
        "dominant_leg",
        "related_event_name",
    ]

    available_columns = [
        column
        for column in desired_columns
        if column in data.columns
    ]

    top_events = (
        data
        .sort_values(
            "abs_z_score",
            ascending=False,
        )
        .head(top_n)
        [available_columns]
        .copy()
    )

    if "date" in top_events.columns:
        top_events["date"] = (
            top_events["date"]
            .dt.strftime("%Y-%m-%d")
        )

    if "primary_reason" in top_events.columns:
        top_events["primary_reason"] = (
            top_events["primary_reason"]
            .apply(
                lambda value: _translate_reason(
                    value,
                    language,
                )
            )
        )

    if "confidence" in top_events.columns:
        top_events["confidence"] = (
            top_events["confidence"]
            .apply(
                lambda value: _translate_confidence(
                    value,
                    language,
                )
            )
        )

    if "dominant_leg" in top_events.columns:
        top_events["dominant_leg"] = (
            top_events["dominant_leg"]
            .apply(
                lambda value: _translate_dominant_leg(
                    value,
                    language,
                )
            )
        )

    rename_map = {
        "date": txt["date_column"],
        "basis": txt["basis"],
        "z_score": txt["z_score"],
        "basis_change": txt["basis_change"],
        "primary_reason": txt["primary_reason"],
        "confidence": txt["confidence"],
        "dominant_leg": txt["dominant_leg"],
        "related_event_name": txt["matched_event_column"],
    }

    top_events = top_events.rename(
        columns=rename_map
    )

    for column in [
        txt["basis"],
        txt["z_score"],
        txt["basis_change"],
    ]:
        if column in top_events.columns:
            top_events[column] = top_events[column].map(
                lambda value: _safe_number(
                    value,
                    missing_text=txt["not_available"],
                )
            )

    if txt["matched_event_column"] in top_events.columns:
        top_events[txt["matched_event_column"]] = (
            top_events[txt["matched_event_column"]]
            .fillna(txt["none"])
            .replace("", txt["none"])
        )

    return top_events


# ============================================================
# 6. 自动生成中英文研究解释
# ============================================================

def build_bilingual_explanation(
    row: pd.Series,
    language: str,
) -> str:
    basis_change = row.get("basis_change", np.nan)
    im_contribution = row.get("IM_contribution", np.nan)
    mo_contribution = row.get("MO_contribution", np.nan)
    im_pct = row.get("IM_contribution_pct", np.nan)
    mo_pct = row.get("MO_contribution_pct", np.nan)

    primary_reason = _safe_text(
        row.get("primary_reason"),
        "Unknown",
    )

    related_event_found = _bool_value(
        row.get("related_event_found")
    )

    if language == "EN":
        if pd.isna(basis_change):
            movement_text = (
                "Insufficient data were available to calculate "
                "the daily basis movement."
            )
        elif basis_change > 0:
            movement_text = (
                f"The IM-MO basis increased by "
                f"{basis_change:.2f} points."
            )
        elif basis_change < 0:
            movement_text = (
                f"The IM-MO basis decreased by "
                f"{abs(basis_change):.2f} points."
            )
        else:
            movement_text = (
                "The IM-MO basis remained unchanged."
            )

        if pd.notna(im_pct) and im_pct >= 65:
            contribution_text = (
                f"The movement was primarily driven by the IM futures leg. "
                f"IM contributed {im_contribution:+.2f} points, accounting "
                f"for {im_pct:.1f}% of the total absolute contribution."
            )
        elif pd.notna(mo_pct) and mo_pct >= 65:
            contribution_text = (
                f"The movement was primarily driven by the MO synthetic "
                f"futures leg. MO contributed {mo_contribution:+.2f} points, "
                f"accounting for {mo_pct:.1f}% of the total absolute contribution."
            )
        elif (
            pd.notna(im_contribution)
            and pd.notna(mo_contribution)
        ):
            contribution_text = (
                f"Both legs contributed materially. IM contributed "
                f"{im_contribution:+.2f} points and MO synthetic futures "
                f"contributed {mo_contribution:+.2f} points."
            )
        else:
            contribution_text = (
                "Insufficient leg-level data were available for contribution analysis."
            )

        reason_mapping = {
            "Contract Roll": (
                "A contract roll occurred on the same date. Part of the "
                "basis movement may therefore reflect pricing differences "
                "between the old and new contracts."
            ),
            "Near Expiry": (
                "The selected contracts were close to expiry, when convergence, "
                "settlement and liquidity effects may become more important."
            ),
            "ATM Strike Change": (
                "The selected MO strike changed, which may have introduced "
                "a discontinuity into the synthetic futures series."
            ),
            "Basis Jump": (
                "The daily basis movement was statistically unusual, but no "
                "higher-scoring structural explanation was identified."
            ),
            "Statistical Basis Shock": (
                "The daily basis movement was statistically unusual, but no "
                "higher-scoring structural explanation was identified."
            ),
            "Unexplained Basis Jump": (
                "No clear structural cause was detected. Additional market, "
                "volatility, liquidity or news data may be required."
            ),
        }

        reason_text = reason_mapping.get(
            primary_reason,
            (
                "No dominant structural explanation was identified. "
                "Additional market information may be required."
            ),
        )

        if related_event_found:
            event_name = _safe_text(
                row.get("related_event_name"),
                "Unknown event",
            )
            event_type = _safe_text(
                row.get("related_event_type"),
                "Unknown",
            )
            event_date = _safe_date(
                row.get("related_event_date"),
            )
            distance = row.get(
                "event_day_distance",
                np.nan,
            )

            if pd.isna(distance):
                timing_text = "near the abnormal observation"
            elif distance == 0:
                timing_text = "on the same date"
            elif distance > 0:
                timing_text = (
                    f"{int(distance)} day(s) after the abnormal observation"
                )
            else:
                timing_text = (
                    f"{abs(int(distance))} day(s) before the abnormal observation"
                )

            event_text = (
                f"The event calendar identified '{event_name}' "
                f"({event_type}) on {event_date}, {timing_text}. "
                "This provides contextual evidence but does not establish causality."
            )
        else:
            event_text = (
                "No external event was matched within the configured calendar window."
            )

        return " ".join(
            [
                movement_text,
                contribution_text,
                reason_text,
                event_text,
            ]
        )

    # 中文解释
    if pd.isna(basis_change):
        movement_text = (
            "当前数据不足以计算该日基差变化。"
        )
    elif basis_change > 0:
        movement_text = (
            f"当日 IM-MO 基差上升 {basis_change:.2f} 点。"
        )
    elif basis_change < 0:
        movement_text = (
            f"当日 IM-MO 基差下降 {abs(basis_change):.2f} 点。"
        )
    else:
        movement_text = (
            "当日 IM-MO 基差没有发生变化。"
        )

    if pd.notna(im_pct) and im_pct >= 65:
        contribution_text = (
            f"此次基差变化主要由 IM 期货端驱动。"
            f"IM 期货贡献为 {im_contribution:+.2f} 点，"
            f"占两端绝对贡献之和的 {im_pct:.1f}%。"
        )
    elif pd.notna(mo_pct) and mo_pct >= 65:
        contribution_text = (
            f"此次基差变化主要由 MO 合成期货端驱动。"
            f"MO 合成期货贡献为 {mo_contribution:+.2f} 点，"
            f"占两端绝对贡献之和的 {mo_pct:.1f}%。"
        )
    elif (
        pd.notna(im_contribution)
        and pd.notna(mo_contribution)
    ):
        contribution_text = (
            f"IM 与 MO 两端均对基差变化产生了明显影响。"
            f"IM 期货贡献为 {im_contribution:+.2f} 点，"
            f"MO 合成期货贡献为 {mo_contribution:+.2f} 点。"
        )
    else:
        contribution_text = (
            "当前缺少足够的分腿价格变化数据，无法完成贡献分解。"
        )

    reason_mapping = {
        "Contract Roll": (
            "当天检测到合约换月，因此部分基差变化可能来自旧合约与新合约之间的定价差异，"
            "不能直接视为真实的市场错价。"
        ),
        "Near Expiry": (
            "所选合约已经临近到期，此时价格收敛、结算方式以及流动性变化可能对基差产生更大影响。"
        ),
        "ATM Strike Change": (
            "当天选取的 MO 行权价发生变化，可能导致合成期货序列出现选券不连续。"
        ),
        "Basis Jump": (
            "该日基差变化在统计上十分异常，但现有结构性指标没有识别出更明确的原因。"
        ),
        "Statistical Basis Shock": (
            "该日基差变化在统计上十分异常，但现有结构性指标没有识别出更明确的原因。"
        ),
        "Unexplained Basis Jump": (
            "当前没有识别出明确的结构性原因，需要进一步结合成交量、隐含波动率、"
            "流动性及相关新闻进行分析。"
        ),
    }

    reason_text = reason_mapping.get(
        primary_reason,
        (
            "当前未识别出占主导地位的结构性原因，"
            "需要进一步结合外部市场信息进行验证。"
        ),
    )

    if related_event_found:
        event_name = _safe_text(
            row.get("related_event_name"),
            "未知事件",
        )
        event_type = _translate_event_type(
            row.get("related_event_type"),
            "CN",
        )
        event_date = _safe_date(
            row.get("related_event_date"),
            "无数据",
        )
        distance = row.get(
            "event_day_distance",
            np.nan,
        )

        if pd.isna(distance):
            timing_text = "发生在异常日期附近"
        elif distance == 0:
            timing_text = "与异常事件发生在同一天"
        elif distance > 0:
            timing_text = f"发生在异常日期之后 {int(distance)} 天"
        else:
            timing_text = f"发生在异常日期之前 {abs(int(distance))} 天"

        event_text = (
            f"事件日历匹配到“{event_name}”（{event_type}），"
            f"事件日期为 {event_date}，{timing_text}。"
            "该信息仅用于补充市场背景，不能单独证明其与基差异常之间存在因果关系。"
        )
    else:
        event_text = (
            "在设定的日期窗口内未匹配到外部事件记录。"
        )

    return "".join(
        [
            movement_text,
            contribution_text,
            reason_text,
            event_text,
        ]
    )


# ============================================================
# 7. 图片插入
# ============================================================

def collect_available_figures(
    report_output_path: Path,
    figure_paths: dict[str, str | Path] | None,
) -> dict[str, str]:
    if not figure_paths:
        return {}

    available = {}
    report_directory = report_output_path.parent

    for title, path_value in figure_paths.items():
        figure_path = Path(path_value)

        if not figure_path.exists():
            continue

        try:
            relative_path = figure_path.relative_to(
                report_directory
            )
        except ValueError:
            relative_path = figure_path

        available[title] = relative_path.as_posix()

    return available


def build_figure_section(
    title: str,
    relative_path: str,
) -> list[str]:
    return [
        f"## {title}",
        "",
        f"![{title}]({relative_path})",
        "",
    ]


# ============================================================
# 8. 单个事件详情
# ============================================================

def build_event_detail_section(
    row: pd.Series,
    language: str,
) -> list[str]:
    txt = TEXT[language]

    event_date = _safe_date(
        row.get("date"),
        txt["not_available"],
    )

    primary_reason = _translate_reason(
        row.get("primary_reason"),
        language,
    )

    confidence = _translate_confidence(
        row.get("confidence"),
        language,
    )

    dominant_leg = _translate_dominant_leg(
        row.get("dominant_leg"),
        language,
    )

    lines = [
        f"### {event_date}",
        "",
        f"#### {txt['market_statistics']}",
        "",
        (
            f"- **{txt['basis']}：** "
            f"{_safe_number(row.get('basis'), missing_text=txt['not_available'])}"
        ),
        (
            f"- **{txt['z_score']}：** "
            f"{_safe_number(row.get('z_score'), missing_text=txt['not_available'])}"
        ),
        (
            f"- **{txt['basis_change']}：** "
            f"{_safe_number(row.get('basis_change'), missing_text=txt['not_available'])}"
        ),
        (
            f"- **{txt['basis_change_z']}：** "
            f"{_safe_number(row.get('basis_change_z'), missing_text=txt['not_available'])}"
        ),
        "",
        f"#### {txt['attribution']}",
        "",
        f"- **{txt['primary_reason']}：** {primary_reason}",
        (
            f"- **{txt['primary_score']}：** "
            f"{_safe_number(row.get('primary_score'), missing_text=txt['not_available'])}"
        ),
        f"- **{txt['confidence']}：** {confidence}",
        f"- **{txt['dominant_leg']}：** {dominant_leg}",
        (
            f"- **{txt['secondary_reasons']}：** "
            f"{_safe_text(row.get('secondary_reasons'), txt['none'])}"
        ),
    ]

    if "IM_contribution" in row.index:
        lines.append(
            (
                f"- **{txt['im_contribution']}：** "
                f"{_safe_number(row.get('IM_contribution'), missing_text=txt['not_available'])}"
            )
        )

    if "MO_contribution" in row.index:
        lines.append(
            (
                f"- **{txt['mo_contribution']}：** "
                f"{_safe_number(row.get('MO_contribution'), missing_text=txt['not_available'])}"
            )
        )

    if "IM_contribution_pct" in row.index:
        lines.append(
            (
                f"- **{txt['im_share']}：** "
                f"{_safe_percent(row.get('IM_contribution_pct'), missing_text=txt['not_available'])}"
            )
        )

    if "MO_contribution_pct" in row.index:
        lines.append(
            (
                f"- **{txt['mo_share']}：** "
                f"{_safe_percent(row.get('MO_contribution_pct'), missing_text=txt['not_available'])}"
            )
        )

    lines.extend(
        [
            "",
            f"#### {txt['contract_diagnostics']}",
            "",
            (
                f"- **{txt['contract']}：** "
                f"{_safe_text(row.get('contract'), txt['not_available'])}"
            ),
            (
                f"- **{txt['previous_contract']}：** "
                f"{_safe_text(row.get('previous_contract'), txt['not_available'])}"
            ),
            (
                f"- **{txt['strike']}：** "
                f"{_safe_number(row.get('strike'), missing_text=txt['not_available'])}"
            ),
            (
                f"- **{txt['previous_strike']}：** "
                f"{_safe_number(row.get('previous_strike'), missing_text=txt['not_available'])}"
            ),
            (
                f"- **{txt['days_to_expiry']}：** "
                f"{_safe_integer(row.get('days_to_expiry'), missing_text=txt['not_available'])}"
            ),
            "",
            f"#### {txt['calendar_match']}",
            "",
        ]
    )

    if _bool_value(row.get("related_event_found")):
        lines.extend(
            [
                (
                    f"- **{txt['event_date']}：** "
                    f"{_safe_date(row.get('related_event_date'), txt['not_available'])}"
                ),
                (
                    f"- **{txt['event_type']}：** "
                    f"{_translate_event_type(row.get('related_event_type'), language)}"
                ),
                (
                    f"- **{txt['event_name']}：** "
                    f"{_safe_text(row.get('related_event_name'), txt['not_available'])}"
                ),
                (
                    f"- **{txt['importance']}：** "
                    f"{_safe_text(row.get('related_event_importance'), txt['not_available'])}"
                ),
                (
                    f"- **{txt['source']}：** "
                    f"{_safe_text(row.get('related_event_source'), txt['not_available'])}"
                ),
                (
                    f"- **{txt['event_distance']}：** "
                    f"{_safe_integer(row.get('event_day_distance'), txt['not_available'])} "
                    f"{txt['days']}"
                ),
            ]
        )
    else:
        lines.append(f"- {txt['no_event']}")

    explanation = build_bilingual_explanation(
        row,
        language,
    )

    lines.extend(
        [
            "",
            f"#### {txt['research_explanation']}",
            "",
            explanation,
            "",
            "---",
            "",
        ]
    )

    return lines


# ============================================================
# 9. 完整双语报告函数
# ============================================================

def generate_research_report(
    attribution: pd.DataFrame,
    output_path: str | Path,
    language: str = "EN",
    project_title: str | None = None,
    top_events: int | None = 10,
    figure_paths: dict[str, str | Path] | None = None,
    include_all_events: bool = False,
) -> Path:
    """
    生成英文或中文 Markdown 研究报告。

    Parameters
    ----------
    attribution:
        attribution_with_events 或 attribution_v2 结果。

    output_path:
        Markdown 输出文件路径。

    language:
        "EN" 或 "CN"。

    project_title:
        自定义报告标题。None 时使用默认标题。

    top_events:
        按绝对 Z-score 选取前 N 个事件写入详细分析。
        None 表示全部。

    figure_paths:
        可选图片路径字典，例如：

        {
            "Basis Curve": "outputs/figures/basis_curve.png",
            "Reason Distribution": "outputs/figures/reason_distribution.png",
        }

    include_all_events:
        True 时忽略 top_events，展示全部事件。
    """

    language = _normalise_language(language)
    txt = TEXT[language]

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = prepare_report_data(attribution)

    if project_title is None:
        project_title = DEFAULT_TITLES[language]

    executive_summary = build_executive_summary(
        data,
        language,
    )

    reason_summary = build_reason_summary(
        data,
        language,
    )

    confidence_summary = build_confidence_summary(
        data,
        language,
    )

    dominant_leg_summary = build_dominant_leg_summary(
        data,
        language,
    )

    event_type_summary = build_event_type_summary(
        data,
        language,
    )

    top_n_for_table = (
        len(data)
        if top_events is None
        else min(top_events, len(data))
    )

    top_event_table = build_top_event_table(
        data,
        language,
        top_n=top_n_for_table,
    )

    available_figures = collect_available_figures(
        report_output_path=output_path,
        figure_paths=figure_paths,
    )

    lines = [
        f"# {project_title}",
        "",
        txt["report_description"],
        "",
        f"> {txt['causality_warning']}",
        "",
        "---",
        "",
        f"## {txt['report_scope']}",
        "",
        (
            f"- **{txt['first_event']}：** "
            f"{_safe_date(data['date'].min(), txt['not_available'])}"
        ),
        (
            f"- **{txt['last_event']}：** "
            f"{_safe_date(data['date'].max(), txt['not_available'])}"
        ),
        (
            f"- **{txt['event_number']}：** "
            f"{len(data)}"
        ),
        "",
        f"## {txt['executive_summary']}",
        "",
        dataframe_to_markdown(
            executive_summary,
            f"_{txt['not_available']}_",
        ),
        "",
        f"## {txt['primary_reason_distribution']}",
        "",
        dataframe_to_markdown(
            reason_summary,
            f"_{txt['not_available']}_",
        ),
        "",
        f"## {txt['confidence_distribution']}",
        "",
        dataframe_to_markdown(
            confidence_summary,
            f"_{txt['not_available']}_",
        ),
        "",
        f"## {txt['dominant_leg_distribution']}",
        "",
        dataframe_to_markdown(
            dominant_leg_summary,
            f"_{txt['not_available']}_",
        ),
        "",
        f"## {txt['event_type_distribution']}",
        "",
        dataframe_to_markdown(
            event_type_summary,
            f"_{txt['not_available']}_",
        ),
        "",
        (
            f"## {txt['top_events']} "
            f"({len(top_event_table)})"
        ),
        "",
        dataframe_to_markdown(
            top_event_table,
            f"_{txt['not_available']}_",
        ),
        "",
    ]

    for title, relative_path in available_figures.items():
        lines.extend(
            build_figure_section(
                title=title,
                relative_path=relative_path,
            )
        )

    lines.extend(
        [
            f"## {txt['detailed_analysis']}",
            "",
        ]
    )

    if include_all_events or top_events is None:
        event_details = data.copy()
    else:
        event_details = (
            data
            .sort_values(
                "abs_z_score",
                ascending=False,
            )
            .head(top_events)
            .sort_values("date")
        )

    for _, row in event_details.iterrows():
        lines.extend(
            build_event_detail_section(
                row,
                language,
            )
        )

    lines.extend(
        [
            f"## {txt['methodology']}",
            "",
            f"1. {txt['method_1']}",
            f"2. {txt['method_2']}",
            f"3. {txt['method_3']}",
            f"4. {txt['method_4']}",
            f"5. {txt['method_5']}",
            "",
            f"## {txt['limitations']}",
            "",
            f"- {txt['limitation_1']}",
            f"- {txt['limitation_2']}",
            f"- {txt['limitation_3']}",
            f"- {txt['limitation_4']}",
            "",
            f"## {txt['disclaimer']}",
            "",
            txt["disclaimer_text"],
            "",
        ]
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("=" * 70)

    if language == "CN":
        print("IM-MO 中文研究报告生成器")
        print("=" * 70)
        print("全部异常事件数量：", len(data))
        print("报告详情事件数量：", len(event_details))
        print("成功插入图片数量：", len(available_figures))
        print("输出文件：", output_path)
    else:
        print("IM-MO English Research Report Generator")
        print("=" * 70)
        print("Total abnormal events:", len(data))
        print("Detailed events:", len(event_details))
        print("Inserted figures:", len(available_figures))
        print("Output file:", output_path)

    return output_path


# ============================================================
# 10. 一键生成中英文两份报告
# ============================================================

def generate_bilingual_reports(
    attribution: pd.DataFrame,
    english_output_path: str | Path = (
        "outputs/IM_MO_Research_Report.md"
    ),
    chinese_output_path: str | Path = (
        "outputs/IM_MO_研究报告.md"
    ),
    english_title: str | None = None,
    chinese_title: str | None = None,
    top_events: int | None = 10,
    figure_paths: dict[str, str | Path] | None = None,
    include_all_events: bool = False,
) -> tuple[Path, Path]:
    """
    一次生成英文和中文两份 Markdown 报告。
    """

    english_path = generate_research_report(
        attribution=attribution,
        output_path=english_output_path,
        language="EN",
        project_title=english_title,
        top_events=top_events,
        figure_paths=figure_paths,
        include_all_events=include_all_events,
    )

    chinese_path = generate_research_report(
        attribution=attribution,
        output_path=chinese_output_path,
        language="CN",
        project_title=chinese_title,
        top_events=top_events,
        figure_paths=figure_paths,
        include_all_events=include_all_events,
    )

    print("=" * 70)
    print("中英文报告均已生成")
    print("English:", english_path)
    print("中文：", chinese_path)

    return english_path, chinese_path