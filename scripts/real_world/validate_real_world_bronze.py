from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd


# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REAL_WORLD_BRONZE_DIR = PROJECT_ROOT / "data" / "real_world" / "bronze"
REPORTS_DIR = PROJECT_ROOT / "reports" / "real_world"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Expected real-world Bronze tables
# =============================================================================

EXPECTED_MIMIC_TABLES = {
    "mimic_demo/patients.parquet": ["subject_id", "gender", "anchor_age"],
    "mimic_demo/admissions.parquet": ["subject_id", "hadm_id", "admittime", "dischtime"],
    "mimic_demo/diagnoses_icd.parquet": ["subject_id", "hadm_id", "icd_code", "icd_version"],
    "mimic_demo/procedures_icd.parquet": ["subject_id", "hadm_id", "icd_code", "icd_version"],
    "mimic_demo/d_icd_diagnoses.parquet": ["icd_code", "icd_version", "long_title"],
    "mimic_demo/d_icd_procedures.parquet": ["icd_code", "icd_version", "long_title"],
    "mimic_demo/labevents.parquet": ["labevent_id", "subject_id", "itemid", "charttime"],
    "mimic_demo/prescriptions.parquet": ["subject_id", "hadm_id", "drug"],
    "mimic_demo/icustays.parquet": ["subject_id", "hadm_id", "stay_id", "intime", "outtime"],
}

EXPECTED_CMS_TABLES = {
    "cms_claims_puf/inpatient_claims.parquet": [
        "_source_file",
        "_claim_type",
        "_source_year",
        "_ingestion_timestamp_utc",
    ],
}

EXPECTED_REPORTS = [
    "mimic_demo_ingestion_report.json",
    "mimic_demo_profile_report.json",
    "mimic_demo_profile_report.md",
    "cms_claims_puf_ingestion_report.json",
    "cms_claims_puf_profile_report.json",
    "cms_claims_puf_profile_report.md",
]


# =============================================================================
# Validation helpers
# =============================================================================

def validate_parquet_table(relative_path: str, required_columns: list[str], source_group: str) -> dict:
    """
    Validates that a Bronze Parquet table exists, has rows, and contains required columns.
    """

    table_path = REAL_WORLD_BRONZE_DIR / relative_path

    result = {
        "source_group": source_group,
        "relative_path": str(table_path.relative_to(PROJECT_ROOT)),
        "exists": table_path.exists(),
        "row_count": 0,
        "column_count": 0,
        "required_columns": required_columns,
        "missing_required_columns": [],
        "passed": False,
        "error": None,
    }

    if not table_path.exists():
        result["error"] = "Table file does not exist."
        return result

    try:
        df = pd.read_parquet(table_path)

        result["row_count"] = int(len(df))
        result["column_count"] = int(len(df.columns))
        result["missing_required_columns"] = [
            column for column in required_columns if column not in df.columns
        ]

        result["passed"] = (
            result["row_count"] > 0
            and result["column_count"] > 0
            and len(result["missing_required_columns"]) == 0
        )

    except Exception as exc:
        result["error"] = str(exc)

    return result


def validate_report_file(report_name: str) -> dict:
    """
    Validates that a report file exists and is not empty.
    """

    report_path = REPORTS_DIR / report_name

    result = {
        "relative_path": str(report_path.relative_to(PROJECT_ROOT)),
        "exists": report_path.exists(),
        "size_bytes": 0,
        "passed": False,
    }

    if report_path.exists():
        result["size_bytes"] = report_path.stat().st_size
        result["passed"] = result["size_bytes"] > 0

    return result


