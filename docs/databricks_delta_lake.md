# Databricks Delta Lake Implementation

## Overview

This project includes Databricks notebook-style scripts that show how the local pandas/Parquet healthcare lakehouse can be migrated to a Databricks Delta Lake architecture.

The local version of this project uses:

- Python
- pandas
- Parquet files
- local validation scripts
- local Gold analytics outputs

The Databricks version maps that same medallion architecture into:

- Bronze Delta tables
- Silver Delta tables
- Gold Delta analytics marts
- Databricks Runtime
- PySpark transformations
- Delta Lake storage

This makes the project more representative of a production healthcare analytics platform.

## Why Databricks Delta Lake?

Databricks Delta Lake is used to demonstrate how a healthcare claims and EHR pipeline could scale beyond a local development workflow.

Delta Lake adds important production data engineering features, including:

- ACID transactions
- Schema enforcement
- Schema evolution
- Time travel
- Scalable PySpark transformations
- Reliable batch processing
- Integration with Databricks Workflows
- Compatibility with BI, analytics, and machine learning workloads

These features matter in healthcare analytics because clinical and claims data often require strong data quality, reproducibility, and auditability.

## Local Pipeline to Databricks Mapping

The local pipeline and Databricks pipeline follow the same logical architecture.

```text
Local pandas/Parquet pipeline

Raw CSV files
    |
    v
Bronze Parquet tables
    |
    v
Silver cleaned Parquet tables
    |
    v
Gold analytics Parquet tables
    |
    v
Streamlit / Tableau / PyTorch / Snowflake / dbt
```

```text
Databricks Delta Lake pipeline

Raw CSV files in cloud storage or DBFS
    |
    v
Bronze Delta tables
    |
    v
Silver Delta tables
    |
    v
Gold Delta marts
    |
    v
BI dashboards / Snowflake / dbt / PyTorch / ML workflows
```

The local implementation proves the data logic.  
The Databricks implementation shows how that logic would translate to a scalable lakehouse environment.

## Databricks Notebook-Style Scripts

The Databricks migration layer currently includes:

```text
notebooks/databricks/01_bronze_delta.py
notebooks/databricks/02_silver_delta.py
notebooks/databricks/03_gold_delta.py
```

These files are written as Databricks notebook-style Python scripts using `# COMMAND ----------` and `%md` cells.

They are intended to be imported or copied into Databricks notebooks.

## Important Local Development Note

These scripts are intended for Databricks Runtime.

When viewing the files locally in VS Code, warnings may appear for:

- `spark`
- `display`
- `pyspark`
- Databricks notebook magic commands

These warnings are expected.

They do not mean the project is incorrect. The files are portfolio migration artifacts designed to show how the local pipeline would be implemented in a Databricks environment.

Local Spark installation is not required unless the project is later expanded to test PySpark locally.

## Bronze Delta Layer

The Bronze Delta layer ingests raw synthetic healthcare files into Delta format.

Bronze tables preserve the raw structure of source data while making it available for scalable downstream processing.

Example Bronze inputs include:

- Synthea-style patients
- Synthea-style encounters
- Synthea-style conditions
- Synthea-style medications
- Synthea-style observations
- CMS SynPUF-style beneficiary records
- CMS SynPUF-style inpatient claims
- CMS SynPUF-style outpatient claims
- CMS SynPUF-style carrier claims
- CMS SynPUF-style prescription drug events

The Bronze layer is responsible for:

- Reading raw source files
- Standardizing table landing locations
- Writing data as Delta tables
- Preserving raw source-level detail
- Creating the foundation for Silver transformations

## Silver Delta Layer

The Silver Delta layer cleans and standardizes Bronze data.

Typical Silver responsibilities include:

- Renaming columns into consistent snake_case names
- Casting date fields
- Casting numeric claim amount fields
- Standardizing patient and beneficiary identifiers
- Removing duplicate records
- Preparing clean clinical and claims tables for Gold aggregation

Silver tables are still relatively close to the source data, but they are cleaner, more reliable, and easier to join.

## Gold Delta Layer

The Gold Delta layer creates analytics-ready patient-level tables.

Gold outputs include:

```text
gold_patient_crosswalk
gold_patient_master
gold_utilization_summary
gold_condition_summary
gold_medication_summary
gold_observation_summary
gold_patient_risk_features
```

These tables support downstream use cases such as:

- Patient risk analysis
- Chronic condition analysis
- Inpatient and outpatient utilization reporting
- Medication and observation summaries
- Tableau and Streamlit dashboards
- Snowflake warehouse loading
- PyTorch model training
- dbt marts and tests

## Gold Patient Crosswalk

The Gold patient crosswalk links EHR patient identifiers to claims beneficiary identifiers.

Current identifier columns include:

```text
ehr_patient_id
claim_beneficiary_id
crosswalk_method
```

In this portfolio project, the linkage is synthetic because the sample data is fictional.

In a real healthcare environment, this would likely be handled through:

- Enterprise master patient index logic
- Deterministic patient matching
- Probabilistic matching
- Privacy-preserving record linkage
- Vendor-provided patient identity resolution

## Gold Patient Master

The Gold patient master table creates a patient-level demographic dimension.

It combines EHR patient fields and claims beneficiary fields into a single analytics-ready table.

Example fields include:

- Patient identifier
- Claims beneficiary identifier
- Age
- Gender
- Race
- Ethnicity
- Geography
- Death flags
- Crosswalk method

This table acts as the central patient dimension for the rest of the Gold layer.

## Gold Utilization Summary

The Gold utilization summary aggregates patient healthcare usage.

It includes metrics such as:

