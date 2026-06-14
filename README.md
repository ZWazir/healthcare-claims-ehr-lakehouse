# Healthcare Claims & EHR Lakehouse with Databricks, Snowflake, dbt & PyTorch

## Overview

This project is an end-to-end healthcare data lakehouse portfolio project that combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data.

The goal is to demonstrate a modern healthcare analytics engineering and machine learning workflow across the full data lifecycle:

* Synthetic raw healthcare data generation
* Bronze, Silver, and Gold medallion architecture
* Data validation and profiling
* Patient 360 analytics mart
* BI-ready Tableau CSV exports
* Streamlit dashboarding
* Tableau Public dashboard publishing
* PyTorch-ready feature engineering
* Baseline PyTorch patient risk modeling
* dbt staging, intermediate, and mart models
* Snowflake loading and validation
* Databricks Delta Lake migration artifacts
* Prefect local orchestration

The project is designed to be recruiter-facing and demonstrates practical skills in healthcare analytics, data engineering, analytics engineering, business intelligence, cloud warehouse loading, orchestration, and machine learning.

## Live Tableau Public Dashboard

A recruiter-facing Tableau Public dashboard has been published for the Patient 360 Gold mart.

**Healthcare Patient 360 Analytics Dashboard**
Synthetic EHR + Claims Lakehouse | Patient Risk, Utilization, and Care Management View

**Live Dashboard:**
https://public.tableau.com/app/profile/zafar.wazir/viz/HealthcareClaimsEHRLakehouseReport/Dashboard1?publish=yes

The dashboard summarizes synthetic linked EHR and claims data transformed through the lakehouse pipeline into patient-level care management insights. It includes:

* Patient population KPI cards
* Care management priority segmentation
* Cost, utilization, and age-band distributions
* Cost proxy vs. utilization scatter plot
* Interactive filters
* Patient 360 detail table

The Patient 360 dashboard intentionally uses the synthetic linked EHR + claims pipeline because those records are designed to be linkable at the patient level. Real-world public datasets from MIMIC-IV Demo and CMS Claims PUF are included separately for ingestion, profiling, and validation, but are not joined into Patient 360 because they are not naturally linkable.

## Business Problem

Healthcare organizations often need to combine clinical EHR data with claims data to understand patient risk, utilization, chronic conditions, and cost drivers.

This project answers questions such as:

* Which patients are most likely to become high-cost patients?
* Which chronic conditions are associated with higher utilization?
* How does inpatient, outpatient, and carrier claim activity vary by patient?
* Which patients may benefit from care management intervention?
* How can curated healthcare data be prepared for BI dashboards and machine learning?
* How can a local healthcare analytics pipeline be migrated toward Databricks, Snowflake, and dbt?

## Data Sources

This project uses two complementary data tracks:

1. A fully reproducible synthetic linked EHR + claims pipeline
2. A real-world/public ingestion extension for separate EHR-style and claims-style public datasets

### Synthetic EHR / FHIR-Style Data

The EHR side of the main pipeline is modeled after Synthea-style patient records.

Example entities include:

* Patients
* Encounters
* Conditions
* Medications
* Observations

### Synthetic CMS Medicare Claims-Style Data

The claims side of the main pipeline is modeled after CMS Medicare DE-SynPUF-style data.

Example entities include:

* Beneficiary summaries
* Inpatient claims
* Outpatient claims
* Carrier-style reimbursement fields
* Chronic condition flags

Because the main pipeline data is synthetic, this project does not contain real patient information or protected health information.

### Real-World/Public Extension Data

The project also includes separate ingestion, profiling, and validation workflows for:

* MIMIC-IV Clinical Database Demo
* CMS Basic Stand Alone Medicare Claims Public Use Files

These public datasets are not joined into Patient 360 because they are not naturally linkable.

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
       medication, observation, risk features,
                 and Patient 360 mart
                            |
        +-------------------+-------------------+-------------------+-------------------+
        |                   |                   |                   |                   |
        v                   v                   v                   v                   v
 Tableau Public       Streamlit Dashboard   PyTorch ML Dataset   Snowflake          dbt
 Dashboard + CSVs
                            |
                            v
                Databricks Delta Lake Migration
          Bronze Delta -> Silver Delta -> Gold Delta
                            |
                            v
                   Prefect Local Orchestration
