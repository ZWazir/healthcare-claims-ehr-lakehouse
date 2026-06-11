# Gold Layer Profile Report

## Project: Healthcare Claims & EHR Lakehouse

This report profiles the Gold layer Parquet outputs used for analytics, business intelligence, and downstream machine learning.

Generated at: `2026-06-10T20:12:49`
Gold directory: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold`

## Summary

| Table | Exists | Rows | Columns | Full Row Duplicates | Key Duplicate Check |
|---|---:|---:|---:|---:|---|
| gold_patient_crosswalk.parquet | Yes | 3 | 3 | 0 | Not applicable |
| gold_patient_master.parquet | Yes | 3 | 17 | 0 | Not applicable |
| gold_condition_summary.parquet | Yes | 3 | 18 | 0 | Not applicable |
| gold_utilization_summary.parquet | Yes | 3 | 19 | 0 | Not applicable |
| gold_medication_summary.parquet | Yes | 3 | 9 | 0 | Not applicable |
| gold_observation_summary.parquet | Yes | 3 | 7 | 0 | Not applicable |
| gold_patient_risk_features.parquet | Yes | 3 | 64 | 0 | Not applicable |

---

## gold_patient_crosswalk.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_patient_crosswalk.parquet`
Rows: `3`
Columns: `3`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |
|:-----------------|:-----------------------|:---------------------------|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |

---

## gold_patient_master.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_patient_master.parquet`
Rows: `3`
Columns: `17`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method
- age
- gender
- race
- ethnicity
- city
- state
- county
- zip_code
- sex_code
- race_code
- state_code
- county_code
- is_deceased_ehr
- is_deceased_claims

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |
| age | int64 | 0 | 0.0% |
| gender | str | 0 | 0.0% |
| race | str | 0 | 0.0% |
| ethnicity | str | 0 | 0.0% |
| city | str | 0 | 0.0% |
| state | str | 0 | 0.0% |
| county | str | 0 | 0.0% |
| zip_code | str | 0 | 0.0% |
| sex_code | str | 0 | 0.0% |
| race_code | str | 0 | 0.0% |
| state_code | str | 0 | 0.0% |
| county_code | str | 0 | 0.0% |
| is_deceased_ehr | bool | 0 | 0.0% |
| is_deceased_claims | bool | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |   age | gender   | race   | ethnicity   | city        | state         | county           |   zip_code |   sex_code |   race_code |   state_code |   county_code | is_deceased_ehr   | is_deceased_claims   |
|:-----------------|:-----------------------|:---------------------------|------:|:---------|:-------|:------------|:------------|:--------------|:-----------------|-----------:|-----------:|------------:|-------------:|--------------:|:------------------|:---------------------|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |    71 | M        | white  | nonhispanic | Boston      | Massachusetts | Suffolk County   |      02108 |          1 |           1 |           22 |           001 | False             | False                |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |    63 | F        | white  | hispanic    | Springfield | Massachusetts | Hampden County   |      01103 |          2 |           5 |           22 |           013 | False             | False                |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |    75 | F        | black  | nonhispanic | Worcester   | Massachusetts | Worcester County |      01608 |          2 |           2 |           22 |           027 | False             | False                |

---

