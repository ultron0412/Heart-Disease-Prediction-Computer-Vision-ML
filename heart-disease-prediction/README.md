# Heart Disease Prediction System - Installation & Setup Guide

## 🎯 Overview
This is a full-stack Heart Disease Prediction application using:
- **Backend:** FastAPI (Python)
- **Frontend:** React with Vite
- **ML Models:** Clinical predictor (scikit-learn) + ECG CNN (TensorFlow)

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- Node.js 16+ and npm
- 2GB free disk space
- 4GB RAM minimum

### Verify Installations
```bash
# Check Python
python --version  # Should be 3.8+

# Check Node and npm
node --version    # Should be 16+
npm --version     # Should be 8+
```

---

## 🚀 Quick Start (Windows)

### Option 1: Using Batch Scripts (Easiest)

#### Step 1: Start Backend
```bash
cd heart-disease-prediction\backend
run_backend.bat
```

#### Step 2: Start Frontend (in new terminal)
```bash
cd heart-disease-prediction\frontend
run_frontend.bat
```

The app will open at `http://localhost:5173`

---

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd heart-disease-prediction\backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run backend server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   ✅ Backend runs at: `http://localhost:8000`
   📊 API docs at: `http://localhost:8000/docs`

#### Frontend Setup (in new terminal)

1. **Navigate to frontend directory:**
   ```bash
   cd heart-disease-prediction\frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   ✅ Frontend runs at: `http://localhost:5173`

---

## 📁 Project Structure

```
heart-disease-prediction/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── api/v1/                  # API routes
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py        # Health check endpoint
│   │   │   │   └── predict.py       # Prediction endpoint
│   │   │   └── router.py
│   │   ├── models/
│   │   │   ├── clinical/            # Clinical ML model
│   │   │   └── image/               # ECG CNN model
│   │   ├── schemas/                 # Request/response schemas
│   │   ├── services/                # Business logic
│   │   ├── fusion/                  # Risk fusion logic
│   │   └── main.py                  # FastAPI app
│   ├── requirements.txt
│   └── run_backend.bat              # Windows startup script
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── App.jsx                  # Main app component
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── run_frontend.bat             # Windows startup script
├── models/
│   ├── clinical/                    # Clinical ML model files
│   └── image/                       # CNN model files
│       ├── heart_cnn.h5
│       └── heart_cnn.keras
└── data/
    ├── clinical/
    │   └── heart.csv
    └── images/
        ├── train/
        │   ├── disease/
        │   └── normal/
        └── test/
            ├── disease/
            └── normal/
```

---

## 🔧 API Endpoints

### Health Check
```
GET /api/v1/health
```
Response:
```json
{
  "status": "OK",
  "service": "Heart Disease Prediction Backend"
}
```

### Make Prediction
```
POST /api/v1/predict
```

**Request (multipart/form-data):**
```json
{
  "data": {
    "age": 45,
    "sex": 1,
    "cp": 1,
    "trestbps": 130,
    "chol": 220,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 3.1,
    "slope": 2,
    "ca": 0,
    "thal": 1,
    "symptoms": "Chest pain"
  },
  "ecg_image": <optional image file>
}
```

**Response:**
```json
{
  "risk_score": 0.65,
  "risk_level": "Moderate Risk",
  "explanation": "Clinical data indicates moderate risk...",
  "clinical_probability": 0.68,
  "ecg_probability": 0.60,
  "confidence": 0.65
}
```

---

## 🎨 Frontend Features

### Clinical Data Input Form
- Age, sex, chest pain type
- Blood pressure, cholesterol, heart rate
- ECG parameters (ST depression, slope, etc.)
- Thalassemia type and vessel count
- Optional symptom description

### ECG Image Upload (Optional)
- Supports JPG, PNG formats
- Image preview before submission
- Automatic preprocessing

### Prediction Results
- Risk score (0-100%)
- Risk level classification (Low/Moderate/High)
- Clinical & ECG probability breakdown
- AI explanation
- Medical recommendations
- Disclaimer

---

## 🔍 Testing the Application

### Test Case 1: Low Risk Patient
```json
{
  "age": 35,
  "sex": 0,
  "cp": 0,
  "trestbps": 120,
  "chol": 200,
  "fbs": 0,
  "restecg": 0,
  "thalach": 170,
  "exang": 0,
  "oldpeak": 0.0,
  "slope": 2,
  "ca": 0,
  "thal": 1
}
```

### Test Case 2: High Risk Patient
```json
{
  "age": 70,
  "sex": 1,
  "cp": 3,
  "trestbps": 180,
  "chol": 350,
  "fbs": 1,
  "restecg": 2,
  "thalach": 80,
  "exang": 1,
  "oldpeak": 5.0,
  "slope": 0,
  "ca": 3,
  "thal": 2
}
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (replace PID)
taskkill /PID <PID> /F
```

**Model not found error:**
- Ensure model files exist in `models/clinical/` and `models/image/`
- Check file paths in `app/models/clinical/predictor.py`

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Kill Vite process or change port in vite.config.js
```

**Cannot connect to backend:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS is enabled in `app/main.py`
- Check firewall settings

**Module not found:**
```bash
# Reinstall packages
rm -r node_modules package-lock.json
npm install
```

---

## 📊 Model Information

### Clinical Model (heart_ml.pkl)
- **Type:** Scikit-learn (Logistic Regression/Random Forest)
- **Features:** 13 clinical parameters
- **Output:** Probability of heart disease (0-1)

### ECG CNN Model (heart_cnn.keras)
- **Type:** TensorFlow/Keras
- **Input:** 224×224 ECG image
- **Output:** Probability of abnormality (0-1)

### Fusion Logic
- **Weight:** 65% Clinical + 35% ECG
- **Categories:** Low (<0.3), Moderate (0.3-0.6), High (>0.6)

---

## 🔐 Security Notes

### Development
- CORS is set to allow all origins (⚠️ Change in production)
- No authentication implemented (Add JWT/OAuth for production)
- Temporary image storage (implement cleanup)

### Production Recommendations
1. Use environment variables for sensitive data
2. Implement user authentication
3. Add rate limiting
4. Enable HTTPS
5. Use proper CORS settings
6. Add input validation & sanitization
7. Implement logging & monitoring

---

## 📈 Performance Optimization

### Backend
- Use model caching (already implemented)
- Consider async task queue for heavy computations
- Add database for result history

### Frontend
- Code splitting with lazy loading
- Image compression before upload
- Service workers for offline capability

---

## 📚 Dependencies

### Backend
- fastapi: Web framework
- uvicorn: ASGI server
- tensorflow: Deep learning
- scikit-learn: ML algorithms
- pandas: Data processing
- pillow: Image processing

### Frontend
- react: UI library
- axios: HTTP client
- vite: Build tool

---

## 📞 Support & Documentation

- **API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)
- **React Docs:** https://react.dev
- **FastAPI Docs:** https://fastapi.tiangolo.com

---

## ⚕️ Medical Disclaimer

This application is for informational purposes only and should NOT be used for:
- Clinical diagnosis
- Treatment decisions
- Medical emergencies

**Always consult with qualified healthcare professionals.**

---

## 📝 License & Credits

Heart Disease Prediction System © 2024

---

**Questions? Issues? Suggestions?** Please check the troubleshooting section above.
