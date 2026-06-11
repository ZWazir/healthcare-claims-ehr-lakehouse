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
```

Each layer must successfully build and validate before the pipeline continues to the next layer.

---

## Script Location

The local pipeline runner is located at:

```text
scripts/run_local_pipeline.py
```

The layer-specific scripts are organized by medallion layer:

```text
scripts/bronze/
scripts/silver/
scripts/gold/
```

This keeps the project structure clean and makes the pipeline easier to maintain as the project grows.

---

## How to Run the Pipeline

From the project root, run:

```bash
python scripts/run_local_pipeline.py
```

The runner executes each build and validation script in order.

---

## Why This Matters

The local pipeline runner makes the project more realistic and production-oriented.

Rather than manually running individual scripts, the project now has a repeatable orchestration process that can rebuild the full analytics layer from source data.

This demonstrates:

* End-to-end data pipeline orchestration
* Medallion architecture implementation
* Automated validation checkpoints
* Modular script organization
* Local development workflow design
* Readiness for future Databricks or cloud orchestration

---

## Failure Behavior

The runner is designed to stop if any step fails.

For example, if Silver validation fails, the Gold build will not run.

This fail-fast behavior is important because it prevents downstream analytics tables from being built on top of invalid or incomplete upstream data.

---

## Portfolio Relevance

This pipeline runner helps demonstrate that the project is more than a collection of isolated scripts.

It shows an end-to-end healthcare data engineering workflow with:

* Raw data ingestion
* Bronze standardization
* Silver cleaning and transformation
* Gold analytics modeling
* Validation after each layer
* A repeatable local execution process

This mirrors the structure of production-grade data platforms while remaining lightweight enough to run locally.
