@echo off
REM Backend Startup Script for Heart Disease Prediction System
REM Windows batch script to start FastAPI backend

echo.
echo ====================================
echo Heart Disease Prediction Backend
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [*] Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo [*] Installing dependencies...
pip install -r requirements.txt

REM Start FastAPI server
echo.
echo [✓] Starting FastAPI backend server...
echo.
echo ====================================
echo Backend running at:
echo   http://localhost:8000
echo.
echo API Documentation at:
echo   http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
