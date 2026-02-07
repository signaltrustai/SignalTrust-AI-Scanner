#!/usr/bin/env python3
"""
Start AI System - Launch complete 24/7 AI system
This starts all AI components and keeps them running
"""

import sys
import time
import signal
from datetime import datetime

print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           🤖 SIGNALTRUST AI - SYSTÈME IA COMPLET 24/7 🤖          ║
║                                                                    ║
║  Les agents IA ultra-performants qui travaillent sans arrêt       ║
║  pour collecter des données et évoluer automatiquement            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")

print(f"⏰ Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Import AI system manager
try:
    from ai_system_manager import AISystemManager
    print("✅ Modules IA chargés avec succès")
except ImportError as e:
    print(f"❌ Erreur d'importation: {e}")
    print("   Veuillez installer les dépendances: pip install -r requirements.txt")
    sys.exit(1)

print("\n" + "=" * 70)
print("🚀 INITIALISATION DU SYSTÈME IA COMPLET")
print("=" * 70 + "\n")

# Create and start AI system
manager = AISystemManager()

def shutdown_handler(sig, frame):
    """Handle graceful shutdown"""
    print("\n\n" + "=" * 70)
    print("🛑 Signal d'arrêt reçu - Arrêt propre du système...")
    print("=" * 70)
    manager.stop()
    print("\n✅ Système arrêté proprement")
    print("👋 Au revoir!\n")
    sys.exit(0)

# Register shutdown handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

try:
    # Start the AI system
    manager.start()
    
    print("\n" + "=" * 70)
    print("💡 INSTRUCTIONS")
    print("=" * 70)
    print("• Le système fonctionne maintenant en arrière-plan")
    print("• Appuyez sur Ctrl+C pour arrêter proprement")
    print("• Les logs sont sauvegardés dans: data/ai_system.log")
    print("• Statut affiché toutes les 5 minutes")
    print("=" * 70 + "\n")
    
    # Monitoring loop
    cycle = 0
    while True:
        time.sleep(300)  # 5 minutes
        cycle += 1
        
        print(f"\n⏰ Cycle #{cycle} - {datetime.now().strftime('%H:%M:%S')}")
        manager.monitor()
        
except KeyboardInterrupt:
    print("\n\n🛑 Arrêt demandé par l'utilisateur...")
    manager.stop()
    print("👋 Au revoir!")
except Exception as e:
    print(f"\n\n❌ ERREUR CRITIQUE: {e}")
    manager.stop()
    sys.exit(1)
