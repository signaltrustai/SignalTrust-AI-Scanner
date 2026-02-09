#!/usr/bin/env python3
"""
AI Evolution Engine
===================
Système d'apprentissage continu pour tous les agents IA.
Les agents apprennent quotidiennement et évoluent pour devenir plus puissants.

Features:
- Apprentissage quotidien automatique
- Évolution des modèles
- Amélioration des performances
- Base de connaissances partagée
- Métriques de progression
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Base de connaissances partagée entre tous les agents"""
    
    def __init__(self, storage_path: str = "data/knowledge_base"):
        self.storage_path = storage_path
        self.knowledge: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        os.makedirs(storage_path, exist_ok=True)
        self._load()
    
    def _load(self):
        """Charger la base de connaissances"""
        kb_file = os.path.join(self.storage_path, "knowledge.json")
        if os.path.exists(kb_file):
            try:
                with open(kb_file, 'r') as f:
                    self.knowledge = json.load(f)
                logger.info(f"Knowledge base loaded: {len(self.knowledge)} entries")
            except Exception as e:
                logger.error(f"Error loading knowledge base: {e}")
    
    def _save(self):
        """Sauvegarder la base de connaissances"""
        kb_file = os.path.join(self.storage_path, "knowledge.json")
        try:
            with open(kb_file, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
    
    def add(self, category: str, key: str, value: Any, metadata: Optional[Dict] = None):
        """Ajouter une connaissance"""
        with self.lock:
            if category not in self.knowledge:
                self.knowledge[category] = {}
            
            self.knowledge[category][key] = {
                "value": value,
                "metadata": metadata or {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "access_count": 0
            }
            self._dirty = True
            # Batch saves - only flush every 10 additions
            if not hasattr(self, '_add_count'):
                self._add_count = 0
            self._add_count += 1
            if self._add_count >= 10:
                self._save()
                self._add_count = 0
    
    def get(self, category: str, key: str) -> Optional[Any]:
        """Récupérer une connaissance"""
        with self.lock:
            if category in self.knowledge and key in self.knowledge[category]:
                entry = self.knowledge[category][key]
                entry["access_count"] += 1
                entry["last_accessed"] = datetime.now(timezone.utc).isoformat()
                return entry["value"]
            return None
    
    def search(self, category: str, query: str) -> List[Dict]:
        """Rechercher dans une catégorie"""
        with self.lock:
            if category not in self.knowledge:
                return []
            
            results = []
            for key, entry in self.knowledge[category].items():
                if query.lower() in key.lower() or query.lower() in str(entry["value"]).lower():
                    results.append({
                        "key": key,
                        "value": entry["value"],
                        "metadata": entry["metadata"]
                    })
            return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Statistiques de la base de connaissances"""
        with self.lock:
            total_entries = sum(len(cat) for cat in self.knowledge.values())
            categories = list(self.knowledge.keys())
            
            return {
                "total_entries": total_entries,
                "categories": len(categories),
                "category_list": categories,
                "size_bytes": os.path.getsize(
                    os.path.join(self.storage_path, "knowledge.json")
                ) if os.path.exists(os.path.join(self.storage_path, "knowledge.json")) else 0
            }


class LearningMetrics:
    """Métriques d'apprentissage pour un agent"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.accuracy_history: List[float] = []
        self.prediction_counts: Dict[str, int] = defaultdict(int)
        self.correct_predictions: Dict[str, int] = defaultdict(int)
        self.response_times: List[float] = []
        self.evolution_level = 1
        self.experience_points = 0
        self.lock = threading.RLock()
    
    def record_prediction(self, prediction_type: str, correct: bool, response_time: float):
        """Enregistrer une prédiction"""
        with self.lock:
            self.prediction_counts[prediction_type] += 1
            if correct:
                self.correct_predictions[prediction_type] += 1
                self.experience_points += 10
            else:
                self.experience_points += 1
            
            self.response_times.append(response_time)
            
            # Calculer accuracy
            total = sum(self.prediction_counts.values())
            correct = sum(self.correct_predictions.values())
            accuracy = correct / total if total > 0 else 0
            self.accuracy_history.append(accuracy)
            
            # Évolution level based on XP
            self.evolution_level = 1 + (self.experience_points // 1000)
    
    def get_accuracy(self, prediction_type: Optional[str] = None) -> float:
        """Obtenir le taux de précision"""
        with self.lock:
            if prediction_type:
                total = self.prediction_counts.get(prediction_type, 0)
                correct = self.correct_predictions.get(prediction_type, 0)
                return correct / total if total > 0 else 0.0
            else:
                total = sum(self.prediction_counts.values())
                correct = sum(self.correct_predictions.values())
                return correct / total if total > 0 else 0.0
    
    def get_avg_response_time(self) -> float:
        """Temps de réponse moyen"""
        with self.lock:
            return sum(self.response_times) / len(self.response_times) if self.response_times else 0.0
    
    def get_progress(self) -> Dict[str, Any]:
        """Progression de l'agent"""
        with self.lock:
            return {
                "evolution_level": self.evolution_level,
                "experience_points": self.experience_points,
                "next_level_xp": (self.evolution_level * 1000),
                "progress_percent": (self.experience_points % 1000) / 10,
                "accuracy": self.get_accuracy(),
                "total_predictions": sum(self.prediction_counts.values()),
                "avg_response_time": self.get_avg_response_time()
            }


class AIAgent:
    """Agent IA avec apprentissage continu"""
    
    def __init__(
        self,
        name: str,
        role: str,
        specialization: str,
        knowledge_base: KnowledgeBase
    ):
        self.name = name
        self.role = role
        self.specialization = specialization
        self.knowledge_base = knowledge_base
        self.metrics = LearningMetrics(name)
        self.last_learning = None
        self.is_learning = False
        
        logger.info(f"AI Agent '{name}' initialized - Role: {role}")
    
    def learn(self, data: Dict[str, Any]):
        """Apprendre à partir de nouvelles données"""
        self.is_learning = True
        start_time = time.time()
        
        try:
            # Extraire et stocker les patterns
            for key, value in data.items():
                self.knowledge_base.add(
                    category=f"{self.name}_patterns",
                    key=key,
                    value=value,
                    metadata={
                        "agent": self.name,
                        "specialization": self.specialization
                    }
                )
            
            # Marquer comme appris
            self.last_learning = datetime.now(timezone.utc)
            
            learning_time = time.time() - start_time
            logger.info(f"{self.name} learned from {len(data)} data points in {learning_time:.2f}s")
            
            return {
                "success": True,
                "patterns_learned": len(data),
                "learning_time": learning_time
            }
            
        except Exception as e:
            logger.error(f"Learning error for {self.name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            self.is_learning = False
    
    def evolve(self) -> Dict[str, Any]:
        """Évoluer en améliorant les capacités"""
        old_level = self.metrics.evolution_level
        
        # Gagner de l'XP pour l'évolution
        self.metrics.experience_points += 100
        
        # Recalculer le niveau
        new_level = 1 + (self.metrics.experience_points // 1000)
        self.metrics.evolution_level = new_level
        
        evolution_data = {
            "agent": self.name,
            "old_level": old_level,
            "new_level": new_level,
            "improved": new_level > old_level,
            "experience": self.metrics.experience_points
        }
        
        if new_level > old_level:
            logger.info(f"{self.name} evolved to level {new_level}!")
        
        return evolution_data
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Faire une prédiction basée sur l'apprentissage"""
        start_time = time.time()
        
        try:
            # Chercher des patterns similaires
            patterns = self.knowledge_base.search(
                f"{self.name}_patterns",
                str(input_data)
            )
            
            response_time = time.time() - start_time
            
            return {
                "success": True,
                "prediction": self._generate_prediction(input_data, patterns),
                "confidence": self._calculate_confidence(patterns),
                "response_time": response_time,
                "patterns_used": len(patterns)
            }
            
        except Exception as e:
            logger.error(f"Prediction error for {self.name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Any:
        """Générer une prédiction (à surcharger par sous-classes)"""
        if not patterns:
            return "insufficient_data"
        
        # Utiliser le pattern le plus récent
        return patterns[0]["value"] if patterns else None
    
    def _calculate_confidence(self, patterns: List[Dict]) -> float:
        """Calculer la confiance de la prédiction"""
        if not patterns:
            return 0.1
        
        # Plus de patterns = plus de confiance
        confidence = min(0.9, 0.3 + (len(patterns) * 0.1))
        
        # Ajuster par le niveau d'évolution
        confidence *= (1 + (self.metrics.evolution_level * 0.05))
        
        return min(1.0, confidence)
    
    def get_status(self) -> Dict[str, Any]:
        """État actuel de l'agent"""
        return {
            "name": self.name,
            "role": self.role,
            "specialization": self.specialization,
            "is_learning": self.is_learning,
            "last_learning": self.last_learning.isoformat() if self.last_learning else None,
            "progress": self.metrics.get_progress()
        }


class MarketIntelligenceAgent(AIAgent):
    """Agent spécialisé dans l'analyse de marchés et prédictions de tendances"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        symbol = input_data.get("symbol", "UNKNOWN")
        price = input_data.get("price", 0)
        volume = input_data.get("volume", 0)

        trend = "neutral"
        if patterns:
            values = [p["value"] for p in patterns if isinstance(p.get("value"), (int, float))]
            if len(values) >= 2:
                trend = "bullish" if values[-1] > values[0] else "bearish"

        confidence_boost = min(0.2, len(patterns) * 0.02)
        return {
            "symbol": symbol,
            "trend": trend,
            "signal": "buy" if trend == "bullish" else ("sell" if trend == "bearish" else "hold"),
            "price_context": price,
            "volume_context": volume,
            "patterns_analyzed": len(patterns),
            "confidence_boost": confidence_boost,
        }


class UserExperienceAgent(AIAgent):
    """Agent spécialisé dans la personnalisation de l'expérience utilisateur"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        user_id = input_data.get("user_id", "anonymous")
        action = input_data.get("action", "browse")
        preferences = input_data.get("preferences", [])

        recommended_features = ["dashboard", "scanner", "predictions"]
        if patterns:
            for p in patterns:
                val = p.get("value")
                if isinstance(val, str) and val not in recommended_features:
                    recommended_features.append(val)

        return {
            "user_id": user_id,
            "action": action,
            "recommended_features": recommended_features[:5],
            "personalization_level": min(100, 50 + len(patterns) * 5),
            "user_segment": "active" if len(patterns) > 3 else "new",
        }


class RiskManagerAgent(AIAgent):
    """Agent spécialisé dans l'évaluation et la gestion des risques"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        portfolio_value = input_data.get("portfolio_value", 0)
        positions = input_data.get("positions", [])
        volatility = input_data.get("volatility", 0.5)

        risk_score = min(100, max(0, int(volatility * 100)))
        if patterns:
            historical_risks = [
                p["value"] for p in patterns if isinstance(p.get("value"), (int, float))
            ]
            if historical_risks:
                avg_risk = sum(historical_risks) / len(historical_risks)
                risk_score = int((risk_score + avg_risk) / 2)

        if risk_score > 70:
            risk_level = "high"
        elif risk_score > 40:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "portfolio_value": portfolio_value,
            "positions_count": len(positions),
            "recommendation": "reduce_exposure" if risk_level == "high" else "maintain",
            "max_drawdown_estimate": round(volatility * portfolio_value * 0.1, 2) if portfolio_value else 0,
        }


class TradingOptimizerAgent(AIAgent):
    """Agent spécialisé dans l'optimisation des stratégies de trading"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        strategy = input_data.get("strategy", "balanced")
        symbol = input_data.get("symbol", "UNKNOWN")
        entry_price = input_data.get("entry_price", 0)

        optimal_strategy = strategy
        stop_loss_pct = 0.05
        take_profit_pct = 0.10

        if patterns:
            numeric_vals = [p["value"] for p in patterns if isinstance(p.get("value"), (int, float))]
            if numeric_vals:
                avg_val = sum(numeric_vals) / len(numeric_vals)
                if avg_val > 0:
                    take_profit_pct = min(0.20, 0.10 + avg_val * 0.001)
                    stop_loss_pct = max(0.02, 0.05 - avg_val * 0.0005)

        return {
            "symbol": symbol,
            "optimal_strategy": optimal_strategy,
            "entry_price": entry_price,
            "stop_loss": round(entry_price * (1 - stop_loss_pct), 2) if entry_price else 0,
            "take_profit": round(entry_price * (1 + take_profit_pct), 2) if entry_price else 0,
            "position_size_recommendation": "standard",
            "patterns_considered": len(patterns),
        }


class ContentGeneratorAgent(AIAgent):
    """Agent spécialisé dans la génération de contenu personnalisé"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        topic = input_data.get("topic", "market_update")
        audience = input_data.get("audience", "general")
        content_type = input_data.get("content_type", "summary")

        insights = []
        if patterns:
            for p in patterns[:5]:
                val = p.get("value", "")
                if val:
                    insights.append(str(val))

        return {
            "topic": topic,
            "audience": audience,
            "content_type": content_type,
            "insights_used": len(insights),
            "content_ready": len(insights) > 0,
            "data_points": insights[:3],
        }


class SecurityGuardAgent(AIAgent):
    """Agent spécialisé dans la détection de fraudes et menaces"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        activity_type = input_data.get("activity_type", "login")
        ip_address = input_data.get("ip_address", "unknown")
        user_id = input_data.get("user_id", "anonymous")

        threat_score = 0
        anomalies = []

        # Check high-risk activity types regardless of patterns
        if activity_type in ("bulk_trade", "large_withdrawal"):
            threat_score += 20
            anomalies.append("high_risk_activity")

        if patterns:
            known_ips = [p["value"] for p in patterns if isinstance(p.get("value"), str)]
            if ip_address not in known_ips and known_ips:
                threat_score += 30
                anomalies.append("unknown_ip")

        if threat_score > 50:
            action = "block"
        elif threat_score > 20:
            action = "review"
        else:
            action = "allow"

        return {
            "threat_score": min(100, threat_score),
            "action": action,
            "anomalies": anomalies,
            "activity_type": activity_type,
            "user_id": user_id,
        }


class SupportAssistantAgent(AIAgent):
    """Agent spécialisé dans le support automatisé 24/7"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        category = input_data.get("category", "general")

        response = "Please contact our support team for assistance."
        confidence_score = 0.3

        if patterns:
            for p in patterns:
                val = p.get("value", "")
                if isinstance(val, str) and len(val) > 10:
                    response = val
                    confidence_score = 0.7
                    break

        return {
            "query": query,
            "category": category,
            "response": response,
            "confidence": confidence_score,
            "requires_human": confidence_score < 0.5,
            "patterns_matched": len(patterns),
        }


class PatternRecognizerAgent(AIAgent):
    """Agent spécialisé dans l'identification de patterns de marché"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        prices = input_data.get("prices", [])
        symbol = input_data.get("symbol", "UNKNOWN")

        detected_patterns = []
        if len(prices) >= 3:
            if prices[-1] > prices[-2] > prices[-3]:
                detected_patterns.append({"name": "uptrend", "strength": "strong"})
            elif prices[-1] < prices[-2] < prices[-3]:
                detected_patterns.append({"name": "downtrend", "strength": "strong"})
            else:
                detected_patterns.append({"name": "consolidation", "strength": "moderate"})

        if patterns:
            for p in patterns:
                val = p.get("value")
                if isinstance(val, dict) and "name" in val:
                    detected_patterns.append(val)

        return {
            "symbol": symbol,
            "patterns_detected": detected_patterns[:5],
            "total_patterns": len(detected_patterns),
            "historical_patterns_used": len(patterns),
            "analysis_depth": len(prices),
        }


class SentimentAnalyzerAgent(AIAgent):
    """Agent spécialisé dans l'analyse de sentiment du marché"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        text = input_data.get("text", "")
        source = input_data.get("source", "unknown")

        positive_words = {"buy", "bull", "up", "gain", "profit", "growth", "rise", "strong"}
        negative_words = {"sell", "bear", "down", "loss", "crash", "drop", "weak", "decline"}

        words = text.lower().split()
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        total = pos_count + neg_count

        if total > 0:
            score = (pos_count - neg_count) / total
        else:
            score = 0.0

        if score > 0.2:
            sentiment = "positive"
        elif score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "source": source,
            "positive_signals": pos_count,
            "negative_signals": neg_count,
            "historical_context": len(patterns),
        }


class PortfolioManagerAgent(AIAgent):
    """Agent spécialisé dans la gestion et l'optimisation de portefeuille"""

    def _generate_prediction(self, input_data: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        holdings = input_data.get("holdings", {})
        risk_tolerance = input_data.get("risk_tolerance", "moderate")
        total_value = input_data.get("total_value", 0)

        num_holdings = len(holdings)
        diversification = "good" if num_holdings >= 5 else ("moderate" if num_holdings >= 3 else "poor")

        if risk_tolerance == "aggressive":
            target_allocation = {"stocks": 0.7, "crypto": 0.2, "bonds": 0.1}
        elif risk_tolerance == "conservative":
            target_allocation = {"stocks": 0.4, "crypto": 0.05, "bonds": 0.55}
        else:
            target_allocation = {"stocks": 0.55, "crypto": 0.1, "bonds": 0.35}

        return {
            "total_value": total_value,
            "num_holdings": num_holdings,
            "diversification": diversification,
            "risk_tolerance": risk_tolerance,
            "target_allocation": target_allocation,
            "rebalance_needed": diversification == "poor",
            "historical_performance_data": len(patterns),
        }


class AIEvolutionEngine:
    """Moteur d'évolution pour tous les agents IA"""
    
    def __init__(self, storage_path: str = "data/ai_evolution"):
        self.storage_path = storage_path
        self.knowledge_base = KnowledgeBase(storage_path)
        self.agents: Dict[str, AIAgent] = {}
        self.lock = threading.Lock()
        
        os.makedirs(storage_path, exist_ok=True)
        
        # Créer les agents spécialisés
        self._initialize_agents()
        
        logger.info("AI Evolution Engine initialized")
    
    def _initialize_agents(self):
        """Initialiser tous les agents IA spécialisés"""
        
        # 1. Market Intelligence Agent
        self.register_agent(MarketIntelligenceAgent(
            name="MarketIntelligence",
            role="Analyser les marchés et prédire les tendances",
            specialization="market_analysis",
            knowledge_base=self.knowledge_base
        ))
        
        # 2. User Experience Agent
        self.register_agent(UserExperienceAgent(
            name="UserExperience",
            role="Personnaliser l'expérience utilisateur",
            specialization="user_behavior",
            knowledge_base=self.knowledge_base
        ))
        
        # 3. Risk Management Agent
        self.register_agent(RiskManagerAgent(
            name="RiskManager",
            role="Évaluer et gérer les risques",
            specialization="risk_assessment",
            knowledge_base=self.knowledge_base
        ))
        
        # 4. Trading Optimization Agent
        self.register_agent(TradingOptimizerAgent(
            name="TradingOptimizer",
            role="Optimiser les stratégies de trading",
            specialization="trading_optimization",
            knowledge_base=self.knowledge_base
        ))
        
        # 5. Content Generation Agent
        self.register_agent(ContentGeneratorAgent(
            name="ContentGenerator",
            role="Générer du contenu personnalisé",
            specialization="content_creation",
            knowledge_base=self.knowledge_base
        ))
        
        # 6. Security Agent
        self.register_agent(SecurityGuardAgent(
            name="SecurityGuard",
            role="Détecter fraudes et menaces",
            specialization="security_detection",
            knowledge_base=self.knowledge_base
        ))
        
        # 7. Customer Support Agent
        self.register_agent(SupportAssistantAgent(
            name="SupportAssistant",
            role="Support automatisé 24/7",
            specialization="customer_support",
            knowledge_base=self.knowledge_base
        ))
        
        # 8. Pattern Recognition Agent
        self.register_agent(PatternRecognizerAgent(
            name="PatternRecognizer",
            role="Identifier les patterns de marché",
            specialization="pattern_detection",
            knowledge_base=self.knowledge_base
        ))
        
        # 9. Sentiment Analysis Agent
        self.register_agent(SentimentAnalyzerAgent(
            name="SentimentAnalyzer",
            role="Analyser le sentiment du marché",
            specialization="sentiment_analysis",
            knowledge_base=self.knowledge_base
        ))
        
        # 10. Portfolio Manager Agent
        self.register_agent(PortfolioManagerAgent(
            name="PortfolioManager",
            role="Gérer et optimiser le portefeuille",
            specialization="portfolio_management",
            knowledge_base=self.knowledge_base
        ))
    
    def register_agent(self, agent: AIAgent):
        """Enregistrer un nouvel agent"""
        with self.lock:
            self.agents[agent.name] = agent
            logger.info(f"Registered agent: {agent.name} ({agent.role})")
    
    def get_agent(self, name: str) -> Optional[AIAgent]:
        """Obtenir un agent par son nom"""
        return self.agents.get(name)
    
    def daily_learning(self) -> Dict[str, Any]:
        """Apprentissage quotidien pour tous les agents"""
        results = {}
        
        for name, agent in self.agents.items():
            try:
                # Collecter les données d'apprentissage (exemple)
                learning_data = self._collect_learning_data(agent)
                
                # Faire apprendre l'agent
                result = agent.learn(learning_data)
                results[name] = result
                
                # Faire évoluer l'agent
                evolution = agent.evolve()
                results[name]["evolution"] = evolution
                
            except Exception as e:
                logger.error(f"Daily learning error for {name}: {e}")
                results[name] = {"success": False, "error": str(e)}
        
        return {
            "success": True,
            "agents_trained": len(results),
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def flush(self):
        """Flush any pending knowledge base writes to disk."""
        self.knowledge_base._save()
    
    def _collect_learning_data(self, agent: AIAgent) -> Dict[str, Any]:
        """Collecter les données d'apprentissage pour un agent depuis les systèmes réels."""
        data: Dict[str, Any] = {}
        try:
            # Try to get real learning data from the AI learning system
            from ai_learning_system import get_learning_system
            learning = get_learning_system()
            summary = learning.get_learning_summary()
            if summary:
                data["market_regime"] = summary.get("current_regime", "unknown")
                data["total_predictions"] = summary.get("total_predictions", 0)
                data["accuracy"] = summary.get("overall_accuracy", 0)
                models = summary.get("model_performance", {})
                for model_name, perf in list(models.items())[:5]:
                    data[f"model_{model_name}"] = perf
        except Exception:
            pass

        # Fallback: generate baseline patterns if no real data available
        if not data:
            data = {
                f"pattern_{i}": f"baseline_{agent.specialization}_{i}"
                for i in range(5)
            }

        return data
    
    def get_all_status(self) -> Dict[str, Any]:
        """État de tous les agents"""
        with self.lock:
            agents_status = {
                name: agent.get_status()
                for name, agent in self.agents.items()
            }
            
            kb_stats = self.knowledge_base.get_stats()
            
            return {
                "total_agents": len(self.agents),
                "agents": agents_status,
                "knowledge_base": kb_stats,
                "average_level": sum(
                    agent.metrics.evolution_level 
                    for agent in self.agents.values()
                ) / len(self.agents) if self.agents else 0
            }
    
    def evolve_all(self) -> Dict[str, Any]:
        """Faire évoluer tous les agents"""
        results = {}
        
        for name, agent in self.agents.items():
            try:
                evolution = agent.evolve()
                results[name] = evolution
            except Exception as e:
                logger.error(f"Evolution error for {name}: {e}")
                results[name] = {"success": False, "error": str(e)}
        
        return {
            "success": True,
            "agents_evolved": len(results),
            "results": results
        }
    
    def get_agent_by_specialization(self, specialization: str) -> Optional[AIAgent]:
        """Obtenir un agent par sa spécialisation"""
        for agent in self.agents.values():
            if agent.specialization == specialization:
                return agent
        return None


# Global instance
_evolution_engine = None


def get_evolution_engine() -> AIEvolutionEngine:
    """Obtenir l'instance globale du moteur d'évolution"""
    global _evolution_engine
    if _evolution_engine is None:
        _evolution_engine = AIEvolutionEngine()
    return _evolution_engine
