# Tableau Public Dashboard Plan

## Purpose

This document outlines the planned Tableau Public dashboard for the Healthcare Claims & EHR Lakehouse portfolio project.

The dashboard is designed to make the project easier for recruiters, hiring managers, and analytics leaders to understand without needing to inspect the full codebase. It turns the Gold-layer analytics outputs into a business-facing healthcare analytics story.

## Dashboard Goal

Create an executive-facing healthcare analytics dashboard that shows how raw EHR and claims data can be transformed into patient-level insights for:

- Care management review
- Utilization monitoring
- Cost-risk segmentation
- Patient population analysis
- Analytics portfolio storytelling

## Primary Tableau Data Source

The main Tableau Public dashboard should use:

```text
data/tableau_exports/patient_360_export.csv
```

This export is generated from:

```text
data/gold/gold_patient_360.parquet
```

The Patient 360 table combines synthetic linked EHR and claims data into a single patient-level analytics mart.

## Supporting Tableau Data Sources

Optional supporting exports:

```text
data/tableau_exports/patient_master_export.csv
data/tableau_exports/utilization_summary_export.csv
data/tableau_exports/condition_summary_export.csv
data/tableau_exports/patient_risk_features_export.csv
```

The first Tableau Public version should focus mainly on `patient_360_export.csv` to keep the dashboard simple, clear, and business-facing.

## Important Data Caveat

The Tableau dashboard should clearly state that the core patient-level analytics use synthetic linked EHR and claims data.

The real-world public MIMIC-IV Demo and CMS Claims PUF datasets are intentionally kept as separate ingestion and validation tracks because they are not naturally linkable. They should not be represented as a joined real-world patient record.

## Recommended Dashboard Title

Healthcare Patient 360 Analytics Dashboard

## Recommended Dashboard Subtitle

Synthetic EHR + Claims Lakehouse | Patient Risk, Utilization, and Care Management View

## Dashboard Page 1: Executive Overview

### Business Question

Which patients or patient segments may require higher care-management attention based on utilization, cost proxy, and condition burden?

### KPI Cards

Recommended KPI cards:

1. Total Patients
2. High Priority Patients
3. Total Cost Proxy
4. Average Utilization Events
5. Average Condition Burden

### Recommended Visuals

#### Care Management Priority Distribution

Chart type:

```text
Bar chart
```

Fields:

- Dimension: `care_management_priority`
- Measure: Count of patients

Purpose:

Shows how the patient population is distributed across care-management priority categories.

#### Cost Segment Distribution

Chart type:

```text
Bar chart
```

Fields:

- Dimension: `cost_segment`
- Measure: Count of patients

Purpose:

Shows how many patients fall into high, medium, low, or low-variation cost proxy groups.

#### Utilization Segment Distribution

Chart type:

```text
Bar chart
```

Fields:

- Dimension: `utilization_segment`
- Measure: Count of patients

Purpose:

Shows how many patients fall into high, medium, or low utilization groups.

#### Age Band Distribution

Chart type:

```text
Bar chart
```

Fields:

- Dimension: `age_band`
- Measure: Count of patients

Purpose:

Adds a basic demographic view of the patient population.

## Dashboard Page 2: Patient 360 Detail

### Business Question

What does an individual patient-level care-management view look like after combining demographics, utilization, condition burden, and risk features?

### Recommended Visuals

#### Patient Detail Table

Chart type:

```text
Text table
```

Recommended fields:

- `ehr_patient_id`
- `claim_beneficiary_id`
- `crosswalk_method`
- `age`
- `gender`
- `age_band`
- `patient_360_total_utilization_events`
- `patient_360_total_cost_proxy`
- `patient_360_condition_burden`
- `utilization_segment`
- `cost_segment`
- `care_management_priority`

Purpose:

Shows that the project can produce a single patient-level analytics view from multiple upstream Gold tables.

#### Cost Proxy vs Utilization

Chart type:

