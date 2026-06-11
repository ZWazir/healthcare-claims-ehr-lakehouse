from pathlib import Path
from datetime import datetime
import json

import numpy as np
import pandas as pd
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_RISK_FEATURES_PATH = PROJECT_ROOT / "data" / "gold" / "gold_patient_risk_features.parquet"
ML_OUTPUT_DIR = PROJECT_ROOT / "data" / "ml"
ML_REPORT_DIR = PROJECT_ROOT / "reports" / "ml"

RANDOM_SEED = 42
TEST_SIZE = 0.25

TARGET_COLUMN = "high_cost_patient_flag"

IDENTIFIER_COLUMNS = [
    "ehr_patient_id",
    "claim_beneficiary_id",
    "crosswalk_method",
]

CATEGORICAL_COLUMNS = [
    "gender",
    "race",
    "ethnicity",
    "city",
    "state",
    "county",
    "zip_code",
    "sex_code",
    "race_code",
    "state_code",
    "county_code",
]

EXCLUDE_FROM_FEATURES = [
    TARGET_COLUMN,
    "care_management_candidate_flag",
]


def load_gold_risk_features() -> pd.DataFrame:
    """
    Loads the Gold patient risk feature table.

    This table is the ML source because it already combines patient demographics,
    condition burden, utilization, medications, observations, and reimbursement features.
    """
    if not GOLD_RISK_FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Missing Gold risk feature table: {GOLD_RISK_FEATURES_PATH}. "
            "Run the local pipeline before creating the ML dataset."
        )

    return pd.read_parquet(GOLD_RISK_FEATURES_PATH)


def validate_target_column(df: pd.DataFrame) -> None:
    """
    Confirms that the target column exists and can be used for supervised learning.

    The current target is high_cost_patient_flag, which turns the dataset into a
    binary classification problem.
    """
    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' was not found. "
            "Expected this column in gold_patient_risk_features.parquet."
        )

    unique_values = sorted(df[TARGET_COLUMN].dropna().unique().tolist())

    if len(unique_values) < 2:
        print(
            f"Warning: target column '{TARGET_COLUMN}' has fewer than 2 classes: "
            f"{unique_values}. The dataset will still be created, but model training "
            "may not be meaningful until the sample data is larger."
        )


def build_ml_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """
    Creates the feature matrix and target vector.

    Numeric columns are kept as model features.
    Categorical columns are one-hot encoded.
    Identifier columns are excluded from the model features but preserved in the
    exported patient-level CSV for traceability.
    """
    validate_target_column(df)

    ml_df = df.copy()

    # Keep a traceable patient-level CSV before removing identifiers.
    ML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ml_df.to_csv(ML_OUTPUT_DIR / "patient_risk_features.csv", index=False)

    columns_to_drop = [
        column for column in IDENTIFIER_COLUMNS + EXCLUDE_FROM_FEATURES
        if column in ml_df.columns
    ]

    feature_df = ml_df.drop(columns=columns_to_drop)

    available_categorical_columns = [
        column for column in CATEGORICAL_COLUMNS
        if column in feature_df.columns
    ]

    # One-hot encode categorical fields so the model receives numeric inputs.
    feature_df = pd.get_dummies(
        feature_df,
        columns=available_categorical_columns,
        dummy_na=True,
        dtype=float,
    )

    # Convert booleans to integers and coerce all remaining values to numeric.
    for column in feature_df.columns:
        if feature_df[column].dtype == bool:
            feature_df[column] = feature_df[column].astype(int)
        else:
            feature_df[column] = pd.to_numeric(feature_df[column], errors="coerce")

    # Replace missing feature values with 0 for a simple baseline ML dataset.
    feature_df = feature_df.fillna(0)

    target = ml_df[TARGET_COLUMN].fillna(0).astype(int)

    feature_columns = feature_df.columns.tolist()

    return feature_df, target, feature_columns


