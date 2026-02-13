#!/usr/bin/env python3
"""
Test Launch Readiness
=====================
Validates that the SignalTrust AI Scanner application is properly configured
and ready for launch. Checks API key configuration, agent setup, core modules,
and Flask app health.
"""

import os
import re
import sys
import json


def test_env_example_has_all_api_keys():
    """Verify .env.example documents all required API keys."""
    with open('.env.example', 'r') as f:
        content = f.read()

    required_keys = [
        'GROQ_API_KEY',
        'ANTHROPIC_API_KEY',
        'COINGECKO_API_KEY',
        'ALPHAVANTAGE_API_KEY',
        'WHALEALERT_API_KEY',
        'NEWS_CATCHER_API_KEY',
        'ETHERSCAN_API_KEY',
        'TWITTER_API_KEY',
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'GLASSNODE_API_KEY',
        'DUNE_API_KEY',
        'FRED_API_KEY',
        'WORLD_BANK_API_KEY',
        'EIA_API_KEY',
    ]

    missing = []
    for key in required_keys:
        if key + '=' not in content:
            missing.append(key)

    print(f"\n{'='*70}")
    print("API Keys in .env.example")
    print(f"{'='*70}")

    if missing:
        print(f"❌ FAIL: Missing API keys in .env.example: {missing}")
        return False
    else:
        print(f"✅ PASS: All {len(required_keys)} API keys documented in .env.example")
        return True


def test_env_render_has_all_api_keys():
    """Verify .env.render documents all required API keys for deployment."""
    with open('.env.render', 'r') as f:
        content = f.read()

    required_keys = [
        'GROQ_API_KEY',
        'COINGECKO_API_KEY',
        'ALPHAVANTAGE_API_KEY',
        'WHALEALERT_API_KEY',
        'NEWS_CATCHER_API_KEY',
        'ETHERSCAN_API_KEY',
        'TWITTER_API_KEY',
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'GLASSNODE_API_KEY',
        'DUNE_API_KEY',
        'FRED_API_KEY',
        'WORLD_BANK_API_KEY',
        'EIA_API_KEY',
    ]

    missing = []
    for key in required_keys:
        if key + '=' not in content:
            missing.append(key)

    print(f"\n{'='*70}")
    print("API Keys in .env.render")
    print(f"{'='*70}")

    if missing:
        print(f"❌ FAIL: Missing API keys in .env.render: {missing}")
        return False
    else:
        print(f"✅ PASS: All {len(required_keys)} API keys documented in .env.render")
        return True


def test_docker_compose_agent_env_vars():
    """Verify docker-compose.yml passes required env vars to each agent."""
    with open('docker-compose.yml', 'r') as f:
        content = f.read()

    checks = {
        'crypto_agent': ['GROQ_API_KEY', 'COINGECKO_API_KEY'],
        'stock_agent': ['GROQ_API_KEY', 'ALPHAVANTAGE_API_KEY'],
        'whale_agent': ['GROQ_API_KEY', 'WHALEALERT_API_KEY'],
        'news_agent': ['GROQ_API_KEY', 'NEWS_CATCHER_API_KEY'],
        'social_sentiment_agent': ['GROQ_API_KEY', 'TWITTER_API_KEY'],
        'onchain_agent': ['GLASSNODE_API_KEY', 'DUNE_API_KEY'],
        'macro_economics_agent': ['FRED_API_KEY', 'WORLD_BANK_API_KEY', 'EIA_API_KEY'],
    }

    print(f"\n{'='*70}")
    print("Docker Compose Agent Environment Variables")
    print(f"{'='*70}")

    all_pass = True
    for agent, keys in checks.items():
        for key in keys:
            if f'{key}=${{{key}}}' not in content:
                print(f"  ❌ {agent}: missing ${{{key}}}")
                all_pass = False

    if all_pass:
        print(f"✅ PASS: All agent env vars properly configured in docker-compose.yml")
    else:
        print(f"❌ FAIL: Some env vars missing in docker-compose.yml")

    return all_pass


