# Silver Layer

## Overview

The Silver layer contains cleaned and conformed healthcare data derived from the Bronze layer.

Bronze tables preserve raw source structure. Silver tables convert those raw source files into standardized, typed, analytics-ready datasets.

In this project, Silver is where Synthea EHR data and CMS SynPUF claims data become easier to query, validate, and eventually join into Gold patient-level analytics tables.

## Input

Silver tables are built from local Bronze Parquet files located in:

```text
data/bronze/synthea/
data/bronze/synpuf/
```

## Output

Silver tables are written as local Parquet files to:

```text
data/silver/
```

## Silver Tables

The current Silver layer creates the following tables:

| Table                                 | Source                     | Description                                                            |
| ------------------------------------- | -------------------------- | ---------------------------------------------------------------------- |
| `silver_patients.parquet`             | Synthea patients           | Clean EHR patient demographics                                         |
| `silver_encounters.parquet`           | Synthea encounters         | Clean clinical encounter records                                       |
| `silver_conditions.parquet`           | Synthea conditions         | Clean diagnosis and chronic condition records                          |
| `silver_medications.parquet`          | Synthea medications        | Clean medication records                                               |
| `silver_observations.parquet`         | Synthea observations       | Clean lab and clinical observation records                             |
| `silver_claims_beneficiaries.parquet` | SynPUF beneficiary summary | Clean claims-side beneficiary demographics and chronic condition flags |
| `silver_inpatient_claims.parquet`     | SynPUF inpatient claims    | Clean inpatient claims                                                 |
| `silver_outpatient_claims.parquet`    | SynPUF outpatient claims   | Clean outpatient claims                                                |

## Transformations Applied

The Silver layer applies the following transformation types:

1. Source-specific column renaming
2. Date parsing
3. Numeric type casting
4. Basic derived fields
5. Standardized patient and claim identifiers
6. Cleaner table-level schemas

## Examples

Synthea patient source column:

```text
Id
```

becomes:

```text
ehr_patient_id
```

Synthea encounter source column:

```text
TOTAL_CLAIM_COST
```

becomes:

```text
total_claim_cost
```

CMS SynPUF source column:

```text
DESYNPUF_ID
```

becomes:

```text
claim_beneficiary_id
```

CMS SynPUF source column:

```text
MEDREIMB_IP
```

becomes:

```text
inpatient_reimbursement_amount
```

## Derived Fields

The Silver layer also creates useful derived fields.

Examples:

| Field                               | Description                                                     |
| ----------------------------------- | --------------------------------------------------------------- |
| `is_deceased`                       | Indicates whether a patient has a death date                    |
| `encounter_duration_hours`          | Duration between encounter start and stop                       |
| `is_active_condition`               | Indicates whether a condition has no stop date                  |
| `is_active_medication`              | Indicates whether a medication has no stop date                 |
| `chronic_condition_count`           | Count of chronic condition flags in claims beneficiary data     |
| `total_annual_reimbursement_amount` | Sum of inpatient, outpatient, and carrier reimbursement amounts |

## Design Rationale

Silver is the first trusted layer of the lakehouse.

The goal is not to build final business metrics yet. The goal is to make source data clean, typed, consistent, and ready for integration.

This layer gives downstream Gold tables a reliable foundation.

## Validation

Silver validation is performed with:

```bash
python scripts/silver/validate_silver_tables.py
```

The validation script checks that:

* Required Silver tables exist
* Each table can be read
* Each table has rows
* Important required columns exist

## Current Project Stage

Current status:

```text
Silver transformation script created
Silver validation script created
Silver documentation created
Local Silver Parquet outputs created from sample raw data
```

## Next Layer

The next step is the Gold layer.

The Gold layer will create patient-level analytics tables for reporting and machine learning.

Planned Gold outputs include:

* Patient master table
* Patient utilization summary
* Patient condition summary
* Patient medication summary
* Patient claims summary
* Patient risk modeling dataset

Gold is where the project begins to answer business questions such as:

* Which patients have the highest total claims cost?
* Which patients have multiple chronic conditions?
* Which patients have emergency or inpatient utilization?
* Which patients may benefit from care management?
