# Backend README

## 🚀 Quick Start

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
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 API Endpoints

### Health Check
```
GET http://localhost:8000/api/v1/health
```

### Interactive API Docs
```
http://localhost:8000/docs  (Swagger UI)
http://localhost:8000/redoc  (ReDoc)
```

### Make Prediction
```
POST http://localhost:8000/api/v1/predict
Content-Type: multipart/form-data

data: JSON with clinical features
ecg_image: (optional) Image file
```

## 📁 Project Structure

```
app/
├── main.py              # FastAPI app with CORS
├── config.py            # Configuration settings
├── logger.py            # Logging setup
├── api/v1/
│   ├── router.py        # API router
│   └── endpoints/
│       ├── health.py    # Health endpoint
│       └── predict.py   # Prediction endpoint
├── models/
│   ├── clinical/        # Clinical ML model
│   └── image/           # ECG CNN model
├── schemas/             # Pydantic schemas
├── services/            # Business logic
└── fusion/              # Risk fusion logic
```

## 🔧 Configuration

Edit `app/config.py` to modify settings:
- App name
- Debug mode
- Model paths

## ⚙️ Model Management

### Load Models
Models are loaded on startup:
- Clinical: `models/clinical/heart_ml.pkl`
- ECG: `models/image/heart_cnn.keras`

### Model Details
- **Clinical:** Scikit-learn model with 13 features
- **ECG:** TensorFlow CNN model (224×224 input)

## 🔐 CORS Configuration

CORS is enabled for all origins in development.
**For production, update `app/main.py`:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

## 📝 API Request Example

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -F "data={\"age\":45,\"sex\":1,\"cp\":1,\"trestbps\":130,\"chol\":220,\"fbs\":0,\"restecg\":0,\"thalach\":150,\"exang\":0,\"oldpeak\":3.1,\"slope\":2,\"ca\":0,\"thal\":1,\"symptoms\":\"Chest pain\"}" \
  -F "ecg_image=@path/to/ecg_image.jpg"
```

## 🚨 Troubleshooting

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
lsof -i :8000
kill -9 <PID>
```

**Module not found:**
```bash
pip install --upgrade -r requirements.txt
```

**Model loading error:**
- Check model files exist in `models/` directory
- Verify paths in model predictor files

## 📚 Documentation

- FastAPI Docs: https://fastapi.tiangolo.com
- Uvicorn Docs: https://www.uvicorn.org
- Pydantic Docs: https://docs.pydantic.dev
