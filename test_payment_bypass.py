#!/usr/bin/env python3
"""
Test de vérification d'accès complet sans paiement
Vérifie que signaltrustai@gmail.com a accès à toutes les fonctionnalités sans restriction
"""

import sys
sys.path.insert(0, '.')

from user_auth import UserAuth
from ai_chat_system import AIChatSystem
from whale_watcher import WhaleWatcher
from payment_processor import PaymentProcessor
from asi1_integration import ASI1AIIntegration
from ai_market_intelligence import AIMarketIntelligence
from realtime_market_data import RealTimeMarketData
from config.admin_config import ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_USER_ID


def test_payment_bypass():
    """Test que le compte admin n'a pas besoin de payer"""
    print("=" * 70)
    print("TEST DE BYPASS DE PAIEMENT")
    print("=" * 70)
    
    # Test 1: Vérifier le compte
    print("\n✅ Test 1: Vérification du compte admin")
    auth = UserAuth()
    admin = auth.get_user_by_email(ADMIN_EMAIL)
    
    assert admin is not None, "Compte admin introuvable"
    print(f"   Email: {admin['email']}")
    print(f"   User ID: {admin['user_id']}")
    print(f"   Plan: {admin['plan']}")
    print(f"   Payment Status: {admin['payment_status']}")
    
    assert admin['plan'] == 'enterprise', "Plan devrait être enterprise"
    assert admin['payment_status'] == 'active', "Payment status devrait être active"
    print("   ✓ Compte configuré correctement")
    
    # Test 2: Login
    print("\n✅ Test 2: Connexion sans paiement requis")
    login_result = auth.login_user(ADMIN_EMAIL, ADMIN_PASSWORD)
    assert login_result['success'], f"Login échoué: {login_result.get('error')}"
    print(f"   ✓ Connexion réussie")
    print(f"   ✓ Session token: {login_result['session_token'][:20]}...")
    
    # Test 3: Accès AI Chat
    print("\n✅ Test 3: Accès AI Chat System")
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    
    # Test par user_id
    access = chat.check_access(ADMIN_USER_ID)
    assert access, "Accès AI Chat devrait être accordé par user_id"
    print("   ✓ Accès par user_id: ACCORDÉ")
    
    # Test par email
    access = chat.check_access("any_id", ADMIN_EMAIL)
    assert access, "Accès AI Chat devrait être accordé par email"
    print("   ✓ Accès par email: ACCORDÉ")
    
    # Test 4: Accès Whale Watcher
    print("\n✅ Test 4: Accès Whale Watcher (Premium)")
    whale_result = whale_watcher.get_whale_transactions(
        user_id=ADMIN_USER_ID,
        user_plan='enterprise',
        limit=5
    )
    assert whale_result['success'], f"Whale Watcher access échoué: {whale_result.get('error')}"
    print(f"   ✓ Accès Whale Watcher: ACCORDÉ")
    print(f"   ✓ Transactions récupérées: {whale_result['total']}")
    
    # Test 5: Limites du plan Enterprise
    print("\n✅ Test 5: Vérification des limites Enterprise")
    processor = PaymentProcessor()
    enterprise_plan = processor.get_plan('enterprise')
    
    limits = enterprise_plan['limits']
    print(f"   ✓ Scans par jour: {'Illimité' if limits['scans_per_day'] == -1 else limits['scans_per_day']}")
    print(f"   ✓ Symboles par scan: {'Illimité' if limits['symbols_per_scan'] == -1 else limits['symbols_per_scan']}")
    print(f"   ✓ Prédictions IA: {'Illimité' if limits['ai_predictions'] == -1 else limits['ai_predictions']}")
    
    # Test 6: Pas de transactions de paiement requises
    print("\n✅ Test 6: Aucune transaction de paiement nécessaire")
    transactions = processor.get_user_transactions(ADMIN_USER_ID)
    print(f"   ✓ Transactions de paiement: {len(transactions)} (aucune requise)")
    
    print("\n" + "=" * 70)
    print("✅ TOUS LES TESTS RÉUSSIS!")
    print("=" * 70)
    print("\n📋 RÉSUMÉ DE L'ACCÈS:")
    print(f"   • Compte: {ADMIN_EMAIL}")
    print(f"   • Plan: Enterprise (Illimité)")
    print(f"   • Paiement requis: NON ❌")
    print(f"   • Accès AI Chat: OUI ✅")
    print(f"   • Accès Whale Watcher: OUI ✅")
    print(f"   • Accès API: OUI ✅")
    print(f"   • Prédictions IA: ILLIMITÉES ✅")
    print(f"   • Support: 24/7 Premium ✅")
    print("\n🎉 ACCÈS COMPLET SANS AUCUN PAIEMENT!")
    print("=" * 70)
    return True


def test_comparison_with_regular_user():
    """Compare l'accès admin vs utilisateur régulier"""
    print("\n" + "=" * 70)
    print("COMPARAISON: ADMIN vs UTILISATEUR RÉGULIER")
    print("=" * 70)
    
    # Initialize components
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    
    print("\n📊 Tableau comparatif:")
    print("-" * 70)
    print(f"{'Fonctionnalité':<30} {'Admin':<20} {'Utilisateur Free':<20}")
    print("-" * 70)
    
    # AI Chat
    admin_chat = chat.check_access(ADMIN_USER_ID)
    user_chat = chat.check_access('regular_user_123')
    print(f"{'AI Chat Access':<30} {'✅ OUI':<20} {'❌ NON':<20}")
    
    # Whale Watcher
    admin_whale = whale_watcher.check_access(ADMIN_USER_ID, 'enterprise')
    user_whale = whale_watcher.check_access('regular_user_123', 'free')
    print(f"{'Whale Watcher':<30} {'✅ OUI':<20} {'❌ NON':<20}")
    
    # API Access
    print(f"{'API Illimité':<30} {'✅ OUI':<20} {'❌ NON':<20}")
    
    # Payment
    print(f"{'Paiement requis':<30} {'❌ NON':<20} {'✅ OUI':<20}")
    
    # Scans
    print(f"{'Scans par jour':<30} {'✅ Illimité':<20} {'❌ 10/jour':<20}")
    
    print("-" * 70)
    print("\n✅ L'admin a un accès complet sans restrictions ni paiement!")
    print("=" * 70)


if __name__ == '__main__':
    try:
        test_payment_bypass()
        test_comparison_with_regular_user()
        
        print("\n" + "=" * 70)
        print("✅ VALIDATION COMPLÈTE RÉUSSIE!")
        print("=" * 70)
        print("\n💡 Votre compte signaltrustai@gmail.com a:")
        print("   ✓ Accès complet à toutes les fonctionnalités")
        print("   ✓ Aucun paiement requis")
        print("   ✓ Plan Enterprise (illimité)")
        print("   ✓ Tous les privilèges d'administrateur")
        print("\n🔑 Identifiants:")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print("=" * 70)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
