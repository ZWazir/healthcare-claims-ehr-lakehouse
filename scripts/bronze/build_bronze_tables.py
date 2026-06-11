from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIRS = {
    "synthea": PROJECT_ROOT / "data" / "raw" / "synthea",
    "synpuf": PROJECT_ROOT / "data" / "raw" / "synpuf",
}

BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"


def standardize_column_name(column_name: str) -> str:
    """
    Convert raw source column names into lowercase snake_case names.

    Example:
        "Patient ID" becomes "patient_id"
        "BENE_SEX_IDENT_CD" becomes "bene_sex_ident_cd"
    """
    return (
        column_name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )


def read_raw_csv(file_path: Path) -> pd.DataFrame:
    """
    Read a raw CSV file into a pandas DataFrame.

    dtype=str keeps source values stable in Bronze instead of letting pandas
    guess types too early.
    """
    return pd.read_csv(file_path, dtype=str)


def add_bronze_metadata(
    df: pd.DataFrame,
    source_system: str,
    source_file: str,
) -> pd.DataFrame:
    """
    Add metadata columns that help trace each Bronze record back to its source.
    """
    ingestion_timestamp = datetime.now(timezone.utc).isoformat()

    df = df.copy()
    df["bronze_source_system"] = source_system
    df["bronze_source_file"] = source_file
    df["bronze_ingested_at_utc"] = ingestion_timestamp

    return df


def write_bronze_table(df: pd.DataFrame, source_system: str, table_name: str) -> None:
    """
    Write a Bronze table as a local Parquet file.

    Later, this same design will map cleanly to Databricks Delta tables.
    """
    output_dir = BRONZE_DIR / source_system
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{table_name}.parquet"

    df.to_parquet(output_path, index=False)

    print(f"Wrote Bronze table: {output_path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print()


def ingest_file_to_bronze(source_system: str, file_path: Path) -> None:
    """
    Ingest one raw CSV file into the Bronze layer.
    """
    table_name = file_path.stem

    print("=" * 100)
    print(f"Ingesting {source_system} file: {file_path.name}")
    print("=" * 100)

    raw_df = read_raw_csv(file_path)

    raw_df.columns = [standardize_column_name(col) for col in raw_df.columns]

    bronze_df = add_bronze_metadata(
        df=raw_df,
        source_system=source_system,
        source_file=file_path.name,
    )

    write_bronze_table(
        df=bronze_df,
        source_system=source_system,
        table_name=table_name,
    )


def ingest_all_raw_files() -> None:
    """
    Ingest all raw CSV files from Synthea and SynPUF into Bronze Parquet files.
    """
    for source_system, raw_dir in RAW_DATA_DIRS.items():
        if not raw_dir.exists():
            print(f"Raw directory does not exist: {raw_dir}")
            continue

        csv_files = sorted(raw_dir.glob("*.csv"))

        if not csv_files:
            print(f"No CSV files found for source: {source_system}")
            continue

        for csv_file in csv_files:
            ingest_file_to_bronze(source_system, csv_file)


if __name__ == "__main__":
    ingest_all_raw_files()