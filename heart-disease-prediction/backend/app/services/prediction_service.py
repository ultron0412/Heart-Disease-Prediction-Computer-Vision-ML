from app.models.clinical.predictor import predict_clinical_risk
from app.models.image.predictor import predict_ecg_image
from app.fusion.risk_fusion import fuse_risk

def predict_heart_disease(
    clinical_data: dict,
    image_path: str | None = None
) -> dict:
    """
    Full multimodal heart disease prediction
    """

    # 1. Clinical prediction
    clinical_prob = predict_clinical_risk(clinical_data)

    # 2. ECG prediction (optional)
    ecg_prob = 0.0
    if image_path:
        ecg_prob = predict_ecg_image(image_path)

    # 3. Fusion
    result = fuse_risk(clinical_prob, ecg_prob)

    return result
