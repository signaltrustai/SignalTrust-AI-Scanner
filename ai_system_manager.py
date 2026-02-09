#!/usr/bin/env python3
"""
AI System Manager - Manages all AI components
Starts and monitors: Worker Service + Orchestrator + Enhanced AI
"""

import os
import sys
import time
import signal
from datetime import datetime
import logging

logger = logging.getLogger('AISystem')


class AISystemManager:
    """Manages all AI system components"""
    
    def __init__(self):
        """Initialize AI System Manager"""
        self.worker_service = None
        self.orchestrator = None
        self.running = False
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
    def start(self):
        """Start all AI components"""
        if self.running:
            logger.warning("⚠️  AI System already running")
            return
        
        logger.info("=" * 80)
        logger.info("🚀 SIGNALTRUST AI SYSTEM - DÉMARRAGE COMPLET")
        logger.info("=" * 80)
        logger.info("")
        logger.info("🧠 Les agents IA vont maintenant:")
        logger.info("   ✅ Travailler 24/7 sans interruption")
        logger.info("   ✅ Collecter des données en continu")
        logger.info("   ✅ Apprendre et évoluer automatiquement")
        logger.info("   ✅ S'améliorer avec chaque cycle")
        logger.info("   ✅ Optimiser les performances continuellement")
        logger.info("")
        logger.info("=" * 80)
        logger.info("")
        
        # Start Worker Service
        logger.info("🔧 Démarrage du Worker Service (Collecte de données 24/7)...")
        try:
            from ai_worker_service import start_worker
            self.worker_service = start_worker()
            logger.info("✅ Worker Service: ACTIF")
        except Exception as e:
            logger.error(f"❌ Erreur Worker Service: {e}")
        
        logger.info("")
        
        # Start Orchestrator
        logger.info("🎭 Démarrage de l'Orchestrateur (Coordination des agents)...")
        try:
            from ai_orchestrator import start_orchestrator
            self.orchestrator = start_orchestrator()
            logger.info("✅ Orchestrateur: ACTIF")
        except Exception as e:
            logger.error(f"❌ Erreur Orchestrateur: {e}")
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("✅ SYSTÈME IA COMPLÈTEMENT OPÉRATIONNEL!")
        logger.info("=" * 80)
        logger.info("")
        logger.info("📊 Les IA travaillent maintenant 24/7 en arrière-plan")
        logger.info("🔄 Elles accumulent des données et évoluent automatiquement")
        logger.info("📈 Les performances s'amélioreront continuellement")
        logger.info("")
        
        self.running = True
        
    def stop(self):
        """Stop all AI components"""
        logger.info("")
        logger.info("=" * 80)
        logger.info("🛑 Arrêt du système IA...")
        logger.info("=" * 80)
        
        # Stop Worker
        if self.worker_service:
            try:
                from ai_worker_service import stop_worker
                stop_worker()
                logger.info("✅ Worker Service arrêté")
            except Exception as e:
                logger.error(f"❌ Erreur arrêt Worker: {e}")
        
        # Stop Orchestrator
        if self.orchestrator:
            try:
                from ai_orchestrator import stop_orchestrator
                stop_orchestrator()
                logger.info("✅ Orchestrateur arrêté")
            except Exception as e:
                logger.error(f"❌ Erreur arrêt Orchestrator: {e}")
        
        self.running = False
        logger.info("👋 Système IA arrêté proprement")
    
    def get_status(self) -> dict:
        """Get status of all components"""
        status = {
            'running': self.running,
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # Worker status
        try:
            from ai_worker_service import get_worker_status
            status['components']['worker'] = get_worker_status()
        except Exception as e:
            status['components']['worker'] = {'error': str(e)}
        
        # Orchestrator status
        try:
            from ai_orchestrator import get_orchestrator_status
            status['components']['orchestrator'] = get_orchestrator_status()
        except Exception as e:
            status['components']['orchestrator'] = {'error': str(e)}
        
        return status
    
    def monitor(self):
        """Monitor and display status"""
        logger.info("\n📊 ═══════════════════════════════════════════════════════════")
        logger.info("   STATUT DU SYSTÈME IA")
        logger.info("   ═══════════════════════════════════════════════════════════")
        
        status = self.get_status()
        
        # Worker status
        if 'worker' in status['components']:
            worker = status['components']['worker']
            if 'error' not in worker:
                logger.info(f"\n   🤖 WORKER SERVICE:")
                logger.info(f"      Status: {worker.get('status', 'N/A')}")
                logger.info(f"      Uptime: {worker.get('uptime', 'N/A')}")
                logger.info(f"      Cycles: {worker.get('total_cycles', 0)}")
                logger.info(f"      Données collectées: {worker.get('data_collected', 0)}")
                logger.info(f"      Prédictions: {worker.get('predictions_made', 0)}")
                logger.info(f"      Précision: {worker.get('current_accuracy', 'N/A')}")
        
        # Orchestrator status
        if 'orchestrator' in status['components']:
            orch = status['components']['orchestrator']
            if 'error' not in orch:
                logger.info(f"\n   🎭 ORCHESTRATEUR:")
                logger.info(f"      Status: {'RUNNING' if orch.get('running') else 'STOPPED'}")
                logger.info(f"      Uptime: {orch.get('uptime', 'N/A')}")
                logger.info(f"      Agents actifs: {orch.get('active_agents', 0)}/{orch.get('total_agents', 0)}")
                logger.info(f"      Tâches: {orch.get('total_tasks', 0)}")
                logger.info(f"      Performance: {orch.get('average_performance', 'N/A')}")
        
        logger.info("\n   ═══════════════════════════════════════════════════════════\n")


# Global system manager
_system_manager = None


def get_system_manager() -> AISystemManager:
    """Get or create system manager"""
    global _system_manager
    if _system_manager is None:
        _system_manager = AISystemManager()
    return _system_manager


def start_ai_system():
    """Start the complete AI system"""
    manager = get_system_manager()
    manager.start()
    return manager


def stop_ai_system():
    """Stop the AI system"""
    manager = get_system_manager()
    manager.stop()


def get_ai_system_status() -> dict:
    """Get AI system status"""
    manager = get_system_manager()
    return manager.get_status()


if __name__ == "__main__":
    """Run AI system standalone"""
    manager = AISystemManager()
    
    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        logger.info("\n🛑 Signal d'arrêt reçu...")
        manager.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start system
    manager.start()
    
    # Monitor loop
    try:
        while True:
            time.sleep(300)  # Monitor every 5 minutes
            manager.monitor()
    except KeyboardInterrupt:
        logger.info("\n🛑 Arrêt demandé...")
        manager.stop()
        logger.info("👋 Au revoir!")
