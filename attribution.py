from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


# ============================================================
# IM-MO Basis Attribution Engine
#
# 默认定义：
# basis = IM_settle - MO_synthetic
#
# 如果你的basis定义相反：
# basis = MO_synthetic - IM_settle
#
# 调用时设置：
# basis_definition="MO_MINUS_IM"
# ============================================================


COLUMN_ALIASES = {
    "date": [
        "date",
        "日期",
        "trade_date",
        "trading_date",
    ],
    "basis": [
        "basis",
        "价差",
    ],
    "im_price": [
        "IM_settle",
        "IM_close",
        "IM_price",
        "im_settle",
        "im_close",
    ],
    "mo_price": [
        "MO_synthetic",
        "synthetic",
        "synthetic_future",
        "MO_synthetic_price",
    ],
    "contract": [
        "交割月份",
        "contract",
        "delivery_month",
        "IM_contract",
        "IM_code",
    ],
    "expiry": [
        "expiry",
        "到期日",
        "expiration_date",
        "最后行权日",
    ],
    "strike": [
        "行权价格",
        "strike",
        "strike_price",
        "K",
    ],
    "rolling_mean": [
        "rolling_mean",
        "basis_mean",
    ],
    "rolling_std": [
        "rolling_std",
        "basis_std",
    ],
    "z_score": [
        "z_score",
        "zscore",
    ],
}


def _find_column(
    df: pd.DataFrame,
    aliases: Iterable[str],
    required: bool = False,
) -> str | None:
    """
    从多个候选列名中寻找实际存在的列。
    """

    for column in aliases:
        if column in df.columns:
            return column

    if required:
        raise KeyError(
            f"找不到所需字段，候选列名为：{list(aliases)}"
        )

    return None


def _normalise_contract(value) -> str:
    """
    把交割月份、合约代码统一转成字符串，便于比较。
    """

    if pd.isna(value):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y%m")

    text = str(value).strip()

    # 处理 2024.0、202409.0 等情况
    if text.endswith(".0"):
        text = text[:-2]

    return text


def _confidence_from_score(score: float) -> str:
    if score >= 90:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def _basis_direction_label(
    basis_change: float,
) -> str:
    if basis_change > 0:
        return "Basis widened upward"
    if basis_change < 0:
        return "Basis moved downward"
    return "Basis unchanged"


