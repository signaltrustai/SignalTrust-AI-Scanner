# Guide d'Intégration des Agents IA

## 📋 Vue d'ensemble

Le système SignalTrust AI Scanner intègre maintenant **9 agents IA spécialisés** qui travaillent ensemble pour fournir une analyse complète des marchés financiers.

## 🤖 Agents Disponibles

### 1. **Coordinator** (Port 8000)
- **Rôle**: Orchestrateur principal utilisant CrewAI
- **API**: Coordonne tous les autres agents
- **Endpoint**: `http://localhost:8000`

### 2. **Crypto Agent** (Port 8001)
- **Rôle**: Analyse des crypto-monnaies avec FinGPT
- **API**: Prédictions et indicateurs techniques
- **Endpoint**: `http://localhost:8001`

### 3. **Stock Agent** (Port 8002)
- **Rôle**: Analyse des actions avec Stock-GPT
- **API**: Recommandations Buy/Hold/Sell
- **Endpoint**: `http://localhost:8002`

### 4. **Whale Agent** (Port 8003)
- **Rôle**: Surveillance des grandes transactions blockchain
- **API**: Détection de patterns d'accumulation/distribution
- **Endpoint**: `http://localhost:8003`

### 5. **News Agent** (Port 8004)
- **Rôle**: Agrégation et analyse des actualités
- **API**: Insights clés et scores d'impact
- **Endpoint**: `http://localhost:8004`

### 6. **Social Sentiment Agent** (Port 8005)
- **Rôle**: Analyse du sentiment sur les réseaux sociaux
- **API**: Sentiment Twitter, Reddit, Discord, Telegram
- **Endpoint**: `http://localhost:8005`

### 7. **On-Chain Agent** (Port 8006)
- **Rôle**: Analyse des métriques blockchain on-chain
- **API**: Métriques Glassnode, flux d'échanges
- **Endpoint**: `http://localhost:8006`

### 8. **Macro Economics Agent** (Port 8007)
- **Rôle**: Analyse des indicateurs macroéconomiques
- **API**: GDP, inflation, taux d'intérêt, événements Fed
- **Endpoint**: `http://localhost:8007`

### 9. **Portfolio Optimizer** (Port 8008)
- **Rôle**: Optimisation d'allocation de portefeuille
- **API**: Calcul de risque, VaR, Sharpe ratio
- **Endpoint**: `http://localhost:8008`

## 🚀 Démarrage Rapide

### Prérequis
```bash
# Docker et Docker Compose installés
docker --version
docker compose --version

# Clés API configurées dans .env
OPENAI_API_KEY=sk-...
COINGECKO_API_KEY=...
ALPHAVANTAGE_API_KEY=...
# ... etc
```

### Lancement des Agents

#### Option 1: Utiliser le script de setup
```bash
./setup_agents.sh
```

#### Option 2: Commandes Docker manuelles
```bash
# Démarrer tous les agents
docker compose up -d

# Vérifier le statut
docker compose ps

# Voir les logs
docker compose logs -f

# Arrêter tous les agents
docker compose down
```

### Tester les Agents
```bash
./test_agents.sh
```

## 📡 Utilisation via l'Interface Web

### 1. Accéder au Dashboard des Agents
```
http://localhost:5000/agents
```

### 2. Fonctionnalités Disponibles
- ✅ **Statut en temps réel** de tous les agents
- 🔄 **Refresh automatique** toutes les 30 secondes
- 🧪 **Tests individuels** de chaque agent
- 📚 **Accès direct** à la documentation API (Swagger)
- 🚀 **Workflow complet** d'analyse multi-agents

### 3. Lancer une Analyse Complète
1. Remplir le formulaire avec:
   - Symbole crypto (ex: BTC/USDT)
   - Ticker action (ex: AAPL)
   - Réseau blockchain (BTC, ETH, BNB)
2. Cliquer sur "Lancer l'Analyse Complète"
3. Voir les résultats agrégés de tous les agents

## 🔌 API REST Endpoints

### Statut des Agents
```http
GET /api/agents/status
```
Retourne le statut de santé de tous les agents.

**Réponse:**
```json
{
  "success": true,
  "agents": {
    "coordinator": {"success": true, "status": "ok"},
    "crypto": {"success": true, "status": "ok"},
    ...
  }
}
```

### Workflow Complet
```http
POST /api/agents/workflow
Content-Type: application/json

{
  "symbol": "BTC/USDT",
  "ticker": "AAPL",
  "network": "btc",
  "topics": ["crypto", "stocks", "market"]
}
```

