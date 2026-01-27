import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# ===============================
# Resolve project root safely
# ===============================
BASE_DIR = Path(__file__).resolve().parents[4]

DATA_PATH = BASE_DIR / "data" / "clinical" / "heart.csv"
MODEL_PATH = BASE_DIR / "models" / "clinical" / "heart_ml.pkl"

# ===============================
# Feature selection (NO TARGET)
# ===============================
FEATURE_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach",
    "exang", "oldpeak", "slope", "ca", "thal"
]

def train_model():
    print(f"📂 Loading dataset from: {DATA_PATH}")

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Separate features and target
    X = df[FEATURE_COLUMNS]
    y = df["target"]

    # Train-test split with strong generalization
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
        shuffle=True
    )

    # Regularized Random Forest (ANTI-OVERFITTING)
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=6,
        min_samples_split=10,
        min_samples_leaf=5,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    )

    # Train model
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)

    print("\n📊 Model Evaluation")
    print("----------------------")
    print(f"Accuracy: {accuracy:.2f}\n")

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\n💾 Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
