{{ config(materialized='view') }}

select
    *
from read_parquet('../../data/gold/gold_condition_summary.parquet')