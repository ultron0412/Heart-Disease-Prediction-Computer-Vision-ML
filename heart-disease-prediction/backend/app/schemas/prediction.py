from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=0, le=120, example=45)
    sex: int = Field(..., ge=0, le=1, example=1)
    cp: int = Field(..., ge=0, le=3, example=1)
    trestbps: int = Field(..., ge=80, le=200, example=130)
    chol: int = Field(..., ge=0, le=400, example=220)
    fbs: int = Field(..., ge=0, le=1, example=0)
    restecg: int = Field(..., ge=0, le=2, example=0)
    thalach: int = Field(..., ge=60, le=202, example=150)
    exang: int = Field(..., ge=0, le=1, example=0)
    oldpeak: float = Field(..., ge=0, le=6.2, example=3.1)
    slope: int = Field(..., ge=0, le=2, example=2)
    ca: int = Field(..., ge=0, le=4, example=0)
    thal: int = Field(..., ge=0, le=3, example=1)
    symptoms: str = Field(default="", example="Chest pain and shortness of breath")


class PredictionResponse(BaseModel):
    risk_score: float = Field(..., description="Final risk score (0-1)")
    risk_level: str = Field(..., description="Risk category")
    explanation: str = Field(..., description="Prediction explanation")
    clinical_probability: float = Field(..., description="Clinical model probability")
    ecg_probability: float = Field(..., description="ECG model probability")
    confidence: float = Field(default=0.0, description="Agreement/confidence signal")
    clinical_weight: float = Field(default=1.0, description="Clinical model fusion weight")
    ecg_weight: float = Field(default=0.0, description="ECG model fusion weight")
    ecg_used: bool = Field(default=False, description="Whether ECG modality was used")
    model_agreement: float = Field(default=1.0, description="Agreement between clinical and ECG")
