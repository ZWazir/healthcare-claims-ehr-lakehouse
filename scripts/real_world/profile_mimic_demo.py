from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd


# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / "data" / "real_world" / "bronze" / "mimic_demo"
REPORTS_DIR = PROJECT_ROOT / "reports" / "real_world"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Expected MIMIC-IV demo Bronze tables and required columns
# =============================================================================

EXPECTED_TABLES = {
    "patients": ["subject_id", "gender", "anchor_age", "anchor_year", "anchor_year_group"],
    "admissions": ["subject_id", "hadm_id", "admittime", "dischtime", "admission_type", "race"],
    "diagnoses_icd": ["subject_id", "hadm_id", "seq_num", "icd_code", "icd_version"],
    "procedures_icd": ["subject_id", "hadm_id", "seq_num", "icd_code", "icd_version"],
    "d_icd_diagnoses": ["icd_code", "icd_version", "long_title"],
    "d_icd_procedures": ["icd_code", "icd_version", "long_title"],
    "labevents": ["labevent_id", "subject_id", "itemid", "charttime"],
    "prescriptions": ["subject_id", "hadm_id", "pharmacy_id", "drug"],
    "icustays": ["subject_id", "hadm_id", "stay_id", "intime", "outtime"],
}


# =============================================================================
# Helper functions
# =============================================================================

def read_bronze_table(table_name: str) -> pd.DataFrame:
    """
    Reads a Bronze Parquet table from the real-world MIMIC demo layer.
    """

    table_path = BRONZE_DIR / f"{table_name}.parquet"

    if not table_path.exists():
        raise FileNotFoundError(f"Missing Bronze table: {table_path}")

    return pd.read_parquet(table_path)


def summarize_missing_values(df: pd.DataFrame) -> list[dict]:
    """
    Summarizes missing values by column.

    Returns only columns with at least one missing value to keep the report readable.
    """

    missing_summary = []

    for column in df.columns:
        missing_count = int(df[column].isna().sum())

        if missing_count > 0:
            missing_summary.append(
                {
                    "column": column,
                    "missing_count": missing_count,
                    "missing_pct": round((missing_count / len(df)) * 100, 2) if len(df) > 0 else 0,
                }
            )

    return missing_summary


def summarize_table(table_name: str, df: pd.DataFrame, required_columns: list[str]) -> dict:
    """
    Creates a compact profile summary for one MIMIC demo Bronze table.
    """

    missing_required_columns = [col for col in required_columns if col not in df.columns]

    duplicate_row_count = int(df.duplicated().sum()) if len(df) > 0 else 0

    profile = {
        "table_name": table_name,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "required_columns": required_columns,
        "missing_required_columns": missing_required_columns,
        "duplicate_row_count": duplicate_row_count,
        "total_missing_values": int(df.isna().sum().sum()),
        "columns_with_missing_values": summarize_missing_values(df),
        "sample_rows": df.head(3).fillna("").to_dict(orient="records"),
    }

    profile["passed_basic_checks"] = (
        profile["row_count"] > 0
        and len(profile["missing_required_columns"]) == 0
    )

    return profile