### Analyse Crypto
```http
POST /api/agents/crypto/analyze
Content-Type: application/json

{
  "symbol": "BTC/USDT",
  "timeframe": "1d"
}
```

### Analyse Action
```http
POST /api/agents/stock/analyze
Content-Type: application/json

{
  "ticker": "AAPL"
}
```

### Surveillance Whale
```http
GET /api/agents/whale/watch?network=btc&min_usd=5000000
```

### Actualités
```http
POST /api/agents/news/get
Content-Type: application/json

{
  "topics": ["crypto", "stocks"],
  "max_items": 10
}
```

### Sentiment Social
```http
POST /api/agents/sentiment/analyze
Content-Type: application/json

{
  "symbol": "BTC",
  "platforms": ["twitter", "reddit"]
}
```

### Trending Symbols
```http
GET /api/agents/sentiment/trending
```

### Analyse On-Chain
```http
POST /api/agents/onchain/analyze
Content-Type: application/json

{
  "symbol": "BTC",
  "network": "mainnet"
}
```

### Indicateurs Macroéconomiques
```http
POST /api/agents/macro/indicators
Content-Type: application/json

{
  "indicators": ["gdp", "inflation", "interest_rate"]
}
```

### Événements Fed
```http
GET /api/agents/macro/fed-events
```

### Optimisation de Portefeuille
```http
POST /api/agents/portfolio/optimize
Content-Type: application/json

{
  "holdings": {
    "BTC": 1.5,
    "ETH": 10,
    "AAPL": 50
  },
  "risk_tolerance": "moderate"
}
```

### Calcul de Risque
```http
POST /api/agents/portfolio/risk
Content-Type: application/json

{
  "holdings": {
    "BTC": 1.5,
    "ETH": 10
  }
}
```

### Analyse Complète Multi-Agents
```http
POST /api/agents/complete-analysis
Content-Type: application/json

{
  "symbol": "BTC/USDT",
  "asset_type": "crypto"
}
```
Combine: marché, sentiment, actualités, on-chain.

## 💻 Utilisation Programmatique (Python)

### Import du Client
```python
from agent_client import get_agent_client

# Obtenir l'instance du client
client = get_agent_client()
```

### Vérifier le Statut des Agents
```python
# Vérifier tous les agents
status = client.check_all_agents()
print(status)

# Vérifier un agent spécifique
health = client.check_health("crypto")
print(health)
```

### Analyser une Crypto
```python
result = client.analyze_crypto("BTC/USDT", timeframe="1d")
print(result)
```

### Analyser une Action
```python
result = client.analyze_stock("AAPL")
print(result)
```

### Surveiller les Whales
```python
result = client.watch_whales(network="btc", min_usd=5_000_000)
print(result)
```

### Obtenir des Actualités
```python
result = client.get_news(
    topics=["crypto", "technology"],
    max_items=10
)
print(result)
```

### Analyser le Sentiment
```python
result = client.analyze_sentiment(
    symbol="BTC",
    platforms=["twitter", "reddit"]
)
print(result)
```

### Workflow Complet
```python
result = client.run_workflow(
    symbol="ETH/USDT",
    ticker="GOOGL",
    network="eth",
    topics=["crypto", "technology"]
)
print(result)
```

### Analyse Complète d'un Symbole
```python
# Combine plusieurs agents automatiquement
result = client.complete_analysis(
    symbol="BTC/USDT",
    asset_type="crypto"
)

print("Analyse de marché:", result["analysis"]["market"])
print("Sentiment:", result["analysis"]["sentiment"])
print("Actualités:", result["analysis"]["news"])
print("On-chain:", result["analysis"]["onchain"])
```

## 🔧 Configuration

### Variables d'Environnement
```bash
# Flask App
PORT=5000
DEBUG=False
SECRET_KEY=your-secret-key

# Agent System
AGENT_BASE_URL=http://localhost

# AI Providers
OPENAI_API_KEY=sk-...

# Data Sources
COINGECKO_API_KEY=...
ALPHAVANTAGE_API_KEY=...
WHALEALERT_API_KEY=...
NEWS_CATCHER_API_KEY=...
TWITTER_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
GLASSNODE_API_KEY=...
DUNE_API_KEY=...
FRED_API_KEY=...
WORLD_BANK_API_KEY=...
EIA_API_KEY=...
```

