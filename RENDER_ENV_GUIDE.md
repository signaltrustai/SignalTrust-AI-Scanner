# 🚀 Guide Rapide: Copier les Variables d'Environnement dans Render
# Quick Guide: Copy Environment Variables to Render

## 📋 Introduction / Introduction

Ce guide explique comment copier rapidement toutes les variables d'environnement du fichier `.env.render` dans votre dashboard Render.

This guide explains how to quickly copy all environment variables from the `.env.render` file into your Render dashboard.

---

## 🎯 Méthode 1: Interface Web Render (Recommandé)
## Method 1: Render Web Interface (Recommended)

### Étape 1: Accéder aux Variables d'Environnement
### Step 1: Access Environment Variables

1. Allez sur https://dashboard.render.com
2. Sélectionnez votre service (ou créez-en un nouveau)
3. Cliquez sur **"Environment"** dans le menu de gauche

### Étape 2: Ajouter les Variables Obligatoires
### Step 2: Add Required Variables

Copiez ces valeurs **OBLIGATOIRES** / Copy these **REQUIRED** values:

```bash
FLASK_ENV=production
DEBUG=false
PYTHON_VERSION=3.11.11
GUNICORN_WORKER=1
```

**Dans Render:**
1. Cliquez sur **"Add Environment Variable"**
2. Key: `FLASK_ENV`, Value: `production`
3. Cliquez sur **"Add Environment Variable"** à nouveau
4. Key: `DEBUG`, Value: `false`
5. Répétez pour `PYTHON_VERSION` et `GUNICORN_WORKER`

### Étape 3: Ajouter la Configuration OpenAI (Recommandé)
### Step 3: Add OpenAI Configuration (Recommended)

```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
OPENAI_MODEL=gpt-4o-mini
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000
USE_AI_PREDICTIONS=true
USE_AI_ANALYSIS=true
USE_AI_CHAT=true
```

⚠️ **IMPORTANT**: Remplacez `YOUR_ACTUAL_KEY_HERE` par votre vraie clé OpenAI!
⚠️ **IMPORTANT**: Replace `YOUR_ACTUAL_KEY_HERE` with your actual OpenAI key!

### Étape 4: Ajouter les APIs Optionnelles (Si vous les avez)
### Step 4: Add Optional APIs (If you have them)

```bash
COINGECKO_API_KEY=your_key_here
ALPHAVANTAGE_API_KEY=your_key_here
WHALEALERT_API_KEY=your_key_here
NEWS_CATCHER_API_KEY=your_key_here
```

### Étape 5: Configuration Avancée (Optionnel)
### Step 5: Advanced Configuration (Optional)

```bash
AGENT_BASE_URL=https://your-app-name.onrender.com
API_RATE_LIMIT=60
API_CACHE_TTL=300
API_MAX_RETRIES=3
CLOUD_PROVIDER=local
CLOUD_COMPRESS=true
CLOUD_AUTO_SYNC=false
```

### Étape 6: Sauvegarder et Déployer
### Step 6: Save and Deploy

1. Cliquez sur **"Save Changes"** en bas de la page
2. Render redémarrera automatiquement votre service
3. Attendez quelques minutes pour le déploiement
4. Vérifiez que tout fonctionne: `https://your-app.onrender.com/health`

---

## 🔧 Méthode 2: Utiliser render.yaml (Automatique)
## Method 2: Using render.yaml (Automatic)

Si vous déployez avec **Blueprint** (fichier `render.yaml`):

1. **Connectez votre repository sur Render**
2. **Sélectionnez "New" → "Blueprint"**
3. **Render détectera automatiquement `render.yaml`**
4. **Vous devrez seulement définir les clés API sensibles:**
   - `OPENAI_API_KEY`
   - `COINGECKO_API_KEY` (optionnel)
   - `ALPHAVANTAGE_API_KEY` (optionnel)
   - Autres clés API que vous avez

Les autres variables sont déjà définies dans `render.yaml`!

