# SignalTrust Multi-Agent System EU

## 🤖 Vue d'ensemble

Le système multi-agent SignalTrust EU est une architecture distribuée qui orchestre 6 agents spécialisés pour l'analyse complète des marchés financiers.

## 📊 Architecture

```
┌───────────────────┐        ┌───────────────────┐
│   Client / UI    │◀──────▶│   Coordinator    │
│ (Web, Mobile…)   │  API   │   (CrewAI)       │
└───────────────────┘        └───────┬───────────┘
                                    │
               ┌────────────────────┼─────────────────────┐
               │                    │                     │
   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
   │ Crypto-Analyst │   │ Stock-Analyst   │   │ Whale-Watcher   │
   │ (FinGPT)       │   │ (Stock-GPT)     │   │ (whale-watcher)│
   └───────▲─────────┘   └───────▲─────────┘   └───────▲─────────┘
           │                     │                     │
   ┌───────┴───────┐   ┌───────┴───────┐   ┌─────────┴───────┐
   │  Market-News  │   │  Supervisor   │   │   LLM (OpenAI)  │
   │   (NewsGPT)   │   │ (Auto-GPT)   │   │                 │
   └───────────────┘   └───────────────┘   └─────────────────┘
```

## 🎯 Les 6 Agents

### 1️⃣ Crypto-Analyst (Port 8001)
**Rôle**: Analyse le marché des crypto-monnaies
- **Base**: FinGPT architecture
- **Données**: OHLCV, indicateurs techniques
- **API**: `POST /predict` avec symbole (ex: BTC/USDT)
- **Sortie**: Tendance, support/résistance, sentiment, prix cibles

### 2️⃣ Stock-Market Analyst (Port 8002)
**Rôle**: Analyse le marché des actions
- **Base**: Stock-GPT architecture  
- **Données**: Prix, volatilité, données fondamentales
- **API**: `POST /predict` avec ticker (ex: AAPL)
- **Sortie**: Recommandation Buy/Hold/Sell, prix cibles, confiance

### 3️⃣ Whale-Watcher (Port 8003)
**Rôle**: Surveillance des grandes transactions blockchain
- **Base**: whale-watcher architecture
- **Données**: Transactions > $5M sur BTC, ETH, BNB
- **API**: `GET /whales?network=btc&min_usd=5000000`
- **Sortie**: Patterns (accumulation/distribution), score de risque

### 4️⃣ Market-News Agent (Port 8004)
**Rôle**: Agrégation et résumé des actualités
- **Base**: NewsGPT architecture
- **Données**: RSS, NewsCatcher API, Google News
- **API**: `POST /news` avec topics
- **Sortie**: 5 insights clés, impact scores

### 5️⃣ Supervisor
**Rôle**: Orchestrateur et gestionnaire de quotas
- **Base**: Auto-GPT architecture
- **Fonctions**: 
  - Surveillance de l'état des agents
  - Gestion du budget API
  - Relance des tâches échouées
  - Logs et historique

### 6️⃣ Coordinator (Port 8000)
**Rôle**: Chef d'orchestre principal
- **Base**: CrewAI framework
- **Fonctions**:
  - Définition des workflows en YAML
  - Orchestration multi-agent
  - Agrégation des résultats
  - Calcul du score de confiance global

## 🚀 Installation

### Prérequis
- Docker et Docker Compose
- Clés API (voir section Configuration)

### Étape 1: Cloner le repository
```bash
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner
```

### Étape 2: Configurer les clés API
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer et ajouter vos clés API
nano .env
```

Clés requises:
- `OPENAI_API_KEY`: Pour tous les agents LLM
- `COINGECKO_API_KEY`: Pour les données crypto
- `ALPHAVANTAGE_API_KEY`: Pour les données boursières
- `WHALEALERT_API_KEY`: Pour les transactions blockchain
- `NEWS_CATCHER_API_KEY`: Pour les actualités

### Étape 3: Lancer les services
```bash
# Construire et démarrer tous les agents
docker compose up -d

# Vérifier que tous les services sont en ligne
docker compose ps
```

### Étape 4: Tester le système
```bash
# Test du coordinator
curl http://localhost:8000/

# Test du crypto analyst
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC/USDT"}'

# Test du stock analyst
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Test du whale watcher
curl "http://localhost:8003/whales?network=btc&min_usd=5000000"

