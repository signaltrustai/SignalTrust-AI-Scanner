#!/bin/bash

echo "================================================"
echo "SignalTrust EU - Multi-Agent System Setup"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - GROQ_API_KEY"
    echo "   - COINGECKO_API_KEY"
    echo "   - ALPHAVANTAGE_API_KEY"
    echo "   - WHALEALERT_API_KEY"
    echo "   - NEWS_CATCHER_API_KEY"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

echo "================================================"
echo "Building and starting all agents..."
echo "================================================"
echo ""

# Build and start services
docker compose build
docker compose up -d

echo ""
echo "================================================"
echo "Waiting for services to start..."
echo "================================================"
echo ""
sleep 10

# Check service status
echo "Checking service status..."
docker compose ps

echo ""
echo "================================================"
echo "Testing services..."
echo "================================================"
echo ""

# Test coordinator
echo "Testing Coordinator..."
curl -s http://localhost:8000/ | python3 -m json.tool || echo "⚠️  Coordinator not responding"
echo ""

# Test crypto agent
echo "Testing Crypto Agent..."
curl -s http://localhost:8001/ | python3 -m json.tool || echo "⚠️  Crypto Agent not responding"
echo ""

# Test stock agent  
echo "Testing Stock Agent..."
curl -s http://localhost:8002/ | python3 -m json.tool || echo "⚠️  Stock Agent not responding"
echo ""

# Test whale agent
echo "Testing Whale Agent..."
curl -s http://localhost:8003/ | python3 -m json.tool || echo "⚠️  Whale Agent not responding"
echo ""

# Test news agent
echo "Testing News Agent..."
curl -s http://localhost:8004/ | python3 -m json.tool || echo "⚠️  News Agent not responding"
echo ""

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Services running:"
echo "  • Coordinator:    http://localhost:8000"
echo "  • Crypto Agent:   http://localhost:8001"
echo "  • Stock Agent:    http://localhost:8002"
echo "  • Whale Agent:    http://localhost:8003"
echo "  • News Agent:     http://localhost:8004"
echo ""
echo "Documentation:"
echo "  • API Docs (Swagger): http://localhost:8000/docs"
echo "  • Full Guide: MULTI_AGENT_SYSTEM.md"
echo ""
echo "To view logs:"
echo "  docker compose logs -f"
echo ""
echo "To stop all services:"
echo "  docker compose down"
echo ""
