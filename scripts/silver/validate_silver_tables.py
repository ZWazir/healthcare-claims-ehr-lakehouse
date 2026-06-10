from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SILVER_DIR = PROJECT_ROOT / "data" / "silver"


REQUIRED_TABLES = {
    "silver_patients.parquet",
    "silver_encounters.parquet",
    "silver_conditions.parquet",
    "silver_medications.parquet",
    "silver_observations.parquet",
    "silver_claims_beneficiaries.parquet",
    "silver_inpatient_claims.parquet",
    "silver_outpatient_claims.parquet",
}


REQUIRED_COLUMNS_BY_TABLE = {
    "silver_patients.parquet": {
        "ehr_patient_id",
        "birth_date",
        "gender",
        "race",
        "ethnicity",
        "source_system",
        "source_file",
    },
    "silver_encounters.parquet": {
        "encounter_id",
        "ehr_patient_id",
        "encounter_start",
        "encounter_class",
        "total_claim_cost",
    },
    "silver_conditions.parquet": {
        "ehr_patient_id",
        "condition_code",
        "condition_description",
        "is_active_condition",
    },
    "silver_medications.parquet": {
        "ehr_patient_id",
        "medication_code",
        "medication_description",
        "total_cost",
    },
    "silver_observations.parquet": {
        "ehr_patient_id",
        "observation_code",
        "observation_description",
        "observation_value",
    },
    "silver_claims_beneficiaries.parquet": {
        "claim_beneficiary_id",
        "birth_date",
        "has_chf",
        "has_diabetes",
        "chronic_condition_count",
        "total_annual_reimbursement_amount",
    },
    "silver_inpatient_claims.parquet": {
        "claim_beneficiary_id",
        "claim_id",
        "claim_payment_amount",
        "claim_type",
    },
    "silver_outpatient_claims.parquet": {
        "claim_beneficiary_id",
        "claim_id",
        "claim_payment_amount",
        "claim_type",
    },
}


def validate_silver_table(file_name: str) -> dict:
    """
    Validate one Silver table.
    """
    file_path = SILVER_DIR / file_name

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
        result["error"] = "Missing required Silver table."
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


def validate_all_silver_tables() -> pd.DataFrame:
    """
    Validate all required Silver tables.
    """
    results = [
        validate_silver_table(file_name)
        for file_name in sorted(REQUIRED_TABLES)
    ]

    return pd.DataFrame(results)


def main() -> None:
    validation_df = validate_all_silver_tables()

    print(validation_df.to_string(index=False))

    failed_count = (validation_df["status"] == "fail").sum()

    if failed_count > 0:
        raise SystemExit(f"Silver validation failed for {failed_count} table(s).")

    print("\nAll Silver tables passed validation.")


if __name__ == "__main__":
    main()