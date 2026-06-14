# Portfolio Talking Points

## Project Name

Healthcare Claims & EHR Lakehouse with Databricks, Snowflake, dbt & PyTorch

## Short GitHub / LinkedIn Description

Built an end-to-end healthcare analytics lakehouse using synthetic EHR/FHIR-style data and Medicare claims-style data. The project demonstrates a complete modern data workflow across Bronze, Silver, and Gold medallion layers, Patient 360 analytics, Prefect orchestration, Snowflake loading, dbt analytics engineering, Streamlit dashboarding, Tableau Public reporting, Databricks Delta Lake migration artifacts, and a PyTorch patient risk modeling workflow.

## One-Sentence Summary

Designed and built a full-stack healthcare data lakehouse that transforms synthetic EHR and claims data into analytics-ready Gold marts, a Patient 360 dashboard layer, Tableau Public reporting, Streamlit dashboards, Snowflake warehouse tables, dbt marts, and PyTorch-ready patient risk features.

## 30-Second Interview Explanation

I built a healthcare claims and EHR lakehouse project to demonstrate a modern end-to-end analytics platform. The pipeline starts with synthetic clinical and Medicare claims-style data, processes it through Bronze, Silver, and Gold medallion layers, and produces patient-level analytics tables. I then built a Patient 360 Gold mart for care-management and executive reporting, published a Tableau Public dashboard, added a Streamlit dashboard, created Snowflake loading and validation scripts, built dbt staging/intermediate/mart models, added Databricks Delta Lake migration artifacts, and trained a baseline PyTorch model for patient risk workflow validation. The goal was to show that I can connect data engineering, analytics engineering, BI, orchestration, and machine learning into one cohesive healthcare analytics workflow.

## 2-Minute Interview Explanation

I built this project as a flagship portfolio healthcare analytics platform that combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data. I wanted the project to reflect the kind of modern data stack used in analytics engineering, data engineering, BI, and machine learning roles, so I structured it around a medallion lakehouse architecture.

The local pipeline uses Python, pandas, and Parquet. Synthetic raw data is generated first, then ingested into a Bronze layer, cleaned and standardized into a Silver layer, and aggregated into Gold patient-level analytics tables. The Gold layer includes patient master data, utilization summaries, condition summaries, medication summaries, observation summaries, and patient risk features.

I then added a Patient 360 Gold mart to make the project more business-facing. Patient 360 combines demographics, utilization, condition burden, cost proxies, risk indicators, and dashboard-friendly segments into a single patient-level view. This supports care management review, utilization monitoring, cost-risk segmentation, and executive reporting.

From the Gold and Patient 360 layers, I created Tableau-ready CSV exports, a published Tableau Public dashboard, and a Streamlit dashboard MVP. I also created validation and profiling reports so the project is reviewable and not just transformation code.

To make the project more aligned with production analytics workflows, I added a dbt implementation with staging, intermediate, and mart models using DuckDB locally. I added schema tests to validate the models. I also built a Snowflake workflow that creates warehouse objects, loads Gold Parquet tables, and validates the loaded tables. For the lakehouse migration layer, I added Databricks notebook-style scripts showing how the local pandas/Parquet pipeline maps to Bronze, Silver, and Gold Delta Lake tables.

I also added a local Prefect orchestration flow so the main workflow can run from synthetic raw data generation through Bronze, Silver, Gold, Patient 360 profiling, and Tableau-ready exports in one command.

Finally, I added a real-world public data extension using the MIMIC-IV Clinical Database Demo and CMS Basic Stand Alone Medicare Claims PUF. Those datasets are ingested, profiled, and validated separately. I intentionally did not join them into Patient 360 because they are not naturally linkable, which reflects a responsible healthcare data design decision.

The main value of the project is that it demonstrates the full path from raw healthcare-style data to business-ready analytics, BI dashboards, cloud warehouse loading, analytics engineering models, orchestration, and machine learning features.

## Resume Bullet Options

### Data Engineering / Analytics Engineering Version

