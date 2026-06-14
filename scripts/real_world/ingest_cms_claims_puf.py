from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd


# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "real_world" / "raw" / "cms_claims_puf"
BRONZE_DIR = PROJECT_ROOT / "data" / "real_world" / "bronze" / "cms_claims_puf"
REPORTS_DIR = PROJECT_ROOT / "reports" / "real_world"

BRONZE_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# CMS Basic Stand Alone Medicare Claims PUF files selected for first milestone
# =============================================================================

CMS_CLAIMS_FILES = {
    "inpatient_claims": {
        "source_path": RAW_DIR / "inpatient" / "2008_BSA_Inpatient_Claims_PUF.csv",
        "claim_type": "inpatient",
        "source_year": "2008",
        "dataset_name": "CMS Basic Stand Alone Medicare Claims PUF - Inpatient Claims",
    }
}


# =============================================================================
# Helper functions
# =============================================================================

def read_cms_claims_csv(file_path: Path) -> pd.DataFrame:
    """
    Reads a CMS Basic Stand Alone Claims PUF CSV file.

    dtype=str keeps this Bronze layer close to the raw source file and avoids
    accidental type conversion issues during ingestion.
    """

    return pd.read_csv(file_path, dtype=str, low_memory=False)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names for easier downstream analysis.

    Bronze keeps the raw values, but light column-name normalization makes
    the data easier to inspect and profile.
    """

    df = df.copy()

    df.columns = [
        column.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        for column in df.columns
    ]

    return df


def add_ingestion_metadata(
    df: pd.DataFrame,
    source_file: Path,
    claim_type: str,
    source_year: str,
    ingestion_timestamp: str,
) -> pd.DataFrame:
    """
    Adds simple ingestion metadata columns.

    These fields make it clear where the Bronze records came from without
    pretending they are linkable to the MIMIC demo data.
    """

    df = df.copy()

    df["_source_file"] = str(source_file.name)
    df["_claim_type"] = claim_type
    df["_source_year"] = source_year
    df["_ingestion_timestamp_utc"] = ingestion_timestamp

    return df


def write_bronze_table(df: pd.DataFrame, table_name: str) -> Path:
    """
    Writes the CMS claims table to the real-world Bronze layer as Parquet.
    """

    output_path = BRONZE_DIR / f"{table_name}.parquet"
    df.to_parquet(output_path, index=False)
    return output_path


def build_table_metadata(
    table_name: str,
    dataset_name: str,
    claim_type: str,
    source_year: str,
    source_path: Path,
    output_path: Path,
    df: pd.DataFrame,
) -> dict:
    """
    Creates a metadata record for each ingested CMS claims table.
    """

    return {
        "table_name": table_name,
        "dataset_name": dataset_name,
        "claim_type": claim_type,
        "source_year": source_year,
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
    print("Starting CMS Claims PUF Bronze ingestion...")

    ingestion_timestamp = datetime.now(timezone.utc).isoformat()

    ingestion_report = {
        "pipeline_name": "cms_claims_puf_bronze_ingestion",
        "dataset": "CMS Basic Stand Alone Medicare Claims Public Use Files",
        "ingestion_timestamp_utc": ingestion_timestamp,
        "raw_directory": str(RAW_DIR.relative_to(PROJECT_ROOT)),
        "bronze_directory": str(BRONZE_DIR.relative_to(PROJECT_ROOT)),
        "tables": [],
        "missing_files": [],
    }

    for table_name, file_config in CMS_CLAIMS_FILES.items():
        print("\n" + "=" * 80)
        print(f"Ingesting table: {table_name}")
        print("=" * 80)

        source_path = file_config["source_path"]

        if not source_path.exists():
            print(f"Missing source file: {source_path}")
            ingestion_report["missing_files"].append(str(source_path.relative_to(PROJECT_ROOT)))
            continue

        df = read_cms_claims_csv(source_path)
        df = standardize_column_names(df)
        df = add_ingestion_metadata(
            df=df,
            source_file=source_path,
            claim_type=file_config["claim_type"],
            source_year=file_config["source_year"],
            ingestion_timestamp=ingestion_timestamp,
        )

        output_path = write_bronze_table(df, table_name)

        table_metadata = build_table_metadata(
            table_name=table_name,
            dataset_name=file_config["dataset_name"],
            claim_type=file_config["claim_type"],
            source_year=file_config["source_year"],
            source_path=source_path,
            output_path=output_path,
            df=df,
        )

        ingestion_report["tables"].append(table_metadata)

        print(f"Rows: {table_metadata['row_count']}")
        print(f"Columns: {table_metadata['column_count']}")
        print(f"Bronze output: {table_metadata['bronze_path']}")

    report_path = REPORTS_DIR / "cms_claims_puf_ingestion_report.json"

    with open(report_path, "w") as f:
        json.dump(ingestion_report, f, indent=2)

    print("\n" + "=" * 80)
    print("CMS Claims PUF Bronze ingestion complete.")
    print("=" * 80)
    print(f"Tables ingested: {len(ingestion_report['tables'])}")
    print(f"Missing files: {len(ingestion_report['missing_files'])}")
    print(f"Report written to: {report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()