from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.predict import router as predict_router
from app.config import settings

api_router = APIRouter(prefix=settings.api_v1_prefix)

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(predict_router, tags=["Prediction"])
