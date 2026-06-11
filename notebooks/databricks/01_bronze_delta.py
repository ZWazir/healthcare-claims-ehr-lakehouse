# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Bronze Delta Layer
# MAGIC
# MAGIC This notebook demonstrates how the local Bronze ingestion layer from the
# MAGIC Healthcare Claims & EHR Lakehouse project could be implemented in Databricks
# MAGIC using Spark and Delta Lake.
# MAGIC
# MAGIC The Bronze layer stores source-aligned raw data in Delta tables with minimal
# MAGIC transformation. Its purpose is to preserve the original source structure while
# MAGIC making the data queryable, versioned, and reliable inside the lakehouse.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import StringType


# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration
# MAGIC
# MAGIC In a production Databricks workspace, these paths would point to cloud object
# MAGIC storage such as ADLS, S3, or GCS.
# MAGIC
# MAGIC Example:
# MAGIC - `abfss://raw@storageaccount.dfs.core.windows.net/healthcare/`
# MAGIC - `s3://my-healthcare-lakehouse/raw/`
# MAGIC
# MAGIC For portfolio documentation, these paths show the intended structure.

# COMMAND ----------

RAW_BASE_PATH = "/mnt/healthcare_lakehouse/raw"
BRONZE_BASE_PATH = "/mnt/healthcare_lakehouse/bronze"

CATALOG_NAME = "healthcare_lakehouse"
BRONZE_SCHEMA = "bronze"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Bronze Schema
# MAGIC
# MAGIC The Bronze schema stores raw source-aligned Delta tables.

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG_NAME}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG_NAME}.{BRONZE_SCHEMA}")

spark.sql(f"USE CATALOG {CATALOG_NAME}")
spark.sql(f"USE SCHEMA {BRONZE_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Helper Function
# MAGIC
# MAGIC This function reads a raw CSV file and writes it as a managed Delta table.
# MAGIC
# MAGIC Bronze transformations are intentionally light:
# MAGIC - Read raw source file
# MAGIC - Standardize column names
# MAGIC - Add ingestion metadata
# MAGIC - Save as Delta

# COMMAND ----------

def standardize_column_names(df):
    """
    Converts source column names to lowercase snake_case style.

    This keeps the Bronze layer easy to query while preserving the original
    source-level meaning of the columns.
    """
    renamed_df = df

    for column_name in df.columns:
        clean_name = (
            column_name.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "_")
            .replace("/", "_")
        )

        renamed_df = renamed_df.withColumnRenamed(column_name, clean_name)

    return renamed_df


def ingest_csv_to_bronze(source_path, table_name, source_system):
    """
    Reads a raw CSV file and writes it to a Bronze Delta table.
    """
    raw_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(source_path)
    )

    bronze_df = (
        standardize_column_names(raw_df)
        .withColumn("source_system", F.lit(source_system))
        .withColumn("ingested_at_utc", F.current_timestamp())
        .withColumn("source_file_path", F.input_file_name())
    )

    target_table = f"{CATALOG_NAME}.{BRONZE_SCHEMA}.{table_name}"

    (
        bronze_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(target_table)
    )

    print(f"Created Bronze Delta table: {target_table}")
    print(f"Rows loaded: {bronze_df.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest Synthea EHR/FHIR-Style Files
# MAGIC
# MAGIC These files represent synthetic EHR data, including patients, encounters,
# MAGIC conditions, medications, and observations.

# COMMAND ----------

synthea_tables = [
    {
        "source_path": f"{RAW_BASE_PATH}/synthea/patients.csv",
        "table_name": "synthea_patients",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synthea/encounters.csv",
        "table_name": "synthea_encounters",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synthea/conditions.csv",
        "table_name": "synthea_conditions",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synthea/medications.csv",
        "table_name": "synthea_medications",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synthea/observations.csv",
        "table_name": "synthea_observations",
    },
]

for table_config in synthea_tables:
    ingest_csv_to_bronze(
        source_path=table_config["source_path"],
        table_name=table_config["table_name"],
        source_system="synthea",
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest CMS SynPUF-Style Claims Files
# MAGIC
# MAGIC These files represent synthetic Medicare-style claims data, including
# MAGIC beneficiary summaries, inpatient claims, outpatient claims, carrier claims,
# MAGIC and prescription drug events.

# COMMAND ----------

synpuf_tables = [
    {
        "source_path": f"{RAW_BASE_PATH}/synpuf/beneficiary_summary.csv",
        "table_name": "synpuf_beneficiary_summary",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synpuf/inpatient_claims.csv",
        "table_name": "synpuf_inpatient_claims",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synpuf/outpatient_claims.csv",
        "table_name": "synpuf_outpatient_claims",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synpuf/carrier_claims.csv",
        "table_name": "synpuf_carrier_claims",
    },
    {
        "source_path": f"{RAW_BASE_PATH}/synpuf/prescription_drug_events.csv",
        "table_name": "synpuf_prescription_drug_events",
    },
]

for table_config in synpuf_tables:
    ingest_csv_to_bronze(
        source_path=table_config["source_path"],
        table_name=table_config["table_name"],
        source_system="cms_synpuf",
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bronze Validation Queries
# MAGIC
# MAGIC These queries validate that the Bronze Delta tables were created and populated.

# COMMAND ----------

bronze_tables = [
    "synthea_patients",
    "synthea_encounters",
    "synthea_conditions",
    "synthea_medications",
    "synthea_observations",
    "synpuf_beneficiary_summary",
    "synpuf_inpatient_claims",
    "synpuf_outpatient_claims",
    "synpuf_carrier_claims",
    "synpuf_prescription_drug_events",
]

validation_results = []

for table_name in bronze_tables:
    full_table_name = f"{CATALOG_NAME}.{BRONZE_SCHEMA}.{table_name}"

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
# MAGIC This Bronze Delta notebook demonstrates how the local pandas/Parquet ingestion
# MAGIC pattern translates to Databricks:
# MAGIC
# MAGIC - Raw CSV files are loaded from cloud storage.
# MAGIC - Source-aligned tables are written as Delta tables.
# MAGIC - Ingestion metadata is added for lineage.
# MAGIC - Tables are organized into a Bronze schema.
# MAGIC - Validation confirms row counts after ingestion.
# MAGIC
# MAGIC Compared with local Parquet files, Delta Lake adds ACID transactions, schema
# MAGIC enforcement, scalable Spark processing, and time travel.