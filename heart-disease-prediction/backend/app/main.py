from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router


def _parse_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["http://localhost:5173"]


cors_origins = _parse_cors_origins()

app = FastAPI(
    title="Heart Disease Prediction System",
    version="1.0.0",
    description="Backend API for Heart Disease Prediction",
)

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Backend running successfully"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
