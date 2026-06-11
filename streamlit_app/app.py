from pathlib import Path
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOLD_DIR = PROJECT_ROOT / "data" / "gold"


GOLD_TABLES = {
    "Patient Crosswalk": "gold_patient_crosswalk.parquet",
    "Patient Master": "gold_patient_master.parquet",
    "Condition Summary": "gold_condition_summary.parquet",
    "Utilization Summary": "gold_utilization_summary.parquet",
    "Medication Summary": "gold_medication_summary.parquet",
    "Observation Summary": "gold_observation_summary.parquet",
    "Patient Risk Features": "gold_patient_risk_features.parquet",
}


st.set_page_config(
    page_title="Healthcare Claims & EHR Lakehouse",
    page_icon="🏥",
    layout="wide",
)


@st.cache_data
def load_gold_table(file_name: str) -> pd.DataFrame:
    """
    Load a Gold layer Parquet table.

    Streamlit caches this function so the app does not reload the same
    data from disk every time the user interacts with the dashboard.
    """

    file_path = GOLD_DIR / file_name

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_parquet(file_path)


def load_all_gold_tables() -> dict[str, pd.DataFrame]:
    """
    Load all expected Gold tables into a dictionary.

    The dictionary keys are friendly table names used in the dashboard.
    """

    return {
        table_label: load_gold_table(file_name)
        for table_label, file_name in GOLD_TABLES.items()
    }


