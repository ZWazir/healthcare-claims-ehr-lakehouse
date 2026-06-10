# Gold Layer

## Overview

The Gold layer contains business-ready analytics tables built from cleaned Silver data.

In this project, the Gold layer combines synthetic EHR data from Synthea with synthetic claims data from CMS SynPUF to create patient-level summaries for reporting, dashboarding, and machine learning.

Gold tables are designed to answer business questions such as:

* Which patients have the highest healthcare cost?
* Which patients have multiple chronic conditions?
* Which patients have high inpatient or emergency utilization?
* Which patients may benefit from care management?
* Which features should be used for patient risk modeling?

## Input

Gold tables are built from local Silver Parquet files located in:

```text
data/silver/
```

## Output

Gold tables are written as local Parquet files to:

```text
data/gold/
```

## Gold Tables

The current Gold layer creates the following tables:

| Table                                | Description                                                          |
| ------------------------------------ | -------------------------------------------------------------------- |
| `gold_patient_crosswalk.parquet`     | Synthetic linkage between EHR patient IDs and claims beneficiary IDs |
| `gold_patient_master.parquet`        | Combined patient demographics from EHR and claims sources            |
| `gold_condition_summary.parquet`     | Patient-level condition and chronic disease features                 |
| `gold_utilization_summary.parquet`   | Patient-level encounter and claims utilization features              |
| `gold_medication_summary.parquet`    | Patient-level medication count and medication cost features          |
| `gold_observation_summary.parquet`   | Patient-level clinical observation summary features                  |
| `gold_patient_risk_features.parquet` | Final analytics and machine learning feature table                   |

## Patient Crosswalk

Synthea and CMS SynPUF are separate synthetic datasets.

They do not naturally share patient identifiers.

To demonstrate EHR and claims integration, this project creates a synthetic patient crosswalk between:

```text
ehr_patient_id
claim_beneficiary_id
```

The current crosswalk method is:

```text
synthetic_row_number_match
```

This means EHR patients and claims beneficiaries are sorted and matched by row number.

This is not intended to represent real patient matching. It is used only to support local portfolio development and demonstrate lakehouse integration patterns.

## Main Gold Feature Table

The most important Gold table is:

```text
gold_patient_risk_features.parquet
```

This table combines:

* Patient demographics
* EHR condition features
* Claims chronic condition flags
* Encounter utilization
* Inpatient claims
* Outpatient claims
* Medication features
* Clinical observation features
* Annual claims reimbursement

This table is used by both the dashboard layer and the PyTorch modeling layer.

## Derived Features

The Gold layer creates patient-level features such as:

| Feature                             | Description                                               |
| ----------------------------------- | --------------------------------------------------------- |
| `age`                               | Patient age as of a fixed reference date                  |
| `ehr_condition_count`               | Count of EHR condition records                            |
| `ehr_active_condition_count`        | Count of active EHR conditions                            |
| `chronic_condition_count`           | Count of claims-side chronic condition flags              |
| `ehr_encounter_count`               | Count of EHR encounters                                   |
| `ehr_emergency_encounter_count`     | Count of EHR emergency encounters                         |
| `inpatient_claim_count`             | Count of inpatient claims                                 |
| `outpatient_claim_count`            | Count of outpatient claims                                |
| `total_claim_count`                 | Total inpatient and outpatient claim count                |
| `total_claims_paid`                 | Total payment amount from inpatient and outpatient claims |
| `medication_count`                  | Count of medication records                               |
| `active_medication_count`           | Count of active medications                               |
| `total_medication_cost`             | Total medication cost                                     |
| `observation_count`                 | Count of clinical observations                            |
| `total_annual_reimbursement_amount` | Annual reimbursement amount from claims summary data      |

## Target and Business Flags

The Gold layer creates two important flags.

### High-Cost Patient Flag

```text
high_cost_patient_flag
```

This flag identifies patients above the median annual reimbursement amount.

It is the first target variable for the PyTorch model.

### Care Management Candidate Flag

```text
care_management_candidate_flag
```

This flag identifies patients who may be candidates for care management based on high clinical or utilization risk.

A patient is flagged if they meet at least one of the following conditions:

* Two or more chronic conditions
* At least one inpatient claim
* At least one emergency encounter

## Design Rationale

The Gold layer is designed for business usability.

Bronze preserves raw source data.

Silver cleans and standardizes source data.

Gold creates patient-level analytics assets that can be consumed by:

* Snowflake
* dbt
* Dashboards
* Machine learning models
* Portfolio demonstrations

This layer represents the transition from data engineering into analytics engineering and predictive modeling.

## Validation

Gold validation is performed with:

```bash
python scripts/gold/validate_gold_tables.py
```

The validation script checks that:

* Required Gold tables exist
* Each Gold table can be read
* Each Gold table has rows
* Important required columns exist
* The machine learning target flag contains only valid values

## Current Project Stage

Current status:

```text
Gold transformation script created
Gold validation script created
Gold documentation created
Gold patient-level analytics tables created from sample data
```

## Next Step

The next step is to create a local pipeline runner.

The runner will execute the project in order:

```text
Generate sample raw data
Inspect raw files
Create raw schema summary
Build Bronze tables
Validate Bronze tables
Build Silver tables
Validate Silver tables
Build Gold tables
Validate Gold tables
```

After that, the project will have a repeatable local pipeline that can be run with one command.