---

## 📝 Liste de Vérification Complète
## Complete Checklist

### ✅ Variables OBLIGATOIRES / REQUIRED
- [ ] `FLASK_ENV=production`
- [ ] `DEBUG=false`
- [ ] `PYTHON_VERSION=3.11.11`
- [ ] `GUNICORN_WORKER=1`

### ✅ Variables RECOMMANDÉES / RECOMMENDED
- [ ] `AI_PROVIDER=openai`
- [ ] `OPENAI_API_KEY=sk-proj-...` ⚠️ VOTRE CLÉ / YOUR KEY
- [ ] `OPENAI_MODEL=gpt-4o-mini`
- [ ] `AI_TEMPERATURE=0.7`
- [ ] `AI_MAX_TOKENS=2000`
- [ ] `USE_AI_PREDICTIONS=true`
- [ ] `USE_AI_ANALYSIS=true`
- [ ] `USE_AI_CHAT=true`

### ✅ Variables OPTIONNELLES / OPTIONAL
- [ ] `COINGECKO_API_KEY` (si vous avez / if you have)
- [ ] `ALPHAVANTAGE_API_KEY` (si vous avez / if you have)
- [ ] `WHALEALERT_API_KEY` (si vous avez / if you have)
- [ ] `NEWS_CATCHER_API_KEY` (si vous avez / if you have)
- [ ] `API_RATE_LIMIT=60`
- [ ] `API_CACHE_TTL=300`
- [ ] `API_MAX_RETRIES=3`

### ✅ Cloud Storage (si nécessaire / if needed)
- [ ] `CLOUD_PROVIDER=local` (ou aws/gcp/azure)
- [ ] `CLOUD_COMPRESS=true`
- [ ] `CLOUD_AUTO_SYNC=false`

---

## 🎬 Configuration Minimale pour Démarrer
## Minimal Configuration to Start

Si vous voulez démarrer **rapidement** avec le minimum:

```bash
# Dans Render Dashboard → Environment:
FLASK_ENV=production
DEBUG=false
OPENAI_API_KEY=sk-proj-VOTRE_CLÉ_ICI
```

C'est tout! Votre application fonctionnera avec ces 3 variables minimum.
That's it! Your application will work with these 3 minimum variables.

---

## 🔐 Sécurité des Clés API
## API Key Security

### ✅ BONNES PRATIQUES / BEST PRACTICES

1. **Ne JAMAIS commiter de vraies clés dans Git**
   - Utilisez toujours des placeholders dans `.env.render`
   - Définissez les vraies clés uniquement dans Render Dashboard

2. **Utiliser des clés différentes pour dev et prod**
   - Clé de développement pour tester localement
   - Clé de production pour Render

3. **Rotation régulière des clés**
   - Changez vos clés API tous les 90 jours
   - Particulièrement important pour OpenAI

4. **Monitorer l'utilisation**
   - Vérifiez votre usage OpenAI: https://platform.openai.com/usage
   - Configurez des alertes de budget

### ❌ À ÉVITER / AVOID

- ❌ Ne pas mettre de clés dans le code source
- ❌ Ne pas partager vos clés API
- ❌ Ne pas utiliser les mêmes clés partout
- ❌ Ne pas oublier de limiter les permissions

---

## 💰 Estimation des Coûts
## Cost Estimation

### Render Hosting

**Plan Gratuit / Free Plan:**
- ✅ 750 heures/mois (suffisant pour 1 app)
- ✅ 512 MB RAM
- ⚠️ Sleep après 15 min d'inactivité
- ✅ HTTPS inclus
- **Coût: GRATUIT / FREE**

**Plan Starter ($7/mois):**
- ✅ Toujours actif (no sleep)
- ✅ 512 MB RAM
- ✅ Plus rapide
- ✅ HTTPS inclus
- **Coût: $7/mois**

### OpenAI API

