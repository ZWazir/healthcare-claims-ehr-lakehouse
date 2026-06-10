# Bronze Layer

## Overview

The Bronze layer stores standardized copies of raw source files.

This layer is intentionally light-touch. It preserves the original source data as much as possible while adding metadata that supports lineage, debugging, and downstream processing.

In this project, the Bronze layer is the first structured step in the lakehouse pipeline.

## Input

Raw CSV files are read from:

```text
data/raw/synthea/
data/raw/synpuf/
```

The Synthea folder contains synthetic EHR/FHIR-style clinical data.

The SynPUF folder contains synthetic Medicare-style claims data.

## Output

Bronze files are written as local Parquet files to:

```text
data/bronze/synthea/
data/bronze/synpuf/
```

Local Parquet files are used during development so the project can run on a personal machine before being adapted to Databricks Delta Lake.

## Transformations Applied

The Bronze ingestion script applies a minimal set of transformations:

1. Reads raw CSV files
2. Standardizes column names to lowercase snake_case
3. Adds source metadata columns
4. Writes each table to Parquet

The Bronze layer does not apply major cleaning, deduplication, business logic, or type casting.

Those transformations belong in the Silver layer.

## Metadata Columns

Each Bronze table includes the following metadata columns:

| Column                   | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `bronze_source_system`   | Source system name, such as `synthea` or `synpuf` |
| `bronze_source_file`     | Original raw file name                            |
| `bronze_ingested_at_utc` | UTC timestamp when the file was ingested          |

These fields make it easier to trace each record back to its original source file.

## Design Rationale

Bronze should remain close to the raw source data.

This is useful because healthcare data often contains messy source formats, inconsistent identifiers, unclear date fields, and source-specific coding systems.

By keeping the Bronze layer simple, the pipeline remains easier to debug. If an issue appears in Silver, Gold, dbt, or the machine learning model, the Bronze layer can be used to compare downstream results against the original ingested data.

## Why Parquet Is Used Locally

The local version of the Bronze layer writes Parquet files instead of Delta tables.

Parquet is a columnar file format that works well with pandas, PySpark, DuckDB, and many cloud data platforms.

This keeps the project easy to run locally while still preparing it for a Databricks implementation.

Later, the same Bronze design can be adapted to write Delta Lake tables in Databricks.

## Bronze Ingestion Script

Bronze ingestion is performed with:

```bash
python scripts/bronze/ingest_raw_to_bronze.py
```

The script scans the raw Synthea and SynPUF folders, reads each CSV file, standardizes column names, adds metadata, and writes the output to the Bronze folder.

## Bronze Validation Script

Bronze validation is performed with:

```bash
python scripts/bronze/validate_bronze_tables.py
```

The validation script checks that each Bronze Parquet file:

* Can be read successfully
* Has at least one row
* Contains the required Bronze metadata columns

## Expected Bronze Folder Structure

After ingestion, the Bronze folder should look similar to this:

```text
data/
└── bronze/
    ├── synthea/
    │   ├── patients.parquet
    │   ├── encounters.parquet
    │   ├── conditions.parquet
    │   ├── medications.parquet
    │   └── observations.parquet
    │
    └── synpuf/
        ├── beneficiary_summary.parquet
        ├── inpatient_claims.parquet
        └── outpatient_claims.parquet
```

Additional files may be included depending on which optional raw datasets are loaded.

## Data Quality Expectations

The Bronze layer is expected to meet only basic quality requirements:

* Files should be readable
* Files should contain rows
* Column names should be standardized
* Metadata columns should exist
* Original source values should be preserved as much as possible

More advanced quality checks are deferred to the Silver and dbt layers.

## Current Project Stage

The project currently has a local Bronze ingestion design.

Current status:

```text
Bronze ingestion script created
Bronze validation script created
Bronze documentation created
Raw source files may not be loaded yet
```

Once raw Synthea and SynPUF files are available, the Bronze script can create the first local lakehouse outputs.

## Next Layer

The next step is the Silver layer.

The Silver layer will clean and conform the Bronze data.

Silver transformations will include:

* Type casting
* Date parsing
* Null handling
* Patient identifier standardization
* Claims amount cleanup
* Encounter normalization
* Diagnosis and condition feature preparation
* Preparation for EHR and claims integration

The Silver layer is where source-specific raw data begins to become trusted analytics data.
