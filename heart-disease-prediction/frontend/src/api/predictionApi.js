import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function predictHeartDisease(clinicalData, ecgImage = null) {
  if (ecgImage) {
    const formDataToSend = new FormData()
    formDataToSend.append('data', JSON.stringify(clinicalData))
    formDataToSend.append('ecg_image', ecgImage)

    const response = await axios.post(`${API_BASE_URL}/api/v1/predict`, formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  }

  const response = await axios.post(`${API_BASE_URL}/api/v1/predict`, clinicalData, {
    headers: { 'Content-Type': 'application/json' }
  })
  return response.data
}

export function getPredictionErrorMessage(error) {
  return (
    error?.response?.data?.detail ||
    error?.message ||
    `Failed to get prediction from ${API_BASE_URL}`
  )
}

