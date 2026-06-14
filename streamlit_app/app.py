from pathlib import Path
import json

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
REPORTS_DIR = PROJECT_ROOT / "reports"
REAL_WORLD_REPORTS_DIR = REPORTS_DIR / "real_world"
REAL_WORLD_BRONZE_DIR = PROJECT_ROOT / "data" / "real_world" / "bronze"
MIMIC_BRONZE_DIR = REAL_WORLD_BRONZE_DIR / "mimic_demo"
CMS_PUF_BRONZE_DIR = REAL_WORLD_BRONZE_DIR / "cms_claims_puf"

st.set_page_config(
    page_title="Healthcare Claims & EHR Lakehouse",
    page_icon="🏥",
    layout="wide",
)


# ---------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------

@st.cache_data
def read_parquet_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    return pd.read_parquet(path)


@st.cache_data
def read_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def read_markdown_if_exists(path: Path) -> str:
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def format_number(value) -> str:
    if pd.isna(value):
        return "0"

    if isinstance(value, float):
        return f"{value:,.2f}"

    return f"{value:,}"


def count_report_tables(report: dict | None) -> int:
    """
    Count ingested/profiled tables from a report JSON using flexible key handling.

    This keeps the Streamlit dashboard resilient if different ingestion/profile
    scripts use slightly different metadata keys.
    """
    if not report:
        return 0

    list_or_dict_keys = [
        "tables_ingested",
        "ingested_tables",
        "tables",
        "table_metadata",
        "outputs",
        "files",
    ]

    for key in list_or_dict_keys:
        value = report.get(key)

        if isinstance(value, list):
            return len(value)

        if isinstance(value, dict):
            return len(value)

    count_keys = [
        "tables_ingested_count",
        "ingested_table_count",
        "table_count",
        "profiled_table_count",
        "expected_table_count",
    ]

    for key in count_keys:
        value = report.get(key)

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        if isinstance(value, str) and value.isdigit():
            return int(value)

    return 0


def show_missing_file_warning(label: str, path: Path) -> None:
    st.warning(
        f"{label} was not found at `{path.relative_to(PROJECT_ROOT)}`. "
        "Run the relevant pipeline script to generate it."
    )


def find_column(df: pd.DataFrame, possible_names: list[str]) -> str | None:
    lower_to_original = {col.lower(): col for col in df.columns}

    for name in possible_names:
        if name.lower() in lower_to_original:
            return lower_to_original[name.lower()]

    return None


def find_numeric_columns(
    df: pd.DataFrame,
    include_terms: list[str],
    exclude_terms: list[str] | None = None,
) -> list[str]:
    exclude_terms = exclude_terms or []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    matched = []

    for col in numeric_cols:
        col_lower = col.lower()

        include_match = any(term in col_lower for term in include_terms)
        exclude_match = any(term in col_lower for term in exclude_terms)

        if include_match and not exclude_match:
            matched.append(col)

    return matched


def show_dataframe_section(title: str, df: pd.DataFrame, max_rows: int = 25) -> None:
    st.subheader(title)

    if df.empty:
        st.info("No data available for this section yet.")
        return

    st.dataframe(df.head(max_rows), use_container_width=True)

def count_bronze_parquet_tables(directory: Path) -> int:
    """
    Count actual ingested Bronze Parquet tables in a real-world data folder.

    This is more reliable for dashboard KPI cards than depending on one specific
    JSON report key name.
    """
    if not directory.exists():
        return 0

    return len(list(directory.glob("*.parquet")))


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

patient_master = read_parquet_if_exists(GOLD_DIR / "gold_patient_master.parquet")
utilization_summary = read_parquet_if_exists(GOLD_DIR / "gold_utilization_summary.parquet")
condition_summary = read_parquet_if_exists(GOLD_DIR / "gold_condition_summary.parquet")
patient_risk_features = read_parquet_if_exists(GOLD_DIR / "gold_patient_risk_features.parquet")
patient_360 = read_parquet_if_exists(GOLD_DIR / "gold_patient_360.parquet")

