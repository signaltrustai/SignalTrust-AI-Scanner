# Guide d'amélioration des Agents AI / AI Agent Enhancement Guide

## 🚀 Vue d'ensemble / Overview

Le système SignalTrust AI Scanner a été amélioré avec des capacités d'IA de pointe utilisant de vrais modèles d'IA au lieu de simulations.

The SignalTrust AI Scanner system has been enhanced with state-of-the-art AI capabilities using real AI models instead of simulations.

## 🎯 Améliorations / Improvements

### Avant / Before
- ❌ Prédictions aléatoires et simulées
- ❌ Aucune vraie intelligence artificielle
- ❌ Analyses basiques limitées
- ❌ Pas d'apprentissage réel

### Après / After
- ✅ Vrais modèles d'IA (GPT-4, Claude, modèles locaux)
- ✅ Analyses intelligentes et contextuelles
- ✅ Prédictions basées sur l'apprentissage profond
- ✅ Support de multiples fournisseurs d'IA
- ✅ Fallback automatique si l'IA n'est pas disponible

## 📦 Providers AI disponibles / Available AI Providers

### 1. OpenAI (GPT-4, GPT-3.5-turbo)
**Avantages:**
- Très performant pour l'analyse de marchés
- Excellent en compréhension contextuelle
- Large base de connaissances

**Configuration:**
```bash
# Dans votre fichier .env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
```

**Coût approximatif:**
- GPT-4: ~$0.03 per 1K tokens input, ~$0.06 per 1K tokens output
- GPT-3.5-turbo: ~$0.001 per 1K tokens

### 2. Anthropic (Claude)
**Avantages:**
- Excellent pour l'analyse détaillée
- Bonne compréhension des données financières
- Réponses plus nuancées

**Configuration:**
```bash
# Dans votre fichier .env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Coût approximatif:**
- Claude 3 Opus: ~$15/$75 per MTok
- Claude 3 Sonnet: ~$3/$15 per MTok
- Claude 3 Haiku: ~$0.25/$1.25 per MTok

### 3. Modèles Locaux (Ollama)
**Avantages:**
- Gratuit et privé
- Pas de dépendance externe
- Contrôle total

**Installation Ollama:**
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Démarrer Ollama
ollama serve

# Télécharger un modèle
ollama pull llama2
ollama pull mistral
```

**Configuration:**
```bash
# Dans votre fichier .env
AI_PROVIDER=local
LOCAL_MODEL=llama2
LOCAL_API_URL=http://localhost:11434
```

## 🔧 Installation et Configuration

### Étape 1: Installer les dépendances

```bash
# Installation complète avec tous les providers
pip install -r requirements.txt

# Ou installation sélective
pip install openai  # Pour OpenAI uniquement
pip install anthropic  # Pour Anthropic uniquement
```

### Étape 2: Créer le fichier .env

```bash
# Copier l'exemple
cp .env.example .env

# Éditer avec vos clés API
nano .env
```

### Étape 3: Configurer votre provider préféré

**Option A: OpenAI (Recommandé pour la performance)**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4
USE_AI_PREDICTIONS=true
USE_AI_ANALYSIS=true
```

**Option B: Anthropic (Recommandé pour l'analyse détaillée)**
```bash
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxx
ANTHROPIC_MODEL=claude-3-sonnet-20240229
USE_AI_PREDICTIONS=true
USE_AI_ANALYSIS=true
```

**Option C: Local (Gratuit mais nécessite ressources)**
```bash
AI_PROVIDER=local
LOCAL_MODEL=mistral
LOCAL_API_URL=http://localhost:11434
USE_AI_PREDICTIONS=true
USE_AI_ANALYSIS=true
```

### Étape 4: Tester l'installation

```python
# Test rapide
python3 -c "from ai_provider import EnhancedAIEngine; ai = EnhancedAIEngine(); print('✅ AI Engine OK')"
```

## 💡 Utilisation / Usage

### Dans votre code Python

```python
from ai_predictor import AIPredictor

# Créer un predictor avec vraie IA
predictor = AIPredictor(use_real_ai=True)