## gold_condition_summary.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_condition_summary.parquet`
Rows: `3`
Columns: `18`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method
- ehr_condition_count
- ehr_active_condition_count
- ehr_unique_condition_count
- has_alzheimer_or_dementia
- has_chf
- has_chronic_kidney_disease
- has_cancer
- has_copd
- has_depression
- has_diabetes
- has_ischemic_heart_disease
- has_osteoporosis
- has_rheumatoid_or_osteoarthritis
- has_stroke_or_tia
- chronic_condition_count

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |
| ehr_condition_count | int64 | 0 | 0.0% |
| ehr_active_condition_count | int64 | 0 | 0.0% |
| ehr_unique_condition_count | int64 | 0 | 0.0% |
| has_alzheimer_or_dementia | int64 | 0 | 0.0% |
| has_chf | int64 | 0 | 0.0% |
| has_chronic_kidney_disease | int64 | 0 | 0.0% |
| has_cancer | int64 | 0 | 0.0% |
| has_copd | int64 | 0 | 0.0% |
| has_depression | int64 | 0 | 0.0% |
| has_diabetes | int64 | 0 | 0.0% |
| has_ischemic_heart_disease | int64 | 0 | 0.0% |
| has_osteoporosis | int64 | 0 | 0.0% |
| has_rheumatoid_or_osteoarthritis | int64 | 0 | 0.0% |
| has_stroke_or_tia | int64 | 0 | 0.0% |
| chronic_condition_count | int64 | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |   ehr_condition_count |   ehr_active_condition_count |   ehr_unique_condition_count |   has_alzheimer_or_dementia |   has_chf |   has_chronic_kidney_disease |   has_cancer |   has_copd |   has_depression |   has_diabetes |   has_ischemic_heart_disease |   has_osteoporosis |   has_rheumatoid_or_osteoarthritis |   has_stroke_or_tia |   chronic_condition_count |
|:-----------------|:-----------------------|:---------------------------|----------------------:|-----------------------------:|-----------------------------:|----------------------------:|----------:|-----------------------------:|-------------:|-----------:|-----------------:|---------------:|-----------------------------:|-------------------:|-----------------------------------:|--------------------:|--------------------------:|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |                     1 |                            1 |                            1 |                           0 |         0 |                            0 |            0 |          0 |                0 |              0 |                            0 |                  0 |                                  0 |                   0 |                         0 |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |                     1 |                            1 |                            1 |                           0 |         0 |                            0 |            0 |          0 |                0 |              1 |                            0 |                  0 |                                  0 |                   0 |                         1 |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |                     1 |                            1 |                            1 |                           0 |         1 |                            1 |            0 |          1 |                1 |              1 |                            1 |                  0 |                                  1 |                   0 |                         7 |

---

## gold_utilization_summary.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_utilization_summary.parquet`
Rows: `3`
Columns: `19`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method
- ehr_encounter_count
- ehr_total_encounter_cost
- ehr_avg_encounter_cost
- ehr_emergency_encounter_count
- ehr_outpatient_encounter_count
- ehr_ambulatory_encounter_count
- ehr_total_encounter_duration_hours
- inpatient_claim_count
- inpatient_total_paid
- inpatient_avg_paid
- inpatient_total_days
- outpatient_claim_count
- outpatient_total_paid
- outpatient_avg_paid
- total_claim_count
- total_claims_paid

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |
| ehr_encounter_count | int64 | 0 | 0.0% |
| ehr_total_encounter_cost | float64 | 0 | 0.0% |
| ehr_avg_encounter_cost | float64 | 0 | 0.0% |
| ehr_emergency_encounter_count | int64 | 0 | 0.0% |
| ehr_outpatient_encounter_count | int64 | 0 | 0.0% |
| ehr_ambulatory_encounter_count | int64 | 0 | 0.0% |
| ehr_total_encounter_duration_hours | float64 | 0 | 0.0% |
| inpatient_claim_count | float64 | 0 | 0.0% |
| inpatient_total_paid | float64 | 0 | 0.0% |
| inpatient_avg_paid | float64 | 0 | 0.0% |
| inpatient_total_days | float64 | 0 | 0.0% |
| outpatient_claim_count | float64 | 0 | 0.0% |
| outpatient_total_paid | float64 | 0 | 0.0% |
| outpatient_avg_paid | float64 | 0 | 0.0% |
| total_claim_count | float64 | 0 | 0.0% |
| total_claims_paid | float64 | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |   ehr_encounter_count |   ehr_total_encounter_cost |   ehr_avg_encounter_cost |   ehr_emergency_encounter_count |   ehr_outpatient_encounter_count |   ehr_ambulatory_encounter_count |   ehr_total_encounter_duration_hours |   inpatient_claim_count |   inpatient_total_paid |   inpatient_avg_paid |   inpatient_total_days |   outpatient_claim_count |   outpatient_total_paid |   outpatient_avg_paid |   total_claim_count |   total_claims_paid |
|:-----------------|:-----------------------|:---------------------------|----------------------:|---------------------------:|-------------------------:|--------------------------------:|---------------------------------:|---------------------------------:|-------------------------------------:|------------------------:|-----------------------:|---------------------:|-----------------------:|-------------------------:|------------------------:|----------------------:|--------------------:|--------------------:|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |                     1 |                     129.16 |                   129.16 |                               0 |                                0 |                                1 |                             0.666667 |                       0 |                      0 |                    0 |                      0 |                        1 |                     550 |                   550 |                   1 |                 550 |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |                     1 |                     415.3  |                   415.3  |                               0 |                                1 |                                0 |                             1        |                       0 |                      0 |                    0 |                      0 |                        1 |                     900 |                   900 |                   1 |                 900 |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |                     1 |                    2750    |                  2750    |                               1 |                                0 |                                0 |                             6.5      |                       1 |                   8500 |                 8500 |                      3 |                        0 |                       0 |                     0 |                   1 |                8500 |