patient_360_report = read_json_if_exists(REPORTS_DIR / "gold" / "patient_360_build_report.json")
mimic_ingestion_report = read_json_if_exists(REAL_WORLD_REPORTS_DIR / "mimic_demo_ingestion_report.json")
mimic_profile_markdown = read_markdown_if_exists(REAL_WORLD_REPORTS_DIR / "mimic_demo_profile_report.md")
cms_ingestion_report = read_json_if_exists(REAL_WORLD_REPORTS_DIR / "cms_claims_puf_ingestion_report.json")
cms_profile_markdown = read_markdown_if_exists(REAL_WORLD_REPORTS_DIR / "cms_claims_puf_profile_report.md")
real_world_validation_markdown = read_markdown_if_exists(
    REAL_WORLD_REPORTS_DIR / "real_world_bronze_validation_report.md"
)


# ---------------------------------------------------------------------
# App header
# ---------------------------------------------------------------------

st.title("Healthcare Claims & EHR Lakehouse")
st.caption(
    "Portfolio project demonstrating a healthcare medallion architecture with "
    "synthetic linked EHR + claims data, BI-ready marts, ML-ready features, "
    "Snowflake/dbt integration, Databricks migration artifacts, and public-data ingestion extensions."
)

overview_tab, patient_360_tab, real_world_tab = st.tabs(
    [
        "Synthetic Lakehouse Dashboard",
        "Patient 360",
        "Real-World Public Data Extension",
    ]
)


# ---------------------------------------------------------------------
# Synthetic Lakehouse Dashboard
# ---------------------------------------------------------------------