```

## Real-World Public Data Ingestion Extension

Version 1.1 adds a real-world/public healthcare data ingestion extension to the original synthetic linked EHR + claims lakehouse.

The synthetic pipeline remains the main fully reproducible end-to-end demo because it uses patient-level EHR and claims records that can be linked safely inside the project. The real-world extension adds separate public data ingestion workflows for real deidentified clinical data and public Medicare claims data.

### Public Data Sources Added

#### MIMIC-IV Clinical Database Demo

The project includes an ingestion workflow for the MIMIC-IV Clinical Database Demo, a real deidentified EHR demo dataset published through PhysioNet.

This workflow ingests selected compressed CSV files from the MIMIC demo into local Parquet Bronze tables under the real-world data extension.

Selected MIMIC demo tables include:

* patients
* admissions
* diagnoses_icd
* procedures_icd
* d_icd_diagnoses
* d_icd_procedures
* labevents
* prescriptions
* icustays

#### CMS Basic Stand Alone Medicare Claims Public Use Files

The project also includes an ingestion workflow for the CMS Basic Stand Alone Medicare Claims Public Use Files.

The first CMS ingestion milestone focuses on the 2008 Inpatient Claims PUF. This public claims file is ingested into a separate real-world Bronze claims table and profiled independently from the MIMIC demo EHR data.

### Important Design Decision

The MIMIC-IV demo and CMS Medicare Claims PUF data are not linked in this project.

These datasets come from different sources, different populations, and different deidentification processes. The project does not attempt to join MIMIC patients to CMS claims records.

Instead, the project demonstrates two complementary patterns:

1. A fully reproducible synthetic linked EHR + claims lakehouse
2. Separate real-world/public ingestion tracks for EHR-style and claims-style healthcare data

This keeps the analytics design responsible while still demonstrating the ability to ingest and profile realistic public healthcare datasets.

### Real-World Extension Folder Structure

```text
data/real_world/
├── raw/
│   ├── mimic_demo/
│   └── cms_claims_puf/
├── bronze/
│   ├── mimic_demo/
│   └── cms_claims_puf/

reports/real_world/
scripts/real_world/
```

The downloaded raw files and generated Bronze Parquet outputs are intentionally excluded from Git. The repository tracks the ingestion scripts, profile scripts, validation scripts, and generated reports.

### Real-World Ingestion Scripts

```text
scripts/real_world/ingest_mimic_demo.py
scripts/real_world/profile_mimic_demo.py
scripts/real_world/ingest_cms_claims_puf.py
scripts/real_world/profile_cms_claims_puf.py
scripts/real_world/validate_real_world_bronze.py
```

### Real-World Reports

```text
reports/real_world/mimic_demo_ingestion_report.json
reports/real_world/mimic_demo_profile_report.json
reports/real_world/mimic_demo_profile_report.md
reports/real_world/cms_claims_puf_ingestion_report.json
reports/real_world/cms_claims_puf_profile_report.json
reports/real_world/cms_claims_puf_profile_report.md
reports/real_world/real_world_bronze_validation_report.json
reports/real_world/real_world_bronze_validation_report.md
```

### Portfolio Value

This extension strengthens the project by showing that the lakehouse design can support both synthetic linked healthcare data and real public healthcare data.

The synthetic pipeline demonstrates the complete end-to-end architecture from raw data through Bronze, Silver, Gold, Patient 360, BI exports, Streamlit, Tableau Public, dbt models, Snowflake loading, Prefect orchestration, and PyTorch modeling.

The real-world extension demonstrates practical public-data ingestion, profiling, validation, and documentation using realistic healthcare schemas.

## Tech Stack

### Data Engineering

* Python
* pandas
* Parquet
* PySpark
* Databricks
* Delta Lake
* Snowflake
* Prefect

### Analytics Engineering

* dbt
* DuckDB
* SQL
* Data tests
* Staging, intermediate, and mart models

### Machine Learning

* PyTorch
* Tensor datasets
* Baseline neural network model
* Model evaluation reporting

### BI and Reporting

* Tableau Public
* Tableau-ready CSV exports
* Streamlit
* Gold profile reports
* JSON metadata reports
* Markdown validation reports

### Development Workflow

* VS Code
* Git
* GitHub
* Bash
* Python virtual environment

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
|   |-- real_world/
|   |   |-- raw/
|   |   |-- bronze/
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
|   |-- tableau_public_dashboard_plan.md
|   |-- patient_360.md
|   |-- prefect_orchestration.md
|   |-- ml_feature_engineering.md
|   |-- pytorch_model.md
|   |-- databricks_delta_lake.md
|   |-- portfolio_talking_points.md
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
|   |-- real_world/
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
|   |-- real_world/
|   |-- orchestration/
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

* Loading raw source data
* Preserving source-level detail
* Standardizing file outputs
* Creating the foundation for downstream validation and cleaning

Key scripts:

```text
scripts/bronze/build_bronze_tables.py
scripts/bronze/validate_bronze_tables.py
```

### Silver Layer

The Silver layer cleans and standardizes Bronze data.

Silver responsibilities include:

* Renaming fields
* Casting dates and numeric values
* Standardizing identifiers
* Removing duplicates
* Preparing clean tables for Gold aggregation

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
gold_patient_360.parquet
```

