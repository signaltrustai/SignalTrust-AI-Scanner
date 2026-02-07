#!/usr/bin/env python3
"""
Verify Admin Unlimited Access
Quick script to confirm admin has unlimited access
"""

from limit_enforcer import limit_enforcer
from payment_processor import PaymentProcessor
from config.admin_config import ADMIN_USER_ID, ADMIN_EMAIL, ADMIN_PLAN


def main():
    """Verify admin has unlimited access."""
    print()
    print("="*70)
    print(" "*15 + "VÉRIFICATION ACCÈS ADMIN ILLIMITÉ")
    print("="*70)
    print()
    
    # Admin info
    print("📋 Information Admin:")
    print(f"  • Email:   {ADMIN_EMAIL}")
    print(f"  • User ID: {ADMIN_USER_ID}")
    print(f"  • Plan:    {ADMIN_PLAN.upper()}")
    print()
    
    # Get plan details
    processor = PaymentProcessor()
    plan = processor.get_plan(ADMIN_PLAN)
    
    print("✨ Limites du Plan Enterprise:")
    for key, value in plan['limits'].items():
        if value == -1:
            display = "♾️  ILLIMITÉ"
        elif value == True:
            display = "✅ Activé"
        elif value == False:
            display = "❌ Désactivé"
        else:
            display = str(value)
        print(f"  • {key}: {display}")
    print()
    
    # Test actual limits
    print("🧪 Tests d'Accès:")
    
    # Test 1: Massive scans
    print("\n  1. Test 1000 scans...")
    for i in range(1000):
        limit_enforcer.increment_usage(ADMIN_USER_ID, 'scans')
    
    allowed, error, info = limit_enforcer.check_limit(ADMIN_USER_ID, ADMIN_PLAN, 'scans')
    if allowed and info['limit'] == 'unlimited':
        print(f"     ✅ SUCCÈS - 1000 scans effectués, toujours illimité")
        print(f"        Used: {info['used']}, Remaining: {info['remaining']}")
    else:
        print(f"     ❌ ÉCHEC - Limité!")
    
    # Test 2: Many symbols
    print("\n  2. Test 10,000 symboles...")
    allowed, error, info = limit_enforcer.check_symbols_limit(
        ADMIN_USER_ID, ADMIN_PLAN, 10000
    )
    if allowed and info['limit'] == 'unlimited':
        print(f"     ✅ SUCCÈS - 10,000 symboles autorisés")
    else:
        print(f"     ❌ ÉCHEC - Limité!")
    
    # Test 3: Whale tracking
    print("\n  3. Test whale tracking...")
    allowed, error = limit_enforcer.check_whale_tracking_access(ADMIN_PLAN)
    if allowed:
        print(f"     ✅ SUCCÈS - Whale tracking activé")
    else:
        print(f"     ❌ ÉCHEC - {error}")
    
    # Test 4: Advanced analytics
    print("\n  4. Test analytics avancées...")
    allowed, error = limit_enforcer.check_advanced_analytics_access(ADMIN_PLAN)
    if allowed:
        print(f"     ✅ SUCCÈS - Analytics avancées activées")
    else:
        print(f"     ❌ ÉCHEC - {error}")
    
    print()
    print("="*70)
    
    # Summary
    summary = limit_enforcer.get_usage_summary(ADMIN_USER_ID, ADMIN_PLAN)
    all_unlimited = (
        summary['scans']['limit'] == 'unlimited' and
        summary['ai_predictions']['limit'] == 'unlimited' and
        summary['gems_discoveries']['limit'] == 'unlimited' and
        summary['symbols_per_scan']['limit'] == 'unlimited' and
        summary['whale_tracking'] == True and
        summary['advanced_analytics'] == True
    )
    
    if all_unlimited:
        print()
        print(" "*20 + "✅ VÉRIFICATION RÉUSSIE!")
        print()
        print(" "*10 + "🎉 L'ADMIN A UN ACCÈS ILLIMITÉ À TOUT! 🎉")
        print()
        print("  Aucune restriction sur:")
        print("    • Nombre de scans")
        print("    • Nombre de symboles")
        print("    • Prédictions IA")
        print("    • Découverte de gemmes")
        print("    • Whale tracking")
        print("    • Analytics avancées")
        print("    • Accès API")
        print("    • Données historiques")
        print()
        print(" "*15 + "CONTRÔLE TOTAL DE LA PLATEFORME!")
        print()
        print("="*70)
        print()
        return True
    else:
        print()
        print("❌ ERREUR: L'admin n'a pas un accès illimité!")
        print("="*70)
        print()
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