- EHR encounter count
- Inpatient claim count
- Outpatient claim count
- Carrier claim count
- Total claim count
- Total inpatient paid amount
- Total outpatient paid amount
- Total carrier paid amount
- Total paid amount

This table supports utilization analysis and helps identify patients with higher healthcare usage.

## Gold Condition Summary

The Gold condition summary aggregates diagnosis and condition history at the patient level.

It includes metrics such as:

- Condition record count
- Distinct condition count
- First condition date
- Last condition date
- Condition description list

This table supports chronic condition analysis and risk stratification.

## Gold Medication Summary

The Gold medication summary aggregates medication history at the patient level.

It includes metrics such as:

- Medication record count
- Distinct medication count
- First medication date
- Last medication date
- Medication description list

This table helps connect medication activity to patient complexity and utilization patterns.

## Gold Observation Summary

The Gold observation summary aggregates clinical observations at the patient level.

It includes metrics such as:

- Observation record count
- Distinct observation count
- First observation date
- Last observation date
- Observation description list

Observation data can support future feature engineering for lab results, vitals, screening data, and other clinical indicators.

## Gold Patient Risk Features

The Gold patient risk features table combines demographics, utilization, conditions, medications, observations, and prescription activity into one machine-learning-ready table.

It supports the PyTorch patient risk modeling workflow.

Example feature groups include:

- Demographic features
- Encounter count features
- Claims utilization features
- Paid amount features
- Condition count features
- Medication count features
- Observation count features
- Prescription drug cost features
- High-cost patient flag

The current synthetic sample dataset is intentionally small, so model metrics are workflow-validation metrics rather than production-grade predictive performance.

The value of this layer is that it demonstrates the full pattern from raw healthcare data to ML-ready patient features.

## Delta Lake Benefits

### ACID Transactions

Delta Lake supports ACID transactions, which help ensure that table writes are reliable and consistent.

This matters in healthcare analytics because incomplete or corrupted writes could affect reporting, patient risk analysis, and downstream business decisions.

### Schema Enforcement

Delta Lake can enforce table schemas during writes.

This helps prevent unexpected source data changes from silently breaking downstream analytics.

For healthcare data, schema enforcement is useful because clinical and claims fields often need strict typing, especially for dates, diagnosis codes, claim amounts, and patient identifiers.

### Schema Evolution

Delta Lake can support controlled schema evolution.

This is useful when new healthcare fields are added over time, such as new claim attributes, clinical observations, or risk model features.

### Time Travel

Delta Lake time travel allows users to query earlier versions of a table.

This is useful for:

- Auditing changes
- Reproducing prior reports
- Debugging pipeline issues
- Comparing model training datasets over time
- Supporting healthcare compliance and governance workflows

### Scalable Transformations

Databricks uses Spark to process large datasets across a cluster.

This matters because real healthcare claims and EHR data can contain millions or billions of records across patients, encounters, claims, medications, procedures, and observations.

The local pandas version is suitable for portfolio development and logic validation.

The Databricks version shows how the same pipeline could scale.

## Databricks Workflows Orchestration

In a production Databricks environment, these notebook-style scripts could be orchestrated with Databricks Workflows.

A workflow could run the notebooks in this order:

```text
01_bronze_delta.py
    |
    v
02_silver_delta.py
    |
    v
03_gold_delta.py
    |
    v
Snowflake load / BI refresh / ML training
```

A production workflow could also include:

- Data quality checks
- Failure alerts
- Job retries
- Scheduled refreshes
- Parameterized environments
- Separate development, staging, and production jobs

## Healthcare Analytics Business Value

This Databricks Delta Lake implementation demonstrates how healthcare organizations can combine EHR and claims data into a unified analytics platform.

Potential business use cases include:

- Identifying high-risk or high-cost patients
- Monitoring inpatient and outpatient utilization
- Understanding chronic condition patterns
- Supporting care management prioritization
- Creating patient-level risk features for machine learning
- Feeding dashboards for operational and executive reporting
- Loading curated Gold data into Snowflake for broader analytics access

## Relationship to Snowflake, dbt, BI, and PyTorch

The Databricks layer is one part of the broader project architecture.

### Snowflake

Gold outputs can be loaded into Snowflake for warehouse-based analytics, SQL analysis, and enterprise reporting.

### dbt

dbt models can transform and test warehouse tables after Gold data lands in Snowflake or a local DuckDB development environment.

### Tableau and Streamlit

Gold tables can feed BI dashboards that show utilization trends, patient risk indicators, and condition patterns.

### PyTorch

The Gold patient risk features table can feed PyTorch training and evaluation scripts.

This demonstrates a full path from raw healthcare data to predictive modeling.

## Portfolio Relevance

This Databricks Delta Lake layer strengthens the project by showing experience with:

- Lakehouse architecture
- Medallion data modeling
- PySpark transformations
- Delta Lake table design
- Healthcare claims and EHR concepts
- Analytics engineering patterns
- ML-ready feature engineering
- Scalable cloud data platform design

Together with the local pipeline, Snowflake workflow, dbt models, Streamlit dashboard, Tableau exports, and PyTorch model, this gives the project an end-to-end recruiter-facing story.

## Summary

The Databricks Delta Lake implementation shows how the local healthcare claims and EHR pipeline can be migrated into a scalable production-style lakehouse.

The project now includes:

- Raw synthetic EHR and claims data
- Bronze ingestion
- Silver cleaning
- Gold analytics marts
- Databricks Delta migration scripts
- Snowflake loading and validation
- dbt transformation and tests
- Tableau-ready exports
- Streamlit dashboard
- PyTorch-ready ML dataset
- Baseline PyTorch model

This completes the Databricks migration artifact milestone and prepares the project for final portfolio polish.