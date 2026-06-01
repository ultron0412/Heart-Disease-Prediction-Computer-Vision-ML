# Project Structure

```text
heart-disease-prediction/
+-- backend/
¦   +-- app/
¦   ¦   +-- api/
¦   ¦   ¦   +-- v1/
¦   ¦   ¦       +-- endpoints/
¦   ¦   ¦       ¦   +-- health.py
¦   ¦   ¦       ¦   +-- predict.py
¦   ¦   ¦       +-- router.py
¦   ¦   +-- fusion/
¦   ¦   ¦   +-- risk_fusion.py
¦   ¦   +-- models/
¦   ¦   ¦   +-- clinical/
¦   ¦   ¦   +-- image/
¦   ¦   +-- schemas/
¦   ¦   ¦   +-- prediction.py
¦   ¦   +-- services/
¦   ¦   ¦   +-- prediction_service.py
¦   ¦   +-- config.py
¦   ¦   +-- logger.py
¦   ¦   +-- main.py
¦   +-- tests/
¦   +-- requirements.txt
¦   +-- run_backend.bat
¦   +-- run_backend.sh
+-- data/
¦   +-- clinical/
¦   +-- images/
+-- docs/
¦   +-- PROJECT_STRUCTURE.md
+-- frontend/
¦   +-- src/
¦   ¦   +-- api/
¦   ¦   +-- components/
¦   ¦   +-- hooks/
¦   ¦   +-- utils/
¦   ¦   +-- App.jsx
¦   ¦   +-- main.jsx
¦   ¦   +-- index.css
¦   +-- index.html
¦   +-- package.json
¦   +-- vite.config.js
+-- models/
¦   +-- clinical/
¦   +-- image/
+-- README.md
+-- start_all.bat
```

## Folder Responsibilities

- `backend/app/api`: HTTP routes and request lifecycle.
- `backend/app/services`: business logic orchestration.
- `backend/app/models`: model loading and inference code.
- `backend/app/fusion`: multimodal risk fusion logic.
- `backend/app/schemas`: validation and response contracts.
- `backend/tests`: backend tests.
- `frontend/src/components`: UI components.
- `frontend/src/api`: HTTP client and endpoint wrappers.
- `frontend/src/hooks`: reusable React hooks.
- `frontend/src/utils`: shared frontend helpers.
- `docs`: project documentation.

## Next Safe Refactor (Optional)

1. Move direct Axios call from `components/PredictionForm.jsx` into `src/api/predictionApi.js`.
2. Add unit tests for `risk_fusion.py` under `backend/tests/`.
3. Add API integration tests for `/api/v1/predict`.