* Built an end-to-end healthcare claims and EHR lakehouse using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Prefect, Streamlit, Tableau Public, and PyTorch to model a modern healthcare analytics platform.
* Developed Bronze, Silver, and Gold medallion pipeline layers to generate, ingest, clean, validate, and aggregate synthetic EHR/FHIR-style and Medicare claims-style data into patient-level analytics tables.
* Built a Patient 360 Gold mart combining demographics, utilization, condition burden, cost proxies, risk features, and care-management segmentation into a single BI-ready patient view.
* Created dbt staging, intermediate, and mart models with schema tests to transform curated Gold data into analytics-ready patient risk and utilization models.
* Built Snowflake object creation, Gold table loading, and validation scripts to demonstrate warehouse deployment of curated healthcare analytics data.
* Designed Databricks notebook-style PySpark scripts to migrate the local pandas/Parquet pipeline into Bronze, Silver, and Gold Delta Lake architecture.
* Added a local Prefect orchestration flow to run the synthetic healthcare pipeline from raw data generation through Gold marts, Patient 360 profiling, and Tableau-ready exports.

### BI / Dashboard Version

* Published a Tableau Public Patient 360 dashboard from a Gold healthcare analytics mart to support care-management review, cost-risk segmentation, utilization monitoring, and patient-level drilldown.
* Created Tableau-ready CSV exports and a Streamlit dashboard from Gold healthcare analytics tables to support patient utilization, chronic condition, cost, and risk feature analysis.
* Designed executive-facing KPI cards, segmentation charts, a cost-vs-utilization scatter plot, interactive filters, and a patient detail table for healthcare analytics storytelling.
* Developed Gold profile reports, Patient 360 profile reports, and export manifests to document curated healthcare data outputs and improve project reviewability for BI and analytics stakeholders.
* Modeled patient-level utilization, condition, medication, observation, reimbursement, and risk feature tables to support healthcare reporting and executive dashboard use cases.

### Machine Learning Version

* Engineered a PyTorch-ready patient risk feature dataset from Gold healthcare analytics tables, including utilization, condition, medication, observation, and claims cost features.
* Trained and evaluated a baseline PyTorch model for high-cost patient risk classification, producing training and evaluation reports for workflow validation.
* Built an end-to-end ML workflow from curated Gold data to tensors, model training, model evaluation, and documented output artifacts.
* Positioned model results as workflow-validation metrics rather than production-grade predictive performance because the dataset is synthetic.

### Public Data / Healthcare Data Version

* Added real-world public healthcare ingestion workflows for MIMIC-IV Clinical Database Demo and CMS Basic Stand Alone Medicare Claims PUF data.
* Ingested selected public EHR-style and claims-style datasets into separate Bronze Parquet layers with profiling, validation, and documentation reports.
* Documented the decision not to join MIMIC-IV Demo and CMS Claims PUF data into Patient 360 because the datasets are not naturally linkable at the patient level.
* Demonstrated responsible healthcare data modeling by separating synthetic linked analytics from real-world public ingestion and validation workflows.

### Short Resume Bullet Set

* Built an end-to-end healthcare claims and EHR lakehouse using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Prefect, Streamlit, Tableau Public, and PyTorch.
* Developed Bronze, Silver, and Gold medallion pipelines to transform synthetic clinical and claims data into patient-level analytics, Patient 360 BI outputs, and ML-ready risk features.
* Published a Tableau Public Patient 360 dashboard with KPI cards, care-management segmentation, cost/utilization analytics, interactive filters, and patient-level drilldown.
* Created dbt models/tests, Snowflake loading and validation scripts, Databricks Delta migration notebooks, Prefect orchestration, and a baseline PyTorch patient risk model.

## Best Resume Version to Use

For most Analytics Engineer, Data Engineer, BI Engineer, and Data Analyst applications, use this version:

```text
Built an end-to-end healthcare claims and EHR lakehouse using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Prefect, Streamlit, Tableau Public, and PyTorch.

Developed Bronze, Silver, and Gold medallion pipelines to transform synthetic clinical and claims data into patient-level analytics tables, Patient 360 BI outputs, and ML-ready risk features.

Published a Tableau Public Patient 360 dashboard with KPI cards, care-management segmentation, cost/utilization analytics, interactive filters, and patient-level drilldown.

Created dbt models/tests, Snowflake loading and validation scripts, Databricks Delta migration notebooks, Prefect orchestration, and a baseline PyTorch patient risk model to demonstrate a full modern analytics workflow.
```