```text
Scatter plot
```

Fields:

- X-axis: `patient_360_total_utilization_events`
- Y-axis: `patient_360_total_cost_proxy`
- Color: `care_management_priority`
- Detail: `ehr_patient_id`

Purpose:

Shows the relationship between utilization intensity and cost proxy.

#### Condition Burden by Priority

Chart type:

```text
Bar chart or box plot
```

Fields:

- Dimension: `care_management_priority`
- Measure: Average `patient_360_condition_burden`

Purpose:

Shows whether higher-priority patients have greater clinical burden.

## Dashboard Page 3: Lakehouse Project Summary

### Business Question

What does this project demonstrate from a data engineering and analytics standpoint?

### Recommended Sections

Use a text panel or dashboard notes section to summarize:

- Raw synthetic EHR and claims ingestion
- Bronze, Silver, Gold medallion architecture
- Patient-level Gold marts
- Tableau-ready exports
- Streamlit dashboard
- PyTorch-ready ML feature dataset
- dbt analytics engineering layer
- Snowflake loading and validation
- Databricks Delta Lake migration scripts
- Real-world public data ingestion extension

### Recommended Architecture Text

```text
Raw synthetic EHR + claims data flows through Bronze, Silver, and Gold layers.
Gold outputs are used for BI dashboards, ML-ready feature engineering, dbt marts,
Snowflake loading, and Databricks Delta Lake migration artifacts.
```

## Recommended Dashboard Filters

Use these filters across the dashboard:

- `care_management_priority`
- `utilization_segment`
- `cost_segment`
- `age_band`
- `gender`
- `crosswalk_method`

## Recommended Tooltip Fields

Add these fields to tooltips where relevant:

- `ehr_patient_id`
- `claim_beneficiary_id`
- `age`
- `gender`
- `patient_360_total_utilization_events`
- `patient_360_total_cost_proxy`
- `patient_360_condition_burden`
- `care_management_priority`

## Recommended Tableau Calculated Fields

### Patient Count

```text
COUNTD([ehr_patient_id])
```

### High Priority Patient Count

```text
COUNTD(
    IF [care_management_priority] = "High priority"
    THEN [ehr_patient_id]
    END
)
```

### Average Utilization Events

```text
AVG([patient_360_total_utilization_events])
```

### Average Condition Burden

```text
AVG([patient_360_condition_burden])
```

### Total Cost Proxy

```text
SUM([patient_360_total_cost_proxy])
```

## Suggested Dashboard Layout

```text
Healthcare Patient 360 Analytics Dashboard

Top row:
- Total Patients
- High Priority Patients
- Total Cost Proxy
- Avg Utilization Events
- Avg Condition Burden

Middle row:
- Care Management Priority Distribution
- Cost Segment Distribution
- Utilization Segment Distribution

Bottom row:
- Cost Proxy vs Utilization Scatter Plot
- Patient Detail Table
```

## Recommended Dashboard Notes

Add a small note on the dashboard:

```text
This dashboard uses synthetic linked EHR and claims data to demonstrate a healthcare lakehouse analytics workflow. Real-world public datasets are included separately for ingestion, profiling, and validation, but are not joined into Patient 360 because they are not naturally linkable.
```

## Recruiter-Facing Talking Point

This Tableau dashboard demonstrates how I can turn an end-to-end data pipeline into a business-facing analytics product.

The project does not stop at raw ingestion or technical transformations. It creates a Patient 360 mart, exports BI-ready data, and presents patient-level risk, utilization, and care-management insights in a format that executives and analytics stakeholders can understand.

## First Tableau Public Version Scope

The first version should stay focused and avoid overbuilding.

Recommended v1 dashboard scope:

- One Tableau workbook
- One main dashboard
- `patient_360_export.csv` as the primary source
- 4 to 5 KPI cards
- 3 to 4 charts
- 1 patient detail table
- Short project methodology note

Future versions can add more pages or visuals after the first version is published.
