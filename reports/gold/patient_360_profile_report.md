# Patient 360 Profile Report

## Overview

This report profiles the `gold_patient_360.parquet` Gold mart. The table combines synthetic linked EHR and claims data into one patient-level analytics view for dashboarding, care-management storytelling, and portfolio review.

## Table Shape

- Rows: `3`
- Columns: `71`

## Patient Key Quality

- Patient keys found: `ehr_patient_id, claim_beneficiary_id, crosswalk_method`
- Unique patient key records: `3`
- Duplicate patient key rows: `0`

## Business Field Counts

### care_management_priority

- High priority: `3`

### utilization_segment

- Not enough variation: `3`

### cost_segment

- Low cost: `1`
- Medium cost: `1`
- High cost: `1`

### age_band

- 65+: `2`
- 50-64: `1`

## Important Numeric Fields

### patient_360_total_utilization_events

- Total: `12.0`
- Mean: `4.0`
- Min: `4.0`
- Median: `4.0`
- Max: `4.0`

### patient_360_total_cost_proxy

- Total: `67135.52`
- Mean: `22378.51`
- Min: `3948.3199999999997`
- Median: `6512.6`
- Max: `56674.6`

### patient_360_condition_burden

- Total: `17`
- Mean: `5.67`
- Min: `3`
- Median: `4.0`
- Max: `10`

## Notes

- This profile is based on the synthetic linked Gold pipeline.
- The MIMIC-IV Demo and CMS Claims PUF public datasets are not joined into Patient 360 because they are separate public data sources and are not naturally linkable.
- The current synthetic sample dataset is intentionally small, so profile metrics validate the workflow rather than production-scale statistical behavior.