## Tableau Public Dashboard

Published a Tableau Public dashboard from the Patient 360 Gold mart:

**Healthcare Patient 360 Analytics Dashboard**
https://public.tableau.com/views/HealthcareClaimsEHRLakehouseReport/HealthcarePatient360AnalyticsDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

The dashboard presents a recruiter-facing healthcare analytics view built from the synthetic linked EHR + claims pipeline. It includes:

* Patient population KPI cards
* Care management priority segmentation
* Cost, utilization, and age-band distributions
* Cost proxy vs. utilization scatter plot
* Patient-level detail table
* Interactive filters for care priority, cost segment, utilization segment, age band, and gender

This dashboard demonstrates how raw EHR and claims data can be transformed through Bronze, Silver, and Gold lakehouse layers into executive-ready analytics artifacts for care management, utilization monitoring, cost-risk segmentation, and patient population analysis.

Important design decision: the Tableau Patient 360 dashboard uses synthetic linked EHR + claims data only. The MIMIC-IV Demo and CMS Claims PUF public-data extensions are documented as separate ingestion, profiling, and validation tracks because those datasets are not naturally linkable at the patient level.

## GitHub README Project Blurb

This project demonstrates an end-to-end healthcare analytics lakehouse using synthetic EHR/FHIR-style data and synthetic Medicare claims-style data. It transforms raw healthcare data through Bronze, Silver, and Gold medallion layers, then extends the curated Gold layer into a Patient 360 mart, Tableau Public dashboard, Streamlit dashboard, PyTorch ML workflow, dbt analytics engineering models, Snowflake warehouse loading, Databricks Delta Lake migration artifacts, and Prefect orchestration.

The project is designed to show practical experience across data engineering, analytics engineering, business intelligence, healthcare analytics, orchestration, cloud warehouse workflows, and machine learning.

## LinkedIn Project Post Draft

I recently built an end-to-end healthcare claims and EHR lakehouse portfolio project using Python, pandas, Parquet, dbt, Snowflake, Databricks Delta Lake, Prefect, Streamlit, Tableau Public, and PyTorch.

The project combines synthetic EHR/FHIR-style data with synthetic Medicare claims-style data and processes it through a Bronze, Silver, and Gold medallion architecture.

The final Gold layer supports multiple downstream workflows:

* Patient 360 analytics mart
* Tableau Public healthcare analytics dashboard
* Streamlit dashboarding
* Patient utilization analytics
* Chronic condition summaries
* Care-management segmentation
* PyTorch-ready patient risk features
* Baseline patient risk model training and evaluation
* dbt staging, intermediate, and mart models
* Snowflake loading and validation
* Databricks Delta Lake migration artifacts
* Prefect local orchestration

I also added a real-world public data extension using MIMIC-IV Clinical Database Demo and CMS Medicare Claims PUF data. These public datasets are ingested, profiled, and validated separately rather than being forced into a patient-level join.

The goal was to build something that reflects how analytics engineering, data engineering, BI, orchestration, and machine learning can connect in a realistic healthcare data platform.

## Technical Skills Demonstrated

* Python scripting
* pandas transformations
* Parquet file workflows
* Medallion architecture
* Synthetic data generation
* Data validation
* Data profiling
* Healthcare data modeling
* Patient-level feature engineering
* Patient 360 mart design
* dbt modeling and testing
* Snowflake loading and validation
* Databricks Delta Lake migration
* PySpark notebook-style development
* Prefect orchestration
* Streamlit dashboarding
* Tableau Public dashboard publishing
* Tableau-ready export design
* PyTorch tensor creation
* Baseline model training and evaluation
* Git/GitHub project workflow

## Business Skills Demonstrated

* Translating healthcare data into patient-level analytics
* Designing risk and utilization features
* Building care-management segmentation logic
* Creating executive-facing KPI dashboards
* Creating recruiter-facing documentation
* Explaining technical architecture clearly
* Connecting data engineering outputs to BI and ML use cases
* Structuring a project around business questions
* Documenting assumptions, limitations, and future improvements
* Making responsible data design decisions around non-linkable healthcare datasets