def get_table_status(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a summary showing whether each Gold table is available.

    This helps users quickly confirm that the local pipeline produced
    the expected analytics outputs.
    """

    status_records = []

    for table_label, file_name in GOLD_TABLES.items():
        df = tables[table_label]
        file_path = GOLD_DIR / file_name

        status_records.append(
            {
                "table_name": table_label,
                "file_name": file_name,
                "exists": file_path.exists(),
                "rows": len(df),
                "columns": len(df.columns),
            }
        )

    return pd.DataFrame(status_records)


def find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """
    Find the first matching column from a list of possible column names.

    This makes the dashboard more resilient if column names change slightly
    during development.
    """

    lower_to_original = {column.lower(): column for column in df.columns}

    for candidate in candidates:
        if candidate.lower() in lower_to_original:
            return lower_to_original[candidate.lower()]

    return None


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Return numeric columns from a DataFrame.
    """

    return df.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """
    Return likely categorical columns from a DataFrame.
    """

    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


def display_table_preview(df: pd.DataFrame, table_name: str) -> None:
    """
    Display a standard preview section for a selected Gold table.
    """

    st.subheader(f"{table_name} Preview")

    if df.empty:
        st.warning(f"No data available for {table_name}. Run the local pipeline first.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", f"{len(df):,}")

    with col2:
        st.metric("Columns", f"{len(df.columns):,}")

    st.dataframe(df.head(50), use_container_width=True)


def display_distribution_chart(df: pd.DataFrame, column: str) -> None:
    """
    Display a simple distribution chart for a selected column.

    For numeric columns with many distinct values, the values are binned.
    For categorical columns, value counts are shown.
    """

    if df.empty or column not in df.columns:
        return

    series = df[column].dropna()

    if series.empty:
        st.info(f"No non-null values available for {column}.")
        return

    if pd.api.types.is_numeric_dtype(series):
        if series.nunique() > 20:
            binned = pd.cut(series, bins=10)
            chart_data = binned.value_counts().sort_index()
            chart_data.index = chart_data.index.astype(str)
        else:
            chart_data = series.value_counts().sort_index()

        st.bar_chart(chart_data)
    else:
        chart_data = series.value_counts().head(20)
        st.bar_chart(chart_data)


def display_overview_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display the main dashboard overview page.
    """

    st.header("Lakehouse Overview")

    table_status = get_table_status(tables)

    patient_master = tables["Patient Master"]
    risk_features = tables["Patient Risk Features"]

    patient_id_col = find_column(
        patient_master,
        ["patient_id", "person_id", "member_id", "beneficiary_id"],
    )

    if patient_id_col:
        patient_count = patient_master[patient_id_col].nunique()
    else:
        patient_count = len(patient_master)

    total_gold_rows = table_status["rows"].sum()
    available_tables = table_status["exists"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Gold Tables Available", f"{available_tables}/{len(GOLD_TABLES)}")

    with col2:
        st.metric("Total Gold Rows", f"{total_gold_rows:,}")

    with col3:
        st.metric("Patients", f"{patient_count:,}")

    with col4:
        st.metric("Risk Feature Rows", f"{len(risk_features):,}")

    st.subheader("Gold Table Status")
    st.dataframe(table_status, use_container_width=True)

    st.subheader("Patient Demographics")

    if patient_master.empty:
        st.warning("Patient master table is empty or missing.")
        return

    demographic_candidates = [
        ["gender", "sex"],
        ["race"],
        ["ethnicity"],
    ]

    available_demo_columns = []

    for candidates in demographic_candidates:
        matched_column = find_column(patient_master, candidates)
        if matched_column:
            available_demo_columns.append(matched_column)

    if not available_demo_columns:
        st.info("No demographic columns found in the patient master table.")
        return

    selected_demo_column = st.selectbox(
        "Select demographic field",
        available_demo_columns,
    )

    display_distribution_chart(patient_master, selected_demo_column)


def display_utilization_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display utilization-focused analytics.
    """

    st.header("Utilization Summary")

    df = tables["Utilization Summary"]
    display_table_preview(df, "Utilization Summary")

    if df.empty:
        return

    numeric_columns = get_numeric_columns(df)

    if not numeric_columns:
        st.info("No numeric utilization columns available for charting.")
        return

    selected_metric = st.selectbox(
        "Select utilization metric",
        numeric_columns,
    )

    patient_id_col = find_column(
        df,
        ["patient_id", "person_id", "member_id", "beneficiary_id"],
    )

    st.subheader(f"Top Records by {selected_metric}")

    if patient_id_col:
        chart_df = (
            df[[patient_id_col, selected_metric]]
            .dropna()
            .sort_values(selected_metric, ascending=False)
            .head(20)
            .set_index(patient_id_col)
        )
        st.bar_chart(chart_df)
    else:
        display_distribution_chart(df, selected_metric)


def display_condition_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display condition-focused analytics.
    """

    st.header("Condition Summary")

    df = tables["Condition Summary"]
    display_table_preview(df, "Condition Summary")

    if df.empty:
        return

    categorical_columns = get_categorical_columns(df)
    numeric_columns = get_numeric_columns(df)

    if categorical_columns:
        st.subheader("Condition Category Distribution")

        selected_category = st.selectbox(
            "Select condition field",
            categorical_columns,
        )

        display_distribution_chart(df, selected_category)

    if numeric_columns:
        st.subheader("Condition Numeric Feature Distribution")

        selected_metric = st.selectbox(
            "Select condition metric",
            numeric_columns,
        )

        display_distribution_chart(df, selected_metric)


def display_medication_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display medication-focused analytics.
    """

    st.header("Medication Summary")

    df = tables["Medication Summary"]
    display_table_preview(df, "Medication Summary")

    if df.empty:
        return

    categorical_columns = get_categorical_columns(df)
    numeric_columns = get_numeric_columns(df)

    if categorical_columns:
        st.subheader("Medication Category Distribution")

        selected_category = st.selectbox(
            "Select medication field",
            categorical_columns,
        )

        display_distribution_chart(df, selected_category)

    if numeric_columns:
        st.subheader("Medication Numeric Feature Distribution")

        selected_metric = st.selectbox(
            "Select medication metric",
            numeric_columns,
        )

        display_distribution_chart(df, selected_metric)


def display_observation_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display observation-focused analytics.
    """

    st.header("Observation Summary")

    df = tables["Observation Summary"]
    display_table_preview(df, "Observation Summary")

    if df.empty:
        return

    categorical_columns = get_categorical_columns(df)
    numeric_columns = get_numeric_columns(df)

    if categorical_columns:
        st.subheader("Observation Category Distribution")

        selected_category = st.selectbox(
            "Select observation field",
            categorical_columns,
        )

        display_distribution_chart(df, selected_category)

    if numeric_columns:
        st.subheader("Observation Numeric Feature Distribution")

        selected_metric = st.selectbox(
            "Select observation metric",
            numeric_columns,
        )

        display_distribution_chart(df, selected_metric)


def display_risk_features_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display patient risk feature analytics.
    """

    st.header("Patient Risk Features")

    df = tables["Patient Risk Features"]
    display_table_preview(df, "Patient Risk Features")

    if df.empty:
        return

    numeric_columns = get_numeric_columns(df)

    if not numeric_columns:
        st.info("No numeric risk feature columns available for charting.")
        return

    selected_metric = st.selectbox(
        "Select risk feature",
        numeric_columns,
    )

    st.subheader(f"Distribution of {selected_metric}")
    display_distribution_chart(df, selected_metric)

    patient_id_col = find_column(
        df,
        ["patient_id", "person_id", "member_id", "beneficiary_id"],
    )

    if patient_id_col:
        st.subheader(f"Top Records by {selected_metric}")

        top_records = (
            df[[patient_id_col, selected_metric]]
            .dropna()
            .sort_values(selected_metric, ascending=False)
            .head(20)
            .set_index(patient_id_col)
        )

        st.bar_chart(top_records)


def display_data_explorer_page(tables: dict[str, pd.DataFrame]) -> None:
    """
    Display a flexible data explorer for any Gold table.
    """

    st.header("Gold Data Explorer")

    selected_table = st.selectbox(
        "Select Gold table",
        list(tables.keys()),
    )

    df = tables[selected_table]

    display_table_preview(df, selected_table)

    if df.empty:
        return

    st.subheader("Column Details")

    column_profile = pd.DataFrame(
        {
            "column_name": df.columns,
            "dtype": [str(df[column].dtype) for column in df.columns],
            "null_count": [int(df[column].isna().sum()) for column in df.columns],
            "null_percent": [
                round(float(df[column].isna().mean() * 100), 2)
                for column in df.columns
            ],
            "unique_values": [int(df[column].nunique()) for column in df.columns],
        }
    )

    st.dataframe(column_profile, use_container_width=True)

    st.subheader("Explore a Column")

    selected_column = st.selectbox(
        "Select column",
        df.columns.tolist(),
    )

    display_distribution_chart(df, selected_column)


def main() -> None:
    """
    Run the Streamlit dashboard application.
    """

    st.title("Healthcare Claims & EHR Lakehouse")
    st.caption(
        "Local medallion architecture dashboard built from Gold analytics Parquet tables."
    )

    tables = load_all_gold_tables()

    page = st.sidebar.radio(
        "Dashboard Page",
        [
            "Overview",
            "Utilization",
            "Conditions",
            "Medications",
            "Observations",
            "Patient Risk Features",
            "Gold Data Explorer",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Location")
    st.sidebar.code(str(GOLD_DIR))

    if page == "Overview":
        display_overview_page(tables)
    elif page == "Utilization":
        display_utilization_page(tables)
    elif page == "Conditions":
        display_condition_page(tables)
    elif page == "Medications":
        display_medication_page(tables)
    elif page == "Observations":
        display_observation_page(tables)
    elif page == "Patient Risk Features":
        display_risk_features_page(tables)
    elif page == "Gold Data Explorer":
        display_data_explorer_page(tables)


if __name__ == "__main__":
    main()