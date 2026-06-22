from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

BASE_DIR = Path(__file__).resolve().parents[4]
MODEL_PATH = BASE_DIR / "models" / "image" / "heart_cnn.keras"


@lru_cache(maxsize=1)
def _load_model() -> Any:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"ECG model file not found: {MODEL_PATH}")
    from tensorflow.keras.models import load_model

    return load_model(MODEL_PATH)


def predict_ecg_image(img_path: str) -> float:
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    from tensorflow.keras.preprocessing import image

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    probability = _load_model().predict(img_array, verbose=0)[0][0]
    return float(probability)
