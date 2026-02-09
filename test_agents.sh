#!/bin/bash

echo "================================================"
echo "SignalTrust EU - Multi-Agent System Test"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test an endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ PASSED${NC} (HTTP $response)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC} (HTTP $response)"
        ((TESTS_FAILED++))
    fi
}

echo "1. Testing Health Endpoints (9 agents)"
echo "----------------------------"
test_endpoint "Coordinator Health"       "http://localhost:8000/" "GET"
test_endpoint "Crypto Agent Health"      "http://localhost:8001/" "GET"
test_endpoint "Stock Agent Health"       "http://localhost:8002/" "GET"
test_endpoint "Whale Agent Health"       "http://localhost:8003/" "GET"
test_endpoint "News Agent Health"        "http://localhost:8004/" "GET"
test_endpoint "Social Sentiment Health"  "http://localhost:8005/" "GET"
test_endpoint "On-Chain Agent Health"    "http://localhost:8006/" "GET"
test_endpoint "Macro Economics Health"   "http://localhost:8007/" "GET"
test_endpoint "Portfolio Optimizer Health" "http://localhost:8008/" "GET"
echo ""

echo "2. Testing Agent Endpoints"
echo "----------------------------"
test_endpoint "Crypto Prediction" "http://localhost:8001/predict" "POST" '{"symbol":"BTC/USDT"}'
test_endpoint "Stock Prediction" "http://localhost:8002/predict" "POST" '{"ticker":"AAPL"}'
test_endpoint "Whale Monitoring" "http://localhost:8003/whales?network=btc&min_usd=5000000" "GET"
test_endpoint "News Aggregation" "http://localhost:8004/news" "POST" '{"topics":["crypto","stocks"],"max_items":5}'
test_endpoint "Social Sentiment" "http://localhost:8005/analyze" "POST" '{"query":"bitcoin","sources":["twitter","reddit"]}'
test_endpoint "On-Chain Metrics" "http://localhost:8006/analyze" "POST" '{"network":"ethereum","metrics":["tvl","gas"]}'
test_endpoint "Macro Indicators" "http://localhost:8007/indicators" "POST" '{"indicators":["gdp","inflation","unemployment"]}'
test_endpoint "Portfolio Optimize" "http://localhost:8008/optimize" "POST" '{"assets":["BTC","ETH","AAPL"],"risk_tolerance":"medium"}'
echo ""

echo "3. Testing Coordinator"
echo "----------------------------"
test_endpoint "List Agents" "http://localhost:8000/agents" "GET"
test_endpoint "Run Workflow" "http://localhost:8000/run-workflow" "POST" '{
    "symbol": "BTC/USDT",
    "ticker": "AAPL",
    "network": "btc",
    "topics": ["crypto", "stocks"]
}'
echo ""

echo "4. Detailed Workflow Test"
echo "----------------------------"
echo "Running complete market analysis workflow..."
echo ""

response=$(curl -s --max-time 30 -X POST http://localhost:8000/run-workflow \
    -H "Content-Type: application/json" \
    -d '{
        "symbol": "ETH/USDT",
        "ticker": "GOOGL",
        "network": "eth",
        "topics": ["cryptocurrency", "technology", "market"]
    }')

if echo "$response" | python3 -m json.tool > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Workflow returned valid JSON${NC}"
    echo ""
    echo "Workflow Response:"
    echo "$response" | python3 -m json.tool | head -n 30
    echo "..."
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Workflow returned invalid JSON${NC}"
    echo "Response: $response"
    ((TESTS_FAILED++))
fi
echo ""

echo "5. API Documentation Check"
echo "----------------------------"
test_endpoint "Coordinator Swagger"       "http://localhost:8000/docs" "GET"
test_endpoint "Crypto Agent Swagger"      "http://localhost:8001/docs" "GET"
test_endpoint "Stock Agent Swagger"       "http://localhost:8002/docs" "GET"
test_endpoint "Whale Agent Swagger"       "http://localhost:8003/docs" "GET"
test_endpoint "News Agent Swagger"        "http://localhost:8004/docs" "GET"
test_endpoint "Social Sentiment Swagger"  "http://localhost:8005/docs" "GET"
test_endpoint "On-Chain Agent Swagger"    "http://localhost:8006/docs" "GET"
test_endpoint "Macro Economics Swagger"   "http://localhost:8007/docs" "GET"
test_endpoint "Portfolio Optimizer Swagger" "http://localhost:8008/docs" "GET"
echo ""

echo "================================================"
echo "Test Summary"
echo "================================================"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "🎉 SignalTrust EU Multi-Agent System is working correctly!"
    echo ""
    echo "Next steps:"
    echo "  • Access the coordinator API: http://localhost:8000"
    echo "  • View Swagger docs: http://localhost:8000/docs"
    echo "  • Check logs: docker compose logs -f"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  • Check if all services are running: docker compose ps"
    echo "  • View logs: docker compose logs"
    echo "  • Verify .env file has all required API keys"
    echo "  • Try rebuilding: docker compose build --no-cache"
    exit 1
fi