---

## gold_medication_summary.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_medication_summary.parquet`
Rows: `3`
Columns: `9`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method
- medication_count
- active_medication_count
- unique_medication_count
- total_medication_cost
- avg_medication_cost
- total_dispenses

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |
| medication_count | int64 | 0 | 0.0% |
| active_medication_count | int64 | 0 | 0.0% |
| unique_medication_count | int64 | 0 | 0.0% |
| total_medication_cost | float64 | 0 | 0.0% |
| avg_medication_cost | float64 | 0 | 0.0% |
| total_dispenses | int64 | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |   medication_count |   active_medication_count |   unique_medication_count |   total_medication_cost |   avg_medication_cost |   total_dispenses |
|:-----------------|:-----------------------|:---------------------------|-------------------:|--------------------------:|--------------------------:|------------------------:|----------------------:|------------------:|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |                  1 |                         1 |                         1 |                   150   |                 150   |                12 |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |                  1 |                         1 |                         1 |                   111   |                 111   |                12 |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |                  1 |                         1 |                         1 |                   136.8 |                 136.8 |                12 |

---

## gold_observation_summary.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_observation_summary.parquet`
Rows: `3`
Columns: `7`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method
- observation_count
- unique_observation_count
- avg_observation_value
- max_observation_value

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |
| observation_count | int64 | 0 | 0.0% |
| unique_observation_count | int64 | 0 | 0.0% |
| avg_observation_value | float64 | 0 | 0.0% |
| max_observation_value | float64 | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |   observation_count |   unique_observation_count |   avg_observation_value |   max_observation_value |
|:-----------------|:-----------------------|:---------------------------|--------------------:|---------------------------:|------------------------:|------------------------:|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |                   1 |                          1 |                   145   |                   145   |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |                   1 |                          1 |                     8.1 |                     8.1 |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |                   1 |                          1 |                   950   |                   950   |

---

## gold_patient_risk_features.parquet

Path: `/Users/zafarwazir/Documents/Career/Projects/healthcare_claims_ehr_lakehouse/data/gold/gold_patient_risk_features.parquet`
Rows: `3`
Columns: `64`

### Columns

- ehr_patient_id
- claim_beneficiary_id
- crosswalk_method
- age
- gender
- race
- ethnicity
- city
- state
- county
- zip_code
- sex_code
- race_code
- state_code
- county_code
- is_deceased_ehr
- is_deceased_claims
- ehr_condition_count
- ehr_active_condition_count
- ehr_unique_condition_count
- has_alzheimer_or_dementia
- has_chf
- has_chronic_kidney_disease
- has_cancer
- has_copd
- has_depression
- has_diabetes
- has_ischemic_heart_disease
- has_osteoporosis
- has_rheumatoid_or_osteoarthritis
- has_stroke_or_tia
- chronic_condition_count
- ehr_encounter_count
- ehr_total_encounter_cost
- ehr_avg_encounter_cost
- ehr_emergency_encounter_count
- ehr_outpatient_encounter_count
- ehr_ambulatory_encounter_count
- ehr_total_encounter_duration_hours
- inpatient_claim_count
- inpatient_total_paid
- inpatient_avg_paid
- inpatient_total_days
- outpatient_claim_count
- outpatient_total_paid
- outpatient_avg_paid
- total_claim_count
- total_claims_paid
- medication_count
- active_medication_count
- unique_medication_count
- total_medication_cost
- avg_medication_cost
- total_dispenses
- observation_count
- unique_observation_count
- avg_observation_value
- max_observation_value
- inpatient_reimbursement_amount
- outpatient_reimbursement_amount
- carrier_reimbursement_amount
- total_annual_reimbursement_amount
- high_cost_patient_flag
- care_management_candidate_flag

### Null Profile

