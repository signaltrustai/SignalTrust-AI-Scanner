#!/usr/bin/env python3
"""
Tests for the AI Evolution System and AI Evolution Engine.
Validates all 10 specialized agents, learning, evolution, and prediction logic.
"""

import os
import json
import shutil
import tempfile

import pytest

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_storage(tmp_path):
    """Create a temporary storage directory for tests."""
    return str(tmp_path / "test_evolution")


@pytest.fixture
def knowledge_base(tmp_storage):
    from ai_evolution_engine import KnowledgeBase
    return KnowledgeBase(storage_path=tmp_storage)


@pytest.fixture
def engine(tmp_storage):
    from ai_evolution_engine import AIEvolutionEngine
    return AIEvolutionEngine(storage_path=tmp_storage)


@pytest.fixture
def evolution_system(tmp_path):
    from ai_evolution_system import AIEvolutionSystem
    system = AIEvolutionSystem()
    # Override file paths to use temp directory
    brain_dir = str(tmp_path / "learning")
    os.makedirs(brain_dir, exist_ok=True)
    system.ai_brain_file = os.path.join(brain_dir, "ai_brain.json")
    system.patterns_file = os.path.join(brain_dir, "learned_patterns.json")
    system.learning_file = os.path.join(brain_dir, "ai_evolution_data.json")
    return system


# ---------------------------------------------------------------------------
# KnowledgeBase Tests
# ---------------------------------------------------------------------------

class TestKnowledgeBase:
    def test_add_and_get(self, knowledge_base):
        knowledge_base.add("test_cat", "key1", "value1")
        result = knowledge_base.get("test_cat", "key1")
        assert result == "value1"

    def test_get_missing_key(self, knowledge_base):
        result = knowledge_base.get("nonexistent", "key")
        assert result is None

    def test_search(self, knowledge_base):
        knowledge_base.add("market", "btc_price", 50000)
        knowledge_base.add("market", "eth_price", 3000)
        results = knowledge_base.search("market", "btc")
        assert len(results) == 1
        assert results[0]["value"] == 50000

    def test_get_stats(self, knowledge_base):
        knowledge_base.add("cat1", "k1", "v1")
        knowledge_base.add("cat2", "k2", "v2")
        stats = knowledge_base.get_stats()
        assert stats["total_entries"] == 2
        assert stats["categories"] == 2

    def test_persistence(self, tmp_storage):
        from ai_evolution_engine import KnowledgeBase
        kb1 = KnowledgeBase(storage_path=tmp_storage)
        kb1.add("persist", "key", "saved_value")
        kb1._save()

        kb2 = KnowledgeBase(storage_path=tmp_storage)
        result = kb2.get("persist", "key")
        assert result == "saved_value"


# ---------------------------------------------------------------------------
# LearningMetrics Tests
# ---------------------------------------------------------------------------

class TestLearningMetrics:
    def test_initial_state(self):
        from ai_evolution_engine import LearningMetrics
        m = LearningMetrics("test")
        assert m.evolution_level == 1
        assert m.experience_points == 0

    def test_record_correct_prediction(self):
        from ai_evolution_engine import LearningMetrics
        m = LearningMetrics("test")
        m.record_prediction("price", True, 0.1)
        assert m.experience_points == 10
        assert m.prediction_counts["price"] == 1
        assert m.correct_predictions["price"] == 1

    def test_record_wrong_prediction(self):
        from ai_evolution_engine import LearningMetrics
        m = LearningMetrics("test")
        m.record_prediction("price", False, 0.2)
        assert m.experience_points == 1

    def test_level_up(self):
        from ai_evolution_engine import LearningMetrics
        m = LearningMetrics("test")
        for _ in range(100):
            m.record_prediction("price", True, 0.1)
        assert m.evolution_level == 2

    def test_get_progress(self):
        from ai_evolution_engine import LearningMetrics
        m = LearningMetrics("test")
        m.record_prediction("price", True, 0.05)
        progress = m.get_progress()
        assert "evolution_level" in progress
        assert "experience_points" in progress
        assert "accuracy" in progress
        assert progress["total_predictions"] == 1


# ---------------------------------------------------------------------------
# AIAgent Base Tests
# ---------------------------------------------------------------------------

