#!/usr/bin/env python3
"""
Script de Vérification Rapide
Vérifie que votre accès gratuit est toujours actif
"""

import sys
sys.path.insert(0, '.')

from user_auth import UserAuth
from config.admin_config import ADMIN_EMAIL, ADMIN_USER_ID

def quick_check():
    """Vérification rapide de l'accès"""
    
    print("╔════════════════════════════════════════════╗")
    print("║  Vérification Rapide - Votre Accès        ║")
    print("╚════════════════════════════════════════════╝")
    
    try:
        auth = UserAuth()
        admin = auth.get_user_by_email(ADMIN_EMAIL)
        
        if not admin:
            print("\n❌ ERREUR: Compte admin introuvable!")
            return False
        
        print(f"\n📧 Email: {admin['email']}")
        print(f"🆔 User ID: {admin['user_id']}")
        print(f"💼 Plan: {admin['plan']}")
        print(f"💰 Payment Status: {admin['payment_status']}")
        
        # Vérifications
        checks = [
            (admin['user_id'] == ADMIN_USER_ID, "User ID correct"),
            (admin['plan'] == 'enterprise', "Plan Enterprise"),
            (admin['payment_status'] == 'active', "Payment status actif"),
            (admin.get('is_active', False), "Compte actif"),
        ]
        
        print("\n🔍 Vérifications:")
        all_ok = True
        for check, label in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {label}")
            if not check:
                all_ok = False
        
        if all_ok:
            print("\n╔════════════════════════════════════════════╗")
            print("║  ✅ TOUT EST OK!                           ║")
            print("║  Votre accès gratuit est actif             ║")
            print("╚════════════════════════════════════════════╝")
            print("\n💡 Vous pouvez utiliser toutes les fonctionnalités sans payer!")
            return True
        else:
            print("\n⚠️  Attention: Certaines vérifications ont échoué")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

if __name__ == '__main__':
    success = quick_check()
    sys.exit(0 if success else 1)
