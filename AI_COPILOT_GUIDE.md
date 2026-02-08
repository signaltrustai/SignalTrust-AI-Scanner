# 🤖 Guide de Collaboration pour Copilot AI / AI Copilot Collaboration Guide

> **Français** 🇫🇷 | **English** 🇬🇧

---

## 🇫🇷 Version Française

### Bienvenue, Assistant IA!

Ce guide vous aidera à comprendre et contribuer efficacement au projet **SignalTrust AI Market Scanner**. Utilisez ce document comme référence contextuelle pour mieux comprendre la structure du projet, les conventions de code et les tâches courantes.

---

### 📋 Vue d'ensemble du projet

**SignalTrust AI Market Scanner** est une plateforme complète d'analyse de marché alimentée par l'IA qui combine:
- Scanner de marché en temps réel (actions, crypto, forex, indices)
- Analyse technique avancée
- Prédictions IA avec apprentissage automatique
- Système multi-agents (6 agents spécialisés)
- Application web Flask avec authentification utilisateur
- Traitement des paiements et abonnements
- Intégration API OpenAI, Anthropic, et modèles locaux

**Version actuelle**: v3.0.0 (2026-02-07)

---

### 🏗️ Architecture du Projet

#### Structure des Dossiers Principaux
```
SignalTrust-AI-Scanner/
├── app.py                      # Application Flask principale
├── agents/                     # Système multi-agents (Docker)
│   ├── coordinator/           # Orchestrateur CrewAI (Port 8000)
│   ├── crypto_agent/          # Analyse crypto FinGPT (Port 8001)
│   ├── stock_agent/           # Analyse actions Stock-GPT (Port 8002)
│   ├── whale_agent/           # Surveillance blockchain (Port 8003)
│   ├── news_agent/            # Agrégation actualités (Port 8004)
│   └── supervisor/            # Auto-GPT supervision
├── static/                    # Fichiers statiques (CSS, JS)
├── templates/                 # Templates HTML Flask
├── data/                      # Données utilisateurs et transactions
└── config/                    # Fichiers de configuration

Modules Python clés:
├── market_scanner.py          # Scanner de marché
├── market_analyzer.py         # Analyse technique
├── ai_predictor.py            # Prédictions IA
├── ai_provider.py             # Gestion fournisseurs IA
├── user_auth.py               # Authentification utilisateurs
├── payment_processor.py       # Traitement paiements
├── whale_watcher.py           # Détection baleines crypto
└── cloud_storage_manager.py   # Stockage cloud
```

---

### 🔑 Concepts Clés

#### 1. **Système Multi-Agents**
- 6 agents spécialisés travaillant ensemble
- Communication via API REST
- Orchestration par CrewAI
- Chaque agent a son propre conteneur Docker

#### 2. **Fournisseurs IA**
- **OpenAI**: GPT-4 pour analyse de marché
- **Anthropic**: Claude pour analyse alternative
- **Local**: Ollama pour modèles gratuits locaux
- Configuration via `.env`

#### 3. **Plans d'Abonnement**
- **Free**: 10 scans/jour, fonctionnalités de base
- **Basic**: $29.99/mois, scans illimités
- **Pro**: $79.99/mois, prédictions IA illimitées + API
- **Enterprise**: $299.99/mois, modèles IA personnalisés

#### 4. **Sécurité**
- Hachage de mots de passe avec PBKDF2-HMAC-SHA256
- Gestion de sessions sécurisée
- Validation de cartes (algorithme Luhn)
- Protection XSS et CSRF

---

### 💻 Tâches de Développement Courantes

#### Démarrer l'Application
```bash
# Linux/Mac
./start.sh

# Windows
start.bat

# Python (multi-plateforme)
python3 start.py
```

#### Configuration des Agents Multi-Agents
```bash
# Installer et démarrer tous les agents
./setup_agents.sh

# Tester tous les agents
./test_agents.sh

# Commandes Makefile
make build       # Construire les conteneurs
make up          # Démarrer les services
make down        # Arrêter les services
make logs        # Voir les logs
```

#### Tests
```bash
# Tests système complet
python3 test_complete_system.py

# Tests IA
python3 test_ai_system.py

# Tests OpenAI
python3 test_openai_integration.py

# Tests agents
python3 test_agents.sh
```

#### Configuration IA
```bash
# Copier le template d'environnement
cp .env.example .env

# Éditer et ajouter vos clés API
nano .env
```

---

### 📚 Points d'Entrée API Principaux

#### Authentification
- `POST /api/auth/register` - Enregistrer un utilisateur
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion

