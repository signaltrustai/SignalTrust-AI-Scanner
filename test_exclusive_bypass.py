#!/usr/bin/env python3
"""
Test de vérification: Bypass UNIQUEMENT pour signaltrustai@gmail.com
Vérifie que les autres utilisateurs DOIVENT PAYER
"""

import sys
sys.path.insert(0, '.')

from user_auth import UserAuth
from ai_chat_system import AIChatSystem
from whale_watcher import WhaleWatcher
from asi1_integration import ASI1AIIntegration
from ai_market_intelligence import AIMarketIntelligence
from realtime_market_data import RealTimeMarketData
from config.admin_config import ADMIN_EMAIL, ADMIN_USER_ID


def test_admin_has_bypass():
    """Test que SEUL l'admin a le bypass"""
    print("=" * 70)
    print("TEST 1: ADMIN A LE BYPASS")
    print("=" * 70)
    
    # Initialize components
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    
    print(f"\n✅ Compte Admin: {ADMIN_EMAIL}")
    
    # Test AI Chat access
    has_chat_access = chat.check_access(ADMIN_USER_ID, ADMIN_EMAIL)
    print(f"   AI Chat Access: {'✅ OUI' if has_chat_access else '❌ NON'}")
    assert has_chat_access, "Admin devrait avoir accès AI Chat"
    
    # Test Whale Watcher access
    whale_result = whale_watcher.get_whale_transactions(
        user_id=ADMIN_USER_ID,
        user_plan='enterprise',
        limit=5
    )
    print(f"   Whale Watcher Access: {'✅ OUI' if whale_result['success'] else '❌ NON'}")
    assert whale_result['success'], "Admin devrait avoir accès Whale Watcher"
    
    # Test user info
    auth = UserAuth()
    admin = auth.get_user_by_email(ADMIN_EMAIL)
    print(f"   Plan: {admin['plan']}")
    print(f"   Payment Status: {admin['payment_status']}")
    print(f"   Paiement Requis: ❌ NON")
    
    print("\n✅ Admin a accès complet sans payer")
    return True


def test_regular_users_must_pay():
    """Test que les utilisateurs réguliers DOIVENT PAYER"""
    print("\n" + "=" * 70)
    print("TEST 2: UTILISATEURS RÉGULIERS DOIVENT PAYER")
    print("=" * 70)
    
    # Initialize components
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    
    # Test plusieurs cas d'utilisateurs réguliers
    test_users = [
        {'email': 'user@example.com', 'user_id': 'user_123', 'plan': 'free'},
        {'email': 'test@test.com', 'user_id': 'user_456', 'plan': 'free'},
        {'email': 'autre@gmail.com', 'user_id': 'user_789', 'plan': 'basic'}
    ]
    
    for user in test_users:
        print(f"\n❌ Utilisateur: {user['email']}")
        
        # Test AI Chat access (devrait être refusé)
        has_chat_access = chat.check_access(user['user_id'], user['email'])
        print(f"   AI Chat Access: {'❌ NON' if not has_chat_access else '⚠️ OUI (ERREUR)'}")
        assert not has_chat_access, f"Utilisateur {user['email']} ne devrait PAS avoir accès AI Chat"
        
        # Test Whale Watcher (devrait être refusé pour plan free/basic)
        if user['plan'] in ['free', 'basic']:
            whale_result = whale_watcher.get_whale_transactions(
                user_id=user['user_id'],
                user_plan=user['plan'],
                limit=5
            )
            print(f"   Whale Watcher Access: {'❌ NON' if not whale_result['success'] else '⚠️ OUI (ERREUR)'}")
            assert not whale_result['success'], f"Utilisateur {user['email']} ne devrait PAS avoir accès Whale Watcher"
            print(f"   Message: {whale_result.get('error', '')}")
        
        print(f"   ✓ Doit payer pour accéder aux fonctionnalités premium")
    
    print("\n✅ Tous les utilisateurs réguliers doivent payer")
    return True


