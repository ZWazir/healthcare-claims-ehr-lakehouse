# Raw Data Manifest

## Overview

This document tracks the raw source files expected by the Healthcare Claims & EHR Lakehouse project.

The project combines two synthetic healthcare data sources:

1. Synthea EHR/FHIR-style clinical data
2. CMS Medicare DE-SynPUF claims data

Raw files are stored locally under the `data/raw/` directory and are not committed to GitHub.

## Directory Structure

Expected raw data folder structure:

```text
data/
└── raw/
    ├── synthea/
    │   ├── patients.csv
    │   ├── encounters.csv
    │   ├── conditions.csv
    │   ├── medications.csv
    │   ├── observations.csv
    │   ├── procedures.csv
    │   ├── careplans.csv
    │   └── immunizations.csv
    │
    └── synpuf/
        ├── beneficiary_summary.csv
        ├── inpatient_claims.csv
        ├── outpatient_claims.csv
        ├── carrier_claims.csv
        └── prescription_drug_events.csv
```

## Synthea EHR Data

Expected directory:

```text
data/raw/synthea/
```

Synthea represents the clinical/EHR side of the project. These files contain synthetic patient demographics, encounters, diagnoses, medications, lab observations, procedures, care plans, and immunizations.

| File                |    Required | Description                           | Expected Use                                      |
| ------------------- | ----------: | ------------------------------------- | ------------------------------------------------- |
| `patients.csv`      |         Yes | Patient demographics and identifiers  | Patient dimension, age, gender, race, ethnicity   |
| `encounters.csv`    |         Yes | Clinical visits and care encounters   | Utilization, encounter frequency, care settings   |
| `conditions.csv`    |         Yes | Diagnoses and chronic conditions      | Chronic disease flags, risk features              |
| `medications.csv`   |         Yes | Medication orders and prescriptions   | Medication burden, therapeutic categories         |
| `observations.csv`  |         Yes | Lab results and clinical observations | Clinical risk indicators and lab-derived features |
| `procedures.csv`    | Recommended | Procedures performed during care      | Procedure utilization and care intensity          |
| `careplans.csv`     |    Optional | Care plans assigned to patients       | Care management context                           |
| `immunizations.csv` |    Optional | Immunization history                  | Preventive care indicators                        |

## CMS Medicare DE-SynPUF Claims Data

Expected directory:

```text
data/raw/synpuf/
```

CMS SynPUF represents the claims and payment side of the project. These files contain synthetic Medicare-style beneficiary, utilization, claim, and prescription drug records.

| Project File Name              |    Required | Description                                        | Expected Use                                       |
| ------------------------------ | ----------: | -------------------------------------------------- | -------------------------------------------------- |
| `beneficiary_summary.csv`      |         Yes | Beneficiary demographics and annual summary fields | Claims-side patient demographics and eligibility   |
| `inpatient_claims.csv`         |         Yes | Inpatient facility claims                          | Hospital utilization, inpatient cost, admissions   |
| `outpatient_claims.csv`        |         Yes | Outpatient facility claims                         | Outpatient utilization and cost                    |
| `carrier_claims.csv`           | Recommended | Professional/carrier claims                        | Physician services and professional claim activity |
| `prescription_drug_events.csv` | Recommended | Part D prescription drug events                    | Pharmacy utilization and medication cost           |

## File Naming Conventions

Official source files may have long names. For this project, files should be renamed into simpler project-friendly names.

Example:

```text
DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv
```

Rename to:

```text
beneficiary_summary.csv
```

This keeps pipeline code easier to read and makes the repository structure more intuitive.

## Required Minimum Files for MVP

The minimum viable project requires these files:

```text
data/raw/synthea/patients.csv
data/raw/synthea/encounters.csv
data/raw/synthea/conditions.csv
data/raw/synthea/medications.csv
data/raw/synthea/observations.csv

data/raw/synpuf/beneficiary_summary.csv
data/raw/synpuf/inpatient_claims.csv
data/raw/synpuf/outpatient_claims.csv
```

With these files, the project can build:

* Patient demographics
* Encounter/utilization features
* Diagnosis/chronic condition features
* Medication features
* Claims cost and utilization features
* Patient risk modeling dataset

## Optional Files for Extended Version

These files are useful but not required for the first working version:

```text
data/raw/synthea/procedures.csv
data/raw/synthea/careplans.csv
data/raw/synthea/immunizations.csv

data/raw/synpuf/carrier_claims.csv
data/raw/synpuf/prescription_drug_events.csv
```

These files can support richer downstream analytics, including procedure intensity, preventive care, care management, physician services, and prescription drug utilization.

## Raw Data Handling Rules

Raw data files should not be modified directly.

Instead, the pipeline should follow this pattern:

```text
Raw CSV files
→ Bronze standardized copies
→ Silver cleaned and conformed tables
→ Gold analytics-ready tables
```

The raw folder should preserve the source data as originally downloaded or exported, except for project-friendly file renaming.

## Git Tracking Rules

Raw data files are excluded from GitHub using `.gitignore`.

The repository should commit:

* Code
* Documentation
* dbt models
* Schema summaries
* Small sample data only if needed

The repository should not commit:

* Full raw datasets
* Large Parquet files
* Delta table files
* Model artifacts
* Environment files
* Secrets or credentials

## Schema Inspection

After placing raw files into the expected folders, run:

```bash
python scripts/inspect/inspect_raw_files.py
```

This prints basic details about each file:

* File path
* Column names
* Sample rows
* Inferred data types

Then run:

```bash
python scripts/inspect/create_schema_summary.py
```

This generates:

```text
docs/raw_schema_summary.md
```

The schema summary is used to document the raw data structure before building the Bronze ingestion layer.

## Current Manifest Status

Current project stage:

```text
Raw data manifest defined
Raw data folders created
Raw data inspection scripts created
Actual source files not yet loaded
```

Once the raw source files are added and inspected, the project can move into Bronze ingestion.

## Next Engineering Step

The next step is to build the Bronze ingestion layer.

The Bronze layer will:

1. Read raw CSV files from `data/raw/synthea/` and `data/raw/synpuf/`
2. Standardize column names
3. Add metadata columns such as source system and ingestion timestamp
4. Write standardized outputs to `data/bronze/`
5. Prepare the project for Databricks Delta Lake implementation