Gold responsibilities include:

* Linking EHR patients to claims beneficiaries
* Creating patient demographic features
* Summarizing utilization
* Summarizing conditions
* Summarizing medications
* Summarizing observations
* Creating ML-ready patient risk features
* Creating Patient 360 dashboard-ready analytics

Key scripts:

```text
scripts/gold/build_gold_tables.py
scripts/gold/validate_gold_tables.py
scripts/gold/profile_gold_tables.py
scripts/gold/build_patient_360.py
scripts/gold/profile_patient_360.py
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

## Patient 360 Analytics Mart

This project includes a Patient 360 Gold mart that combines the most useful synthetic linked EHR and claims data into a single patient-level analytics table.

The Patient 360 mart is designed for executive dashboarding, care-management review, Tableau exports, and Streamlit-based portfolio storytelling. It combines patient demographics, utilization metrics, condition burden, ML-ready risk features, reimbursement/cost proxies, and dashboard-friendly business segments.

Key Patient 360 outputs include:

```text
data/gold/gold_patient_360.parquet
data/tableau_exports/patient_360_export.csv
reports/gold/patient_360_build_report.json
reports/gold/patient_360_profile_report.json
reports/gold/patient_360_profile_report.md
```

Patient 360 includes business-facing fields such as:

```text
patient_360_total_utilization_events
patient_360_total_cost_proxy
patient_360_condition_burden
utilization_segment
cost_segment
care_management_priority
age_band
```

The Patient 360 table uses the synthetic linked Gold pipeline. The real-world public MIMIC-IV Demo and CMS Claims PUF datasets are intentionally kept as separate ingestion and validation tracks because they are not naturally linkable.

## Tableau-Ready Exports

The project creates CSV extracts designed for Tableau Public or Tableau Desktop.

Current Tableau export outputs:

```text
data/tableau_exports/patient_360_export.csv
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
docs/tableau_public_dashboard_plan.md
```

These exports allow the curated Gold layer to be consumed by BI tools without requiring a database connection.

## Streamlit Dashboard

The project includes a Streamlit dashboard MVP for interactive exploration of the Gold layer, Patient 360 mart, and real-world public data extension reports.

Key file:

```text
streamlit_app/app.py
```

The dashboard is designed to highlight:

* Synthetic linked EHR + claims pipeline metrics
* Patient-level Gold outputs
* Patient 360 executive view
* Care management priority segmentation
* Cost and utilization segments
* Real-world public data ingestion summaries
* MIMIC-IV Demo and CMS Claims PUF profile reports
* Real-world Bronze validation report

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

The PyTorch model metrics are workflow-validation metrics, not production-grade predictive performance.

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

* Staging models
* Intermediate models
* Mart models
* Schema tests

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

* Bronze Delta ingestion
* Silver Delta cleaning
* Gold Delta marts
* PySpark transformations
* Delta Lake table writes
* Gold validation checks
* Migration from local Parquet to cloud lakehouse architecture

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

## Prefect Orchestration Layer

The project includes a local Prefect flow that orchestrates the main synthetic linked healthcare lakehouse workflow.

Key file:

```text
scripts/orchestration/run_prefect_pipeline.py
```

The Prefect flow runs:

```text
Generate synthetic raw data
        |
        v
