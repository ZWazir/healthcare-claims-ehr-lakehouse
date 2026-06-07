# Data Sources

## Synthea Synthetic EHR Data

Synthea is an open-source synthetic patient generator that creates realistic but fictional patient records.

For this project, Synthea represents the EHR/FHIR side of the healthcare ecosystem.

Relevant entities:
- Patients
- Encounters
- Conditions
- Medications
- Observations
- Procedures
- Immunizations
- Care plans

These tables represent clinical activity such as diagnoses, lab observations, procedures, and medication history.

## CMS Medicare DE-SynPUF Claims Data

CMS DE-SynPUF is a synthetic Medicare claims dataset designed to mimic the structure of real Medicare claims data while protecting beneficiary privacy.

For this project, SynPUF represents the claims and payment side of the healthcare ecosystem.

Relevant entities:
- Beneficiary summary
- Inpatient claims
- Outpatient claims
- Carrier claims
- Prescription drug events

These tables represent utilization, submitted claims, allowed amounts, provider services, and prescription drug activity.

## Integration Note

Synthea and SynPUF are separate synthetic datasets and do not share real patient identifiers.

This project creates a synthetic patient crosswalk to connect EHR-style clinical records with claims-style payment records. The crosswalk is used only for portfolio demonstration purposes.

## Important Limitation

Both datasets are synthetic. They are appropriate for software development, analytics engineering, modeling practice, and portfolio demonstration.

They should not be used to draw real-world clinical or policy conclusions.