# Configuration Examples for SignalTrust EU Multi-Agent System

This document provides configuration examples for customizing the multi-agent system.

## 📋 Table of Contents

- [Environment Variables](#environment-variables)
- [Custom Workflows](#custom-workflows)
- [Agent Configuration](#agent-configuration)
- [Docker Compose Overrides](#docker-compose-overrides)
- [Supervisor Settings](#supervisor-settings)

## Environment Variables

### Complete .env example

```bash
# ============================================
# OPENAI CONFIGURATION
# ============================================
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini  # Options: gpt-4, gpt-4-turbo, gpt-4o-mini, gpt-3.5-turbo

# Temperature (creativity): 0.0 (deterministic) to 1.0 (creative)
AI_TEMPERATURE=0.7

# Max tokens per response
AI_MAX_TOKENS=2000

# ============================================
# DATA SOURCE APIS
# ============================================

# CoinGecko (Free: 50 calls/min)
COINGECKO_API_KEY=CG-your-key-here
CCXT_EXCHANGE=binance  # Options: binance, coinbase, kraken

# Alpha Vantage (Free: 500 calls/day)
ALPHAVANTAGE_API_KEY=your-key-here

# WhaleAlert (Free: 1000 calls/day)
WHALEALERT_API_KEY=your-key-here

# NewsCatcher (Trial available)
NEWS_CATCHER_API_KEY=your-key-here

# ============================================
# SUPERVISOR SETTINGS
# ============================================
API_BUDGET=200  # Maximum API calls per session
COORDINATOR_LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# ============================================
# DEVELOPMENT SETTINGS
# ============================================
DEBUG=false
LOG_LEVEL=INFO
```

## Custom Workflows

### Example 1: Crypto-focused workflow

Edit `agents/coordinator/crew.yaml`:

```yaml
name: crypto_focus_pipeline
description: |
  Workflow focused on cryptocurrency analysis
  
agents:
  - name: crypto_analyst
    role: "Deep crypto analysis"
    task: "POST /predict"
    url: "http://crypto_agent:8000"
    
  - name: whale_watcher
    role: "Monitor whale activity"
    task: "GET /whales"
    url: "http://whale_agent:8000"
    
  - name: news_agent
    role: "Crypto news only"
    task: "POST /news"
    url: "http://news_agent:8000"

workflow:
  - step: crypto_analyst
    input:
      symbol: "BTC/USDT"
      
  - step: crypto_analyst
    input:
      symbol: "ETH/USDT"
      
  - step: whale_watcher
    input:
      network: "btc"
      min_usd: 10000000  # $10M+ transactions only
      
  - step: whale_watcher
    input:
      network: "eth"
      min_usd: 5000000
      
  - step: news_agent
    input:
      topics: ["bitcoin", "ethereum", "DeFi", "crypto regulation"]
      max_items: 20
```

### Example 2: Stock-focused workflow

```yaml
name: stock_focus_pipeline
description: |
  Workflow focused on stock market analysis
  
agents:
  - name: stock_analyst
    role: "Analyze multiple stocks"
    task: "POST /predict"
    url: "http://stock_agent:8000"
    
  - name: news_agent
    role: "Market news"
    task: "POST /news"
    url: "http://news_agent:8000"

workflow:
  - step: stock_analyst
    input:
      ticker: "AAPL"
      
  - step: stock_analyst
    input:
      ticker: "GOOGL"
      
  - step: stock_analyst
    input:
      ticker: "MSFT"
      
  - step: news_agent
    input:
      topics: ["technology stocks", "FAANG", "market trends"]
      max_items: 15
```

### Example 3: Quick scan workflow

```yaml
name: quick_scan
description: |
  Fast market scan with minimal agents
  
agents:
  - name: crypto_analyst
    role: "Quick crypto check"
    task: "POST /predict"
    url: "http://crypto_agent:8000"
    
  - name: stock_analyst
    role: "Quick stock check"
    task: "POST /predict"
    url: "http://stock_agent:8000"

workflow:
  - step: crypto_analyst
    input:
      symbol: "BTC/USDT"
      
  - step: stock_analyst
    input:
      ticker: "SPY"  # S&P 500 ETF
```

## Agent Configuration

### Crypto Agent Customization

Create `agents/crypto_agent/config.py`:

```python
# Custom configuration for crypto agent

# Supported exchanges
EXCHANGES = ["binance", "coinbase", "kraken", "bitfinex"]

# Default timeframes
TIMEFRAMES = {
    "short": "1h",
    "medium": "4h",
    "long": "1d"
}

# Technical indicators to calculate
INDICATORS = [
    "SMA_20",
    "SMA_50",
    "RSI_14",
    "MACD",
    "Bollinger_Bands"
]

# Prompt template
ANALYSIS_PROMPT = """
Analyze {symbol} cryptocurrency:

Data: {data}

Provide:
1. Trend (bullish/bearish/sideways)
2. Key support/resistance levels
3. Market sentiment
4. Price targets (24h, 7d, 30d) with probabilities
5. Risk factors

Respond in JSON format.
"""
```

### Stock Agent Customization

Create `agents/stock_agent/config.py`:

```python
# Custom configuration for stock agent

# Analysis parameters
VOLATILITY_PERIOD = 30  # days
CONFIDENCE_THRESHOLD = 0.6

# Recommendation logic
RECOMMENDATION_RULES = {
    "strong_buy": {"score": 0.8, "confidence": 0.7},
    "buy": {"score": 0.6, "confidence": 0.6},
    "hold": {"score": 0.4, "confidence": 0.5},
    "sell": {"score": 0.2, "confidence": 0.6},
    "strong_sell": {"score": 0.0, "confidence": 0.7}
}

# Prompt template
ANALYSIS_PROMPT = """
Analyze {ticker} stock:

Recent data: {data}

Provide:
1. Current assessment
2. 30-day volatility
3. Analyst sentiment
4. Technical analysis
5. Buy/Hold/Sell recommendation with confidence (0-1)
6. Price targets (7d, 30d) with probabilities

Respond in JSON format.
"""
```

## Docker Compose Overrides

### Production configuration

Create `docker-compose.prod.yml`:

```yaml
version: "3.9"

services:
  coordinator:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  crypto_agent:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    restart: always
    
  stock_agent:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    restart: always
    
  whale_agent:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: always
    
  news_agent:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: always

  supervisor:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: always
```

Usage:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Development with hot-reload

Create `docker-compose.dev.yml`:

```yaml
version: "3.9"

services:
  coordinator:
    volumes:
      - ./agents/coordinator:/app:delegated
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    environment:
      - DEBUG=true
      
  crypto_agent:
    volumes:
      - ./agents/crypto_agent:/app:delegated
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    environment:
      - DEBUG=true
```

Usage:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Supervisor Settings

### Custom supervisor configuration

Edit `agents/supervisor/auto_gpt.cfg`:

```ini
# Auto-GPT Configuration for SignalTrust EU

[General]
AiName = SignalTrustSuperEU
AiRole = Superviseur qui orchestre les sous-agents
ApiBudget = 500  # Increase for production

[Plugins]
# Available plugins
EnableWebSearch = true
EnableFileManagement = true
EnableTerminal = true

[Logging]
LogLevel = INFO  # DEBUG, INFO, WARNING, ERROR
LogFile = /app/workspace/supervisor.log

[Retry]
MaxRetries = 3
RetryDelay = 2  # seconds

[Monitoring]
HealthCheckInterval = 60  # seconds
AlertOnFailure = true
```

## Advanced Configurations

### Load Balancing Multiple Instances

```yaml
version: "3.9"

services:
  # Multiple crypto agent instances
  crypto_agent_1:
    build: ./agents/crypto_agent
    environment:
      - INSTANCE_ID=1
      
  crypto_agent_2:
    build: ./agents/crypto_agent
    environment:
      - INSTANCE_ID=2
      
  # Load balancer
  nginx:
    image: nginx:alpine
    ports:
      - "8001:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - crypto_agent_1
      - crypto_agent_2
```

### Rate Limiting

Add to agent code:

```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(request: Request, data: PredictRequest):
    # ... your code
```

### Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def get_market_data(symbol: str, timestamp: int):
    # timestamp rounded to 5 minutes for caching
    # ... fetch data
    pass

# Usage
current_5min = int(datetime.now().timestamp() / 300) * 300
data = get_market_data("BTC/USDT", current_5min)
```

---

**For more examples, see:**
- [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) - Complete system guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture diagrams
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
