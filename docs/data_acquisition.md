# Data Acquisition

## Overview

This project uses two synthetic healthcare data sources:

1. Synthea synthetic EHR/FHIR data
2. CMS Medicare DE-SynPUF synthetic claims data

The goal is to combine clinical patient data with healthcare claims data in a modern lakehouse architecture.

The raw datasets are not committed to this repository because they can be large. Instead, the repository documents where each file should be placed and provides inspection scripts to validate the raw data locally.

## Data Source 1: Synthea EHR/FHIR Data

Synthea is an open-source synthetic patient generator that creates realistic but fictional patient medical histories.

In this project, Synthea represents the clinical/EHR side of the healthcare ecosystem.

Expected directory:

```text
data/raw/synthea/
```

Expected CSV files:

```text
patients.csv
encounters.csv
conditions.csv
medications.csv
observations.csv
procedures.csv
careplans.csv
immunizations.csv
```

These files represent clinical activity such as patient demographics, encounters, diagnoses, medications, lab observations, procedures, care plans, and immunizations.

## Data Source 2: CMS Medicare DE-SynPUF Claims Data

CMS Medicare DE-SynPUF is a synthetic Medicare claims dataset designed to mimic the structure of real Medicare claims data while protecting beneficiary privacy.

In this project, SynPUF represents the claims and payment side of the healthcare ecosystem.

Expected directory:

```text
data/raw/synpuf/
```

Expected project-friendly file names:

```text
beneficiary_summary.csv
inpatient_claims.csv
outpatient_claims.csv
carrier_claims.csv
prescription_drug_events.csv
```

These files represent Medicare-style claims activity, including beneficiary demographics, inpatient claims, outpatient claims, carrier/professional claims, and prescription drug events.

## File Naming Strategy

Raw source files may have long official names.

For local development, this project uses simpler file names to make transformation code easier to read and maintain.

Example official-style file name:

```text
DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv
```

Project-friendly file name:

```text
beneficiary_summary.csv
```

This naming strategy keeps the pipeline code cleaner while preserving documentation about the original data source.

## Integration Note

Synthea and CMS SynPUF are separate synthetic datasets.

They do not naturally share patient identifiers.

To demonstrate a realistic healthcare data integration workflow, this project will create a synthetic patient crosswalk between the EHR data and claims data.

The crosswalk is used only for portfolio demonstration purposes and should not be interpreted as a real patient linkage process.

## Local Data Placement

Place Synthea CSV files in:

```text
data/raw/synthea/
```

Place CMS SynPUF CSV files in:

```text
data/raw/synpuf/
```

The raw data folders are excluded from Git tracking through `.gitignore`.

Only code, documentation, schemas, and small sample files should be committed to GitHub.

## Validation Scripts

After adding raw files, run:

```bash
python scripts/inspect/inspect_raw_files.py
```

This script prints basic information about each raw CSV file, including:

* File path
* Column names
* Sample rows
* Inferred data types

Then run:

```bash
python scripts/inspect/create_schema_summary.py
```

This script generates a Markdown schema summary at:

```text
docs/raw_schema_summary.md
```

The schema summary helps document the raw source structure before building Bronze, Silver, and Gold lakehouse layers.

## Important Limitation

Both Synthea and CMS SynPUF are synthetic datasets.

They are appropriate for software development, analytics engineering practice, machine learning experimentation, and portfolio demonstration.

They should not be used to draw real-world clinical, actuarial, financial, or public policy conclusions.

## Current Project Stage

At this stage, the project has selected its source systems and created documentation for raw data placement and validation.

The next step is to build the Bronze ingestion layer, which will read raw CSV files and write standardized local lakehouse files.
