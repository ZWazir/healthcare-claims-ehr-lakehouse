# Healthcare Claims & EHR Lakehouse with Databricks, Snowflake, dbt & PyTorch

## Overview

This project is an end-to-end healthcare data lakehouse portfolio project that combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data.

The goal is to demonstrate a modern analytics engineering and machine learning workflow across the full data lifecycle:

- Raw healthcare data ingestion
- Bronze, Silver, and Gold medallion architecture
- Data validation and profiling
- BI-ready exports
- Streamlit dashboarding
- Tableau-ready CSV extracts
- PyTorch-ready feature engineering
- Baseline PyTorch patient risk modeling
- dbt staging, intermediate, and mart models
- Snowflake loading and validation
- Databricks Delta Lake migration artifacts

The project is designed to be recruiter-facing and demonstrates practical skills in healthcare analytics, data engineering, analytics engineering, business intelligence, and machine learning.

## Business Problem

Healthcare organizations often need to combine clinical EHR data with claims data to understand patient risk, utilization, chronic conditions, and cost drivers.

This project answers questions such as:

- Which patients are most likely to become high-cost patients?
- Which chronic conditions are associated with higher utilization?
- How does inpatient, outpatient, and carrier claim activity vary by patient?
- Which patients may benefit from care management intervention?
- How can curated healthcare data be prepared for BI dashboards and machine learning?

## Data Sources

This project uses synthetic data only.

### Synthetic EHR / FHIR-Style Data

The EHR side of the project is modeled after Synthea-style patient records.

Example entities include:

- Patients
- Encounters
- Conditions
- Medications
- Observations

### Synthetic CMS Medicare Claims-Style Data

The claims side of the project is modeled after CMS Medicare DE-SynPUF-style data.

Example entities include:

- Beneficiary summaries
- Inpatient claims
- Outpatient claims
- Carrier claims
- Prescription drug events

Because the data is synthetic, this project does not contain real patient information or protected health information.

## Architecture

```text
Synthetic EHR/FHIR Data              Synthetic CMS Claims Data
        |                                      |
        v                                      v
Raw CSV / Source Files              Raw CSV / Source Files
        |                                      |
        +-------------------+------------------+
                            |
                            v
                    Bronze Layer
              Raw standardized Parquet tables
                            |
                            v
                    Silver Layer
          Cleaned, typed, analytics-ready tables
                            |
                            v
                     Gold Layer
        Patient master, utilization, condition,
       medication, observation, and risk features
                            |
        +-------------------+-------------------+-------------------+
        |                   |                   |                   |
        v                   v                   v                   v
 Tableau-ready CSVs   Streamlit Dashboard   PyTorch ML Dataset   Snowflake
                                                                    |
                                                                    v
                                                                  dbt
                            |
                            v
                Databricks Delta Lake Migration
          Bronze Delta -> Silver Delta -> Gold Delta
```

## Tech Stack

### Data Engineering

- Python
- pandas
- Parquet
- PySpark
- Databricks
- Delta Lake
- Snowflake

### Analytics Engineering

- dbt
- DuckDB
- SQL
- Data tests
- Staging, intermediate, and mart models

### Machine Learning

- PyTorch
- Tensor datasets
- Baseline neural network model
- Model evaluation reporting

### BI and Reporting

- Streamlit
- Tableau-ready CSV exports
- Gold profile reports
- JSON metadata reports

### Development Workflow

- VS Code
- Git
- GitHub
- Bash
- Python virtual environment

## Project Structure

```text
healthcare_claims_ehr_lakehouse/
|
|-- data/
|   |-- raw/
|   |   |-- synthea/
|   |   |-- synpuf/
|   |-- bronze/
|   |-- silver/
|   |-- gold/
|   |-- tableau_exports/
|   |-- ml/
|   |-- dbt/                      # ignored by Git
|
|-- dbt/
|   |-- healthcare_claims/
|       |-- dbt_project.yml
|       |-- models/
|           |-- staging/
|           |-- intermediate/
|           |-- marts/
|
|-- docs/
|   |-- data_acquisition.md
|   |-- raw_data_manifest.md
|   |-- bronze_layer.md
|   |-- silver_layer.md
|   |-- gold_layer.md
|   |-- local_pipeline_runner.md
|   |-- tableau_exports.md
|   |-- ml_feature_engineering.md
|   |-- pytorch_model.md
|   |-- databricks_delta_lake.md
|
|-- notebooks/
|   |-- databricks/
|       |-- 01_bronze_delta.py
|       |-- 02_silver_delta.py
|       |-- 03_gold_delta.py
|
|-- reports/
|   |-- gold/
|   |-- tableau_exports/
|   |-- ml/
|   |-- snowflake/
|
|-- scripts/
|   |-- generate_data/
|   |-- inspect/
|   |-- bronze/
|   |-- silver/
|   |-- gold/
|   |-- exports/
|   |-- ml/
|   |-- snowflake/
|   |-- run_local_pipeline.py
|
|-- streamlit_app/
|   |-- app.py
|
|-- README.md
|-- requirements.txt
|-- .gitignore
```

