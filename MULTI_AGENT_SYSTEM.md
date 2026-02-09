# 🚀 SignalTrust AI — Enhanced Multi‑Agent System + Colab Integration

This document introduces the improved multi‑agent architecture and provides a direct Google Colab integration for testing, orchestrating, and extending the SignalTrust AI system.

---

## 🧠 Multi‑Agent Intelligence System (Enhanced)

SignalTrust AI uses a distributed multi‑agent architecture designed for deep market intelligence.
Each agent specializes in a specific domain and collaborates through a central orchestrator.

### Core Agents
- 🎯 **Coordinator (Port 8000)** — CrewAI-based orchestrator
- 💰 **Crypto Agent (8001)** — FinGPT crypto analysis
- 📈 **Stock Agent (8002)** — StockGPT stock analysis
- 🐋 **Whale Agent (8003)** — Blockchain whale tracking
- 📰 **News Agent (8004)** — Market news aggregation

### Advanced Agents
- 💬 **Social Sentiment (8005)** — Twitter, Reddit, Discord sentiment
- ⛓️ **On‑Chain Data (8006)** — Blockchain metrics
- 🌍 **Macro Economics (8007)** — Global macro analysis
- 📊 **Portfolio Optimizer (8008)** — Allocation & risk optimization

### Supervisor
- 🔍 **Auto‑GPT Supervisor** — Monitors, corrects, and improves agent behavior

---

## 📘 Official Google Colab Notebook

Launch SignalTrust AI directly in Google Colab — no installation required.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/signaltrustai/SignalTrust-AI-Scanner/blob/main/SignalTrust_AI_Scanner.ipynb)

The notebook includes:
- Automatic environment setup
- Flask server launch
- ngrok exposure
- Multi‑agent startup
- API testing examples

---

## ⚡ Quick Start (Multi‑Agent System)

```bash
./setup_agents.sh
./test_agents.sh
```

---

## 📊 Architecture

```
┌───────────────────┐        ┌────────────────────┐
│   Client / UI     │◀──────▶│   Coordinator      │
│ (Web, Mobile…)    │  API   │   (CrewAI, 8000)   │
└───────────────────┘        └───────┬────────────┘
                                     │
        ┌──────────┬─────────┬───────┼───────┬──────────┬──────────┐
        │          │         │       │       │          │          │
   ┌────▼────┐ ┌───▼────┐ ┌─▼──────┐│  ┌────▼────┐ ┌──▼───────┐ │
   │ Crypto  │ │ Stock  │ │ Whale  ││  │  News   │ │ Social   │ │
   │ (8001)  │ │ (8002) │ │ (8003) ││  │ (8004)  │ │ Sent.    │ │
   │ FinGPT  │ │StockGPT│ │Whale-W ││  │ NewsGPT │ │ (8005)   │ │
   └─────────┘ └────────┘ └────────┘│  └─────────┘ └──────────┘ │
                                     │                            │
                      ┌──────────────┼──────────────┐             │
                      │              │              │             │
                 ┌────▼─────┐ ┌─────▼─────┐ ┌──────▼──────┐      │
                 │ On-Chain │ │ Macro     │ │ Portfolio   │      │
                 │  (8006)  │ │ Econ.     │ │ Optimizer   │      │
                 │ Metrics  │ │  (8007)   │ │  (8008)     │      │
                 └──────────┘ └───────────┘ └─────────────┘      │
                                                                  │
                               ┌──────────────────────┐           │
                               │  Supervisor          │◀──────────┘
                               │  (Auto-GPT)          │
                               └──────────────────────┘
```

## 🎯 The 9 Agents

### 1️⃣ Coordinator (Port 8000)
**Role**: Central orchestrator
- **Base**: CrewAI framework
- **API**: `POST /run-workflow`, `GET /agents`, `GET /health`
- **Output**: Aggregated analysis with confidence score

### 2️⃣ Crypto Agent (Port 8001)
**Role**: Cryptocurrency market analysis
- **Base**: FinGPT architecture
- **Data**: OHLCV, technical indicators
- **API**: `POST /predict` with symbol (e.g. BTC/USDT)
- **Output**: Trend, support/resistance, sentiment, price targets

### 3️⃣ Stock Agent (Port 8002)
**Role**: Stock market analysis
- **Base**: StockGPT architecture
- **Data**: Price, volatility, fundamentals
- **API**: `POST /predict` with ticker (e.g. AAPL)
- **Output**: Buy/Hold/Sell recommendation, price targets, confidence

### 4️⃣ Whale Agent (Port 8003)
**Role**: Large blockchain transaction monitoring
- **Data**: Transactions > $5M on BTC, ETH, BNB
- **API**: `GET /whales?network=btc&min_usd=5000000`
- **Output**: Accumulation/distribution patterns, risk score

