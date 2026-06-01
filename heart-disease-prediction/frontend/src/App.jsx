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

  const resetForm = () => {
    setPrediction(null)
    setError(null)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Heart Disease Prediction System</h1>
        <p className="subtitle">Multimodal AI Risk Assessment with Clinical Data and ECG Imaging</p>
      </header>

      <main className="app-main">
        <div className="content-wrapper">
          <div className="form-section">
            <PredictionForm
              onPrediction={handlePrediction}
              onError={handleError}
              onLoadingChange={setLoading}
              isLoading={loading}
            />
          </div>

          <div className="result-section">
            {error && (
              <div className="error-message">
                <span>{error}</span>
                <button onClick={resetForm} className="reset-btn">Reset</button>
              </div>
            )}

            {loading && (
              <div className="loading-indicator">
                <div className="spinner"></div>
                <p>Analyzing clinical and ECG signals...</p>
              </div>
            )}

            {prediction && !loading && <ResultDisplay prediction={prediction} onReset={resetForm} />}

            {!prediction && !error && !loading && (
              <div className="welcome-message">
                <p>Fill the form and optionally upload an ECG image to generate risk analysis.</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>Disclaimer: This tool supports screening only and does not replace medical diagnosis.</p>
      </footer>
    </div>
  )
}

export default App
