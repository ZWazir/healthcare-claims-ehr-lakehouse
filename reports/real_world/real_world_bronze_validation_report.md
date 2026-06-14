# Real-World Bronze Validation Report

## Overview

This report validates the real-world/public healthcare Bronze ingestion extension.

It checks that selected MIMIC-IV demo EHR tables and CMS Medicare Claims PUF tables exist as local Parquet Bronze outputs, contain rows, and include expected core columns.

The real-world MIMIC and CMS tracks are intentionally separate and are not force-linked.

## Run Metadata

- Pipeline: `real_world_bronze_validation`
- Validation timestamp UTC: 2026-06-14T01:45:49.512135+00:00
- Bronze directory: `data/real_world/bronze`

## Summary

- Total table checks: 10
- Passed table checks: 10
- Failed table checks: 0
- Total report checks: 6
- Passed report checks: 6
- Failed report checks: 0
- Overall passed: True

## Table Validation Results

| Source Group | Table | Rows | Columns | Missing Required Columns | Passed |
|---|---|---:|---:|---|---|
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/patients.parquet` | 100 | 6 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/admissions.parquet` | 275 | 16 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/diagnoses_icd.parquet` | 4506 | 5 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/procedures_icd.parquet` | 722 | 6 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/d_icd_diagnoses.parquet` | 109775 | 3 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/d_icd_procedures.parquet` | 85257 | 3 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/labevents.parquet` | 107727 | 16 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/prescriptions.parquet` | 18087 | 21 | None | True |
| MIMIC-IV Demo | `data/real_world/bronze/mimic_demo/icustays.parquet` | 140 | 8 | None | True |
| CMS Claims PUF | `data/real_world/bronze/cms_claims_puf/inpatient_claims.parquet` | 588415 | 12 | None | True |

## Report File Validation Results

| Report | Size Bytes | Passed |
|---|---:|---|
| `reports/real_world/mimic_demo_ingestion_report.json` | 4722 | True |
| `reports/real_world/mimic_demo_profile_report.json` | 19762 | True |
| `reports/real_world/mimic_demo_profile_report.md` | 5295 | True |
| `reports/real_world/cms_claims_puf_ingestion_report.json` | 1158 | True |
| `reports/real_world/cms_claims_puf_profile_report.json` | 4400 | True |
| `reports/real_world/cms_claims_puf_profile_report.md` | 2883 | True |

## Interpretation

This validation step confirms that the v1.1 real-world ingestion extension can produce local Bronze Parquet outputs and documentation reports from public healthcare datasets.

The synthetic linked EHR + claims pipeline remains the main end-to-end lakehouse demo. The real-world extension demonstrates public-data ingestion and profiling without making invalid patient-level linkage assumptions.
