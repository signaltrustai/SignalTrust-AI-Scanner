# 🚀 Enhanced Colab Integration for SignalTrust AI

This file improves the Colab integration for AI assistants and developers.

## 📘 Google Colab — Full AI & Multi‑Agent Environment

Launch SignalTrust AI directly in Google Colab — no installation required.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/signaltrustai/SignalTrust-AI-Scanner/blob/main/SignalTrust_AI_Scanner.ipynb)

### ✨ What's Included

#### 🔧 Automatic Setup
- Repository cloning and dependency installation
- Environment configuration with secure key storage
- Python environment optimization

#### 🔐 Secure API Key Management
- Encrypted key storage using Fernet encryption
- Environment variable integration
- Key validation and health monitoring
- Support for multiple AI providers

#### 🌐 Public Access
- ngrok integration for public URL
- Automatic tunnel creation
- Persistent connection management

#### 🤖 Multi-Agent System
- Coordinator (CrewAI) - Port 8000
- Crypto Agent (FinGPT) - Port 8001
- Stock Agent (Stock-GPT) - Port 8002
- Whale Watcher - Port 8003
- News Agent - Port 8004
- Supervisor (Auto-GPT)

#### 🧪 API Testing
- Pre-configured test examples
- Real-time monitoring dashboard
- Health check endpoints

#### 📊 Real-Time Monitoring
- Application status tracking
- Active connection monitoring
- API key health dashboard

## 🚀 Quick Start Guide

### 1. Open in Colab
Click the badge above or visit: https://colab.research.google.com/github/signaltrustai/SignalTrust-AI-Scanner/blob/main/SignalTrust_AI_Scanner.ipynb

### 2. Prepare API Keys
Before starting, gather these API keys:

**Required:**
- OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))

