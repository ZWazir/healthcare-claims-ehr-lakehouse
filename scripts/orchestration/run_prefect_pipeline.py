from pathlib import Path
import subprocess
import sys
from typing import Optional

from prefect import flow, task, get_run_logger


PROJECT_ROOT = Path(__file__).resolve().parents[2]


PIPELINE_STEPS = [
    {
        "step_name": "Run local medallion pipeline",
        "script_path": PROJECT_ROOT / "scripts" / "run_local_pipeline.py",
        "description": "Runs the core synthetic EHR + claims Bronze, Silver, Gold, validation, and local pipeline workflow.",
    },
    {
        "step_name": "Build Patient 360 Gold mart",
        "script_path": PROJECT_ROOT / "scripts" / "gold" / "build_patient_360.py",
        "description": "Builds the executive-facing Patient 360 Gold table from synthetic linked Gold outputs.",
    },
    {
        "step_name": "Profile Patient 360 Gold mart",
        "script_path": PROJECT_ROOT / "scripts" / "gold" / "profile_patient_360.py",
        "description": "Creates JSON and Markdown data-quality/profile reports for the Patient 360 mart.",
    },
    {
        "step_name": "Create Tableau-ready exports",
        "script_path": PROJECT_ROOT / "scripts" / "exports" / "create_tableau_exports.py",
        "description": "Exports Gold and Patient 360 tables to CSV files for BI tools such as Tableau Public.",
    },
]


@task(
    name="Validate pipeline script exists",
    retries=1,
    retry_delay_seconds=5,
    log_prints=True,
)
def validate_script_exists(script_path: Path) -> str:
    """
    Confirms that a pipeline script exists before attempting to run it.

    This makes Prefect failures easier to understand because a missing script
    fails with a clear message instead of a lower-level subprocess error.
    """
    logger = get_run_logger()

    if not script_path.exists():
        raise FileNotFoundError(f"Pipeline script not found: {script_path}")

    logger.info(f"Validated script exists: {script_path.relative_to(PROJECT_ROOT)}")
    return str(script_path)


@task(
    name="Run pipeline script",
    retries=0,
    log_prints=True,
)
def run_pipeline_script(
    step_name: str,
    script_path: Path,
    description: Optional[str] = None,
) -> dict:
    """
    Runs one existing project script as a Prefect task.

    Using sys.executable ensures the script runs with the same Python interpreter
    and virtual environment that launched the Prefect flow.
    """
    logger = get_run_logger()

    logger.info(f"Starting step: {step_name}")

    if description:
        logger.info(description)

    completed_process = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if completed_process.stdout:
        logger.info(f"STDOUT for {step_name}:\n{completed_process.stdout}")

    if completed_process.stderr:
        logger.warning(f"STDERR for {step_name}:\n{completed_process.stderr}")

    if completed_process.returncode != 0:
        raise RuntimeError(
            f"Step failed: {step_name}. "
            f"Script: {script_path.relative_to(PROJECT_ROOT)}. "
            f"Return code: {completed_process.returncode}"
        )

    logger.info(f"Completed step: {step_name}")

    return {
        "step_name": step_name,
        "script_path": str(script_path.relative_to(PROJECT_ROOT)),
        "return_code": completed_process.returncode,
        "status": "success",
    }


@flow(
    name="healthcare-claims-ehr-local-lakehouse-pipeline",
    log_prints=True,
)
def healthcare_lakehouse_prefect_flow() -> list[dict]:
    """
    Orchestrates the local healthcare lakehouse workflow with Prefect.

    This flow intentionally focuses on the synthetic linked pipeline because it
    is the main end-to-end patient-level analytics workflow. The real-world
    MIMIC-IV Demo and CMS Claims PUF extension remains documented separately
    because those public datasets are not naturally linkable to Patient 360.
    """
    logger = get_run_logger()

    logger.info("Starting Healthcare Claims & EHR Lakehouse Prefect flow.")
    logger.info(f"Project root: {PROJECT_ROOT}")

    results = []

    for step in PIPELINE_STEPS:
        script_path = step["script_path"]

        validate_script_exists(script_path)

        result = run_pipeline_script(
            step_name=step["step_name"],
            script_path=script_path,
            description=step["description"],
        )

        results.append(result)

    logger.info("Healthcare lakehouse Prefect flow completed successfully.")

    return results


if __name__ == "__main__":
    healthcare_lakehouse_prefect_flow()