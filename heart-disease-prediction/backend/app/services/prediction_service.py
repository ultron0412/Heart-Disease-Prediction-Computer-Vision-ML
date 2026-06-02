from __future__ import annotations

from pathlib import Path
from typing import Mapping, TypedDict

from app.fusion.risk_fusion import fuse_risk
from app.models.clinical.predictor import predict_clinical_risk
from app.models.image.predictor import predict_ecg_image


class FusionResult(TypedDict):
    clinical_probability: float
    ecg_probability: float
    clinical_weight: float
    ecg_weight: float
    ecg_used: bool
    model_agreement: float
    final_risk_score: float
    risk_category: str


def predict_heart_disease(
    clinical_data: Mapping[str, int | float | str],
    image_path: str | None = None,
) -> FusionResult:
    """Run clinical prediction, optional ECG prediction, then fusion."""
    if not clinical_data:
        raise ValueError("clinical_data must be a non-empty dictionary.")

    clinical_prob = predict_clinical_risk(dict(clinical_data))

    ecg_prob: float | None = None
    if image_path:
        path = Path(image_path)
        if not path.exists() or not path.is_file():
            raise ValueError(f"ECG image file not found: {image_path}")
        ecg_prob = predict_ecg_image(str(path))

    return fuse_risk(clinical_prob=clinical_prob, ecg_prob=ecg_prob)
