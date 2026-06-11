from pathlib import Path
from datetime import datetime
import json
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
REPORTS_DIR = PROJECT_ROOT / "reports" / "gold"

MARKDOWN_REPORT_PATH = REPORTS_DIR / "gold_profile_report.md"
JSON_REPORT_PATH = REPORTS_DIR / "gold_profile_report.json"


EXPECTED_GOLD_TABLES = [
    "gold_patient_crosswalk.parquet",
    "gold_patient_master.parquet",
    "gold_condition_summary.parquet",
    "gold_utilization_summary.parquet",
    "gold_medication_summary.parquet",
    "gold_observation_summary.parquet",
    "gold_patient_risk_features.parquet",
]


UNIQUE_KEY_CANDIDATES = {
    "gold_patient_crosswalk.parquet": ["patient_id"],
    "gold_patient_master.parquet": ["patient_id"],
    "gold_utilization_summary.parquet": ["patient_id"],
    "gold_patient_risk_features.parquet": ["patient_id"],
}


def read_gold_table(file_path: Path) -> pd.DataFrame:
    """
    Read a Gold layer Parquet table into a pandas DataFrame.
    """

    return pd.read_parquet(file_path)


def get_null_profile(df: pd.DataFrame) -> list[dict]:
    """
    Create a column-level null profile.

    For each column, this reports:
    - column name
    - data type
    - null count
    - null percentage
    """

    row_count = len(df)

    null_profile = []

    for column in df.columns:
        null_count = int(df[column].isna().sum())
        null_percent = round((null_count / row_count) * 100, 2) if row_count > 0 else 0

        null_profile.append(
            {
                "column_name": column,
                "dtype": str(df[column].dtype),
                "null_count": null_count,
                "null_percent": null_percent,
            }
        )

    return null_profile


def get_duplicate_profile(df: pd.DataFrame, table_name: str) -> dict:
    """
    Create duplicate checks for a Gold table.

    This includes:
    - full row duplicate count
    - key-level duplicate count when a known key exists
    """

    duplicate_profile = {
        "full_row_duplicate_count": int(df.duplicated().sum()),
        "key_check_performed": False,
        "key_columns": [],
        "key_duplicate_count": None,
    }

    key_columns = UNIQUE_KEY_CANDIDATES.get(table_name)

    if key_columns and all(column in df.columns for column in key_columns):
        duplicate_profile["key_check_performed"] = True
        duplicate_profile["key_columns"] = key_columns
        duplicate_profile["key_duplicate_count"] = int(df.duplicated(subset=key_columns).sum())

    return duplicate_profile


def get_sample_records(df: pd.DataFrame, sample_size: int = 5) -> list[dict]:
    """
    Return a small sample of records for quick inspection.

    Datetime values are converted to strings so the output can be written to JSON.
    """

    sample_df = df.head(sample_size).copy()

    for column in sample_df.columns:
        if pd.api.types.is_datetime64_any_dtype(sample_df[column]):
            sample_df[column] = sample_df[column].astype(str)

    return sample_df.fillna("").to_dict(orient="records")


def profile_table(table_name: str) -> dict:
    """
    Build a complete profile for one Gold table.
    """

    file_path = GOLD_DIR / table_name

    if not file_path.exists():
        return {
            "table_name": table_name,
            "file_path": str(file_path),
            "exists": False,
            "error": "Expected Gold table file does not exist.",
        }

    df = read_gold_table(file_path)

    profile = {
        "table_name": table_name,
        "file_path": str(file_path),
        "exists": True,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "null_profile": get_null_profile(df),
        "duplicate_profile": get_duplicate_profile(df, table_name),
        "sample_records": get_sample_records(df),
    }

    return profile


