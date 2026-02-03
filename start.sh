#!/bin/bash
# SignalTrust AI Market Scanner Startup Script for Linux/Mac

echo "========================================"
echo "SignalTrust AI Market Scanner - Starting..."
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher to run this application."
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo "Using $PYTHON_VERSION"
echo ""

# Check if requirements are installed
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt --quiet
    echo "Dependencies installed."
    echo ""
fi

echo "Starting SignalTrust AI Market Scanner Web Application..."
echo "Access the application at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""

# Start the Flask web application
python3 app.py