## Medallion Architecture

### Bronze Layer

The Bronze layer ingests raw synthetic EHR and claims files into standardized Parquet tables.

Bronze responsibilities include:

- Loading raw source data
- Preserving source-level detail
- Standardizing file outputs
- Creating the foundation for downstream validation and cleaning

Key scripts:

```text
scripts/bronze/build_bronze_tables.py
scripts/bronze/validate_bronze_tables.py
```

### Silver Layer

The Silver layer cleans and standardizes Bronze data.

Silver responsibilities include:

- Renaming fields
- Casting dates and numeric values
- Standardizing identifiers
- Removing duplicates
- Preparing clean tables for Gold aggregation

Key scripts:

```text
scripts/silver/build_silver_tables.py
scripts/silver/validate_silver_tables.py
```

### Gold Layer

The Gold layer creates patient-level analytics tables.

Gold outputs include:

```text
gold_patient_crosswalk.parquet
gold_patient_master.parquet
gold_condition_summary.parquet
gold_utilization_summary.parquet
gold_medication_summary.parquet
gold_observation_summary.parquet
gold_patient_risk_features.parquet
```

Gold responsibilities include:

- Linking EHR patients to claims beneficiaries
- Creating patient demographic features
- Summarizing utilization
- Summarizing conditions
- Summarizing medications
- Summarizing observations
- Creating ML-ready patient risk features

Key scripts:

```text
scripts/gold/build_gold_tables.py
scripts/gold/validate_gold_tables.py
scripts/gold/profile_gold_tables.py
```

## Patient Identifier Strategy

The project uses a synthetic patient crosswalk to link EHR-style patients and claims-style beneficiaries.

Core identifier columns used across Gold, Tableau exports, ML source data, dbt, and Snowflake:

```text
ehr_patient_id
claim_beneficiary_id
crosswalk_method
```

In a real healthcare environment, patient matching would typically require an enterprise master patient index, deterministic matching, probabilistic matching, or privacy-preserving record linkage.

For this portfolio project, the synthetic crosswalk demonstrates the architectural pattern without using real patient data.

## Tableau-Ready Exports

The project creates CSV extracts designed for Tableau Public or Tableau Desktop.

Current Tableau export outputs:

```text
data/tableau_exports/patient_master_export.csv
data/tableau_exports/utilization_summary_export.csv
data/tableau_exports/condition_summary_export.csv
data/tableau_exports/patient_risk_features_export.csv
reports/tableau_exports/tableau_export_manifest.json
```

Key script:

```text
scripts/exports/create_tableau_exports.py
```

Documentation:

```text
docs/tableau_exports.md
```

These exports allow the curated Gold layer to be consumed by BI tools without requiring a database connection.

## Streamlit Dashboard

The project includes a Streamlit dashboard MVP for interactive exploration of the Gold layer.

Key file:

```text
streamlit_app/app.py
```

The dashboard is designed to highlight:

- Patient-level metrics
- Utilization summaries
- Condition summaries
- Risk feature outputs

Run command:

```bash
streamlit run streamlit_app/app.py
```

## PyTorch Machine Learning Layer

The project includes a PyTorch-ready machine learning workflow.

The ML layer creates patient-level tensors from Gold patient risk features and trains a baseline model for high-cost patient risk classification.

Current ML outputs:

```text
data/ml/patient_risk_features.csv
data/ml/train_features.pt
data/ml/train_labels.pt
data/ml/test_features.pt
data/ml/test_labels.pt
reports/ml/ml_dataset_metadata.json
reports/ml/training_report.json
reports/ml/model_evaluation_report.json
```

Key scripts:

```text
scripts/ml/create_ml_dataset.py
scripts/ml/train_patient_risk_model.py
scripts/ml/evaluate_patient_risk_model.py
```

Documentation:

```text
docs/ml_feature_engineering.md
docs/pytorch_model.md
```

