import React, { useMemo, useState } from 'react'
import axios from 'axios'
import './PredictionForm.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const numericFields = new Set([
  'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
  'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
])

const PredictionForm = ({ onPrediction, onError, onLoadingChange, isLoading }) => {
  const [formData, setFormData] = useState({
    age: 45,
    sex: 1,
    cp: 1,
    trestbps: 130,
    chol: 220,
    fbs: 0,
    restecg: 0,
    thalach: 150,
    exang: 0,
    oldpeak: 3.1,
    slope: 2,
    ca: 0,
    thal: 1,
    symptoms: ''
  })

  const [ecgImage, setEcgImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)

  const canSubmit = useMemo(() => {
    return Number.isFinite(formData.age) && formData.age >= 18 && formData.age <= 120
  }, [formData.age])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    const parsedValue = numericFields.has(name)
      ? name === 'oldpeak'
        ? Number.parseFloat(value)
        : Number.parseInt(value, 10)
      : value

    setFormData((prev) => ({
      ...prev,
      [name]: parsedValue
    }))
  }

  const handleImageChange = (e) => {
    const file = e.target.files?.[0]
    if (!file) {
      return
    }

    setEcgImage(file)
    const reader = new FileReader()
    reader.onloadend = () => setImagePreview(reader.result)
    reader.readAsDataURL(file)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    onLoadingChange(true)

    try {
      let response
      if (ecgImage) {
        const formDataToSend = new FormData()
        formDataToSend.append('data', JSON.stringify(formData))
        formDataToSend.append('ecg_image', ecgImage)

        response = await axios.post(`${API_BASE_URL}/api/v1/predict`, formDataToSend, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      } else {
        response = await axios.post(`${API_BASE_URL}/api/v1/predict`, formData, {
          headers: { 'Content-Type': 'application/json' }
        })
      }

      onPrediction(response.data)
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        `Failed to get prediction from ${API_BASE_URL}`
      onError(errorMessage)
    } finally {
      onLoadingChange(false)
    }
  }

  const clearImage = () => {
    setEcgImage(null)
    setImagePreview(null)
  }

  return (
    <form onSubmit={handleSubmit} className="prediction-form">
      <h2>Clinical Information</h2>

      <div className="form-group">
        <label htmlFor="age">Age (years) *</label>
        <input type="number" id="age" name="age" value={formData.age} onChange={handleInputChange} min="18" max="120" required />
        <small>Accepted range: 18-120</small>
      </div>

      <div className="form-group">
        <label htmlFor="sex">Sex *</label>
        <select id="sex" name="sex" value={formData.sex} onChange={handleInputChange} required>
          <option value="0">Female</option>
          <option value="1">Male</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="cp">Chest Pain Type *</label>
        <select id="cp" name="cp" value={formData.cp} onChange={handleInputChange} required>
          <option value="0">Typical Angina</option>
          <option value="1">Atypical Angina</option>
          <option value="2">Non-anginal Pain</option>
          <option value="3">Asymptomatic</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="trestbps">Resting Blood Pressure (mmHg) *</label>
        <input type="number" id="trestbps" name="trestbps" value={formData.trestbps} onChange={handleInputChange} min="80" max="200" required />
      </div>

      <div className="form-group">
        <label htmlFor="chol">Serum Cholesterol (mg/dl) *</label>
        <input type="number" id="chol" name="chol" value={formData.chol} onChange={handleInputChange} min="0" max="400" required />
      </div>

      <div className="form-group">
        <label htmlFor="fbs">Fasting Blood Sugar &gt; 120 mg/dl *</label>
        <select id="fbs" name="fbs" value={formData.fbs} onChange={handleInputChange} required>
          <option value="0">No</option>
          <option value="1">Yes</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="restecg">Resting ECG Results *</label>
        <select id="restecg" name="restecg" value={formData.restecg} onChange={handleInputChange} required>
          <option value="0">Normal</option>
          <option value="1">ST-T Abnormality</option>
          <option value="2">LV Hypertrophy</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="thalach">Max Heart Rate Achieved *</label>
        <input type="number" id="thalach" name="thalach" value={formData.thalach} onChange={handleInputChange} min="60" max="202" required />
      </div>

      <div className="form-group">
        <label htmlFor="exang">Exercise Induced Angina *</label>
        <select id="exang" name="exang" value={formData.exang} onChange={handleInputChange} required>
          <option value="0">No</option>
          <option value="1">Yes</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="oldpeak">ST Depression (0-6.2) *</label>
        <input type="number" id="oldpeak" name="oldpeak" value={formData.oldpeak} onChange={handleInputChange} min="0" max="6.2" step="0.1" required />
      </div>

      <div className="form-group">
        <label htmlFor="slope">ST Segment Slope *</label>
        <select id="slope" name="slope" value={formData.slope} onChange={handleInputChange} required>
          <option value="0">Upsloping</option>
          <option value="1">Flat</option>
          <option value="2">Downsloping</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="ca">Major Vessels Colored by Fluoroscopy *</label>
        <select id="ca" name="ca" value={formData.ca} onChange={handleInputChange} required>
          <option value="0">0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="thal">Thalassemia *</label>
        <select id="thal" name="thal" value={formData.thal} onChange={handleInputChange} required>
          <option value="0">Normal</option>
          <option value="1">Fixed Defect</option>
          <option value="2">Reversible Defect</option>
          <option value="3">Other</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="symptoms">Additional Symptoms (optional)</label>
        <textarea id="symptoms" name="symptoms" value={formData.symptoms} onChange={handleInputChange} rows="3" />
      </div>

      <div className="image-section">
        <h3>ECG Image (Optional)</h3>
        <div className="image-upload">
          <input type="file" id="ecg-image" accept="image/*" onChange={handleImageChange} disabled={isLoading} />
          <label htmlFor="ecg-image" className="upload-label">{ecgImage ? 'Image selected' : 'Choose ECG image'}</label>
        </div>

        {imagePreview && (
          <div className="image-preview">
            <img src={imagePreview} alt="ECG preview" />
            <button type="button" onClick={clearImage} className="clear-image-btn" disabled={isLoading}>
              Remove Image
            </button>
          </div>
        )}
      </div>

      <button type="submit" className="submit-btn" disabled={isLoading || !canSubmit}>
        {isLoading ? 'Analyzing...' : 'Get Prediction'}
      </button>
    </form>
  )
}

export default PredictionForm
