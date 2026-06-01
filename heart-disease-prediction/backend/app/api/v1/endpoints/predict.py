from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from app.fusion.risk_fusion import fuse_risk
from app.models.clinical.predictor import predict_clinical_risk
from app.models.image.predictor import predict_ecg_image
from app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter()

UPLOAD_DIR = Path("temp_images")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: Request,
    data: str | None = Form(None),
    ecg_image: UploadFile | None = File(None),
):
    """Multimodal heart disease prediction endpoint."""
    try:
        if data is not None:
            payload = json.loads(data)
        else:
            payload = await request.json()

        parsed = PredictionRequest(**payload)
        clinical_data = parsed.model_dump(exclude={"symptoms"})
        clinical_prob = predict_clinical_risk(clinical_data)

        ecg_prob: float | None = None
        if ecg_image:
            filename = f"{uuid.uuid4()}_{ecg_image.filename}"
            image_path = UPLOAD_DIR / filename
            with open(image_path, "wb") as file_obj:
                shutil.copyfileobj(ecg_image.file, file_obj)
            ecg_prob = predict_ecg_image(str(image_path))

        fusion_result = fuse_risk(clinical_prob=clinical_prob, ecg_prob=ecg_prob)

        explanation = (
            f"Clinical model probability is {fusion_result['clinical_probability']:.3f}. "
            f"Final risk category is {fusion_result['risk_category']}. "
        )
        if fusion_result["ecg_used"]:
            explanation += (
                f"ECG probability is {fusion_result['ecg_probability']:.3f} and contributes "
                f"with dynamic weight {fusion_result['ecg_weight']:.3f}."
            )
        else:
            explanation += "No ECG image was provided, so prediction is clinical-only."

        return PredictionResponse(
            risk_score=fusion_result["final_risk_score"],
            risk_level=fusion_result["risk_category"],
            explanation=explanation,
            clinical_probability=fusion_result["clinical_probability"],
            ecg_probability=fusion_result["ecg_probability"],
            confidence=fusion_result["model_agreement"],
            clinical_weight=fusion_result["clinical_weight"],
            ecg_weight=fusion_result["ecg_weight"],
            ecg_used=fusion_result["ecg_used"],
            model_agreement=fusion_result["model_agreement"],
        )
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {error}") from error
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
