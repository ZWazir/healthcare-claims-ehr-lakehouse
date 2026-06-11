{{ config(materialized='view') }}

select
    *
from read_parquet('../../data/gold/gold_utilization_summary.parquet')