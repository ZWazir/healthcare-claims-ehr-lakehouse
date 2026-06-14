# CMS Claims PUF Bronze Profile Report

## Overview

This report profiles the real-world/public CMS Basic Stand Alone Medicare Claims Public Use File Bronze tables.

The purpose of this report is to validate that the selected CMS claims CSV file was ingested into the project as a Parquet Bronze table and can be inspected for claims-oriented columns.

This public claims ingestion track is intentionally separate from the MIMIC-IV demo EHR ingestion track.

## Run Metadata

- Pipeline: `cms_claims_puf_bronze_profile`
- Dataset: CMS Basic Stand Alone Medicare Claims Public Use Files
- Profile timestamp UTC: 2026-06-14T01:40:58.439127+00:00
- Bronze directory: `data/real_world/bronze/cms_claims_puf`

## Summary

- Expected tables: 1
- Profiled tables: 1
- Missing tables: 0
- Tables passing basic checks: 1

## Table Profiles

### `inpatient_claims`

- Description: CMS Basic Stand Alone Medicare Claims PUF - 2008 Inpatient Claims
- Expected claim type: inpatient
- Expected source year: 2008
- Rows: 588415
- Columns: 12
- Duplicate rows: 0
- Total missing values: 276546
- Metadata columns present: True
- Passed basic checks: True

#### Candidate Claims Columns

- diagnosis_columns: `ip_clm_icd9_prcdr_cd`
- procedure_columns: `ip_clm_icd9_prcdr_cd`
- payment_or_cost_columns: `ip_drg_quint_pmt_avg`, `ip_drg_quint_pmt_cd`
- date_columns: `_source_year`
- provider_columns: None detected
- metadata_columns: `_source_file`, `_claim_type`, `_source_year`, `_ingestion_timestamp_utc`

#### Columns With Missing Values

| Column | Missing Count | Missing % |
|---|---:|---:|
| `ip_clm_icd9_prcdr_cd` | 276546 | 47.0% |

#### Top Value Summaries

**`bene_sex_ident_cd`**

- Unique values: 2
- Top values:
  - `2`: 330198
  - `1`: 258217

**`bene_age_cat_cd`**

- Unique values: 6
- Top values:
  - `6`: 122287
  - `1`: 116080
  - `5`: 94759
  - `4`: 91487
  - `3`: 86205

**`ip_clm_days_cd`**

- Unique values: 4
- Top values:
  - `2`: 261419
  - `4`: 128898
  - `3`: 122073
  - `1`: 76025

**`ip_drg_quint_pmt_cd`**

- Unique values: 5
- Top values:
  - `2`: 118387
  - `5`: 118218
  - `3`: 117659
  - `1`: 117509
  - `4`: 116642

#### Columns

`ip_clm_id`, `bene_sex_ident_cd`, `bene_age_cat_cd`, `ip_clm_base_drg_cd`, `ip_clm_icd9_prcdr_cd`, `ip_clm_days_cd`, `ip_drg_quint_pmt_avg`, `ip_drg_quint_pmt_cd`, `_source_file`, `_claim_type`, `_source_year`, `_ingestion_timestamp_utc`

## Interpretation

The CMS Claims PUF Bronze ingestion validates that public Medicare claims-style CSV files can be ingested into the project as local Parquet tables.

This does not replace or link to the synthetic EHR + claims pipeline or the MIMIC-IV demo EHR ingestion. It is a separate public claims ingestion extension.

This separation is important because the CMS public use files do not provide linkable beneficiary identities and should not be joined to unrelated clinical datasets.
