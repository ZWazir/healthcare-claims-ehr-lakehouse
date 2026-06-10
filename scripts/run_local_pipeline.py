from pathlib import Path
import subprocess
import sys
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[1]


PIPELINE_STEPS = [
    {
        "name": "Build Bronze Layer",
        "script": PROJECT_ROOT / "scripts" / "bronze" / "build_bronze_tables.py",
    },
    {
        "name": "Validate Bronze Layer",
        "script": PROJECT_ROOT / "scripts" / "bronze" / "validate_bronze_tables.py",
    },
    {
        "name": "Build Silver Layer",
        "script": PROJECT_ROOT / "scripts" / "silver" / "build_silver_tables.py",
    },
    {
        "name": "Validate Silver Layer",
        "script": PROJECT_ROOT / "scripts" / "silver" / "validate_silver_tables.py",
    },
    {
        "name": "Build Gold Layer",
        "script": PROJECT_ROOT / "scripts" / "gold" / "build_gold_tables.py",
    },
    {
        "name": "Validate Gold Layer",
        "script": PROJECT_ROOT / "scripts" / "gold" / "validate_gold_tables.py",
    },
]


def run_step(step_name: str, script_path: Path) -> None:
    """
    Run a single pipeline script as a subprocess.

    If the script fails, stop the full pipeline immediately.
    """

    print("\n" + "=" * 80)
    print(f"Running step: {step_name}")
    print(f"Script: {script_path}")
    print("=" * 80)

    if not script_path.exists():
        raise FileNotFoundError(f"Missing pipeline script: {script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline failed during step: {step_name}. "
            f"Script exited with return code {result.returncode}."
        )

    print(f"Completed step: {step_name}")


def main() -> None:
    """
    Run the full local healthcare lakehouse pipeline.

    Pipeline flow:
    Raw data -> Bronze -> Silver -> Gold
    """

    start_time = datetime.now()

    print("\nStarting local healthcare lakehouse pipeline")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Started at: {start_time}")

    for step in PIPELINE_STEPS:
        run_step(step["name"], step["script"])

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 80)
    print("Local healthcare lakehouse pipeline completed successfully")
    print(f"Finished at: {end_time}")
    print(f"Total runtime: {duration}")
    print("=" * 80)


if __name__ == "__main__":
    main()