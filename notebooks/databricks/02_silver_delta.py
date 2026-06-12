# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Silver Delta Layer
# MAGIC
# MAGIC This notebook demonstrates how the local Silver cleaning layer from the
# MAGIC Healthcare Claims & EHR Lakehouse project could be implemented in Databricks
# MAGIC using Spark and Delta Lake.
# MAGIC
# MAGIC The Silver layer standardizes raw Bronze tables into cleaned, typed, and
# MAGIC analytics-ready entities. It prepares EHR and claims data for downstream
# MAGIC Gold patient-level marts.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window


# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration
# MAGIC
# MAGIC These catalog and schema names mirror a Databricks lakehouse implementation
# MAGIC of the local medallion architecture.

# COMMAND ----------

CATALOG_NAME = "healthcare_lakehouse"

BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG_NAME}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG_NAME}.{SILVER_SCHEMA}")

spark.sql(f"USE CATALOG {CATALOG_NAME}")
spark.sql(f"USE SCHEMA {SILVER_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Helper Functions
# MAGIC
# MAGIC These helpers keep the Silver transformations consistent across tables.

# COMMAND ----------

def read_bronze_table(table_name):
    """
    Reads a Bronze Delta table from the Databricks catalog.
    """
    return spark.table(f"{CATALOG_NAME}.{BRONZE_SCHEMA}.{table_name}")


def write_silver_table(df, table_name):
    """
    Writes a DataFrame as a Silver Delta table.
    """
    target_table = f"{CATALOG_NAME}.{SILVER_SCHEMA}.{table_name}"

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )

    print(f"Created Silver Delta table: {target_table}")
    print(f"Rows written: {df.count()}")


def clean_string_column(column_name):
    """
    Trims blank strings and converts empty values to null.
    """
    return F.when(
        F.trim(F.col(column_name)) == "",
        F.lit(None)
    ).otherwise(F.trim(F.col(column_name)))


# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Patients
# MAGIC
# MAGIC Standardizes the synthetic EHR patient table into a clean patient dimension.
# MAGIC
# MAGIC In the local pipeline, this maps to the patient cleaning logic that feeds
# MAGIC the Gold patient master table.

# COMMAND ----------

bronze_patients = read_bronze_table("synthea_patients")

silver_patients = (
    bronze_patients
    .select(
        F.col("id").alias("ehr_patient_id"),
        clean_string_column("first").alias("first_name"),
        clean_string_column("last").alias("last_name"),
        clean_string_column("gender").alias("gender"),
        clean_string_column("race").alias("race"),
        clean_string_column("ethnicity").alias("ethnicity"),
        clean_string_column("city").alias("city"),
        clean_string_column("state").alias("state"),
        clean_string_column("county").alias("county"),
        clean_string_column("zip").alias("zip_code"),
        F.to_date(F.col("birthdate")).alias("birth_date"),
        F.to_date(F.col("deathdate")).alias("death_date"),
        F.col("source_system"),
        F.col("ingested_at_utc")
    )
    .withColumn(
        "is_deceased_ehr",
        F.col("death_date").isNotNull()
    )
    .withColumn(
        "age",
        F.floor(F.months_between(F.current_date(), F.col("birth_date")) / 12)
    )
    .dropDuplicates(["ehr_patient_id"])
)

write_silver_table(silver_patients, "silver_patients")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Encounters
# MAGIC
# MAGIC Standardizes EHR encounter records into patient-level clinical utilization
# MAGIC events.

# COMMAND ----------

bronze_encounters = read_bronze_table("synthea_encounters")

silver_encounters = (
    bronze_encounters
    .select(
        F.col("id").alias("encounter_id"),
        F.col("patient").alias("ehr_patient_id"),
        F.to_timestamp(F.col("start")).alias("encounter_start_at"),
        F.to_timestamp(F.col("stop")).alias("encounter_end_at"),
        clean_string_column("encounterclass").alias("encounter_class"),
        clean_string_column("code").alias("encounter_code"),
        clean_string_column("description").alias("encounter_description"),
        F.col("source_system"),
        F.col("ingested_at_utc")
    )
    .dropDuplicates(["encounter_id"])
)

write_silver_table(silver_encounters, "silver_encounters")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Conditions
# MAGIC
# MAGIC Standardizes diagnosis and condition records for patient-level chronic
# MAGIC condition analytics.

