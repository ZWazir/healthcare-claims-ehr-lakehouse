from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"


REQUIRED_TABLES = {
    "gold_patient_crosswalk.parquet",
    "gold_patient_master.parquet",
    "gold_condition_summary.parquet",
    "gold_utilization_summary.parquet",
    "gold_medication_summary.parquet",
    "gold_observation_summary.parquet",
    "gold_patient_risk_features.parquet",
}


REQUIRED_COLUMNS_BY_TABLE = {
    "gold_patient_crosswalk.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "crosswalk_method",
    },
    "gold_patient_master.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "age",
        "gender",
        "race",
        "ethnicity",
    },
    "gold_condition_summary.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "ehr_condition_count",
        "chronic_condition_count",
        "has_chf",
        "has_diabetes",
    },
    "gold_utilization_summary.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "ehr_encounter_count",
        "inpatient_claim_count",
        "outpatient_claim_count",
        "total_claims_paid",
    },
    "gold_medication_summary.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "medication_count",
        "total_medication_cost",
    },
    "gold_observation_summary.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "observation_count",
        "avg_observation_value",
    },
    "gold_patient_risk_features.parquet": {
        "ehr_patient_id",
        "claim_beneficiary_id",
        "age",
        "chronic_condition_count",
        "total_annual_reimbursement_amount",
        "high_cost_patient_flag",
        "care_management_candidate_flag",
    },
}


def validate_gold_table(file_name: str) -> dict:
    """
    Validate one Gold table.
    """
    file_path = GOLD_DIR / file_name

    result = {
        "table": file_name,
        "status": "pass",
        "row_count": 0,
        "column_count": 0,
        "missing_columns": [],
        "error": "",
    }

    if not file_path.exists():
        result["status"] = "fail"
        result["error"] = "Missing required Gold table."
        return result

    try:
        df = pd.read_parquet(file_path)
    except Exception as exc:
        result["status"] = "fail"
        result["error"] = str(exc)
        return result

    result["row_count"] = len(df)
    result["column_count"] = len(df.columns)

    if len(df) == 0:
        result["status"] = "fail"
        result["error"] = "Table has zero rows."

    required_columns = REQUIRED_COLUMNS_BY_TABLE[file_name]
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        result["status"] = "fail"
        result["missing_columns"] = sorted(missing_columns)

    return result


def validate_high_cost_flag() -> dict:
    """
    Validate the high-cost target field used by the ML model.
    """
    file_path = GOLD_DIR / "gold_patient_risk_features.parquet"

    result = {
        "table": "gold_patient_risk_features.parquet",
        "check": "high_cost_patient_flag_has_valid_values",
        "status": "pass",
        "error": "",
    }

    if not file_path.exists():
        result["status"] = "fail"
        result["error"] = "Risk feature table does not exist."
        return result

    df = pd.read_parquet(file_path)

    valid_values = {0, 1}
    actual_values = set(df["high_cost_patient_flag"].dropna().unique())

    if not actual_values.issubset(valid_values):
        result["status"] = "fail"
        result["error"] = f"Invalid values found: {actual_values}"

    return result


def validate_all_gold_tables() -> pd.DataFrame:
    """
    Validate all required Gold tables.
    """
    table_results = [
        validate_gold_table(file_name)
        for file_name in sorted(REQUIRED_TABLES)
    ]

    target_result = validate_high_cost_flag()

    return pd.concat(
        [
            pd.DataFrame(table_results),
            pd.DataFrame([target_result]),
        ],
        ignore_index=True,
        sort=False,
    )


def main() -> None:
    validation_df = validate_all_gold_tables()

    print(validation_df.to_string(index=False))

    failed_count = (validation_df["status"] == "fail").sum()

    if failed_count > 0:
        raise SystemExit(f"Gold validation failed for {failed_count} check(s).")

    print("\nAll Gold tables passed validation.")


if __name__ == "__main__":
    main()