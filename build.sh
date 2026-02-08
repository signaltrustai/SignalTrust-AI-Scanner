#!/bin/bash
# Build script for Render deployment
# This ensures all necessary directories and setup are complete

echo "=== SignalTrust AI Scanner - Render Build ==="

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/users
mkdir -p data/transactions
mkdir -p data/backups
mkdir -p data/ai_learning
mkdir -p uploads

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Verify critical dependencies
echo "Verifying critical dependencies..."
python3 -c "import flask; print('Flask:', flask.__version__)"
python3 -c "import gunicorn; print('Gunicorn:', gunicorn.__version__)"

echo "Build completed successfully!"