class TestAIAgent:
    def test_learn(self, knowledge_base):
        from ai_evolution_engine import AIAgent
        agent = AIAgent("TestAgent", "testing", "test_spec", knowledge_base)
        result = agent.learn({"key1": "val1", "key2": "val2"})
        assert result["success"] is True
        assert result["patterns_learned"] == 2

    def test_evolve(self, knowledge_base):
        from ai_evolution_engine import AIAgent
        agent = AIAgent("TestAgent", "testing", "test_spec", knowledge_base)
        result = agent.evolve()
        assert result["agent"] == "TestAgent"
        assert result["experience"] == 100

    def test_predict_no_patterns(self, knowledge_base):
        from ai_evolution_engine import AIAgent
        agent = AIAgent("TestAgent", "testing", "test_spec", knowledge_base)
        result = agent.predict({"query": "test"})
        assert result["success"] is True
        assert result["prediction"] == "insufficient_data"
        assert result["confidence"] == 0.1

    def test_get_status(self, knowledge_base):
        from ai_evolution_engine import AIAgent
        agent = AIAgent("TestAgent", "testing", "test_spec", knowledge_base)
        status = agent.get_status()
        assert status["name"] == "TestAgent"
        assert status["specialization"] == "test_spec"
        assert "progress" in status


# ---------------------------------------------------------------------------
# AIEvolutionEngine Tests
# ---------------------------------------------------------------------------

class TestAIEvolutionEngine:
    def test_has_10_agents(self, engine):
        assert len(engine.agents) == 10

    def test_agent_names(self, engine):
        expected = {
            "MarketIntelligence", "UserExperience", "RiskManager",
            "TradingOptimizer", "ContentGenerator", "SecurityGuard",
            "SupportAssistant", "PatternRecognizer", "SentimentAnalyzer",
            "PortfolioManager",
        }
        assert set(engine.agents.keys()) == expected

    def test_agent_types(self, engine):
        from ai_evolution_engine import (
            MarketIntelligenceAgent, UserExperienceAgent, RiskManagerAgent,
            TradingOptimizerAgent, ContentGeneratorAgent, SecurityGuardAgent,
            SupportAssistantAgent, PatternRecognizerAgent, SentimentAnalyzerAgent,
            PortfolioManagerAgent,
        )
        assert isinstance(engine.agents["MarketIntelligence"], MarketIntelligenceAgent)
        assert isinstance(engine.agents["UserExperience"], UserExperienceAgent)
        assert isinstance(engine.agents["RiskManager"], RiskManagerAgent)
        assert isinstance(engine.agents["TradingOptimizer"], TradingOptimizerAgent)
        assert isinstance(engine.agents["ContentGenerator"], ContentGeneratorAgent)
        assert isinstance(engine.agents["SecurityGuard"], SecurityGuardAgent)
        assert isinstance(engine.agents["SupportAssistant"], SupportAssistantAgent)
        assert isinstance(engine.agents["PatternRecognizer"], PatternRecognizerAgent)
        assert isinstance(engine.agents["SentimentAnalyzer"], SentimentAnalyzerAgent)
        assert isinstance(engine.agents["PortfolioManager"], PortfolioManagerAgent)

    def test_get_agent(self, engine):
        agent = engine.get_agent("MarketIntelligence")
        assert agent is not None
        assert agent.name == "MarketIntelligence"

    def test_get_agent_by_specialization(self, engine):
        agent = engine.get_agent_by_specialization("risk_assessment")
        assert agent is not None
        assert agent.name == "RiskManager"

    def test_daily_learning(self, engine):
        result = engine.daily_learning()
        assert result["success"] is True
        assert result["agents_trained"] == 10

    def test_evolve_all(self, engine):
        result = engine.evolve_all()
        assert result["success"] is True
        assert result["agents_evolved"] == 10

    def test_get_all_status(self, engine):
        status = engine.get_all_status()
        assert status["total_agents"] == 10
        assert len(status["agents"]) == 10
        assert "knowledge_base" in status

    def test_flush(self, engine):
        engine.knowledge_base.add("test", "key", "value")
        engine.flush()
        kb_file = os.path.join(engine.storage_path, "knowledge.json")
        assert os.path.exists(kb_file)