#### Données de Marché
- `GET /api/markets/overview` - Vue d'ensemble des marchés
- `POST /api/markets/scan` - Scanner des marchés spécifiques
- `GET /api/markets/trending` - Actifs tendance

#### Analyse
- `POST /api/analyze/technical` - Analyse technique
- `POST /api/analyze/sentiment` - Analyse de sentiment
- `POST /api/analyze/patterns` - Détection de patterns

#### Prédictions IA
- `POST /api/predict/price` - Prédictions de prix
- `POST /api/predict/signals` - Signaux de trading
- `POST /api/predict/risk` - Évaluation des risques

#### Multi-Agents (Docker)
- `POST http://localhost:8000/run-workflow` - Exécuter workflow
- `POST http://localhost:8001/predict` - Agent crypto
- `POST http://localhost:8002/predict` - Agent actions
- `GET http://localhost:8003/whales` - Agent baleines
- `POST http://localhost:8004/news` - Agent actualités

---

### 🎯 Conventions de Code

#### Style Python
- Suivre PEP 8
- Indentation: 4 espaces
- Noms de fonctions: `snake_case`
- Noms de classes: `PascalCase`
- Constantes: `UPPER_CASE`

#### Exemple de Structure de Fonction
```python
def analyze_market_data(symbol: str, timeframe: str = "1d") -> dict:
    """
    Analyser les données de marché pour un symbole donné.
    
    Args:
        symbol: Symbole du ticker (ex: "AAPL", "BTC")
        timeframe: Période de temps (ex: "1d", "1h", "5m")
    
    Returns:
        dict: Résultats d'analyse avec indicateurs techniques
    """
    # Votre code ici
    pass
```

#### Gestion des Erreurs
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Error in operation: {str(e)}")
    return {"success": False, "error": str(e)}
```

---

### 🔧 Modules Clés à Connaître

#### 1. **ai_provider.py**
Gère les différents fournisseurs IA (OpenAI, Anthropic, Local).
```python
from ai_provider import AIProvider

ai = AIProvider()
analysis = ai.analyze_market("AAPL", market_data)
```

#### 2. **market_scanner.py**
Scanner de marché en temps réel.
```python
from market_scanner import MarketScanner

scanner = MarketScanner()
results = scanner.scan_markets(["stocks", "crypto"])
```

#### 3. **ai_predictor.py**
Prédictions basées sur l'IA.
```python
from ai_predictor import AIPredictor

predictor = AIPredictor()
prediction = predictor.predict_price("BTC", days=7)
```

#### 4. **user_auth.py**
Authentification et gestion des utilisateurs.
```python
from user_auth import UserAuth

auth = UserAuth()
user = auth.register_user(email, password, full_name)
```

---

### 📖 Documentation de Référence

#### Documentation Principale
- `README.md` - Vue d'ensemble complète
- `QUICKSTART.md` - Guide de démarrage rapide
- `MULTI_AGENT_SYSTEM.md` - Guide du système multi-agents
- `ARCHITECTURE.md` - Diagrammes d'architecture
- `CONFIGURATION.md` - Exemples de configuration

#### Guides Spécifiques
- `OPENAI_SETUP_GUIDE.md` - Configuration OpenAI
- `AI_ENHANCEMENT_GUIDE.md` - Guide d'amélioration IA
- `CLOUD_STORAGE_GUIDE.md` - Guide stockage cloud
- `ADMIN_ACCESS.md` - Accès administrateur

#### Documentation Française
- `GUIDE_COMPLET_FINAL.md` - Guide complet en français
- `GUIDE_RAPIDE.md` - Guide rapide en français
- `GUIDE_UTILISATION.md` - Guide d'utilisation
- `RÉSUMÉ_AMÉLIORATIONS.md` - Résumé des améliorations

---

### 🐛 Débogage et Logs

#### Activer le Mode Debug
```bash
export DEBUG=True
python3 app.py
```

#### Voir les Logs Docker
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f coordinator
docker-compose logs -f crypto_agent
```

#### Vérifier le Statut des Services
```bash
# Tous les conteneurs
docker-compose ps

# Santé des services
curl http://localhost:8000/health
curl http://localhost:8001/health
```

---

### ⚠️ Informations Importantes

#### Compte Administrateur par Défaut
- **Email**: signaltrustai@gmail.com
- **Mot de passe**: !Obiwan12!
- **Niveau d'accès**: Enterprise (Accès complet)
- ⚠️ **CHANGER CE MOT DE PASSE EN PRODUCTION!**

#### Variables d'Environnement Requises
```bash
# IA
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4

# APIs de Données
COINGECKO_API_KEY=your-key
ALPHA_VANTAGE_API_KEY=your-key
WHALE_ALERT_API_KEY=your-key
NEWSCATCHER_API_KEY=your-key

# Configuration
PORT=5000
DEBUG=False
```

