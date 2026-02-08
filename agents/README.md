# SignalTrust EU - Agents Directory

This directory contains the implementation of all specialized agents for the SignalTrust EU multi-agent system.

## 📁 Structure

```
agents/
├── coordinator/          # CrewAI-based orchestrator (Port 8000)
│   ├── main.py
│   ├── crew.yaml
│   ├── Dockerfile
│   └── requirements.txt
│
├── crypto_agent/        # FinGPT-based crypto analyst (Port 8001)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── stock_agent/         # Stock-GPT-based stock analyst (Port 8002)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── whale_agent/         # Whale transaction monitor (Port 8003)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── news_agent/          # NewsGPT-based news aggregator (Port 8004)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── social_sentiment_agent/  # Social media sentiment (Port 8005) ✨ NEW
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── onchain_agent/       # On-chain data analyst (Port 8006) ✨ NEW
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── supervisor/          # Auto-GPT-based supervisor
    ├── supervisor.py
    ├── auto_gpt.cfg
    ├── Dockerfile
    └── requirements.txt
```

## 🤖 Agent Details

### Core Agents

#### Coordinator (Port 8000)
- **Framework**: CrewAI
- **Purpose**: Orchestrates all other agents
- **API**: 
  - `POST /run-workflow` - Execute complete market analysis
  - `GET /agents` - List all available agents
- **Config**: `crew.yaml`

#### Crypto Agent (Port 8001)
- **Base**: FinGPT architecture
- **Purpose**: Cryptocurrency market analysis
- **API**: 
  - `POST /predict` - Analyze crypto symbol
- **Example**:
  ```json
  {"symbol": "BTC/USDT"}
  ```

#### Stock Agent (Port 8002)
- **Base**: Stock-GPT architecture
- **Purpose**: Stock market analysis
- **API**: 
  - `POST /predict` - Analyze stock ticker
- **Example**:
  ```json
  {"ticker": "AAPL"}
  ```

#### Whale Agent (Port 8003)
- **Base**: whale-watcher architecture
- **Purpose**: Monitor large blockchain transactions
- **API**: 
  - `GET /whales?network=btc&min_usd=5000000`

#### News Agent (Port 8004)
- **Base**: NewsGPT architecture
- **Purpose**: Aggregate and analyze market news
- **API**: 
  - `POST /news` - Get news for topics
- **Example**:
  ```json
  {"topics": ["crypto", "stocks"], "max_items": 10}
  ```

### Complementary Agents ✨ NEW

#### Social Sentiment Agent (Port 8005)
- **Purpose**: Real-time social media sentiment analysis
- **Platforms**: Twitter, Reddit, Discord, Telegram
- **Technology**: BERT-finance sentiment model
- **API**:
  - `POST /analyze` - Analyze sentiment for symbol
  - `GET /trending` - Get trending symbols
- **Priority**: ⭐⭐⭐⭐ (High)

#### On-Chain Data Agent (Port 8006)
- **Purpose**: Blockchain metrics and on-chain analysis
- **Metrics**: Active addresses, whale activity, exchange flows
- **Technology**: Glassnode SDK, Dune Analytics
- **API**:
  - `POST /analyze` - Get on-chain metrics
  - `GET /whale-alerts` - Recent whale transactions
- **Priority**: ⭐⭐⭐⭐ (High)

#### Supervisor (No external port)
- **Base**: Auto-GPT architecture
- **Purpose**: Monitor agents, manage API quotas, retry failed tasks
- **Config**: `auto_gpt.cfg`

## 🚀 Quick Start

### Run all agents:
```bash
# From the project root
docker compose up -d
```

### Test an individual agent:
```bash
# Test crypto agent
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC/USDT"}'

# Test social sentiment agent (NEW)
curl -X POST http://localhost:8005/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "platforms": ["twitter", "reddit"]}'

# Test on-chain agent (NEW)
curl -X POST http://localhost:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "network": "mainnet"}'
```

