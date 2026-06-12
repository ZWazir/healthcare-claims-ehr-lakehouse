# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Gold Delta Layer
# MAGIC
# MAGIC This notebook-style script builds Gold analytics tables from Silver Delta tables.
# MAGIC
# MAGIC The Gold layer creates patient-level analytics marts that are ready for:
# MAGIC
# MAGIC - Healthcare utilization analysis
# MAGIC - Chronic condition analysis
# MAGIC - Medication and observation summaries
# MAGIC - Patient risk feature engineering
# MAGIC - BI dashboards in Tableau or Streamlit
# MAGIC - Downstream warehouse loading into Snowflake
# MAGIC - Machine learning workflows in PyTorch
# MAGIC
# MAGIC **Note:** This file is intended for Databricks Runtime. Local VS Code warnings about
# MAGIC `spark`, `display`, or PySpark are expected if Spark is not installed locally.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Configure Lakehouse Paths
# MAGIC
# MAGIC These paths assume the Bronze and Silver notebooks wrote Delta tables to DBFS.
# MAGIC Adjust the base path if your Databricks workspace uses a different mount location.

# COMMAND ----------

BASE_PATH = "/mnt/healthcare_claims_ehr_lakehouse"
SILVER_PATH = f"{BASE_PATH}/silver"
GOLD_PATH = f"{BASE_PATH}/gold"

# Silver Delta input paths
SILVER_PATIENTS_PATH = f"{SILVER_PATH}/silver_patients"
SILVER_ENCOUNTERS_PATH = f"{SILVER_PATH}/silver_encounters"
SILVER_CONDITIONS_PATH = f"{SILVER_PATH}/silver_conditions"
SILVER_MEDICATIONS_PATH = f"{SILVER_PATH}/silver_medications"
SILVER_OBSERVATIONS_PATH = f"{SILVER_PATH}/silver_observations"
SILVER_BENEFICIARIES_PATH = f"{SILVER_PATH}/silver_claims_beneficiaries"
SILVER_INPATIENT_PATH = f"{SILVER_PATH}/silver_inpatient_claims"
SILVER_OUTPATIENT_PATH = f"{SILVER_PATH}/silver_outpatient_claims"
SILVER_CARRIER_PATH = f"{SILVER_PATH}/silver_carrier_claims"
SILVER_PRESCRIPTION_PATH = f"{SILVER_PATH}/silver_prescription_drug_events"

# Gold Delta output paths
GOLD_CROSSWALK_PATH = f"{GOLD_PATH}/gold_patient_crosswalk"
GOLD_PATIENT_MASTER_PATH = f"{GOLD_PATH}/gold_patient_master"
GOLD_UTILIZATION_SUMMARY_PATH = f"{GOLD_PATH}/gold_utilization_summary"
GOLD_CONDITION_SUMMARY_PATH = f"{GOLD_PATH}/gold_condition_summary"
GOLD_MEDICATION_SUMMARY_PATH = f"{GOLD_PATH}/gold_medication_summary"
GOLD_OBSERVATION_SUMMARY_PATH = f"{GOLD_PATH}/gold_observation_summary"
GOLD_PATIENT_RISK_FEATURES_PATH = f"{GOLD_PATH}/gold_patient_risk_features"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Helper Functions
# MAGIC
# MAGIC These functions keep the notebook readable and make the Gold logic easier to reuse.

# COMMAND ----------

def read_delta(path: str):
    """Read a Delta table from DBFS."""
    return spark.read.format("delta").load(path)


def write_gold_delta(df, path: str):
    """
    Write a Gold Delta table.
    
    overwriteSchema is useful during portfolio development because table schemas
    may evolve as features are added.
    """
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(path)
    )


def add_missing_column(df, column_name: str, default_value=None):
    """Add a column only if it does not already exist."""
    if column_name not in df.columns:
        return df.withColumn(column_name, F.lit(default_value))
    return df


def select_existing_columns(df, columns):
    """Select only columns that exist in a DataFrame."""
    return df.select([c for c in columns if c in df.columns])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Read Silver Delta Tables
# MAGIC
# MAGIC The Silver layer contains cleaned, standardized clinical and claims tables.

# COMMAND ----------

