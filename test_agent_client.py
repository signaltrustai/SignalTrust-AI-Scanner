#!/usr/bin/env python3
"""
Test script for Agent Integration
Tests the agent_client module and Flask API endpoints
"""

import sys
import requests
import json
import pytest
from agent_client import get_agent_client


@pytest.fixture
def client():
    """Pytest fixture providing AgentClient instance."""
    return get_agent_client()

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_agent_client():
    """Test the AgentClient class"""
    print_section("Testing AgentClient Module")
    
    try:
        client = get_agent_client()
        print("✅ AgentClient initialized successfully")
        
        # Test configuration
        print(f"   Base URL: {client.base_url}")
        print(f"   Timeout: {client.timeout}s")
        print(f"   Number of agents: {len(client.agent_ports)}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize AgentClient: {e}")
        return False

def test_health_checks(client):
    """Test health check functionality"""
    print_section("Testing Agent Health Checks")
    
    try:
        # Check individual agents
        agents = ["coordinator", "crypto", "stock", "whale", "news"]
        
        for agent in agents:
            result = client.check_health(agent)
            status = "✅ Online" if result.get("success") else "❌ Offline"
            print(f"   {agent.capitalize()}: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_flask_api():
    """Test Flask API endpoints"""
    print_section("Testing Flask API Endpoints")
    
    base_url = "http://localhost:5000"
    
    # Test endpoints
    endpoints = [
        ("GET", "/api/agents/status", None),
        ("POST", "/api/agents/crypto/analyze", {"symbol": "BTC/USDT"}),
        ("POST", "/api/agents/stock/analyze", {"ticker": "AAPL"}),
    ]
    
    results = []
    for method, endpoint, data in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                response = requests.post(
                    f"{base_url}{endpoint}",
                    json=data,
                    timeout=5
                )
            
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {method} {endpoint}: HTTP {response.status_code}")
            results.append(response.status_code == 200)
            
        except requests.ConnectionError:
            print(f"   ⚠️  {method} {endpoint}: Flask app not running")
            results.append(False)
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: {str(e)}")
            results.append(False)
    
    return any(results)

def test_agent_methods(client):
    """Test specific agent methods"""
    print_section("Testing Agent Methods")
    
    tests = [
        ("Crypto Analysis", lambda: client.analyze_crypto("BTC/USDT")),
        ("Stock Analysis", lambda: client.analyze_stock("AAPL")),
        ("Whale Watch", lambda: client.watch_whales("btc", 5_000_000)),
        ("News Fetch", lambda: client.get_news(["crypto"], 5)),
    ]
    
    results = []
    for name, func in tests:
        try:
            result = func()
            if isinstance(result, dict):
                status = "✅" if result.get("success") is not False else "⚠️"
                print(f"   {status} {name}")
                results.append(True)
            else:
                print(f"   ❌ {name}: Invalid response type")
                results.append(False)
        except Exception as e:
            print(f"   ⚠️  {name}: {str(e)}")
            results.append(False)
    
    return any(results)

def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  SignalTrust AI - Agent Integration Test")
    print("=" * 60)
    
    results = []
    
    # Test 1: AgentClient initialization
    if test_agent_client():
        client = get_agent_client()
        results.append(True)
        
        # Test 2: Health checks
        results.append(test_health_checks(client))
        
        # Test 3: Agent methods
        results.append(test_agent_methods(client))
    else:
        results.append(False)
    
    # Test 4: Flask API
    results.append(test_flask_api())
    
    # Summary
    print_section("Test Summary")
    passed = sum(results)
    total = len(results)
    print(f"\n   Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n   ✅ All tests passed!")
        print("\n   Next steps:")
        print("   1. Start Docker agents: docker compose up -d")
        print("   2. Start Flask app: python3 app.py")
        print("   3. Visit: http://localhost:5000/agents")
        return 0
    elif passed > 0:
        print("\n   ⚠️  Some tests failed")
        print("\n   Note: This is expected if agents are not running.")
        print("   To start agents: docker compose up -d")
        return 1
    else:
        print("\n   ❌ All tests failed")
        print("\n   Troubleshooting:")
        print("   - Check if Docker is installed: docker --version")
        print("   - Check if .env file exists with API keys")
        print("   - Check Python dependencies: pip install -r requirements.txt")
        return 2

if __name__ == "__main__":
    sys.exit(main())
