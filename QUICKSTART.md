# 🚀 Quick Start Guide - SignalTrust EU Multi-Agent System

Get started with the SignalTrust EU Multi-Agent System in 5 minutes!

## ⚡ Prerequisites

- Docker & Docker Compose installed
- API keys ready (see below)

## 📝 Step 1: Get API Keys (Free Tiers Available)

### Required:
- **OpenAI** (required): https://platform.openai.com/api-keys
  - Cost: ~$0.01-0.10 per analysis with gpt-4o-mini

### Optional (free tiers):
- **CoinGecko**: https://www.coingecko.com/en/api (50 calls/min free)
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (500/day free)
- **WhaleAlert**: https://whale-alert.io/ (1000/day free)
- **NewsCatcher**: https://www.newscatcherapi.com/ (trial available)

## 🛠️ Step 2: Setup

```bash
# Clone the repository
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner

# Run the setup script
./setup_agents.sh
```

The setup script will:
1. Create `.env` from `.env.example`
2. Prompt you to add API keys
3. Build all Docker images
4. Start all 6 agents
5. Run health checks

## ⚙️ Step 3: Configure API Keys

Edit the `.env` file:

```bash
nano .env
```

Add your keys:
```bash
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini

# Optional but recommended
COINGECKO_API_KEY=your-key-here
ALPHAVANTAGE_API_KEY=your-key-here
WHALEALERT_API_KEY=your-key-here
NEWS_CATCHER_API_KEY=your-key-here
```

## 🎯 Step 4: Start the System

```bash
# Using the setup script
./setup_agents.sh

# OR using Docker Compose directly
docker compose up -d

# OR using Make
make up
```

## ✅ Step 5: Verify Installation

```bash
# Run tests
./test_agents.sh

# OR using Make
make test
```

Expected output:
```
Testing Coordinator... ✅ PASSED
Testing Crypto Agent... ✅ PASSED
Testing Stock Agent... ✅ PASSED
Testing Whale Agent... ✅ PASSED
Testing News Agent... ✅ PASSED
```

## 🎮 Step 6: Try It Out!

### Option A: Using cURL

```bash
# Run complete workflow
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "ticker": "AAPL",
    "network": "btc",
    "topics": ["crypto", "stocks"]
  }' | python3 -m json.tool
```

### Option B: Using Python

```bash
python3 example_multi_agent_usage.py
```

### Option C: Using Make

```bash
make workflow
```

### Option D: Using the Web Interface

Open in your browser: http://localhost:8000/docs

## 📊 Available Endpoints

| Service | Port | Endpoint | Description |
|---------|------|----------|-------------|
| Coordinator | 8000 | POST /run-workflow | Run complete analysis |
| Crypto Agent | 8001 | POST /predict | Analyze crypto |
| Stock Agent | 8002 | POST /predict | Analyze stocks |
| Whale Agent | 8003 | GET /whales | Monitor whales |
| News Agent | 8004 | POST /news | Get news |

## 🔍 Useful Commands

```bash
# View logs
make logs                    # All services
make logs-coordinator        # Coordinator only
make logs-crypto            # Crypto agent only

# Restart services
make restart                 # All services
make restart-coordinator     # Coordinator only

# Check status
make ps                      # Container status
make test-quick             # Quick health check

# Stop everything
make down                    # Stop services
make clean                   # Stop and remove volumes
```

## 📚 Next Steps

1. **Read the full documentation**: [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)
2. **Explore API docs**: http://localhost:8000/docs
3. **Customize workflows**: Edit `agents/coordinator/crew.yaml`
4. **Monitor performance**: `make logs`

## 🐛 Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# Rebuild images
make rebuild

# Check logs
make logs
```

### API key errors
```bash
# Verify .env file exists and has keys
cat .env | grep API_KEY

# Restart after adding keys
make restart
```

### Port conflicts
Edit `docker-compose.yml` to use different ports:
```yaml
ports:
  - "8100:8000"  # Change external port
```

## 💡 Tips

1. **Start simple**: Use only OpenAI key initially, add others later
2. **Monitor costs**: Check OpenAI usage dashboard regularly
3. **Use gpt-4o-mini**: Most cost-effective model for this use case
4. **Development mode**: Use `make dev` for hot-reload during development
5. **Save money**: External API calls are cached when possible

## 🎉 Success!

You're now running the SignalTrust EU Multi-Agent System!

**What you have:**
- 6 specialized AI agents working together
- Complete market analysis pipeline
- Real-time crypto, stock, and blockchain monitoring
- AI-powered news aggregation
- Orchestrated workflow with confidence scoring

## 📞 Need Help?

- **Documentation**: [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md)
- **GitHub Issues**: https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues
- **Email**: support@signaltrust.ai

---

**Happy Trading! 🚀**

*Made with ❤️ by SignalTrust EU Team*
