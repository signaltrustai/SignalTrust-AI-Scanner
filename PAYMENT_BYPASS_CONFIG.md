# Bypass de Paiement - Configuration Exclusive

## ⚠️ IMPORTANT: Bypass Uniquement pour l'Administrateur

Ce document confirme que le **bypass de paiement est UNIQUEMENT actif pour le compte administrateur** et **PAS pour les autres utilisateurs**.

## Compte avec Bypass de Paiement

**UN SEUL COMPTE a accès sans paiement:**

- **Email:** signaltrustai@gmail.com
- **User ID:** owner_admin_001
- **Plan:** Enterprise (Illimité)
- **Payment Status:** active
- **Paiement Requis:** ❌ NON

### Privilèges Exclusifs

Ce compte possède:
- ✅ Accès complet à toutes les fonctionnalités
- ✅ Plan Enterprise sans frais
- ✅ Aucune transaction de paiement requise
- ✅ Accès AI Chat illimité
- ✅ Accès Whale Watcher illimité
- ✅ API sans restrictions
- ✅ Support 24/7 premium

## Tous les Autres Utilisateurs

**Tous les autres comptes (sauf signaltrustai@gmail.com) doivent payer:**

### Utilisateurs Réguliers

Quand quelqu'un d'autre crée un compte:
- Plan par défaut: **free** (limité)
- Payment Status: **pending** (doit payer pour premium)
- Payment Bypass: **❌ NON**
- Paiement requis: **✅ OUI**

### Plans Payants pour les Autres

Les autres utilisateurs doivent payer pour accéder aux plans premium:

1. **Plan Free (Gratuit)**
   - Limité: 10 scans/jour
   - Pas d'accès AI Chat
   - Pas d'accès Whale Watcher
   - Support communauté seulement

2. **Plan Trader ($49/mois)**
   - Scanning illimité
   - 100 prédictions IA/mois
   - Support email
   - **PAIEMENT REQUIS** ✅

3. **Plan Professional ($149/mois)**
   - Tout du Trader
   - Whale Watcher
   - Prédictions IA illimitées
   - Accès API
   - **PAIEMENT REQUIS** ✅

4. **Plan Enterprise ($499/mois)**
   - Toutes les fonctionnalités
   - Support dédié
   - 10 comptes d'équipe
   - **PAIEMENT REQUIS** ✅

## Vérification Technique

### Code de Vérification

Le système vérifie l'accès via:

```python
# Dans config/admin_config.py
ADMIN_USER_ID = "owner_admin_001"
ADMIN_EMAIL = "signaltrustai@gmail.com"

def is_admin_email(email: str) -> bool:
    return email.lower() == ADMIN_EMAIL.lower()

def is_admin_user_id(user_id: str) -> bool:
    return user_id == ADMIN_USER_ID
```

### Contrôle d'Accès

```python
# Dans ai_chat_system.py
def check_access(self, user_id: str, user_email: str = None) -> bool:
    # Uniquement pour owner_admin_001 ou signaltrustai@gmail.com
    if is_admin_user_id(user_id):
        return True
    if user_email and is_admin_email(user_email):
        return True
    # Tous les autres: accès refusé
    return False
```

### Whale Watcher Access

```python
# Dans whale_watcher.py
OWNER_ID = 'owner_admin_001'  # Seul owner_admin_001 a accès gratuit
ALLOWED_TIERS = ['pro', 'enterprise']  # Les autres doivent payer pour ces plans

def check_access(self, user_id: str, user_plan: str) -> bool:
    if user_id == self.OWNER_ID:  # Uniquement owner_admin_001
        return True
    return user_plan in self.ALLOWED_TIERS  # Les autres doivent avoir payé
```

## Résumé

### ✅ Votre Compte (signaltrustai@gmail.com)
- Accès complet: **OUI**
- Paiement requis: **NON**
- Raison: Compte administrateur/propriétaire

### ❌ Tous les Autres Comptes
- Accès complet: **NON** (sauf s'ils paient)
- Paiement requis: **OUI**
- Raison: Utilisateurs réguliers

## Sécurité

Le bypass est codé en dur dans la configuration et vérifie:
1. L'email exact: `signaltrustai@gmail.com`
2. Le user_id exact: `owner_admin_001`

**Aucun autre compte ne peut bénéficier de ce privilège.**

---

**Date:** 2026-02-07  
**Status:** Actif  
**Type:** Configuration Exclusive Owner
