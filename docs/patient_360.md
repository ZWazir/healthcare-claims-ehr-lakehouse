# Patient 360 Gold Mart

## Purpose

The Patient 360 Gold mart is an executive-facing patient-level table that combines the most useful synthetic linked EHR and claims data into one analytics-ready view.

This table is designed for:

- Care management review
- Executive dashboarding
- Tableau and Streamlit reporting
- Portfolio storytelling
- Patient-level analytics exploration

The Patient 360 table is built from the synthetic linked Gold pipeline, not from the real-world public MIMIC-IV Demo or CMS Claims PUF datasets.

## Why Patient 360 Uses Synthetic Linked Data

The main v1.0 lakehouse uses synthetic EHR and claims data that were intentionally designed to be linkable at the patient level.

The v1.1 real-world public data extension uses:

- MIMIC-IV Clinical Database Demo
- CMS Basic Stand Alone Medicare Claims Public Use Files

These are separate public datasets and are not naturally linkable to each other. For that reason, the real-world extension demonstrates ingestion, profiling, validation, and documentation, while the synthetic linked data remains the core end-to-end patient analytics pipeline.

This avoids falsely implying that unrelated public datasets can be joined into a real patient-level record.

## Source Tables

The Patient 360 mart is built from existing Gold layer outputs:

- `gold_patient_master.parquet`
- `gold_utilization_summary.parquet`
- `gold_condition_summary.parquet`
- `gold_medication_summary.parquet`
- `gold_observation_summary.parquet`
- `gold_patient_risk_features.parquet`

The patient identifier fields used for joins are:

- `ehr_patient_id`
- `claim_beneficiary_id`
- `crosswalk_method`

## Output Files

The Patient 360 build creates:

```text
data/gold/gold_patient_360.parquet
reports/gold/patient_360_build_report.json
```

The Tableau export workflow also creates:

```text
data/tableau_exports/patient_360_export.csv
```

## Derived Business Fields

The Patient 360 mart adds dashboard-friendly fields that make the table easier to use in BI tools.

### `age_band`

Groups patients into age categories:

- `0-17`
- `18-34`
- `35-49`
- `50-64`
- `65+`

### `patient_360_total_utilization_events`

A utilization proxy created by summing available patient-level count fields such as encounter, claim, admission, or visit counts.

### `patient_360_total_cost_proxy`

A cost proxy created by summing available patient-level cost, paid, payment, charge, or amount fields.

### `patient_360_condition_burden`

A clinical burden proxy created from available patient-level condition or diagnosis count fields.

### `utilization_segment`

Categorizes patients into dashboard-friendly utilization groups:

- High utilization
- Medium utilization
- Low utilization
- Not enough variation

### `cost_segment`

Categorizes patients into dashboard-friendly cost groups:

- High cost
- Medium cost
- Low cost
- Not enough variation

### `care_management_priority`

Creates a simple prioritization field for care-management storytelling:

- High priority
- Medium priority
- Clinical review
- Low priority

## Streamlit Dashboard Integration

The Streamlit app includes a dedicated Patient 360 tab with:

- Patient 360 row and column counts
- High-priority patient count
- Total cost proxy
- Care-management priority filter
- Utilization segment filter
- Cost segment filter
- Patient 360 preview table
- Patient 360 build report viewer

This gives recruiters and hiring managers an easy way to understand the business value of the lakehouse beyond the raw technical pipeline.

## Tableau Integration

The Patient 360 table is exported as:

```text
data/tableau_exports/patient_360_export.csv
```

This CSV can be used as a simple Tableau Public data source for an executive-facing patient overview dashboard.

## Portfolio Talking Point

This milestone demonstrates how raw clinical and claims data can be transformed into a patient-centered analytics mart. It shows the ability to design a data product that connects engineering, analytics, business segmentation, BI consumption, and care-management use cases.