def write_markdown_report(validation_report: dict, markdown_path: Path) -> None:
    """
    Writes a recruiter-readable validation report for the real-world Bronze layer.
    """

    lines = []

    lines.append("# Real-World Bronze Validation Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("This report validates the real-world/public healthcare Bronze ingestion extension.")
    lines.append("")
    lines.append("It checks that selected MIMIC-IV demo EHR tables and CMS Medicare Claims PUF tables exist as local Parquet Bronze outputs, contain rows, and include expected core columns.")
    lines.append("")
    lines.append("The real-world MIMIC and CMS tracks are intentionally separate and are not force-linked.")
    lines.append("")
    lines.append("## Run Metadata")
    lines.append("")
    lines.append(f"- Pipeline: `{validation_report['pipeline_name']}`")
    lines.append(f"- Validation timestamp UTC: {validation_report['validation_timestamp_utc']}")
    lines.append(f"- Bronze directory: `{validation_report['bronze_directory']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total table checks: {validation_report['total_table_checks']}")
    lines.append(f"- Passed table checks: {validation_report['passed_table_checks']}")
    lines.append(f"- Failed table checks: {validation_report['failed_table_checks']}")
    lines.append(f"- Total report checks: {validation_report['total_report_checks']}")
    lines.append(f"- Passed report checks: {validation_report['passed_report_checks']}")
    lines.append(f"- Failed report checks: {validation_report['failed_report_checks']}")
    lines.append(f"- Overall passed: {validation_report['overall_passed']}")
    lines.append("")

    lines.append("## Table Validation Results")
    lines.append("")
    lines.append("| Source Group | Table | Rows | Columns | Missing Required Columns | Passed |")
    lines.append("|---|---|---:|---:|---|---|")

    for table in validation_report["table_results"]:
        missing_columns = ", ".join(table["missing_required_columns"]) if table["missing_required_columns"] else "None"
        lines.append(
            f"| {table['source_group']} | `{table['relative_path']}` | "
            f"{table['row_count']} | {table['column_count']} | {missing_columns} | {table['passed']} |"
        )

    lines.append("")
    lines.append("## Report File Validation Results")
    lines.append("")
    lines.append("| Report | Size Bytes | Passed |")
    lines.append("|---|---:|---|")

    for report in validation_report["report_results"]:
        lines.append(
            f"| `{report['relative_path']}` | {report['size_bytes']} | {report['passed']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This validation step confirms that the v1.1 real-world ingestion extension can produce local Bronze Parquet outputs and documentation reports from public healthcare datasets.")
    lines.append("")
    lines.append("The synthetic linked EHR + claims pipeline remains the main end-to-end lakehouse demo. The real-world extension demonstrates public-data ingestion and profiling without making invalid patient-level linkage assumptions.")
    lines.append("")

    markdown_path.write_text("\n".join(lines))


# =============================================================================
# Main validation workflow
# =============================================================================

def main() -> None:
    print("Starting real-world Bronze validation...")

    validation_report = {
        "pipeline_name": "real_world_bronze_validation",
        "validation_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bronze_directory": str(REAL_WORLD_BRONZE_DIR.relative_to(PROJECT_ROOT)),
        "table_results": [],
        "report_results": [],
    }

    for relative_path, required_columns in EXPECTED_MIMIC_TABLES.items():
        print(f"Validating MIMIC table: {relative_path}")
        validation_report["table_results"].append(
            validate_parquet_table(
                relative_path=relative_path,
                required_columns=required_columns,
                source_group="MIMIC-IV Demo",
            )
        )

    for relative_path, required_columns in EXPECTED_CMS_TABLES.items():
        print(f"Validating CMS table: {relative_path}")
        validation_report["table_results"].append(
            validate_parquet_table(
                relative_path=relative_path,
                required_columns=required_columns,
                source_group="CMS Claims PUF",
            )
        )

    for report_name in EXPECTED_REPORTS:
        print(f"Validating report file: {report_name}")
        validation_report["report_results"].append(validate_report_file(report_name))

    validation_report["total_table_checks"] = len(validation_report["table_results"])
    validation_report["passed_table_checks"] = sum(
        1 for result in validation_report["table_results"] if result["passed"]
    )
    validation_report["failed_table_checks"] = (
        validation_report["total_table_checks"] - validation_report["passed_table_checks"]
    )

    validation_report["total_report_checks"] = len(validation_report["report_results"])
    validation_report["passed_report_checks"] = sum(
        1 for result in validation_report["report_results"] if result["passed"]
    )
    validation_report["failed_report_checks"] = (
        validation_report["total_report_checks"] - validation_report["passed_report_checks"]
    )

    validation_report["overall_passed"] = (
        validation_report["failed_table_checks"] == 0
        and validation_report["failed_report_checks"] == 0
    )

    json_report_path = REPORTS_DIR / "real_world_bronze_validation_report.json"
    markdown_report_path = REPORTS_DIR / "real_world_bronze_validation_report.md"

    with open(json_report_path, "w") as f:
        json.dump(validation_report, f, indent=2)

    write_markdown_report(validation_report, markdown_report_path)

    print("\n" + "=" * 80)
    print("Real-world Bronze validation complete.")
    print("=" * 80)
    print(f"Passed table checks: {validation_report['passed_table_checks']}/{validation_report['total_table_checks']}")
    print(f"Passed report checks: {validation_report['passed_report_checks']}/{validation_report['total_report_checks']}")
    print(f"Overall passed: {validation_report['overall_passed']}")
    print(f"JSON report written to: {json_report_path.relative_to(PROJECT_ROOT)}")
    print(f"Markdown report written to: {markdown_report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()