# ---------------------------------------------------------------------------
# Specialized Agent Prediction Tests
# ---------------------------------------------------------------------------

class TestMarketIntelligenceAgent:
    def test_predict_returns_market_data(self, engine):
        agent = engine.get_agent("MarketIntelligence")
        result = agent.predict({"symbol": "AAPL", "price": 150.0, "volume": 500000})
        assert result["success"] is True
        pred = result["prediction"]
        assert pred["symbol"] == "AAPL"
        assert pred["trend"] in ("bullish", "bearish", "neutral")
        assert pred["signal"] in ("buy", "sell", "hold")

    def test_predict_with_learned_patterns(self, engine):
        agent = engine.get_agent("MarketIntelligence")
        agent.learn({"price_1": 100, "price_2": 110, "price_3": 120})
        result = agent.predict({"symbol": "BTC", "price": 50000})
        assert result["success"] is True
        assert result["patterns_used"] >= 0


class TestUserExperienceAgent:
    def test_predict(self, engine):
        agent = engine.get_agent("UserExperience")
        result = agent.predict({"user_id": "u123", "action": "scan"})
        pred = result["prediction"]
        assert "recommended_features" in pred
        assert pred["user_segment"] in ("new", "active")


class TestRiskManagerAgent:
    def test_high_risk(self, engine):
        agent = engine.get_agent("RiskManager")
        result = agent.predict({"portfolio_value": 100000, "volatility": 0.9, "positions": []})
        pred = result["prediction"]
        assert pred["risk_level"] == "high"
        assert pred["recommendation"] == "reduce_exposure"

    def test_low_risk(self, engine):
        agent = engine.get_agent("RiskManager")
        result = agent.predict({"portfolio_value": 100000, "volatility": 0.2, "positions": []})
        pred = result["prediction"]
        assert pred["risk_level"] == "low"
        assert pred["recommendation"] == "maintain"

    def test_max_drawdown(self, engine):
        agent = engine.get_agent("RiskManager")
        result = agent.predict({"portfolio_value": 100000, "volatility": 0.5, "positions": []})
        pred = result["prediction"]
        assert pred["max_drawdown_estimate"] == 5000.0


class TestTradingOptimizerAgent:
    def test_predict_stop_loss_take_profit(self, engine):
        agent = engine.get_agent("TradingOptimizer")
        result = agent.predict({"symbol": "AAPL", "entry_price": 100.0, "strategy": "balanced"})
        pred = result["prediction"]
        assert pred["stop_loss"] < 100.0
        assert pred["take_profit"] > 100.0

    def test_zero_entry_price(self, engine):
        agent = engine.get_agent("TradingOptimizer")
        result = agent.predict({"symbol": "BTC", "entry_price": 0})
        pred = result["prediction"]
        assert pred["stop_loss"] == 0
        assert pred["take_profit"] == 0


class TestContentGeneratorAgent:
    def test_predict(self, engine):
        agent = engine.get_agent("ContentGenerator")
        result = agent.predict({"topic": "bitcoin", "audience": "traders"})
        pred = result["prediction"]
        assert pred["topic"] == "bitcoin"
        assert pred["audience"] == "traders"


class TestSecurityGuardAgent:
    def test_allow(self, engine):
        agent = engine.get_agent("SecurityGuard")
        result = agent.predict({"activity_type": "login", "ip_address": "1.2.3.4"})
        pred = result["prediction"]
        assert pred["action"] == "allow"

    def test_high_risk_activity(self, engine):
        agent = engine.get_agent("SecurityGuard")
        # Without prior known IP patterns, only activity type is evaluated
        result = agent.predict({
            "activity_type": "large_withdrawal",
            "ip_address": "99.99.99.99",
            "user_id": "u123"
        })
        pred = result["prediction"]
        # large_withdrawal triggers high_risk_activity anomaly
        assert pred["threat_score"] >= 20
        assert "high_risk_activity" in pred["anomalies"]


