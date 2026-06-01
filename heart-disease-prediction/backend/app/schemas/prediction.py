from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    # Clinical features
    age: int = Field(..., ge=0, le=120, example=45, description="Patient age in years")
    sex: int = Field(..., ge=0, le=1, example=1, description="Sex (0=Female, 1=Male)")
    cp: int = Field(..., ge=0, le=3, example=1, description="Chest pain type (0-3)")
    trestbps: int = Field(..., ge=80, le=200, example=130, description="Resting blood pressure")
    chol: int = Field(..., ge=0, le=400, example=220, description="Serum cholesterol level")
    fbs: int = Field(..., ge=0, le=1, example=0, description="Fasting blood sugar >120 mg/dl (0=No, 1=Yes)")
    restecg: int = Field(..., ge=0, le=2, example=0, description="Resting ECG results (0-2)")
    thalach: int = Field(..., ge=60, le=202, example=150, description="Max heart rate achieved")
    exang: int = Field(..., ge=0, le=1, example=0, description="Exercise induced angina (0=No, 1=Yes)")
    oldpeak: float = Field(..., ge=0, le=6.2, example=3.1, description="ST depression induced by exercise")
    slope: int = Field(..., ge=0, le=2, example=2, description="Slope of ST segment (0-2)")
    ca: int = Field(..., ge=0, le=4, example=0, description="Number of major vessels (0-4)")
    thal: int = Field(..., ge=0, le=3, example=1, description="Thalassemia (0-3)")
    # Optional image
    symptoms: str = Field(default="", example="Chest pain and shortness of breath", description="Optional symptom description")

class PredictionResponse(BaseModel):
    risk_score: float = Field(..., description="Final risk score (0-1)")
    risk_level: str = Field(..., description="Risk category (Low/Moderate/High Risk)")
    explanation: str = Field(..., description="Detailed explanation of the prediction")
    clinical_probability: float = Field(..., description="Clinical model probability")
    ecg_probability: float = Field(..., description="ECG model probability")
    confidence: float = Field(default=0.0, description="Model confidence score")