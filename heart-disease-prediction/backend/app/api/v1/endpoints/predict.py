from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.models.clinical.predictor import predict_clinical_risk
from app.models.image.predictor import predict_ecg_image
from app.fusion.risk_fusion import fuse_risk

router = APIRouter()

# Temporary upload directory for ECG images
UPLOAD_DIR = Path("temp_images")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    data: PredictionRequest,
    ecg_image: UploadFile | None = File(None)
):
    """
    Multimodal heart disease prediction endpoint
    """

    try:
        # 1️⃣ Clinical ML prediction (PRIMARY)
        clinical_prob = predict_clinical_risk(data.dict())

        # 2️⃣ ECG CNN prediction (OPTIONAL)
        ecg_prob = 0.0
        image_path = None

        if ecg_image:
            filename = f"{uuid.uuid4()}_{ecg_image.filename}"
            image_path = UPLOAD_DIR / filename

            with open(image_path, "wb") as f:
                shutil.copyfileobj(ecg_image.file, f)

            ecg_prob = predict_ecg_image(str(image_path))

        # 3️⃣ Decision Fusion
        fusion_result = fuse_risk(
            clinical_prob=clinical_prob,
            ecg_prob=ecg_prob
        )

        ### 4️⃣ Human-readable explanation
        explanation = (
            f"Clinical data indicates a {fusion_result['risk_category'].lower()} "
            f"with a clinical risk probability of {fusion_result['clinical_probability']}. "
        )

        if ecg_image:
            explanation += (
                f"ECG image analysis supports this assessment "
                f"(ECG risk probability: {fusion_result['ecg_probability']})."
            )
        else:
            explanation += (
                "ECG image was not provided, so prediction is based on clinical data only."
            )

        return PredictionResponse(
            risk_score=fusion_result["final_risk_score"],
            risk_level=fusion_result["risk_category"],
            explanation=explanation
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