def write_markdown_report(profile_report: dict, markdown_path: Path) -> None:
    """
    Writes a recruiter-readable Markdown profile report for the MIMIC demo Bronze layer.
    """

    lines = []

    lines.append("# MIMIC-IV Demo Bronze Profile Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("This report profiles the real-world/public MIMIC-IV Clinical Database Demo Bronze tables.")
    lines.append("")
    lines.append("The purpose of this report is to validate that selected MIMIC-IV demo CSV files were ingested into the project as Parquet Bronze tables and that the expected core columns are present.")
    lines.append("")
    lines.append("This real-world ingestion track is intentionally separate from the synthetic linked EHR + claims pipeline.")
    lines.append("")
    lines.append("## Run Metadata")
    lines.append("")
    lines.append(f"- Pipeline: `{profile_report['pipeline_name']}`")
    lines.append(f"- Dataset: {profile_report['dataset']}")
    lines.append(f"- Dataset version: {profile_report['dataset_version']}")
    lines.append(f"- Profile timestamp UTC: {profile_report['profile_timestamp_utc']}")
    lines.append(f"- Bronze directory: `{profile_report['bronze_directory']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Expected tables: {profile_report['expected_table_count']}")
    lines.append(f"- Profiled tables: {profile_report['profiled_table_count']}")
    lines.append(f"- Missing tables: {len(profile_report['missing_tables'])}")
    lines.append(f"- Tables passing basic checks: {profile_report['tables_passing_basic_checks']}")
    lines.append("")

    if profile_report["missing_tables"]:
        lines.append("## Missing Tables")
        lines.append("")
        for table_name in profile_report["missing_tables"]:
            lines.append(f"- `{table_name}`")
        lines.append("")

    lines.append("## Table Profiles")
    lines.append("")

    for table in profile_report["tables"]:
        lines.append(f"### `{table['table_name']}`")
        lines.append("")
        lines.append(f"- Rows: {table['row_count']}")
        lines.append(f"- Columns: {table['column_count']}")
        lines.append(f"- Duplicate rows: {table['duplicate_row_count']}")
        lines.append(f"- Total missing values: {table['total_missing_values']}")
        lines.append(f"- Passed basic checks: {table['passed_basic_checks']}")
        lines.append("")

        if table["missing_required_columns"]:
            lines.append("Missing required columns:")
            lines.append("")
            for column in table["missing_required_columns"]:
                lines.append(f"- `{column}`")
            lines.append("")
        else:
            lines.append("Missing required columns: None")
            lines.append("")

        if table["columns_with_missing_values"]:
            lines.append("Columns with missing values:")
            lines.append("")
            lines.append("| Column | Missing Count | Missing % |")
            lines.append("|---|---:|---:|")

            for column_summary in table["columns_with_missing_values"][:15]:
                lines.append(
                    f"| `{column_summary['column']}` | "
                    f"{column_summary['missing_count']} | "
                    f"{column_summary['missing_pct']}% |"
                )

            if len(table["columns_with_missing_values"]) > 15:
                remaining_count = len(table["columns_with_missing_values"]) - 15
                lines.append(f"| Additional columns not shown | {remaining_count} |  |")

            lines.append("")
        else:
            lines.append("Columns with missing values: None")
            lines.append("")

        lines.append("Columns:")
        lines.append("")
        lines.append(", ".join([f"`{col}`" for col in table["columns"]]))
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("The MIMIC-IV demo Bronze ingestion validates that real deidentified EHR-style CSV files can be ingested into the project as local Parquet tables.")
    lines.append("")
    lines.append("This does not replace the synthetic linked EHR + claims pipeline. Instead, it extends the project by adding a separate real-world ingestion track for public clinical data.")
    lines.append("")

    markdown_path.write_text("\n".join(lines))


# =============================================================================
# Main profile workflow
# =============================================================================

def main() -> None:
    print("Starting MIMIC-IV demo Bronze profiling...")

    profile_report = {
        "pipeline_name": "mimic_demo_bronze_profile",
        "dataset": "MIMIC-IV Clinical Database Demo",
        "dataset_version": "2.2",
        "profile_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bronze_directory": str(BRONZE_DIR.relative_to(PROJECT_ROOT)),
        "expected_table_count": len(EXPECTED_TABLES),
        "profiled_table_count": 0,
        "tables_passing_basic_checks": 0,
        "missing_tables": [],
        "tables": [],
    }

    for table_name, required_columns in EXPECTED_TABLES.items():
        print("\n" + "=" * 80)
        print(f"Profiling table: {table_name}")
        print("=" * 80)

        table_path = BRONZE_DIR / f"{table_name}.parquet"

        if not table_path.exists():
            print(f"Missing Bronze table: {table_path}")
            profile_report["missing_tables"].append(table_name)
            continue

        df = read_bronze_table(table_name)
        table_profile = summarize_table(table_name, df, required_columns)

        profile_report["tables"].append(table_profile)
        profile_report["profiled_table_count"] += 1

        if table_profile["passed_basic_checks"]:
            profile_report["tables_passing_basic_checks"] += 1

        print(f"Rows: {table_profile['row_count']}")
        print(f"Columns: {table_profile['column_count']}")
        print(f"Passed checks: {table_profile['passed_basic_checks']}")

    json_report_path = REPORTS_DIR / "mimic_demo_profile_report.json"
    markdown_report_path = REPORTS_DIR / "mimic_demo_profile_report.md"

    with open(json_report_path, "w") as f:
        json.dump(profile_report, f, indent=2)

    write_markdown_report(profile_report, markdown_report_path)

    print("\n" + "=" * 80)
    print("MIMIC-IV demo Bronze profiling complete.")
    print("=" * 80)
    print(f"Profiled tables: {profile_report['profiled_table_count']}")
    print(f"Tables passing checks: {profile_report['tables_passing_basic_checks']}")
    print(f"Missing tables: {len(profile_report['missing_tables'])}")
    print(f"JSON report written to: {json_report_path.relative_to(PROJECT_ROOT)}")
    print(f"Markdown report written to: {markdown_report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()