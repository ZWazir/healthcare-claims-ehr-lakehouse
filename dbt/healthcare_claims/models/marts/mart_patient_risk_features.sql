{{ config(materialized='table') }}

select
    risk.ehr_patient_id,
    risk.claim_beneficiary_id,
    risk.crosswalk_method,

    patient.age,
    patient.gender,
    patient.race,
    patient.ethnicity,
    patient.state,

    risk.* exclude (
        ehr_patient_id,
        claim_beneficiary_id,
        crosswalk_method
    )

from {{ ref('stg_gold_patient_risk_features') }} as risk

left join {{ ref('stg_gold_patient_master') }} as patient
    on risk.ehr_patient_id = patient.ehr_patient_id