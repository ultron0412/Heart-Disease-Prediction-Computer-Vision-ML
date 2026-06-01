#!/bin/bash
# Frontend Startup Script for Heart Disease Prediction System
# Linux/macOS bash script to start React Vite dev server

echo ""
echo "===================================="
echo "Heart Disease Prediction Frontend"
echo "===================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi

echo "[*] Node.js found"
node --version

echo "[*] npm found"
npm --version

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "[*] Installing npm dependencies..."
    echo "This may take a minute..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Start Vite dev server
echo ""
echo "[✓] Starting React development server..."
echo ""
echo "===================================="
echo "Frontend running at:"
echo "  http://localhost:5173"
echo ""
echo "Backend should be running at:"
echo "  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

npm run dev