def test_key_validator_patterns():
    """Verify key_validator.py has patterns for all API keys."""
    with open('config/api_keys/key_validator.py', 'r') as f:
        content = f.read()

    required_patterns = [
        'GROQ_API_KEY',
        'ANTHROPIC_API_KEY',
        'COINGECKO_API_KEY',
        'ALPHAVANTAGE_API_KEY',
        'WHALEALERT_API_KEY',
        'NEWS_CATCHER_API_KEY',
        'ETHERSCAN_API_KEY',
        'TWITTER_API_KEY',
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'GLASSNODE_API_KEY',
        'DUNE_API_KEY',
        'FRED_API_KEY',
        'WORLD_BANK_API_KEY',
        'EIA_API_KEY',
    ]

    print(f"\n{'='*70}")
    print("Key Validator Patterns")
    print(f"{'='*70}")

    missing = []
    for pattern in required_patterns:
        if f"'{pattern}'" not in content:
            missing.append(pattern)

    if missing:
        print(f"❌ FAIL: Missing validation patterns: {missing}")
        return False
    else:
        print(f"✅ PASS: All {len(required_patterns)} key validation patterns present")
        return True


def test_agent_directories_exist():
    """Verify all agent directories and required files exist."""
    agents = [
        'coordinator',
        'crypto_agent',
        'stock_agent',
        'whale_agent',
        'news_agent',
        'social_sentiment_agent',
        'onchain_agent',
        'macro_economics_agent',
        'portfolio_optimizer_agent',
        'supervisor',
    ]

    print(f"\n{'='*70}")
    print("Agent Directory Structure")
    print(f"{'='*70}")

    all_pass = True
    for agent in agents:
        agent_dir = os.path.join('agents', agent)
        if not os.path.isdir(agent_dir):
            print(f"  ❌ Missing directory: {agent_dir}")
            all_pass = False
            continue

        # Check for required files
        has_dockerfile = os.path.isfile(os.path.join(agent_dir, 'Dockerfile'))
        has_requirements = os.path.isfile(os.path.join(agent_dir, 'requirements.txt'))
        has_main = os.path.isfile(os.path.join(agent_dir, 'main.py'))
        has_supervisor = os.path.isfile(os.path.join(agent_dir, 'supervisor.py'))

        if has_dockerfile and has_requirements and (has_main or has_supervisor):
            print(f"  ✅ {agent}: OK")
        else:
            missing = []
            if not has_dockerfile:
                missing.append('Dockerfile')
            if not has_requirements:
                missing.append('requirements.txt')
            if not has_main and not has_supervisor:
                missing.append('main.py')
            print(f"  ⚠️  {agent}: missing {missing}")
            # Not a hard failure if supervisor uses supervisor.py instead of main.py
            if agent != 'supervisor':
                all_pass = False

    if all_pass:
        print(f"✅ PASS: All {len(agents)} agent directories properly structured")
    return all_pass


def test_agent_client_all_ports():
    """Verify agent_client.py has port mappings for all agents."""
    with open('agent_client.py', 'r') as f:
        content = f.read()

    required_agents = [
        'coordinator',
        'crypto',
        'stock',
        'whale',
        'news',
        'social_sentiment',
        'onchain',
        'macro_economics',
        'portfolio_optimizer',
    ]

    print(f"\n{'='*70}")
    print("Agent Client Port Mappings")
    print(f"{'='*70}")

    missing = []
    for agent in required_agents:
        if f'"{agent}"' not in content:
            missing.append(agent)

    if missing:
        print(f"❌ FAIL: Missing port mappings: {missing}")
        return False
    else:
        print(f"✅ PASS: All {len(required_agents)} agents have port mappings")
        return True