---

### 🚀 Commandes Rapides

```bash
# Démarrage rapide
./start.sh

# Configuration agents
./setup_agents.sh

# Tests
python3 test_complete_system.py

# Docker
make up        # Démarrer
make down      # Arrêter
make logs      # Logs
make restart   # Redémarrer

# Git
git status
git add .
git commit -m "Description des changements"
git push
```

---

### 📞 Support

- **Email**: support@signaltrust.ai
- **GitHub**: https://github.com/signaltrustai/SignalTrust-AI-Scanner
- **Documentation**: https://docs.signaltrust.ai

---

## 🇬🇧 English Version

### Welcome, AI Assistant!

This guide will help you understand and effectively contribute to the **SignalTrust AI Market Scanner** project. Use this document as contextual reference to better understand the project structure, code conventions, and common tasks.

---

### 📋 Project Overview

**SignalTrust AI Market Scanner** is a comprehensive AI-powered market analysis platform that combines:
- Real-time market scanning (stocks, crypto, forex, indices)
- Advanced technical analysis
- AI predictions with machine learning
- Multi-agent system (6 specialized agents)
- Flask web application with user authentication
- Payment processing and subscriptions
- OpenAI, Anthropic, and local model integration

**Current Version**: v3.0.0 (2026-02-07)

---

### 🏗️ Project Architecture

#### Main Folder Structure
```
SignalTrust-AI-Scanner/
├── app.py                      # Main Flask application
├── agents/                     # Multi-agent system (Docker)
│   ├── coordinator/           # CrewAI orchestrator (Port 8000)
│   ├── crypto_agent/          # FinGPT crypto analysis (Port 8001)
│   ├── stock_agent/           # Stock-GPT stock analysis (Port 8002)
│   ├── whale_agent/           # Blockchain monitoring (Port 8003)
│   ├── news_agent/            # News aggregation (Port 8004)
│   └── supervisor/            # Auto-GPT supervision
├── static/                    # Static files (CSS, JS)
├── templates/                 # Flask HTML templates
├── data/                      # User and transaction data
└── config/                    # Configuration files

Key Python Modules:
├── market_scanner.py          # Market scanner
├── market_analyzer.py         # Technical analysis
├── ai_predictor.py            # AI predictions
├── ai_provider.py             # AI provider management
├── user_auth.py               # User authentication
├── payment_processor.py       # Payment processing
├── whale_watcher.py           # Crypto whale detection
└── cloud_storage_manager.py   # Cloud storage
```

---

### 🔑 Key Concepts

#### 1. **Multi-Agent System**
- 6 specialized agents working together
- Communication via REST API
- Orchestration by CrewAI
- Each agent has its own Docker container

#### 2. **AI Providers**
- **OpenAI**: GPT-4 for market analysis
- **Anthropic**: Claude for alternative analysis
- **Local**: Ollama for free local models
- Configuration via `.env`

#### 3. **Subscription Plans**
- **Free**: 10 scans/day, basic features
- **Basic**: $29.99/month, unlimited scans
- **Pro**: $79.99/month, unlimited AI predictions + API
- **Enterprise**: $299.99/month, custom AI models

#### 4. **Security**
- Password hashing with PBKDF2-HMAC-SHA256
- Secure session management
- Card validation (Luhn algorithm)
- XSS and CSRF protection

---

### 💻 Common Development Tasks

#### Start the Application
```bash
# Linux/Mac
./start.sh

# Windows
start.bat

# Python (cross-platform)
python3 start.py
```

#### Multi-Agent Setup
```bash
# Install and start all agents
./setup_agents.sh

# Test all agents
./test_agents.sh

# Makefile commands
make build       # Build containers
make up          # Start services
make down        # Stop services
make logs        # View logs
```

#### Testing
```bash
# Complete system tests
python3 test_complete_system.py

# AI tests
python3 test_ai_system.py

# OpenAI tests
python3 test_openai_integration.py

# Agent tests
python3 test_agents.sh
```

#### AI Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit and add your API keys
nano .env
```

---

### 📚 Main API Endpoints

#### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout

#### Market Data
- `GET /api/markets/overview` - Market overview
- `POST /api/markets/scan` - Scan specific markets
- `GET /api/markets/trending` - Trending assets

#### Analysis
- `POST /api/analyze/technical` - Technical analysis
- `POST /api/analyze/sentiment` - Sentiment analysis
- `POST /api/analyze/patterns` - Pattern detection

#### AI Predictions
- `POST /api/predict/price` - Price predictions
- `POST /api/predict/signals` - Trading signals
- `POST /api/predict/risk` - Risk assessment

#### Multi-Agent (Docker)
- `POST http://localhost:8000/run-workflow` - Run workflow
- `POST http://localhost:8001/predict` - Crypto agent
- `POST http://localhost:8002/predict` - Stock agent
- `GET http://localhost:8003/whales` - Whale agent
- `POST http://localhost:8004/news` - News agent

