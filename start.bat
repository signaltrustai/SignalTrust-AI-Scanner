@echo off
REM SignalTrust AI Market Scanner Startup Script for Windows

echo ========================================
echo SignalTrust AI Market Scanner - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.7 or higher to run this application.
    pause
    exit /b 1
)

REM Display Python version
echo Using Python:
python --version
echo.

REM Check if requirements are installed
if exist requirements.txt (
    echo Installing dependencies...
    python -m pip install -r requirements.txt --quiet
    echo Dependencies installed.
    echo.
)

echo Starting SignalTrust AI Market Scanner Web Application...
echo Access the application at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

REM Start the Flask web application
python app.py

pause
