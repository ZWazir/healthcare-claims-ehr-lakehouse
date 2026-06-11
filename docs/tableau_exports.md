# Tableau Export Layer

## Purpose

The Tableau export layer creates clean CSV extracts from the Gold analytics tables in the local healthcare lakehouse project.

The Gold layer is stored in Parquet format because Parquet is efficient for local analytics workflows and lakehouse-style data processing. However, Tableau Public works most easily with CSV extracts, especially for portfolio projects that need to be easy to share, inspect, and reproduce.

This layer provides a bridge between the lakehouse analytics outputs and business intelligence dashboarding.

## Source Layer

The Tableau exports are created from the Gold layer located at:

```text
data/gold/
```

Current source tables include:

```text
gold_patient_master.parquet
gold_utilization_summary.parquet
gold_condition_summary.parquet
gold_patient_risk_features.parquet
```

## Export Location

The Tableau-ready CSV files are written to:

```text
data/tableau_exports/
```

Generated export files:

```text
patient_master_export.csv
utilization_summary_export.csv
condition_summary_export.csv
patient_risk_features_export.csv
```

## Export Script

The export script is located at:

```text
scripts/exports/create_tableau_exports.py
```

Run the script from the project root:

```bash
python scripts/exports/create_tableau_exports.py
```

## Validation Manifest

The script also creates a JSON manifest report at:

```text
reports/tableau_exports/tableau_export_manifest.json
```

The manifest includes:

* Export timestamp
* Source file path
* Output CSV path
* Row count
* Column count
* Validation status
* Any warnings

## Why CSV Exports Are Included

This project already includes a Streamlit dashboard MVP, but Tableau exports add another business intelligence path.

This is useful because Tableau Public is easy to share externally and is commonly recognized by recruiters, hiring managers, and analytics teams.

The export layer demonstrates that the lakehouse pipeline can support multiple downstream consumers:

```text
Gold Parquet Tables
        |
        |-- Streamlit dashboard
        |
        |-- Tableau Public CSV extracts
        |
        |-- Future PyTorch ML dataset
        |
        |-- Future Snowflake/dbt warehouse layer
```

## Tableau Use Cases

The exported CSV files can support dashboard pages such as:

### Patient Overview

Source:

```text
patient_master_export.csv
```

Possible views:

* Patient count
* Patient demographics
* Patient age distribution
* Patient gender distribution
* Patient geography, if available

### Utilization Analysis

Source:

```text
utilization_summary_export.csv
```

Possible views:

* Encounter count by patient
* Inpatient/outpatient utilization
* High-utilization patient segments
* Utilization distribution

### Condition Analysis

Source:

```text
condition_summary_export.csv
```

Possible views:

* Most common conditions
* Chronic condition burden
* Condition count by patient
* Condition patterns by patient segment

### Patient Risk Features

Source:

```text
patient_risk_features_export.csv
```

Possible views:

* High-risk patient flag
* Risk feature distributions
* Relationship between utilization, conditions, and risk
* Patients who may benefit from care management

## Design Choices

### CSV Format

CSV was selected because it is simple, portable, and easy to upload into Tableau Public.

### Gold Layer Source

The exports come from the Gold layer because Gold tables are already cleaned, modeled, and analytics-ready.

### Minimal Transformation

The export script does not substantially change business logic. It only performs lightweight cleanup needed for BI compatibility, such as:

* Standardizing column names
* Replacing infinite values
* Formatting datetime columns
* Writing clean CSV files
* Creating a validation manifest

This keeps the Tableau layer separate from the core lakehouse transformation logic.

## Portfolio Value

This layer strengthens the project by showing that the lakehouse can serve multiple practical business use cases.

It demonstrates:

* BI extract creation
* Gold-layer data product thinking
* Tableau Public readiness
* Dashboard-friendly data modeling
* Validation and reproducibility
* A clear path from data engineering to stakeholder-facing analytics

## Current Status

The Tableau export layer is part of the 75% to 78% project milestone.

Completion criteria:

* Tableau export script exists
* CSV extracts are generated
* Export manifest is created
* Documentation is added
* Files are committed to Git