**gpt-4o-mini (Recommandé):**
- Input: ~$0.00015 / 1K tokens
- Output: ~$0.0006 / 1K tokens
- **Estimation: $5-20/mois** (usage modéré)

**gpt-4o:**
- Input: ~$0.0025 / 1K tokens  
- Output: ~$0.01 / 1K tokens
- **Estimation: $20-100/mois** (usage modéré)

### APIs Marché (Gratuites!)

- ✅ **CoinGecko**: 10-50 appels/min GRATUIT
- ✅ **Alpha Vantage**: 500 requêtes/jour GRATUIT
- ✅ **WhaleAlert**: 1000 requêtes/jour GRATUIT
- ✅ **NewsCatcher**: Essai gratuit disponible

**Total Coût Minimal: $0-5/mois** (Render Free + OpenAI léger)
**Total Minimal Cost: $0-5/month** (Render Free + Light OpenAI)

---

## 🐛 Dépannage / Troubleshooting

### Problème: L'application ne démarre pas
### Issue: Application won't start

**Solution:**
1. Vérifiez que `FLASK_ENV=production` et `DEBUG=false`
2. Vérifiez les logs Render: Dashboard → Logs
3. Assurez-vous que `OPENAI_API_KEY` est valide

### Problème: Erreur "OpenAI API key not found"
### Issue: Error "OpenAI API key not found"

**Solution:**
1. Ajoutez `OPENAI_API_KEY` dans Render Environment
2. Format: `sk-proj-...` (commence toujours par `sk-`)
3. Pas d'espaces avant/après la clé

### Problème: L'application s'endort (Free Plan)
### Issue: Application sleeps (Free Plan)

**Solution:**
1. C'est normal sur le plan gratuit après 15 min d'inactivité
2. L'app se réveille automatiquement à la prochaine requête (30 sec)
3. Pour éviter ça: upgrader vers Starter Plan ($7/mois)

### Problème: Timeout ou 503 errors
### Issue: Timeout or 503 errors

**Solution:**
1. Augmentez `GUNICORN_WORKER` si vous êtes sur un plan payant
2. Vérifiez que les APIs externes répondent
3. Vérifiez les logs pour identifier la cause

---

## 📚 Ressources Supplémentaires
## Additional Resources

### Documentation Projet / Project Documentation
- 📖 [README.md](README.md) - Vue d'ensemble du projet
- 🚀 [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Guide détaillé Render
- 🔧 [.env.example](.env.example) - Toutes les variables expliquées
- ☁️ [CLOUD_STORAGE_GUIDE.md](CLOUD_STORAGE_GUIDE.md) - Configuration cloud
- 🤖 [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md) - Setup OpenAI détaillé

### Documentation Externe / External Documentation
- 🌐 [Render Docs](https://render.com/docs) - Documentation Render officielle
- 🤖 [OpenAI Platform](https://platform.openai.com) - Gestion clés OpenAI
- 💰 [OpenAI Pricing](https://openai.com/pricing) - Tarifs OpenAI
- 🐙 [GitHub Repo](https://github.com/signaltrustai/SignalTrust-AI-Scanner) - Code source

### Support / Help
- 🐛 [GitHub Issues](https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues) - Rapporter bugs
- 📧 Render Support: support@render.com
- 💬 OpenAI Help: https://help.openai.com

---

## 🎉 C'est Tout! / That's It!

Votre application SignalTrust AI Scanner devrait maintenant fonctionner parfaitement sur Render! 🚀

Your SignalTrust AI Scanner application should now work perfectly on Render! 🚀

### Prochaines Étapes / Next Steps:

1. ✅ Vérifier que l'app fonctionne: `https://your-app.onrender.com`
2. ✅ Tester le health check: `https://your-app.onrender.com/health`
3. ✅ Explorer les fonctionnalités IA
4. ✅ (Optionnel) Ajouter un domaine personnalisé
5. ✅ (Optionnel) Configurer les backups cloud

**Bon déploiement! / Happy deploying!** 🎊
