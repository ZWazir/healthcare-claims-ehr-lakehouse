from pathlib import Path
import json

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
REPORTS_DIR = PROJECT_ROOT / "reports" / "gold"

INPUT_PATH = GOLD_DIR / "gold_patient_360.parquet"
BUILD_REPORT_PATH = REPORTS_DIR / "patient_360_build_report.json"

JSON_REPORT_PATH = REPORTS_DIR / "patient_360_profile_report.json"
MARKDOWN_REPORT_PATH = REPORTS_DIR / "patient_360_profile_report.md"

PATIENT_KEYS = ["ehr_patient_id", "claim_beneficiary_id", "crosswalk_method"]


def make_json_safe(value):
    """
    Converts pandas/numpy values into JSON-safe Python values.
    """
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def read_json_if_exists(path: Path) -> dict:
    """
    Reads a JSON file if it exists. Returns an empty dictionary otherwise.
    """
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_column_profile(df: pd.DataFrame) -> dict:
    """
    Creates a column-level profile showing data types, null counts,
    null percentages, and distinct value counts.
    """
    profile = {}

    for col in df.columns:
        null_count = int(df[col].isna().sum())
        non_null_count = int(df[col].notna().sum())

        profile[col] = {
            "dtype": str(df[col].dtype),
            "null_count": null_count,
            "non_null_count": non_null_count,
            "null_percentage": round((null_count / len(df)) * 100, 2) if len(df) else 0,
            "distinct_count": int(df[col].nunique(dropna=True)),
        }

    return profile


