from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"


def read_silver_table(table_name: str) -> pd.DataFrame:
    """
    Read a Silver Parquet table into a pandas DataFrame.
    """
    file_path = SILVER_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver table not found: {file_path}")

    return pd.read_parquet(file_path)


def write_gold_table(df: pd.DataFrame, table_name: str) -> None:
    """
    Write a Gold table to the local Gold folder as Parquet.
    """
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    output_path = GOLD_DIR / f"{table_name}.parquet"

    df.to_parquet(output_path, index=False)

    print(f"Wrote Gold table: {output_path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print()


def calculate_age(birth_date: pd.Series, reference_date: str = "2024-01-01") -> pd.Series:
    """
    Calculate approximate patient age as of a fixed reference date.

    A fixed date keeps the portfolio output reproducible.
    """
    reference_timestamp = pd.Timestamp(reference_date)
    age_days = reference_timestamp - birth_date

    return (age_days.dt.days / 365.25).fillna(0).astype(int)


def build_patient_crosswalk() -> pd.DataFrame:
    """
    Create a synthetic crosswalk between EHR patient IDs and claims beneficiary IDs.

    Synthea and SynPUF are separate synthetic datasets, so they do not naturally
    share patient identifiers. For portfolio purposes, we create a deterministic
    row-number based crosswalk.
    """
    patients = read_silver_table("silver_patients")
    beneficiaries = read_silver_table("silver_claims_beneficiaries")

    patients_sorted = patients.sort_values("ehr_patient_id").reset_index(drop=True)
    beneficiaries_sorted = beneficiaries.sort_values("claim_beneficiary_id").reset_index(
        drop=True
    )

    crosswalk_size = min(len(patients_sorted), len(beneficiaries_sorted))

    crosswalk = pd.DataFrame(
        {
            "ehr_patient_id": patients_sorted.loc[: crosswalk_size - 1, "ehr_patient_id"],
            "claim_beneficiary_id": beneficiaries_sorted.loc[
                : crosswalk_size - 1, "claim_beneficiary_id"
            ],
            "crosswalk_method": "synthetic_row_number_match",
        }
    )

    return crosswalk


def build_gold_patient_master() -> pd.DataFrame:
    """
    Build a combined patient master table using EHR demographics and claims demographics.
    """
    patients = read_silver_table("silver_patients")
    beneficiaries = read_silver_table("silver_claims_beneficiaries")
    crosswalk = build_patient_crosswalk()

    patient_master = (
        crosswalk.merge(patients, on="ehr_patient_id", how="left")
        .merge(beneficiaries, on="claim_beneficiary_id", how="left", suffixes=("_ehr", "_claims"))
    )

    patient_master["age"] = calculate_age(patient_master["birth_date_ehr"])

    selected_columns = [
        "ehr_patient_id",
        "claim_beneficiary_id",
        "crosswalk_method",
        "age",
        "gender",
        "race",
        "ethnicity",
        "city",
        "state",
        "county",
        "zip_code",
        "sex_code",
        "race_code",
        "state_code",
        "county_code",
        "is_deceased_ehr",
        "is_deceased_claims",
    ]

    return patient_master[selected_columns]


def build_gold_condition_summary() -> pd.DataFrame:
    """
    Build patient-level condition features from EHR conditions and claims chronic flags.
    """
    conditions = read_silver_table("silver_conditions")
    beneficiaries = read_silver_table("silver_claims_beneficiaries")
    crosswalk = build_patient_crosswalk()

    ehr_condition_summary = (
        conditions.groupby("ehr_patient_id")
        .agg(
            ehr_condition_count=("condition_code", "count"),
            ehr_active_condition_count=("is_active_condition", "sum"),
            ehr_unique_condition_count=("condition_code", "nunique"),
        )
        .reset_index()
    )

    chronic_cols = [
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
        "chronic_condition_count",
    ]

    claims_condition_summary = beneficiaries[
        ["claim_beneficiary_id"] + chronic_cols
    ].copy()

    condition_summary = (
        crosswalk.merge(ehr_condition_summary, on="ehr_patient_id", how="left")
        .merge(claims_condition_summary, on="claim_beneficiary_id", how="left")
    )

    fill_zero_cols = [
        "ehr_condition_count",
        "ehr_active_condition_count",
        "ehr_unique_condition_count",
    ] + chronic_cols

    condition_summary[fill_zero_cols] = condition_summary[fill_zero_cols].fillna(0)

    return condition_summary


def build_gold_utilization_summary() -> pd.DataFrame:
    """
    Build patient-level utilization features from encounters and claims.
    """
    encounters = read_silver_table("silver_encounters")
    inpatient_claims = read_silver_table("silver_inpatient_claims")
    outpatient_claims = read_silver_table("silver_outpatient_claims")
    crosswalk = build_patient_crosswalk()

    encounter_summary = (
        encounters.groupby("ehr_patient_id")
        .agg(
            ehr_encounter_count=("encounter_id", "count"),
            ehr_total_encounter_cost=("total_claim_cost", "sum"),
            ehr_avg_encounter_cost=("total_claim_cost", "mean"),
            ehr_emergency_encounter_count=(
                "encounter_class",
                lambda values: (values == "emergency").sum(),
            ),
            ehr_outpatient_encounter_count=(
                "encounter_class",
                lambda values: (values == "outpatient").sum(),
            ),
            ehr_ambulatory_encounter_count=(
                "encounter_class",
                lambda values: (values == "ambulatory").sum(),
            ),
            ehr_total_encounter_duration_hours=("encounter_duration_hours", "sum"),
        )
        .reset_index()
    )

    inpatient_summary = (
        inpatient_claims.groupby("claim_beneficiary_id")
        .agg(
            inpatient_claim_count=("claim_id", "count"),
            inpatient_total_paid=("claim_payment_amount", "sum"),
            inpatient_avg_paid=("claim_payment_amount", "mean"),
            inpatient_total_days=("utilization_day_count", "sum"),
        )
        .reset_index()
    )

    outpatient_summary = (
        outpatient_claims.groupby("claim_beneficiary_id")
        .agg(
            outpatient_claim_count=("claim_id", "count"),
            outpatient_total_paid=("claim_payment_amount", "sum"),
            outpatient_avg_paid=("claim_payment_amount", "mean"),
        )
        .reset_index()
    )

    utilization_summary = (
        crosswalk.merge(encounter_summary, on="ehr_patient_id", how="left")
        .merge(inpatient_summary, on="claim_beneficiary_id", how="left")
        .merge(outpatient_summary, on="claim_beneficiary_id", how="left")
    )

    numeric_cols = [
        col
        for col in utilization_summary.columns
        if col not in {"ehr_patient_id", "claim_beneficiary_id", "crosswalk_method"}
    ]

    utilization_summary[numeric_cols] = utilization_summary[numeric_cols].fillna(0)

    utilization_summary["total_claim_count"] = (
        utilization_summary["inpatient_claim_count"]
        + utilization_summary["outpatient_claim_count"]
    )

    utilization_summary["total_claims_paid"] = (
        utilization_summary["inpatient_total_paid"]
        + utilization_summary["outpatient_total_paid"]
    )

    return utilization_summary


def build_gold_medication_summary() -> pd.DataFrame:
    """
    Build patient-level medication features from EHR medications.
    """
    medications = read_silver_table("silver_medications")
    crosswalk = build_patient_crosswalk()

    medication_summary = (
        medications.groupby("ehr_patient_id")
        .agg(
            medication_count=("medication_code", "count"),
            active_medication_count=("is_active_medication", "sum"),
            unique_medication_count=("medication_code", "nunique"),
            total_medication_cost=("total_cost", "sum"),
            avg_medication_cost=("total_cost", "mean"),
            total_dispenses=("dispenses", "sum"),
        )
        .reset_index()
    )

    medication_summary = crosswalk.merge(
        medication_summary,
        on="ehr_patient_id",
        how="left",
    )

    numeric_cols = [
        "medication_count",
        "active_medication_count",
        "unique_medication_count",
        "total_medication_cost",
        "avg_medication_cost",
        "total_dispenses",
    ]

    medication_summary[numeric_cols] = medication_summary[numeric_cols].fillna(0)

    return medication_summary


def build_gold_observation_summary() -> pd.DataFrame:
    """
    Build patient-level clinical observation features from EHR observations.

    For this MVP, we summarize numeric observation values generally.
    Later, this can be expanded into specific lab features such as A1c or blood pressure.
    """
    observations = read_silver_table("silver_observations")
    crosswalk = build_patient_crosswalk()

    observation_summary = (
        observations.groupby("ehr_patient_id")
        .agg(
            observation_count=("observation_code", "count"),
            unique_observation_count=("observation_code", "nunique"),
            avg_observation_value=("observation_value", "mean"),
            max_observation_value=("observation_value", "max"),
        )
        .reset_index()
    )

    observation_summary = crosswalk.merge(
        observation_summary,
        on="ehr_patient_id",
        how="left",
    )

    numeric_cols = [
        "observation_count",
        "unique_observation_count",
        "avg_observation_value",
        "max_observation_value",
    ]

    observation_summary[numeric_cols] = observation_summary[numeric_cols].fillna(0)

    return observation_summary


def build_gold_patient_risk_features() -> pd.DataFrame:
    """
    Build the main patient-level feature table for reporting and machine learning.
    """
    patient_master = build_gold_patient_master()
    condition_summary = build_gold_condition_summary()
    utilization_summary = build_gold_utilization_summary()
    medication_summary = build_gold_medication_summary()
    observation_summary = build_gold_observation_summary()
    beneficiaries = read_silver_table("silver_claims_beneficiaries")

    reimbursement_cols = [
        "claim_beneficiary_id",
        "inpatient_reimbursement_amount",
        "outpatient_reimbursement_amount",
        "carrier_reimbursement_amount",
        "total_annual_reimbursement_amount",
    ]

    claims_reimbursement = beneficiaries[reimbursement_cols].copy()

    risk_features = (
        patient_master.merge(
            condition_summary.drop(columns=["crosswalk_method"]),
            on=["ehr_patient_id", "claim_beneficiary_id"],
            how="left",
        )
        .merge(
            utilization_summary.drop(columns=["crosswalk_method"]),
            on=["ehr_patient_id", "claim_beneficiary_id"],
            how="left",
        )
        .merge(
            medication_summary.drop(columns=["crosswalk_method"]),
            on=["ehr_patient_id", "claim_beneficiary_id"],
            how="left",
        )
        .merge(
            observation_summary.drop(columns=["crosswalk_method"]),
            on=["ehr_patient_id", "claim_beneficiary_id"],
            how="left",
        )
        .merge(claims_reimbursement, on="claim_beneficiary_id", how="left")
    )

    numeric_cols = risk_features.select_dtypes(include=["number"]).columns
    risk_features[numeric_cols] = risk_features[numeric_cols].fillna(0)

    reimbursement_threshold = risk_features[
        "total_annual_reimbursement_amount"
    ].median()

    risk_features["high_cost_patient_flag"] = (
        risk_features["total_annual_reimbursement_amount"] > reimbursement_threshold
    ).astype(int)

    risk_features["care_management_candidate_flag"] = (
        (
            risk_features["chronic_condition_count"] >= 2
        )
        | (
            risk_features["inpatient_claim_count"] >= 1
        )
        | (
            risk_features["ehr_emergency_encounter_count"] >= 1
        )
    ).astype(int)

    return risk_features


def build_all_gold_tables() -> None:
    """
    Build all Gold analytics tables.
    """
    gold_builders = {
        "gold_patient_crosswalk": build_patient_crosswalk,
        "gold_patient_master": build_gold_patient_master,
        "gold_condition_summary": build_gold_condition_summary,
        "gold_utilization_summary": build_gold_utilization_summary,
        "gold_medication_summary": build_gold_medication_summary,
        "gold_observation_summary": build_gold_observation_summary,
        "gold_patient_risk_features": build_gold_patient_risk_features,
    }

    for table_name, builder_func in gold_builders.items():
        print("=" * 100)
        print(f"Building {table_name}")
        print("=" * 100)

        gold_df = builder_func()
        write_gold_table(gold_df, table_name)


if __name__ == "__main__":
    build_all_gold_tables()