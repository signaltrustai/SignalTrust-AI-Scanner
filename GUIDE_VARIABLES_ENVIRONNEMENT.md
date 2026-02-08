# 📚 Guide Complet des Variables d'Environnement

## 🎯 Qu'est-ce qu'une Variable d'Environnement?

Une **variable d'environnement** est comme une **note secrète** que votre application peut lire. C'est un moyen sûr de stocker des informations sensibles (comme des mots de passe, clés API) sans les écrire directement dans votre code.

### 🔐 Pourquoi c'est Important?

```
❌ MAUVAIS (dans le code):
    api_key = "sk-123456789abcdef"  ← Visible par tous!

✅ BON (variable d'environnement):
    api_key = os.getenv('OPENAI_API_KEY')  ← Sécurisé!
```

---

## 📊 Schéma Visuel du Système

```
┌─────────────────────────────────────────────────────────────┐
│                    VOTRE ORDINATEUR                         │
│                                                             │
│  ┌──────────────┐         ┌─────────────────┐             │
│  │   Fichier    │         │   Application   │             │
│  │    .env      │────────▶│  SignalTrust    │             │
│  │              │  lit    │                 │             │
│  │ OPENAI_KEY=  │         │  Utilise les    │             │
│  │ ADMIN_PASS=  │         │  clés API       │─────────────┼──▶ Internet
│  │ DATABASE=    │         │  en toute       │  (APIs)     │
│  │              │         │  sécurité       │             │
│  └──────────────┘         └─────────────────┘             │
│        ↑                                                    │
│        │                                                    │
│  ┌─────┴────────┐                                          │
│  │ .env.example │  (Modèle à copier)                       │
│  └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Configuration Étape par Étape

### Étape 1: Localiser le Fichier Modèle

```
📂 Votre Projet
   ├── 📄 .env.example      ← Modèle (fourni)
   ├── 📄 .env              ← À créer (vos vraies clés)
   ├── 📄 app.py
   └── 📁 templates
```

**Action**: Trouvez le fichier `.env.example` dans votre projet.

---

### Étape 2: Copier le Modèle

#### Sur Windows:
```bash
copy .env.example .env
```

#### Sur Mac/Linux:
```bash
cp .env.example .env
```

**Résultat**: Vous avez maintenant un fichier `.env` vide avec tous les emplacements pour vos clés.

---

### Étape 3: Ouvrir le Fichier .env

```
┌─────────────────────────────────────────┐
│  Comment ouvrir le fichier .env?        │
├─────────────────────────────────────────┤
│                                         │
│  Option 1: Éditeur de texte            │
│  • Windows: Notepad                     │
│  • Mac: TextEdit                        │
│  • Tous: VS Code, Sublime Text         │
│                                         │
│  Option 2: Dans le terminal             │
│  • nano .env                            │
│  • vim .env                             │
│  • code .env (VS Code)                  │
│                                         │
└─────────────────────────────────────────┘
```

---

### Étape 4: Comprendre la Structure

Voici comment est organisé le fichier `.env`:

```ini
# ============================================
# SECTION: AI CONFIGURATION
# ============================================
# Commentaire explicatif
# Des instructions détaillées

NOM_VARIABLE=valeur_à_remplacer

