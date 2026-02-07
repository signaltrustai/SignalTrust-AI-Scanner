# SignalTrust EU - Agents Directory

This directory contains the implementation of all 6 specialized agents for the SignalTrust EU multi-agent system.

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
└── supervisor/          # Auto-GPT-based supervisor
    ├── supervisor.py
    ├── auto_gpt.cfg
    ├── Dockerfile
    └── requirements.txt
```

## 🤖 Agent Details

### Coordinator (Port 8000)
- **Framework**: CrewAI
- **Purpose**: Orchestrates all other agents
- **API**: 
  - `POST /run-workflow` - Execute complete market analysis
  - `GET /agents` - List all available agents
- **Config**: `crew.yaml`

### Crypto Agent (Port 8001)
- **Base**: FinGPT architecture
- **Purpose**: Cryptocurrency market analysis
- **API**: 
  - `POST /predict` - Analyze crypto symbol
- **Example**:
  ```json
  {"symbol": "BTC/USDT"}
  ```

### Stock Agent (Port 8002)
- **Base**: Stock-GPT architecture
- **Purpose**: Stock market analysis
- **API**: 
  - `POST /predict` - Analyze stock ticker
- **Example**:
  ```json
  {"ticker": "AAPL"}
  ```

### Whale Agent (Port 8003)
- **Base**: whale-watcher architecture
- **Purpose**: Monitor large blockchain transactions
- **API**: 
  - `GET /whales?network=btc&min_usd=5000000`

### News Agent (Port 8004)
- **Base**: NewsGPT architecture
- **Purpose**: Aggregate and analyze market news
- **API**: 
  - `POST /news` - Get news for topics
- **Example**:
  ```json
  {"topics": ["crypto", "stocks"], "max_items": 10}
  ```

### Supervisor (No external port)
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
cd agents/crypto_agent
docker build -t signaltrust-crypto-agent .
docker run -p 8001:8000 -e OPENAI_API_KEY=your_key signaltrust-crypto-agent
```

### Run agent locally (without Docker):
```bash
cd agents/crypto_agent
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
python main.py
```

## 📊 API Documentation

Each agent exposes Swagger documentation at `/docs`:
- Coordinator: http://localhost:8000/docs
- Crypto Agent: http://localhost:8001/docs
- Stock Agent: http://localhost:8002/docs
- Whale Agent: http://localhost:8003/docs
- News Agent: http://localhost:8004/docs

## 🔐 Environment Variables

Each agent requires:
- `OPENAI_API_KEY` - For LLM inference

Additional agent-specific keys:
- **Crypto Agent**: `COINGECKO_API_KEY`, `CCXT_EXCHANGE`
- **Stock Agent**: `ALPHAVANTAGE_API_KEY`
- **Whale Agent**: `WHALEALERT_API_KEY`
- **News Agent**: `NEWS_CATCHER_API_KEY`

See `.env.example` for complete list.

## 🧪 Testing

### Health checks:
```bash
# Check all agents
for port in 8000 8001 8002 8003 8004; do
  echo "Testing port $port..."
  curl http://localhost:$port/health
done
```

### Integration test:
```bash
# Run the complete workflow
./test_agents.sh
```

## 📝 Adding a New Agent

1. Create a new directory under `agents/`
2. Implement `main.py` with FastAPI
3. Create `Dockerfile` and `requirements.txt`
4. Add service to `docker-compose.yml`
5. Register in coordinator's `crew.yaml`

## 🐛 Troubleshooting

### Agent not starting:
```bash
# Check logs
docker compose logs crypto_agent

# Rebuild
docker compose build crypto_agent
docker compose up -d crypto_agent
```

### Port already in use:
```bash
# Change port in docker-compose.yml
ports:
  - "8101:8000"  # Use different external port
```

## 📚 Further Reading

- [MULTI_AGENT_SYSTEM.md](../MULTI_AGENT_SYSTEM.md) - Complete system documentation
- [README.md](../README.md) - Project overview
- Individual agent READMEs in each subdirectory

---

**SignalTrust EU - Multi-Agent System**