### Important Modeling Note

The current synthetic sample dataset is intentionally small.

The PyTorch model metrics are mainly workflow-validation metrics, not production-grade predictive performance.

The purpose of this layer is to demonstrate the full machine learning pipeline pattern:

```text
Gold patient features
        |
        v
ML-ready CSV
        |
        v
PyTorch tensors
        |
        v
Baseline model training
        |
        v
Evaluation report
```

## dbt Analytics Engineering Layer

The project includes a dbt implementation using DuckDB for local analytics engineering development.

The dbt project includes:

- Staging models
- Intermediate models
- Mart models
- Schema tests

dbt project path:

```text
dbt/healthcare_claims/
```

Key dbt files:

```text
dbt/healthcare_claims/dbt_project.yml

dbt/healthcare_claims/models/staging/stg_gold_patient_master.sql
dbt/healthcare_claims/models/staging/stg_gold_utilization_summary.sql
dbt/healthcare_claims/models/staging/stg_gold_condition_summary.sql
dbt/healthcare_claims/models/staging/stg_gold_patient_risk_features.sql
dbt/healthcare_claims/models/staging/schema.yml

dbt/healthcare_claims/models/intermediate/int_patient_utilization.sql
dbt/healthcare_claims/models/intermediate/int_patient_conditions.sql
dbt/healthcare_claims/models/intermediate/schema.yml

dbt/healthcare_claims/models/marts/mart_patient_risk_features.sql
dbt/healthcare_claims/models/marts/schema.yml
```

Run commands:

```bash
cd dbt/healthcare_claims
dbt run
dbt test
```

The dbt layer demonstrates analytics engineering best practices by transforming Gold data into tested, documented analytical models.

## Snowflake Warehouse Layer

The project includes a Snowflake loading and validation workflow for the Gold layer.

Current Snowflake outputs:

```text
scripts/snowflake/create_snowflake_objects.sql
scripts/snowflake/load_gold_to_snowflake.py
scripts/snowflake/validate_snowflake_tables.py
reports/snowflake/snowflake_load_report.json
reports/snowflake/snowflake_validation_report.json
```

Snowflake workflow:

```text
Create Snowflake objects
        |
        v
Load Gold Parquet tables
        |
        v
Validate Snowflake table counts and structure
```

Key scripts:

```text
scripts/snowflake/load_gold_to_snowflake.py
scripts/snowflake/validate_snowflake_tables.py
```

### Snowflake Boolean Handling Note

Some local Parquet flag columns are stored as `0` and `1`.

Snowflake table flag columns were set to `NUMBER(1,0)` instead of `BOOLEAN` to avoid Parquet casting issues.

For this portfolio project:

```text
1 = true
0 = false
```

This design choice is documented because it reflects a realistic data engineering decision when loading typed Parquet files into a warehouse.

## Databricks Delta Lake Layer

The project includes Databricks notebook-style scripts that show how the local pandas/Parquet pipeline maps to a scalable Databricks Delta Lake architecture.

Databricks files:

```text
notebooks/databricks/01_bronze_delta.py
notebooks/databricks/02_silver_delta.py
notebooks/databricks/03_gold_delta.py
```

Documentation:

```text
docs/databricks_delta_lake.md
```

The Databricks layer demonstrates:

- Bronze Delta ingestion
- Silver Delta cleaning
- Gold Delta marts
- PySpark transformations
- Delta Lake table writes
- Gold validation checks
- Migration from local Parquet to cloud lakehouse architecture

### Important Databricks Note

These files are intended for Databricks Runtime.

Local VS Code warnings about the following are expected:

```text
spark
display
pyspark
Databricks notebook magic commands
```

These warnings do not mean the project is incorrect.

The files are portfolio migration artifacts that show how the pipeline would be implemented in a Databricks environment.

## Reports and Metadata

The project generates reports that document pipeline outputs and validation results.

Current report outputs include:

```text
reports/gold/gold_profile_report.md
reports/gold/gold_profile_report.json

reports/tableau_exports/tableau_export_manifest.json

reports/ml/ml_dataset_metadata.json
reports/ml/training_report.json
reports/ml/model_evaluation_report.json

reports/snowflake/snowflake_load_report.json
reports/snowflake/snowflake_validation_report.json
```

These reports make the project easier to review because they show what was created, validated, and modeled.

## How to Run This Project Locally

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the local pipeline

```bash
python scripts/run_local_pipeline.py
```

