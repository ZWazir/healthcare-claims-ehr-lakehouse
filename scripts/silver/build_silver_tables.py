from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"
SILVER_DIR = PROJECT_ROOT / "data" / "silver"


def read_bronze_table(source_system: str, table_name: str) -> pd.DataFrame:
    """
    Read a Bronze Parquet table into a pandas DataFrame.
    """
    file_path = BRONZE_DIR / source_system / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Bronze table not found: {file_path}")

    return pd.read_parquet(file_path)


def write_silver_table(df: pd.DataFrame, table_name: str) -> None:
    """
    Write a Silver table to the local Silver folder as Parquet.
    """
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    output_path = SILVER_DIR / f"{table_name}.parquet"

    df.to_parquet(output_path, index=False)

    print(f"Wrote Silver table: {output_path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print()


def parse_date(series: pd.Series) -> pd.Series:
    """
    Parse date-like values into pandas datetime values.

    Invalid or blank values become NaT.
    """
    return pd.to_datetime(series.replace("", pd.NA), errors="coerce")


def parse_yyyymmdd(series: pd.Series) -> pd.Series:
    """
    Parse CMS-style YYYYMMDD date fields.
    """
    return pd.to_datetime(series.replace("", pd.NA), format="%Y%m%d", errors="coerce")


def to_numeric(series: pd.Series) -> pd.Series:
    """
    Convert numeric-looking values into numbers.

    Invalid or blank values become 0.
    """
    return pd.to_numeric(series.replace("", pd.NA), errors="coerce").fillna(0)


def build_silver_patients() -> pd.DataFrame:
    """
    Build a cleaned EHR patient table from Synthea patients.
    """
    df = read_bronze_table("synthea", "patients")

    silver_df = pd.DataFrame(
        {
            "ehr_patient_id": df["id"],
            "birth_date": parse_date(df["birthdate"]),
            "death_date": parse_date(df["deathdate"]),
            "first_name": df["first"],
            "last_name": df["last"],
            "gender": df["gender"],
            "race": df["race"],
            "ethnicity": df["ethnicity"],
            "city": df["city"],
            "state": df["state"],
            "county": df["county"],
            "zip_code": df["zip"],
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    silver_df["is_deceased"] = silver_df["death_date"].notna()

    return silver_df


def build_silver_encounters() -> pd.DataFrame:
    """
    Build a cleaned EHR encounter table from Synthea encounters.
    """
    df = read_bronze_table("synthea", "encounters")

    silver_df = pd.DataFrame(
        {
            "encounter_id": df["id"],
            "ehr_patient_id": df["patient"],
            "encounter_start": parse_date(df["start"]),
            "encounter_stop": parse_date(df["stop"]),
            "organization_id": df["organization"],
            "provider_id": df["provider"],
            "payer_id": df["payer"],
            "encounter_class": df["encounterclass"],
            "encounter_code": df["code"],
            "encounter_description": df["description"],
            "base_encounter_cost": to_numeric(df["base_encounter_cost"]),
            "total_claim_cost": to_numeric(df["total_claim_cost"]),
            "payer_coverage": to_numeric(df["payer_coverage"]),
            "reason_code": df["reasoncode"],
            "reason_description": df["reasondescription"],
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    silver_df["encounter_duration_hours"] = (
        silver_df["encounter_stop"] - silver_df["encounter_start"]
    ).dt.total_seconds() / 3600

    silver_df["encounter_duration_hours"] = silver_df[
        "encounter_duration_hours"
    ].fillna(0)

    return silver_df


def build_silver_conditions() -> pd.DataFrame:
    """
    Build a cleaned EHR condition table from Synthea conditions.
    """
    df = read_bronze_table("synthea", "conditions")

    silver_df = pd.DataFrame(
        {
            "condition_start_date": parse_date(df["start"]),
            "condition_stop_date": parse_date(df["stop"]),
            "ehr_patient_id": df["patient"],
            "encounter_id": df["encounter"],
            "condition_code": df["code"],
            "condition_description": df["description"],
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    silver_df["is_active_condition"] = silver_df["condition_stop_date"].isna()

    return silver_df


def build_silver_medications() -> pd.DataFrame:
    """
    Build a cleaned EHR medication table from Synthea medications.
    """
    df = read_bronze_table("synthea", "medications")

    silver_df = pd.DataFrame(
        {
            "medication_start_date": parse_date(df["start"]),
            "medication_stop_date": parse_date(df["stop"]),
            "ehr_patient_id": df["patient"],
            "payer_id": df["payer"],
            "encounter_id": df["encounter"],
            "medication_code": df["code"],
            "medication_description": df["description"],
            "base_cost": to_numeric(df["base_cost"]),
            "payer_coverage": to_numeric(df["payer_coverage"]),
            "dispenses": to_numeric(df["dispenses"]),
            "total_cost": to_numeric(df["totalcost"]),
            "reason_code": df["reasoncode"],
            "reason_description": df["reasondescription"],
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    silver_df["is_active_medication"] = silver_df["medication_stop_date"].isna()

    return silver_df


def build_silver_observations() -> pd.DataFrame:
    """
    Build a cleaned EHR observation table from Synthea observations.
    """
    df = read_bronze_table("synthea", "observations")

    silver_df = pd.DataFrame(
        {
            "observation_date": parse_date(df["date"]),
            "ehr_patient_id": df["patient"],
            "encounter_id": df["encounter"],
            "observation_code": df["code"],
            "observation_description": df["description"],
            "observation_value": to_numeric(df["value"]),
            "observation_units": df["units"],
            "observation_type": df["type"],
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    return silver_df


def build_silver_claims_beneficiaries() -> pd.DataFrame:
    """
    Build a cleaned claims-side beneficiary table from SynPUF beneficiary summary.
    """
    df = read_bronze_table("synpuf", "beneficiary_summary")

    silver_df = pd.DataFrame(
        {
            "claim_beneficiary_id": df["desynpuf_id"],
            "birth_date": parse_yyyymmdd(df["bene_birth_dt"]),
            "death_date": parse_yyyymmdd(df["bene_death_dt"]),
            "sex_code": df["bene_sex_ident_cd"],
            "race_code": df["bene_race_cd"],
            "state_code": df["sp_state_code"],
            "county_code": df["bene_county_cd"],
            "has_esrd": to_numeric(df["bene_esrd_ind"]).astype(int),
            "has_alzheimer_or_dementia": to_numeric(df["sp_alzhdmta"]).astype(int),
            "has_chf": to_numeric(df["sp_chf"]).astype(int),
            "has_chronic_kidney_disease": to_numeric(df["sp_chrnkidn"]).astype(int),
            "has_cancer": to_numeric(df["sp_cncr"]).astype(int),
            "has_copd": to_numeric(df["sp_copd"]).astype(int),
            "has_depression": to_numeric(df["sp_depressn"]).astype(int),
            "has_diabetes": to_numeric(df["sp_diabetes"]).astype(int),
            "has_ischemic_heart_disease": to_numeric(df["sp_ischmcht"]).astype(int),
            "has_osteoporosis": to_numeric(df["sp_osteoprs"]).astype(int),
            "has_rheumatoid_or_osteoarthritis": to_numeric(df["sp_ra_oa"]).astype(int),
            "has_stroke_or_tia": to_numeric(df["sp_strketia"]).astype(int),
            "inpatient_reimbursement_amount": to_numeric(df["medreimb_ip"]),
            "outpatient_reimbursement_amount": to_numeric(df["medreimb_op"]),
            "carrier_reimbursement_amount": to_numeric(df["medreimb_car"]),
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    chronic_condition_cols = [
        "has_alzheimer_or_dementia",
        "has_chf",
        "has_chronic_kidney_disease",
        "has_cancer",
        "has_copd",
        "has_depression",
        "has_diabetes",
        "has_ischemic_heart_disease",
        "has_osteoporosis",
        "has_rheumatoid_or_osteoarthritis",
        "has_stroke_or_tia",
    ]

    silver_df["chronic_condition_count"] = silver_df[chronic_condition_cols].sum(axis=1)

    silver_df["total_annual_reimbursement_amount"] = (
        silver_df["inpatient_reimbursement_amount"]
        + silver_df["outpatient_reimbursement_amount"]
        + silver_df["carrier_reimbursement_amount"]
    )

    silver_df["is_deceased"] = silver_df["death_date"].notna()

    return silver_df


def build_silver_inpatient_claims() -> pd.DataFrame:
    """
    Build a cleaned inpatient claims table from SynPUF inpatient claims.
    """
    df = read_bronze_table("synpuf", "inpatient_claims")

    silver_df = pd.DataFrame(
        {
            "claim_beneficiary_id": df["desynpuf_id"],
            "claim_id": df["clm_id"],
            "claim_from_date": parse_yyyymmdd(df["clm_from_dt"]),
            "claim_thru_date": parse_yyyymmdd(df["clm_thru_dt"]),
            "provider_id": df["prvdr_num"],
            "claim_payment_amount": to_numeric(df["clm_pmt_amt"]),
            "admission_date": parse_yyyymmdd(df["clm_admsn_dt"]),
            "discharge_date": parse_yyyymmdd(df["nch_bene_dschrg_dt"]),
            "utilization_day_count": to_numeric(df["clm_utlztn_day_cnt"]),
            "primary_diagnosis_code": df["icd9_dgns_cd_1"],
            "diagnosis_code_2": df["icd9_dgns_cd_2"],
            "diagnosis_code_3": df["icd9_dgns_cd_3"],
            "primary_procedure_code": df["icd9_prcdr_cd_1"],
            "drg_code": df["clm_drg_cd"],
            "claim_type": "inpatient",
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    return silver_df


def build_silver_outpatient_claims() -> pd.DataFrame:
    """
    Build a cleaned outpatient claims table from SynPUF outpatient claims.
    """
    df = read_bronze_table("synpuf", "outpatient_claims")

    silver_df = pd.DataFrame(
        {
            "claim_beneficiary_id": df["desynpuf_id"],
            "claim_id": df["clm_id"],
            "claim_from_date": parse_yyyymmdd(df["clm_from_dt"]),
            "claim_thru_date": parse_yyyymmdd(df["clm_thru_dt"]),
            "provider_id": df["prvdr_num"],
            "claim_payment_amount": to_numeric(df["clm_pmt_amt"]),
            "primary_diagnosis_code": df["icd9_dgns_cd_1"],
            "claim_type": "outpatient",
            "source_system": df["bronze_source_system"],
            "source_file": df["bronze_source_file"],
        }
    )

    return silver_df


def build_all_silver_tables() -> None:
    """
    Build all Silver tables.
    """
    silver_builders = {
        "silver_patients": build_silver_patients,
        "silver_encounters": build_silver_encounters,
        "silver_conditions": build_silver_conditions,
        "silver_medications": build_silver_medications,
        "silver_observations": build_silver_observations,
        "silver_claims_beneficiaries": build_silver_claims_beneficiaries,
        "silver_inpatient_claims": build_silver_inpatient_claims,
        "silver_outpatient_claims": build_silver_outpatient_claims,
    }

    for table_name, builder_func in silver_builders.items():
        print("=" * 100)
        print(f"Building {table_name}")
        print("=" * 100)

        silver_df = builder_func()
        write_silver_table(silver_df, table_name)


if __name__ == "__main__":
    build_all_silver_tables()