# Test du news agent
curl -X POST http://localhost:8004/news \
  -H "Content-Type: application/json" \
  -d '{"topics": ["crypto", "stocks"], "max_items": 10}'
```

## 📡 API du Coordinator

### Lancer un workflow complet
```bash
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "ticker": "AAPL",
    "network": "btc",
    "topics": ["crypto", "stocks", "market"]
  }'
```

**Réponse**:
```json
{
  "workflow": "signaltrust_market_pipeline_eu",
  "status": "completed",
  "confidence": 0.95,
  "results": {
    "crypto_analyst": { "status": "success", "data": {...} },
    "stock_analyst": { "status": "success", "data": {...} },
    "whale_watcher": { "status": "success", "data": {...} },
    "news_agent": { "status": "success", "data": {...} }
  },
  "aggregated_data": {...},
  "timestamp": "2026-02-07T23:45:00"
}
```

### Lister les agents disponibles
```bash
curl http://localhost:8000/agents
```

## 🔧 Configuration avancée

### Personnaliser le workflow (crew.yaml)
```yaml
name: custom_workflow
description: Mon workflow personnalisé
agents:
  - name: crypto_analyst
    role: "Analyse crypto"
    task: "POST /predict"
    url: "http://crypto_agent:8000"
workflow:
  - step: crypto_analyst
    input:
      symbol: "ETH/USDT"
  - step: aggregator
```

### Ajuster les ressources Docker
```yaml
# docker-compose.yml
services:
  coordinator:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

## 📊 Monitoring

### Vérifier les logs
```bash
# Tous les services
docker compose logs -f

# Un service spécifique
docker compose logs -f crypto_agent
docker compose logs -f coordinator
```

### État du Supervisor
Le supervisor maintient un historique de toutes les tâches:
```bash
docker exec -it signaltrust_supervisor_eu python supervisor.py
```

## 🛑 Arrêt des services
```bash
# Arrêter tous les services
docker compose down

# Arrêter et supprimer les volumes
docker compose down -v
```

## 🔐 Sécurité

### Bonnes pratiques
1. ✅ Ne jamais commiter le fichier `.env`
2. ✅ Utiliser des clés API différentes pour dev/prod
3. ✅ Activer l'authentification sur l'API coordinator
4. ✅ Limiter l'accès réseau avec des firewalls
5. ✅ Surveiller l'utilisation des API pour éviter les surcoûts

### Budget API
Le supervisor limite automatiquement les appels API:
```bash
# Dans .env
API_BUDGET=200  # Maximum 200 appels par session
```

## 💰 Coûts estimés

### APIs gratuites (avec limitations)
- **CoinGecko**: Gratuit (50 calls/min)
- **Alpha Vantage**: Gratuit (500 calls/jour)
- **WhaleAlert**: Gratuit (1000 calls/jour)
- **NewsCatcher**: Trial disponible

### OpenAI (payant)
- **gpt-4o-mini**: ~$0.00015/1K tokens (entrée), ~$0.0006/1K tokens (sortie)
- **Usage typique**: 500-2000 tokens/analyse = $0.0003-$0.0012 par requête

**Budget mensuel estimé** (100 analyses/jour):
- APIs externes: Gratuit (dans les limites)
- OpenAI: ~$3-10/mois avec gpt-4o-mini

## 🐛 Dépannage

### Les agents ne démarrent pas
```bash
# Vérifier les logs
docker compose logs

# Reconstruire les images
docker compose build --no-cache
```

### Erreur "API key not found"
Vérifier que le fichier `.env` est présent et contient toutes les clés.

### Erreur de connexion entre agents
Vérifier que tous les services sont sur le même réseau Docker:
```bash
docker network inspect signaltrust-ai-scanner_signaltrust_network_eu
```

## 📚 Documentation des agents

Chaque agent expose sa propre documentation Swagger:
- Coordinator: http://localhost:8000/docs
- Crypto Agent: http://localhost:8001/docs
- Stock Agent: http://localhost:8002/docs
- Whale Agent: http://localhost:8003/docs
- News Agent: http://localhost:8004/docs

## 🤝 Contribution

Les contributions sont bienvenues! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

## 📝 License

Copyright © 2026 SignalTrust EU. All rights reserved.

---

**Made with ❤️ by SignalTrust EU Team**
