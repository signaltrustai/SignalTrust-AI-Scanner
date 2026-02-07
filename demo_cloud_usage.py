#!/usr/bin/env python3
"""
Démonstration d'utilisation du Cloud Storage System
Montre comment les IA peuvent accéder aux backups
"""

from cloud_storage_manager import cloud_storage
from datetime import datetime


def demo_create_backup():
    """Demo: Créer un backup."""
    print("=" * 80)
    print("📦 DEMO: Créer un Backup Unifié")
    print("=" * 80)
    
    backup = cloud_storage.backup_all_data()
    
    print(f"\n✅ Backup créé avec succès!")
    print(f"   ID: {backup['backup_id']}")
    print(f"   Taille: {backup['size_bytes'] / 1024 / 1024:.2f}MB")
    print(f"   Compressé: {backup.get('compressed', True)}")
    print(f"   Path: {backup['local_path']}")
    
    return backup['backup_id']


def demo_list_backups():
    """Demo: Lister les backups."""
    print("\n" + "=" * 80)
    print("📋 DEMO: Lister les Backups Disponibles")
    print("=" * 80)
    
    backups = cloud_storage.list_backups(limit=5)
    
    print(f"\n✅ {len(backups)} backups trouvés:")
    for i, backup in enumerate(backups, 1):
        print(f"\n   {i}. {backup['backup_id']}")
        print(f"      Timestamp: {backup['timestamp']}")
        print(f"      Taille: {backup['size_bytes'] / 1024:.1f}KB")
        print(f"      Cloud sync: {'✅' if backup['cloud_synced'] else '⏳ Pending'}")


def demo_load_backup(backup_id):
    """Demo: Charger un backup."""
    print("\n" + "=" * 80)
    print("📂 DEMO: Charger un Backup")
    print("=" * 80)
    
    data = cloud_storage.get_backup(backup_id)
    
    if not data:
        print("❌ Backup non trouvé!")
        return
    
    print(f"\n✅ Backup chargé: {backup_id}")
    print(f"   Version: {data['version']}")
    print(f"   Timestamp: {data['timestamp']}")
    
    print("\n📊 Sources de données:")
    for source, content in data['data_sources'].items():
        if isinstance(content, dict):
            print(f"   • {source}: {len(content)} items")
        elif isinstance(content, list):
            print(f"   • {source}: {len(content)} items")
        else:
            print(f"   • {source}: data présente")


def demo_ai_access(backup_id):
    """Demo: Comment une IA accède aux données."""
    print("\n" + "=" * 80)
    print("🤖 DEMO: Accès IA aux Données")
    print("=" * 80)
    
    data = cloud_storage.get_backup(backup_id)
    
    if not data:
        print("❌ Backup non trouvé!")
        return
    
    # Exemple 1: Accéder à l'intelligence collective
    ai_hub = data['data_sources'].get('ai_hub', {})
    if ai_hub and 'collective_intelligence' in ai_hub:
        ci = ai_hub['collective_intelligence']
        print("\n🧠 Intelligence Collective:")
        print(f"   IQ Collectif: {ci.get('collective_iq', 0):.1f}")
        print(f"   Précision: {ci.get('collective_accuracy', 0)*100:.1f}%")
        print(f"   Synergy: {ci.get('evolution_synergy', 0):.1f}x")
    
    # Exemple 2: Accéder aux patterns appris
    market_data = data['data_sources'].get('total_market_intelligence', {})
    if market_data and 'learned_patterns' in market_data:
        patterns = market_data['learned_patterns']
        print(f"\n📈 Patterns Appris: {len(patterns)}")
        if patterns:
            print(f"   Dernier pattern: {patterns[-1].get('type', 'N/A')}")
    
    # Exemple 3: Accéder aux gemmes découvertes
    gems = data['data_sources'].get('discovered_gems', {})
    if isinstance(gems, dict) and 'gems' in gems:
        gem_list = gems['gems']
        print(f"\n💎 Gemmes Découvertes: {len(gem_list)}")
        if gem_list:
            top_gem = max(gem_list, key=lambda x: x.get('gem_score', 0))
            print(f"   Top gem: {top_gem.get('symbol', 'N/A')} (score: {top_gem.get('gem_score', 0)})")


def demo_statistics():
    """Demo: Statistiques du système."""
    print("\n" + "=" * 80)
    print("📊 DEMO: Statistiques Cloud Storage")
    print("=" * 80)
    
    stats = cloud_storage.get_statistics()
    
    print(f"\n✅ Statistiques:")
    print(f"   Total backups: {stats['total_backups']}")
    print(f"   Taille totale: {stats['total_size_mb']:.2f}MB")
    print(f"   Cloud syncés: {stats['cloud_synced']}")
    print(f"   Provider: {stats['provider']}")
    print(f"   Compression: {'Activée' if stats['compression_enabled'] else 'Désactivée'}")
    
    if stats.get('last_sync'):
        print(f"   Dernier sync: {stats['last_sync']}")


def demo_query():
    """Demo: Query system."""
    print("\n" + "=" * 80)
    print("🔍 DEMO: Query Backups")
    print("=" * 80)
    
    # Query backups locaux seulement
    local_backups = cloud_storage.query_backups(cloud_synced=False)
    print(f"\n✅ Backups locaux (non-syncés): {len(local_backups)}")
    
    # Query backups syncés
    synced_backups = cloud_storage.query_backups(cloud_synced=True)
    print(f"✅ Backups syncés au cloud: {len(synced_backups)}")


def main():
    """Main demo."""
    print("\n" + "=" * 80)
    print("🌟 DÉMONSTRATION CLOUD STORAGE SYSTEM")
    print("SignalTrust AI - Sauvegardes Accessibles pour IA")
    print("=" * 80)
    
    # 1. Créer backup
    backup_id = demo_create_backup()
    
    # 2. Lister backups
    demo_list_backups()
    
    # 3. Charger backup
    demo_load_backup(backup_id)
    
    # 4. Accès IA
    demo_ai_access(backup_id)
    
    # 5. Statistiques
    demo_statistics()
    
    # 6. Query
    demo_query()
    
    # Résumé
    print("\n" + "=" * 80)
    print("✅ DÉMONSTRATION TERMINÉE")
    print("=" * 80)
    print("\nCe que tu peux faire maintenant:")
    print("   1. Configurer cloud provider dans .env")
    print("   2. Utiliser API: curl http://localhost:5000/api/cloud/status")
    print("   3. Intégrer dans tes IA avec: from cloud_storage_manager import cloud_storage")
    print("\n💡 Les backups se font automatiquement toutes les 24h!")


if __name__ == "__main__":
    main()