### Run complete workflow:
```bash
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "ticker": "AAPL",
    "network": "btc",
    "topics": ["crypto", "stocks"]
  }'
```

## 🔧 Development

### Build a single agent:
```bash
cd agents/social_sentiment_agent
docker build -t signaltrust-social-sentiment .
docker run -p 8005:8000 \
  -e OPENAI_API_KEY=your_key \
  -e TWITTER_API_KEY=your_key \
  signaltrust-social-sentiment
```

### Run agent locally (without Docker):
```bash
cd agents/onchain_agent
pip install -r requirements.txt
export GLASSNODE_API_KEY=your_key
python main.py
```

## 📊 API Documentation

Each agent exposes Swagger documentation at `/docs`:
- Coordinator: http://localhost:8000/docs
- Crypto Agent: http://localhost:8001/docs
- Stock Agent: http://localhost:8002/docs
- Whale Agent: http://localhost:8003/docs
- News Agent: http://localhost:8004/docs
- **Social Sentiment: http://localhost:8005/docs** ✨ NEW
- **On-Chain Data: http://localhost:8006/docs** ✨ NEW

## 🔐 Environment Variables

Each agent requires:
- `OPENAI_API_KEY` - For LLM inference

Additional agent-specific keys:
- **Crypto Agent**: `COINGECKO_API_KEY`, `CCXT_EXCHANGE`
- **Stock Agent**: `ALPHAVANTAGE_API_KEY`
- **Whale Agent**: `WHALEALERT_API_KEY`
- **News Agent**: `NEWS_CATCHER_API_KEY`
- **Social Sentiment**: `TWITTER_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` ✨
- **On-Chain**: `GLASSNODE_API_KEY`, `DUNE_API_KEY` ✨

See `.env.example` for complete list.

## 🧪 Testing

### Health checks:
```bash
# Check all agents (including new ones)
for port in 8000 8001 8002 8003 8004 8005 8006; do
  echo "Testing port $port..."
  curl http://localhost:$port/health
done
```

### Integration test:
```bash
# Run the complete workflow
./test_agents.sh
```

## 🗺️ Roadmap: Additional Agents

The following complementary agents are planned for future releases:

| Agent | Priority | Purpose |
|-------|----------|---------|
| Macro-Economics | ⭐⭐⭐ | Fed, CPI, GDP events |
| Risk Manager | ⭐⭐⭐ | VaR, correlations, stress testing |
| Portfolio Optimizer | ⭐⭐⭐⭐ | Position sizing (Kelly criterion) |
| Explainability | ⭐⭐⭐ | SHAP/LIME for model transparency |
| Alternative Data | ⭐⭐ | Google Trends, satellite imagery |
| Compliance/AML | ⭐⭐ | KYC, blacklist filtering |
| Options Pricing | ⭐⭐ | Greeks, implied volatility |

## 📝 Adding a New Agent

1. Create a new directory under `agents/`
2. Implement `main.py` with FastAPI
3. Create `Dockerfile` and `requirements.txt`
4. Add service to `docker-compose.yml`
5. Register in coordinator's `crew.yaml`
6. Update this README

## 🐛 Troubleshooting

### Agent not starting:
```bash
# Check logs
docker compose logs social_sentiment_agent

# Rebuild
docker compose build social_sentiment_agent
docker compose up -d social_sentiment_agent
```

### Port already in use:
```bash
# Change port in docker-compose.yml
ports:
  - "8105:8000"  # Use different external port
```

## 📚 Further Reading

- [COMPREHENSIVE_ARCHITECTURE.md](../COMPREHENSIVE_ARCHITECTURE.md) - Full architecture guide
- [MULTI_AGENT_SYSTEM.md](../MULTI_AGENT_SYSTEM.md) - Complete system documentation
- [README.md](../README.md) - Project overview
- Individual agent READMEs in each subdirectory

---

**SignalTrust EU - Multi-Agent System**  
**Version**: 2.0.0 (with Social Sentiment & On-Chain agents)  
**Last Updated**: February 2026
