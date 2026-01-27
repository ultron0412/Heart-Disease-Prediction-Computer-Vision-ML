import joblib
import numpy as np
from pathlib import Path
from app.models.clinical.features import FEATURE_COLUMNS

# =====================================================
# Load model once (efficient)
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[4]
MODEL_PATH = BASE_DIR / "models" / "clinical" / "heart_ml.pkl"

model = joblib.load(MODEL_PATH)

def predict_clinical_risk(input_data: dict) -> float:
    """
    Predict heart disease risk using clinical data.

    Args:
        input_data (dict): clinical feature dictionary

    Returns:
        float: probability of heart disease (0–1)
    """

    # Validate input
    missing = [col for col in FEATURE_COLUMNS if col not in input_data]
    if missing:
        raise ValueError(f"Missing clinical features: {missing}")

    # Arrange features in correct order
    features = np.array([[input_data[col] for col in FEATURE_COLUMNS]])

    # Predict probability
    probability = model.predict_proba(features)[0][1]

    return float(probability)