# COMMAND ----------

bronze_conditions = read_bronze_table("synthea_conditions")

silver_conditions = (
    bronze_conditions
    .select(
        F.col("patient").alias("ehr_patient_id"),
        F.col("encounter").alias("encounter_id"),
        F.to_date(F.col("start")).alias("condition_start_date"),
        F.to_date(F.col("stop")).alias("condition_stop_date"),
        clean_string_column("code").alias("condition_code"),
        clean_string_column("description").alias("condition_description"),
        F.col("source_system"),
        F.col("ingested_at_utc")
    )
    .dropDuplicates([
        "ehr_patient_id",
        "encounter_id",
        "condition_code",
        "condition_start_date"
    ])
)

write_silver_table(silver_conditions, "silver_conditions")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Medications
# MAGIC
# MAGIC Standardizes medication records for downstream medication-count features.

# COMMAND ----------

bronze_medications = read_bronze_table("synthea_medications")

silver_medications = (
    bronze_medications
    .select(
        F.col("patient").alias("ehr_patient_id"),
        F.col("encounter").alias("encounter_id"),
        F.to_date(F.col("start")).alias("medication_start_date"),
        F.to_date(F.col("stop")).alias("medication_stop_date"),
        clean_string_column("code").alias("medication_code"),
        clean_string_column("description").alias("medication_description"),
        F.col("source_system"),
        F.col("ingested_at_utc")
    )
    .dropDuplicates([
        "ehr_patient_id",
        "encounter_id",
        "medication_code",
        "medication_start_date"
    ])
)

write_silver_table(silver_medications, "silver_medications")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Observations
# MAGIC
# MAGIC Standardizes clinical observation records such as BMI, blood pressure,
# MAGIC and glucose values.

# COMMAND ----------

bronze_observations = read_bronze_table("synthea_observations")

silver_observations = (
    bronze_observations
    .select(
        F.col("patient").alias("ehr_patient_id"),
        F.col("encounter").alias("encounter_id"),
        F.to_timestamp(F.col("date")).alias("observation_at"),
        clean_string_column("code").alias("observation_code"),
        clean_string_column("description").alias("observation_description"),
        F.col("value").cast("double").alias("observation_value"),
        clean_string_column("units").alias("observation_units"),
        F.col("source_system"),
        F.col("ingested_at_utc")
    )
    .dropDuplicates([
        "ehr_patient_id",
        "encounter_id",
        "observation_code",
        "observation_at"
    ])
)

write_silver_table(silver_observations, "silver_observations")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Beneficiaries
# MAGIC
# MAGIC Standardizes synthetic Medicare beneficiary records. This table provides
# MAGIC the claims-side patient identifier and demographic fields.

# COMMAND ----------

bronze_beneficiaries = read_bronze_table("synpuf_beneficiary_summary")

silver_beneficiaries = (
    bronze_beneficiaries
    .select(
        F.col("desynpuf_id").alias("claim_beneficiary_id"),
        F.to_date(F.col("bene_birth_dt").cast("string"), "yyyyMMdd").alias("claim_birth_date"),
        F.to_date(F.col("bene_death_dt").cast("string"), "yyyyMMdd").alias("claim_death_date"),
        clean_string_column("bene_sex_ident_cd").alias("sex_code"),
        clean_string_column("bene_race_cd").alias("race_code"),
        clean_string_column("sp_state_code").alias("state_code"),
        clean_string_column("bene_county_cd").alias("county_code"),
        F.col("source_system"),
        F.col("ingested_at_utc")
    )
    .withColumn(
        "is_deceased_claims",
        F.col("claim_death_date").isNotNull()
    )
    .dropDuplicates(["claim_beneficiary_id"])
)

write_silver_table(silver_beneficiaries, "silver_beneficiaries")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Claims
# MAGIC
# MAGIC Combines inpatient, outpatient, and carrier claim files into one standardized
# MAGIC claims fact table.
# MAGIC
# MAGIC This mirrors the local project pattern of creating a clean claims foundation
# MAGIC before building Gold utilization metrics.

# COMMAND ----------

