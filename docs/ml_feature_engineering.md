# ML Feature Engineering Dataset

## Purpose

This document describes the machine learning feature engineering layer for the Healthcare Claims & EHR Lakehouse project.

The goal of this layer is to convert the Gold patient risk feature table into a PyTorch-ready supervised learning dataset. This connects the lakehouse pipeline to downstream predictive modeling and demonstrates how analytics-ready Gold data can support machine learning workflows.

## Source Table

The ML dataset is created from the Gold table:

```text
data/gold/gold_patient_risk_features.parquet
```

This table combines patient-level information from the EHR and claims sides of the project, including:

* Patient demographics
* EHR condition burden
* EHR utilization
* Claims utilization
* Medication summaries
* Observation summaries
* Reimbursement amounts
* Risk and care management flags

## Output Location

The ML-ready files are written to:

```text
data/ml/
```

Generated files:

```text
patient_risk_features.csv
train_features.pt
train_labels.pt
test_features.pt
test_labels.pt
```

A metadata report is written to:

```text
reports/ml/ml_dataset_metadata.json
```

## Script

The feature engineering script is located at:

```text
scripts/ml/create_ml_dataset.py
```

Run it from the project root:

```bash
python scripts/ml/create_ml_dataset.py
```

## Target Variable

The current supervised learning target is:

```text
high_cost_patient_flag
```

This turns the problem into a binary classification task.

The model will eventually learn to predict whether a patient is likely to be a high-cost patient based on demographics, condition burden, utilization, medications, observations, and reimbursement features.

## Feature Engineering Steps

The script performs the following steps:

1. Loads the Gold patient risk feature table.
2. Validates that the target column exists.
3. Preserves a patient-level CSV for inspection and traceability.
4. Removes identifier columns from the model features.
5. Removes target and leakage-prone output columns from the feature matrix.
6. One-hot encodes categorical fields.
7. Converts boolean values to numeric values.
8. Fills missing feature values with zero for the baseline dataset.
9. Creates a reproducible train/test split.
10. Scales numeric features using training-set statistics.
11. Saves PyTorch tensor files.
12. Writes metadata for reproducibility.

## Identifier Columns

The following identifier columns are excluded from the model feature matrix:

```text
ehr_patient_id
claim_beneficiary_id
crosswalk_method
```

These fields are useful for traceability but should not be used directly as model inputs.

## Categorical Columns

The script one-hot encodes categorical fields when they are available, including:

```text
gender
race
ethnicity
city
state
county
zip_code
sex_code
race_code
state_code
county_code
```

One-hot encoding converts categorical values into numeric indicator columns that can be used by a PyTorch model.

## Excluded Columns

The following columns are excluded from model features:

```text
high_cost_patient_flag
care_management_candidate_flag
```

`high_cost_patient_flag` is excluded because it is the target.

`care_management_candidate_flag` is excluded because it is another derived output flag and could introduce target leakage depending on how it was created.

## Train/Test Split

The script creates a reproducible train/test split using:

```text
random_seed = 42
test_size = 0.25
```

This means approximately 25% of rows are reserved for testing.

Because the current project uses a small synthetic sample dataset, the train/test split is primarily intended to demonstrate the workflow. As the sample data grows, this split will become more meaningful for model evaluation.

## Feature Scaling

The script standardizes feature values using the training set only.

The scaling formula is:

```text
scaled_value = (value - training_mean) / training_standard_deviation
```

The test set is scaled using the training-set mean and standard deviation to avoid data leakage.

## PyTorch Outputs

The generated PyTorch tensor files are:

```text
train_features.pt
train_labels.pt
test_features.pt
test_labels.pt
```

These files will be used by the next modeling milestone to train a baseline PyTorch patient risk prediction model.

## Metadata

The metadata report includes:

* Source file path
* Target column
* Target type
* Random seed
* Test size
* Source row count
* Feature count
* Train row count
* Test row count
* Target distribution
* Identifier columns excluded from modeling
* Categorical columns encoded
* Feature column names
* Output file paths
* Scaling information

The metadata file is useful for reproducibility, documentation, and explaining the ML workflow in interviews.

## Business Value

This layer demonstrates how healthcare data engineering can support predictive analytics.

Potential business use cases include:

* Identifying high-cost patients earlier
* Prioritizing care management outreach
* Understanding drivers of utilization
* Supporting population health analytics
* Connecting clinical and claims data for risk modeling

## Portfolio Value

This milestone adds a clear machine learning bridge to the lakehouse project.

It demonstrates:

* Patient-level feature engineering
* Supervised learning dataset preparation
* Train/test splitting
* Feature scaling
* PyTorch tensor creation
* Reproducible ML metadata
* Downstream use of Gold analytics tables

This strengthens the project for Data Engineer, Analytics Engineer, BI Engineer, and entry-level Machine Learning/Data Scientist roles.

## Current Status

This feature engineering layer is part of the 78% to 83% project milestone.

Completion criteria:

* ML feature engineering script exists
* Patient-level ML CSV is created
* Train/test PyTorch tensors are created
* Metadata report is created
* Documentation is added
* Files are committed to Git
