from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
TABLEAU_EXPORT_DIR = PROJECT_ROOT / "data" / "tableau_exports"
REPORT_DIR = PROJECT_ROOT / "reports" / "tableau_exports"
MANIFEST_PATH = REPORT_DIR / "tableau_export_manifest.json"


EXPORT_SPECS = [
    {
        "name": "patient_master",
        "source_candidates": [
            GOLD_DIR / "gold_patient_master.parquet",
            GOLD_DIR / "patient_master.parquet",
        ],
        "export_path": TABLEAU_EXPORT_DIR / "patient_master_export.csv",
    },
    {
        "name": "utilization_summary",
        "source_candidates": [
            GOLD_DIR / "gold_utilization_summary.parquet",
            GOLD_DIR / "utilization_summary.parquet",
        ],
        "export_path": TABLEAU_EXPORT_DIR / "utilization_summary_export.csv",
    },
    {
        "name": "condition_summary",
        "source_candidates": [
            GOLD_DIR / "gold_condition_summary.parquet",
            GOLD_DIR / "condition_summary.parquet",
        ],
        "export_path": TABLEAU_EXPORT_DIR / "condition_summary_export.csv",
    },
    {
        "name": "patient_risk_features",
        "source_candidates": [
            GOLD_DIR / "gold_patient_risk_features.parquet",
            GOLD_DIR / "patient_risk_features.parquet",
        ],
        "export_path": TABLEAU_EXPORT_DIR / "patient_risk_features_export.csv",
    },
    {
        "name": "patient_360",
        "source_candidates": [
            GOLD_DIR / "gold_patient_360.parquet",
            GOLD_DIR / "patient_360.parquet",
        ],
        "export_path": TABLEAU_EXPORT_DIR / "patient_360_export.csv",
    },
]


def find_existing_source(source_candidates: list[Path]) -> Path:
    """
    Return the first existing source file from a list of possible parquet paths.
    This keeps the export script resilient if gold marts use slightly different names.
    """
    for path in source_candidates:
        if path.exists():
            return path

    candidate_list = "\n".join(f"  - {path}" for path in source_candidates)
    raise FileNotFoundError(
        "Could not find any source parquet file from these candidates:\n"
        f"{candidate_list}"
    )


def export_parquet_to_csv(source_path: Path, export_path: Path) -> dict:
    """
    Read one Gold parquet mart and export it as a Tableau-ready CSV.
    Returns metadata used in the export manifest.
    """
    df = pd.read_parquet(source_path)

    export_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(export_path, index=False)

    return {
        "source_path": str(source_path.relative_to(PROJECT_ROOT)),
        "export_path": str(export_path.relative_to(PROJECT_ROOT)),
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
    }


def main() -> None:
    TABLEAU_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Tableau-ready CSV exports from Gold analytics marts.",
        "exports": {},
    }

    print("Creating Tableau exports...")

    for spec in EXPORT_SPECS:
        export_name = spec["name"]
        source_path = find_existing_source(spec["source_candidates"])
        export_path = spec["export_path"]

        print(f"\nExporting {export_name}")
        print(f"Source: {source_path}")
        print(f"Output: {export_path}")

        export_metadata = export_parquet_to_csv(source_path, export_path)
        manifest["exports"][export_name] = export_metadata

        print(
            f"Rows: {export_metadata['row_count']} | "
            f"Columns: {export_metadata['column_count']}"
        )

    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\nTableau export manifest written to:")
    print(MANIFEST_PATH)
    print("\nTableau exports complete.")


if __name__ == "__main__":
    main()