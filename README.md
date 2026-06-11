# Healthcare Claims & EHR Lakehouse with Databricks, Snowflake, dbt & PyTorch

## Overview

This project builds an end-to-end healthcare analytics lakehouse that combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data.

The project currently includes a working local medallion pipeline built with Python, pandas, and Parquet. The local pipeline generates sample raw healthcare data, inspects source files, builds Bronze, Silver, and Gold layers, validates each layer, and profiles the final Gold analytics outputs.

The long-term goal is to extend this local lakehouse into a cloud-oriented healthcare data platform using Databricks Delta Lake, Snowflake, dbt, PyTorch, Streamlit, and Tableau.

---

## Business Problem

Healthcare organizations need to combine clinical EHR data and claims data to better understand patient risk, utilization, cost, and care patterns.

This project models that problem by building a pipeline that can answer questions such as:

* Which patients have the highest utilization?
* Which patients may be at higher risk based on conditions, encounters, medications, and observations?
* How can raw clinical and claims data be transformed into analytics-ready patient-level features?
* How can healthcare data engineering outputs support dashboards and predictive modeling?

---

## Current Project Status

Current completion estimate: **65%**

Completed:

* Project folder structure
* Synthetic raw healthcare data generation
* Raw data inspection
* Raw schema summary creation
* Bronze ingestion layer
* Bronze validation layer
* Silver cleaning layer
* Silver validation layer
* Gold analytics layer
* Gold validation layer
* One-command local pipeline runner
* Gold layer profiling report

Remaining major components:

* Streamlit dashboard
* Tableau-ready exports
* PyTorch feature engineering dataset
* Baseline PyTorch patient risk model
* dbt transformation layer
* Snowflake integration
* Databricks Delta Lake implementation plan or notebooks
* Final portfolio polish

---

## Tech Stack

### Current Local Implementation

* Python
* pandas
* Parquet
* pathlib
* JSON
* Markdown
* Git/GitHub

### Planned / Portfolio Extension Stack

* Databricks
* Delta Lake
* Snowflake
* dbt
* PyTorch
* Streamlit
* Tableau

---

## Data Sources

### Synthetic EHR/FHIR-Style Data

The EHR portion of the project is based on synthetic Synthea-style healthcare data.

Example domains include:

* Patients
* Encounters
* Conditions
* Medications
* Observations

### Synthetic Medicare Claims-Style Data

The claims portion of the project is based on synthetic CMS Medicare SynPUF-style data.

Example domains include:

* Beneficiary summaries
* Inpatient claims
* Outpatient claims
* Carrier claims
* Prescription drug events

The current local version uses generated sample data to simulate these structures.

---

## Architecture

### Current Local Architecture

```text
Synthetic Raw Data
        |
        v
Raw CSV Files
        |
        v
Bronze Parquet Tables
        |
        v
Bronze Validation
        |
        v
Silver Cleaned Parquet Tables
        |
        v
Silver Validation
        |
        v
Gold Analytics Parquet Tables
        |
        v
Gold Validation
        |
        v
Gold Profile Report
```

### Planned Cloud Lakehouse Architecture

```text
Synthea EHR/FHIR Data       CMS SynPUF Claims Data
            |                         |
            v                         v
        Databricks Bronze Delta Tables
                      |
                      v
        Databricks Silver Cleaned Tables
                      |
                      v
        Databricks Gold Patient Analytics Tables
                      |
                      v
              Snowflake Warehouse
                      |
                      v
                  dbt Marts
                      |
                      v
        PyTorch Patient Risk Prediction Model
                      |
                      v
          Streamlit / Tableau Dashboard
```

---

## Medallion Architecture

This project follows a Bronze / Silver / Gold medallion architecture.

### Raw Layer

The raw layer contains synthetic source files that represent EHR and claims data.

Purpose:

* Preserve source-like data
* Simulate external healthcare data ingestion
* Provide input files for Bronze ingestion

### Bronze Layer

The Bronze layer stores raw data in a standardized Parquet format.

