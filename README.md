# SignalTrust AI Market Scanner

The **Ultimate AI-Powered Market Scanner** for intelligent trading and investment decisions. A comprehensive web-based platform that combines real-time market scanning, technical analysis, AI predictions, and secure payment processing.

## 🧠 NEW: AI Evolution System ✨✨✨

SignalTrust intègre maintenant un **système d'IA évolutif** avec **10 agents IA spécialisés** qui:
- 🎓 **Apprennent quotidiennement** à partir de nouvelles données
- 🚀 **Évoluent continuellement** pour devenir plus puissants
- 🤝 **Partagent leurs connaissances** via une base commune
- 🎯 **Ont chacun un rôle spécifique** bien défini

### Les 10 Agents IA
1. **💹 MarketIntelligence** - Analyse des marchés et prédictions
2. **👤 UserExperience** - Personnalisation de l'expérience
3. **🛡️ RiskManager** - Gestion des risques
4. **📈 TradingOptimizer** - Optimisation des stratégies
5. **📝 ContentGenerator** - Génération de contenu
6. **🔐 SecurityGuard** - Détection de fraudes
7. **💬 SupportAssistant** - Support automatisé 24/7
8. **🔍 PatternRecognizer** - Reconnaissance de patterns
9. **😊 SentimentAnalyzer** - Analyse de sentiment
10. **💼 PortfolioManager** - Gestion de portefeuille

**Accéder au système:**
```
http://localhost:5000/ai-evolution
```

📚 **Documentation complète**: [AI_EVOLUTION_GUIDE.md](AI_EVOLUTION_GUIDE.md)

## 🤖 NEW: Multi-Agent System EU ✨

SignalTrust now includes a powerful **multi-agent architecture** with **9 specialized agents** working together for comprehensive market analysis:

### Core Agents
- **🎯 Coordinator** (Port 8000): Orchestrates all agents using CrewAI framework
- **💰 Crypto Agent** (Port 8001): FinGPT-based cryptocurrency market analysis
- **📈 Stock Agent** (Port 8002): Stock-GPT-based stock market analysis  
- **🐋 Whale Agent** (Port 8003): Monitors large blockchain transactions
- **📰 News Agent** (Port 8004): Aggregates and analyzes market news

### Advanced Agents ✨ NEW
- **💬 Social Sentiment** (Port 8005): Real-time sentiment from Twitter, Reddit, Discord
- **⛓️ On-Chain Data** (Port 8006): Blockchain metrics and whale activity
- **🌍 Macro Economics** (Port 8007): GDP, inflation, Fed events analysis
- **📊 Portfolio Optimizer** (Port 8008): Risk management and allocation optimization
- **🔍 Supervisor**: Auto-GPT-based task orchestration and monitoring

**Quick Start with Multi-Agent System:**
```bash
./setup_agents.sh   # Setup and start all agents
./test_agents.sh    # Test all agents
```

**Access Agent Dashboard:**
- Web Interface: `http://localhost:5000/agents`
- API Status: `http://localhost:5000/api/agents/status`

📚 **Full Documentation**: 
- [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) - Complete system guide
- [AGENT_INTEGRATION_GUIDE.md](AGENT_INTEGRATION_GUIDE.md) - Integration & API reference
- [agents/README.md](agents/README.md) - Individual agent documentation

## 🚀 Features

### Advanced AI Capabilities ✨ NEW
- **OpenAI Integration**: GPT-4 powered market analysis and predictions
- **Multiple AI Providers**: Support for OpenAI GPT-4, Anthropic Claude, and local models (Ollama)
- **Real AI Analysis**: Genuine AI-powered market analysis instead of simulations
- **Intelligent Predictions**: Deep learning-based price forecasting
- **Adaptive Learning**: AI that improves over time with market data
- **Flexible Configuration**: Easy switch between AI providers

### Market Analysis
- **Real-time Market Scanning**: Scan stocks, crypto, forex, and indices simultaneously
- **AI-Powered Predictions**: Machine learning algorithms for price forecasting
- **Technical Analysis**: Advanced indicators, patterns, and signals
- **Sentiment Analysis**: AI-driven market sentiment evaluation
- **Risk Assessment**: Comprehensive risk analysis and scoring

### User Features
- **User Authentication**: Secure registration and login system
- **Multiple Subscription Plans**: Free, Basic, Pro, and Enterprise tiers
- **Secure Payment Processing**: Credit card, PayPal, and cryptocurrency support
- **Personalized Dashboard**: Track your investments and watchlists
- **Real-time Alerts**: Get notified of important market movements

### Platform Capabilities
- **Web-Based Interface**: Modern, responsive design
- **RESTful API**: Full API access for Pro and Enterprise users
- **Multiple Payment Methods**: Flexible payment options
- **Cross-Platform**: Works on Windows, Linux, and macOS