| Column | Data Type | Null Count | Null Percent |
|---|---|---:|---:|
| ehr_patient_id | str | 0 | 0.0% |
| claim_beneficiary_id | str | 0 | 0.0% |
| crosswalk_method | str | 0 | 0.0% |
| age | int64 | 0 | 0.0% |
| gender | str | 0 | 0.0% |
| race | str | 0 | 0.0% |
| ethnicity | str | 0 | 0.0% |
| city | str | 0 | 0.0% |
| state | str | 0 | 0.0% |
| county | str | 0 | 0.0% |
| zip_code | str | 0 | 0.0% |
| sex_code | str | 0 | 0.0% |
| race_code | str | 0 | 0.0% |
| state_code | str | 0 | 0.0% |
| county_code | str | 0 | 0.0% |
| is_deceased_ehr | bool | 0 | 0.0% |
| is_deceased_claims | bool | 0 | 0.0% |
| ehr_condition_count | int64 | 0 | 0.0% |
| ehr_active_condition_count | int64 | 0 | 0.0% |
| ehr_unique_condition_count | int64 | 0 | 0.0% |
| has_alzheimer_or_dementia | int64 | 0 | 0.0% |
| has_chf | int64 | 0 | 0.0% |
| has_chronic_kidney_disease | int64 | 0 | 0.0% |
| has_cancer | int64 | 0 | 0.0% |
| has_copd | int64 | 0 | 0.0% |
| has_depression | int64 | 0 | 0.0% |
| has_diabetes | int64 | 0 | 0.0% |
| has_ischemic_heart_disease | int64 | 0 | 0.0% |
| has_osteoporosis | int64 | 0 | 0.0% |
| has_rheumatoid_or_osteoarthritis | int64 | 0 | 0.0% |
| has_stroke_or_tia | int64 | 0 | 0.0% |
| chronic_condition_count | int64 | 0 | 0.0% |
| ehr_encounter_count | int64 | 0 | 0.0% |
| ehr_total_encounter_cost | float64 | 0 | 0.0% |
| ehr_avg_encounter_cost | float64 | 0 | 0.0% |
| ehr_emergency_encounter_count | int64 | 0 | 0.0% |
| ehr_outpatient_encounter_count | int64 | 0 | 0.0% |
| ehr_ambulatory_encounter_count | int64 | 0 | 0.0% |
| ehr_total_encounter_duration_hours | float64 | 0 | 0.0% |
| inpatient_claim_count | float64 | 0 | 0.0% |
| inpatient_total_paid | float64 | 0 | 0.0% |
| inpatient_avg_paid | float64 | 0 | 0.0% |
| inpatient_total_days | float64 | 0 | 0.0% |
| outpatient_claim_count | float64 | 0 | 0.0% |
| outpatient_total_paid | float64 | 0 | 0.0% |
| outpatient_avg_paid | float64 | 0 | 0.0% |
| total_claim_count | float64 | 0 | 0.0% |
| total_claims_paid | float64 | 0 | 0.0% |
| medication_count | int64 | 0 | 0.0% |
| active_medication_count | int64 | 0 | 0.0% |
| unique_medication_count | int64 | 0 | 0.0% |
| total_medication_cost | float64 | 0 | 0.0% |
| avg_medication_cost | float64 | 0 | 0.0% |
| total_dispenses | int64 | 0 | 0.0% |
| observation_count | int64 | 0 | 0.0% |
| unique_observation_count | int64 | 0 | 0.0% |
| avg_observation_value | float64 | 0 | 0.0% |
| max_observation_value | float64 | 0 | 0.0% |
| inpatient_reimbursement_amount | int64 | 0 | 0.0% |
| outpatient_reimbursement_amount | int64 | 0 | 0.0% |
| carrier_reimbursement_amount | int64 | 0 | 0.0% |
| total_annual_reimbursement_amount | int64 | 0 | 0.0% |
| high_cost_patient_flag | int64 | 0 | 0.0% |
| care_management_candidate_flag | int64 | 0 | 0.0% |

### Duplicate Profile

- Full row duplicate count: `0`
- Key-level duplicate check: `Not applicable`

### Sample Records

