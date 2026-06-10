# Local Pipeline Runner

## Project: Healthcare Claims & EHR Lakehouse

This project includes a local pipeline runner that executes the full medallion architecture workflow from raw synthetic healthcare data through validated Gold analytics tables.

The local runner is designed to simulate the orchestration pattern that would later be handled by tools such as Databricks Workflows, Airflow, Prefect, or Dagster in a production environment.

---

## Pipeline Flow

The local pipeline runs the following sequence:

```text
Raw Data
  ↓
Bronze Build
  ↓
Bronze Validation
  ↓
Silver Build
  ↓
Silver Validation
  ↓
Gold Build
  ↓
Gold Validation