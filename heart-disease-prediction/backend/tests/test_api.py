from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _valid_payload() -> dict[str, int | float | str]:
    return {
        "age": 52,
        "sex": 1,
        "cp": 2,
        "trestbps": 138,
        "chol": 212,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 2,
        "symptoms": "intermittent chest discomfort",
    }


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "backend running successfully" in response.json()["message"].lower()


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_predict_with_json_payload(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.endpoints.predict.predict_clinical_risk",
        lambda _: 0.41,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.predict.build_prediction_explanation",
        lambda *_: "Deterministic explanation",
    )

    response = client.post("/api/v1/predict", json=_valid_payload())

    body = response.json()
    assert response.status_code == 200
    assert body["risk_level"] == "Moderate Risk"
    assert body["ecg_used"] is False
    assert body["explanation"] == "Deterministic explanation"


def test_predict_with_multipart_payload(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.endpoints.predict.predict_clinical_risk",
        lambda _: 0.3,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.predict.predict_ecg_image",
        lambda _: 0.9,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.predict.build_prediction_explanation",
        lambda *_: "Deterministic explanation",
    )

    response = client.post(
        "/api/v1/predict",
        data={"data": json.dumps(_valid_payload())},
        files={"ecg_image": ("ecg.png", b"fake-image-bytes", "image/png")},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ecg_used"] is True
    assert body["risk_level"] == "Moderate Risk"


def test_predict_rejects_unknown_fields() -> None:
    payload = _valid_payload()
    payload["unexpected"] = "value"

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422
