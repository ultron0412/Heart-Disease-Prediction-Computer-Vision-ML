from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Heart Disease Prediction System",
    version="1.0.0",
    description="Backend API for Heart Disease Prediction"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Backend running successfully"}