def write_json_report(report: dict) -> None:
    """
    Write the full Gold profile report as JSON.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(JSON_REPORT_PATH, "w") as file:
        json.dump(report, file, indent=2)


def write_markdown_report(report: dict) -> None:
    """
    Write a human-readable Gold profile report as Markdown.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# Gold Layer Profile Report")
    lines.append("")
    lines.append("## Project: Healthcare Claims & EHR Lakehouse")
    lines.append("")
    lines.append(
        "This report profiles the Gold layer Parquet outputs used for analytics, "
        "business intelligence, and downstream machine learning."
    )
    lines.append("")
    lines.append(f"Generated at: `{report['generated_at']}`")
    lines.append(f"Gold directory: `{report['gold_directory']}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| Table | Exists | Rows | Columns | Full Row Duplicates | Key Duplicate Check |")
    lines.append("|---|---:|---:|---:|---:|---|")

    for table in report["tables"]:
        if not table["exists"]:
            lines.append(
                f"| {table['table_name']} | No |  |  |  | Missing file |"
            )
            continue

        duplicate_profile = table["duplicate_profile"]

        if duplicate_profile["key_check_performed"]:
            key_check = (
                f"{duplicate_profile['key_columns']} duplicate count = "
                f"{duplicate_profile['key_duplicate_count']}"
            )
        else:
            key_check = "Not applicable"

        lines.append(
            f"| {table['table_name']} | Yes | {table['row_count']} | "
            f"{table['column_count']} | "
            f"{duplicate_profile['full_row_duplicate_count']} | "
            f"{key_check} |"
        )

    lines.append("")

    for table in report["tables"]:
        lines.append("---")
        lines.append("")
        lines.append(f"## {table['table_name']}")
        lines.append("")

        if not table["exists"]:
            lines.append("Status: Missing expected Gold table.")
            lines.append("")
            lines.append(f"Expected path: `{table['file_path']}`")
            lines.append("")
            continue

        lines.append(f"Path: `{table['file_path']}`")
        lines.append(f"Rows: `{table['row_count']}`")
        lines.append(f"Columns: `{table['column_count']}`")
        lines.append("")

        lines.append("### Columns")
        lines.append("")
        for column in table["columns"]:
            lines.append(f"- {column}")
        lines.append("")

        lines.append("### Null Profile")
        lines.append("")
        lines.append("| Column | Data Type | Null Count | Null Percent |")
        lines.append("|---|---|---:|---:|")

        for column_profile in table["null_profile"]:
            lines.append(
                f"| {column_profile['column_name']} | "
                f"{column_profile['dtype']} | "
                f"{column_profile['null_count']} | "
                f"{column_profile['null_percent']}% |"
            )

        lines.append("")

        lines.append("### Duplicate Profile")
        lines.append("")
        duplicate_profile = table["duplicate_profile"]
        lines.append(
            f"- Full row duplicate count: "
            f"`{duplicate_profile['full_row_duplicate_count']}`"
        )

        if duplicate_profile["key_check_performed"]:
            lines.append(
                f"- Key columns checked: "
                f"`{duplicate_profile['key_columns']}`"
            )
            lines.append(
                f"- Key duplicate count: "
                f"`{duplicate_profile['key_duplicate_count']}`"
            )
        else:
            lines.append("- Key-level duplicate check: `Not applicable`")

        lines.append("")

        lines.append("### Sample Records")
        lines.append("")

        if table["sample_records"]:
            sample_df = pd.DataFrame(table["sample_records"])
            lines.append(sample_df.to_markdown(index=False))
        else:
            lines.append("No sample records available.")

        lines.append("")

    with open(MARKDOWN_REPORT_PATH, "w") as file:
        file.write("\n".join(lines))


def main() -> None:
    """
    Profile all expected Gold layer outputs and write reports.

    Outputs:
    - reports/gold/gold_profile_report.md
    - reports/gold/gold_profile_report.json
    """

    print("Starting Gold layer profiling")
    print(f"Gold directory: {GOLD_DIR}")

    if not GOLD_DIR.exists():
        raise FileNotFoundError(f"Gold directory does not exist: {GOLD_DIR}")

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "gold_directory": str(GOLD_DIR),
        "tables": [],
    }

    for table_name in EXPECTED_GOLD_TABLES:
        print(f"Profiling table: {table_name}")
        table_profile = profile_table(table_name)
        report["tables"].append(table_profile)

    write_json_report(report)
    write_markdown_report(report)

    print("")
    print("Gold layer profiling completed successfully")
    print(f"Markdown report written to: {MARKDOWN_REPORT_PATH}")
    print(f"JSON report written to: {JSON_REPORT_PATH}")


if __name__ == "__main__":
    main()