def test_core_modules_import():
    """Test that all core modules can be imported."""
    print(f"\n{'='*70}")
    print("Core Module Imports")
    print(f"{'='*70}")

    modules = [
        'ai_provider',
        'market_scanner',
        'market_analyzer',
        'ai_predictor',
        'user_auth',
        'payment_processor',
        'agent_client',
        'api_processor',
        'notification_center',
    ]

    all_pass = True
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except Exception as e:
            print(f"  ❌ {module_name}: {e}")
            all_pass = False

    if all_pass:
        print(f"✅ PASS: All {len(modules)} core modules import successfully")
    return all_pass


def test_flask_app_health():
    """Test Flask app starts and health endpoint works."""
    print(f"\n{'='*70}")
    print("Flask App Health Check")
    print(f"{'='*70}")

    try:
        os.environ['DEBUG'] = 'false'
        os.environ.setdefault('SECRET_KEY', 'test-secret-key-launch-readiness')
        from app import app as flask_app

        client = flask_app.test_client()

        # Health endpoint
        resp = client.get('/health')
        if resp.status_code != 200:
            print(f"  ❌ /health returned {resp.status_code}")
            return False

        data = resp.get_json()
        if data.get('status') != 'healthy':
            print(f"  ❌ /health status is not 'healthy': {data}")
            return False

        print(f"  ✅ /health: {data['status']}")

        # Home page
        resp = client.get('/')
        if resp.status_code != 200:
            print(f"  ❌ / returned {resp.status_code}")
            return False
        print(f"  ✅ / : {resp.status_code} ({len(resp.data)} bytes)")

        # Markets overview
        resp = client.get('/api/markets/overview')
        if resp.status_code != 200:
            print(f"  ❌ /api/markets/overview returned {resp.status_code}")
            return False
        print(f"  ✅ /api/markets/overview: {resp.status_code}")

        print(f"✅ PASS: Flask app is healthy and responding")
        return True

    except Exception as e:
        print(f"❌ FAIL: Flask app error: {e}")
        return False


def test_docker_compose_override_has_all_agents():
    """Verify docker-compose.override.yml.example includes all agents."""
    with open('docker-compose.override.yml.example', 'r') as f:
        content = f.read()

    agents = [
        'coordinator',
        'crypto_agent',
        'stock_agent',
        'whale_agent',
        'news_agent',
        'social_sentiment_agent',
        'onchain_agent',
        'macro_economics_agent',
        'portfolio_optimizer_agent',
    ]

    print(f"\n{'='*70}")
    print("Docker Compose Override Agent Coverage")
    print(f"{'='*70}")

    missing = []
    for agent in agents:
        if f'{agent}:' not in content:
            missing.append(agent)

    if missing:
        print(f"❌ FAIL: Missing agents in override: {missing}")
        return False
    else:
        print(f"✅ PASS: All {len(agents)} agents in docker-compose.override.yml.example")
        return True


def main():
    """Run all launch readiness tests."""
    print("\n" + "="*70)
    print("SignalTrust AI Scanner - Launch Readiness Tests")
    print("Validates all API keys, agents, modules, and app health")
    print("="*70)

    tests = [
        ("API Keys in .env.example", test_env_example_has_all_api_keys),
        ("API Keys in .env.render", test_env_render_has_all_api_keys),
        ("Docker Compose Agent Env Vars", test_docker_compose_agent_env_vars),
        ("Key Validator Patterns", test_key_validator_patterns),
        ("Agent Directory Structure", test_agent_directories_exist),
        ("Agent Client Port Mappings", test_agent_client_all_ports),
        ("Core Module Imports", test_core_modules_import),
        ("Flask App Health", test_flask_app_health),
        ("Docker Compose Override Coverage", test_docker_compose_override_has_all_agents),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'='*70}")
    print("Launch Readiness Summary")
    print(f"{'='*70}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🚀 ALL TESTS PASSED! Application is ready for launch!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed - review before launch")
        return 1


if __name__ == "__main__":
    sys.exit(main())
