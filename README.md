# Healthcare Claims & EHR Lakehouse with Databricks, Snowflake, dbt & PyTorch

## Overview

This project builds an end-to-end healthcare data lakehouse that combines synthetic EHR/FHIR data from Synthea with synthetic Medicare claims data from CMS DE-SynPUF.

The goal is to demonstrate a modern healthcare analytics platform using Databricks, Delta Lake, Snowflake, dbt, and PyTorch. The pipeline ingests raw clinical and claims data, transforms it through a medallion architecture, creates analytics-ready marts, and trains a machine learning model to predict high-risk or high-cost patients.

## Data Sources

### Synthea EHR/FHIR Data

Synthea provides realistic but fictional patient medical histories, including patients, encounters, conditions, medications, observations, procedures, care plans, and immunizations.

### CMS Medicare DE-SynPUF Claims Data

CMS DE-SynPUF provides synthetic Medicare-style claims data, including beneficiary summaries, inpatient claims, outpatient claims, carrier claims, and prescription drug events.

## Architecture

```text
Synthea CSV / FHIR Data       CMS SynPUF Claims Data
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
### Planned Outputs

Bronze, Silver, and Gold lakehouse tables
Snowflake analytics warehouse schema
dbt staging and mart models
dbt data quality tests
PyTorch patient risk model
Streamlit dashboard
Tableau Public dashboard
Architecture documentation
Business Questions
Which patients are most likely to become high-cost patients?
Which chronic conditions are associated with higher claims cost?
How does inpatient utilization vary by patient segment?
What are the relationships between medications, diagnoses, and cost?
Which patients may benefit from care management intervention?

### Tech Stack

Python
pandas
PySpark
Databricks
Delta Lake
Snowflake
dbt
PyTorch
Streamlit
Tableau