### 5️⃣ News Agent (Port 8004)
**Role**: News aggregation and sentiment
- **Data**: RSS, NewsCatcher API, Google News
- **API**: `POST /news` with topics
- **Output**: 5 key insights, impact scores

### 6️⃣ Social Sentiment Agent (Port 8005)
**Role**: Social media sentiment analysis
- **Data**: Twitter, Reddit, Discord
- **API**: `POST /analyze` with query and sources
- **Output**: Sentiment scores, trending topics, influencer activity

### 7️⃣ On-Chain Agent (Port 8006)
**Role**: Blockchain on-chain metrics
- **Data**: Glassnode, Dune Analytics
- **API**: `POST /analyze` with network and metrics
- **Output**: TVL, gas fees, active addresses, DeFi metrics

### 8️⃣ Macro Economics Agent (Port 8007)
**Role**: Global macroeconomic analysis
- **Data**: FRED, World Bank, EIA
- **API**: `POST /indicators` with indicator list
- **Output**: GDP, inflation, unemployment, Fed events

### 9️⃣ Portfolio Optimizer Agent (Port 8008)
**Role**: Portfolio allocation and risk management
- **API**: `POST /optimize` with assets and risk tolerance
- **Output**: Optimal allocation, expected return, risk metrics

### 🔍 Supervisor (No public port)
**Role**: Auto-GPT based oversight
- Monitors agent health
- Manages API budget
- Retries failed tasks
- Logs all activity

---

## 🚀 Installation

### Prerequisites
- Docker and Docker Compose
- API keys (see Configuration section)

### Step 1: Clone the repository
```bash
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner
```

### Step 2: Configure API keys
```bash
cp .env.example .env
nano .env
```

Required keys:
- `OPENAI_API_KEY`: For all LLM agents
- `COINGECKO_API_KEY`: For crypto data
- `ALPHAVANTAGE_API_KEY`: For stock data
- `WHALEALERT_API_KEY`: For blockchain transactions
- `NEWS_CATCHER_API_KEY`: For news

Optional (enhanced AI):
- `DEEPSEEK_API_KEY`: Strong reasoning for predictions
- `GOOGLE_AI_API_KEY`: Fast Gemini for summaries
- `ANTHROPIC_API_KEY`: Claude for deep analysis

### Step 3: Launch all services
```bash
./setup_agents.sh
```

Or manually:
```bash
docker compose build
docker compose up -d
docker compose ps
```

### Step 4: Test the system
```bash
./test_agents.sh
```

Or test individual agents:
```bash
# Coordinator
curl http://localhost:8000/

# Crypto prediction
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC/USDT"}'

# Stock prediction
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Whale monitoring
curl "http://localhost:8003/whales?network=btc&min_usd=5000000"

# Full workflow
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "ticker": "AAPL",
    "network": "btc",
    "topics": ["crypto", "stocks", "market"]
  }'
```

---

## 📡 API Documentation

Each agent exposes Swagger docs:

| Agent | URL |
|-------|-----|
| Coordinator | http://localhost:8000/docs |
| Crypto Agent | http://localhost:8001/docs |
| Stock Agent | http://localhost:8002/docs |
| Whale Agent | http://localhost:8003/docs |
| News Agent | http://localhost:8004/docs |
| Social Sentiment | http://localhost:8005/docs |
| On-Chain Agent | http://localhost:8006/docs |
| Macro Economics | http://localhost:8007/docs |
| Portfolio Optimizer | http://localhost:8008/docs |

---

## 🔐 Security

1. ✅ Never commit the `.env` file
2. ✅ Use different API keys for dev/prod
3. ✅ Enable authentication on the coordinator API
4. ✅ Limit network access with firewalls
5. ✅ Monitor API usage to avoid overcharges

---

## 💰 Cost Estimates

### Free APIs (with limits)
- **CoinGecko**: Free (50 calls/min)
- **Alpha Vantage**: Free (500 calls/day)
- **WhaleAlert**: Free (1000 calls/day)
- **NewsCatcher**: Trial available

### AI Providers (pay-per-use)
- **OpenAI gpt-4o-mini**: ~$0.00015/1K tokens (input)
- **DeepSeek**: ~$0.14/1M tokens (very affordable)
- **Google Gemini**: Free tier (60 req/min)

**Monthly budget** (100 analyses/day): ~$3-10/month

---

## 🛑 Stop Services

```bash
docker compose down      # Stop all
docker compose down -v   # Stop and remove volumes
```

---

## 🐛 Troubleshooting

### Agents won't start
```bash
docker compose logs
docker compose build --no-cache
```

### "API key not found"
Check `.env` file is present and contains all required keys.

### Agent connection errors
```bash
docker network inspect signaltrust-ai-scanner_signaltrust_network_eu
```

---

**Made with ❤️ by SignalTrust AI Team**