Purpose:

* Convert raw CSV files into Parquet
* Preserve source-level detail
* Create a consistent local lakehouse storage format

### Silver Layer

The Silver layer contains cleaned and standardized healthcare data.

Purpose:

* Standardize column names
* Clean patient, encounter, condition, medication, observation, and claims data
* Prepare reliable intermediate tables for analytics modeling

### Gold Layer

The Gold layer contains analytics-ready patient and healthcare summary tables.

Purpose:

* Create patient-level analytical outputs
* Support business intelligence dashboards
* Support patient risk feature engineering
* Prepare data for downstream machine learning

---

## Current Gold Outputs

The current Gold layer produces the following Parquet tables:

| Gold Table                           | Purpose                                                     |
| ------------------------------------ | ----------------------------------------------------------- |
| `gold_patient_crosswalk.parquet`     | Links patient identifiers across EHR and claims-style data  |
| `gold_patient_master.parquet`        | Creates a consolidated patient-level master table           |
| `gold_condition_summary.parquet`     | Summarizes patient condition history                        |
| `gold_utilization_summary.parquet`   | Summarizes patient encounter and utilization patterns       |
| `gold_medication_summary.parquet`    | Summarizes medication history by patient                    |
| `gold_observation_summary.parquet`   | Summarizes observation and measurement data                 |
| `gold_patient_risk_features.parquet` | Creates patient-level features for downstream risk modeling |

---

## Project Structure

```text
.
├── data/
│   ├── raw/
│   │   ├── synthea/
│   │   └── synpuf/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── data_acquisition.md
│   ├── raw_data_manifest.md
│   ├── bronze_layer.md
│   ├── silver_layer.md
│   ├── gold_layer.md
│   └── local_pipeline_runner.md
│
├── reports/
│   └── gold/
│       ├── gold_profile_report.md
│       └── gold_profile_report.json
│
├── scripts/
│   ├── generate_data/
│   │   └── create_sample_raw_data.py
│   ├── inspect/
│   │   ├── inspect_raw_files.py
│   │   └── create_schema_summary.py
│   ├── bronze/
│   │   ├── ingest_raw_to_bronze.py
│   │   └── validate_bronze_tables.py
│   ├── silver/
│   │   ├── build_silver_tables.py
│   │   └── validate_silver_tables.py
│   ├── gold/
│   │   ├── build_gold_tables.py
│   │   ├── validate_gold_tables.py
│   │   └── profile_gold_tables.py
│   └── run_local_pipeline.py
│
├── dbt/
│   └── healthcare_claims/
│
├── streamlit_app/
│
└── README.md
```

---

## How to Run the Local Pipeline

From the project root, run:

```bash
python scripts/run_local_pipeline.py
```

The local pipeline runner executes the project in this order:

1. Generate sample raw data
2. Inspect raw files
3. Create raw schema summary
4. Build Bronze tables
5. Validate Bronze tables
6. Build Silver tables
7. Validate Silver tables
8. Build Gold tables
9. Validate Gold tables

This provides a repeatable local workflow that simulates how the project could later be orchestrated with Databricks Workflows, Airflow, Prefect, or Dagster.

---

## How to Profile the Gold Layer

After the Gold tables are built, run:

```bash
python scripts/gold/profile_gold_tables.py
```

This creates:

```text
reports/gold/gold_profile_report.md
reports/gold/gold_profile_report.json
```

The Gold profile report includes:

* Row counts
* Column counts
* Column names
* Null counts
* Null percentages
* Duplicate checks
* Sample records

This provides evidence that the Gold analytics tables were inspected and are ready for downstream BI and ML use cases.

---

## Key Scripts