def get_numeric_summary(df: pd.DataFrame) -> dict:
    """
    Creates summary statistics for numeric columns.
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    summary = {}

    for col in numeric_cols:
        series = df[col].dropna()

        if series.empty:
            summary[col] = {
                "count": 0,
                "mean": None,
                "min": None,
                "median": None,
                "max": None,
            }
            continue

        summary[col] = {
            "count": int(series.count()),
            "mean": make_json_safe(round(series.mean(), 2)),
            "min": make_json_safe(series.min()),
            "median": make_json_safe(series.median()),
            "max": make_json_safe(series.max()),
        }

    return summary


def get_value_counts(df: pd.DataFrame, column_name: str) -> dict:
    """
    Returns value counts for a column if it exists.
    """
    if column_name not in df.columns:
        return {}

    counts = (
        df[column_name]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .to_dict()
    )

    return {str(key): int(value) for key, value in counts.items()}


def get_patient_key_quality(df: pd.DataFrame) -> dict:
    """
    Checks whether the Patient 360 table is unique at the patient key level.
    """
    existing_keys = [col for col in PATIENT_KEYS if col in df.columns]

    if not existing_keys:
        return {
            "patient_keys_found": [],
            "duplicate_patient_key_rows": None,
            "unique_patient_key_records": None,
            "message": "No expected patient key columns found.",
        }

    duplicate_rows = int(df.duplicated(subset=existing_keys).sum())
    unique_records = int(df[existing_keys].drop_duplicates().shape[0])

    return {
        "patient_keys_found": existing_keys,
        "duplicate_patient_key_rows": duplicate_rows,
        "unique_patient_key_records": unique_records,
        "message": "Patient key uniqueness check completed.",
    }


def build_profile_report(df: pd.DataFrame, build_report: dict) -> dict:
    """
    Builds the full Patient 360 profile report.
    """
    report = {
        "input_path": str(INPUT_PATH.relative_to(PROJECT_ROOT)),
        "profile_json_path": str(JSON_REPORT_PATH.relative_to(PROJECT_ROOT)),
        "profile_markdown_path": str(MARKDOWN_REPORT_PATH.relative_to(PROJECT_ROOT)),
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "patient_key_quality": get_patient_key_quality(df),
        "business_field_counts": {
            "care_management_priority": get_value_counts(df, "care_management_priority"),
            "utilization_segment": get_value_counts(df, "utilization_segment"),
            "cost_segment": get_value_counts(df, "cost_segment"),
            "age_band": get_value_counts(df, "age_band"),
        },
        "important_numeric_fields": {},
        "column_profile": get_column_profile(df),
        "numeric_summary": get_numeric_summary(df),
        "source_build_report_available": bool(build_report),
        "source_build_report": build_report,
    }

    important_numeric_cols = [
        "patient_360_total_utilization_events",
        "patient_360_total_cost_proxy",
        "patient_360_condition_burden",
    ]

    for col in important_numeric_cols:
        if col in df.columns:
            series = df[col].fillna(0)

            report["important_numeric_fields"][col] = {
                "total": make_json_safe(round(series.sum(), 2)),
                "mean": make_json_safe(round(series.mean(), 2)),
                "min": make_json_safe(series.min()),
                "median": make_json_safe(series.median()),
                "max": make_json_safe(series.max()),
            }

    return report


def write_json_report(report: dict) -> None:
    """
    Writes the profile report as JSON.
    """
    with open(JSON_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def write_markdown_report(report: dict) -> None:
    """
    Writes a recruiter-friendly Markdown summary of the Patient 360 profile.
    """
    lines = []

    lines.append("# Patient 360 Profile Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(
        "This report profiles the `gold_patient_360.parquet` Gold mart. "
        "The table combines synthetic linked EHR and claims data into one "
        "patient-level analytics view for dashboarding, care-management storytelling, "
        "and portfolio review."
    )
    lines.append("")
    lines.append("## Table Shape")
    lines.append("")
    lines.append(f"- Rows: `{report['row_count']}`")
    lines.append(f"- Columns: `{report['column_count']}`")
    lines.append("")
    lines.append("## Patient Key Quality")
    lines.append("")

    key_quality = report["patient_key_quality"]

    lines.append(
        f"- Patient keys found: `{', '.join(key_quality.get('patient_keys_found', []))}`"
    )
    lines.append(
        f"- Unique patient key records: `{key_quality.get('unique_patient_key_records')}`"
    )
    lines.append(
        f"- Duplicate patient key rows: `{key_quality.get('duplicate_patient_key_rows')}`"
    )
    lines.append("")

    lines.append("## Business Field Counts")
    lines.append("")

    for field_name, counts in report["business_field_counts"].items():
        lines.append(f"### {field_name}")
        lines.append("")

        if not counts:
            lines.append("- Field not found.")
        else:
            for key, value in counts.items():
                lines.append(f"- {key}: `{value}`")

        lines.append("")

    lines.append("## Important Numeric Fields")
    lines.append("")

    important_numeric_fields = report["important_numeric_fields"]

    if not important_numeric_fields:
        lines.append("No important Patient 360 numeric fields were found.")
        lines.append("")
    else:
        for field_name, stats in important_numeric_fields.items():
            lines.append(f"### {field_name}")
            lines.append("")
            lines.append(f"- Total: `{stats.get('total')}`")
            lines.append(f"- Mean: `{stats.get('mean')}`")
            lines.append(f"- Min: `{stats.get('min')}`")
            lines.append(f"- Median: `{stats.get('median')}`")
            lines.append(f"- Max: `{stats.get('max')}`")
            lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append(
        "- This profile is based on the synthetic linked Gold pipeline."
    )
    lines.append(
        "- The MIMIC-IV Demo and CMS Claims PUF public datasets are not joined into Patient 360 because they are separate public data sources and are not naturally linkable."
    )
    lines.append(
        "- The current synthetic sample dataset is intentionally small, so profile metrics validate the workflow rather than production-scale statistical behavior."
    )
    lines.append("")

    MARKDOWN_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """
    Main execution flow:
    1. Read the Patient 360 Gold mart.
    2. Load the Patient 360 build report if available.
    3. Generate JSON and Markdown profile reports.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Patient 360 table not found: {INPUT_PATH}. "
            "Run scripts/gold/build_patient_360.py first."
        )

    df = pd.read_parquet(INPUT_PATH)
    build_report = read_json_if_exists(BUILD_REPORT_PATH)

    profile_report = build_profile_report(df=df, build_report=build_report)

    write_json_report(profile_report)
    write_markdown_report(profile_report)

    print("Patient 360 profiling complete.")
    print(f"Input table: {INPUT_PATH}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Wrote JSON report: {JSON_REPORT_PATH}")
    print(f"Wrote Markdown report: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    main()