# Portfolio Talking Points

## Project Name

Healthcare Claims & EHR Lakehouse with Databricks, Snowflake, dbt & PyTorch

## Short GitHub / LinkedIn Description

Built an end-to-end healthcare analytics lakehouse using synthetic EHR/FHIR-style data and Medicare claims-style data. The project demonstrates a complete modern data workflow across Bronze, Silver, and Gold medallion layers, Snowflake loading, dbt analytics engineering, Streamlit dashboarding, Tableau-ready exports, and a PyTorch patient risk modeling workflow.

## One-Sentence Summary

Designed and built a full-stack healthcare data lakehouse that transforms synthetic EHR and claims data into analytics-ready tables, BI outputs, Snowflake warehouse tables, dbt marts, and PyTorch-ready patient risk features.

## 30-Second Interview Explanation

I built a healthcare claims and EHR lakehouse project to demonstrate a modern end-to-end data platform. The pipeline starts with synthetic clinical and Medicare claims-style data, processes it through Bronze, Silver, and Gold medallion layers, and produces patient-level analytics tables. From there, I created Tableau-ready exports, a Streamlit dashboard, a Snowflake loading and validation workflow, dbt staging/intermediate/mart models, and a PyTorch baseline model for patient risk prediction. The goal was to show that I can connect data engineering, analytics engineering, BI, and machine learning into one cohesive healthcare analytics workflow.

## 2-Minute Interview Explanation

I built this project as a portfolio healthcare analytics platform that combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data. I wanted the project to reflect the kind of modern data stack used in analytics engineering and data engineering roles, so I structured it around a medallion lakehouse architecture.

The local pipeline uses Python, pandas, and Parquet. Raw synthetic data is first ingested into a Bronze layer, then cleaned and standardized into a Silver layer, and finally aggregated into Gold patient-level analytics tables. The Gold layer includes patient master data, utilization summaries, condition summaries, medication summaries, observation summaries, and patient risk features.

After building the core pipeline, I added validation and profiling scripts so the project was not just transformation code, but also had quality checks and output reports. I then extended the Gold layer into multiple downstream use cases. I created Tableau-ready CSV exports, a Streamlit dashboard MVP, a PyTorch-ready machine learning dataset, and a baseline PyTorch model for high-cost patient risk classification.

To make the project more aligned with production analytics workflows, I also added a dbt implementation with staging, intermediate, and mart models using DuckDB locally. I created dbt tests to validate the models. I also added a Snowflake workflow that creates warehouse objects, loads Gold Parquet tables, and validates the loaded tables. Finally, I added Databricks Delta Lake notebook-style scripts showing how the local pandas/Parquet pipeline maps to Bronze, Silver, and Gold Delta tables.

The main value of the project is that it demonstrates the full path from raw healthcare data to business-ready analytics and machine learning features. It shows practical experience with data pipelines, dimensional modeling, validation, BI outputs, cloud warehouse loading, analytics engineering, and ML workflow development.

## Resume Bullet Options

### Data Engineering / Analytics Engineering Version

- Built an end-to-end healthcare claims and EHR lakehouse using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, and PyTorch to model a modern healthcare analytics platform.
- Developed Bronze, Silver, and Gold medallion pipeline layers to ingest, clean, validate, and aggregate synthetic EHR/FHIR-style and Medicare claims-style data into patient-level analytics tables.
- Created dbt staging, intermediate, and mart models with schema tests to transform curated Gold data into analytics-ready patient risk and utilization models.
- Built Snowflake object creation, Gold table loading, and validation scripts to demonstrate warehouse deployment of curated healthcare analytics data.
- Designed Databricks notebook-style PySpark scripts to migrate the local pandas/Parquet pipeline into Bronze, Silver, and Gold Delta Lake architecture.

### BI / Dashboard Version