| Script                                            | Purpose                                        |
| ------------------------------------------------- | ---------------------------------------------- |
| `scripts/generate_data/create_sample_raw_data.py` | Generates sample synthetic healthcare raw data |
| `scripts/inspect/inspect_raw_files.py`            | Inspects raw source files                      |
| `scripts/inspect/create_schema_summary.py`        | Creates a schema summary of raw files          |
| `scripts/bronze/ingest_raw_to_bronze.py`          | Converts raw files into Bronze Parquet tables  |
| `scripts/bronze/validate_bronze_tables.py`        | Validates Bronze table existence and structure |
| `scripts/silver/build_silver_tables.py`           | Builds cleaned Silver tables                   |
| `scripts/silver/validate_silver_tables.py`        | Validates Silver table outputs                 |
| `scripts/gold/build_gold_tables.py`               | Builds Gold analytics tables                   |
| `scripts/gold/validate_gold_tables.py`            | Validates Gold table outputs                   |
| `scripts/gold/profile_gold_tables.py`             | Profiles Gold analytics outputs                |
| `scripts/run_local_pipeline.py`                   | Runs the local medallion pipeline end-to-end   |

---

## Analytics Use Cases

The Gold layer is designed to support healthcare analytics questions such as:

* Which patients have the highest utilization?
* Which patients have multiple chronic conditions?
* Which patient groups show higher medication or observation activity?
* Which patients may be higher risk based on combined clinical and claims-style features?
* What patient-level features can be used for predictive modeling?

---

## Machine Learning Use Case

The project is designed to support a future PyTorch model that predicts patient risk or utilization.

Potential model target variables:

* High-risk patient flag
* High-utilization patient flag
* High-cost patient flag

Potential feature groups:

* Demographics
* Encounter counts
* Condition counts
* Medication counts
* Observation counts
* Claims-style utilization indicators
* Patient-level risk features

The current Gold table `gold_patient_risk_features.parquet` is intended to become the foundation for this ML workflow.

---

## Portfolio Value

This project demonstrates:

* Healthcare data modeling
* Claims and EHR data integration concepts
* Medallion architecture design
* Local lakehouse development with Parquet
* Data pipeline orchestration
* Data validation
* Data profiling
* Analytics-ready Gold table design
* Feature engineering preparation
* BI and ML pipeline planning
* Git-based project organization

---

## Planned Next Steps

### 1. Streamlit Dashboard

Build a Streamlit dashboard from the Gold layer.

Planned features:

* Patient count overview
* Utilization summary
* Condition summary
* Medication summary
* Observation summary
* Patient risk feature exploration

### 2. Tableau-Ready Exports

Create clean CSV exports for Tableau Public.

Planned outputs:

* Patient master export
* Utilization summary export
* Condition summary export
* Patient risk features export

### 3. PyTorch Feature Engineering

Create an ML-ready dataset from the Gold patient risk features table.

Planned outputs:

* Train/test split
* Numeric features
* Target variable
* Saved PyTorch tensors or CSV files

### 4. Baseline PyTorch Model

Train a simple neural network to predict patient risk or utilization.

Planned outputs:

* Model training script
* Evaluation script
* Saved model artifact
* Metrics report

### 5. dbt Layer

Mirror key transformations in dbt.

Planned components:

* Sources
* Staging models
* Intermediate models
* Mart models
* dbt tests
* dbt documentation

### 6. Snowflake Integration

Load Gold analytics tables into Snowflake.

Planned components:

* Snowflake database/schema setup
* Table creation
* Data loading script
* Validation queries

### 7. Databricks Delta Lake Implementation

Document or build a Databricks version of the medallion architecture.

Planned components:

* Bronze Delta tables
* Silver Delta transformations
* Gold Delta marts
* Delta Lake documentation
* Databricks workflow plan

---

## Final Goal

The final version of this project will demonstrate a full healthcare data platform workflow:

```text
Synthetic Healthcare Data
        |
        v
Local Medallion Lakehouse
        |
        v
Validated Gold Analytics Tables
        |
        v
Snowflake / dbt Analytics Layer
        |
        v
PyTorch Patient Risk Model
        |
        v
Streamlit / Tableau Dashboard
```

The project is intended to serve as a portfolio artifact for Analytics Engineering, Data Engineering, BI Engineering, and healthcare analytics roles.