## 📋 Requirements

### Standard Installation
- Python 3.7 or higher
- pip (Python package manager)
- (Optional) OpenAI or Anthropic API key for enhanced AI features
- (Optional) Ollama for free local AI models

### Multi-Agent System (Docker-based)
- Docker 20.10+ and Docker Compose v2.0+
- 4GB+ RAM recommended
- API keys for:
  - OpenAI (required for all agents)
  - CoinGecko (for crypto data)
  - Alpha Vantage (for stock data)
  - WhaleAlert (for blockchain monitoring)
  - NewsCatcher (for news aggregation)

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure AI Provider (Optional but Recommended)**:

   **🔥 NEW: OpenAI Integration**
   
   SignalTrust AI Scanner now uses OpenAI (GPT-4) for powerful AI analysis!
   
   ```bash
   # Copy the environment template
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   nano .env
   ```
   
   Add to your `.env` file:
   ```bash
   OPENAI_API_KEY=sk-proj-your-actual-api-key-here
   OPENAI_MODEL=gpt-4
   ```
   
   📖 **Detailed Setup Guide**: See [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md) for:
   - How to get your OpenAI API key
   - Available models and pricing
   - Security best practices
   - Usage examples
   - Troubleshooting
   
   💡 **Quick Example**:
   ```bash
   # Run the example script to test your OpenAI setup
   python example_openai_usage.py
   ```

## 🎯 Quick Start

### Start the Web Application

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Cross-Platform (Python):**
```bash
python3 start.py
```

The application will be available at: **http://localhost:5000**

### Default Administrator Account

The application includes a pre-configured administrator account for initial setup:

- **Email:** signaltrustai@gmail.com
- **Password:** !Obiwan12!
- **User ID:** owner_admin_001
- **Access Level:** Enterprise (Full Access)

⚠️ **IMPORTANT SECURITY NOTICE**: This default password is for development and initial setup only. **You MUST change this password immediately after first login in any production environment.** See [ADMIN_ACCESS.md](ADMIN_ACCESS.md) for detailed information.

The admin account has full access to:
- AI Chat System (all modes)
- Whale Watcher (unlimited access)
- All premium features and dashboards

### Command Line Scanner (Legacy)

You can still use the CLI scanner:
```bash
python3 scanner.py --help
python3 scanner.py -v myfile.txt
```

## 📚 Documentation

### Web Application Routes

#### Public Pages
- `/` - Homepage
- `/register` - User registration
- `/login` - User login
- `/pricing` - Subscription plans
- `/payment` - Payment processing

#### Protected Pages (Require Login)
- `/dashboard` - User dashboard
- `/scanner` - Market scanner interface
- `/analyzer` - Technical analysis tools
- `/predictions` - AI predictions
- `/settings` - Account settings

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/verify` - Verify session

#### Market Data
- `GET /api/markets/overview` - Get markets overview
- `POST /api/markets/scan` - Scan specific markets
- `GET /api/markets/trending` - Get trending assets

#### Analysis
- `POST /api/analyze/technical` - Technical analysis
- `POST /api/analyze/sentiment` - Sentiment analysis
- `POST /api/analyze/patterns` - Pattern detection

#### AI Predictions
- `POST /api/predict/price` - Price predictions
- `POST /api/predict/signals` - Trading signals
- `POST /api/predict/risk` - Risk assessment

#### Payment
- `GET /api/payment/plans` - Get subscription plans
- `POST /api/payment/process` - Process payment
- `POST /api/payment/validate-card` - Validate card
- `GET /api/payment/transactions` - Get transactions
- `POST /api/payment/cancel` - Cancel subscription

## 💳 Subscription Plans

### Free Plan - $0/month
- Basic market scanning
- Limited to 10 scans per day
- Basic technical indicators
- Community support

### Basic Plan - $29.99/month
- Unlimited market scanning
- Advanced technical analysis
- Real-time alerts
- 50 AI predictions/month
- Email support

### Professional Plan - $79.99/month ⭐ Most Popular
- Everything in Basic
- Unlimited AI predictions
- Pattern recognition
- Portfolio management
- API access
- Priority support

### Enterprise Plan - $299.99/month
- Everything in Pro
- Custom AI models
- Dedicated support
- White-label options
- 10 user accounts
- Custom integrations

## 🏗️ Project Structure

```
SignalTrust-AI-Scanner/
├── app.py                  # Main Flask application
├── market_scanner.py       # Market scanning module
├── market_analyzer.py      # Technical analysis module
├── ai_predictor.py         # AI prediction module
├── user_auth.py            # User authentication
├── payment_processor.py    # Payment processing
├── scanner.py              # CLI scanner (legacy)
├── config.json             # Configuration
├── requirements.txt        # Dependencies
├── templates/              # HTML templates
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── pricing.html
│   ├── payment.html
│   ├── dashboard.html
│   ├── scanner.html
│   ├── analyzer.html
│   ├── predictions.html
│   └── settings.html
├── static/                 # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── register.js
│       ├── login.js
│       ├── pricing.js
│       └── payment.js
├── data/                   # User and transaction data (created automatically)
├── start.sh                # Linux/Mac startup script
├── start.bat               # Windows startup script
└── start.py                # Python startup script
```

## 🔐 Security Features

- Password hashing with PBKDF2-HMAC-SHA256 (100,000 iterations)
- Unique salt generation for each user
- Secure session management
- HTTPS support
- Card validation (Luhn algorithm)
- XSS and CSRF protection
- Encrypted data storage

### Admin Account Security

The application includes a default administrator account for initial setup. **For production deployments:**

1. Change the default admin password immediately after first login
2. Review and update `config/admin_config.py` to load credentials from environment variables
3. Consider removing the default password from version control
4. See [ADMIN_ACCESS.md](ADMIN_ACCESS.md) for detailed security guidelines

## 🛠️ Development

### Running in Development Mode

```bash
export DEBUG=True
python3 app.py
```

### Environment Variables

- `PORT` - Server port (default: 5000)
- `DEBUG` - Debug mode (default: False)

### AI Configuration

Configure your preferred AI provider in the `.env` file:

**OpenAI (GPT-4):**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
USE_AI_PREDICTIONS=true
```

