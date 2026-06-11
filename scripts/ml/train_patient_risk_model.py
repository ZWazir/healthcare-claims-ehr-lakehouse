from pathlib import Path
from datetime import datetime
import json

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_DATA_DIR = PROJECT_ROOT / "data" / "ml"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports" / "ml"

TRAIN_FEATURES_PATH = ML_DATA_DIR / "train_features.pt"
TRAIN_LABELS_PATH = ML_DATA_DIR / "train_labels.pt"
TEST_FEATURES_PATH = ML_DATA_DIR / "test_features.pt"
TEST_LABELS_PATH = ML_DATA_DIR / "test_labels.pt"

MODEL_PATH = MODEL_DIR / "patient_risk_model.pt"
TRAINING_REPORT_PATH = REPORT_DIR / "training_report.json"

RANDOM_SEED = 42
BATCH_SIZE = 8
LEARNING_RATE = 0.001
EPOCHS = 100


class PatientRiskModel(nn.Module):
    """
    Simple baseline neural network for binary patient risk classification.

    The model predicts whether a patient is likely to be a high-cost patient
    using features generated from the Gold patient risk feature table.
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
    Confirms that the ML tensor files exist before training starts.
    """
    required_files = [
        TRAIN_FEATURES_PATH,
        TRAIN_LABELS_PATH,
        TEST_FEATURES_PATH,
        TEST_LABELS_PATH,
    ]

    missing_files = [path for path in required_files if not path.exists()]

    if missing_files:
        missing_file_list = "\n".join(str(path) for path in missing_files)
        raise FileNotFoundError(
            "Missing required ML tensor files. Run "
            "scripts/ml/create_ml_dataset.py first.\n\n"
            f"Missing files:\n{missing_file_list}"
        )


def load_training_data() -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Loads train/test tensors created by the ML feature engineering step.
    """
    validate_required_files()

    train_features = torch.load(TRAIN_FEATURES_PATH)
    train_labels = torch.load(TRAIN_LABELS_PATH)
    test_features = torch.load(TEST_FEATURES_PATH)
    test_labels = torch.load(TEST_LABELS_PATH)

    return train_features, train_labels, test_features, test_labels


def create_data_loader(
    train_features: torch.Tensor,
    train_labels: torch.Tensor,
) -> DataLoader:
    """
    Wraps training tensors in a PyTorch DataLoader.

    This creates batches for training. The current sample dataset is small,
    but the same pattern scales to larger datasets.
    """
    dataset = TensorDataset(train_features, train_labels)

    return DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )


def calculate_binary_metrics(
    labels: torch.Tensor,
    probabilities: torch.Tensor,
) -> dict:
    """
    Calculates simple binary classification metrics without requiring sklearn.

    This keeps the project lightweight and makes the evaluation logic explicit.
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


def evaluate_model(
    model: PatientRiskModel,
    features: torch.Tensor,
    labels: torch.Tensor,
    loss_function: nn.Module,
) -> dict:
    """
    Evaluates the model on a supplied tensor dataset.
    """
    model.eval()

    with torch.no_grad():
        logits = model(features)
        loss = loss_function(logits, labels)
        probabilities = torch.sigmoid(logits)

    metrics = calculate_binary_metrics(
        labels=labels,
        probabilities=probabilities,
    )

    metrics["loss"] = round(float(loss.item()), 6)

    return metrics


def train_model() -> None:
    """
    Runs the full baseline PyTorch training workflow.

    The script:
    - Loads ML tensors
    - Builds a simple neural network
    - Trains the model
    - Evaluates train and test performance
    - Saves the model artifact
    - Saves a training report
    """
    torch.manual_seed(RANDOM_SEED)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    train_features, train_labels, test_features, test_labels = load_training_data()

    input_dim = train_features.shape[1]

    model = PatientRiskModel(input_dim=input_dim)
    loss_function = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    train_loader = create_data_loader(
        train_features=train_features,
        train_labels=train_labels,
    )

    epoch_losses = []

    print("Training baseline PyTorch patient risk model...")
    print(f"Input feature count: {input_dim}")
    print(f"Training rows: {len(train_features)}")
    print(f"Testing rows: {len(test_features)}")
    print(f"Epochs: {EPOCHS}")

    for epoch in range(EPOCHS):
        model.train()
        batch_losses = []

        for batch_features, batch_labels in train_loader:
            optimizer.zero_grad()

            logits = model(batch_features)
            loss = loss_function(logits, batch_labels)

            loss.backward()
            optimizer.step()

            batch_losses.append(loss.item())

        avg_epoch_loss = sum(batch_losses) / len(batch_losses)
        epoch_losses.append(avg_epoch_loss)

        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch + 1:03d}/{EPOCHS} | Loss: {avg_epoch_loss:.6f}")

    train_metrics = evaluate_model(
        model=model,
        features=train_features,
        labels=train_labels,
        loss_function=loss_function,
    )

    test_metrics = evaluate_model(
        model=model,
        features=test_features,
        labels=test_labels,
        loss_function=loss_function,
    )

    model_artifact = {
        "model_state_dict": model.state_dict(),
        "input_dim": input_dim,
        "model_class": "PatientRiskModel",
        "target": "high_cost_patient_flag",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    torch.save(model_artifact, MODEL_PATH)

    training_report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "model_path": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
        "training_data": {
            "train_features": str(TRAIN_FEATURES_PATH.relative_to(PROJECT_ROOT)),
            "train_labels": str(TRAIN_LABELS_PATH.relative_to(PROJECT_ROOT)),
            "test_features": str(TEST_FEATURES_PATH.relative_to(PROJECT_ROOT)),
            "test_labels": str(TEST_LABELS_PATH.relative_to(PROJECT_ROOT)),
        },
        "model_config": {
            "model_type": "feedforward_neural_network",
            "input_dim": int(input_dim),
            "hidden_layers": [32, 16],
            "output_dim": 1,
            "activation": "ReLU",
            "loss_function": "BCEWithLogitsLoss",
            "optimizer": "Adam",
            "learning_rate": LEARNING_RATE,
            "batch_size": BATCH_SIZE,
            "epochs": EPOCHS,
            "random_seed": RANDOM_SEED,
        },
        "final_train_loss": round(float(epoch_losses[-1]), 6),
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "notes": [
            "This is a baseline model for portfolio demonstration.",
            "The current synthetic sample dataset is intentionally small.",
            "Metrics should be interpreted as workflow validation, not production model performance.",
        ],
    }

    with TRAINING_REPORT_PATH.open("w", encoding="utf-8") as report_file:
        json.dump(training_report, report_file, indent=2)

    print("\nTraining complete.")
    print(f"Model saved to: {MODEL_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Training report saved to: {TRAINING_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print("\nTest metrics:")
    print(json.dumps(test_metrics, indent=2))


if __name__ == "__main__":
    train_model()