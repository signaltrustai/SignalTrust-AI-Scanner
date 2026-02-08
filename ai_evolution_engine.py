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
        self.lock = threading.Lock()
    
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
        self.register_agent(AIAgent(
            name="MarketIntelligence",
            role="Analyser les marchés et prédire les tendances",
            specialization="market_analysis",
            knowledge_base=self.knowledge_base
        ))
        
        # 2. User Experience Agent
        self.register_agent(AIAgent(
            name="UserExperience",
            role="Personnaliser l'expérience utilisateur",
            specialization="user_behavior",
            knowledge_base=self.knowledge_base
        ))
        
        # 3. Risk Management Agent
        self.register_agent(AIAgent(
            name="RiskManager",
            role="Évaluer et gérer les risques",
            specialization="risk_assessment",
            knowledge_base=self.knowledge_base
        ))
        
        # 4. Trading Optimization Agent
        self.register_agent(AIAgent(
            name="TradingOptimizer",
            role="Optimiser les stratégies de trading",
            specialization="trading_optimization",
            knowledge_base=self.knowledge_base
        ))
        
        # 5. Content Generation Agent
        self.register_agent(AIAgent(
            name="ContentGenerator",
            role="Générer du contenu personnalisé",
            specialization="content_creation",
            knowledge_base=self.knowledge_base
        ))
        
        # 6. Security Agent
        self.register_agent(AIAgent(
            name="SecurityGuard",
            role="Détecter fraudes et menaces",
            specialization="security_detection",
            knowledge_base=self.knowledge_base
        ))
        
        # 7. Customer Support Agent
        self.register_agent(AIAgent(
            name="SupportAssistant",
            role="Support automatisé 24/7",
            specialization="customer_support",
            knowledge_base=self.knowledge_base
        ))
        
        # 8. Pattern Recognition Agent
        self.register_agent(AIAgent(
            name="PatternRecognizer",
            role="Identifier les patterns de marché",
            specialization="pattern_detection",
            knowledge_base=self.knowledge_base
        ))
        
        # 9. Sentiment Analysis Agent
        self.register_agent(AIAgent(
            name="SentimentAnalyzer",
            role="Analyser le sentiment du marché",
            specialization="sentiment_analysis",
            knowledge_base=self.knowledge_base
        ))
        
        # 10. Portfolio Manager Agent
        self.register_agent(AIAgent(
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