# Prédiction de prix
result = predictor.predict_price('AAPL', days_ahead=7)
print(result)

# Génération de signaux
signals = predictor.generate_signals('BTC')
print(signals)
```

### Via l'API web

L'application Flask utilisera automatiquement l'IA configurée:

```bash
# Démarrer l'application
python3 start.py

# L'application détectera automatiquement:
# ✅ Quelle IA est configurée
# ✅ Si les clés API sont valides
# ✅ Utilisera le fallback si nécessaire
```

## 🎓 Obtenir des clés API

### OpenAI
1. Visitez: https://platform.openai.com/signup
2. Créez un compte
3. Allez dans API Keys: https://platform.openai.com/api-keys
4. Créez une nouvelle clé
5. Ajoutez des crédits (minimum $5)

### Anthropic
1. Visitez: https://console.anthropic.com/
2. Créez un compte
3. Allez dans API Keys
4. Créez une nouvelle clé
5. Ajoutez des crédits

### Ollama (Local - Gratuit)
1. Installez: https://ollama.ai/download
2. Lancez: `ollama serve`
3. Téléchargez un modèle: `ollama pull llama2`
4. Pas de clé API nécessaire!

## 📊 Comparaison des Performances

| Provider | Qualité | Vitesse | Coût | Privé |
|----------|---------|---------|------|-------|
| GPT-4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $$$ | ❌ |
| GPT-3.5-turbo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $ | ❌ |
| Claude 3 Opus | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $$$$ | ❌ |
| Claude 3 Sonnet | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $$ | ❌ |
| Llama 2 (Local) | ⭐⭐⭐ | ⭐⭐ | GRATUIT | ✅ |
| Mistral (Local) | ⭐⭐⭐⭐ | ⭐⭐⭐ | GRATUIT | ✅ |

## 🔒 Sécurité / Security

**Important:**
- ❌ Ne committez JAMAIS votre fichier .env avec de vraies clés
- ✅ Utilisez des variables d'environnement en production
- ✅ Rotez vos clés API régulièrement
- ✅ Limitez les permissions des clés API
- ✅ Surveillez l'utilisation pour éviter les coûts élevés

## 🐛 Dépannage / Troubleshooting

### L'IA ne fonctionne pas

```bash
# Vérifier que les dépendances sont installées
pip list | grep -E "openai|anthropic"

# Vérifier les clés API
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY:', 'Configured' if os.getenv('OPENAI_API_KEY') else 'Missing')"

# Tester la connexion
python3 -c "from ai_provider import EnhancedAIEngine; ai = EnhancedAIEngine(); print(ai.provider)"
```

### Erreur "Module not found: openai"

```bash
pip install openai anthropic
```

### Ollama ne démarre pas

```bash
# Vérifier si Ollama est installé
ollama --version

# Démarrer Ollama en debug
OLLAMA_DEBUG=1 ollama serve

# Vérifier les modèles installés
ollama list
```

### Coûts trop élevés

**Solutions:**
1. Utilisez GPT-3.5-turbo au lieu de GPT-4
2. Réduisez MAX_TOKENS dans .env
3. Passez à Claude Haiku (moins cher)
4. Utilisez un modèle local (gratuit)

## 📈 Amélioration Continue

Le système apprend et s'améliore avec:
- Chaque analyse de marché effectuée
- Feedback sur la précision des prédictions
- Patterns détectés dans les données historiques

## 🆘 Support

Pour toute question ou problème:
1. Consultez la documentation: README.md
2. Vérifiez les issues GitHub
3. Contactez: support@signaltrust.ai

## 📝 Changelog

### Version 3.0.0 (2026-02-07)
- ✨ Ajout du système AI Provider multi-fournisseur
- ✨ Support OpenAI GPT-4 et GPT-3.5-turbo
- ✨ Support Anthropic Claude 3
- ✨ Support modèles locaux via Ollama
- ✨ Fallback automatique vers simulation
- ✨ Configuration flexible via .env
- 🔧 Amélioration des prédictions
- 🔧 Amélioration de l'analyse de marché
- 📚 Documentation complète en français/anglais

---

**Fait avec ❤️ par SignalTrust AI**