This runs the main local pipeline stages and creates Bronze, Silver, Gold, validation, and report outputs.

### 4. Create Tableau exports

```bash
python scripts/exports/create_tableau_exports.py
```

### 5. Create the ML dataset

```bash
python scripts/ml/create_ml_dataset.py
```

### 6. Train the PyTorch model

```bash
python scripts/ml/train_patient_risk_model.py
```

### 7. Evaluate the PyTorch model

```bash
python scripts/ml/evaluate_patient_risk_model.py
```

### 8. Launch the Streamlit dashboard

```bash
streamlit run streamlit_app/app.py
```

## How to Run dbt

From the dbt project directory:

```bash
cd dbt/healthcare_claims
dbt run
dbt test
```

## How to Run Snowflake Workflow

The Snowflake layer requires valid Snowflake credentials and environment configuration.

Create Snowflake objects using:

```text
scripts/snowflake/create_snowflake_objects.sql
```

Then run:

```bash
python scripts/snowflake/load_gold_to_snowflake.py
python scripts/snowflake/validate_snowflake_tables.py
```

## How to Use Databricks Artifacts

The Databricks files are notebook-style Python scripts intended for Databricks Runtime.

Recommended Databricks order:

```text
01_bronze_delta.py
        |
        v
02_silver_delta.py
        |
        v
03_gold_delta.py
```

These files can be imported into Databricks notebooks or copied into a Databricks workspace.

They are not required for the local pipeline to run.

## Business Value

This project demonstrates how a healthcare organization could build a unified analytics platform across clinical and claims data.

Potential business value includes:

- Improved visibility into patient utilization
- Identification of high-cost or high-risk patients
- Better chronic condition monitoring
- Care management prioritization
- BI-ready executive reporting
- ML-ready patient feature generation
- Scalable migration path from local development to Databricks and Snowflake

## Skills Demonstrated

### Data Engineering

- Medallion architecture
- Raw to Bronze ingestion
- Bronze to Silver cleaning
- Silver to Gold aggregation
- Parquet data modeling
- Validation scripts
- Pipeline orchestration
- Snowflake loading
- Databricks Delta Lake migration

### Analytics Engineering

- dbt project structure
- Staging models
- Intermediate models
- Mart models
- Schema tests
- SQL transformations
- Patient-level analytical modeling

### Machine Learning Engineering

- Feature engineering
- Train/test split creation
- PyTorch tensor generation
- Baseline neural network model training
- Model evaluation reporting
- ML workflow documentation

### Business Intelligence

- Streamlit dashboard development
- Tableau-ready extracts
- KPI design
- Patient utilization analysis
- Risk feature reporting

### Healthcare Analytics

- EHR-style data modeling
- Claims-style data modeling
- Patient crosswalk design
- Utilization summaries
- Chronic condition summaries
- High-cost patient risk features

## Current Status

The project currently includes:

- Synthetic raw healthcare data
- Bronze, Silver, and Gold local Parquet pipeline
- Bronze, Silver, and Gold validation
- Gold profiling reports
- One-command local pipeline runner
- Streamlit dashboard MVP
- Tableau-ready CSV exports
- PyTorch-ready ML dataset
- Baseline PyTorch model training and evaluation
- dbt staging, intermediate, and mart models
- dbt tests
- Snowflake object creation, loading, and validation workflow
- Databricks Bronze, Silver, and Gold Delta notebook-style scripts
- Databricks Delta Lake documentation

## Future Improvements

Potential future enhancements include:

- Use larger synthetic datasets
- Add more realistic patient matching logic
- Add more clinical features from observations and medications
- Add diagnosis grouping such as CCS or HCC-style categories
- Add model comparison across logistic regression, tree-based models, and neural networks
- Add SHAP or feature importance explainability
- Add automated orchestration with Prefect, Airflow, or Databricks Workflows
- Add CI checks for Python scripts and dbt models
- Deploy the Streamlit dashboard
- Publish Tableau Public dashboard screenshots
- Expand Snowflake/dbt documentation with lineage screenshots
- Add a formal architecture diagram image

## Recruiter Summary

This project demonstrates an end-to-end healthcare analytics lakehouse using Python, pandas, Parquet, Databricks, Delta Lake, Snowflake, dbt, PyTorch, Streamlit, and Tableau-ready exports.

It shows the ability to design a full data platform from raw synthetic clinical and claims data through curated analytics marts, BI outputs, warehouse loading, analytics engineering models, and machine learning-ready patient risk features.