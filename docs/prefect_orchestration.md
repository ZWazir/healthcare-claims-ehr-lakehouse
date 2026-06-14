# Prefect Orchestration

## Purpose

This project includes a Prefect orchestration layer to demonstrate how the local healthcare lakehouse pipeline can be managed as a repeatable workflow.

The Prefect flow turns the project from a collection of standalone scripts into an orchestrated data pipeline with clear task boundaries, logging, step-level execution, and failure visibility.

## Orchestration File

The main Prefect orchestration script is:

```text
scripts/orchestration/run_prefect_pipeline.py
```

## Flow Name

```text
healthcare-claims-ehr-local-lakehouse-pipeline
```

## What the Flow Runs

The Prefect flow currently orchestrates the main synthetic linked pipeline and Patient 360 BI outputs.

Pipeline steps:

1. Run local medallion pipeline
2. Build Patient 360 Gold mart
3. Profile Patient 360 Gold mart
4. Create Tableau-ready exports

## Scripts Orchestrated

```text
scripts/run_local_pipeline.py
scripts/gold/build_patient_360.py
scripts/gold/profile_patient_360.py
scripts/exports/create_tableau_exports.py
```

## Why This Scope Was Chosen

The first Prefect implementation intentionally focuses on the synthetic linked pipeline because this is the main end-to-end patient-level analytics workflow.

The real-world public data extension remains documented separately because MIMIC-IV Demo and CMS Claims PUF are separate public ingestion tracks and are not naturally linkable to the synthetic Patient 360 mart.

This design keeps the orchestration layer accurate, explainable, and portfolio-friendly.

## How to Run the Prefect Flow Locally

From the project root, activate the virtual environment and run:

```bash
python scripts/orchestration/run_prefect_pipeline.py
```

The flow will execute the pipeline scripts in sequence and log each step.

## Current Orchestration Flow

```text
Prefect Flow
    |
    v
Run Local Pipeline
    |
    v
Build Patient 360 Gold Mart
    |
    v
Profile Patient 360 Gold Mart
    |
    v
Create Tableau-Ready Exports
```

## Outputs Refreshed by the Flow

The Prefect flow refreshes the core synthetic lakehouse outputs, including:

```text
data/bronze/
data/silver/
data/gold/
data/gold/gold_patient_360.parquet
reports/gold/patient_360_build_report.json
reports/gold/patient_360_profile_report.json
reports/gold/patient_360_profile_report.md
data/tableau_exports/
reports/tableau_exports/tableau_export_manifest.json
```

## Portfolio Value

This milestone demonstrates orchestration and production-readiness concepts without overcomplicating the project.

It shows that the pipeline can be:

- Re-run consistently
- Organized into clear workflow steps
- Logged at the task level
- Extended later with schedules, deployments, retries, notifications, and cloud execution
- Presented as a realistic analytics engineering workflow

## Future Enhancements

Potential future improvements include:

- Adding a Prefect deployment
- Adding a scheduled pipeline run
- Adding separate real-world ingestion flows
- Adding flow-level JSON run reports
- Adding notifications for failed runs
- Running Prefect against Databricks, Snowflake, or cloud storage

## Recruiter-Facing Talking Point

I added Prefect orchestration to show how the local lakehouse workflow could be managed as a repeatable production-style pipeline.

Rather than manually running each script one by one, the Prefect flow coordinates the medallion pipeline, Patient 360 mart build, Patient 360 profiling, and Tableau export generation. This demonstrates workflow orchestration, task-level logging, and a clear path toward scheduled production jobs.
