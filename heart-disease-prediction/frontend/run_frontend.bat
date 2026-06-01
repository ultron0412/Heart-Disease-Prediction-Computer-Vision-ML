@echo off
REM Frontend Startup Script for Heart Disease Prediction System
REM Windows batch script to start React Vite dev server

echo.
echo ====================================
echo Heart Disease Prediction Frontend
echo ====================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo [*] Node.js found
node --version

echo [*] npm found
npm --version

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo [*] Installing npm dependencies...
    echo This may take a minute...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start Vite dev server
echo.
echo [✓] Starting React development server...
echo.
echo ====================================
echo Frontend running at:
echo   http://localhost:5173
echo.
echo Backend should be running at:
echo   http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

call npm run dev

pause