def create_train_test_split(
    feature_df: pd.DataFrame,
    target: pd.Series,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Creates a reproducible train/test split.

    This avoids adding an extra scikit-learn dependency while still giving us
    a standard supervised learning split.
    """
    np.random.seed(RANDOM_SEED)

    row_count = len(feature_df)

    if row_count < 2:
        raise ValueError("Need at least 2 rows to create a train/test split.")

    shuffled_indices = np.random.permutation(row_count)
    test_count = max(1, int(row_count * TEST_SIZE))

    test_indices = shuffled_indices[:test_count]
    train_indices = shuffled_indices[test_count:]

    if len(train_indices) == 0:
        train_indices = test_indices
        print(
            "Warning: sample size is very small. Reusing available rows for training."
        )

    x_train = feature_df.iloc[train_indices].to_numpy(dtype=np.float32)
    x_test = feature_df.iloc[test_indices].to_numpy(dtype=np.float32)

    y_train = target.iloc[train_indices].to_numpy(dtype=np.float32)
    y_test = target.iloc[test_indices].to_numpy(dtype=np.float32)

    return x_train, x_test, y_train, y_test


def scale_numeric_features(
    x_train: np.ndarray,
    x_test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Standardizes features using train-set statistics.

    The model should learn from scaled inputs, but the test set must be scaled
    using the train mean and standard deviation to avoid data leakage.
    """
    train_mean = x_train.mean(axis=0)
    train_std = x_train.std(axis=0)

    # Prevent divide-by-zero for constant columns.
    train_std = np.where(train_std == 0, 1, train_std)

    x_train_scaled = (x_train - train_mean) / train_std
    x_test_scaled = (x_test - train_mean) / train_std

    return x_train_scaled, x_test_scaled, train_mean, train_std


def save_torch_tensors(
    x_train: np.ndarray,
    x_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> None:
    """
    Saves the ML dataset as PyTorch tensor files.

    These files will be used by the next milestone when we train a baseline
    patient risk prediction model.
    """
    train_features = torch.tensor(x_train, dtype=torch.float32)
    test_features = torch.tensor(x_test, dtype=torch.float32)

    train_labels = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    test_labels = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    torch.save(train_features, ML_OUTPUT_DIR / "train_features.pt")
    torch.save(train_labels, ML_OUTPUT_DIR / "train_labels.pt")
    torch.save(test_features, ML_OUTPUT_DIR / "test_features.pt")
    torch.save(test_labels, ML_OUTPUT_DIR / "test_labels.pt")


def save_metadata(
    df: pd.DataFrame,
    feature_columns: list[str],
    x_train: np.ndarray,
    x_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    train_mean: np.ndarray,
    train_std: np.ndarray,
) -> None:
    """
    Saves dataset metadata for reproducibility and portfolio documentation.

    This makes it clear what target was used, which features were included,
    how many rows were created, and what files were generated.
    """
    ML_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    target_distribution = (
        df[TARGET_COLUMN]
        .fillna(0)
        .astype(int)
        .value_counts()
        .sort_index()
        .to_dict()
    )

    metadata = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_file": str(GOLD_RISK_FEATURES_PATH.relative_to(PROJECT_ROOT)),
        "target_column": TARGET_COLUMN,
        "target_type": "binary_classification",
        "random_seed": RANDOM_SEED,
        "test_size": TEST_SIZE,
        "source_row_count": int(len(df)),
        "feature_count": int(len(feature_columns)),
        "train_row_count": int(len(x_train)),
        "test_row_count": int(len(x_test)),
        "target_distribution": {
            str(key): int(value)
            for key, value in target_distribution.items()
        },
        "identifier_columns_excluded_from_model": [
            column for column in IDENTIFIER_COLUMNS if column in df.columns
        ],
        "categorical_columns_encoded": [
            column for column in CATEGORICAL_COLUMNS if column in df.columns
        ],
        "excluded_columns": [
            column for column in EXCLUDE_FROM_FEATURES if column in df.columns
        ],
        "feature_columns": feature_columns,
        "outputs": {
            "patient_level_csv": "data/ml/patient_risk_features.csv",
            "train_features": "data/ml/train_features.pt",
            "train_labels": "data/ml/train_labels.pt",
            "test_features": "data/ml/test_features.pt",
            "test_labels": "data/ml/test_labels.pt",
            "metadata": "reports/ml/ml_dataset_metadata.json",
        },
        "scaling": {
            "method": "standardization",
            "mean_source": "training_features_only",
            "std_source": "training_features_only",
            "train_mean": train_mean.tolist(),
            "train_std": train_std.tolist(),
        },
    }

    metadata_path = ML_REPORT_DIR / "ml_dataset_metadata.json"

    with metadata_path.open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)


def create_ml_dataset() -> None:
    """
    Runs the full ML feature engineering workflow.

    This converts the Gold patient risk feature table into:
    - A patient-level CSV
    - Scaled train/test PyTorch tensors
    - Metadata for reproducibility
    """
    ML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ML_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Creating PyTorch-ready ML dataset...")
    print(f"Source: {GOLD_RISK_FEATURES_PATH.relative_to(PROJECT_ROOT)}")

    df = load_gold_risk_features()

    feature_df, target, feature_columns = build_ml_dataframe(df)

    x_train, x_test, y_train, y_test = create_train_test_split(
        feature_df=feature_df,
        target=target,
    )

    x_train_scaled, x_test_scaled, train_mean, train_std = scale_numeric_features(
        x_train=x_train,
        x_test=x_test,
    )

    save_torch_tensors(
        x_train=x_train_scaled,
        x_test=x_test_scaled,
        y_train=y_train,
        y_test=y_test,
    )

    save_metadata(
        df=df,
        feature_columns=feature_columns,
        x_train=x_train_scaled,
        x_test=x_test_scaled,
        y_train=y_train,
        y_test=y_test,
        train_mean=train_mean,
        train_std=train_std,
    )

    print("\nML dataset created successfully.")
    print(f"Rows in source table: {len(df)}")
    print(f"Feature count: {len(feature_columns)}")
    print(f"Train rows: {len(x_train_scaled)}")
    print(f"Test rows: {len(x_test_scaled)}")
    print(f"Target column: {TARGET_COLUMN}")
    print("\nOutputs:")
    print("- data/ml/patient_risk_features.csv")
    print("- data/ml/train_features.pt")
    print("- data/ml/train_labels.pt")
    print("- data/ml/test_features.pt")
    print("- data/ml/test_labels.pt")
    print("- reports/ml/ml_dataset_metadata.json")


if __name__ == "__main__":
    create_ml_dataset()