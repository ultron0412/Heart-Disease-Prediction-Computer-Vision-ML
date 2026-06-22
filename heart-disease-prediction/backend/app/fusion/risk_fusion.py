from __future__ import annotations

"""Decision-level fusion for clinical + ECG predictions."""

from typing import Literal, TypedDict

RiskCategory = Literal["Low Risk", "Moderate Risk", "High Risk"]


class FusionResult(TypedDict):
    clinical_probability: float
    ecg_probability: float
    clinical_weight: float
    ecg_weight: float
    ecg_used: bool
    model_agreement: float
    final_risk_score: float
    risk_category: RiskCategory


def _risk_category(final_risk: float) -> RiskCategory:
    if final_risk < 0.30:
        return "Low Risk"
    if final_risk < 0.60:
        return "Moderate Risk"
    return "High Risk"


def fuse_risk(clinical_prob: float, ecg_prob: float | None = None) -> FusionResult:
    """
    If ECG is unavailable, use the clinical model only.
    If ECG is available, adapt fusion weight by ECG certainty.
    """
    clinical_prob = max(0.0, min(1.0, float(clinical_prob)))
    has_ecg = ecg_prob is not None

    if not has_ecg:
        final_risk = clinical_prob
        clinical_weight = 1.0
        ecg_weight = 0.0
        ecg_probability = 0.0
    else:
        assert ecg_prob is not None
        ecg_probability = max(0.0, min(1.0, float(ecg_prob)))
        ecg_certainty = abs(ecg_probability - 0.5) * 2.0
        ecg_weight = 0.15 + (0.35 * ecg_certainty)
        clinical_weight = 1.0 - ecg_weight
        final_risk = (clinical_weight * clinical_prob) + (ecg_weight * ecg_probability)

    category = _risk_category(final_risk)
    agreement = 1.0 if not has_ecg else 1.0 - abs(clinical_prob - ecg_probability)

    return {
        "clinical_probability": round(clinical_prob, 3),
        "ecg_probability": round(ecg_probability, 3),
        "clinical_weight": round(clinical_weight, 3),
        "ecg_weight": round(ecg_weight, 3),
        "ecg_used": has_ecg,
        "model_agreement": round(max(0.0, min(1.0, agreement)), 3),
        "final_risk_score": round(final_risk, 3),
        "risk_category": category,
    }
