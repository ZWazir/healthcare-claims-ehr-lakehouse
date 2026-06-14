from pathlib import Path
import json
import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
REPORTS_DIR = PROJECT_ROOT / "reports" / "gold"

OUTPUT_PATH = GOLD_DIR / "gold_patient_360.parquet"
REPORT_PATH = REPORTS_DIR / "patient_360_build_report.json"

PATIENT_KEYS = ["ehr_patient_id", "claim_beneficiary_id", "crosswalk_method"]


SOURCE_TABLES = {
    "patient_master": GOLD_DIR / "gold_patient_master.parquet",
    "utilization_summary": GOLD_DIR / "gold_utilization_summary.parquet",
    "condition_summary": GOLD_DIR / "gold_condition_summary.parquet",
    "medication_summary": GOLD_DIR / "gold_medication_summary.parquet",
    "observation_summary": GOLD_DIR / "gold_observation_summary.parquet",
    "patient_risk_features": GOLD_DIR / "gold_patient_risk_features.parquet",
}


def read_gold_table(table_name: str, path: Path, required: bool = False) -> pd.DataFrame:
    """
    Reads a Gold parquet table if it exists.

    The patient_master table is required because it is the base of Patient 360.
    Other Gold tables are optional so the script remains durable if a future
    pipeline run excludes medications or observations.
    """
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Required Gold table not found: {path}")
        print(f"WARNING: Optional Gold table missing: {table_name} -> {path}")
        return pd.DataFrame()

    df = pd.read_parquet(path)
    print(f"Read {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def normalize_key_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes patient identifier columns before joins.

    Keeping these columns as strings avoids mismatches caused by mixed integer,
    float, or null identifier types across different Gold outputs.
    """
    if df.empty:
        return df

    df = df.copy()

    for col in PATIENT_KEYS:
        if col not in df.columns:
            df[col] = pd.NA

        df[col] = df[col].astype("string").fillna("unknown")

    return df


def select_non_duplicate_columns(
    base_df: pd.DataFrame,
    incoming_df: pd.DataFrame,
    source_name: str,
) -> pd.DataFrame:
    """
    Keeps patient keys plus only new columns from the incoming table.

    This prevents duplicate columns such as age_x, age_y, gender_x, gender_y
    when multiple Gold tables carry overlapping patient attributes.
    """
    if incoming_df.empty:
        return incoming_df

    keep_cols = list(PATIENT_KEYS)

    duplicate_cols_skipped = []

    for col in incoming_df.columns:
        if col in PATIENT_KEYS:
            continue

        if col in base_df.columns:
            duplicate_cols_skipped.append(col)
            continue

        keep_cols.append(col)

    if duplicate_cols_skipped:
        print(
            f"Skipped {len(duplicate_cols_skipped)} duplicate columns from {source_name}: "
            f"{duplicate_cols_skipped}"
        )

    return incoming_df[keep_cols]


def merge_gold_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Builds the Patient 360 table by left-joining all available Gold summaries
    onto the patient master table.
    """
    patient_360 = tables["patient_master"].copy()

    for source_name, source_df in tables.items():
        if source_name == "patient_master":
            continue

        if source_df.empty:
            continue

        source_df = select_non_duplicate_columns(
            base_df=patient_360,
            incoming_df=source_df,
            source_name=source_name,
        )

        patient_360 = patient_360.merge(
            source_df,
            on=PATIENT_KEYS,
            how="left",
            validate="one_to_one",
        )

        print(
            f"Merged {source_name}: "
            f"{patient_360.shape[0]} rows, {patient_360.shape[1]} columns"
        )

    return patient_360


def find_numeric_columns(df: pd.DataFrame, include_terms: list[str], exclude_terms: list[str] | None = None) -> list[str]:
    """
    Finds numeric columns whose names contain one or more business keywords.

    This makes the script flexible as the upstream Gold schema evolves.
    """
    exclude_terms = exclude_terms or []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    matched_cols = []

    for col in numeric_cols:
        col_lower = col.lower()

        include_match = any(term in col_lower for term in include_terms)
        exclude_match = any(term in col_lower for term in exclude_terms)

        if include_match and not exclude_match:
            matched_cols.append(col)

    return matched_cols


def add_patient_360_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds executive-facing fields that make the table easier to use in dashboards.

    These are not replacing the ML feature table. They are simple, explainable
    business fields for patient overview, segmentation, and care-management use cases.
    """
    patient_360 = df.copy()

    # Age band for dashboard filtering.
    if "age" in patient_360.columns:
        patient_360["age_band"] = pd.cut(
            patient_360["age"],
            bins=[0, 17, 34, 49, 64, 200],
            labels=["0-17", "18-34", "35-49", "50-64", "65+"],
            right=True,
        ).astype("string")
    else:
        patient_360["age_band"] = "unknown"

    # Total utilization proxy from encounter/claim/admission/visit count columns.
    utilization_count_cols = find_numeric_columns(
        patient_360,
        include_terms=["encounter_count", "claim_count", "admission_count", "visit_count"],
        exclude_terms=["condition", "medication", "observation"],
    )

    if utilization_count_cols:
        patient_360["patient_360_total_utilization_events"] = (
            patient_360[utilization_count_cols].fillna(0).sum(axis=1)
        )
    else:
        patient_360["patient_360_total_utilization_events"] = 0

    # Cost proxy from paid/charge/cost/amount columns if available.
    cost_cols = find_numeric_columns(
        patient_360,
        include_terms=["cost", "paid", "payment", "charge", "amount"],
        exclude_terms=[],
    )

    if cost_cols:
        patient_360["patient_360_total_cost_proxy"] = (
            patient_360[cost_cols].fillna(0).sum(axis=1)
        )
    else:
        patient_360["patient_360_total_cost_proxy"] = 0

    # Condition burden proxy.
    condition_count_cols = find_numeric_columns(
        patient_360,
        include_terms=["condition_count", "diagnosis_count", "chronic_condition_count"],
        exclude_terms=[],
    )

    if condition_count_cols:
        patient_360["patient_360_condition_burden"] = (
            patient_360[condition_count_cols].fillna(0).sum(axis=1)
        )
    else:
        patient_360["patient_360_condition_burden"] = 0

    # Dashboard-friendly utilization segment.
    util_values = patient_360["patient_360_total_utilization_events"]

    if util_values.max() > 0 and util_values.nunique() > 1:
        high_util_threshold = util_values.quantile(0.75)
        medium_util_threshold = util_values.quantile(0.50)

        patient_360["utilization_segment"] = np.select(
            [
                util_values >= high_util_threshold,
                util_values >= medium_util_threshold,
            ],
            [
                "High utilization",
                "Medium utilization",
            ],
            default="Low utilization",
        )
    else:
        patient_360["utilization_segment"] = "Not enough variation"

    # Dashboard-friendly cost segment.
    cost_values = patient_360["patient_360_total_cost_proxy"]

    if cost_values.max() > 0 and cost_values.nunique() > 1:
        high_cost_threshold = cost_values.quantile(0.75)
        medium_cost_threshold = cost_values.quantile(0.50)

        patient_360["cost_segment"] = np.select(
            [
                cost_values >= high_cost_threshold,
                cost_values >= medium_cost_threshold,
            ],
            [
                "High cost",
                "Medium cost",
            ],
            default="Low cost",
        )
    else:
        patient_360["cost_segment"] = "Not enough variation"

    # Care-management priority field for recruiter-facing dashboard storytelling.
    #
    # This combines dashboard-friendly cost, utilization, and condition-burden
    # signals into a simple triage field. The goal is not clinical decisioning;
    # it is an explainable portfolio metric for care-management analytics.
    condition_values = patient_360["patient_360_condition_burden"].fillna(0)

    if condition_values.max() > 0 and condition_values.nunique() > 1:
        high_condition_threshold = condition_values.quantile(0.75)
        medium_condition_threshold = condition_values.quantile(0.50)
    else:
        high_condition_threshold = 1
        medium_condition_threshold = 1

    high_priority_mask = (
        patient_360["cost_segment"].eq("High cost")
        | patient_360["utilization_segment"].eq("High utilization")
        | (
            condition_values.ge(high_condition_threshold)
            & condition_values.gt(0)
        )
    )

    medium_priority_mask = (
        patient_360["cost_segment"].eq("Medium cost")
        | patient_360["utilization_segment"].eq("Medium utilization")
        | (
            condition_values.ge(medium_condition_threshold)
            & condition_values.gt(0)
        )
        | patient_360.get(
            "care_management_candidate_flag",
            pd.Series(0, index=patient_360.index),
        )
        .fillna(0)
        .astype(int)
        .eq(1)
        | patient_360.get(
            "high_cost_patient_flag",
            pd.Series(0, index=patient_360.index),
        )
        .fillna(0)
        .astype(int)
        .eq(1)
    )

    patient_360["care_management_priority"] = np.select(
        [
            high_priority_mask,
            medium_priority_mask,
        ],
        [
            "High priority",
            "Medium priority",
        ],
        default="Low priority",
    )

    return patient_360


def build_report(
    source_tables: dict[str, pd.DataFrame],
    patient_360: pd.DataFrame,
    utilization_count_cols: list[str],
    cost_cols: list[str],
) -> dict:
    """
    Creates a JSON report documenting the Patient 360 build.
    """
    return {
        "output_path": str(OUTPUT_PATH.relative_to(PROJECT_ROOT)),
        "output_rows": int(patient_360.shape[0]),
        "output_columns": int(patient_360.shape[1]),
        "patient_keys": PATIENT_KEYS,
        "source_tables": {
            name: {
                "rows": int(df.shape[0]) if not df.empty else 0,
                "columns": int(df.shape[1]) if not df.empty else 0,
                "available": not df.empty,
            }
            for name, df in source_tables.items()
        },
        "derived_columns_added": [
            "age_band",
            "patient_360_total_utilization_events",
            "patient_360_total_cost_proxy",
            "patient_360_condition_burden",
            "utilization_segment",
            "cost_segment",
            "care_management_priority",
        ],
        "utilization_columns_used": utilization_count_cols,
        "cost_columns_used": cost_cols,
    }


def main() -> None:
    """
    Main execution flow:
    1. Read existing Gold tables.
    2. Normalize patient identifiers.
    3. Merge Gold summaries into one Patient 360 table.
    4. Add executive-facing segmentation fields.
    5. Write parquet output and JSON build report.
    """
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    raw_tables = {}

    for table_name, path in SOURCE_TABLES.items():
        raw_tables[table_name] = read_gold_table(
            table_name=table_name,
            path=path,
            required=(table_name == "patient_master"),
        )

    normalized_tables = {
        table_name: normalize_key_columns(df)
        for table_name, df in raw_tables.items()
    }

    patient_360 = merge_gold_tables(normalized_tables)
    patient_360 = add_patient_360_features(patient_360)

    utilization_count_cols = find_numeric_columns(
        patient_360,
        include_terms=["encounter_count", "claim_count", "admission_count", "visit_count"],
        exclude_terms=["condition", "medication", "observation"],
    )

    cost_cols = find_numeric_columns(
        patient_360,
        include_terms=["cost", "paid", "payment", "charge", "amount"],
        exclude_terms=[],
    )

    patient_360.to_parquet(OUTPUT_PATH, index=False)

    report = build_report(
        source_tables=normalized_tables,
        patient_360=patient_360,
        utilization_count_cols=utilization_count_cols,
        cost_cols=cost_cols,
    )

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\nPatient 360 build complete.")
    print(f"Wrote table: {OUTPUT_PATH}")
    print(f"Wrote report: {REPORT_PATH}")
    print(f"Rows: {patient_360.shape[0]}")
    print(f"Columns: {patient_360.shape[1]}")


if __name__ == "__main__":
    main()