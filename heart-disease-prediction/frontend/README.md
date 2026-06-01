# Frontend README

## 🚀 Quick Start

### Windows
```bash
cd frontend
run_frontend.bat
```

### Linux/macOS
```bash
cd frontend
chmod +x run_frontend.sh
./run_frontend.sh
```

### Manual Setup
```bash
npm install
npm run dev
```

The app will open at `http://localhost:5173`

## 📋 Features

### Patient Input Form
- **Demographics:** Age, sex
- **Symptoms:** Chest pain type, symptoms
- **Vitals:** Blood pressure, heart rate
- **Labs:** Cholesterol, blood sugar
- **Diagnostics:** ECG parameters, vessel count, thalassemia type
- **Images:** Optional ECG image upload

### Results Display
- Risk score (0-100%)
- Risk classification (Low/Moderate/High)
- Clinical & ECG model probabilities
- AI-generated explanation
- Medical recommendations
- Medical disclaimer

### UI/UX
- Modern gradient design
- Responsive layout (mobile-friendly)
- Real-time form validation
- Image preview
- Loading indicators
- Error handling

## 🛠️ Technology Stack

- **React 18:** UI library
- **Vite:** Build tool & dev server
- **Axios:** HTTP client
- **CSS3:** Styling & animations

## 📁 Project Structure

```
src/
├── App.jsx              # Main app component
├── App.css              # App styles
├── main.jsx             # React entry point
├── index.css            # Global styles
└── components/
    ├── PredictionForm.jsx      # Form component
    ├── PredictionForm.css       # Form styles
    ├── ResultDisplay.jsx        # Results component
    └── ResultDisplay.css        # Results styles
```

## 🔧 Configuration

### Backend Connection
Edit the API URL in `src/components/PredictionForm.jsx`:

```javascript
const response = await axios.post(
  'http://localhost:8000/api/v1/predict',  // Change this if backend is on different host
  ...
)
```

### Vite Config
Proxy settings in `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // Backend URL
      changeOrigin: true,
    }
  }
}
```

## 📦 Available Scripts

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

## 🎨 Styling

### Color Scheme
- Primary: Gradient (Purple - #667eea to #764ba2)
- Success (Low Risk): #4caf50
- Warning (Moderate): #ff9800
- Danger (High Risk): #f44336

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 📱 Form Validation

All clinical fields are required and validated:
- **Age:** 0-120 years
- **Blood Pressure:** 80-200 mmHg
- **Cholesterol:** 0-400 mg/dl
- **Heart Rate:** 60-202 bpm
- **ST Depression:** 0-6.2

## 🖼️ Image Upload

- Accepted formats: JPG, PNG, GIF, WebP
- Maximum size: Browser dependent (typically 50-100MB)
- Preview displayed before submission
- Optional - can submit without image

## 🔌 API Integration

### Request
```javascript
const formDataToSend = new FormData()
formDataToSend.append('data', JSON.stringify(clinicalData))
formDataToSend.append('ecg_image', imageFile)

const response = await axios.post(
  'http://localhost:8000/api/v1/predict',
  formDataToSend,
  { headers: { 'Content-Type': 'multipart/form-data' } }
)
```

### Response
```javascript
{
  "risk_score": 0.65,
  "risk_level": "Moderate Risk",
  "explanation": "...",
  "clinical_probability": 0.68,
  "ecg_probability": 0.60,
  "confidence": 0.65
}
```

## 🚨 Troubleshooting

**Cannot connect to backend:**
- Ensure backend is running on http://localhost:8000
- Check CORS settings in backend
- Check browser console for errors

**npm install fails:**
```bash
rm -r node_modules package-lock.json
npm install
```

**Port 5173 already in use:**
Edit `vite.config.js`:
```javascript
server: {
  port: 5174  // Use different port
}
```

**Module not found errors:**
```bash
npm install
npm run dev
```

## 📚 Dependencies

- **react@^18.2.0** - UI library
- **react-dom@^18.2.0** - React DOM
- **axios@^1.6.0** - HTTP client
- **vite@^5.0.0** - Build tool
- **@vitejs/plugin-react@^4.2.0** - Vite React plugin

## 🌐 Deployment

### Build Production
```bash
npm run build  # Creates dist/ folder
```

### Deploy to Server
```bash
# Copy dist/ folder to web server
cp -r dist/ /var/www/html/heartprediction/
```

### Environment Variables
Create `.env` for production:
```
VITE_API_URL=https://api.example.com
```

Use in components:
```javascript
const API_URL = import.meta.env.VITE_API_URL
```

## 📚 Documentation

- React: https://react.dev
- Vite: https://vitejs.dev
- Axios: https://axios-http.com
- MDN Web Docs: https://developer.mozilla.org

## ⚕️ Medical Disclaimer

This application is for informational purposes only. Always consult with healthcare professionals for medical decisions.
