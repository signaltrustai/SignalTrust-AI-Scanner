# ⚡ Guide Ultra-Rapide Variables d'Environnement

## 🎯 En 3 Minutes Top Chrono!

### Qu'est-ce que c'est?

```
Une variable d'environnement = Un mot de passe secret pour votre app

┌──────────────┐         ┌─────────────┐
│  Fichier     │         │     App     │
│   .env       │────────▶│ SignalTrust │─────▶ Internet
│              │  lit    │             │ (APIs)
│ OPENAI_KEY=  │         │  Utilise    │
│ PASSWORD=    │         │  en secret  │
└──────────────┘         └─────────────┘
```

---

## 🚀 Configuration en 4 Étapes

### Étape 1: Copier le Modèle (30 secondes)

**Windows:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

### Étape 2: Obtenir une Clé OpenAI (2 minutes)

```
1. Aller sur: https://platform.openai.com
2. Créer un compte (gratuit)
3. Cliquer: Settings → API Keys
4. Cliquer: "Create new secret key"
5. COPIER la clé (commence par "sk-proj-")
```

### Étape 3: Éditer le Fichier .env (1 minute)

Ouvrir `.env` avec Notepad/TextEdit et remplir:

```ini
# AI Configuration (OBLIGATOIRE)
OPENAI_API_KEY=sk-proj-COLLEZ_VOTRE_CLÉ_ICI
OPENAI_MODEL=gpt-4o-mini

# Security (OBLIGATOIRE)
SECRET_KEY=génère_32_caractères_aléatoires
ADMIN_PASSWORD=VotreMotDePasse123!

# Admin Info (DÉJÀ CONFIGURÉ)
ADMIN_EMAIL=signaltrustai@gmail.com
```

**Pour générer SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Étape 4: Démarrer! (30 secondes)

```bash
python start.py
```

---

## 📊 Schéma Visuel Complet

```
┌─────────────────────────────────────────────────────┐
│                  CONFIGURATION                      │
└─────────────────────────────────────────────────────┘

AVANT:                          APRÈS:
─────                           ─────

.env.example                    .env
│                               │
│ OPENAI_KEY=votre_clé         │ OPENAI_KEY=sk-proj-abc123...
│ SECRET_KEY=génerer           │ SECRET_KEY=a1b2c3d4e5f6...
│ ADMIN_PASSWORD=choisir       │ ADMIN_PASSWORD=MonPass123!
│                               │
└─ Modèle vide                  └─ Configuré! ✅


┌──────────────────────────────────────────────────────┐
│               FLUX D'UTILISATION                     │
└──────────────────────────────────────────────────────┘

1. COPIER            2. OBTENIR           3. ÉDITER
   ↓                    ↓                    ↓
.env.example        OpenAI.com           .env
   ↓                    ↓                    ↓
   └────────────────────┴────────────────────┘
                        ↓
                   4. LANCER
                        ↓
                  python start.py
                        ↓
                   ✅ SUCCESS!
```

---

## ✅ Checklist Minute

```
☐ Fichier .env créé (cp .env.example .env)
☐ Clé OpenAI obtenue (https://platform.openai.com)
☐ Clé OpenAI collée dans .env
☐ SECRET_KEY généré (32 caractères)
☐ ADMIN_PASSWORD choisi
☐ Fichier sauvegardé
☐ python start.py lancé
```

---

## 🐛 Problèmes? Solutions Rapides!

### ❌ "API Key not found"
```
✅ Vérifier:
   • Fichier s'appelle ".env" (pas .env.txt)
   • Dans le même dossier que app.py
   • Pas d'espaces: OPENAI_API_KEY=sk-...
   • Redémarrer l'app
```

### ❌ "Invalid API key"
```
✅ Solutions:
   • Copier toute la clé (pas coupée)
   • Pas de guillemets: ❌ "sk-..." ✅ sk-...
   • Clé active sur OpenAI.com
   • Régénérer nouvelle clé si besoin
```

### ❌ "File not found"
```
✅ Afficher fichiers cachés:
   Windows: Explorateur → Affichage → Éléments masqués
   Mac: Finder → Cmd + Shift + .
   Terminal: ls -la
```

---

## 💰 Coûts OpenAI

```
Plan Gratuit:  $5 de crédit initial
Modèle:        gpt-4o-mini (recommandé)
Coût:          ~$0.15-0.60 par million tokens
Par analyse:   ~$0.01-0.10
Budget/mois:   $10-50 (usage normal)
```

---

## 🔒 Règles de Sécurité

```
❌ JAMAIS committer .env sur Git
❌ JAMAIS partager vos clés API
✅ Utiliser des clés différentes (dev/prod)
✅ Sauvegarder .env en lieu sûr
✅ Changer les clés tous les 3-6 mois
```

---

## 🚀 Sur Render (Production)

Pas de fichier .env! Utiliser l'interface web:

```
1. dashboard.render.com
2. Votre service → Environment
3. Add Environment Variable
4. Ajouter chaque variable:
   Key: OPENAI_API_KEY
   Value: sk-proj-...
5. Save Changes
```

---

## 📚 Besoin d'Aide?

```
Guide Complet:    GUIDE_VARIABLES_ENVIRONNEMENT.md
Render Setup:     RENDER_SETUP_COMPLETE.md
Support:          signaltrustai@gmail.com
Documentation:    .env.example (commentaires détaillés)
```

---

## 🎉 C'est Tout!

```
┌─────────────────────────────┐
│                             │
│   ✅ Configuration OK       │
│                             │
│   Temps: ~3-5 minutes       │
│   Difficulté: Facile        │
│                             │
│   → python start.py         │
│   → Profitez! 🚀           │
│                             │
└─────────────────────────────┘
```

**Dernière mise à jour**: 8 février 2026
