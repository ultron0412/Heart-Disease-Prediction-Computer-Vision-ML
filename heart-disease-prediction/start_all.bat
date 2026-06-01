@echo off
REM ====================================
REM Heart Disease Prediction System
REM Complete Startup Script (Windows)
REM ====================================

setlocal enabledelayedexpansion

echo.
echo ====================================
echo Starting Heart Disease Prediction
echo System (Backend + Frontend)
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)

echo [✓] Python and Node.js found

REM Start Backend in new window
echo.
echo [*] Starting Backend server...
cd backend
start cmd /k "call run_backend.bat"
cd ..

REM Wait for backend to start
timeout /t 5 /nobreak

REM Start Frontend in new window
echo [*] Starting Frontend server...
cd frontend
start cmd /k "call run_frontend.bat"
cd ..

echo.
echo ====================================
echo SUCCESS! 
echo ====================================
echo.
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Frontend: http://localhost:5173
echo.
echo Opening frontend in browser...
timeout /t 3 /nobreak

REM Try to open in browser
start http://localhost:5173

echo.
echo Both servers are running!
echo Press any key to continue...
pause

exit /b 0
