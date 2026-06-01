import React, { useState } from 'react'
import PredictionForm from './components/PredictionForm'
import ResultDisplay from './components/ResultDisplay'
import './App.css'

function App() {
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handlePrediction = (result) => {
    setPrediction(result)
    setError(null)
  }

  const handleError = (err) => {
    setError(err)
    setPrediction(null)
  }

  const handleLoadingChange = (isLoading) => {
    setLoading(isLoading)
  }

  const resetForm = () => {
    setPrediction(null)
    setError(null)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>❤️ Heart Disease Prediction System</h1>
        <p className="subtitle">AI-Powered Risk Assessment using Clinical Data & ECG Images</p>
      </header>

      <main className="app-main">
        <div className="content-wrapper">
          <div className="form-section">
            <PredictionForm 
              onPrediction={handlePrediction}
              onError={handleError}
              onLoadingChange={handleLoadingChange}
              isLoading={loading}
            />
          </div>

          <div className="result-section">
            {error && (
              <div className="error-message">
                <span>⚠️ {error}</span>
                <button onClick={resetForm} className="reset-btn">Reset</button>
              </div>
            )}
            
            {loading && (
              <div className="loading-indicator">
                <div className="spinner"></div>
                <p>Analyzing your data...</p>
              </div>
            )}
            
            {prediction && !loading && (
              <ResultDisplay 
                prediction={prediction}
                onReset={resetForm}
              />
            )}
            
            {!prediction && !error && !loading && (
              <div className="welcome-message">
                <p>👈 Fill out the form to get a heart disease risk prediction</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>⚕️ Disclaimer: This tool is for informational purposes only and should not replace professional medical advice.</p>
      </footer>
    </div>
  )
}

export default App