## Business Questions Answered

This project supports analysis of questions such as:

* Which patients have the highest utilization?
* Which patients have multiple chronic conditions?
* Which patients are likely to become high-cost patients?
* Which patients may benefit from care management review?
* How do inpatient, outpatient, and carrier-style reimbursement fields contribute to total cost proxy?
* How are patients distributed across cost, utilization, age, and care-management priority segments?
* Which Gold tables are most useful for BI dashboards?
* How can patient-level healthcare features be prepared for machine learning?
* How can synthetic linked healthcare data and real public healthcare data be handled responsibly in the same project?

## Project Limitations

The main patient-level pipeline uses synthetic data, so the model metrics should not be interpreted as production-grade predictive performance.

The purpose of the project is to demonstrate the workflow pattern:

```text
Synthetic raw healthcare data
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
Patient 360
    |
    v
BI exports / Tableau Public / Streamlit / Snowflake / dbt / PyTorch / Databricks
```

The real-world public data extension demonstrates ingestion, profiling, and validation of realistic healthcare schemas, but those public datasets are not joined into Patient 360 because they are not naturally linkable.

A production version would require larger datasets, stronger patient matching logic, additional clinical features, model explainability, access controls, PHI governance, healthcare compliance review, and deployment-grade orchestration.

## How to Discuss the Synthetic Dataset

If asked about the synthetic dataset, say:

The main pipeline uses synthetic linked EHR and claims data because the goal is to demonstrate architecture and workflow without using protected health information. I expanded the synthetic cohort enough to support meaningful dashboard segmentation, but I still treat the model metrics as workflow-validation metrics rather than production-grade predictive performance.

The value is that the pipeline shows the full pattern from raw healthcare data to validated Gold tables, Patient 360 analytics, Tableau Public reporting, Streamlit dashboarding, Snowflake loading, dbt models, Databricks migration artifacts, Prefect orchestration, and PyTorch-ready ML artifacts.

With larger or production data, the same architecture could be extended into more realistic reporting, modeling, and care-management workflows.

## How to Explain the Tableau Dashboard

The Tableau dashboard is the main recruiter-facing business artifact.

It is built from the Patient 360 Gold mart and shows how raw synthetic EHR and claims data can be transformed into an executive healthcare analytics view. It includes KPI cards, care-management priority segmentation, cost and utilization distributions, age-band distribution, a cost-vs-utilization scatter plot, patient-level detail table, and interactive filters.

The dashboard is intentionally focused and polished rather than overbuilt. The goal is to show healthcare analytics storytelling: who the high-priority patients are, how cost and utilization vary, and how a care-management team might review a patient population.

## How to Explain the Patient 360 Component

I added a Patient 360 Gold mart to make the project more business-facing and easier to explain to recruiters, hiring managers, and analytics leaders.

Rather than only showing separate technical tables, Patient 360 combines demographics, utilization, condition burden, risk features, cost proxies, and dashboard-friendly segments into one patient-level view. This mirrors how healthcare analytics teams often build patient-centered marts for care management, executive reporting, population health, and BI consumption.

The Patient 360 milestone demonstrates that I can move beyond raw engineering and design an analytics product that connects:

* Data ingestion
* Medallion architecture
* Patient-level data modeling
* BI-ready exports
* Tableau Public dashboarding
* Streamlit dashboarding
* Data quality profiling
* Business segmentation
* Care-management storytelling

I also kept the real-world public data extension separate from Patient 360 because MIMIC-IV Demo and CMS Claims PUF are not naturally linkable. This is an important design decision because it avoids falsely implying that unrelated public datasets can be joined into a real patient-level record.

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

I created SQL object definitions, a Python loading script, and a validation script that checks the loaded tables. I also documented a practical type-handling issue where local Parquet flag fields were stored as `0/1`, so Snowflake table columns were defined as `NUMBER(1,0)` instead of `BOOLEAN`.

That reflects a real data engineering decision when dealing with typed files and warehouse loading.

