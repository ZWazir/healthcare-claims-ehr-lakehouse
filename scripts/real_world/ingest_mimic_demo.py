from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd


# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "real_world" / "raw" / "mimic_demo"
BRONZE_DIR = PROJECT_ROOT / "data" / "real_world" / "bronze" / "mimic_demo"
REPORTS_DIR = PROJECT_ROOT / "reports" / "real_world"

BRONZE_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# MIMIC-IV demo tables selected for first ingestion milestone
# =============================================================================

MIMIC_TABLES = {
    "patients": RAW_DIR / "hosp" / "patients.csv.gz",
    "admissions": RAW_DIR / "hosp" / "admissions.csv.gz",
    "diagnoses_icd": RAW_DIR / "hosp" / "diagnoses_icd.csv.gz",
    "procedures_icd": RAW_DIR / "hosp" / "procedures_icd.csv.gz",
    "d_icd_diagnoses": RAW_DIR / "hosp" / "d_icd_diagnoses.csv.gz",
    "d_icd_procedures": RAW_DIR / "hosp" / "d_icd_procedures.csv.gz",
    "labevents": RAW_DIR / "hosp" / "labevents.csv.gz",
    "prescriptions": RAW_DIR / "hosp" / "prescriptions.csv.gz",
    "icustays": RAW_DIR / "icu" / "icustays.csv.gz",
}


# =============================================================================
# Helper functions
# =============================================================================

def read_mimic_csv(file_path: Path) -> pd.DataFrame:
    """
    Reads a compressed MIMIC-IV demo CSV file.

    dtype=str keeps the first Bronze layer close to the raw source files.
    This avoids accidental type conversion issues during ingestion.
    """

    return pd.read_csv(file_path, compression="gzip", dtype=str, low_memory=False)


def write_bronze_table(df: pd.DataFrame, table_name: str) -> Path:
    """
    Writes a MIMIC table to the real-world Bronze layer as Parquet.
    """

    output_path = BRONZE_DIR / f"{table_name}.parquet"
    df.to_parquet(output_path, index=False)
    return output_path


def build_table_metadata(table_name: str, source_path: Path, output_path: Path, df: pd.DataFrame) -> dict:
    """
    Creates a metadata record for each ingested table.
    """

    return {
        "table_name": table_name,
        "source_path": str(source_path.relative_to(PROJECT_ROOT)),
        "bronze_path": str(output_path.relative_to(PROJECT_ROOT)),
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
    }


# =============================================================================
# Main ingestion workflow
# =============================================================================

def main() -> None:
    print("Starting MIMIC-IV demo Bronze ingestion...")

    ingestion_report = {
        "pipeline_name": "mimic_demo_bronze_ingestion",
        "dataset": "MIMIC-IV Clinical Database Demo",
        "dataset_version": "2.2",
        "ingestion_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "raw_directory": str(RAW_DIR.relative_to(PROJECT_ROOT)),
        "bronze_directory": str(BRONZE_DIR.relative_to(PROJECT_ROOT)),
        "tables": [],
        "missing_files": [],
    }

    for table_name, source_path in MIMIC_TABLES.items():
        print("\n" + "=" * 80)
        print(f"Ingesting table: {table_name}")
        print("=" * 80)

        if not source_path.exists():
            print(f"Missing source file: {source_path}")
            ingestion_report["missing_files"].append(str(source_path.relative_to(PROJECT_ROOT)))
            continue

        df = read_mimic_csv(source_path)
        output_path = write_bronze_table(df, table_name)

        table_metadata = build_table_metadata(
            table_name=table_name,
            source_path=source_path,
            output_path=output_path,
            df=df,
        )

        ingestion_report["tables"].append(table_metadata)

        print(f"Rows: {table_metadata['row_count']}")
        print(f"Columns: {table_metadata['column_count']}")
        print(f"Bronze output: {table_metadata['bronze_path']}")

    report_path = REPORTS_DIR / "mimic_demo_ingestion_report.json"

    with open(report_path, "w") as f:
        json.dump(ingestion_report, f, indent=2)

    print("\n" + "=" * 80)
    print("MIMIC-IV demo Bronze ingestion complete.")
    print("=" * 80)
    print(f"Tables ingested: {len(ingestion_report['tables'])}")
    print(f"Missing files: {len(ingestion_report['missing_files'])}")
    print(f"Report written to: {report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()