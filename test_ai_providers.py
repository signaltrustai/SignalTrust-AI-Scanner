#!/usr/bin/env python3
"""
Test AI Provider System — validates all AI providers and coordinator enhancements.

Tests:
- Provider class instantiation (OpenAI, Anthropic, DeepSeek, Gemini, Local)
- AIProviderFactory auto-detection and explicit creation
- MultiAICoordinator worker registration and task specialist mapping
- AIOrchestrator agent configuration with preferred AI assignments
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_all_provider_classes_exist():
    """All 5 AI provider classes can be imported and instantiated."""
    from ai_provider import (
        OpenAIProvider,
        AnthropicProvider,
        DeepSeekProvider,
        GeminiProvider,
        LocalModelProvider,
    )
    # Instantiate with no real keys — should not crash
    providers = [
        OpenAIProvider(api_key="test"),
        AnthropicProvider(api_key="test"),
        DeepSeekProvider(api_key="test"),
        GeminiProvider(api_key="test"),
        LocalModelProvider(model="test"),
    ]
    assert len(providers) == 5
    print("  ✅ All 5 provider classes instantiate without error")
    return True


def test_provider_factory_supports_all_types():
    """AIProviderFactory creates correct provider for each type."""
    from ai_provider import AIProviderFactory, OpenAIProvider, AnthropicProvider
    from ai_provider import DeepSeekProvider, GeminiProvider, LocalModelProvider

    type_map = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'deepseek': DeepSeekProvider,
        'gemini': GeminiProvider,
    }

    for ptype, expected_cls in type_map.items():
        provider = AIProviderFactory.create_provider(ptype, api_key="test")
        assert isinstance(provider, expected_cls), f"{ptype} -> {type(provider)} != {expected_cls}"

    # Local provider does not take api_key
    local = AIProviderFactory.create_provider('local')
    assert isinstance(local, LocalModelProvider)

    print("  ✅ Factory creates correct provider for all 5 types")
    return True


def test_provider_factory_rejects_unknown():
    """AIProviderFactory raises ValueError for unknown provider type."""
    from ai_provider import AIProviderFactory

    try:
        AIProviderFactory.create_provider("nonexistent_provider")
        print("  ❌ Should have raised ValueError")
        return False
    except ValueError:
        print("  ✅ Factory rejects unknown provider type")
        return True


def test_deepseek_provider_attributes():
    """DeepSeek provider has correct defaults."""
    from ai_provider import DeepSeekProvider

    dp = DeepSeekProvider()
    assert dp.model == "deepseek-chat"
    assert dp.base_url == "https://api.deepseek.com/v1"
    assert hasattr(dp, 'generate_response')
    assert hasattr(dp, 'analyze_market_data')

    dp_custom = DeepSeekProvider(model="deepseek-reasoner")
    assert dp_custom.model == "deepseek-reasoner"
    print("  ✅ DeepSeek provider has correct attributes")
    return True


def test_gemini_provider_attributes():
    """Gemini provider has correct defaults."""
    from ai_provider import GeminiProvider

    gp = GeminiProvider()
    assert gp.model == "gemini-2.0-flash"
    assert "generativelanguage.googleapis.com" in gp.base_url
    assert hasattr(gp, 'generate_response')
    assert hasattr(gp, 'analyze_market_data')

    gp_custom = GeminiProvider(model="gemini-2.5-pro")
    assert gp_custom.model == "gemini-2.5-pro"
    print("  ✅ Gemini provider has correct attributes")
    return True


def test_coordinator_worker_priorities():
    """AIWorker.PROVIDER_PRIORITY includes all 6 provider types."""
    from multi_ai_coordinator import AIWorker

    expected_providers = {"openai", "anthropic", "deepseek", "gemini", "ollama", "rule_based"}
    actual_providers = set(AIWorker.PROVIDER_PRIORITY.keys())
    assert expected_providers == actual_providers, f"Missing: {expected_providers - actual_providers}"

    # Verify priority ordering (lower = higher priority)
    assert AIWorker.PROVIDER_PRIORITY["openai"] < AIWorker.PROVIDER_PRIORITY["rule_based"]
    assert AIWorker.PROVIDER_PRIORITY["deepseek"] < AIWorker.PROVIDER_PRIORITY["ollama"]
    print("  ✅ Coordinator worker priorities include all 6 providers")
    return True


def test_coordinator_task_specialists():
    """MultiAICoordinator has expanded task specialist mapping."""
    from multi_ai_coordinator import MultiAICoordinator

    specialists = MultiAICoordinator.TASK_SPECIALISTS

    # Check key specialist assignments
    assert specialists["price_prediction"] == "deepseek", "DeepSeek should handle predictions"
    assert specialists["market_overview"] == "gemini", "Gemini should handle overviews"
    assert specialists["deep_analysis"] == "anthropic", "Anthropic should handle deep analysis"
    assert specialists["sentiment_analysis"] == "openai", "OpenAI should handle sentiment"
    assert specialists["technical_analysis"] == "rule_based", "Rule engine for technicals"
    assert specialists["news_analysis"] == "gemini", "Gemini for news"
    assert specialists["correlation_analysis"] == "deepseek", "DeepSeek for correlations"

    # Minimum 10 specialized task types
    assert len(specialists) >= 10, f"Expected 10+ task types, got {len(specialists)}"
    print("  ✅ Task specialist mapping has 12 optimized assignments")
    return True


def test_orchestrator_agent_preferred_ai():
    """AIOrchestrator agents have preferred_ai assignments."""
    from ai_orchestrator import AIOrchestrator

    orch = AIOrchestrator()

    for agent_id, config in orch.agent_config.items():
        assert 'preferred_ai' in config, f"Agent {agent_id} missing preferred_ai"
        assert config['preferred_ai'] in ('openai', 'anthropic', 'deepseek', 'gemini', 'rule_based'), \
            f"Agent {agent_id} has invalid preferred_ai: {config['preferred_ai']}"

    # Verify specific assignments
    assert orch.agent_config['predictor']['preferred_ai'] == 'openai'
    assert orch.agent_config['pattern_analyzer']['preferred_ai'] == 'deepseek'
    assert orch.agent_config['market_scanner']['preferred_ai'] == 'gemini'
    assert orch.agent_config['learning_agent']['preferred_ai'] == 'anthropic'
    print("  ✅ All orchestrator agents have valid preferred_ai assignments")
    return True


def test_coordinator_registers_rule_engine():
    """Coordinator always registers the rule engine (zero-cost fallback)."""
    from multi_ai_coordinator import get_coordinator

    coord = get_coordinator()
    worker_names = [w.name for w in coord.workers]
    assert "RuleEngine" in worker_names, "RuleEngine must always be registered"
    assert len(coord.workers) >= 1, "At least 1 worker must be available"
    print(f"  ✅ Coordinator has {len(coord.workers)} workers: {worker_names}")
    return True


def run_all_tests():
    """Run all AI provider and coordinator tests."""
    print(f"\n{'='*70}")
    print("AI Provider & Coordinator Enhancement Tests")
    print(f"{'='*70}")

    tests = [
        test_all_provider_classes_exist,
        test_provider_factory_supports_all_types,
        test_provider_factory_rejects_unknown,
        test_deepseek_provider_attributes,
        test_gemini_provider_attributes,
        test_coordinator_worker_priorities,
        test_coordinator_task_specialists,
        test_orchestrator_agent_preferred_ai,
        test_coordinator_registers_rule_engine,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  ❌ {test.__name__} returned False")
        except Exception as e:
            failed += 1
            print(f"  ❌ {test.__name__} raised {type(e).__name__}: {e}")

    print(f"\n{'='*70}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print(f"{'='*70}")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
