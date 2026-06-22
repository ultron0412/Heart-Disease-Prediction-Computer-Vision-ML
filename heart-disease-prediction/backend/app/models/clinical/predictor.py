from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from app.models.clinical.features import FEATURE_COLUMNS

BASE_DIR = Path(__file__).resolve().parents[4]
MODEL_PATH = BASE_DIR / "models" / "clinical" / "heart_ml.pkl"


@lru_cache(maxsize=1)
def _load_model() -> Any:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Clinical model file not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def predict_clinical_risk(input_data: dict[str, Any]) -> float:
    missing = [column for column in FEATURE_COLUMNS if column not in input_data]
    if missing:
        raise ValueError(f"Missing clinical features: {missing}")

    features = np.array([[input_data[column] for column in FEATURE_COLUMNS]])
    probability = _load_model().predict_proba(features)[0][1]
    return float(probability)