## How to Explain the dbt Component

The dbt layer demonstrates analytics engineering practices on top of the curated Gold data.

I created staging models to standardize Gold tables, intermediate models to combine patient utilization and condition logic, and a mart model for patient risk features. I also added schema tests so the project includes transformation logic and quality checks.

## How to Explain the Prefect Component

The Prefect layer demonstrates local orchestration of the main synthetic healthcare lakehouse workflow.

The flow runs the pipeline from synthetic raw data generation through Bronze, Silver, Gold, Patient 360 profiling, and Tableau-ready exports. This gives the project a one-command orchestration path and shows how the separate scripts can be coordinated as a repeatable workflow.

I used Prefect locally rather than overcomplicating deployment because the goal was to demonstrate orchestration structure and portfolio readability.

## How to Explain the Real-World Public Data Extension

The real-world public data extension demonstrates that the project can handle realistic healthcare schemas beyond synthetic data.

I added ingestion, profiling, and validation workflows for MIMIC-IV Clinical Database Demo and CMS Basic Stand Alone Medicare Claims PUF. The MIMIC track represents public deidentified EHR-style data, while the CMS PUF track represents public Medicare claims-style data.

I intentionally did not join these datasets together because they come from different sources, populations, and deidentification processes. Instead, I kept them as separate public ingestion tracks. That design decision is important because it shows responsible healthcare data modeling rather than forcing an invalid patient-level join.

## Interview Q&A

### Why did you build this project?

I wanted a flagship portfolio project that showed more than isolated SQL or dashboard work. I wanted to demonstrate a full data lifecycle: ingestion, transformation, validation, orchestration, warehouse loading, analytics engineering, dashboarding, and machine learning.

### Why healthcare data?

Healthcare data is complex and business-critical. EHR and claims data are often stored separately, but combining them can support utilization analysis, care management, cost-risk segmentation, and patient risk modeling. Using synthetic healthcare data let me demonstrate those patterns without using protected health information.

### What was the hardest part?

The hardest part was keeping the project cohesive across many layers. It was not just about writing one script. I had to make sure the Gold outputs could support Patient 360, Tableau, Streamlit, ML, dbt, Snowflake, and Databricks artifacts while keeping the identifier strategy and documentation consistent.

### Why did you use synthetic linked data for Patient 360?

Patient 360 requires patient-level linkage between EHR and claims records. The synthetic EHR and claims datasets in this project are intentionally linkable, so they are appropriate for the Patient 360 dashboard. The public MIMIC-IV Demo and CMS Claims PUF datasets are not naturally linkable, so I kept them separate for ingestion, profiling, and validation.

### Why include MIMIC-IV Demo and CMS Claims PUF if they are not joined?

I included them to demonstrate real-world public healthcare data ingestion and profiling. They strengthen the project by showing that the architecture can handle realistic healthcare schemas, but I kept them separate because joining them would be analytically irresponsible.

### What does the Tableau dashboard show?

The Tableau dashboard shows an executive Patient 360 view of the synthetic linked patient population. It includes total patient counts, high-priority patient counts, cost proxy, average utilization, average condition burden, care-management segmentation, cost and utilization distributions, age-band distribution, a cost-vs-utilization scatter plot, interactive filters, and a patient-level detail table.

### What would you improve next?

I would add a formal architecture diagram image, include Tableau dashboard screenshots in the README, scale the synthetic data volume, add more realistic patient matching, improve clinical feature engineering, add diagnosis groupers such as HCC-style categories, add model explainability, add CI checks, and deploy the Streamlit dashboard.

### What does this project say about your skills?

It shows that I can think across the full analytics stack. I can build data pipelines, validate outputs, model analytics-ready tables, create BI artifacts, prepare ML features, work with warehouse workflows, build dbt models, orchestrate pipelines, and document the business value of the project.

### How would this translate to a real company?

In a real healthcare organization, this kind of architecture could support patient population analytics, utilization monitoring, cost-risk segmentation, care-management prioritization, BI dashboards, and ML feature generation. The synthetic data would be replaced with governed production EHR and claims sources, and the patient crosswalk would be handled with enterprise matching or privacy-preserving linkage.