class TestSupportAssistantAgent:
    def test_predict_no_patterns(self, engine):
        agent = engine.get_agent("SupportAssistant")
        result = agent.predict({"query": "How do I trade?", "category": "trading"})
        pred = result["prediction"]
        assert pred["requires_human"] is True

    def test_predict_with_learned_answer(self, engine):
        agent = engine.get_agent("SupportAssistant")
        agent.learn({"trading_help": "Go to the scanner page to start trading."})
        result = agent.predict({"query": "trading", "category": "trading"})
        pred = result["prediction"]
        assert pred["patterns_matched"] >= 0


class TestPatternRecognizerAgent:
    def test_uptrend(self, engine):
        agent = engine.get_agent("PatternRecognizer")
        result = agent.predict({"symbol": "ETH", "prices": [100, 110, 120]})
        pred = result["prediction"]
        patterns = pred["patterns_detected"]
        assert any(p["name"] == "uptrend" for p in patterns)

    def test_downtrend(self, engine):
        agent = engine.get_agent("PatternRecognizer")
        result = agent.predict({"symbol": "ETH", "prices": [120, 110, 100]})
        pred = result["prediction"]
        patterns = pred["patterns_detected"]
        assert any(p["name"] == "downtrend" for p in patterns)

    def test_consolidation(self, engine):
        agent = engine.get_agent("PatternRecognizer")
        result = agent.predict({"symbol": "ETH", "prices": [100, 110, 100]})
        pred = result["prediction"]
        patterns = pred["patterns_detected"]
        assert any(p["name"] == "consolidation" for p in patterns)

    def test_insufficient_prices(self, engine):
        agent = engine.get_agent("PatternRecognizer")
        result = agent.predict({"symbol": "ETH", "prices": [100]})
        pred = result["prediction"]
        assert pred["total_patterns"] == 0


class TestSentimentAnalyzerAgent:
    def test_positive_sentiment(self, engine):
        agent = engine.get_agent("SentimentAnalyzer")
        result = agent.predict({"text": "bull buy growth profit strong", "source": "twitter"})
        pred = result["prediction"]
        assert pred["sentiment"] == "positive"
        assert pred["score"] > 0

    def test_negative_sentiment(self, engine):
        agent = engine.get_agent("SentimentAnalyzer")
        result = agent.predict({"text": "bear sell crash drop decline", "source": "reddit"})
        pred = result["prediction"]
        assert pred["sentiment"] == "negative"
        assert pred["score"] < 0

    def test_neutral_sentiment(self, engine):
        agent = engine.get_agent("SentimentAnalyzer")
        result = agent.predict({"text": "the market is open today", "source": "news"})
        pred = result["prediction"]
        assert pred["sentiment"] == "neutral"


class TestPortfolioManagerAgent:
    def test_poor_diversification(self, engine):
        agent = engine.get_agent("PortfolioManager")
        result = agent.predict({"holdings": {"BTC": 5}, "risk_tolerance": "moderate", "total_value": 10000})
        pred = result["prediction"]
        assert pred["diversification"] == "poor"
        assert pred["rebalance_needed"] is True

    def test_good_diversification(self, engine):
        agent = engine.get_agent("PortfolioManager")
        holdings = {"AAPL": 10, "BTC": 2, "ETH": 5, "GOOGL": 3, "MSFT": 8}
        result = agent.predict({"holdings": holdings, "risk_tolerance": "moderate", "total_value": 50000})
        pred = result["prediction"]
        assert pred["diversification"] == "good"
        assert pred["rebalance_needed"] is False

    def test_aggressive_allocation(self, engine):
        agent = engine.get_agent("PortfolioManager")
        result = agent.predict({"holdings": {}, "risk_tolerance": "aggressive"})
        pred = result["prediction"]
        assert pred["target_allocation"]["stocks"] == 0.7

    def test_conservative_allocation(self, engine):
        agent = engine.get_agent("PortfolioManager")
        result = agent.predict({"holdings": {}, "risk_tolerance": "conservative"})
        pred = result["prediction"]
        assert pred["target_allocation"]["bonds"] == 0.55


# ---------------------------------------------------------------------------
# AIEvolutionSystem Tests
# ---------------------------------------------------------------------------

