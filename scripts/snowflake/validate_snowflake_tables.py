from pathlib import Path
import json
import os
from datetime import datetime, timezone

import pandas as pd
import snowflake.connector


# -----------------------------------------------------------------------------
# Project paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
REPORTS_DIR = PROJECT_ROOT / "reports" / "snowflake"
REPORT_PATH = REPORTS_DIR / "snowflake_validation_report.json"


# -----------------------------------------------------------------------------
# Snowflake object names
# -----------------------------------------------------------------------------

SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "HEALTHCARE_LAKEHOUSE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "GOLD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "HEALTHCARE_LAKEHOUSE_WH")


# -----------------------------------------------------------------------------
# Local Gold Parquet files mapped to Snowflake Gold tables
# -----------------------------------------------------------------------------

GOLD_TABLE_VALIDATIONS = [
    {
        "local_file": "gold_patient_master.parquet",
        "snowflake_table": "GOLD_PATIENT_MASTER",
        "required_columns": [
            "ehr_patient_id",
            "claim_beneficiary_id",
            "crosswalk_method",
        ],
    },
    {
        "local_file": "gold_utilization_summary.parquet",
        "snowflake_table": "GOLD_UTILIZATION_SUMMARY",
        "required_columns": [
            "ehr_patient_id",
            "claim_beneficiary_id",
            "crosswalk_method",
        ],
    },
    {
        "local_file": "gold_condition_summary.parquet",
        "snowflake_table": "GOLD_CONDITION_SUMMARY",
        "required_columns": [
            "ehr_patient_id",
            "claim_beneficiary_id",
            "crosswalk_method",
        ],
    },
    {
        "local_file": "gold_medication_summary.parquet",
        "snowflake_table": "GOLD_MEDICATION_SUMMARY",
        "required_columns": [
            "ehr_patient_id",
            "claim_beneficiary_id",
            "crosswalk_method",
        ],
    },
    {
        "local_file": "gold_observation_summary.parquet",
        "snowflake_table": "GOLD_OBSERVATION_SUMMARY",
        "required_columns": [
            "ehr_patient_id",
            "claim_beneficiary_id",
            "crosswalk_method",
        ],
    },
    {
        "local_file": "gold_patient_risk_features.parquet",
        "snowflake_table": "GOLD_PATIENT_RISK_FEATURES",
        "required_columns": [
            "ehr_patient_id",
            "claim_beneficiary_id",
            "crosswalk_method",
        ],
    },
]


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def get_required_env_var(name: str) -> str:
    """
    Reads a required environment variable and raises a clear error if missing.
    """
    value = os.getenv(name)

    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: {name}\n\n"
            "Set your Snowflake connection variables before running this script:\n"
            "export SNOWFLAKE_ACCOUNT='your_account_identifier'\n"
            "export SNOWFLAKE_USER='your_username'\n"
            "export SNOWFLAKE_PASSWORD='your_password'\n"
            "export SNOWFLAKE_ROLE='ACCOUNTADMIN'\n"
        )

    return value


def connect_to_snowflake():
    """
    Creates a Snowflake connection using environment variables.
    """
    return snowflake.connector.connect(
        account=get_required_env_var("SNOWFLAKE_ACCOUNT"),
        user=get_required_env_var("SNOWFLAKE_USER"),
        password=get_required_env_var("SNOWFLAKE_PASSWORD"),
        role=get_required_env_var("SNOWFLAKE_ROLE"),
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )


def get_snowflake_row_count(cursor, table_name: str) -> int:
    """
    Returns the row count from a Snowflake table.
    """
    cursor.execute(f"select count(*) from {table_name}")
    return int(cursor.fetchone()[0])


def get_snowflake_null_id_count(cursor, table_name: str) -> int:
    """
    Returns count of rows missing the primary EHR patient identifier.
    """
    cursor.execute(
        f"""
        select count(*)
        from {table_name}
        where ehr_patient_id is null
        """
    )
    return int(cursor.fetchone()[0])


def get_snowflake_columns(cursor, table_name: str) -> list[str]:
    """
    Returns the column names for a Snowflake table.
    """
    cursor.execute(
        f"""
        select column_name
        from information_schema.columns
        where table_catalog = upper('{SNOWFLAKE_DATABASE}')
          and table_schema = upper('{SNOWFLAKE_SCHEMA}')
          and table_name = upper('{table_name}')
        order by ordinal_position
        """
    )

    return [row[0].lower() for row in cursor.fetchall()]