def test_email_verification():
    """Test que seul l'email exact de l'admin fonctionne"""
    print("\n" + "=" * 70)
    print("TEST 3: VÉRIFICATION EMAIL STRICT")
    print("=" * 70)
    
    # Initialize components
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    
    # Emails similaires qui NE DEVRAIENT PAS fonctionner
    fake_emails = [
        'signaltrustai2@gmail.com',
        'signaltrustai@yahoo.com',
        'admin@signaltrust.com',
        'signaltrust@gmail.com',
        'signaltrustai@gmail.co'
    ]
    
    print(f"\n✅ Email Admin Valide: {ADMIN_EMAIL}")
    admin_access = chat.check_access("any_id", ADMIN_EMAIL)
    print(f"   Access: {'✅ OUI' if admin_access else '❌ NON'}")
    assert admin_access, "Admin email devrait avoir accès"
    
    print(f"\n❌ Emails Similaires (DOIVENT être refusés):")
    for email in fake_emails:
        access = chat.check_access("any_id", email)
        status = '✅ Refusé' if not access else '⚠️ ERREUR: Accepté!'
        print(f"   {email:<35} {status}")
        assert not access, f"Email {email} ne devrait PAS avoir accès"
    
    print("\n✅ Seul l'email exact de l'admin fonctionne")
    return True


def test_user_id_verification():
    """Test que seul le user_id exact de l'admin fonctionne"""
    print("\n" + "=" * 70)
    print("TEST 4: VÉRIFICATION USER_ID STRICT")
    print("=" * 70)
    
    # Initialize components
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    
    # User IDs similaires qui NE DEVRAIENT PAS fonctionner
    fake_user_ids = [
        'owner_admin_002',
        'owner_admin',
        'admin_001',
        'owner_001',
        'owner_admin_0001'
    ]
    
    print(f"\n✅ User ID Admin Valide: {ADMIN_USER_ID}")
    admin_access = chat.check_access(ADMIN_USER_ID)
    print(f"   Access: {'✅ OUI' if admin_access else '❌ NON'}")
    assert admin_access, "Admin user_id devrait avoir accès"
    
    print(f"\n❌ User IDs Similaires (DOIVENT être refusés):")
    for user_id in fake_user_ids:
        access = chat.check_access(user_id)
        status = '✅ Refusé' if not access else '⚠️ ERREUR: Accepté!'
        print(f"   {user_id:<35} {status}")
        assert not access, f"User ID {user_id} ne devrait PAS avoir accès"
    
    print("\n✅ Seul le user_id exact de l'admin fonctionne")
    return True


def print_summary():
    """Affiche un résumé clair"""
    print("\n" + "=" * 70)
    print("RÉSUMÉ FINAL")
    print("=" * 70)
    
    print("\n✅ COMPTE AVEC BYPASS (UN SEUL):")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"   User ID: {ADMIN_USER_ID}")
    print("   Paiement requis: ❌ NON")
    print("   Accès complet: ✅ OUI")
    
    print("\n❌ TOUS LES AUTRES COMPTES:")
    print("   Paiement requis: ✅ OUI")
    print("   Accès complet: ❌ NON (sauf s'ils paient)")
    print("   Plans payants: Trader ($49), Professional ($149), Enterprise ($499)")
    
    print("\n🔒 SÉCURITÉ:")
    print("   ✓ Email vérifié de manière stricte")
    print("   ✓ User ID vérifié de manière stricte")
    print("   ✓ Aucune possibilité de contournement pour les autres")
    
    print("\n" + "=" * 70)
    print("✅ BYPASS EXCLUSIF CONFIRMÉ POUR signaltrustai@gmail.com")
    print("=" * 70)


if __name__ == '__main__':
    try:
        print("=" * 70)
        print("TESTS DE VÉRIFICATION: BYPASS UNIQUEMENT POUR ADMIN")
        print("=" * 70)
        
        # Run all tests
        test_admin_has_bypass()
        test_regular_users_must_pay()
        test_email_verification()
        test_user_id_verification()
        print_summary()
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n💡 Confirmation:")
        print("   ✓ Votre compte a accès complet sans payer")
        print("   ✓ Tous les autres utilisateurs doivent payer")
        print("   ✓ Le système est sécurisé et exclusif")
        print("=" * 70)
        
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n❌ TEST ÉCHOUÉ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
