@echo off
echo 🌱 KissanAI - Crop Disease Detection
echo ====================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "fast_api.py" (
    echo ❌ fast_api.py not found
    pause
    exit /b 1
)

if not exist "streamlit_app.py" (
    echo ❌ streamlit_app.py not found
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the application
echo 🚀 Starting KissanAI...
python run_app.py

pause 