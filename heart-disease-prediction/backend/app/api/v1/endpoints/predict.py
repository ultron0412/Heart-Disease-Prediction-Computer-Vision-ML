from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from pydantic import ValidationError

from app.fusion.risk_fusion import fuse_risk
from app.logger import logger
from app.models.clinical.predictor import predict_clinical_risk
from app.models.image.predictor import predict_ecg_image
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.llm_service import build_prediction_explanation

router = APIRouter()

BACKEND_ROOT = Path(__file__).resolve().parents[4]
UPLOAD_DIR = BACKEND_ROOT / "temp_images"
UPLOAD_DIR.mkdir(exist_ok=True)


def _to_dict(model: PredictionRequest) -> dict[str, Any]:
    """Support both Pydantic v1 and v2."""
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude={"symptoms"})
    return model.dict(exclude={"symptoms"})


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: Request,
    data: str | None = Form(None),
    ecg_image: UploadFile | None = File(None),
):
    """Multimodal heart disease prediction endpoint."""
    image_path: Path | None = None
    try:
        if data is not None:
            payload = json.loads(data)
        else:
            payload = await request.json()
            if not isinstance(payload, dict):
                raise HTTPException(status_code=400, detail="JSON body must be an object.")

        parsed = PredictionRequest(**payload)
        clinical_data = _to_dict(parsed)
        clinical_prob = predict_clinical_risk(clinical_data)

        ecg_prob: float | None = None
        if ecg_image:
            safe_name = Path(ecg_image.filename or "ecg_image").name
            filename = f"{uuid.uuid4()}_{safe_name}"
            image_path = UPLOAD_DIR / filename
            with open(image_path, "wb") as file_obj:
                shutil.copyfileobj(ecg_image.file, file_obj)
            ecg_prob = predict_ecg_image(str(image_path))

        fusion_result = fuse_risk(clinical_prob=clinical_prob, ecg_prob=ecg_prob)

        explanation = build_prediction_explanation(payload, fusion_result)

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
    except ValidationError as error:
        raise HTTPException(status_code=422, detail=error.errors()) from error
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {error}") from error
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Prediction request failed")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed due to a server-side error.",
        ) from error
    finally:
        if ecg_image is not None:
            await ecg_image.close()
        if image_path and image_path.exists():
            image_path.unlink(missing_ok=True)
