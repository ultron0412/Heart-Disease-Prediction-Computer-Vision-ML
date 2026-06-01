import React from 'react'
import './ResultDisplay.css'

const ResultDisplay = ({ prediction, onReset }) => {
  const getRiskColor = (riskLevel) => {
    if (riskLevel.includes('Low')) return '#4caf50'
    if (riskLevel.includes('Moderate')) return '#ff9800'
    if (riskLevel.includes('High')) return '#f44336'
    return '#999'
  }

  const getRiskIcon = (riskLevel) => {
    if (riskLevel.includes('Low')) return '✅'
    if (riskLevel.includes('Moderate')) return '⚠️'
    if (riskLevel.includes('High')) return '🚨'
    return '❓'
  }

  const riskColor = getRiskColor(prediction.risk_level)
  const riskIcon = getRiskIcon(prediction.risk_level)

  return (
    <div className="result-display">
      <div className="result-header">
        <h2>📊 Prediction Result</h2>
      </div>

      <div className="risk-card" style={{ borderColor: riskColor }}>
        <div className="risk-icon">{riskIcon}</div>
        <div className="risk-info">
          <h3>Risk Level</h3>
          <p className="risk-level" style={{ color: riskColor }}>
            {prediction.risk_level}
          </p>
        </div>
      </div>

      <div className="score-section">
        <div className="score-box">
          <h4>Final Risk Score</h4>
          <div className="score-meter">
            <div 
              className="score-fill" 
              style={{ 
                width: `${prediction.risk_score * 100}%`,
                backgroundColor: riskColor
              }}
            ></div>
          </div>
          <p className="score-value">{(prediction.risk_score * 100).toFixed(1)}%</p>
        </div>
      </div>

      <div className="probability-section">
        <div className="probability-box">
          <h4>Clinical Model</h4>
          <div className="prob-bar">
            <div 
              className="prob-fill"
              style={{ width: `${prediction.clinical_probability * 100}%` }}
            ></div>
          </div>
          <p className="prob-value">{(prediction.clinical_probability * 100).toFixed(1)}%</p>
        </div>

        <div className="probability-box">
          <h4>ECG Model</h4>
          <div className="prob-bar">
            <div 
              className="prob-fill"
              style={{ 
                width: `${prediction.ecg_probability * 100}%`,
                backgroundColor: prediction.ecg_probability > 0 ? '#2196f3' : '#ddd'
              }}
            ></div>
          </div>
          <p className="prob-value">{prediction.ecg_probability > 0 ? `${(prediction.ecg_probability * 100).toFixed(1)}%` : 'N/A'}</p>
        </div>
      </div>

      <div className="explanation-box">
        <h3>📝 Analysis Explanation</h3>
        <p className="explanation-text">{prediction.explanation}</p>
      </div>

      <div className="recommendation-box">
        <h3>💡 Recommendations</h3>
        <ul>
          {prediction.risk_level.includes('Low') && (
            <>
              <li>✓ Continue regular health check-ups</li>
              <li>✓ Maintain healthy lifestyle and exercise routine</li>
              <li>✓ Monitor blood pressure and cholesterol regularly</li>
            </>
          )}
          {prediction.risk_level.includes('Moderate') && (
            <>
              <li>⚠️ Schedule a consultation with your cardiologist</li>
              <li>⚠️ Implement lifestyle modifications (diet, exercise)</li>
              <li>⚠️ Increase frequency of health monitoring</li>
              <li>⚠️ Consider preventive medications if recommended</li>
            </>
          )}
          {prediction.risk_level.includes('High') && (
            <>
              <li>🚨 Seek immediate medical attention</li>
              <li>🚨 Schedule urgent consultation with a cardiologist</li>
              <li>🚨 May require diagnostic testing (stress test, angiography)</li>
              <li>🚨 Follow doctor's treatment plan strictly</li>
            </>
          )}
          <li>📖 Consult with healthcare professionals for personalized advice</li>
        </ul>
      </div>

      <div className="disclaimer-box">
        <p>⚕️ <strong>Medical Disclaimer:</strong> This prediction is based on AI analysis and should not replace professional medical diagnosis. Always consult with healthcare providers for medical decisions.</p>
      </div>

      <div className="action-buttons">
        <button onClick={onReset} className="reset-button">
          ← New Prediction
        </button>
        <a href="https://www.heart.org" target="_blank" rel="noopener noreferrer" className="info-button">
          Learn More →
        </a>
      </div>
    </div>
  )
}

export default ResultDisplay