---

### 🎯 Code Conventions

#### Python Style
- Follow PEP 8
- Indentation: 4 spaces
- Function names: `snake_case`
- Class names: `PascalCase`
- Constants: `UPPER_CASE`

#### Example Function Structure
```python
def analyze_market_data(symbol: str, timeframe: str = "1d") -> dict:
    """
    Analyze market data for a given symbol.
    
    Args:
        symbol: Ticker symbol (e.g., "AAPL", "BTC")
        timeframe: Time period (e.g., "1d", "1h", "5m")
    
    Returns:
        dict: Analysis results with technical indicators
    """
    # Your code here
    pass
```

#### Error Handling
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Error in operation: {str(e)}")
    return {"success": False, "error": str(e)}
```

---

### 🔧 Key Modules to Know

#### 1. **ai_provider.py**
Manages different AI providers (OpenAI, Anthropic, Local).
```python
from ai_provider import AIProvider

ai = AIProvider()
analysis = ai.analyze_market("AAPL", market_data)
```

#### 2. **market_scanner.py**
Real-time market scanner.
```python
from market_scanner import MarketScanner

scanner = MarketScanner()
results = scanner.scan_markets(["stocks", "crypto"])
```

#### 3. **ai_predictor.py**
AI-based predictions.
```python
from ai_predictor import AIPredictor

predictor = AIPredictor()
prediction = predictor.predict_price("BTC", days=7)
```

#### 4. **user_auth.py**
User authentication and management.
```python
from user_auth import UserAuth

auth = UserAuth()
user = auth.register_user(email, password, full_name)
```

---

### 📖 Reference Documentation

#### Main Documentation
- `README.md` - Complete overview
- `QUICKSTART.md` - Quick start guide
- `MULTI_AGENT_SYSTEM.md` - Multi-agent system guide
- `ARCHITECTURE.md` - Architecture diagrams
- `CONFIGURATION.md` - Configuration examples

#### Specific Guides
- `OPENAI_SETUP_GUIDE.md` - OpenAI setup
- `AI_ENHANCEMENT_GUIDE.md` - AI enhancement guide
- `CLOUD_STORAGE_GUIDE.md` - Cloud storage guide
- `ADMIN_ACCESS.md` - Administrator access

#### French Documentation
- `GUIDE_COMPLET_FINAL.md` - Complete guide in French
- `GUIDE_RAPIDE.md` - Quick guide in French
- `GUIDE_UTILISATION.md` - Usage guide
- `RÉSUMÉ_AMÉLIORATIONS.md` - Improvements summary

---

### 🐛 Debugging and Logs

#### Enable Debug Mode
```bash
export DEBUG=True
python3 app.py
```

#### View Docker Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f coordinator
docker-compose logs -f crypto_agent
```

#### Check Service Status
```bash
# All containers
docker-compose ps

# Service health
curl http://localhost:8000/health
curl http://localhost:8001/health
```

---

### ⚠️ Important Information

#### Default Administrator Account
- **Email**: signaltrustai@gmail.com
- **Password**: !Obiwan12!
- **Access Level**: Enterprise (Full Access)
- ⚠️ **CHANGE THIS PASSWORD IN PRODUCTION!**

#### Required Environment Variables
```bash
# AI
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4

# Data APIs
COINGECKO_API_KEY=your-key
ALPHA_VANTAGE_API_KEY=your-key
WHALE_ALERT_API_KEY=your-key
NEWSCATCHER_API_KEY=your-key

# Configuration
PORT=5000
DEBUG=False
```

---

### 🚀 Quick Commands

```bash
# Quick start
./start.sh

# Agent setup
./setup_agents.sh

# Tests
python3 test_complete_system.py

# Docker
make up        # Start
make down      # Stop
make logs      # Logs
make restart   # Restart

# Git
git status
git add .
git commit -m "Description of changes"
git push
```

---

### 📞 Support

- **Email**: support@signaltrust.ai
- **GitHub**: https://github.com/signaltrustai/SignalTrust-AI-Scanner
- **Documentation**: https://docs.signaltrust.ai

---

**Made with ❤️ by SignalTrust AI**

**🤖 Happy Collaborating, AI Assistant!**
