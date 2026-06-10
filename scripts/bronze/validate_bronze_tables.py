from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"


REQUIRED_METADATA_COLUMNS = {
    "bronze_source_system",
    "bronze_source_file",
    "bronze_ingested_at_utc",
}


def validate_bronze_file(file_path: Path) -> dict:
    """
    Validate a single Bronze Parquet file.

    Checks whether the file can be read, has rows, and includes required metadata.
    """
    result = {
        "file": str(file_path.relative_to(PROJECT_ROOT)),
        "status": "pass",
        "row_count": 0,
        "column_count": 0,
        "missing_metadata_columns": [],
        "error": "",
    }

    try:
        df = pd.read_parquet(file_path)
    except Exception as exc:
        result["status"] = "fail"
        result["error"] = str(exc)
        return result

    result["row_count"] = len(df)
    result["column_count"] = len(df.columns)

    missing_metadata = REQUIRED_METADATA_COLUMNS - set(df.columns)

    if missing_metadata:
        result["status"] = "fail"
        result["missing_metadata_columns"] = sorted(missing_metadata)

    if len(df) == 0:
        result["status"] = "fail"
        result["error"] = "File has zero rows."

    return result


def validate_all_bronze_tables() -> pd.DataFrame:
    """
    Validate all Bronze Parquet files.
    """
    parquet_files = sorted(BRONZE_DIR.glob("*/*.parquet"))

    if not parquet_files:
        print("No Bronze Parquet files found.")
        return pd.DataFrame()

    results = [validate_bronze_file(file_path) for file_path in parquet_files]

    return pd.DataFrame(results)


def main() -> None:
    validation_df = validate_all_bronze_tables()

    if validation_df.empty:
        return

    print(validation_df.to_string(index=False))

    failed_count = (validation_df["status"] == "fail").sum()

    if failed_count > 0:
        raise SystemExit(f"Bronze validation failed for {failed_count} file(s).")

    print("\nAll Bronze tables passed validation.")


if __name__ == "__main__":
    main()