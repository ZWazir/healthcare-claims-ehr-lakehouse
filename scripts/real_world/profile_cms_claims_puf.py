from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd


# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / "data" / "real_world" / "bronze" / "cms_claims_puf"
REPORTS_DIR = PROJECT_ROOT / "reports" / "real_world"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Expected CMS Claims PUF Bronze tables
# =============================================================================

EXPECTED_TABLES = {
    "inpatient_claims": {
        "description": "CMS Basic Stand Alone Medicare Claims PUF - 2008 Inpatient Claims",
        "expected_claim_type": "inpatient",
        "expected_source_year": "2008",
    }
}


# =============================================================================
# Helper functions
# =============================================================================

def read_bronze_table(table_name: str) -> pd.DataFrame:
    """
    Reads a CMS Claims PUF Bronze Parquet table.
    """

    table_path = BRONZE_DIR / f"{table_name}.parquet"

    if not table_path.exists():
        raise FileNotFoundError(f"Missing Bronze table: {table_path}")

    return pd.read_parquet(table_path)


def summarize_missing_values(df: pd.DataFrame) -> list[dict]:
    """
    Summarizes missing values by column.

    Returns only columns with missing values to keep the report readable.
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


def find_columns_by_keyword(df: pd.DataFrame, keywords: list[str]) -> list[str]:
    """
    Finds columns containing any of the provided keywords.

    This is useful for public-use claims files because field names can vary
    across claim types and documentation versions.
    """

    matched_columns = []

    for column in df.columns:
        lower_column = column.lower()

        if any(keyword in lower_column for keyword in keywords):
            matched_columns.append(column)

    return matched_columns


def summarize_candidate_columns(df: pd.DataFrame) -> dict:
    """
    Identifies likely business-relevant columns in the claims file.
    """

    return {
        "diagnosis_columns": find_columns_by_keyword(df, ["diag", "icd", "dgns"]),
        "procedure_columns": find_columns_by_keyword(df, ["proc", "prcdr", "hcpcs"]),
        "payment_or_cost_columns": find_columns_by_keyword(df, ["pmt", "pay", "charge", "cost", "amt", "reimb"]),
        "date_columns": find_columns_by_keyword(df, ["date", "dt", "year"]),
        "provider_columns": find_columns_by_keyword(df, ["provider", "prvdr", "npi"]),
        "metadata_columns": find_columns_by_keyword(df, ["_source", "_claim", "_ingestion"]),
    }


def summarize_top_values(df: pd.DataFrame, max_columns: int = 8, max_values: int = 5) -> dict:
    """
    Creates compact top-value summaries for a few useful low-cardinality columns.
    """

    summaries = {}

    for column in df.columns:
        if len(summaries) >= max_columns:
            break

        unique_count = df[column].nunique(dropna=True)

        if 1 < unique_count <= 25:
            top_values = (
                df[column]
                .fillna("")
                .value_counts()
                .head(max_values)
                .to_dict()
            )

            summaries[column] = {
                "unique_count": int(unique_count),
                "top_values": {str(key): int(value) for key, value in top_values.items()},
            }

    return summaries


def summarize_table(table_name: str, df: pd.DataFrame, table_config: dict) -> dict:
    """
    Creates a compact profile summary for one CMS Claims PUF Bronze table.
    """

    duplicate_row_count = int(df.duplicated().sum()) if len(df) > 0 else 0

    candidate_columns = summarize_candidate_columns(df)

    profile = {
        "table_name": table_name,
        "description": table_config["description"],
        "expected_claim_type": table_config["expected_claim_type"],
        "expected_source_year": table_config["expected_source_year"],
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "duplicate_row_count": duplicate_row_count,
        "total_missing_values": int(df.isna().sum().sum()),
        "columns_with_missing_values": summarize_missing_values(df),
        "candidate_columns": candidate_columns,
        "top_value_summaries": summarize_top_values(df),
        "sample_rows": df.head(3).fillna("").to_dict(orient="records"),
    }

    metadata_columns_present = all(
        column in df.columns
        for column in ["_source_file", "_claim_type", "_source_year", "_ingestion_timestamp_utc"]
    )

    profile["metadata_columns_present"] = metadata_columns_present

    profile["passed_basic_checks"] = (
        profile["row_count"] > 0
        and profile["column_count"] > 0
        and metadata_columns_present
    )

    return profile


def write_markdown_report(profile_report: dict, markdown_path: Path) -> None:
    """
    Writes a recruiter-readable Markdown profile report for the CMS Claims PUF Bronze layer.
    """

    lines = []

    lines.append("# CMS Claims PUF Bronze Profile Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("This report profiles the real-world/public CMS Basic Stand Alone Medicare Claims Public Use File Bronze tables.")
    lines.append("")
    lines.append("The purpose of this report is to validate that the selected CMS claims CSV file was ingested into the project as a Parquet Bronze table and can be inspected for claims-oriented columns.")
    lines.append("")
    lines.append("This public claims ingestion track is intentionally separate from the MIMIC-IV demo EHR ingestion track.")
    lines.append("")
    lines.append("## Run Metadata")
    lines.append("")
    lines.append(f"- Pipeline: `{profile_report['pipeline_name']}`")
    lines.append(f"- Dataset: {profile_report['dataset']}")
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
        lines.append(f"- Description: {table['description']}")
        lines.append(f"- Expected claim type: {table['expected_claim_type']}")
        lines.append(f"- Expected source year: {table['expected_source_year']}")
        lines.append(f"- Rows: {table['row_count']}")
        lines.append(f"- Columns: {table['column_count']}")
        lines.append(f"- Duplicate rows: {table['duplicate_row_count']}")
        lines.append(f"- Total missing values: {table['total_missing_values']}")
        lines.append(f"- Metadata columns present: {table['metadata_columns_present']}")
        lines.append(f"- Passed basic checks: {table['passed_basic_checks']}")
        lines.append("")

        lines.append("#### Candidate Claims Columns")
        lines.append("")
        for category, columns in table["candidate_columns"].items():
            if columns:
                preview = ", ".join([f"`{column}`" for column in columns[:20]])
                extra_count = max(len(columns) - 20, 0)

                if extra_count > 0:
                    preview += f", ... plus {extra_count} more"

                lines.append(f"- {category}: {preview}")
            else:
                lines.append(f"- {category}: None detected")
        lines.append("")

        if table["columns_with_missing_values"]:
            lines.append("#### Columns With Missing Values")
            lines.append("")
            lines.append("| Column | Missing Count | Missing % |")
            lines.append("|---|---:|---:|")

            for column_summary in table["columns_with_missing_values"][:20]:
                lines.append(
                    f"| `{column_summary['column']}` | "
                    f"{column_summary['missing_count']} | "
                    f"{column_summary['missing_pct']}% |"
                )

            if len(table["columns_with_missing_values"]) > 20:
                remaining_count = len(table["columns_with_missing_values"]) - 20
                lines.append(f"| Additional columns not shown | {remaining_count} |  |")

            lines.append("")
        else:
            lines.append("#### Columns With Missing Values")
            lines.append("")
            lines.append("None")
            lines.append("")

        if table["top_value_summaries"]:
            lines.append("#### Top Value Summaries")
            lines.append("")

            for column, summary in table["top_value_summaries"].items():
                lines.append(f"**`{column}`**")
                lines.append("")
                lines.append(f"- Unique values: {summary['unique_count']}")
                lines.append("- Top values:")

                for value, count in summary["top_values"].items():
                    display_value = value if value != "" else "[blank]"
                    lines.append(f"  - `{display_value}`: {count}")

                lines.append("")

        lines.append("#### Columns")
        lines.append("")
        lines.append(", ".join([f"`{column}`" for column in table["columns"]]))
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("The CMS Claims PUF Bronze ingestion validates that public Medicare claims-style CSV files can be ingested into the project as local Parquet tables.")
    lines.append("")
    lines.append("This does not replace or link to the synthetic EHR + claims pipeline or the MIMIC-IV demo EHR ingestion. It is a separate public claims ingestion extension.")
    lines.append("")
    lines.append("This separation is important because the CMS public use files do not provide linkable beneficiary identities and should not be joined to unrelated clinical datasets.")
    lines.append("")

    markdown_path.write_text("\n".join(lines))


# =============================================================================
# Main profile workflow
# =============================================================================

def main() -> None:
    print("Starting CMS Claims PUF Bronze profiling...")

    profile_report = {
        "pipeline_name": "cms_claims_puf_bronze_profile",
        "dataset": "CMS Basic Stand Alone Medicare Claims Public Use Files",
        "profile_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bronze_directory": str(BRONZE_DIR.relative_to(PROJECT_ROOT)),
        "expected_table_count": len(EXPECTED_TABLES),
        "profiled_table_count": 0,
        "tables_passing_basic_checks": 0,
        "missing_tables": [],
        "tables": [],
    }

    for table_name, table_config in EXPECTED_TABLES.items():
        print("\n" + "=" * 80)
        print(f"Profiling table: {table_name}")
        print("=" * 80)

        table_path = BRONZE_DIR / f"{table_name}.parquet"

        if not table_path.exists():
            print(f"Missing Bronze table: {table_path}")
            profile_report["missing_tables"].append(table_name)
            continue

        df = read_bronze_table(table_name)
        table_profile = summarize_table(table_name, df, table_config)

        profile_report["tables"].append(table_profile)
        profile_report["profiled_table_count"] += 1

        if table_profile["passed_basic_checks"]:
            profile_report["tables_passing_basic_checks"] += 1

        print(f"Rows: {table_profile['row_count']}")
        print(f"Columns: {table_profile['column_count']}")
        print(f"Passed checks: {table_profile['passed_basic_checks']}")

    json_report_path = REPORTS_DIR / "cms_claims_puf_profile_report.json"
    markdown_report_path = REPORTS_DIR / "cms_claims_puf_profile_report.md"

    with open(json_report_path, "w") as f:
        json.dump(profile_report, f, indent=2)

    write_markdown_report(profile_report, markdown_report_path)

    print("\n" + "=" * 80)
    print("CMS Claims PUF Bronze profiling complete.")
    print("=" * 80)
    print(f"Profiled tables: {profile_report['profiled_table_count']}")
    print(f"Tables passing checks: {profile_report['tables_passing_basic_checks']}")
    print(f"Missing tables: {len(profile_report['missing_tables'])}")
    print(f"JSON report written to: {json_report_path.relative_to(PROJECT_ROOT)}")
    print(f"Markdown report written to: {markdown_report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()