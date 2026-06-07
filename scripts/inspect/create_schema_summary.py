from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIRS = {
    "synthea": PROJECT_ROOT / "data" / "raw" / "synthea",
    "synpuf": PROJECT_ROOT / "data" / "raw" / "synpuf",
}

OUTPUT_PATH = PROJECT_ROOT / "docs" / "raw_schema_summary.md"


def summarize_csv_schema(source_name: str, file_path: Path) -> list[dict]:
    """
    Read a CSV file and return one row per column.

    Each row contains source name, file name, column name, and inferred dtype.
    """
    try:
        df = pd.read_csv(file_path, nrows=100)
    except Exception as exc:
        return [
            {
                "source": source_name,
                "file": file_path.name,
                "column": "ERROR",
                "dtype": str(exc),
            }
        ]

    rows = []

    for column_name, dtype in df.dtypes.items():
        rows.append(
            {
                "source": source_name,
                "file": file_path.name,
                "column": column_name,
                "dtype": str(dtype),
            }
        )

    return rows


def build_schema_summary() -> pd.DataFrame:
    """
    Build a combined schema summary for all raw CSV files.
    """
    all_rows = []

    for source_name, source_dir in RAW_DATA_DIRS.items():
        csv_files = sorted(source_dir.glob("*.csv"))

        for csv_file in csv_files:
            all_rows.extend(summarize_csv_schema(source_name, csv_file))

    return pd.DataFrame(all_rows)


def write_markdown_summary(schema_df: pd.DataFrame) -> None:
    """
    Write the schema summary to a Markdown file in the docs folder.
    """
    if schema_df.empty:
        markdown = "# Raw Schema Summary\n\nNo raw CSV files found yet.\n"
    else:
        markdown = "# Raw Schema Summary\n\n"
        markdown += schema_df.to_markdown(index=False)

    OUTPUT_PATH.write_text(markdown, encoding="utf-8")

    print(f"Wrote schema summary to: {OUTPUT_PATH}")


if __name__ == "__main__":
    schema_summary_df = build_schema_summary()
    write_markdown_summary(schema_summary_df)