**Optional:**
- Anthropic API Key ([Get it here](https://console.anthropic.com/))
- CoinGecko API Key ([Get it here](https://www.coingecko.com/en/api))
- Alpha Vantage Key ([Get it here](https://www.alphavantage.co/support/#api-key))
- ngrok Auth Token ([Get it here](https://dashboard.ngrok.com/get-started/your-authtoken))

### 3. Run the Notebook
Execute cells in order (Shift+Enter):
1. **Environment Setup** - Clones repo and installs dependencies
2. **Configure API Keys** - Securely stores your keys
3. **Setup ngrok** - Creates public URL
4. **Start Application** - Launches Flask server
5. **Test API** - Validates functionality
6. **Monitor** - Track application status

### 4. Access Your App
- Open the ngrok URL provided in Step 4
- Login with your credentials
- Start analyzing markets!

## 🔒 Security Features

### Encrypted Key Storage
- Keys encrypted using Fernet (AES 128-bit)
- PBKDF2 key derivation (100,000 iterations)
- Master password auto-generated per session

### Key Management
```python
from config.api_keys import KeyManager

# Store keys securely
manager = KeyManager()
manager.set_key('OPENAI_API_KEY', 'sk-...', save=True)

# Retrieve keys
api_key = manager.get_key('OPENAI_API_KEY')
```

### Key Validation
```python
from config.api_keys import KeyValidator

# Validate and test keys
validator = KeyValidator()
result = validator.validate_key('OPENAI_API_KEY', 'sk-...', test_connection=True)
```

## 🎯 Features

### Market Analysis
- Real-time crypto and stock scanning
- Technical indicators (RSI, MACD, Bollinger Bands)
- AI-powered predictions
- Whale transaction monitoring

### AI Integration
- Multiple AI providers (OpenAI, Anthropic, Local)
- Intelligent market analysis
- Automated trading signals
- Sentiment analysis

### Multi-Agent System
- Distributed agent architecture
- Specialized domain agents
- Coordinated analysis
- Automated task supervision

## 🛠️ Advanced Configuration

### Custom Environment Variables
Add to the configuration cell:
```python
# Custom settings
env_content += \"\"\"
# Your custom variables
CUSTOM_SETTING=value
ANOTHER_SETTING=value
\"\"\"
```

### Local Development
Clone and run locally:
```bash
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner
cp .env.example .env
# Edit .env with your keys
python3 start.py
```

### Docker Deployment
Run with multi-agent system:
```bash
./setup_agents.sh
docker-compose up
```

## 📊 API Examples

### Market Scan
```python
import requests

response = requests.post(f"{BASE_URL}/api/markets/scan", json={
    "symbols": ["BTC", "ETH", "AAPL"],
    "timeframe": "1d"
})
```

### AI Analysis
```python
response = requests.post(f"{BASE_URL}/api/ai/analyze", json={
    "symbol": "BTC",
    "type": "prediction"
})
```

## 🐛 Troubleshooting

### Flask Not Starting
- Check if port 5000 is available
- Verify API keys are valid
- Review error logs in Colab output

### ngrok Connection Failed
- Verify ngrok token is correct
- Check firewall settings
- Try restarting the ngrok cell

### API Keys Not Working
- Validate key format
- Test connection manually
- Check provider status pages

## 📚 Documentation

### Core Documentation
- [README.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/README.md) - Project overview
- [QUICKSTART.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/QUICKSTART.md) - Quick start
- [ARCHITECTURE.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/ARCHITECTURE.md) - System architecture

### Specialized Guides
- [MULTI_AGENT_SYSTEM.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/MULTI_AGENT_SYSTEM.md) - Multi-agent setup
- [OPENAI_SETUP_GUIDE.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/OPENAI_SETUP_GUIDE.md) - OpenAI configuration
- [CLOUD_STORAGE_GUIDE.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/CLOUD_STORAGE_GUIDE.md) - Cloud backup

### AI Assistant Integration
- [AI_COPILOT_GUIDE.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/AI_COPILOT_GUIDE.md) - Complete AI guide
- [COPILOT_COOPERATION.md](https://github.com/signaltrustai/SignalTrust-AI-Scanner/blob/main/COPILOT_COOPERATION.md) - Copilot collaboration

## 🔗 Useful Links

### API Providers
- [OpenAI Platform](https://platform.openai.com/) - GPT models
- [Anthropic Console](https://console.anthropic.com/) - Claude models
- [CoinGecko](https://www.coingecko.com/en/api) - Crypto data
- [Alpha Vantage](https://www.alphavantage.co/) - Stock data

### Tools
- [ngrok Dashboard](https://dashboard.ngrok.com/) - Tunnel management
- [Google Colab](https://colab.research.google.com/) - Cloud notebooks

### Community
- [GitHub Repository](https://github.com/signaltrustai/SignalTrust-AI-Scanner)
- [Issues](https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues)
- [Discussions](https://github.com/signaltrustai/SignalTrust-AI-Scanner/discussions)

## 💡 Tips & Tricks

### Optimizing Performance
1. Use gpt-4o-mini for cost-effective AI analysis
2. Enable caching for repeated API calls
3. Configure rate limits appropriately

### Keeping Session Alive
- Keep the Flask cell running
- Refresh browser regularly
- Note: Free Colab disconnects after ~12 hours

### Cost Management
- Monitor API usage in provider dashboards
- Set budget limits in .env configuration
- Use free tier APIs when possible

## ⚠️ Important Notes

1. **Session Persistence**: Colab sessions reset - data is not permanent
2. **API Costs**: Monitor your API usage to avoid unexpected charges
3. **Security**: Never commit real API keys to public repositories
4. **Rate Limits**: Respect API provider rate limits
5. **ngrok Limits**: Free tier has 2-hour session limit

## 🎉 Success Checklist

- [ ] Notebook opened in Colab
- [ ] Dependencies installed
- [ ] API keys configured
- [ ] Flask server running
- [ ] ngrok URL active
- [ ] API tests passed
- [ ] Application accessible

## 🤝 Contributing

Found a bug or have a feature request?
- Open an [issue](https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues)
- Submit a [pull request](https://github.com/signaltrustai/SignalTrust-AI-Scanner/pulls)
- Join the [discussion](https://github.com/signaltrustai/SignalTrust-AI-Scanner/discussions)

---

**Made with ❤️ by SignalTrust AI**

🚀 **Happy Trading in the Cloud!**  
