# MIMIC-IV Demo Bronze Profile Report

## Overview

This report profiles the real-world/public MIMIC-IV Clinical Database Demo Bronze tables.

The purpose of this report is to validate that selected MIMIC-IV demo CSV files were ingested into the project as Parquet Bronze tables and that the expected core columns are present.

This real-world ingestion track is intentionally separate from the synthetic linked EHR + claims pipeline.

## Run Metadata

- Pipeline: `mimic_demo_bronze_profile`
- Dataset: MIMIC-IV Clinical Database Demo
- Dataset version: 2.2
- Profile timestamp UTC: 2026-06-14T01:24:24.961547+00:00
- Bronze directory: `data/real_world/bronze/mimic_demo`

## Summary

- Expected tables: 9
- Profiled tables: 9
- Missing tables: 0
- Tables passing basic checks: 9

## Table Profiles

### `patients`

- Rows: 100
- Columns: 6
- Duplicate rows: 0
- Total missing values: 69
- Passed basic checks: True

Missing required columns: None

Columns with missing values:

| Column | Missing Count | Missing % |
|---|---:|---:|
| `dod` | 69 | 69.0% |

Columns:

`subject_id`, `gender`, `anchor_age`, `anchor_year`, `anchor_year_group`, `dod`

### `admissions`

- Rows: 275
- Columns: 16
- Duplicate rows: 0
- Total missing values: 500
- Passed basic checks: True

Missing required columns: None

Columns with missing values:

| Column | Missing Count | Missing % |
|---|---:|---:|
| `deathtime` | 260 | 94.55% |
| `discharge_location` | 42 | 15.27% |
| `marital_status` | 12 | 4.36% |
| `edregtime` | 93 | 33.82% |
| `edouttime` | 93 | 33.82% |

Columns:

`subject_id`, `hadm_id`, `admittime`, `dischtime`, `deathtime`, `admission_type`, `admit_provider_id`, `admission_location`, `discharge_location`, `insurance`, `language`, `marital_status`, `race`, `edregtime`, `edouttime`, `hospital_expire_flag`

### `diagnoses_icd`

- Rows: 4506
- Columns: 5
- Duplicate rows: 0
- Total missing values: 0
- Passed basic checks: True

Missing required columns: None

Columns with missing values: None

Columns:

`subject_id`, `hadm_id`, `seq_num`, `icd_code`, `icd_version`

### `procedures_icd`

- Rows: 722
- Columns: 6
- Duplicate rows: 0
- Total missing values: 0
- Passed basic checks: True

Missing required columns: None

Columns with missing values: None

Columns:

`subject_id`, `hadm_id`, `seq_num`, `chartdate`, `icd_code`, `icd_version`

### `d_icd_diagnoses`

- Rows: 109775
- Columns: 3
- Duplicate rows: 0
- Total missing values: 0
- Passed basic checks: True

Missing required columns: None

Columns with missing values: None

Columns:

`icd_code`, `icd_version`, `long_title`

### `d_icd_procedures`

- Rows: 85257
- Columns: 3
- Duplicate rows: 0
- Total missing values: 0
- Passed basic checks: True

Missing required columns: None

Columns with missing values: None

Columns:

`icd_code`, `icd_version`, `long_title`

### `labevents`

- Rows: 107727
- Columns: 16
- Duplicate rows: 0
- Total missing values: 362091
- Passed basic checks: True

Missing required columns: None

Columns with missing values:

| Column | Missing Count | Missing % |
|---|---:|---:|
| `hadm_id` | 28420 | 26.38% |
| `order_provider_id` | 90897 | 84.38% |
| `storetime` | 992 | 0.92% |
| `value` | 9588 | 8.9% |
| `valuenum` | 12481 | 11.59% |
| `valueuom` | 16203 | 15.04% |
| `ref_range_lower` | 18728 | 17.38% |
| `ref_range_upper` | 18728 | 17.38% |
| `flag` | 67452 | 62.61% |
| `priority` | 9329 | 8.66% |
| `comments` | 89273 | 82.87% |

Columns:

`labevent_id`, `subject_id`, `hadm_id`, `specimen_id`, `itemid`, `order_provider_id`, `charttime`, `storetime`, `value`, `valuenum`, `valueuom`, `ref_range_lower`, `ref_range_upper`, `flag`, `priority`, `comments`

### `prescriptions`

- Rows: 18087
- Columns: 21
- Duplicate rows: 0
- Total missing values: 28405
- Passed basic checks: True

Missing required columns: None

Columns with missing values:

| Column | Missing Count | Missing % |
|---|---:|---:|
| `poe_id` | 118 | 0.65% |
| `poe_seq` | 118 | 0.65% |
| `order_provider_id` | 94 | 0.52% |
| `stoptime` | 14 | 0.08% |
| `formulary_drug_cd` | 12 | 0.07% |
| `gsn` | 2519 | 13.93% |
| `ndc` | 21 | 0.12% |
| `prod_strength` | 9 | 0.05% |
| `form_rx` | 18075 | 99.93% |
| `dose_val_rx` | 9 | 0.05% |
| `dose_unit_rx` | 9 | 0.05% |
| `form_val_disp` | 9 | 0.05% |
| `form_unit_disp` | 9 | 0.05% |
| `doses_per_24_hrs` | 7383 | 40.82% |
| `route` | 6 | 0.03% |

Columns:

`subject_id`, `hadm_id`, `pharmacy_id`, `poe_id`, `poe_seq`, `order_provider_id`, `starttime`, `stoptime`, `drug_type`, `drug`, `formulary_drug_cd`, `gsn`, `ndc`, `prod_strength`, `form_rx`, `dose_val_rx`, `dose_unit_rx`, `form_val_disp`, `form_unit_disp`, `doses_per_24_hrs`, `route`

### `icustays`

- Rows: 140
- Columns: 8
- Duplicate rows: 0
- Total missing values: 0
- Passed basic checks: True

Missing required columns: None

Columns with missing values: None

Columns:

`subject_id`, `hadm_id`, `stay_id`, `first_careunit`, `last_careunit`, `intime`, `outtime`, `los`

## Interpretation

The MIMIC-IV demo Bronze ingestion validates that real deidentified EHR-style CSV files can be ingested into the project as local Parquet tables.

This does not replace the synthetic linked EHR + claims pipeline. Instead, it extends the project by adding a separate real-world ingestion track for public clinical data.
