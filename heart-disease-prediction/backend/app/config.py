from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_csv(value: str | None, default: list[str]) -> list[str]:
    if value is None:
        return default
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or default


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    debug: bool
    api_v1_prefix: str
    cors_origins: list[str]
    llm_enabled: bool
    llm_base_url: str
    llm_model: str | None
    llm_api_key: str | None
    llm_timeout_seconds: float
    log_level: str


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Heart Disease Prediction"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        debug=_parse_bool(os.getenv("DEBUG"), False),
        api_v1_prefix=os.getenv("API_V1_PREFIX", "/api/v1"),
        cors_origins=_parse_csv(
            os.getenv("CORS_ORIGINS"),
            ["http://localhost:5173", "http://127.0.0.1:5173"],
        ),
        llm_enabled=_parse_bool(os.getenv("LLM_ENABLED"), True),
        llm_base_url=os.getenv("LLM_BASE_URL", "http://127.0.0.1:1234").rstrip("/"),
        llm_model=os.getenv("LLM_MODEL") or None,
        llm_api_key=os.getenv("LLM_API_KEY") or None,
        llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "10")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


settings = get_settings()