patients = read_delta(SILVER_PATIENTS_PATH)
encounters = read_delta(SILVER_ENCOUNTERS_PATH)
conditions = read_delta(SILVER_CONDITIONS_PATH)
medications = read_delta(SILVER_MEDICATIONS_PATH)
observations = read_delta(SILVER_OBSERVATIONS_PATH)
beneficiaries = read_delta(SILVER_BENEFICIARIES_PATH)
inpatient_claims = read_delta(SILVER_INPATIENT_PATH)
outpatient_claims = read_delta(SILVER_OUTPATIENT_PATH)
carrier_claims = read_delta(SILVER_CARRIER_PATH)
prescription_events = read_delta(SILVER_PRESCRIPTION_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Create Patient Crosswalk
# MAGIC
# MAGIC This creates a simple synthetic bridge between EHR patients and claims beneficiaries.
# MAGIC
# MAGIC In a real healthcare lakehouse, this would usually come from an enterprise master
# MAGIC patient index, deterministic matching, or privacy-preserving patient linkage process.
# MAGIC For this portfolio project, a row-number based synthetic crosswalk is acceptable.

# COMMAND ----------

ehr_patient_ids = (
    patients
    .select(F.col("patient_id").alias("ehr_patient_id"))
    .dropDuplicates()
    .withColumn("crosswalk_row_number", F.row_number().over(Window.orderBy("ehr_patient_id")))
)

claim_beneficiary_ids = (
    beneficiaries
    .select(F.col("beneficiary_id").alias("claim_beneficiary_id"))
    .dropDuplicates()
    .withColumn("crosswalk_row_number", F.row_number().over(Window.orderBy("claim_beneficiary_id")))
)

gold_patient_crosswalk = (
    ehr_patient_ids
    .join(claim_beneficiary_ids, on="crosswalk_row_number", how="inner")
    .drop("crosswalk_row_number")
    .withColumn("crosswalk_method", F.lit("synthetic_row_number_match"))
)

write_gold_delta(gold_patient_crosswalk, GOLD_CROSSWALK_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Create Gold Patient Master
# MAGIC
# MAGIC The patient master table combines EHR demographic fields with claims beneficiary identifiers.
# MAGIC This becomes the main patient dimension for analytics, BI, and ML.

# COMMAND ----------

gold_patient_master = (
    gold_patient_crosswalk
    .join(
        patients,
        gold_patient_crosswalk.ehr_patient_id == patients.patient_id,
        how="left"
    )
    .join(
        beneficiaries,
        gold_patient_crosswalk.claim_beneficiary_id == beneficiaries.beneficiary_id,
        how="left"
    )
    .select(
        "ehr_patient_id",
        "claim_beneficiary_id",
        "crosswalk_method",
        F.col("birth_date"),
        F.col("gender"),
        F.col("race"),
        F.col("ethnicity"),
        F.col("city"),
        F.col("state"),
        F.col("county"),
        F.col("zip_code"),
        F.col("sex_code"),
        F.col("race_code"),
        F.col("state_code"),
        F.col("county_code"),
        F.col("is_deceased").alias("is_deceased_ehr"),
        F.col("beneficiary_death_flag").alias("is_deceased_claims")
    )
    .withColumn(
        "age",
        F.floor(F.months_between(F.current_date(), F.col("birth_date")) / 12)
    )
)

write_gold_delta(gold_patient_master, GOLD_PATIENT_MASTER_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Create Gold Utilization Summary
# MAGIC
# MAGIC This table summarizes patient healthcare usage across EHR encounters and claims.
# MAGIC It supports questions like:
# MAGIC
# MAGIC - Which patients have the highest utilization?
# MAGIC - How many inpatient, outpatient, and carrier claims does each patient have?
# MAGIC - Which patients may need care management intervention?

# COMMAND ----------

ehr_utilization = (
    encounters
    .groupBy(F.col("patient_id").alias("ehr_patient_id"))
    .agg(
        F.count("*").alias("ehr_encounter_count"),
        F.countDistinct("encounter_id").alias("distinct_ehr_encounter_count"),
        F.min("encounter_start_date").alias("first_ehr_encounter_date"),
        F.max("encounter_start_date").alias("last_ehr_encounter_date")
    )
)

inpatient_utilization = (
    inpatient_claims
    .groupBy(F.col("beneficiary_id").alias("claim_beneficiary_id"))
    .agg(
        F.count("*").alias("inpatient_claim_count"),
        F.sum(F.coalesce(F.col("claim_payment_amount"), F.lit(0))).alias("total_inpatient_paid_amount")
    )
)

outpatient_utilization = (
    outpatient_claims
    .groupBy(F.col("beneficiary_id").alias("claim_beneficiary_id"))
    .agg(
        F.count("*").alias("outpatient_claim_count"),
        F.sum(F.coalesce(F.col("claim_payment_amount"), F.lit(0))).alias("total_outpatient_paid_amount")
    )
)

carrier_utilization = (
    carrier_claims
    .groupBy(F.col("beneficiary_id").alias("claim_beneficiary_id"))
    .agg(
        F.count("*").alias("carrier_claim_count"),
        F.sum(F.coalesce(F.col("claim_payment_amount"), F.lit(0))).alias("total_carrier_paid_amount")
    )
)

gold_utilization_summary = (
    gold_patient_crosswalk
    .join(ehr_utilization, on="ehr_patient_id", how="left")
    .join(inpatient_utilization, on="claim_beneficiary_id", how="left")
    .join(outpatient_utilization, on="claim_beneficiary_id", how="left")
    .join(carrier_utilization, on="claim_beneficiary_id", how="left")
    .fillna(
        {
            "ehr_encounter_count": 0,
            "distinct_ehr_encounter_count": 0,
            "inpatient_claim_count": 0,
            "outpatient_claim_count": 0,
            "carrier_claim_count": 0,
            "total_inpatient_paid_amount": 0,
            "total_outpatient_paid_amount": 0,
            "total_carrier_paid_amount": 0
        }
    )
    .withColumn(
        "total_claim_count",
        F.col("inpatient_claim_count") + F.col("outpatient_claim_count") + F.col("carrier_claim_count")
    )
    .withColumn(
        "total_paid_amount",
        F.col("total_inpatient_paid_amount")
        + F.col("total_outpatient_paid_amount")
        + F.col("total_carrier_paid_amount")
    )
)

write_gold_delta(gold_utilization_summary, GOLD_UTILIZATION_SUMMARY_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Create Gold Condition Summary
# MAGIC
# MAGIC This table summarizes diagnosis/condition activity per patient.
# MAGIC It supports chronic disease analysis and patient risk stratification.

# COMMAND ----------

gold_condition_summary = (
    conditions
    .groupBy(F.col("patient_id").alias("ehr_patient_id"))
    .agg(
        F.count("*").alias("condition_record_count"),
        F.countDistinct("condition_code").alias("distinct_condition_count"),
        F.collect_set("condition_description").alias("condition_description_list"),
        F.min("condition_start_date").alias("first_condition_date"),
        F.max("condition_start_date").alias("last_condition_date")
    )
)

gold_condition_summary = (
    gold_patient_crosswalk
    .join(gold_condition_summary, on="ehr_patient_id", how="left")
    .fillna(
        {
            "condition_record_count": 0,
            "distinct_condition_count": 0
        }
    )
)

write_gold_delta(gold_condition_summary, GOLD_CONDITION_SUMMARY_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Create Gold Medication Summary
# MAGIC
# MAGIC This table summarizes medication activity per patient.
# MAGIC It helps connect medication patterns to chronic conditions and utilization.

# COMMAND ----------

gold_medication_summary = (
    medications
    .groupBy(F.col("patient_id").alias("ehr_patient_id"))
    .agg(
        F.count("*").alias("medication_record_count"),
        F.countDistinct("medication_code").alias("distinct_medication_count"),
        F.collect_set("medication_description").alias("medication_description_list"),
        F.min("medication_start_date").alias("first_medication_date"),
        F.max("medication_start_date").alias("last_medication_date")
    )
)

gold_medication_summary = (
    gold_patient_crosswalk
    .join(gold_medication_summary, on="ehr_patient_id", how="left")
    .fillna(
        {
            "medication_record_count": 0,
            "distinct_medication_count": 0
        }
    )
)

write_gold_delta(gold_medication_summary, GOLD_MEDICATION_SUMMARY_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Create Gold Observation Summary
# MAGIC
# MAGIC This table summarizes clinical observation activity per patient.
# MAGIC Observation data can include measurements such as lab values, vitals, or screening results.

# COMMAND ----------

gold_observation_summary = (
    observations
    .groupBy(F.col("patient_id").alias("ehr_patient_id"))
    .agg(
        F.count("*").alias("observation_record_count"),
        F.countDistinct("observation_code").alias("distinct_observation_count"),
        F.collect_set("observation_description").alias("observation_description_list"),
        F.min("observation_date").alias("first_observation_date"),
        F.max("observation_date").alias("last_observation_date")
    )
)

gold_observation_summary = (
    gold_patient_crosswalk
    .join(gold_observation_summary, on="ehr_patient_id", how="left")
    .fillna(
        {
            "observation_record_count": 0,
            "distinct_observation_count": 0
        }
    )
)

write_gold_delta(gold_observation_summary, GOLD_OBSERVATION_SUMMARY_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Create Gold Patient Risk Features
# MAGIC
# MAGIC This table combines demographics, utilization, conditions, medications, and observations
# MAGIC into a single patient-level feature table.
# MAGIC
# MAGIC This is the main Gold table used by the PyTorch patient risk model.

# COMMAND ----------

prescription_summary = (
    prescription_events
    .groupBy(F.col("beneficiary_id").alias("claim_beneficiary_id"))
    .agg(
        F.count("*").alias("prescription_claim_count"),
        F.sum(F.coalesce(F.col("drug_cost_amount"), F.lit(0))).alias("total_prescription_drug_cost")
    )
)

gold_patient_risk_features = (
    gold_patient_master
    .join(
        gold_utilization_summary,
        on=["ehr_patient_id", "claim_beneficiary_id", "crosswalk_method"],
        how="left"
    )
    .join(
        gold_condition_summary.select(
            "ehr_patient_id",
            "condition_record_count",
            "distinct_condition_count"
        ),
        on="ehr_patient_id",
        how="left"
    )
    .join(
        gold_medication_summary.select(
            "ehr_patient_id",
            "medication_record_count",
            "distinct_medication_count"
        ),
        on="ehr_patient_id",
        how="left"
    )
    .join(
        gold_observation_summary.select(
            "ehr_patient_id",
            "observation_record_count",
            "distinct_observation_count"
        ),
        on="ehr_patient_id",
        how="left"
    )
    .join(
        prescription_summary,
        on="claim_beneficiary_id",
        how="left"
    )
    .fillna(
        {
            "ehr_encounter_count": 0,
            "distinct_ehr_encounter_count": 0,
            "inpatient_claim_count": 0,
            "outpatient_claim_count": 0,
            "carrier_claim_count": 0,
            "total_claim_count": 0,
            "total_inpatient_paid_amount": 0,
            "total_outpatient_paid_amount": 0,
            "total_carrier_paid_amount": 0,
            "total_paid_amount": 0,
            "condition_record_count": 0,
            "distinct_condition_count": 0,
            "medication_record_count": 0,
            "distinct_medication_count": 0,
            "observation_record_count": 0,
            "distinct_observation_count": 0,
            "prescription_claim_count": 0,
            "total_prescription_drug_cost": 0
        }
    )
    .withColumn(
        "total_medical_paid_amount",
        F.col("total_paid_amount") + F.col("total_prescription_drug_cost")
    )
    .withColumn(
        "has_inpatient_utilization",
        F.when(F.col("inpatient_claim_count") > 0, F.lit(1)).otherwise(F.lit(0))
    )
    .withColumn(
        "has_multiple_conditions",
        F.when(F.col("distinct_condition_count") >= 2, F.lit(1)).otherwise(F.lit(0))
    )
    .withColumn(
        "high_cost_patient_flag",
        F.when(
            F.col("total_medical_paid_amount")
            >= F.percentile_approx("total_medical_paid_amount", 0.75).over(Window.partitionBy()),
            F.lit(1)
        ).otherwise(F.lit(0))
    )
)

write_gold_delta(gold_patient_risk_features, GOLD_PATIENT_RISK_FEATURES_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Gold Validation Checks
# MAGIC
# MAGIC These checks validate that the Gold layer was created successfully.
# MAGIC In production, these checks could become Databricks workflow tasks, Delta Live Tables expectations,
# MAGIC dbt tests, or Great Expectations checks.

# COMMAND ----------

gold_tables = {
    "gold_patient_crosswalk": GOLD_CROSSWALK_PATH,
    "gold_patient_master": GOLD_PATIENT_MASTER_PATH,
    "gold_utilization_summary": GOLD_UTILIZATION_SUMMARY_PATH,
    "gold_condition_summary": GOLD_CONDITION_SUMMARY_PATH,
    "gold_medication_summary": GOLD_MEDICATION_SUMMARY_PATH,
    "gold_observation_summary": GOLD_OBSERVATION_SUMMARY_PATH,
    "gold_patient_risk_features": GOLD_PATIENT_RISK_FEATURES_PATH,
}

validation_results = []

for table_name, table_path in gold_tables.items():
    df = read_delta(table_path)
    row_count = df.count()
    column_count = len(df.columns)

    validation_results.append(
        {
            "table_name": table_name,
            "table_path": table_path,
            "row_count": row_count,
            "column_count": column_count,
            "status": "PASS" if row_count > 0 else "WARN_EMPTY_TABLE"
        }
    )

validation_df = spark.createDataFrame(validation_results)

display(validation_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12. Preview Final Patient Risk Features
# MAGIC
# MAGIC The patient risk feature table is the primary ML-ready Gold output.

# COMMAND ----------

display(gold_patient_risk_features)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold Delta Layer Complete
# MAGIC
# MAGIC This notebook creates the Databricks Gold Delta layer for the healthcare claims and EHR lakehouse.
# MAGIC
# MAGIC Gold outputs created:
# MAGIC
# MAGIC - `gold_patient_crosswalk`
# MAGIC - `gold_patient_master`
# MAGIC - `gold_utilization_summary`
# MAGIC - `gold_condition_summary`
# MAGIC - `gold_medication_summary`
# MAGIC - `gold_observation_summary`
# MAGIC - `gold_patient_risk_features`
# MAGIC
# MAGIC These tables represent the analytics-ready layer of the Databricks lakehouse and align with
# MAGIC the local pandas/Parquet Gold outputs used elsewhere in this portfolio project.