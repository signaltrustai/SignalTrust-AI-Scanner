# 🚀 SignalTrust AI - Quick Implementation Guide

This guide provides step-by-step instructions to implement the comprehensive architecture enhancements.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Infrastructure Setup](#phase-1-infrastructure-setup)
3. [Phase 2: Deploy New Agents](#phase-2-deploy-new-agents)
4. [Phase 3: Meta-Model Integration](#phase-3-meta-model-integration)
5. [Phase 4: Testing & Validation](#phase-4-testing--validation)
6. [Phase 5: Production Deployment](#phase-5-production-deployment)

---

## Prerequisites

### Required Software
- Docker 20.10+ and Docker Compose v2.0+
- Python 3.9+
- Git

### Required API Keys
```bash
# Core agents
OPENAI_API_KEY=sk-...
COINGECKO_API_KEY=...
ALPHAVANTAGE_API_KEY=...
WHALEALERT_API_KEY=...
NEWS_CATCHER_API_KEY=...

# New complementary agents
TWITTER_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
GLASSNODE_API_KEY=...
DUNE_API_KEY=...
FRED_API_KEY=...
```

### Hardware Requirements
- **Minimum**: 8GB RAM, 4 CPU cores, 50GB storage
- **Recommended**: 16GB RAM, 8 CPU cores, 100GB storage
- **Production**: 32GB+ RAM, 16+ CPU cores, 500GB+ storage

---

## Phase 1: Infrastructure Setup

### Step 1.1: Update Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your API keys
nano .env
```

Add the new agent API keys to `.env`:
```bash
# Complementary Agents
TWITTER_API_KEY=your_twitter_key
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
GLASSNODE_API_KEY=your_glassnode_key
DUNE_API_KEY=your_dune_key
FRED_API_KEY=your_fred_key
```

### Step 1.2: Install Python Dependencies

```bash
# Install base dependencies
pip install -r requirements.txt

# Install optional ML libraries (recommended)
pip install xgboost lightgbm shap mlflow

# Install optional RAG libraries
pip install sentence-transformers faiss-cpu
```

### Step 1.3: Verify Agent Structure

```bash
# Check that all agent directories exist
ls -la agents/

# Should see:
# - coordinator/
# - crypto_agent/
# - stock_agent/
# - whale_agent/
# - news_agent/
# - social_sentiment_agent/  ← NEW
# - onchain_agent/  ← NEW
# - macro_economics_agent/  ← NEW
# - portfolio_optimizer_agent/  ← NEW
# - supervisor/
```

---

## Phase 2: Deploy New Agents

### Step 2.1: Build All Agents

```bash
# Build all containers
docker compose build

# Or build specific agents
docker compose build social_sentiment_agent
docker compose build onchain_agent
docker compose build macro_economics_agent
docker compose build portfolio_optimizer_agent
```

### Step 2.2: Start All Services

```bash
# Start all agents in detached mode
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Step 2.3: Verify Agents Are Running

```bash
# Test health endpoints
curl http://localhost:8000/health  # Coordinator
curl http://localhost:8001/health  # Crypto
curl http://localhost:8002/health  # Stock
curl http://localhost:8003/health  # Whale
curl http://localhost:8004/health  # News
curl http://localhost:8005/health  # Social Sentiment ← NEW
curl http://localhost:8006/health  # On-Chain ← NEW
curl http://localhost:8007/health  # Macro Economics ← NEW
curl http://localhost:8008/health  # Portfolio Optimizer ← NEW
```

Expected response:
```json
{
  "status": "healthy",
  "agent": "social_sentiment",
  "timestamp": "2026-02-08T00:00:00"
}
```

---

## Phase 3: Meta-Model Integration

### Step 3.1: Test Meta-Model Module

```bash
# Test the meta-model implementation
python meta_model.py
```

Expected output:
```
Breakout Score: 0.745
Classification: Strong Breakout

Engineered 30 features

==================================================
Meta-Model Module Ready!
==================================================
```

### Step 3.2: Train Meta-Model (Optional)

```python
# example_train_meta_model.py
from meta_model import MetaModel, FeatureEngineer
import pandas as pd
import numpy as np

# Load historical data (you need to provide this)
# X_train, y_train = load_historical_features()

# Initialize and train
model = MetaModel(model_type="xgboost")
# model.train(X_train, y_train)

print("Meta-model trained successfully!")
```

### Step 3.3: Integrate with Main Application

```python
# In your main application
from meta_model import HybridSignalGenerator, MetaModel

# Initialize
meta_model = MetaModel()
signal_generator = HybridSignalGenerator(meta_model)

# Generate signal
signal = await signal_generator.generate_signal(
    ticker="BTC",
    llm_result=llm_analysis,
    market_data=market_data
)

print(f"Signal Score: {signal['final_score']}")
print(f"Recommendation: {signal['recommendation']}")
```

---

## Phase 4: Testing & Validation

### Step 4.1: Test Individual Agents

#### Test Social Sentiment Agent
```bash
curl -X POST http://localhost:8005/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "platforms": ["twitter", "reddit"],
    "timeframe": "24h"
  }'
```

#### Test On-Chain Agent
```bash
curl -X POST http://localhost:8006/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "network": "mainnet",
    "metrics": ["all"]
  }'
```

#### Test Macro Economics Agent
```bash
curl -X POST http://localhost:8007/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "region": "US",
    "timeframe": "7d",
    "indicators": ["all"]
  }'
```

#### Test Portfolio Optimizer
```bash
curl -X POST http://localhost:8008/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "signals": [
      {"symbol": "BTC", "score": 0.85, "expected_return": 0.3, "volatility": 0.4},
      {"symbol": "ETH", "score": 0.75, "expected_return": 0.25, "volatility": 0.35}
    ],
    "total_capital": 100000,
    "method": "kelly",
    "risk_tolerance": 0.5,
    "max_position_size": 0.25
  }'
```

### Step 4.2: Run Integration Test

```bash
# Test complete workflow
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "ticker": "AAPL",
    "network": "btc",
    "topics": ["crypto", "stocks"]
  }'
```

### Step 4.3: Check Logs for Errors

```bash
# Check all agent logs
docker compose logs --tail=100

# Check specific agent
docker compose logs social_sentiment_agent --tail=50
```

---

## Phase 5: Production Deployment

### Step 5.1: Security Checklist

- [ ] All API keys in environment variables (not hardcoded)
- [ ] TLS/HTTPS enabled on API gateway
- [ ] Rate limiting configured
- [ ] JWT authentication enabled
- [ ] Network policies enforced (if using Kubernetes)
- [ ] Regular security scans (Trivy, Snyk)

### Step 5.2: Monitoring Setup

```bash
# Add Prometheus metrics (example)
pip install prometheus-client

# In your agent code:
from prometheus_client import Counter, Histogram

request_count = Counter('agent_requests_total', 'Total requests')
request_duration = Histogram('agent_request_duration_seconds', 'Request duration')
```

### Step 5.3: Configure Backups

```bash
# Backup configuration
# Add to crontab:
0 2 * * * docker compose exec -T coordinator python backup_data.py

# Or use cloud backup
# Configure in cloud_storage_manager.py
```

### Step 5.4: Load Balancing (Optional)

For high-traffic deployments, add nginx load balancer:

```nginx
# nginx.conf
upstream agents {
    server localhost:8005;
    server localhost:8006;
    server localhost:8007;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://agents;
    }
}
```

---

## 📊 Expected Performance Metrics

After full deployment, you should achieve:

| Metric | Target | Achieved |
|--------|--------|----------|
| API Latency | < 300ms | ⏱️ Test |
| Throughput | > 800 RPS | 📈 Monitor |
| Uptime | > 99.5% | 🎯 Track |
| Signal Accuracy | > 62% | 🎲 Validate |

---

## 🐛 Troubleshooting

### Agent Won't Start

```bash
# Check logs
docker compose logs agent_name

# Common issues:
# 1. Missing API key → Check .env file
# 2. Port conflict → Change port in docker-compose.yml
# 3. Out of memory → Increase Docker memory limit
```

### Slow Performance

```bash
# Check resource usage
docker stats

# Optimize:
# 1. Enable caching (Redis)
# 2. Use quantized models
# 3. Increase concurrent workers
```

### Connection Refused

```bash
# Check if agent is running
docker compose ps

# Check network
docker network ls
docker network inspect signaltrust_network_eu

# Restart services
docker compose restart
```

---

## 📚 Next Steps

1. **Read Full Documentation**
   - [COMPREHENSIVE_ARCHITECTURE.md](COMPREHENSIVE_ARCHITECTURE.md) - Complete architecture
   - [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) - Agent system details

2. **Train Meta-Models**
   - Collect historical data
   - Train XGBoost/LightGBM models
   - Set up SHAP explainer

3. **Add More Agents**
   - Risk Manager (VaR calculations)
   - Compliance/AML agent
   - Options Pricing agent

4. **Implement RAG**
   - Set up vector database (Milvus/Pinecone)
   - Index news articles and reports
   - Enable semantic search

5. **Set Up Continuous Learning**
   - Implement data collection pipeline
   - Set up nightly retraining
   - Configure MLflow for model versioning

---

## 💡 Tips & Best Practices

### Development
- Use `.env.local` for local development
- Keep API keys secure (never commit)
- Test agents independently before integration

### Production
- Use Kubernetes for orchestration
- Implement proper logging (ELK stack)
- Monitor with Grafana + Prometheus
- Set up alerting (PagerDuty, Slack)

### Optimization
- Cache frequently accessed data (Redis)
- Use async/await for I/O operations
- Batch API requests when possible
- Quantize LLM models for faster inference

---

## 🆘 Support

- **GitHub Issues**: https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues
- **Documentation**: See /docs directory
- **Email**: support@signaltrust.ai

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Implementation Ready

---

*This guide will help you implement the comprehensive SignalTrust AI architecture efficiently and effectively.*