- Created Tableau-ready CSV exports and a Streamlit dashboard MVP from Gold healthcare analytics tables to support patient utilization, chronic condition, and risk feature analysis.
- Developed Gold profile reports and export manifests to document curated healthcare data outputs and improve project reviewability for BI and analytics stakeholders.
- Modeled patient-level utilization, condition, medication, observation, and risk feature tables to support healthcare reporting and executive dashboard use cases.

### Machine Learning Version

- Engineered a PyTorch-ready patient risk feature dataset from Gold healthcare analytics tables, including utilization, condition, medication, observation, and claims cost features.
- Trained and evaluated a baseline PyTorch model for high-cost patient risk classification, producing training and evaluation reports for workflow validation.
- Built an end-to-end ML workflow from curated Gold data to tensors, model training, model evaluation, and documented output artifacts.

### Short Resume Bullet Set

- Built an end-to-end healthcare claims and EHR lakehouse using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Streamlit, Tableau-ready exports, and PyTorch.
- Developed Bronze, Silver, and Gold medallion pipelines to transform synthetic clinical and claims data into patient-level analytics and ML-ready risk features.
- Created dbt models/tests, Snowflake loading/validation scripts, Databricks Delta migration notebooks, BI exports, and a baseline PyTorch patient risk model.

## Best Resume Version to Use

For most Analytics Engineer, Data Engineer, BI Engineer, and Data Analyst applications, use this version:

```text
Built an end-to-end healthcare claims and EHR lakehouse using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Streamlit, Tableau-ready exports, and PyTorch.

Developed Bronze, Silver, and Gold medallion pipelines to transform synthetic clinical and claims data into patient-level analytics tables, BI-ready outputs, and ML-ready risk features.

Created dbt models/tests, Snowflake loading and validation scripts, Databricks Delta migration notebooks, and a baseline PyTorch patient risk model to demonstrate a full modern analytics workflow.
```

## GitHub README Project Blurb

This project demonstrates an end-to-end healthcare analytics lakehouse using synthetic EHR/FHIR-style data and synthetic Medicare claims-style data. It transforms raw healthcare data through Bronze, Silver, and Gold medallion layers, then extends the curated Gold layer into BI exports, a Streamlit dashboard, a PyTorch ML workflow, dbt analytics engineering models, Snowflake warehouse loading, and Databricks Delta Lake migration artifacts.

The project is designed to show practical experience across data engineering, analytics engineering, business intelligence, healthcare analytics, and machine learning.

## LinkedIn Project Post Draft

I recently built an end-to-end healthcare claims and EHR lakehouse portfolio project using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Streamlit, Tableau-ready exports, and PyTorch.

The project combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data and processes it through a Bronze, Silver, and Gold medallion architecture.

The final Gold layer supports multiple downstream workflows:

- Patient utilization analytics
- Chronic condition summaries
- Tableau-ready CSV exports
- Streamlit dashboarding
- PyTorch-ready patient risk features
- Baseline patient risk model training and evaluation
- dbt staging, intermediate, and mart models
- Snowflake loading and validation
- Databricks Delta Lake migration artifacts

The goal was to build something that reflects how analytics engineering, data engineering, BI, and machine learning can connect in a realistic healthcare data platform.

## Technical Skills Demonstrated

- Python scripting
- pandas transformations
- Parquet file workflows
- Medallion architecture
- Data validation
- Data profiling
- Healthcare data modeling
- Patient-level feature engineering
- dbt modeling and testing
- Snowflake loading and validation
- Databricks Delta Lake migration
- PySpark notebook-style development
- Streamlit dashboarding
- Tableau-ready export design
- PyTorch tensor creation
- Baseline model training and evaluation
- Git/GitHub project workflow

## Business Skills Demonstrated

- Translating healthcare data into patient-level analytics
- Designing risk and utilization features
- Creating recruiter-facing documentation
- Explaining technical architecture clearly
- Connecting data engineering outputs to BI and ML use cases
- Structuring a project around business questions
- Documenting assumptions, limitations, and future improvements

## Business Questions Answered

This project supports analysis of questions such as:

- Which patients have the highest utilization?
- Which patients have multiple chronic conditions?
- Which patients are likely to become high-cost patients?
- How do inpatient, outpatient, and carrier claims contribute to total cost?
- Which Gold tables are most useful for BI dashboards?
- How can patient-level healthcare features be prepared for machine learning?

## Project Limitations

The project uses synthetic sample data, so the model metrics should not be interpreted as production-grade predictive performance.

The purpose of the project is to demonstrate the workflow pattern:

```text
Raw healthcare data
    |
    v
Bronze ingestion
    |
    v
Silver cleaning
    |
    v
Gold analytics marts
    |
    v
BI exports / Snowflake / dbt / PyTorch / Databricks
```

A production version would require larger datasets, stronger patient matching logic, additional clinical features, model explainability, orchestration, access controls, and healthcare compliance review.

## How to Discuss the Small Synthetic Dataset

If asked about the small dataset, say:

The dataset is intentionally synthetic and small because the purpose of the project is to demonstrate architecture and workflow, not to claim production-grade model performance. I documented that limitation directly in the project. The value is that the pipeline shows the full pattern from raw healthcare data to validated Gold tables, BI outputs, Snowflake loading, dbt models, and PyTorch-ready ML artifacts. With larger data, the same structure could be extended into more realistic modeling and reporting.

## How to Explain the PyTorch Component

The PyTorch component is a baseline workflow, not the main claim of predictive accuracy.

The goal was to show that I can take curated Gold analytics data, convert it into ML-ready features, create train/test tensors, train a simple neural network, evaluate it, and document the results.

This demonstrates the bridge between analytics engineering and machine learning engineering.

## How to Explain the Databricks Component

The Databricks files are notebook-style migration artifacts that show how the local pandas/Parquet pipeline maps to Databricks Runtime and Delta Lake.

The local pipeline proves the logic. The Databricks notebooks show how the same Bronze, Silver, and Gold architecture could scale using PySpark and Delta tables.

Local VS Code warnings for `spark`, `display`, or PySpark are expected because those files are intended for Databricks Runtime.

## How to Explain the Snowflake Component

The Snowflake layer shows how curated Gold data can be loaded into a cloud warehouse for analytics and validation.

I created SQL object definitions, a Python loading script, and a validation script that checks the loaded tables. I also documented a practical type handling issue where local Parquet flag fields were stored as `0/1`, so Snowflake table columns were defined as `NUMBER(1,0)` instead of `BOOLEAN`.

That reflects a real data engineering decision when dealing with typed files and warehouse loading.

## How to Explain the dbt Component

The dbt layer demonstrates analytics engineering practices on top of the curated Gold data.

I created staging models to standardize Gold tables, intermediate models to combine patient utilization and condition logic, and a mart model for patient risk features. I also added schema tests so the project includes transformation logic and quality checks.

## Interview Q&A

### Why did you build this project?

I wanted a flagship portfolio project that showed more than isolated SQL or dashboard work. I wanted to demonstrate a full data lifecycle: ingestion, transformation, validation, warehouse loading, analytics engineering, dashboarding, and machine learning.

### Why healthcare data?

Healthcare data is complex and business-critical. EHR and claims data are often stored separately, but combining them can support utilization analysis, care management, and patient risk modeling. Using synthetic healthcare data let me demonstrate those patterns without using real patient information.

### What was the hardest part?

The hardest part was keeping the project cohesive across many layers. It was not just about writing one script. I had to make sure the Gold outputs could support BI, ML, dbt, Snowflake, and Databricks artifacts while keeping the identifier strategy and documentation consistent.

### What would you improve next?

I would scale the synthetic data volume, add more realistic patient matching, improve clinical feature engineering, add model explainability, and orchestrate the pipeline with Databricks Workflows, Airflow, or Prefect.

### What does this project say about your skills?

It shows that I can think across the full analytics stack. I can build data pipelines, validate outputs, model analytics-ready tables, create BI artifacts, prepare ML features, work with warehouse workflows, and document the business value of the project.