**Anthropic (Claude):**
```bash
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
USE_AI_PREDICTIONS=true
```

**Local Models (Free):**
```bash
# First install Ollama: https://ollama.ai
# Then run: ollama serve && ollama pull llama2

AI_PROVIDER=local
LOCAL_MODEL=llama2
LOCAL_API_URL=http://localhost:11434
USE_AI_PREDICTIONS=true
```

For detailed AI setup instructions, see **[AI_ENHANCEMENT_GUIDE.md](AI_ENHANCEMENT_GUIDE.md)**

## 📊 API Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "full_name": "John Doe",
    "plan": "pro"
  }'
```

### Scan Markets

```bash
curl -X POST http://localhost:5000/api/markets/scan \
  -H "Content-Type: application/json" \
  -d '{
    "market_type": "stocks",
    "symbols": ["AAPL", "GOOGL", "MSFT"]
  }'
```

### Get AI Price Prediction

```bash
curl -X POST http://localhost:5000/api/predict/price \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "days": 7
  }'
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 🤖 AI Assistant Collaboration

Working with GitHub Copilot or other AI assistants? We've created comprehensive guides to help AI understand and contribute to this project:

- **[AI_COPILOT_GUIDE.md](AI_COPILOT_GUIDE.md)** - Complete bilingual guide (French/English) for AI assistants
- **[.copilot-instructions.md](.copilot-instructions.md)** - Quick reference for project context
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - GitHub Copilot-specific instructions

These files provide context about:
- Project architecture and structure
- Code conventions and patterns
- Common development tasks
- API endpoints and data models
- Security best practices
- Quick commands and troubleshooting

## 📝 License

Copyright © 2026 SignalTrust AI. All rights reserved.

## 📧 Support

For support, email support@signaltrust.ai or visit our support portal.

## 🔗 Links

- **Website**: https://signaltrust.ai
- **GitHub**: https://github.com/signaltrustai/SignalTrust-AI-Scanner
- **Documentation**: https://docs.signaltrust.ai

## 📈 Version History

### v3.0.0 (2026-02-07) ✨ NEW
- 🤖 **Enhanced AI System**: Real AI models instead of simulations
- 🔌 **Multiple AI Providers**: OpenAI GPT-4, Anthropic Claude, local models (Ollama)
- 🧠 **Intelligent Analysis**: Genuine AI-powered market analysis
- 🎯 **Better Predictions**: Deep learning-based price forecasting
- 📚 **Comprehensive Guide**: Complete AI setup and configuration guide
- 🔄 **Auto-fallback**: Graceful degradation if AI not configured
- 🌍 **Multilingual**: Documentation in English and French
- ⚙️ **Flexible Config**: Easy AI provider switching via .env

### v2.0.0 (2026-02-02)
- 🌐 Complete web application with modern UI
- 👤 User registration and authentication system
- 💳 Payment processing with multiple payment methods
- 📊 Market scanner for stocks, crypto, forex
- 🤖 AI-powered predictions and analysis
- 📱 Responsive design for mobile and desktop
- 🔐 Secure payment and data handling
- 📡 RESTful API for all features

### v1.0.0 (2026-02-02)
- Initial CLI-based scanner
- Basic file and text scanning
- Security pattern detection

---

**Made with ❤️ by SignalTrust AI**

