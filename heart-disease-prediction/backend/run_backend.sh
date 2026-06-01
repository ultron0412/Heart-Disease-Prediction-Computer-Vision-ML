#!/bin/bash
# Backend Startup Script for Heart Disease Prediction System
# Linux/macOS bash script to start FastAPI backend

echo ""
echo "===================================="
echo "Heart Disease Prediction Backend"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[*] Python found"
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "[*] Installing dependencies..."
pip install -r requirements.txt

# Start FastAPI server
echo ""
echo "[✓] Starting FastAPI backend server..."
echo ""
echo "===================================="
echo "Backend running at:"
echo "  http://localhost:8000"
echo ""
echo "API Documentation at:"
echo "  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