def validate_local_file_exists(local_file: str) -> Path:
    """
    Confirms that a local Gold Parquet file exists.
    """
    file_path = GOLD_DIR / local_file

    if not file_path.exists():
        raise FileNotFoundError(
            f"Missing local Gold file: {file_path}\n\n"
            "Run the local pipeline first:\n"
            "python scripts/run_local_pipeline.py"
        )

    return file_path


def validate_table(cursor, local_file: str, snowflake_table: str, required_columns: list[str]) -> dict:
    """
    Compares one local Gold Parquet file against one Snowflake table.

    Checks:
        1. Local row count
        2. Snowflake row count
        3. Row count match
        4. Required columns exist in Snowflake
        5. Snowflake ehr_patient_id null count
    """
    local_path = validate_local_file_exists(local_file)
    local_df = pd.read_parquet(local_path)

    local_row_count = int(len(local_df))
    snowflake_row_count = get_snowflake_row_count(cursor, snowflake_table)
    row_count_matches = local_row_count == snowflake_row_count

    snowflake_columns = get_snowflake_columns(cursor, snowflake_table)

    missing_required_columns = [
        column
        for column in required_columns
        if column.lower() not in snowflake_columns
    ]

    null_ehr_patient_id_count = get_snowflake_null_id_count(cursor, snowflake_table)

    validation_status = (
        "pass"
        if row_count_matches
        and not missing_required_columns
        and null_ehr_patient_id_count == 0
        else "fail"
    )

    return {
        "local_file": local_file,
        "snowflake_table": snowflake_table,
        "local_row_count": local_row_count,
        "snowflake_row_count": snowflake_row_count,
        "row_count_matches": row_count_matches,
        "required_columns": required_columns,
        "missing_required_columns": missing_required_columns,
        "null_ehr_patient_id_count": null_ehr_patient_id_count,
        "validation_status": validation_status,
    }


# -----------------------------------------------------------------------------
# Main workflow
# -----------------------------------------------------------------------------

def main():
    print("Validating Snowflake Gold tables against local Gold Parquet files...")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    connection = connect_to_snowflake()
    validation_results = []

    try:
        cursor = connection.cursor()

        cursor.execute(f"use warehouse {SNOWFLAKE_WAREHOUSE}")
        cursor.execute(f"use database {SNOWFLAKE_DATABASE}")
        cursor.execute(f"use schema {SNOWFLAKE_SCHEMA}")

        for validation_config in GOLD_TABLE_VALIDATIONS:
            result = validate_table(
                cursor=cursor,
                local_file=validation_config["local_file"],
                snowflake_table=validation_config["snowflake_table"],
                required_columns=validation_config["required_columns"],
            )

            validation_results.append(result)

            status_icon = "PASS" if result["validation_status"] == "pass" else "FAIL"
            print(
                f"{status_icon} | {result['snowflake_table']} | "
                f"local rows: {result['local_row_count']} | "
                f"snowflake rows: {result['snowflake_row_count']}"
            )

        failed_validations = [
            result
            for result in validation_results
            if result["validation_status"] != "pass"
        ]

        overall_status = "pass" if not failed_validations else "fail"

        report = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "snowflake_database": SNOWFLAKE_DATABASE,
            "snowflake_schema": SNOWFLAKE_SCHEMA,
            "snowflake_warehouse": SNOWFLAKE_WAREHOUSE,
            "source_gold_directory": str(GOLD_DIR.relative_to(PROJECT_ROOT)),
            "overall_status": overall_status,
            "validation_results": validation_results,
        }

        with open(REPORT_PATH, "w") as file:
            json.dump(report, file, indent=2)

        print("\nSnowflake validation complete.")
        print(f"Validation report saved to: {REPORT_PATH}")
        print(f"Overall status: {overall_status.upper()}")

        if failed_validations:
            raise ValueError(
                "One or more Snowflake table validations failed. "
                f"See report: {REPORT_PATH}"
            )

    finally:
        connection.close()


if __name__ == "__main__":
    main()