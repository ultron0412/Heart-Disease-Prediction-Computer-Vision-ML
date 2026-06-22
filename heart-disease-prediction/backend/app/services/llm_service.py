from __future__ import annotations

from functools import lru_cache
from typing import Any, Mapping

import requests

from app.config import settings
from app.logger import logger


def build_prediction_explanation(
    clinical_payload: Mapping[str, Any],
    fusion_result: Mapping[str, Any],
) -> str:
    fallback = _build_fallback_explanation(clinical_payload, fusion_result)
    if not settings.llm_enabled:
        return fallback

    try:
        model_name = _resolve_model_name()
        if not model_name:
            return fallback

        response = requests.post(
            f"{settings.llm_base_url}/v1/chat/completions",
            headers=_build_headers(),
            json={
                "model": model_name,
                "temperature": 0.2,
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "You are a medical-risk explainer for a heart disease screening app. "
                            "Write a short, plain-language explanation with no diagnosis claims. "
                            "Mention the risk level, key drivers, and tell the user to consult a doctor. "
                            f"Patient payload: {clinical_payload}\n"
                            f"Prediction summary: {fusion_result}\n"
                            "Return 3 short sentences maximum."
                        ),
                    },
                ],
            },
            timeout=settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        content = (
            response.json()
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        return content or fallback
    except requests.RequestException as error:
        logger.warning("LLM explanation fallback triggered: %s", error)
        return fallback
    except (KeyError, IndexError, TypeError, ValueError) as error:
        logger.warning("Unexpected LLM response format, using fallback: %s", error)
        return fallback


def _build_fallback_explanation(
    clinical_payload: Mapping[str, Any],
    fusion_result: Mapping[str, Any],
) -> str:
    symptoms = str(clinical_payload.get("symptoms", "")).strip()
    risk_level = fusion_result["risk_category"]
    clinical_prob = fusion_result["clinical_probability"]
    final_risk = fusion_result["final_risk_score"]
    uses_ecg = fusion_result["ecg_used"]
    ecg_note = (
        f" The ECG model contributed a score of {fusion_result['ecg_probability']:.3f}."
        if uses_ecg
        else " No ECG image was provided, so the estimate is based on clinical factors only."
    )
    symptom_note = f" Reported symptoms: {symptoms}." if symptoms else ""
    return (
        f"The current screening result is {risk_level} with an overall risk score of {final_risk:.3f}. "
        f"Clinical features produced a probability of {clinical_prob:.3f}.{ecg_note}{symptom_note} "
        "This is an assistive estimate only and should be reviewed by a qualified clinician."
    )


def _build_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if settings.llm_api_key:
        headers["Authorization"] = f"Bearer {settings.llm_api_key}"
    return headers


@lru_cache(maxsize=1)
def _resolve_model_name() -> str | None:
    if settings.llm_model:
        return settings.llm_model

    response = requests.get(
        f"{settings.llm_base_url}/v1/models",
        headers=_build_headers(),
        timeout=settings.llm_timeout_seconds,
    )
    response.raise_for_status()
    models = response.json().get("data", [])
    if not models:
        logger.warning("No models returned from local LLM endpoint %s", settings.llm_base_url)
        return None
    return str(models[0]["id"])
