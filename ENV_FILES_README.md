# 📁 Guide des Fichiers .env / .env Files Guide

Ce projet contient plusieurs fichiers de configuration d'environnement pour différents cas d'usage.

This project contains multiple environment configuration files for different use cases.

---

## 📋 Fichiers Disponibles / Available Files

### 1. `.env.example` - Configuration Complète de Référence
**Complete Reference Configuration**

- **Usage**: Documentation et développement local
- **Contenu**: TOUTES les variables possibles (39 variables)
- **Langue**: Bilingue (Français/Anglais)
- **Détails**: Explications détaillées, exemples, coûts

**Utilisation / Usage:**
```bash
cp .env.example .env
# Puis éditer .env avec vos clés
# Then edit .env with your keys
```

**Idéal pour / Ideal for:**
- ✅ Comprendre toutes les options disponibles
- ✅ Développement local
- ✅ Documentation de référence
- ✅ Apprentissage de la configuration

---

### 2. `.env.render` - Configuration Render (Production)
**Render Configuration (Production)**

- **Usage**: Déploiement sur Render.com
- **Contenu**: Variables optimisées pour production (25 variables)
- **Langue**: Bilingue (Français/Anglais)
- **Focus**: Simplicité et sécurité en production

**Utilisation / Usage:**
```bash
# Copier les variables dans Render Dashboard
# Copy variables to Render Dashboard
# https://dashboard.render.com → Environment
```

**Idéal pour / Ideal for:**
- ✅ Déploiement production sur Render
- ✅ Configuration cloud
- ✅ Démarrage rapide
- ✅ Sécurité renforcée

**Voir aussi / See also:** [RENDER_ENV_GUIDE.md](RENDER_ENV_GUIDE.md)

---

## 🔍 Comparaison / Comparison

| Caractéristique | .env.example | .env.render |
|-----------------|--------------|-------------|
| **Lignes** | 348 | 251 |
| **Variables** | 39 | 25 |
| **Documentation** | Très détaillée | Focalisée |
| **Usage** | Dev + Référence | Production |
| **Langue** | FR/EN | FR/EN |
| **Cloud Ready** | Tous | Render |
| **Priorités** | Toutes égales | Triées |

---

## 🎯 Quel Fichier Utiliser? / Which File to Use?

### Pour Développement Local / For Local Development
→ Utilisez / Use **`.env.example`**
```bash
cp .env.example .env
nano .env  # Éditer avec vos clés / Edit with your keys
python3 start.py
```

### Pour Déploiement Render / For Render Deployment
→ Utilisez / Use **`.env.render`**
1. Ouvrez `.env.render`
2. Copiez les variables dans Render Dashboard
3. Remplacez les placeholders par vos vraies clés
4. Sauvegardez et déployez!

Voir le guide détaillé: [RENDER_ENV_GUIDE.md](RENDER_ENV_GUIDE.md)

---

## 🔐 Sécurité / Security

### ⚠️ IMPORTANT

**Ne JAMAIS commiter ces fichiers avec de vraies clés!**
**NEVER commit these files with real keys!**

```bash
# ✅ BON / GOOD
.env.example  → Placeholders seulement
.env.render   → Placeholders seulement

# ❌ MAUVAIS / BAD
.env → Contient vos vraies clés (git ignoré!)
.env → Contains your real keys (git ignored!)
```

### Fichiers Git-Ignorés / Git-Ignored Files

Ces fichiers ne doivent JAMAIS être commités:
These files should NEVER be committed:
- `.env` (votre configuration locale / your local config)
- Tout fichier contenant de vraies clés API
- Any file containing real API keys

---

## 📚 Documentation Supplémentaire / Additional Documentation

### Guides de Configuration / Configuration Guides
- 📖 [.env.example](.env.example) - Configuration complète
- 🚀 [.env.render](.env.render) - Configuration Render
- �� [RENDER_ENV_GUIDE.md](RENDER_ENV_GUIDE.md) - Guide Render détaillé
- 🔧 [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Déploiement complet

### Guides Techniques / Technical Guides
- 🤖 [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md) - Configuration OpenAI
- ☁️ [CLOUD_STORAGE_GUIDE.md](CLOUD_STORAGE_GUIDE.md) - Stockage cloud
- 🤝 [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) - Système multi-agents
- 📖 [README.md](README.md) - Vue d'ensemble projet

---

## 🆘 Besoin d'Aide? / Need Help?

### Documentation / Documentation
1. Lisez [RENDER_ENV_GUIDE.md](RENDER_ENV_GUIDE.md) pour un guide pas-à-pas
2. Consultez [.env.example](.env.example) pour toutes les options
3. Vérifiez [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) pour le déploiement

### Support / Support
- 🐛 [GitHub Issues](https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues)
- 📧 Render Support: support@render.com
- 🌐 [Render Docs](https://render.com/docs)

---

## ✅ Checklist de Démarrage Rapide / Quick Start Checklist

### Développement Local / Local Development
- [ ] Copier `.env.example` vers `.env`
- [ ] Ajouter `OPENAI_API_KEY` dans `.env`
- [ ] Configurer autres APIs (optionnel)
- [ ] Démarrer: `python3 start.py`

### Déploiement Render / Render Deployment
- [ ] Ouvrir `.env.render`
- [ ] Copier variables OBLIGATOIRES dans Render
- [ ] Ajouter `OPENAI_API_KEY`
- [ ] Configurer Build/Start commands
- [ ] Déployer!

---

## 🎉 C'est Tout! / That's It!

Vous avez maintenant tous les outils pour configurer SignalTrust AI Scanner!

You now have all the tools to configure SignalTrust AI Scanner!

**Bon développement! / Happy coding!** 🚀
