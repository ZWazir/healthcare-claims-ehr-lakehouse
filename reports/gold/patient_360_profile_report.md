# Patient 360 Profile Report

## Overview

This report profiles the `gold_patient_360.parquet` Gold mart. The table combines synthetic linked EHR and claims data into one patient-level analytics view for dashboarding, care-management storytelling, and portfolio review.

## Table Shape

- Rows: `250`
- Columns: `71`

## Patient Key Quality

- Patient keys found: `ehr_patient_id, claim_beneficiary_id, crosswalk_method`
- Unique patient key records: `250`
- Duplicate patient key rows: `0`

## Business Field Counts

### care_management_priority

- High priority: `94`
- Low priority: `86`
- Medium priority: `70`

### utilization_segment

- Low utilization: `119`
- High utilization: `80`
- Medium utilization: `51`

### cost_segment

- Low cost: `125`
- High cost: `63`
- Medium cost: `62`

### age_band

- 50-64: `94`
- 65+: `72`
- 35-49: `62`
- 18-34: `22`

## Important Numeric Fields

### patient_360_total_utilization_events

- Total: `2798.0`
- Mean: `11.19`
- Min: `2.0`
- Median: `8.0`
- Max: `34.0`

### patient_360_total_cost_proxy

- Total: `14836222.37`
- Mean: `59344.89`
- Min: `546.0`
- Median: `11869.625`
- Max: `373741.519047619`

### patient_360_condition_burden

- Total: `1612.0`
- Mean: `6.45`
- Min: `0.0`
- Median: `4.0`
- Max: `24.0`

## Notes

- This profile is based on the synthetic linked Gold pipeline.
- The MIMIC-IV Demo and CMS Claims PUF public datasets are not joined into Patient 360 because they are separate public data sources and are not naturally linkable.
- The current synthetic sample dataset is intentionally small, so profile metrics validate the workflow rather than production-scale statistical behavior.
