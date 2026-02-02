@echo off
REM SignalTrust AI Scanner Startup Script for Windows

echo ========================================
echo SignalTrust AI Scanner - Starting...
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

REM Check if requirements are installed (optional, since we have no required packages)
if exist requirements.txt (
    echo Installing dependencies...
    python -m pip install -r requirements.txt --quiet
    echo Dependencies installed.
    echo.
)

REM Check for command line arguments
if "%~1"=="" (
    echo Starting SignalTrust AI Scanner in interactive mode...
    echo.
    python scanner.py
) else (
    echo Starting SignalTrust AI Scanner with arguments...
    echo.
    python scanner.py %*
)

echo.
echo ========================================
echo SignalTrust AI Scanner - Finished
echo ========================================
pause
