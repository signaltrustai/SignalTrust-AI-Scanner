#!/bin/bash
# SignalTrust AI Scanner Startup Script for Linux/Mac

echo "========================================"
echo "SignalTrust AI Scanner - Starting..."
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

# Check if requirements are installed (optional, since we have no required packages)
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt --quiet
    echo "Dependencies installed."
    echo ""
fi

# Check for command line arguments
if [ $# -eq 0 ]; then
    echo "Starting SignalTrust AI Scanner in interactive mode..."
    echo ""
    python3 scanner.py
else
    echo "Starting SignalTrust AI Scanner with arguments..."
    echo ""
    python3 scanner.py "$@"
fi

echo ""
echo "========================================"
echo "SignalTrust AI Scanner - Finished"
echo "========================================"
