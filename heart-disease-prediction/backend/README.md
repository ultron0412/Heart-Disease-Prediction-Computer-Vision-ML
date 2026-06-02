# Backend README

## Quick Start

### Windows
```bash
cd backend
run_backend.bat
```

### Linux/macOS
```bash
cd backend
chmod +x run_backend.sh
./run_backend.sh
```

### Manual Setup
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate    # Linux/macOS
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/api/v1/health`

### Docs
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

### Prediction
- `POST http://localhost:8000/api/v1/predict`
- Supports:
  - `application/json` (clinical data only)
  - `multipart/form-data` (`data` JSON + optional `ecg_image`)

## CORS Configuration

Set allowed origins with environment variable:

```bash
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Common Issues

### Form data runtime error
If you see:
`Form data requires "python-multipart" to be installed`

Install dependency in your active environment:

```bash
pip install python-multipart
```

### Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Model loading error
- Ensure files exist:
  - `models/clinical/heart_ml.pkl`
  - `models/image/heart_cnn.keras`
