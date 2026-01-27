from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    age: int = Field(..., example=45)
    blood_pressure: int = Field(..., example=130)
    cholesterol: int = Field(..., example=220)
    symptoms: str = Field(..., example="Chest pain and shortness of breath")

class PredictionResponse(BaseModel):
    risk_score: float
    risk_level: str
    explanation: str
    confidence: float