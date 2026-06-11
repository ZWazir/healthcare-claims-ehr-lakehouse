from pathlib import Path
import json
import os
from datetime import datetime, timezone

import snowflake.connector


# -----------------------------------------------------------------------------
# Project paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
REPORTS_DIR = PROJECT_ROOT / "reports" / "snowflake"
REPORT_PATH = REPORTS_DIR / "snowflake_load_report.json"


# -----------------------------------------------------------------------------
# Snowflake object names
# -----------------------------------------------------------------------------

SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "HEALTHCARE_LAKEHOUSE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "GOLD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "HEALTHCARE_LAKEHOUSE_WH")
SNOWFLAKE_STAGE = os.getenv("SNOWFLAKE_STAGE", "GOLD_PARQUET_STAGE")


# -----------------------------------------------------------------------------
# Local Gold Parquet files mapped to Snowflake Gold tables
# -----------------------------------------------------------------------------

GOLD_TABLE_LOADS = [
    {
        "local_file": "gold_patient_master.parquet",
        "snowflake_table": "GOLD_PATIENT_MASTER",
    },
    {
        "local_file": "gold_utilization_summary.parquet",
        "snowflake_table": "GOLD_UTILIZATION_SUMMARY",
    },
    {
        "local_file": "gold_condition_summary.parquet",
        "snowflake_table": "GOLD_CONDITION_SUMMARY",
    },
    {
        "local_file": "gold_medication_summary.parquet",
        "snowflake_table": "GOLD_MEDICATION_SUMMARY",
    },
    {
        "local_file": "gold_observation_summary.parquet",
        "snowflake_table": "GOLD_OBSERVATION_SUMMARY",
    },
    {
        "local_file": "gold_patient_risk_features.parquet",
        "snowflake_table": "GOLD_PATIENT_RISK_FEATURES",
    },
]


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def get_required_env_var(name: str) -> str:
    """
    Reads a required environment variable and raises a clear error if it is missing.
    """
    value = os.getenv(name)

    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: {name}\n\n"
            "Set your Snowflake connection variables before running this script.\n"
            "Example:\n"
            "export SNOWFLAKE_ACCOUNT='your_account_identifier'\n"
            "export SNOWFLAKE_USER='your_username'\n"
            "export SNOWFLAKE_PASSWORD='your_password'\n"
            "export SNOWFLAKE_ROLE='ACCOUNTADMIN'\n"
        )

    return value


def validate_local_files() -> None:
    """
    Confirms that all expected Gold Parquet files exist before connecting to Snowflake.
    """
    missing_files = []

    for table_load in GOLD_TABLE_LOADS:
        file_path = GOLD_DIR / table_load["local_file"]

        if not file_path.exists():
            missing_files.append(str(file_path))

    if missing_files:
        raise FileNotFoundError(
            "Missing required Gold Parquet files:\n"
            + "\n".join(missing_files)
            + "\n\nRun the local pipeline first:\n"
            + "python scripts/run_local_pipeline.py"
        )


def connect_to_snowflake():
    """
    Creates a Snowflake connection using environment variables.

    Required:
        SNOWFLAKE_ACCOUNT
        SNOWFLAKE_USER
        SNOWFLAKE_PASSWORD
        SNOWFLAKE_ROLE

    Optional:
        SNOWFLAKE_DATABASE
        SNOWFLAKE_SCHEMA
        SNOWFLAKE_WAREHOUSE
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


def execute_sql(cursor, sql: str) -> None:
    """
    Executes one SQL statement and prints a short progress message.
    """
    print(f"Running SQL:\n{sql}\n")
    cursor.execute(sql)


def get_table_row_count(cursor, table_name: str) -> int:
    """
    Returns the row count for a Snowflake table.
    """
    cursor.execute(f"select count(*) from {table_name}")
    return cursor.fetchone()[0]


def load_parquet_file(cursor, local_file: str, snowflake_table: str) -> dict:
    """
    Loads one local Parquet file into one Snowflake table.

    Process:
        1. Truncate target table.
        2. PUT local Parquet file into Snowflake internal stage.
        3. COPY staged Parquet file into the target table.
        4. Capture row count.
    """
    local_path = GOLD_DIR / local_file
    absolute_file_uri = f"file://{local_path.resolve().as_posix()}"

    print("=" * 80)
    print(f"Loading {local_file} into {snowflake_table}")
    print("=" * 80)

    execute_sql(cursor, f"truncate table {snowflake_table}")

    put_sql = (
        f"put '{absolute_file_uri}' "
        f"@{SNOWFLAKE_STAGE} "
        "auto_compress=false "
        "overwrite=true"
    )
    execute_sql(cursor, put_sql)

    copy_sql = f"""
copy into {snowflake_table}
from @{SNOWFLAKE_STAGE}/{local_file}
file_format = (format_name = HEALTHCARE_PARQUET_FORMAT)
match_by_column_name = case_insensitive
on_error = 'abort_statement'
"""
    execute_sql(cursor, copy_sql)

    row_count = get_table_row_count(cursor, snowflake_table)

    return {
        "local_file": local_file,
        "snowflake_table": snowflake_table,
        "loaded_row_count": row_count,
        "status": "loaded",
    }


# -----------------------------------------------------------------------------
# Main workflow
# -----------------------------------------------------------------------------

def main():
    print("Starting Snowflake Gold table load...")

    validate_local_files()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    load_results = []

    connection = connect_to_snowflake()

    try:
        cursor = connection.cursor()

        execute_sql(cursor, f"use warehouse {SNOWFLAKE_WAREHOUSE}")
        execute_sql(cursor, f"use database {SNOWFLAKE_DATABASE}")
        execute_sql(cursor, f"use schema {SNOWFLAKE_SCHEMA}")

        for table_load in GOLD_TABLE_LOADS:
            result = load_parquet_file(
                cursor=cursor,
                local_file=table_load["local_file"],
                snowflake_table=table_load["snowflake_table"],
            )
            load_results.append(result)

        report = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "snowflake_database": SNOWFLAKE_DATABASE,
            "snowflake_schema": SNOWFLAKE_SCHEMA,
            "snowflake_warehouse": SNOWFLAKE_WAREHOUSE,
            "snowflake_stage": SNOWFLAKE_STAGE,
            "source_gold_directory": str(GOLD_DIR.relative_to(PROJECT_ROOT)),
            "load_results": load_results,
            "status": "success",
        }

        with open(REPORT_PATH, "w") as file:
            json.dump(report, file, indent=2)

        print("\nSnowflake load complete.")
        print(f"Load report saved to: {REPORT_PATH}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()