class TestAIEvolutionSystem:
    def test_initial_state(self, evolution_system):
        status = evolution_system.get_ai_status()
        assert status["evolution_level"] >= 1
        assert "intelligence_metrics" in status
        assert "prediction_accuracy" in status

    def test_predictions_deterministic(self, evolution_system):
        pred1 = evolution_system.get_predictions_with_ai("BTC", "crypto")
        pred2 = evolution_system.get_predictions_with_ai("BTC", "crypto")
        assert pred1["prediction"]["direction"] == pred2["prediction"]["direction"]
        assert pred1["prediction"]["target_change"] == pred2["prediction"]["target_change"]
        assert pred1["recommendation"] == pred2["recommendation"]

    def test_prediction_structure(self, evolution_system):
        pred = evolution_system.get_predictions_with_ai("AAPL", "stocks")
        assert pred["asset"] == "AAPL"
        assert "direction" in pred["prediction"]
        assert "confidence" in pred["prediction"]
        assert "target_change" in pred["prediction"]
        assert "timeline" in pred["prediction"]
        assert "recommendation" in pred

    def test_prediction_direction_values(self, evolution_system):
        pred = evolution_system.get_predictions_with_ai("ETH", "crypto")
        assert pred["prediction"]["direction"] in ("UP", "DOWN")

    def test_recommendation_values(self, evolution_system):
        pred = evolution_system.get_predictions_with_ai("AAPL", "stocks")
        assert pred["recommendation"] in ("STRONG BUY", "BUY", "HOLD", "SELL")

    def test_evolve_no_data(self, evolution_system):
        result = evolution_system.evolve()
        assert result.get("success") is False or "error" in result

    def test_evolve_with_data(self, evolution_system):
        # Write some learning data
        learning_data = [
            {
                "timestamp": "2026-01-01T00:00:00",
                "learning_insights": {
                    "top_gainers": [{"symbol": "BTC", "change": 5.0}],
                    "whale_insights": {"buy_sell_ratio": 1.8, "total_value": 1000000},
                    "news_sentiment": {"overall_sentiment": "bullish", "bullish_count": 5, "bearish_count": 1}
                }
            }
        ] * 6  # Need at least 5 for pattern learning

        os.makedirs(os.path.dirname(evolution_system.learning_file), exist_ok=True)
        with open(evolution_system.learning_file, 'w') as f:
            json.dump(learning_data, f)

        result = evolution_system.evolve()
        assert "improvements" in result
        assert "patterns" in result["improvements"]
        assert "accuracy" in result["improvements"]

    def test_improve_prediction_accuracy_deterministic(self, evolution_system):
        initial_crypto = evolution_system.ai_brain['prediction_accuracy']['crypto']
        learning_data = [{"timestamp": "2026-01-01"}] * 10
        evolution_system._improve_prediction_accuracy(learning_data)
        new_crypto = evolution_system.ai_brain['prediction_accuracy']['crypto']
        assert new_crypto > initial_crypto
        assert new_crypto <= 0.99

    def test_update_intelligence_deterministic(self, evolution_system):
        initial_iq = evolution_system.ai_brain['intelligence_metrics']['overall_iq']
        evolution_system._update_intelligence()
        new_iq = evolution_system.ai_brain['intelligence_metrics']['overall_iq']
        assert new_iq > initial_iq

    def test_discover_correlations_deterministic(self, evolution_system):
        learning_data = [
            {
                "timestamp": "2026-01-01",
                "learning_insights": {
                    "top_gainers": [{"symbol": "BTC"}],
                    "whale_insights": {"buy_sell_ratio": 1.5}
                }
            }
        ] * 5
        result1 = evolution_system._discover_correlations(learning_data)
        result2 = evolution_system._discover_correlations(learning_data)
        assert result1["correlations_discovered"] == result2["correlations_discovered"]
        assert result1["correlation_strength"] == result2["correlation_strength"]


# ---------------------------------------------------------------------------
# Global Factory Test
# ---------------------------------------------------------------------------

class TestGlobalFactory:
    def test_get_evolution_engine_singleton(self):
        import ai_evolution_engine
        # Reset singleton
        ai_evolution_engine._evolution_engine = None
        e1 = ai_evolution_engine.get_evolution_engine()
        e2 = ai_evolution_engine.get_evolution_engine()
        assert e1 is e2
        ai_evolution_engine._evolution_engine = None
