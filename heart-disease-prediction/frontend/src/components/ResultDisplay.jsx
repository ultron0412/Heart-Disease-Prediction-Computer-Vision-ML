import React from 'react'
import './ResultDisplay.css'

const ResultDisplay = ({ prediction, onReset }) => {
  const getRiskColor = (riskLevel) => {
    if (riskLevel.includes('Low')) return '#2e7d32'
    if (riskLevel.includes('Moderate')) return '#ef6c00'
    if (riskLevel.includes('High')) return '#c62828'
    return '#616161'
  }

  const riskColor = getRiskColor(prediction.risk_level)

  const recommendationsByRisk = {
    low: [
      'Continue routine check-ups and healthy exercise.',
      'Maintain blood pressure and cholesterol monitoring.'
    ],
    moderate: [
      'Schedule cardiology follow-up soon.',
      'Start strict lifestyle improvements (diet, activity, sleep).',
      'Discuss preventive medications with your doctor.'
    ],
    high: [
      'Seek urgent medical evaluation.',
      'Arrange immediate cardiology consultation.',
      'Follow diagnostic and treatment advice without delay.'
    ]
  }

  const recommendationKey = prediction.risk_level.toLowerCase().includes('high')
    ? 'high'
    : prediction.risk_level.toLowerCase().includes('moderate')
      ? 'moderate'
      : 'low'

  return (
    <div className="result-display">
      <div className="result-header">
        <h2>Prediction Result</h2>
      </div>

      <div className="risk-card" style={{ borderColor: riskColor }}>
        <div className="risk-info">
          <h3>Risk Level</h3>
          <p className="risk-level" style={{ color: riskColor }}>{prediction.risk_level}</p>
        </div>
      </div>

      <div className="score-section">
        <div className="score-box">
          <h4>Final Risk Score</h4>
          <div className="score-meter">
            <div className="score-fill" style={{ width: `${prediction.risk_score * 100}%`, backgroundColor: riskColor }} />
          </div>
          <p className="score-value">{(prediction.risk_score * 100).toFixed(1)}%</p>
        </div>
      </div>

      <div className="probability-section">
        <div className="probability-box">
          <h4>Clinical Model ({(prediction.clinical_weight * 100).toFixed(0)}%)</h4>
          <div className="prob-bar"><div className="prob-fill" style={{ width: `${prediction.clinical_probability * 100}%` }} /></div>
          <p className="prob-value">{(prediction.clinical_probability * 100).toFixed(1)}%</p>
        </div>

        <div className="probability-box">
          <h4>ECG Model ({(prediction.ecg_weight * 100).toFixed(0)}%)</h4>
          <div className="prob-bar">
            <div
              className="prob-fill"
              style={{
                width: `${prediction.ecg_probability * 100}%`,
                backgroundColor: prediction.ecg_used ? '#0288d1' : '#cfd8dc'
              }}
            />
          </div>
          <p className="prob-value">
            {prediction.ecg_used ? `${(prediction.ecg_probability * 100).toFixed(1)}%` : 'Not used'}
          </p>
        </div>
      </div>

      <div className="explanation-box">
        <h3>Explanation</h3>
        <p className="explanation-text">{prediction.explanation}</p>
        <p className="explanation-text">Model agreement: {(prediction.model_agreement * 100).toFixed(1)}%</p>
      </div>

      <div className="recommendation-box">
        <h3>Recommendations</h3>
        <ul>
          {recommendationsByRisk[recommendationKey].map((item) => <li key={item}>{item}</li>)}
          <li>Consult healthcare professionals for medical decisions.</li>
        </ul>
      </div>

      <div className="disclaimer-box">
        <p><strong>Medical Disclaimer:</strong> This AI prediction is informational and is not a diagnosis.</p>
      </div>

      <div className="action-buttons">
        <button onClick={onReset} className="reset-button">New Prediction</button>
        <a href="https://www.heart.org" target="_blank" rel="noopener noreferrer" className="info-button">Learn More</a>
      </div>
    </div>
  )
}

export default ResultDisplay
