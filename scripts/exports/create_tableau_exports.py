from pathlib import Path
from datetime import datetime
import json

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
EXPORT_DIR = PROJECT_ROOT / "data" / "tableau_exports"
REPORT_DIR = PROJECT_ROOT / "reports" / "tableau_exports"

EXPORT_CONFIG = [
    {
        "source_file": "gold_patient_master.parquet",
        "export_file": "patient_master_export.csv",
        "description": "Patient-level demographic and master record extract for Tableau.",
        "preferred_key_columns": ["ehr_patient_id", "claim_beneficiary_id"],
    },
    {
        "source_file": "gold_utilization_summary.parquet",
        "export_file": "utilization_summary_export.csv",
        "description": "Patient utilization summary extract for Tableau analysis.",
        "preferred_key_columns": ["ehr_patient_id", "claim_beneficiary_id"],
    },
    {
        "source_file": "gold_condition_summary.parquet",
        "export_file": "condition_summary_export.csv",
        "description": "Patient condition summary extract for Tableau analysis.",
        "preferred_key_columns": ["ehr_patient_id", "claim_beneficiary_id"],
    },
    {
        "source_file": "gold_patient_risk_features.parquet",
        "export_file": "patient_risk_features_export.csv",
        "description": "Patient-level risk feature extract for dashboarding and downstream ML.",
        "preferred_key_columns": ["ehr_patient_id", "claim_beneficiary_id"],
    },
]


def clean_column_name(column_name: str) -> str:
    """
    Standardizes column names for BI tools.

    Tableau can handle many column formats, but clean snake_case names
    are easier to work with in dashboards, joins, and calculated fields.
    """
    return (
        str(column_name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace(".", "_")
    )


def prepare_dataframe_for_tableau(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs lightweight cleanup before exporting to CSV.

    This keeps the Gold data mostly unchanged, while making it easier
    for Tableau Public to read and use.
    """
    cleaned_df = df.copy()

    # Standardize column names.
    cleaned_df.columns = [clean_column_name(col) for col in cleaned_df.columns]

    # Replace infinite values with nulls so Tableau does not misread them.
    cleaned_df = cleaned_df.replace([np.inf, -np.inf], pd.NA)

    # Convert datetime columns to ISO-style date/time strings for CSV compatibility.
    for column in cleaned_df.columns:
        if pd.api.types.is_datetime64_any_dtype(cleaned_df[column]):
            cleaned_df[column] = cleaned_df[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Convert complex object values, if any, into strings that Tableau can safely ingest.
    for column in cleaned_df.columns:
        if cleaned_df[column].dtype == "object":
            cleaned_df[column] = cleaned_df[column].apply(
                lambda value: json.dumps(value) if isinstance(value, (dict, list)) else value
            )

    return cleaned_df


def move_key_columns_to_front(
    df: pd.DataFrame,
    preferred_key_columns: list[str],
) -> pd.DataFrame:
    """
    Moves useful join/key columns to the front of the export.

    This is not required by Tableau, but it makes the CSV easier to inspect
    and easier to join manually in Tableau Public.
    """
    existing_key_columns = [col for col in preferred_key_columns if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in existing_key_columns]

    return df[existing_key_columns + remaining_columns]


def validate_export(
    source_path: Path,
    export_path: Path,
    df: pd.DataFrame,
    preferred_key_columns: list[str],
) -> dict:
    """
    Runs simple validation checks on each Tableau export.

    These checks confirm that the source existed, the export was created,
    rows were written, and expected key columns are present when available.
    """
    validation_result = {
        "source_file": str(source_path.relative_to(PROJECT_ROOT)),
        "export_file": str(export_path.relative_to(PROJECT_ROOT)),
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_preferred_key_columns": [],
        "status": "passed",
        "warnings": [],
    }

    if not source_path.exists():
        validation_result["status"] = "failed"
        validation_result["warnings"].append("Source Parquet file does not exist.")

    if not export_path.exists():
        validation_result["status"] = "failed"
        validation_result["warnings"].append("Export CSV file was not created.")
    elif export_path.stat().st_size == 0:
        validation_result["status"] = "failed"
        validation_result["warnings"].append("Export CSV file is empty.")

    if len(df) == 0:
        validation_result["status"] = "failed"
        validation_result["warnings"].append("Export contains zero rows.")

    duplicate_columns = df.columns[df.columns.duplicated()].tolist()
    if duplicate_columns:
        validation_result["status"] = "failed"
        validation_result["warnings"].append(
            f"Duplicate column names found after cleaning: {duplicate_columns}"
        )

    missing_keys = [col for col in preferred_key_columns if col not in df.columns]
    validation_result["missing_preferred_key_columns"] = missing_keys

    if missing_keys:
        validation_result["warnings"].append(
            f"Preferred key columns not found: {missing_keys}"
        )

    return validation_result


def export_tableau_files() -> dict:
    """
    Creates Tableau-ready CSV extracts from selected Gold Parquet tables.

    The output is intentionally simple: clean CSV files that can be loaded
    directly into Tableau Public or used as shareable BI extracts.
    """
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "export_timestamp": datetime.now().isoformat(timespec="seconds"),
        "source_layer": "Gold",
        "export_layer": "Tableau CSV extracts",
        "exports": [],
    }

    print("Creating Tableau-ready exports...")
    print(f"Gold source directory: {GOLD_DIR}")
    print(f"Tableau export directory: {EXPORT_DIR}")

    for export_config in EXPORT_CONFIG:
        source_path = GOLD_DIR / export_config["source_file"]
        export_path = EXPORT_DIR / export_config["export_file"]

        print("\n----------------------------------------")
        print(f"Source: {source_path.relative_to(PROJECT_ROOT)}")
        print(f"Export: {export_path.relative_to(PROJECT_ROOT)}")

        if not source_path.exists():
            raise FileNotFoundError(
                f"Missing required Gold table: {source_path}. "
                "Run the local pipeline before creating Tableau exports."
            )

        df = pd.read_parquet(source_path)
        cleaned_df = prepare_dataframe_for_tableau(df)
        cleaned_df = move_key_columns_to_front(
            cleaned_df,
            export_config["preferred_key_columns"],
        )

        cleaned_df.to_csv(export_path, index=False)

        validation_result = validate_export(
            source_path=source_path,
            export_path=export_path,
            df=cleaned_df,
            preferred_key_columns=export_config["preferred_key_columns"],
        )

        export_record = {
            "description": export_config["description"],
            **validation_result,
        }

        manifest["exports"].append(export_record)

        print(f"Rows exported: {validation_result['row_count']}")
        print(f"Columns exported: {validation_result['column_count']}")
        print(f"Validation status: {validation_result['status']}")

        if validation_result["warnings"]:
            print("Warnings:")
            for warning in validation_result["warnings"]:
                print(f"  - {warning}")

    manifest_path = REPORT_DIR / "tableau_export_manifest.json"

    with manifest_path.open("w", encoding="utf-8") as manifest_file:
        json.dump(manifest, manifest_file, indent=2)

    print("\n========================================")
    print("Tableau export process complete.")
    print(f"Manifest written to: {manifest_path.relative_to(PROJECT_ROOT)}")

    failed_exports = [
        export for export in manifest["exports"] if export["status"] != "passed"
    ]

    if failed_exports:
        raise ValueError(
            "One or more Tableau exports failed validation. "
            f"Review {manifest_path.relative_to(PROJECT_ROOT)} for details."
        )

    return manifest


if __name__ == "__main__":
    export_tableau_files()