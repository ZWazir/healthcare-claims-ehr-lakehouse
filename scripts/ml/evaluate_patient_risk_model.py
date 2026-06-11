from pathlib import Path
from datetime import datetime
import json

import torch
import torch.nn as nn


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_DATA_DIR = PROJECT_ROOT / "data" / "ml"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports" / "ml"

MODEL_PATH = MODEL_DIR / "patient_risk_model.pt"
TEST_FEATURES_PATH = ML_DATA_DIR / "test_features.pt"
TEST_LABELS_PATH = ML_DATA_DIR / "test_labels.pt"
EVALUATION_REPORT_PATH = REPORT_DIR / "model_evaluation_report.json"


class PatientRiskModel(nn.Module):
    """
    Same model architecture used during training.

    The saved model artifact stores the trained weights, while this class
    defines the network structure needed to load those weights.
    """

    def __init__(self, input_dim: int):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def validate_required_files() -> None:
    """
    Confirms that the saved model and test tensor files exist.
    """
    required_files = [
        MODEL_PATH,
        TEST_FEATURES_PATH,
        TEST_LABELS_PATH,
    ]

    missing_files = [path for path in required_files if not path.exists()]

    if missing_files:
        missing_file_list = "\n".join(str(path) for path in missing_files)
        raise FileNotFoundError(
            "Missing required files. Train the model first by running "
            "scripts/ml/train_patient_risk_model.py.\n\n"
            f"Missing files:\n{missing_file_list}"
        )


def calculate_binary_metrics(
    labels: torch.Tensor,
    probabilities: torch.Tensor,
) -> dict:
    """
    Calculates binary classification metrics and confusion matrix values.
    """
    predictions = (probabilities >= 0.5).int()
    labels_int = labels.int()

    true_positive = int(((predictions == 1) & (labels_int == 1)).sum().item())
    true_negative = int(((predictions == 0) & (labels_int == 0)).sum().item())
    false_positive = int(((predictions == 1) & (labels_int == 0)).sum().item())
    false_negative = int(((predictions == 0) & (labels_int == 1)).sum().item())

    total = true_positive + true_negative + false_positive + false_negative

    accuracy = (
        (true_positive + true_negative) / total
        if total > 0
        else 0
    )

    precision = (
        true_positive / (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
        "confusion_matrix": {
            "true_positive": true_positive,
            "true_negative": true_negative,
            "false_positive": false_positive,
            "false_negative": false_negative,
        },
    }


def evaluate_saved_model() -> None:
    """
    Loads the saved PyTorch model and evaluates it on the test tensor dataset.
    """
    validate_required_files()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    model_artifact = torch.load(MODEL_PATH)

    input_dim = model_artifact["input_dim"]
    model = PatientRiskModel(input_dim=input_dim)
    model.load_state_dict(model_artifact["model_state_dict"])
    model.eval()

    test_features = torch.load(TEST_FEATURES_PATH)
    test_labels = torch.load(TEST_LABELS_PATH)

    loss_function = nn.BCEWithLogitsLoss()

    with torch.no_grad():
        logits = model(test_features)
        loss = loss_function(logits, test_labels)
        probabilities = torch.sigmoid(logits)
        predictions = (probabilities >= 0.5).int()

    metrics = calculate_binary_metrics(
        labels=test_labels,
        probabilities=probabilities,
    )

    evaluation_report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "model_path": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
        "test_features": str(TEST_FEATURES_PATH.relative_to(PROJECT_ROOT)),
        "test_labels": str(TEST_LABELS_PATH.relative_to(PROJECT_ROOT)),
        "target": model_artifact.get("target", "high_cost_patient_flag"),
        "test_row_count": int(len(test_features)),
        "test_loss": round(float(loss.item()), 6),
        "metrics": metrics,
        "predictions": predictions.view(-1).tolist(),
        "probabilities": [
            round(float(value), 6)
            for value in probabilities.view(-1).tolist()
        ],
        "actual_labels": test_labels.view(-1).int().tolist(),
        "notes": [
            "This evaluation validates the baseline PyTorch workflow.",
            "The current synthetic sample dataset is small, so metrics should not be interpreted as production-grade model performance.",
        ],
    }

    with EVALUATION_REPORT_PATH.open("w", encoding="utf-8") as report_file:
        json.dump(evaluation_report, report_file, indent=2)

    print("Model evaluation complete.")
    print(f"Evaluation report saved to: {EVALUATION_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print("\nEvaluation metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    evaluate_saved_model()