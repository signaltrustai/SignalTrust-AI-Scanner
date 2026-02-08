#!/bin/bash
# Startup script for Render deployment
# Ensures environment is ready before starting Gunicorn

echo "=== SignalTrust AI Scanner - Starting ==="

# Create data directories if they don't exist
mkdir -p data/users
mkdir -p data/transactions
mkdir -p data/backups
mkdir -p data/ai_learning
mkdir -p data/ai_hub
mkdir -p data/ai_orchestrator
mkdir -p data/notification_ai
mkdir -p data/total_market_intelligence
mkdir -p data/unified_backups
mkdir -p uploads

# Initialize empty JSON files if they don't exist
[ ! -f data/users.json ] && echo "[]" > data/users.json
[ ! -f data/coupons.json ] && echo "[]" > data/coupons.json
[ ! -f data/ai_learning_data.json ] && echo "{}" > data/ai_learning_data.json
[ ! -f data/discovered_gems.json ] && echo "[]" > data/discovered_gems.json
[ ! -f data/signalai_history.json ] && echo "[]" > data/signalai_history.json
[ ! -f data/universal_market_analysis.json ] && echo "{}" > data/universal_market_analysis.json
[ ! -f data/usage_tracking.json ] && echo "{}" > data/usage_tracking.json

echo "Environment initialized successfully!"
echo "Starting Gunicorn server..."

# Start Gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --worker-class sync --access-logfile - --error-logfile -