Build Bronze layer
        |
        v
Validate Bronze layer
        |
        v
Build Silver layer
        |
        v
Validate Silver layer
        |
        v
Build Gold layer
        |
        v
Validate Gold layer
        |
        v
Build Patient 360 Gold mart
        |
        v
Profile Patient 360 Gold mart
        |
        v
Create Tableau-ready exports
```

Run command:

```bash
python scripts/orchestration/run_prefect_pipeline.py
```

This gives the project a one-command local orchestration path from synthetic raw data generation through Patient 360 and Tableau-ready outputs.

## Reports and Metadata

The project generates reports that document pipeline outputs and validation results.

Current report outputs include:

```text
reports/gold/gold_profile_report.md
reports/gold/gold_profile_report.json
reports/gold/patient_360_build_report.json
reports/gold/patient_360_profile_report.json
reports/gold/patient_360_profile_report.md

reports/tableau_exports/tableau_export_manifest.json

reports/ml/ml_dataset_metadata.json
reports/ml/training_report.json
reports/ml/model_evaluation_report.json

reports/snowflake/snowflake_load_report.json
reports/snowflake/snowflake_validation_report.json

reports/real_world/mimic_demo_ingestion_report.json
reports/real_world/mimic_demo_profile_report.json
reports/real_world/mimic_demo_profile_report.md
reports/real_world/cms_claims_puf_ingestion_report.json
reports/real_world/cms_claims_puf_profile_report.json
reports/real_world/cms_claims_puf_profile_report.md
reports/real_world/real_world_bronze_validation_report.json
reports/real_world/real_world_bronze_validation_report.md
```

These reports make the project easier to review because they show what was created, validated, profiled, exported, and modeled.

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

### 3. Run the full Prefect orchestration flow

```bash
python scripts/orchestration/run_prefect_pipeline.py
```

This runs the main synthetic linked workflow from raw data generation through Bronze, Silver, Gold, Patient 360, profiling, and Tableau-ready exports.

### 4. Run the local medallion pipeline only

```bash
python scripts/run_local_pipeline.py
```

This runs the local synthetic raw data generation, Bronze, Silver, Gold, and validation stages.

### 5. Rebuild Patient 360 manually if needed

```bash
python scripts/gold/build_patient_360.py
python scripts/gold/profile_patient_360.py
```

### 6. Create Tableau exports manually if needed

```bash
python scripts/exports/create_tableau_exports.py
```

### 7. Create the ML dataset

```bash
python scripts/ml/create_ml_dataset.py
```

### 8. Train the PyTorch model

```bash
python scripts/ml/train_patient_risk_model.py
```

### 9. Evaluate the PyTorch model

```bash
python scripts/ml/evaluate_patient_risk_model.py
```

### 10. Launch the Streamlit dashboard

```bash
streamlit run streamlit_app/app.py
```

## How to Run the Real-World Public Data Extension

The real-world extension requires local copies of the MIMIC-IV Demo files and CMS Claims PUF files in the expected `data/real_world/raw/` folders.

Run the MIMIC-IV Demo ingestion and profiling workflow:

```bash
python scripts/real_world/ingest_mimic_demo.py
python scripts/real_world/profile_mimic_demo.py
```

Run the CMS Claims PUF ingestion and profiling workflow:

```bash
python scripts/real_world/ingest_cms_claims_puf.py
python scripts/real_world/profile_cms_claims_puf.py
```

Validate the real-world Bronze outputs:

```bash
python scripts/real_world/validate_real_world_bronze.py
```

The real-world extension is intentionally separate from Patient 360 because the public MIMIC and CMS Claims PUF datasets are not naturally linkable.

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

This project demonstrates how a healthcare organization could build a unified analytics platform across clinical and claims-style data.

Potential business value includes:

* Improved visibility into patient utilization
* Identification of high-cost or high-risk patients
* Better chronic condition monitoring
* Care management prioritization
* BI-ready executive reporting
* ML-ready patient feature generation
* Real-world public data ingestion and validation
* Scalable migration path from local development to Databricks and Snowflake

## Skills Demonstrated

### Data Engineering

* Medallion architecture
* Raw to Bronze ingestion
* Bronze to Silver cleaning
* Silver to Gold aggregation
* Parquet data modeling
* Validation scripts
* Pipeline orchestration with Prefect
* Snowflake loading
* Databricks Delta Lake migration

### Analytics Engineering

* dbt project structure
* Staging models
* Intermediate models
* Mart models
* Schema tests
* SQL transformations
* Patient-level analytical modeling

### Machine Learning Engineering

* Feature engineering
* Train/test split creation
* PyTorch tensor generation
* Baseline neural network model training
* Model evaluation reporting
* ML workflow documentation

### Business Intelligence

* Tableau Public dashboard publishing
* Tableau-ready extracts
* Streamlit dashboard development
* KPI design
* Patient utilization analysis
* Risk feature reporting
* Patient 360 dashboard design

### Healthcare Analytics

* EHR-style data modeling
* Claims-style data modeling
* Patient crosswalk design
* Utilization summaries
* Chronic condition summaries
* High-cost patient risk features
* Care management segmentation
* Public healthcare data ingestion

## Current Status

The project currently includes:

* Synthetic raw healthcare data generation
* Bronze, Silver, and Gold local Parquet pipeline
* Bronze, Silver, and Gold validation
* Gold profiling reports
* One-command local pipeline runner
* Prefect local orchestration flow
* Patient 360 Gold mart
* Patient 360 profiling report
* Streamlit dashboard MVP with Patient 360 and real-world public data tabs
* Tableau-ready CSV exports
* Published Tableau Public dashboard
* PyTorch-ready ML dataset
* Baseline PyTorch model training and evaluation
* dbt staging, intermediate, and mart models
* dbt tests
* Snowflake object creation, loading, and validation workflow
* Databricks Bronze, Silver, and Gold Delta notebook-style scripts
* Databricks Delta Lake documentation
* Real-world public data ingestion extension for MIMIC-IV Demo and CMS Claims PUF
* Real-world public data profiling and validation reports
* Portfolio talking points documentation

## Future Improvements

Potential future enhancements include:

* Add a formal architecture diagram image
* Add Tableau dashboard screenshots to the README
* Add more realistic patient matching logic
* Add diagnosis grouping such as CCS, HCC-style categories, or service-line groupings
* Add more clinical features from observations and medications
* Add model comparison across logistic regression, tree-based models, and neural networks
* Add SHAP or feature importance explainability
* Add CI checks for Python scripts and dbt models
* Deploy the Streamlit dashboard
* Expand Snowflake/dbt documentation with lineage screenshots
* Add Databricks Workflow or Asset Bundle deployment examples
* Add a larger-scale synthetic dataset option for performance testing

## Recruiter Summary

This project demonstrates an end-to-end healthcare analytics lakehouse using Python, pandas, Parquet, Databricks, Delta Lake, Snowflake, dbt, PyTorch, Streamlit, Tableau Public, and Prefect.

It shows the ability to design a full data platform from raw synthetic clinical and claims data through curated analytics marts, Patient 360 reporting, BI outputs, warehouse loading, analytics engineering models, orchestration, and machine learning-ready patient risk features.

The project also includes separate public-data ingestion extensions for MIMIC-IV Demo and CMS Claims PUF, demonstrating responsible handling of real-world healthcare datasets without forcing inappropriate patient-level linkage.
