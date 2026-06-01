from app.fusion.risk_fusion import fuse_risk
from app.models.clinical.predictor import predict_clinical_risk
from app.models.image.predictor import predict_ecg_image


def predict_heart_disease(clinical_data: dict, image_path: str | None = None) -> dict:
    """Full multimodal heart disease prediction."""
    clinical_prob = predict_clinical_risk(clinical_data)
    ecg_prob = predict_ecg_image(image_path) if image_path else None
    return fuse_risk(clinical_prob, ecg_prob)
