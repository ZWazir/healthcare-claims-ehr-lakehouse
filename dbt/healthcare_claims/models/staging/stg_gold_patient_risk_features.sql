{{ config(materialized='view') }}

select
    *
from read_parquet('../../data/gold/gold_patient_risk_features.parquet')