with overview_tab:
    st.header("Synthetic Linked EHR + Claims Lakehouse")

    st.write(
        """
        This dashboard summarizes the main synthetic linked pipeline. The synthetic data
        remains the core end-to-end patient-level analytics workflow because those EHR
        and claims records are intentionally linkable through the project crosswalk.
        """
    )

    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

    with metric_col_1:
        st.metric("Patients", format_number(len(patient_master)))

    with metric_col_2:
        st.metric("Utilization Rows", format_number(len(utilization_summary)))

    with metric_col_3:
        st.metric("Condition Rows", format_number(len(condition_summary)))

    with metric_col_4:
        st.metric("ML Feature Rows", format_number(len(patient_risk_features)))

    st.divider()

    chart_col_1, chart_col_2 = st.columns(2)

    with chart_col_1:
        st.subheader("Patient Demographics")

        if patient_master.empty:
            show_missing_file_warning(
                "Gold patient master",
                GOLD_DIR / "gold_patient_master.parquet",
            )
        else:
            gender_col = find_column(patient_master, ["gender", "sex", "sex_code"])
            age_col = find_column(patient_master, ["age"])

            if gender_col:
                gender_counts = (
                    patient_master[gender_col]
                    .fillna("Unknown")
                    .value_counts()
                    .reset_index()
                )
                gender_counts.columns = [gender_col, "patient_count"]
                st.bar_chart(gender_counts, x=gender_col, y="patient_count")

            if age_col:
                st.write("Age summary")
                st.dataframe(
                    patient_master[[age_col]].describe().T,
                    use_container_width=True,
                )

    with chart_col_2:
        st.subheader("Utilization Overview")

        if utilization_summary.empty:
            show_missing_file_warning(
                "Gold utilization summary",
                GOLD_DIR / "gold_utilization_summary.parquet",
            )
        else:
            utilization_cols = find_numeric_columns(
                utilization_summary,
                include_terms=["encounter_count", "claim_count", "admission_count", "visit_count"],
                exclude_terms=["condition", "medication", "observation"],
            )

            if utilization_cols:
                utilization_totals = (
                    utilization_summary[utilization_cols]
                    .fillna(0)
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                utilization_totals.columns = ["metric", "value"]
                st.bar_chart(utilization_totals, x="metric", y="value")
            else:
                st.info("No utilization count columns found.")

    st.divider()

    show_dataframe_section("Gold Patient Master Preview", patient_master)
    show_dataframe_section("Gold Patient Risk Features Preview", patient_risk_features)


# ---------------------------------------------------------------------
# Patient 360
# ---------------------------------------------------------------------

with patient_360_tab:
    st.header("Patient 360 Executive View")

    st.write(
        """
        Patient 360 combines demographics, utilization, conditions, risk features,
        and dashboard-friendly segments into a single Gold mart. This is designed
        for executive review, care-management storytelling, and BI consumption.
        """
    )

    if patient_360.empty:
        show_missing_file_warning(
            "Gold Patient 360",
            GOLD_DIR / "gold_patient_360.parquet",
        )
    else:
        metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

        with metric_col_1:
            st.metric("Patient 360 Rows", format_number(len(patient_360)))

        with metric_col_2:
            st.metric("Patient 360 Columns", format_number(len(patient_360.columns)))

        with metric_col_3:
            priority_col = find_column(patient_360, ["care_management_priority"])

            if priority_col:
                high_priority_count = int(
                    (patient_360[priority_col] == "High priority").sum()
                )
            else:
                high_priority_count = 0

            st.metric("High Priority Patients", format_number(high_priority_count))

        with metric_col_4:
            cost_col = find_column(patient_360, ["patient_360_total_cost_proxy"])

            if cost_col:
                total_cost_proxy = patient_360[cost_col].fillna(0).sum()
            else:
                total_cost_proxy = 0

            st.metric("Total Cost Proxy", format_number(float(total_cost_proxy)))

        st.divider()

        filter_col_1, filter_col_2, filter_col_3 = st.columns(3)

        filtered_patient_360 = patient_360.copy()

        with filter_col_1:
            priority_col = find_column(filtered_patient_360, ["care_management_priority"])

            if priority_col:
                priority_options = sorted(
                    filtered_patient_360[priority_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_priorities = st.multiselect(
                    "Care management priority",
                    priority_options,
                    default=priority_options,
                )

                filtered_patient_360 = filtered_patient_360[
                    filtered_patient_360[priority_col].astype(str).isin(selected_priorities)
                ]

        with filter_col_2:
            utilization_segment_col = find_column(filtered_patient_360, ["utilization_segment"])

            if utilization_segment_col:
                utilization_options = sorted(
                    filtered_patient_360[utilization_segment_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_utilization_segments = st.multiselect(
                    "Utilization segment",
                    utilization_options,
                    default=utilization_options,
                )

                filtered_patient_360 = filtered_patient_360[
                    filtered_patient_360[utilization_segment_col]
                    .astype(str)
                    .isin(selected_utilization_segments)
                ]

        with filter_col_3:
            cost_segment_col = find_column(filtered_patient_360, ["cost_segment"])

            if cost_segment_col:
                cost_options = sorted(
                    filtered_patient_360[cost_segment_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_cost_segments = st.multiselect(
                    "Cost segment",
                    cost_options,
                    default=cost_options,
                )

                filtered_patient_360 = filtered_patient_360[
                    filtered_patient_360[cost_segment_col].astype(str).isin(selected_cost_segments)
                ]

        st.divider()

        chart_col_1, chart_col_2 = st.columns(2)

        with chart_col_1:
            st.subheader("Care Management Priority")

            priority_col = find_column(filtered_patient_360, ["care_management_priority"])

            if priority_col:
                priority_counts = (
                    filtered_patient_360[priority_col]
                    .fillna("Unknown")
                    .value_counts()
                    .reset_index()
                )
                priority_counts.columns = ["priority", "patient_count"]
                st.bar_chart(priority_counts, x="priority", y="patient_count")
            else:
                st.info("No care management priority column found.")

        with chart_col_2:
            st.subheader("Cost Segment")

            cost_segment_col = find_column(filtered_patient_360, ["cost_segment"])

            if cost_segment_col:
                cost_segment_counts = (
                    filtered_patient_360[cost_segment_col]
                    .fillna("Unknown")
                    .value_counts()
                    .reset_index()
                )
                cost_segment_counts.columns = ["cost_segment", "patient_count"]
                st.bar_chart(cost_segment_counts, x="cost_segment", y="patient_count")
            else:
                st.info("No cost segment column found.")

        st.divider()

        st.subheader("Patient 360 Build Summary")

        if patient_360_report:
            summary_cols = st.columns(3)

            with summary_cols[0]:
                st.metric(
                    "Output Rows",
                    format_number(patient_360_report.get("output_rows", 0)),
                )

            with summary_cols[1]:
                st.metric(
                    "Output Columns",
                    format_number(patient_360_report.get("output_columns", 0)),
                )

            with summary_cols[2]:
                source_tables = patient_360_report.get("source_tables", {})
                available_sources = sum(
                    1 for source in source_tables.values() if source.get("available")
                )
                st.metric("Source Tables Used", format_number(available_sources))

            with st.expander("View Patient 360 build report JSON"):
                st.json(patient_360_report)
        else:
            st.info("Patient 360 build report not found yet.")

        st.divider()

        show_dataframe_section("Patient 360 Preview", filtered_patient_360, max_rows=50)


# ---------------------------------------------------------------------
# Real-world public data extension
# ---------------------------------------------------------------------

with real_world_tab:
    st.header("Real-World Public Data Ingestion Extension")

    st.write(
        """
        This section documents the v1.1 public-data extension. MIMIC-IV Demo
        and CMS Basic Stand Alone Medicare Claims PUF are intentionally treated
        as separate public ingestion tracks. They are not joined into the synthetic
        Patient 360 pipeline because they are not naturally linkable.
        """
    )

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)

    with metric_col_1:
        mimic_table_count = count_bronze_parquet_tables(MIMIC_BRONZE_DIR)
        st.metric("MIMIC Tables Ingested", format_number(mimic_table_count))

    with metric_col_2:
        cms_table_count = count_bronze_parquet_tables(CMS_PUF_BRONZE_DIR)
        st.metric("CMS PUF Tables Ingested", format_number(cms_table_count))

    with metric_col_3:
        validation_available = bool(real_world_validation_markdown)
        st.metric("Validation Report Available", "Yes" if validation_available else "No")

    st.divider()

    mimic_tab, cms_tab, validation_tab = st.tabs(
        [
            "MIMIC-IV Demo",
            "CMS Claims PUF",
            "Bronze Validation",
        ]
    )

    with mimic_tab:
        st.subheader("MIMIC-IV Demo Ingestion Summary")

        if mimic_ingestion_report:
            st.json(mimic_ingestion_report)
        else:
            show_missing_file_warning(
                "MIMIC ingestion report",
                REAL_WORLD_REPORTS_DIR / "mimic_demo_ingestion_report.json",
            )

        st.subheader("MIMIC-IV Demo Profile Report")

        if mimic_profile_markdown:
            st.markdown(mimic_profile_markdown)
        else:
            show_missing_file_warning(
                "MIMIC profile report",
                REAL_WORLD_REPORTS_DIR / "mimic_demo_profile_report.md",
            )

    with cms_tab:
        st.subheader("CMS Claims PUF Ingestion Summary")

        if cms_ingestion_report:
            st.json(cms_ingestion_report)
        else:
            show_missing_file_warning(
                "CMS Claims PUF ingestion report",
                REAL_WORLD_REPORTS_DIR / "cms_claims_puf_ingestion_report.json",
            )

        st.subheader("CMS Claims PUF Profile Report")

        if cms_profile_markdown:
            st.markdown(cms_profile_markdown)
        else:
            show_missing_file_warning(
                "CMS Claims PUF profile report",
                REAL_WORLD_REPORTS_DIR / "cms_claims_puf_profile_report.md",
            )

    with validation_tab:
        st.subheader("Real-World Bronze Validation")

        if real_world_validation_markdown:
            st.markdown(real_world_validation_markdown)
        else:
            show_missing_file_warning(
                "Real-world Bronze validation report",
                REAL_WORLD_REPORTS_DIR / "real_world_bronze_validation_report.md",
            )