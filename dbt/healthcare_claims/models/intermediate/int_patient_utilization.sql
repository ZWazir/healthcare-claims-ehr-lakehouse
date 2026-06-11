{{ config(materialized='view') }}

select
    patient.ehr_patient_id,
    patient.claim_beneficiary_id,
    patient.crosswalk_method,
    patient.age,
    patient.gender,
    patient.race,
    patient.ethnicity,
    patient.state,

    utilization.* exclude (
        ehr_patient_id,
        claim_beneficiary_id,
        crosswalk_method
    )

from {{ ref('stg_gold_patient_master') }} as patient

left join {{ ref('stg_gold_utilization_summary') }} as utilization
    on patient.ehr_patient_id = utilization.ehr_patient_id