# Exemple concret:
OPENAI_API_KEY=your_openai_api_key_here  ← Remplacez ici!
```

**Structure**:
- Lignes avec `#` = Commentaires (ignorés par l'app)
- Lignes avec `=` = Variables (utilisées par l'app)
- Pas d'espaces autour du `=`
- Pas de guillemets nécessaires

---

## 🗺️ Carte des Variables (Organisée par Importance)

### ⭐⭐⭐ ESSENTIELLES (Minimum pour démarrer)

```
┌──────────────────────────────────────────────┐
│  🔑 CLÉS OBLIGATOIRES                        │
├──────────────────────────────────────────────┤
│                                              │
│  1. SECRET_KEY (Sécurité app)                │
│     └─ Génère: python -c "import secrets;   │
│                print(secrets.token_hex(32))" │
│                                              │
│  2. OPENAI_API_KEY ou ANTHROPIC_API_KEY      │
│     └─ Choisir AU MOINS un                   │
│     └─ Obtenir: voir section ci-dessous      │
│                                              │
│  3. ADMIN_PASSWORD                           │
│     └─ Votre mot de passe admin             │
│                                              │
└──────────────────────────────────────────────┘
```

### ⭐⭐ IMPORTANTES (Recommandées)

```
┌──────────────────────────────────────────────┐
│  💳 PAIEMENTS                                │
│  • Adresses crypto (configurées)            │
│  • PayPal email                              │
│  • Stripe links                              │
│                                              │
│  📊 MARKET DATA                              │
│  • COINGECKO_API_KEY                         │
│  • ALPHA_VANTAGE_API_KEY                     │
│                                              │
└──────────────────────────────────────────────┘
```

### ⭐ OPTIONNELLES (Pour fonctionnalités avancées)

```
┌──────────────────────────────────────────────┐
│  📱 SOCIAL MEDIA (Marketing)                 │
│  • Twitter, Instagram, TikTok                │
│                                              │
│  💾 CLOUD STORAGE                            │
│  • AWS S3, Google Cloud                      │
│                                              │
│  📧 NOTIFICATIONS                            │
│  • Email SMTP, Twilio SMS                    │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🔐 Guide d'Obtention des Clés API

### 1. OpenAI (GPT-4, GPT-3.5)

```
┌─────────────────────────────────────────┐
│  ÉTAPES POUR OBTENIR OPENAI_API_KEY    │
├─────────────────────────────────────────┤
│                                         │
│  1️⃣  Aller sur:                        │
│      https://platform.openai.com       │
│                                         │
│  2️⃣  Créer un compte (Sign Up)         │
│                                         │
│  3️⃣  Aller dans: Settings → API Keys   │
│                                         │
│  4️⃣  Cliquer: "Create new secret key"  │
│                                         │
│  5️⃣  COPIER la clé (commence par       │
│      "sk-proj-...")                     │
│                                         │
│  6️⃣  COLLER dans .env:                 │
│      OPENAI_API_KEY=sk-proj-...         │
│                                         │
│  💰 Coût: ~$0.15-$10 par million        │
│      tokens selon le modèle             │
│                                         │
└─────────────────────────────────────────┘
```

### 2. Anthropic Claude (Recommandé)

```
┌─────────────────────────────────────────┐
│  ÉTAPES POUR ANTHROPIC_API_KEY         │
├─────────────────────────────────────────┤
│                                         │
│  1️⃣  Aller sur:                        │
│      https://console.anthropic.com     │
│                                         │
│  2️⃣  Créer un compte                   │
│                                         │
│  3️⃣  Aller dans: Account → API Keys    │
│                                         │
│  4️⃣  Cliquer: "Create Key"             │
│                                         │
│  5️⃣  COPIER la clé (commence par       │
│      "sk-ant-...")                      │
│                                         │
│  6️⃣  COLLER dans .env:                 │
│      ANTHROPIC_API_KEY=sk-ant-...       │
│                                         │
│  💰 Coût: $3-$15 par million tokens     │
│      (Claude 3.5 Sonnet recommandé)     │
│                                         │
│  ⭐ MEILLEUR pour analyse financière    │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Market Data APIs (Optionnel)

```
┌─────────────────────────────────────────┐
│  COINGECKO (Crypto Data - GRATUIT)     │
├─────────────────────────────────────────┤
│                                         │
│  1️⃣  Aller sur:                        │
│      https://www.coingecko.com/en/api  │
│                                         │
│  2️⃣  Créer compte → Get Free API Key   │
│                                         │
│  3️⃣  COLLER dans .env:                 │
│      COINGECKO_API_KEY=CG-...           │
│                                         │
│  💰 Plan Gratuit: 10-50 appels/min     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📝 Exemple de Configuration Complète

Voici à quoi doit ressembler votre fichier `.env` complété:

```ini
# ============================================
# AI CONFIGURATION (MINIMUM REQUIS)
# ============================================
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-AbCdEf123456789XyZ
OPENAI_MODEL=gpt-4o-mini

# OU si vous utilisez Claude:
# ANTHROPIC_API_KEY=sk-ant-api03-AbCdEf123456789XyZ
# ANTHROPIC_MODEL=claude-3-5-sonnet-20240620

# ============================================
# APPLICATION SECURITY
# ============================================
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
ADMIN_PASSWORD=MonMotDePasseSecurise123!

# ============================================
# ADMIN CREDENTIALS
# ============================================
ADMIN_EMAIL=signaltrustai@gmail.com
ADMIN_USER_ID=owner_admin_001

# ============================================
# CRYPTO WALLET ADDRESSES (Déjà configuré)
# ============================================
ETHEREUM_WALLET_ADDRESS=0xFDAf80b517993A3420E96Fb11D01e959EE35A419
POLYGON_WALLET_ADDRESS=0xFDAf80b517993A3420E96Fb11D01e959EE35A419
BITCOIN_WALLET_ADDRESS=bc1qz4kq6hu05j6rdnzv2xe325wf0404smhsaxas86
SOLANA_WALLET_ADDRESS=BATM5MQZxeNaJGPGdUsRGD5mputbCkHheckcm1y8Vt6r

# ============================================
# PAYPAL CONFIGURATION (Optionnel)
# ============================================
PAYPAL_EMAIL=payments@signaltrust.ai
# PAYPAL_CLIENT_ID=votre_client_id_ici
# PAYPAL_CLIENT_SECRET=votre_secret_ici

# ============================================
# MARKET DATA APIs (Optionnel mais recommandé)
# ============================================
# COINGECKO_API_KEY=CG-VotreCléIci
# ALPHA_VANTAGE_API_KEY=VotreCléIci

# ============================================
# SOCIAL MEDIA (Pour marketing viral)
# ============================================
# TWITTER_API_KEY=votre_clé_ici
# INSTAGRAM_USERNAME=signaltrust_ai
# ... (etc.)
```

---

## 🔄 Flux de Configuration Visuel

```
┌──────────────────────────────────────────────────────────────┐
│                     PROCESSUS COMPLET                        │
└──────────────────────────────────────────────────────────────┘

    Étape 1: COPIER                Étape 2: OBTENIR
    ─────────────                  ─────────────
    
    .env.example                   OpenAI.com
         │                              │
         │ cp                           │ Sign Up
         ▼                              ▼
       .env                        Obtenir Clé
         │                              │
         │                              │ sk-proj-...
         │                              │
         │ ◄────────────────────────────┘
         │         Copier
         │
         │
    Étape 3: CONFIGURER            Étape 4: VÉRIFIER
    ───────────────                ─────────────
         │
         │ Éditer avec                python start.py
         │ Notepad/VS Code                 │
         ▼                                 │
    Remplir les                            ▼
    variables                    ┌──────────────────┐
         │                       │   ✅ SUCCESS!    │
         │                       │   App démarre    │
         └──────────────────────▶│   avec vos clés  │
                Sauvegarder      └──────────────────┘
```

---

## ✅ Checklist de Vérification

Avant de démarrer l'application, vérifiez:

```
Configuration Minimale:
──────────────────────
☐ Fichier .env créé (copié depuis .env.example)
☐ SECRET_KEY généré (32+ caractères aléatoires)
☐ Au moins UNE clé AI configurée:
   ☐ OPENAI_API_KEY (commence par sk-proj-)
   OU
   ☐ ANTHROPIC_API_KEY (commence par sk-ant-)
☐ ADMIN_PASSWORD défini (votre choix)
☐ Fichier .env sauvegardé

Configuration Recommandée:
──────────────────────────
☐ COINGECKO_API_KEY (données crypto gratuites)
☐ Adresses wallet vérifiées
☐ PAYPAL_EMAIL configuré

Configuration Avancée (Optionnel):
──────────────────────────────────
☐ APIs social media (pour marketing)
☐ Cloud storage (AWS/Google)
☐ Email/SMS notifications
```

---

## 🐛 Dépannage - Problèmes Courants

### Problème 1: "No module named 'dotenv'"

```
❌ Erreur:
   ModuleNotFoundError: No module named 'dotenv'

✅ Solution:
   pip install python-dotenv
```

### Problème 2: "API Key not found"

```
❌ Erreur:
   Error: OPENAI_API_KEY not found

✅ Solutions:
   1. Vérifier que le fichier s'appelle exactement ".env" (pas .env.txt)
   2. Vérifier qu'il est dans le même dossier que app.py
   3. Vérifier qu'il n'y a pas d'espaces:
      ✅ OPENAI_API_KEY=sk-...
      ❌ OPENAI_API_KEY = sk-...
   4. Redémarrer l'application après modification
```

### Problème 3: "Invalid API Key"

```
❌ Erreur:
   OpenAI API error: Invalid API key

✅ Solutions:
   1. Vérifier que la clé est complète (pas coupée)
   2. Pas de guillemets autour de la clé:
      ✅ OPENAI_API_KEY=sk-proj-abc123
      ❌ OPENAI_API_KEY="sk-proj-abc123"
   3. Vérifier que la clé est active sur OpenAI.com
   4. Régénérer une nouvelle clé si nécessaire
```

### Problème 4: Fichier .env invisible

```
❌ Problème:
   Je ne vois pas le fichier .env

✅ Solutions:
   Windows:
   • Ouvrir l'Explorateur de fichiers
   • Onglet "Affichage"
   • Cocher "Éléments masqués"

   Mac:
   • Finder → Cmd + Shift + . (point)
   
   Terminal:
   • ls -la (affiche tous les fichiers)
```

---

## 🔒 Sécurité - Règles d'Or

```
┌──────────────────────────────────────────┐
│  ⚠️  RÈGLES DE SÉCURITÉ IMPORTANTES     │
├──────────────────────────────────────────┤
│                                          │
│  1. ❌ JAMAIS committer .env sur Git    │
│     └─ Fichier .gitignore protège ça    │
│                                          │
│  2. ❌ JAMAIS partager vos clés API     │
│     └─ Régénérer si compromises         │
│                                          │
│  3. ✅ Utiliser des clés différentes:   │
│     • Développement (local)             │
│     • Production (Render/Heroku)        │
│                                          │
│  4. ✅ Sauvegarder .env en lieu sûr     │
│     └─ Pas sur GitHub!                  │
│     └─ Gestionnaire de mots de passe    │
│                                          │
│  5. ✅ Rotation régulière des clés      │
│     └─ Tous les 3-6 mois                │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🚀 Sur Render.com (Déploiement Production)

Pour déployer sur Render, vous n'avez PAS besoin de fichier .env!

```
┌─────────────────────────────────────────────┐
│  Configuration sur Render (Interface Web)  │
├─────────────────────────────────────────────┤
│                                             │
│  1. Aller sur dashboard.render.com         │
│                                             │
│  2. Sélectionner votre service             │
│     (srv-d63efo0gjchc7390sp9g)             │
│                                             │
│  3. Onglet "Environment"                    │
│                                             │
│  4. Cliquer "Add Environment Variable"      │
│                                             │
│  5. Ajouter une par une:                    │
│     ┌─────────────────────────────────┐    │
│     │ Key:   OPENAI_API_KEY           │    │
│     │ Value: sk-proj-...              │    │
│     └─────────────────────────────────┘    │
│                                             │
│  6. Répéter pour chaque variable            │
│                                             │
│  7. Cliquer "Save Changes"                  │
│                                             │
│  8. Render redéploie automatiquement        │
│                                             │
└─────────────────────────────────────────────┘
```

**Avantages**:
- ✅ Plus sécurisé que fichiers
- ✅ Facile à modifier
- ✅ Pas de risque Git
- ✅ Différent par environnement

---

## 📚 Ressources Supplémentaires

### Documentation Officielle
- **Variables d'environnement**: https://12factor.net/config
- **Python dotenv**: https://pypi.org/project/python-dotenv/
- **Render Config**: https://render.com/docs/environment-variables

### Guides du Projet
- `RENDER_SETUP_COMPLETE.md` - Guide déploiement Render
- `ADMIN_PAYMENT_QUICK_REFERENCE.md` - Configuration paiements
- `.env.example` - Modèle complet avec commentaires

### Obtenir des Clés API
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/account/keys
- **CoinGecko**: https://www.coingecko.com/en/api/pricing
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key

---

## 🎯 Résumé Rapide

```
┌────────────────────────────────────────────────────┐
│  EN 5 MINUTES - CONFIG MINIMALE                   │
├────────────────────────────────────────────────────┤
│                                                    │
│  1️⃣  cp .env.example .env              (1 min)   │
│                                                    │
│  2️⃣  Obtenir clé OpenAI                (2 min)   │
│      → https://platform.openai.com                │
│                                                    │
│  3️⃣  Éditer .env:                      (1 min)   │
│      OPENAI_API_KEY=sk-proj-...                   │
│      SECRET_KEY=[générer aléatoire]               │
│      ADMIN_PASSWORD=[votre choix]                 │
│                                                    │
│  4️⃣  Sauvegarder fichier .env         (10 sec)   │
│                                                    │
│  5️⃣  python start.py                  (30 sec)   │
│                                                    │
│  ✅ TERMINÉ! Application démarrée                 │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🎓 Pour Aller Plus Loin

### Niveau Débutant ✅
Vous avez compris:
- Ce qu'est une variable d'environnement
- Comment créer un fichier .env
- Où obtenir les clés API
- Comment démarrer l'application

### Niveau Intermédiaire 📚
Prochaines étapes:
- Configurer les APIs de market data
- Ajouter les intégrations social media
- Configurer les notifications
- Optimiser les modèles AI

### Niveau Avancé 🚀
Pour experts:
- Multi-cloud deployment
- CI/CD avec variables d'environnement
- Secrets management (Vault, AWS Secrets)
- Rotation automatique des clés

---

## ❓ Questions Fréquentes (FAQ)

**Q1: Combien ça coûte d'utiliser OpenAI?**
```
R: Plan Gratuit: $5 de crédit initial
   Ensuite: Pay-as-you-go
   • GPT-4o-mini: ~$0.15-0.60 par million tokens
   • Usage typique: $0.01-0.10 par analyse
   • Budget mensuel suggéré: $10-50
```

**Q2: Puis-je utiliser plusieurs clés AI en même temps?**
```
R: Oui! Configurez:
   AI_PROVIDER=multi
   OPENAI_API_KEY=...
   ANTHROPIC_API_KEY=...
   
   L'app utilisera le meilleur modèle pour chaque tâche.
```

**Q3: Que faire si ma clé API est compromise?**
```
R: 1. Aller sur le site du provider (OpenAI, etc.)
   2. Révoquer l'ancienne clé immédiatement
   3. Générer une nouvelle clé
   4. Mettre à jour .env
   5. Redémarrer l'application
```

**Q4: Le fichier .env est-il obligatoire en local?**
```
R: Oui pour le développement local.
   Non sur Render (utilise interface web).
```

**Q5: Puis-je avoir plusieurs fichiers .env?**
```
R: Oui, pratique courante:
   .env.local (développement)
   .env.staging (test)
   .env.production (production)
   
   Charger avec: dotenv_path='.env.local'
```

---

## 🎉 Félicitations!

Vous savez maintenant tout sur les variables d'environnement!

```
   ┌─────────────────────────────────┐
   │                                 │
   │     🎊 VOUS ÊTES PRÊT! 🎊      │
   │                                 │
   │  Configuration terminée         │
   │  Application sécurisée          │
   │  Clés API protégées             │
   │                                 │
   │  Prochaine étape:               │
   │  → python start.py              │
   │  → Profiter de l'app! 🚀        │
   │                                 │
   └─────────────────────────────────┘
```

---

**Dernière mise à jour**: 8 février 2026  
**Version**: 1.0  
**Support**: signaltrustai@gmail.com  

**Guides connexes**:
- `RENDER_SETUP_COMPLETE.md` - Déploiement
- `ADMIN_PAYMENT_QUICK_REFERENCE.md` - Paiements
- `README.md` - Vue d'ensemble du projet