### Ports des Agents
| Agent | Port | Conteneur Docker |
|-------|------|------------------|
| Coordinator | 8000 | signaltrust_coordinator_eu |
| Crypto | 8001 | signaltrust_crypto_eu |
| Stock | 8002 | signaltrust_stock_eu |
| Whale | 8003 | signaltrust_whale_eu |
| News | 8004 | signaltrust_news_eu |
| Social Sentiment | 8005 | signaltrust_social_sentiment_eu |
| On-Chain | 8006 | signaltrust_onchain_eu |
| Macro Economics | 8007 | signaltrust_macro_eu |
| Portfolio Optimizer | 8008 | signaltrust_portfolio_eu |

## 🐛 Dépannage

### Agent ne démarre pas
```bash
# Vérifier les logs
docker compose logs <agent_name>

# Exemple: Crypto Agent
docker compose logs crypto_agent

# Rebuild l'agent
docker compose build crypto_agent
docker compose up -d crypto_agent
```

### Port déjà utilisé
```bash
# Modifier le port dans docker-compose.yml
# Au lieu de "8001:8000", utiliser "8101:8000"
```

### Clés API manquantes
```bash
# Vérifier le fichier .env
cat .env | grep API_KEY

# Copier l'exemple si nécessaire
cp .env.example .env
nano .env
```

### Agent timeout
```python
# Augmenter le timeout dans agent_client.py
client = AgentClient()
client.timeout = 60  # 60 secondes au lieu de 30
```

## 📚 Documentation Supplémentaire

- **Architecture complète**: [COMPREHENSIVE_ARCHITECTURE.md](COMPREHENSIVE_ARCHITECTURE.md)
- **Système multi-agents**: [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)
- **Guide des agents**: [agents/README.md](agents/README.md)
- **Setup OpenAI**: [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md)
- **API principale**: [README.md](README.md)

## 🎯 Exemples d'Utilisation

### Exemple 1: Analyse Rapide BTC
```python
from agent_client import get_agent_client

client = get_agent_client()

# Analyse crypto
crypto_result = client.analyze_crypto("BTC/USDT")

# Sentiment social
sentiment = client.analyze_sentiment("BTC")

# Métriques on-chain
onchain = client.analyze_onchain("BTC")

print(f"Prix: {crypto_result.get('price')}")
print(f"Sentiment: {sentiment.get('overall_sentiment')}")
print(f"Active Addresses: {onchain.get('active_addresses')}")
```

### Exemple 2: Portfolio Analysis
```python
# Mon portefeuille actuel
my_holdings = {
    "BTC": 1.5,
    "ETH": 10,
    "AAPL": 50,
    "GOOGL": 20
}

# Calculer le risque
risk = client.calculate_risk(my_holdings)
print(f"VaR: {risk.get('var')}")
print(f"Sharpe Ratio: {risk.get('sharpe_ratio')}")

# Obtenir des recommandations d'optimisation
optimized = client.optimize_portfolio(my_holdings, "moderate")
print(f"Allocation recommandée: {optimized.get('recommended_allocation')}")
```

### Exemple 3: Market Intelligence
```python
# Obtenir une vue complète du marché
workflow = client.run_workflow(
    symbol="BTC/USDT",
    ticker="AAPL",
    network="btc",
    topics=["crypto", "stocks", "technology", "fed"]
)

# Extraire les insights clés
print("=== Crypto Analysis ===")
print(workflow["results"]["crypto"])

print("\n=== Stock Analysis ===")
print(workflow["results"]["stock"])

print("\n=== Market News ===")
print(workflow["results"]["news"]["insights"][:5])

print("\n=== Macro Economics ===")
print(workflow["results"]["macro"])
```

## 🔐 Sécurité

- ✅ Toutes les routes nécessitent une authentification (`@login_required`)
- ✅ Les clés API sont stockées dans `.env` (non commitées)
- ✅ Les requêtes aux agents ont des timeouts configurables
- ✅ Validation des entrées utilisateur
- ✅ Gestion sécurisée des erreurs (pas de leak d'infos sensibles)

## 🚀 Prochaines Étapes

1. **Test de Charge**: Tester avec plusieurs utilisateurs simultanés
2. **Monitoring**: Ajouter Prometheus/Grafana pour le monitoring
3. **Cache**: Implémenter Redis pour cacher les résultats fréquents
4. **Rate Limiting**: Limiter les appels API par utilisateur
5. **Webhooks**: Ajouter des notifications push pour les événements importants

## 📞 Support

Pour toute question ou problème:
- 📖 Documentation: [GitHub Wiki](https://github.com/signaltrustai/SignalTrust-AI-Scanner/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues)
- 💬 Email: signaltrustai@gmail.com

---

**Version**: 2.0.0  
**Dernière mise à jour**: Février 2026  
**Auteurs**: SignalTrust AI Team
