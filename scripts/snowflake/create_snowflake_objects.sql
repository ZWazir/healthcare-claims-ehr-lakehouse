-- Healthcare Claims & EHR Lakehouse
-- Snowflake Object Creation Script
--
-- Purpose:
-- Creates the Snowflake database, schemas, warehouse, file format,
-- stages, and Gold-layer table structures for the healthcare lakehouse.
--
-- Note:
-- This script is designed for portfolio demonstration and Snowflake migration planning.
-- Update role, warehouse size, and database names as needed for your Snowflake account.

-- -----------------------------------------------------------------------------
-- Warehouse
-- -----------------------------------------------------------------------------

create warehouse if not exists HEALTHCARE_LAKEHOUSE_WH
    warehouse_size = 'XSMALL'
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true
    comment = 'Warehouse for healthcare claims and EHR lakehouse portfolio project.';

-- -----------------------------------------------------------------------------
-- Database and schemas
-- -----------------------------------------------------------------------------

create database if not exists HEALTHCARE_LAKEHOUSE_DB
    comment = 'Healthcare Claims and EHR Lakehouse portfolio database.';

use database HEALTHCARE_LAKEHOUSE_DB;

create schema if not exists RAW
    comment = 'Raw landing schema for source healthcare data.';

create schema if not exists BRONZE
    comment = 'Bronze schema for ingested source-aligned data.';

create schema if not exists SILVER
    comment = 'Silver schema for cleaned and standardized healthcare data.';

create schema if not exists GOLD
    comment = 'Gold schema for analytics-ready patient-level marts.';

create schema if not exists ML
    comment = 'Machine learning feature and scoring schema.';

use schema GOLD;

-- -----------------------------------------------------------------------------
-- File format
-- -----------------------------------------------------------------------------

create file format if not exists HEALTHCARE_PARQUET_FORMAT
    type = parquet
    comment = 'Parquet file format for loading local Gold outputs into Snowflake.';

-- -----------------------------------------------------------------------------
-- Internal stage
-- -----------------------------------------------------------------------------

create stage if not exists GOLD_PARQUET_STAGE
    file_format = HEALTHCARE_PARQUET_FORMAT
    comment = 'Internal stage for Gold-layer Parquet files.';

-- -----------------------------------------------------------------------------
-- Gold table: patient master
-- -----------------------------------------------------------------------------

create table if not exists GOLD_PATIENT_MASTER (
    ehr_patient_id string,
    claim_beneficiary_id string,
    crosswalk_method string,
    age integer,
    gender string,
    race string,
    ethnicity string,
    city string,
    state string,
    county string,
    zip_code string,
    sex_code string,
    race_code string,
    state_code string,
    county_code string,
    is_deceased_ehr boolean,
    is_deceased_claims boolean
)
comment = 'Gold patient master table combining EHR and claims identifiers with demographic attributes.';

-- -----------------------------------------------------------------------------
-- Gold table: utilization summary
-- -----------------------------------------------------------------------------

create table if not exists GOLD_UTILIZATION_SUMMARY (
    ehr_patient_id string,
    claim_beneficiary_id string,
    crosswalk_method string,
    ehr_encounter_count integer,
    ehr_inpatient_encounter_count integer,
    ehr_outpatient_encounter_count integer,
    claim_inpatient_count integer,
    claim_outpatient_count integer,
    claim_carrier_count integer,
    total_claim_count integer,
    total_allowed_amount float,
    total_paid_amount float,
    total_patient_responsibility float,
    avg_allowed_amount_per_claim float,
    avg_paid_amount_per_claim float
)
comment = 'Gold patient-level utilization and claims cost summary table.';

-- -----------------------------------------------------------------------------
-- Gold table: condition summary
-- -----------------------------------------------------------------------------

create table if not exists GOLD_CONDITION_SUMMARY (
    ehr_patient_id string,
    claim_beneficiary_id string,
    crosswalk_method string,
    condition_count integer,
    chronic_condition_count integer,
    has_diabetes number(1,0),
    has_hypertension number(1,0),
    has_copd number(1,0),
    has_chf number(1,0),
    has_ckd number(1,0),
    has_cancer number(1,0),
    has_depression number(1,0)
)
comment = 'Gold patient-level condition summary table.';

-- -----------------------------------------------------------------------------
-- Gold table: medication summary
-- -----------------------------------------------------------------------------

create table if not exists GOLD_MEDICATION_SUMMARY (
    ehr_patient_id string,
    claim_beneficiary_id string,
    crosswalk_method string,
    medication_count integer,
    unique_medication_count integer
)
comment = 'Gold patient-level medication summary table.';

-- -----------------------------------------------------------------------------
-- Gold table: observation summary
-- -----------------------------------------------------------------------------

create table if not exists GOLD_OBSERVATION_SUMMARY (
    ehr_patient_id string,
    claim_beneficiary_id string,
    crosswalk_method string,
    observation_count integer,
    avg_systolic_bp float,
    avg_diastolic_bp float,
    avg_bmi float,
    avg_glucose float
)
comment = 'Gold patient-level observation and clinical measurement summary table.';

-- -----------------------------------------------------------------------------
-- Gold table: patient risk features
-- -----------------------------------------------------------------------------

create table if not exists GOLD_PATIENT_RISK_FEATURES (
    ehr_patient_id string,
    claim_beneficiary_id string,
    crosswalk_method string,
    age integer,
    gender string,
    race string,
    ethnicity string,
    state string,
    ehr_encounter_count integer,
    ehr_inpatient_encounter_count integer,
    ehr_outpatient_encounter_count integer,
    claim_inpatient_count integer,
    claim_outpatient_count integer,
    claim_carrier_count integer,
    total_claim_count integer,
    total_allowed_amount float,
    total_paid_amount float,
    total_patient_responsibility float,
    avg_allowed_amount_per_claim float,
    avg_paid_amount_per_claim float,
    condition_count integer,
    chronic_condition_count integer,
    has_diabetes number(1,0),
    has_hypertension number(1,0),
    has_copd number(1,0),
    has_chf number(1,0),
    has_ckd number(1,0),
    has_cancer number(1,0),
    has_depression number(1,0),
    medication_count integer,
    unique_medication_count integer,
    observation_count integer,
    avg_systolic_bp float,
    avg_diastolic_bp float,
    avg_bmi float,
    avg_glucose float,
    patient_risk_score float,
    high_risk_flag number(1,0)
)
comment = 'Gold patient-level feature table used for analytics, BI, and ML workflows.';

-- -----------------------------------------------------------------------------
-- Basic validation queries
-- -----------------------------------------------------------------------------

select 'GOLD_PATIENT_MASTER' as table_name, count(*) as row_count
from GOLD_PATIENT_MASTER
union all
select 'GOLD_UTILIZATION_SUMMARY' as table_name, count(*) as row_count
from GOLD_UTILIZATION_SUMMARY
union all
select 'GOLD_CONDITION_SUMMARY' as table_name, count(*) as row_count
from GOLD_CONDITION_SUMMARY
union all
select 'GOLD_MEDICATION_SUMMARY' as table_name, count(*) as row_count
from GOLD_MEDICATION_SUMMARY
union all
select 'GOLD_OBSERVATION_SUMMARY' as table_name, count(*) as row_count
from GOLD_OBSERVATION_SUMMARY
union all
select 'GOLD_PATIENT_RISK_FEATURES' as table_name, count(*) as row_count
from GOLD_PATIENT_RISK_FEATURES;