def standardize_claims_table(df, claim_type):
    """
    Converts a raw SynPUF-style claims table into a common claims schema.
    """
    return (
        df
        .select(
            F.col("desynpuf_id").alias("claim_beneficiary_id"),
            F.col("clm_id").alias("claim_id"),
            F.to_date(F.col("clm_from_dt").cast("string"), "yyyyMMdd").alias("claim_start_date"),
            F.to_date(F.col("clm_thru_dt").cast("string"), "yyyyMMdd").alias("claim_end_date"),
            F.col("clm_pmt_amt").cast("double").alias("paid_amount"),
            F.col("nch_prmry_pyr_clm_pd_amt").cast("double").alias("primary_payer_paid_amount"),
            F.col("source_system"),
            F.col("ingested_at_utc")
        )
        .withColumn("claim_type", F.lit(claim_type))
    )


inpatient_claims = standardize_claims_table(
    read_bronze_table("synpuf_inpatient_claims"),
    "inpatient"
)

outpatient_claims = standardize_claims_table(
    read_bronze_table("synpuf_outpatient_claims"),
    "outpatient"
)

carrier_claims = standardize_claims_table(
    read_bronze_table("synpuf_carrier_claims"),
    "carrier"
)

silver_claims = (
    inpatient_claims
    .unionByName(outpatient_claims, allowMissingColumns=True)
    .unionByName(carrier_claims, allowMissingColumns=True)
    .dropDuplicates(["claim_id"])
)

write_silver_table(silver_claims, "silver_claims")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Patient Crosswalk
# MAGIC
# MAGIC Creates a simple patient crosswalk between EHR patient IDs and claims
# MAGIC beneficiary IDs.
# MAGIC
# MAGIC In a production environment, this would use deterministic or probabilistic
# MAGIC matching logic. For this portfolio project, it demonstrates where identity
# MAGIC resolution would happen in the Databricks lakehouse.

# COMMAND ----------

patient_window = Window.orderBy("ehr_patient_id")
beneficiary_window = Window.orderBy("claim_beneficiary_id")

patient_ranked = (
    spark.table(f"{CATALOG_NAME}.{SILVER_SCHEMA}.silver_patients")
    .select("ehr_patient_id")
    .withColumn("crosswalk_row_number", F.row_number().over(patient_window))
)

beneficiary_ranked = (
    spark.table(f"{CATALOG_NAME}.{SILVER_SCHEMA}.silver_beneficiaries")
    .select("claim_beneficiary_id")
    .withColumn("crosswalk_row_number", F.row_number().over(beneficiary_window))
)

silver_patient_crosswalk = (
    patient_ranked
    .join(beneficiary_ranked, on="crosswalk_row_number", how="inner")
    .drop("crosswalk_row_number")
    .withColumn("crosswalk_method", F.lit("synthetic_rank_match"))
)

write_silver_table(silver_patient_crosswalk, "silver_patient_crosswalk")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Validation
# MAGIC
# MAGIC These validation checks confirm that the main Silver Delta tables exist and
# MAGIC contain records.

# COMMAND ----------

silver_tables = [
    "silver_patients",
    "silver_encounters",
    "silver_conditions",
    "silver_medications",
    "silver_observations",
    "silver_beneficiaries",
    "silver_claims",
    "silver_patient_crosswalk",
]

validation_results = []

for table_name in silver_tables:
    full_table_name = f"{CATALOG_NAME}.{SILVER_SCHEMA}.{table_name}"
    row_count = spark.table(full_table_name).count()

    validation_results.append(
        {
            "table_name": full_table_name,
            "row_count": row_count,
        }
    )

display(validation_results)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Portfolio Notes
# MAGIC
# MAGIC This Silver Delta notebook demonstrates how the local pandas-based cleaning
# MAGIC logic would translate to Databricks:
# MAGIC
# MAGIC - Bronze Delta tables are read from the lakehouse catalog.
# MAGIC - EHR and claims records are cleaned and standardized.
# MAGIC - Dates and numeric fields are typed for analytics.
# MAGIC - A patient crosswalk connects EHR and claims identities.
# MAGIC - Silver tables are written back as Delta tables.
# MAGIC
# MAGIC Compared with local Parquet processing, Databricks adds distributed Spark
# MAGIC processing, managed table metadata, schema enforcement, ACID transactions,
# MAGIC and easier orchestration through Databricks Workflows.