| ehr_patient_id   | claim_beneficiary_id   | crosswalk_method           |   age | gender   | race   | ethnicity   | city        | state         | county           |   zip_code |   sex_code |   race_code |   state_code |   county_code | is_deceased_ehr   | is_deceased_claims   |   ehr_condition_count |   ehr_active_condition_count |   ehr_unique_condition_count |   has_alzheimer_or_dementia |   has_chf |   has_chronic_kidney_disease |   has_cancer |   has_copd |   has_depression |   has_diabetes |   has_ischemic_heart_disease |   has_osteoporosis |   has_rheumatoid_or_osteoarthritis |   has_stroke_or_tia |   chronic_condition_count |   ehr_encounter_count |   ehr_total_encounter_cost |   ehr_avg_encounter_cost |   ehr_emergency_encounter_count |   ehr_outpatient_encounter_count |   ehr_ambulatory_encounter_count |   ehr_total_encounter_duration_hours |   inpatient_claim_count |   inpatient_total_paid |   inpatient_avg_paid |   inpatient_total_days |   outpatient_claim_count |   outpatient_total_paid |   outpatient_avg_paid |   total_claim_count |   total_claims_paid |   medication_count |   active_medication_count |   unique_medication_count |   total_medication_cost |   avg_medication_cost |   total_dispenses |   observation_count |   unique_observation_count |   avg_observation_value |   max_observation_value |   inpatient_reimbursement_amount |   outpatient_reimbursement_amount |   carrier_reimbursement_amount |   total_annual_reimbursement_amount |   high_cost_patient_flag |   care_management_candidate_flag |
|:-----------------|:-----------------------|:---------------------------|------:|:---------|:-------|:------------|:------------|:--------------|:-----------------|-----------:|-----------:|------------:|-------------:|--------------:|:------------------|:---------------------|----------------------:|-----------------------------:|-----------------------------:|----------------------------:|----------:|-----------------------------:|-------------:|-----------:|-----------------:|---------------:|-----------------------------:|-------------------:|-----------------------------------:|--------------------:|--------------------------:|----------------------:|---------------------------:|-------------------------:|--------------------------------:|---------------------------------:|---------------------------------:|-------------------------------------:|------------------------:|-----------------------:|---------------------:|-----------------------:|-------------------------:|------------------------:|----------------------:|--------------------:|--------------------:|-------------------:|--------------------------:|--------------------------:|------------------------:|----------------------:|------------------:|--------------------:|---------------------------:|------------------------:|------------------------:|---------------------------------:|----------------------------------:|-------------------------------:|------------------------------------:|-------------------------:|---------------------------------:|
| ehr-patient-001  | claim-bene-001         | synthetic_row_number_match |    71 | M        | white  | nonhispanic | Boston      | Massachusetts | Suffolk County   |      02108 |          1 |           1 |           22 |           001 | False             | False                |                     1 |                            1 |                            1 |                           0 |         0 |                            0 |            0 |          0 |                0 |              0 |                            0 |                  0 |                                  0 |                   0 |                         0 |                     1 |                     129.16 |                   129.16 |                               0 |                                0 |                                1 |                             0.666667 |                       0 |                      0 |                    0 |                      0 |                        1 |                     550 |                   550 |                   1 |                 550 |                  1 |                         1 |                         1 |                   150   |                 150   |                12 |                   1 |                          1 |                   145   |                   145   |                                0 |                               550 |                            320 |                                 870 |                        0 |                                0 |
| ehr-patient-002  | claim-bene-002         | synthetic_row_number_match |    63 | F        | white  | hispanic    | Springfield | Massachusetts | Hampden County   |      01103 |          2 |           5 |           22 |           013 | False             | False                |                     1 |                            1 |                            1 |                           0 |         0 |                            0 |            0 |          0 |                0 |              1 |                            0 |                  0 |                                  0 |                   0 |                         1 |                     1 |                     415.3  |                   415.3  |                               0 |                                1 |                                0 |                             1        |                       0 |                      0 |                    0 |                      0 |                        1 |                     900 |                   900 |                   1 |                 900 |                  1 |                         1 |                         1 |                   111   |                 111   |                12 |                   1 |                          1 |                     8.1 |                     8.1 |                                0 |                               900 |                            480 |                                1380 |                        0 |                                0 |
| ehr-patient-003  | claim-bene-003         | synthetic_row_number_match |    75 | F        | black  | nonhispanic | Worcester   | Massachusetts | Worcester County |      01608 |          2 |           2 |           22 |           027 | False             | False                |                     1 |                            1 |                            1 |                           0 |         1 |                            1 |            0 |          1 |                1 |              1 |                            1 |                  0 |                                  1 |                   0 |                         7 |                     1 |                    2750    |                  2750    |                               1 |                                0 |                                0 |                             6.5      |                       1 |                   8500 |                 8500 |                      3 |                        0 |                       0 |                     0 |                   1 |                8500 |                  1 |                         1 |                         1 |                   136.8 |                 136.8 |                12 |                   1 |                          1 |                   950   |                   950   |                             8500 |                              2400 |                           1800 |                               12700 |                        1 |                                1 |
