# Real-World Public Healthcare Data Sources

## Purpose

Version 1.1 of this project adds a real-world/public data ingestion extension to the existing healthcare claims and EHR lakehouse.

The original v1.0 pipeline remains the main fully reproducible end-to-end demo because it uses linked synthetic EHR and claims data. The v1.1 extension adds real public healthcare data sources to demonstrate that the project can ingest external healthcare datasets with realistic schemas and documentation requirements.

This extension is intentionally separate from the synthetic linked EHR + claims pipeline.

## Design Decision

The real-world EHR and claims datasets used in v1.1 are not naturally linkable.

This project will not attempt to join MIMIC-IV demo patients to CMS Medicare Claims Public Use File records. Doing so would be analytically incorrect because these datasets come from different sources, different populations, and different de-identification processes.

Instead, the project story is:

1. Fully reproducible synthetic linked EHR + claims lakehouse
2. Real public EHR ingestion using MIMIC-IV Clinical Database Demo
3. Real public Medicare claims ingestion using CMS Basic Stand Alone Medicare Claims Public Use Files

This preserves the integrity of the original end-to-end workflow while adding a realistic public-data ingestion layer.

---

## Source 1: MIMIC-IV Clinical Database Demo

### Source Name

MIMIC-IV Clinical Database Demo

### Official Publisher

PhysioNet / MIT Laboratory for Computational Physiology

### Official Source Page

https://www.physionet.org/content/mimic-iv-demo/2.2/

### Verified Version

Version 2.2

### Published Date

January 31, 2023

### Dataset Type

Real deidentified electronic health record demo dataset.

### Description

The MIMIC-IV Clinical Database Demo is an openly available demo subset of the MIMIC-IV Clinical Database. It contains deidentified electronic health record data from patients admitted to Beth Israel Deaconess Medical Center.

The demo contains a subset of 100 patients and is intended to help researchers understand the structure and contents of MIMIC-IV before requesting access to the full credentialed dataset.

### Format

CSV files.

### Schema Notes

The demo shares the same schema and structure as the corresponding version of MIMIC-IV. MIMIC-IV is a relational clinical database organized into hospital and ICU modules.

The demo includes tables from the MIMIC-IV structure, including patient, admission, transfer, diagnosis, procedure, lab, medication, and ICU-related tables.

### Access Notes

The MIMIC-IV demo is openly accessible through PhysioNet, subject to the dataset license and usage terms.

The full MIMIC-IV Clinical Database may require credentialing, training, and a data use agreement. This project starts with the demo because it is smaller, easier to use for a public portfolio project, and appropriate for reproducible ingestion examples.

### Intended Use in This Project

This dataset will be used to demonstrate ingestion of real public EHR-style data into the lakehouse structure.

Planned path:

```text
data/real_world/raw/mimic_demo/
        |
        v
data/real_world/bronze/mimic_demo/
        |
        v
reports/real_world/mimic_demo_profile_report.md