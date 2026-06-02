from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict
except ImportError:  # Pydantic v1 compatibility
    ConfigDict = None  # type: ignore[assignment]


if ConfigDict is not None:
    class StrictBaseModel(BaseModel):
        model_config = ConfigDict(extra="forbid")
else:
    class StrictBaseModel(BaseModel):
        class Config:
            extra = "forbid"


class PredictionRequest(StrictBaseModel):

    age: int = Field(..., ge=0, le=120)
    sex: int = Field(..., ge=0, le=1)
    cp: int = Field(..., ge=0, le=3)
    trestbps: int = Field(..., ge=80, le=200)
    chol: int = Field(..., ge=0, le=400)
    fbs: int = Field(..., ge=0, le=1)
    restecg: int = Field(..., ge=0, le=2)
    thalach: int = Field(..., ge=60, le=202)
    exang: int = Field(..., ge=0, le=1)
    oldpeak: float = Field(..., ge=0, le=6.2)
    slope: int = Field(..., ge=0, le=2)
    ca: int = Field(..., ge=0, le=4)
    thal: int = Field(..., ge=0, le=3)
    symptoms: str = Field(default="", max_length=1000)


class PredictionResponse(StrictBaseModel):

    risk_score: float = Field(..., ge=0.0, le=1.0, description="Final risk score (0-1)")
    risk_level: Literal["Low Risk", "Moderate Risk", "High Risk"] = Field(
        ..., description="Risk category"
    )
    explanation: str = Field(..., description="Prediction explanation")
    clinical_probability: float = Field(..., ge=0.0, le=1.0, description="Clinical model probability")
    ecg_probability: float = Field(..., ge=0.0, le=1.0, description="ECG model probability")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Agreement/confidence signal")
    clinical_weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Clinical model fusion weight")
    ecg_weight: float = Field(default=0.0, ge=0.0, le=1.0, description="ECG model fusion weight")
    ecg_used: bool = Field(default=False, description="Whether ECG modality was used")
    model_agreement: float = Field(default=1.0, ge=0.0, le=1.0, description="Agreement between clinical and ECG")
