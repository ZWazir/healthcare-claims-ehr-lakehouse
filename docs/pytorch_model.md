# PyTorch Patient Risk Model

## Overview

This project includes a baseline PyTorch model that predicts a patient-level risk or utilization target from the machine learning feature dataset generated from the Gold layer.

The purpose of this model is to demonstrate how the healthcare lakehouse supports downstream predictive modeling. The current dataset is intentionally small and synthetic, so the model metrics should be interpreted as workflow validation rather than production-grade predictive performance.

## Model Objective

The baseline model uses patient-level features created from the Gold analytics layer to predict a binary patient risk target.

The model demonstrates the following workflow:

1. Load ML-ready tensors generated from Gold patient risk features.
2. Train a simple PyTorch neural network.
3. Evaluate model performance on a held-out test set.
4. Save a trained model artifact.
5. Generate JSON reports for training and evaluation metrics.

## Input Data

The model uses ML-ready tensor files created by:

```bash
python scripts/ml/create_ml_dataset.py
```

Input files:

```text
data/ml/train_features.pt
data/ml/train_labels.pt
data/ml/test_features.pt
data/ml/test_labels.pt
```

The source feature dataset is:

```text
data/ml/patient_risk_features.csv
```

The ML dataset is derived from Gold patient-level analytics outputs, including utilization, condition, medication, observation, and patient risk summary features.

## Model Scripts

Training script:

```text
scripts/ml/train_patient_risk_model.py
```

Evaluation script:

```text
scripts/ml/evaluate_patient_risk_model.py
```

## Model Architecture

The baseline model is a simple feedforward neural network built in PyTorch.

The architecture includes:

```text
Input layer: patient-level feature vector
Hidden layer 1: fully connected layer
Activation: ReLU
Hidden layer 2: fully connected layer
Activation: ReLU
Output layer: single binary classification logit
```

The model is trained using binary classification loss.

## Training Workflow

To train the model, run:

```bash
python scripts/ml/train_patient_risk_model.py
```

This script performs the following steps:

1. Loads training and test tensors from `data/ml/`.
2. Initializes a baseline PyTorch neural network.
3. Trains the model using a binary classification objective.
4. Calculates test-set metrics.
5. Saves the trained model artifact.
6. Writes a training report to `reports/ml/`.

Expected outputs:

```text
models/patient_risk_model.pt
reports/ml/training_report.json
```

## Evaluation Workflow

To evaluate the model, run:

```bash
python scripts/ml/evaluate_patient_risk_model.py
```

This script performs the following steps:

1. Loads the saved PyTorch model artifact.
2. Loads the test feature and label tensors.
3. Generates predictions.
4. Calculates classification metrics.
5. Writes an evaluation report to `reports/ml/`.

Expected output:

```text
reports/ml/model_evaluation_report.json
```

## Evaluation Metrics

The baseline evaluation report includes:

```text
Accuracy
Precision
Recall
F1 score
Confusion matrix
```

Because the current synthetic dataset is very small, the metrics should not be interpreted as a reliable measure of real-world model performance.

For example, with only one test record, the model may achieve high accuracy if the single test case is classified correctly, while precision, recall, and F1 may remain zero if there are no positive labels or no positive predictions.

## Current Limitation

The current project uses a small synthetic sample dataset with only a few patients. This is intentional for local development and portfolio demonstration.

The model is useful for validating the pipeline pattern:

```text
Raw synthetic healthcare data
        ↓
Bronze ingestion
        ↓
Silver cleaning
        ↓
Gold analytics tables
        ↓
ML feature engineering
        ↓
PyTorch tensors
        ↓
Model training and evaluation
```

The model is not intended to represent production-level clinical or financial prediction performance.

## Portfolio Value

This PyTorch milestone strengthens the project by showing that the lakehouse supports both analytics and machine learning use cases.

It demonstrates:

* End-to-end data engineering from raw data to ML-ready features
* Patient-level feature engineering
* Tensor generation for PyTorch
* Baseline neural network training
* Model evaluation and metric reporting
* Saved model artifacts
* Clear separation between data pipeline, BI outputs, and ML outputs

## Future Improvements

Future versions of this model could include:

1. Larger synthetic or public healthcare datasets.
2. More realistic risk labels.
3. Better class balance.
4. Cross-validation.
5. Hyperparameter tuning.
6. Feature importance analysis.
7. Model comparison against logistic regression, random forest, and gradient boosting baselines.
8. Integration with Snowflake or Databricks feature tables.
9. MLflow experiment tracking.
10. Deployment through a Streamlit risk scoring interface.
