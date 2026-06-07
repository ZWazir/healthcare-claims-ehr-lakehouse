from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIRS = {
    "synthea": PROJECT_ROOT / "data" / "raw" / "synthea",
    "synpuf": PROJECT_ROOT / "data" / "raw" / "synpuf",
}


def inspect_csv_file(file_path: Path, sample_rows: int = 5) -> None:
    """
    Print basic information about a CSV file.

    This helps us understand the schema before building Bronze tables.
    """
    print("=" * 100)
    print(f"File: {file_path}")
    print("=" * 100)

    try:
        df = pd.read_csv(file_path, nrows=sample_rows)
    except Exception as exc:
        print(f"Could not read file: {exc}")
        return

    print(f"Columns ({len(df.columns)}):")
    for col in df.columns:
        print(f"  - {col}")

    print("\nSample rows:")
    print(df.head(sample_rows))

    print("\nInferred dtypes:")
    print(df.dtypes)

    print()


def inspect_raw_data() -> None:
    """
    Inspect all CSV files in the raw Synthea and SynPUF folders.
    """
    for source_name, source_dir in RAW_DATA_DIRS.items():
        print("\n")
        print("#" * 100)
        print(f"Inspecting source: {source_name}")
        print(f"Directory: {source_dir}")
        print("#" * 100)

        if not source_dir.exists():
            print(f"Directory does not exist: {source_dir}")
            continue

        csv_files = sorted(source_dir.glob("*.csv"))

        if not csv_files:
            print("No CSV files found.")
            continue

        for csv_file in csv_files:
            inspect_csv_file(csv_file)


if __name__ == "__main__":
    inspect_raw_data()