def prepare_attribution_data(
    final_data: pd.DataFrame,
    basis_definition: str = "IM_MINUS_MO",
    rolling_window: int = 100,
    min_periods: int = 40,
) -> pd.DataFrame:
    """
    整理归因分析所需的数据。

    Parameters
    ----------
    final_data:
        原始回测数据。

    basis_definition:
        "IM_MINUS_MO":
            basis = IM_settle - MO_synthetic

        "MO_MINUS_IM":
            basis = MO_synthetic - IM_settle
    """

    df = final_data.copy()

    # --------------------------------------------------------
    # 1. 日期
    # --------------------------------------------------------

    date_col = _find_column(
        df,
        COLUMN_ALIASES["date"],
        required=False,
    )

    if date_col is None:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()

            first_col = df.columns[0]

            df = df.rename(
                columns={
                    first_col: "date"
                }
            )

            date_col = "date"

        else:
            raise KeyError(
                "找不到日期列，并且index也不是DatetimeIndex。"
            )

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce",
    )

    # --------------------------------------------------------
    # 2. 找出主要字段
    # --------------------------------------------------------

    basis_col = _find_column(
        df,
        COLUMN_ALIASES["basis"],
        required=True,
    )

    im_col = _find_column(
        df,
        COLUMN_ALIASES["im_price"],
        required=True,
    )

    mo_col = _find_column(
        df,
        COLUMN_ALIASES["mo_price"],
        required=True,
    )

    contract_col = _find_column(
        df,
        COLUMN_ALIASES["contract"],
        required=False,
    )

    expiry_col = _find_column(
        df,
        COLUMN_ALIASES["expiry"],
        required=False,
    )

    strike_col = _find_column(
        df,
        COLUMN_ALIASES["strike"],
        required=False,
    )

    rolling_mean_col = _find_column(
        df,
        COLUMN_ALIASES["rolling_mean"],
        required=False,
    )

    rolling_std_col = _find_column(
        df,
        COLUMN_ALIASES["rolling_std"],
        required=False,
    )

    z_col = _find_column(
        df,
        COLUMN_ALIASES["z_score"],
        required=False,
    )

    # --------------------------------------------------------
    # 3. 标准化列名
    # --------------------------------------------------------

    rename_map = {
        date_col: "date",
        basis_col: "basis",
        im_col: "IM_price",
        mo_col: "MO_price",
    }

    if contract_col is not None:
        rename_map[contract_col] = "contract"

    if expiry_col is not None:
        rename_map[expiry_col] = "expiry"

    if strike_col is not None:
        rename_map[strike_col] = "strike"

    if rolling_mean_col is not None:
        rename_map[rolling_mean_col] = "rolling_mean"

    if rolling_std_col is not None:
        rename_map[rolling_std_col] = "rolling_std"

    if z_col is not None:
        rename_map[z_col] = "z_score"

    df = df.rename(columns=rename_map)

    # --------------------------------------------------------
    # 4. 数值格式
    # --------------------------------------------------------

    numeric_columns = [
        "basis",
        "IM_price",
        "MO_price",
        "strike",
        "rolling_mean",
        "rolling_std",
        "z_score",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    if "expiry" in df.columns:
        df["expiry"] = pd.to_datetime(
            df["expiry"],
            errors="coerce",
        )

    if "contract" in df.columns:
        df["contract"] = df["contract"].map(
            _normalise_contract
        )

    df = (
        df
        .dropna(
            subset=[
                "date",
                "basis",
                "IM_price",
                "MO_price",
            ]
        )
        .sort_values("date")
        .drop_duplicates(
            subset=["date"],
            keep="last",
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # 5. Basis定义验算
    # --------------------------------------------------------

    basis_definition = basis_definition.upper()

    if basis_definition == "IM_MINUS_MO":

        df["basis_check"] = (
            df["IM_price"]
            - df["MO_price"]
        )

    elif basis_definition == "MO_MINUS_IM":

        df["basis_check"] = (
            df["MO_price"]
            - df["IM_price"]
        )

    else:
        raise ValueError(
            "basis_definition只能是 "
            "'IM_MINUS_MO' 或 'MO_MINUS_IM'。"
        )

    df["basis_definition_error"] = (
        df["basis"]
        - df["basis_check"]
    )

    # --------------------------------------------------------
    # 6. 价格变化及Basis变化
    # --------------------------------------------------------

    df["IM_change"] = df["IM_price"].diff()
    df["MO_change"] = df["MO_price"].diff()
    df["basis_change"] = df["basis"].diff()

    df["IM_return"] = df["IM_price"].pct_change()
    df["MO_return"] = df["MO_price"].pct_change()

    # --------------------------------------------------------
    # 7. 合约切换
    # --------------------------------------------------------

    if "contract" in df.columns:

        df["previous_contract"] = (
            df["contract"].shift(1)
        )

        df["contract_changed"] = (
            df["contract"].ne(
                df["previous_contract"]
            )
            & df["previous_contract"].notna()
            & df["contract"].ne("")
            & df["previous_contract"].ne("")
        )

    else:
        df["previous_contract"] = pd.NA
        df["contract_changed"] = False

    # --------------------------------------------------------
    # 8. 行权价切换
    # --------------------------------------------------------

    if "strike" in df.columns:

        df["previous_strike"] = (
            df["strike"].shift(1)
        )

        df["strike_changed"] = (
            df["strike"].ne(
                df["previous_strike"]
            )
            & df["previous_strike"].notna()
        )

        df["strike_change"] = (
            df["strike"]
            - df["previous_strike"]
        )

    else:
        df["previous_strike"] = np.nan
        df["strike_changed"] = False
        df["strike_change"] = np.nan

    # --------------------------------------------------------
    # 9. 距离到期日
    # --------------------------------------------------------

    if "expiry" in df.columns:

        df["days_to_expiry"] = (
            df["expiry"]
            - df["date"]
        ).dt.days

    else:
        df["days_to_expiry"] = np.nan

    # --------------------------------------------------------
    # 10. z-score
    # --------------------------------------------------------

    if "rolling_mean" not in df.columns:

        df["rolling_mean"] = (
            df["basis"]
            .rolling(
                rolling_window,
                min_periods=min_periods,
            )
            .mean()
            .shift(1)
        )

    if "rolling_std" not in df.columns:

        df["rolling_std"] = (
            df["basis"]
            .rolling(
                rolling_window,
                min_periods=min_periods,
            )
            .std()
            .shift(1)
        )

    if "z_score" not in df.columns:

        df["z_score"] = (
            df["basis"]
            - df["rolling_mean"]
        ) / df["rolling_std"].replace(
            0,
            np.nan,
        )

    # Basis单日变化的滚动标准差
    df["basis_change_std"] = (
        df["basis_change"]
        .rolling(
            rolling_window,
            min_periods=min_periods,
        )
        .std()
        .shift(1)
    )

    df["basis_change_z"] = (
        df["basis_change"]
        / df["basis_change_std"].replace(
            0,
            np.nan,
        )
    )

    return df


def detect_abnormal_basis(
    prepared_data: pd.DataFrame,
    z_threshold: float = 2.0,
    change_z_threshold: float = 2.0,
    top_n: int | None = 30,
    min_gap_days: int = 3,
) -> pd.DataFrame:
    """
    检测两类异常：

    1. Basis水平异常：
       abs(z_score) >= z_threshold

    2. Basis单日变化异常：
       abs(basis_change_z) >= change_z_threshold
    """

    df = prepared_data.copy()

    df["level_anomaly"] = (
        df["z_score"].abs()
        >= z_threshold
    )

    df["change_anomaly"] = (
        df["basis_change_z"].abs()
        >= change_z_threshold
    )

    abnormal = df.loc[
        df["level_anomaly"]
        | df["change_anomaly"]
    ].copy()

    abnormal["anomaly_strength"] = (
        abnormal[
            [
                "z_score",
                "basis_change_z",
            ]
        ]
        .abs()
        .max(axis=1)
    )

    abnormal = abnormal.sort_values(
        "anomaly_strength",
        ascending=False,
    )

    selected_rows = []
    selected_dates = []

    for _, row in abnormal.iterrows():

        current_date = pd.Timestamp(
            row["date"]
        )

        belongs_to_existing_event = any(
            abs(
                (
                    current_date
                    - selected_date
                ).days
            )
            < min_gap_days
            for selected_date in selected_dates
        )

        if belongs_to_existing_event:
            continue

        selected_rows.append(row)
        selected_dates.append(current_date)

        if (
            top_n is not None
            and len(selected_rows) >= top_n
        ):
            break

    if not selected_rows:
        return abnormal.head(0)

    return (
        pd.DataFrame(selected_rows)
        .sort_values("date")
        .reset_index(drop=True)
    )


def _calculate_price_contribution(
    row: pd.Series,
    basis_definition: str,
) -> tuple[float, float]:
    """
    把Basis变化分解成IM和MO两部分贡献。

    若：
        basis = IM - MO

    则：
        Δbasis = ΔIM - ΔMO

    IM贡献 = ΔIM
    MO贡献 = -ΔMO
    """

    im_change = row.get("IM_change", np.nan)
    mo_change = row.get("MO_change", np.nan)

    if pd.isna(im_change) or pd.isna(mo_change):
        return np.nan, np.nan

    basis_definition = basis_definition.upper()

    if basis_definition == "IM_MINUS_MO":

        im_contribution = im_change
        mo_contribution = -mo_change

    else:

        im_contribution = -im_change
        mo_contribution = mo_change

    return (
        float(im_contribution),
        float(mo_contribution),
    )


def attribute_one_event(
    row: pd.Series,
    basis_definition: str = "IM_MINUS_MO",
    near_expiry_days: int = 5,
    large_basis_change_z: float = 2.0,
) -> dict:
    """
    对单个异常日期打分并生成解释。
    """

    reasons = []

    # --------------------------------------------------------
    # 1. 合约换月
    # --------------------------------------------------------

    if bool(row.get("contract_changed", False)):

        reasons.append(
            {
                "reason": "Contract Roll",
                "score": 100,
                "explanation": (
                    f"Contract changed from "
                    f"{row.get('previous_contract', '')} "
                    f"to {row.get('contract', '')}. "
                    "The abnormal basis may be affected by "
                    "differences between old and new contract pricing."
                ),
            }
        )

    # --------------------------------------------------------
    # 2. 临近到期
    # --------------------------------------------------------

    days_to_expiry = row.get(
        "days_to_expiry",
        np.nan,
    )

    if (
        pd.notna(days_to_expiry)
        and 0 <= days_to_expiry <= near_expiry_days
    ):

        reasons.append(
            {
                "reason": "Near Expiry",
                "score": 85,
                "explanation": (
                    f"The selected contracts were only "
                    f"{int(days_to_expiry)} calendar days "
                    "from expiry. Expiry-related liquidity, "
                    "settlement and convergence effects may "
                    "have influenced the basis."
                ),
            }
        )

    # --------------------------------------------------------
    # 3. 行权价变化
    # --------------------------------------------------------

    if bool(row.get("strike_changed", False)):

        strike_change = row.get(
            "strike_change",
            np.nan,
        )

        explanation = (
            f"The selected MO strike changed from "
            f"{row.get('previous_strike', np.nan)} "
            f"to {row.get('strike', np.nan)}."
        )

        if pd.notna(strike_change):
            explanation += (
                f" The strike change was "
                f"{strike_change:+.2f} points."
            )

        explanation += (
            " Part of the basis movement may therefore "
            "reflect contract-selection discontinuity "
            "rather than pure market mispricing."
        )

        reasons.append(
            {
                "reason": "ATM Strike Change",
                "score": 75,
                "explanation": explanation,
            }
        )

    # --------------------------------------------------------
    # 4. 单日Basis剧烈变化
    # --------------------------------------------------------

    basis_change_z = row.get(
        "basis_change_z",
        np.nan,
    )

    if (
        pd.notna(basis_change_z)
        and abs(basis_change_z)
        >= large_basis_change_z
    ):

        reasons.append(
            {
                "reason": "Basis Jump",
                "score": min(
                    80,
                    50 + abs(basis_change_z) * 10,
                ),
                "explanation": (
                    f"The daily basis change was "
                    f"{row.get('basis_change', np.nan):+.2f} "
                    f"points, equivalent to "
                    f"{basis_change_z:+.2f} standard deviations "
                    "of historical daily basis changes."
                ),
            }
        )

    # --------------------------------------------------------
    # 5. IM / MO贡献分解
    # --------------------------------------------------------

    im_contribution, mo_contribution = (
        _calculate_price_contribution(
            row=row,
            basis_definition=basis_definition,
        )
    )

    dominant_leg = "Unknown"
    contribution_explanation = (
        "Insufficient price-change data."
    )

    if (
        pd.notna(im_contribution)
        and pd.notna(mo_contribution)
    ):

        total_absolute_contribution = (
            abs(im_contribution)
            + abs(mo_contribution)
        )

        if total_absolute_contribution > 0:

            im_share = (
                abs(im_contribution)
                / total_absolute_contribution
            )

            mo_share = (
                abs(mo_contribution)
                / total_absolute_contribution
            )

            if im_share >= 0.65:
                dominant_leg = "IM"
            elif mo_share >= 0.65:
                dominant_leg = "MO Synthetic"
            else:
                dominant_leg = "Mixed"

            contribution_explanation = (
                f"IM contribution to the basis change was "
                f"{im_contribution:+.2f} points, while the "
                f"MO synthetic contribution was "
                f"{mo_contribution:+.2f} points. "
                f"The dominant leg was {dominant_leg}."
            )

            reasons.append(
                {
                    "reason": (
                        f"{dominant_leg} Price Contribution"
                    ),
                    "score": (
                        65
                        if dominant_leg != "Mixed"
                        else 45
                    ),
                    "explanation": (
                        contribution_explanation
                    ),
                }
            )

    # --------------------------------------------------------
    # 6. 如果没有找到明确结构原因
    # --------------------------------------------------------

    if not reasons:

        reasons.append(
            {
                "reason": "Unexplained Market Movement",
                "score": 20,
                "explanation": (
                    "No contract roll, near-expiry condition "
                    "or strike change was detected. External "
                    "market, volatility or liquidity information "
                    "may be required for further attribution."
                ),
            }
        )

    reasons = sorted(
        reasons,
        key=lambda item: item["score"],
        reverse=True,
    )

    primary = reasons[0]

    secondary_reasons = [
        item["reason"]
        for item in reasons[1:]
    ]

    full_explanation = " ".join(
        item["explanation"]
        for item in reasons
    )

    return {
        "date": row["date"],
        "basis": row.get("basis", np.nan),
        "z_score": row.get("z_score", np.nan),
        "basis_change": row.get(
            "basis_change",
            np.nan,
        ),
        "basis_change_z": row.get(
            "basis_change_z",
            np.nan,
        ),
        "basis_direction": (
            _basis_direction_label(
                row.get("basis_change", 0)
            )
        ),
        "contract": row.get(
            "contract",
            pd.NA,
        ),
        "previous_contract": row.get(
            "previous_contract",
            pd.NA,
        ),
        "strike": row.get(
            "strike",
            np.nan,
        ),
        "previous_strike": row.get(
            "previous_strike",
            np.nan,
        ),
        "days_to_expiry": row.get(
            "days_to_expiry",
            np.nan,
        ),
        "IM_change": row.get(
            "IM_change",
            np.nan,
        ),
        "MO_change": row.get(
            "MO_change",
            np.nan,
        ),
        "IM_contribution": im_contribution,
        "MO_contribution": mo_contribution,
        "dominant_leg": dominant_leg,
        "primary_reason": primary["reason"],
        "primary_score": primary["score"],
        "confidence": (
            _confidence_from_score(
                primary["score"]
            )
        ),
        "secondary_reasons": " | ".join(
            secondary_reasons
        ),
        "explanation": full_explanation,
    }


def run_basis_attribution(
    final_data: pd.DataFrame,
    basis_definition: str = "IM_MINUS_MO",
    z_threshold: float = 2.0,
    change_z_threshold: float = 2.0,
    top_n: int | None = 30,
    min_gap_days: int = 3,
    near_expiry_days: int = 5,
    output_dir: str = "outputs",
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """
    一键运行整个归因流程。

    Returns
    -------
    prepared_data
    abnormal_events
    attribution_results
    """

    prepared_data = prepare_attribution_data(
        final_data=final_data,
        basis_definition=basis_definition,
    )

    max_basis_error = (
        prepared_data[
            "basis_definition_error"
        ]
        .abs()
        .max()
    )

    print("=" * 70)
    print("IM-MO Basis Attribution Engine")
    print("=" * 70)
    print(
        "Basis定义最大验算误差：",
        max_basis_error,
    )

    abnormal_events = detect_abnormal_basis(
        prepared_data=prepared_data,
        z_threshold=z_threshold,
        change_z_threshold=change_z_threshold,
        top_n=top_n,
        min_gap_days=min_gap_days,
    )

    attribution_records = []

    for _, row in abnormal_events.iterrows():

        result = attribute_one_event(
            row=row,
            basis_definition=basis_definition,
            near_expiry_days=near_expiry_days,
            large_basis_change_z=(
                change_z_threshold
            ),
        )

        attribution_records.append(result)

    attribution_results = pd.DataFrame(
        attribution_records
    )

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    prepared_data.to_csv(
        output_path
        / "attribution_prepared_data.csv",
        index=False,
        encoding="utf-8-sig",
    )

    abnormal_events.to_csv(
        output_path
        / "abnormal_basis_events.csv",
        index=False,
        encoding="utf-8-sig",
    )

    attribution_results.to_csv(
        output_path
        / "basis_attribution_results.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"异常事件数量：{len(abnormal_events)}"
    )

    print(
        "归因结果已保存至："
    )

    print(
        output_path
        / "basis_attribution_results.csv"
    )

    return (
        prepared_data,
        abnormal_events,
        attribution_results,
    )


def export_attribution_markdown(
    attribution_results: pd.DataFrame,
    output_path: str = (
        "outputs/basis_attribution_report.md"
    ),
) -> Path:
    """
    输出GitHub可直接查看的Markdown报告。
    """

    file_path = Path(output_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        "# IM-MO Basis Attribution Report",
        "",
        (
            "This report automatically attributes "
            "abnormal IM-MO basis observations using "
            "contract, expiry, strike and price-contribution data."
        ),
        "",
        (
            "> The attribution results identify plausible "
            "mechanical or market explanations. They do not "
            "establish strict causal relationships."
        ),
        "",
    ]

    for _, row in attribution_results.iterrows():

        event_date = pd.Timestamp(
            row["date"]
        ).strftime("%Y-%m-%d")

        lines.extend(
            [
                f"## {event_date}",
                "",
                f"- **Basis:** {row['basis']:.4f}",
                f"- **Z-score:** {row['z_score']:.4f}",
                (
                    f"- **Basis change:** "
                    f"{row['basis_change']:.4f}"
                ),
                (
                    f"- **Primary reason:** "
                    f"{row['primary_reason']}"
                ),
                (
                    f"- **Confidence:** "
                    f"{row['confidence']}"
                ),
                (
                    f"- **Dominant leg:** "
                    f"{row['dominant_leg']}"
                ),
                (
                    f"- **Days to expiry:** "
                    f"{row['days_to_expiry']}"
                ),
                (
                    f"- **Secondary reasons:** "
                    f"{row['secondary_reasons']}"
                ),
                "",
                "### Explanation",
                "",
                str(row["explanation"]),
                "",
                "---",
                "",
            ]
        )

    file_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return file_path

