# SignalTrust AI Market Scanner

The **Ultimate AI-Powered Market Scanner** — a comprehensive platform combining real-time market scanning, technical analysis, multi-agent AI architecture, cloud backup, and multi-payment processing for intelligent trading and investment decisions.

**Stack**: Python 3.11 · Flask · Docker · Groq/Anthropic/Ollama · CrewAI Multi-Agents · PWA

---

## 🧠 AI Evolution System

SignalTrust intègre un **système d'IA évolutif** avec **10 agents IA spécialisés** qui :
- 🎓 **Apprennent quotidiennement** à partir de nouvelles données
- 🚀 **Évoluent continuellement** pour devenir plus puissants
- 🤝 **Partagent leurs connaissances** via une base commune
- 🎯 **Ont chacun un rôle spécifique** bien défini

### Les 10 Agents IA
1. **💹 MarketIntelligence** — Analyse des marchés et prédictions
2. **👤 UserExperience** — Personnalisation de l'expérience
3. **🛡️ RiskManager** — Gestion des risques
4. **📈 TradingOptimizer** — Optimisation des stratégies
5. **📝 ContentGenerator** — Génération de contenu
6. **🔐 SecurityGuard** — Détection de fraudes
7. **💬 SupportAssistant** — Support automatisé 24/7
8. **🔍 PatternRecognizer** — Reconnaissance de patterns
9. **😊 SentimentAnalyzer** — Analyse de sentiment
10. **💼 PortfolioManager** — Gestion de portefeuille

**Accéder au système :** `http://localhost:5000/ai-evolution`

📚 **Documentation complète** : [AI_EVOLUTION_GUIDE.md](AI_EVOLUTION_GUIDE.md)

## 🤖 Multi-Agent System (Docker)

A powerful **multi-agent architecture** with **10 specialized agents** working together for comprehensive market analysis:

### Core Agents
| Agent | Port | Description |
|-------|------|-------------|
| 🎯 **Coordinator** | 8000 | Orchestrates all agents using CrewAI framework |
| 💰 **Crypto Agent** | 8001 | FinGPT-based cryptocurrency market analysis |
| 📈 **Stock Agent** | 8002 | Stock-GPT-based stock market analysis |
| 🐋 **Whale Agent** | 8003 | Monitors large blockchain transactions |
| 📰 **News Agent** | 8004 | Aggregates and analyzes market news |

### Advanced Agents
| Agent | Port | Description |
|-------|------|-------------|
| 💬 **Social Sentiment** | 8005 | Real-time sentiment from Twitter, Reddit, Discord |
| ⛓️ **On-Chain Data** | 8006 | Blockchain metrics and whale activity |
| 🌍 **Macro Economics** | 8007 | GDP, inflation, Fed events analysis |
| 📊 **Portfolio Optimizer** | 8008 | Risk management and allocation optimization |
| 🔍 **Supervisor** | — | Auto-GPT-based task orchestration and monitoring |

```bash
./setup_agents.sh   # Setup and start all agents
./test_agents.sh    # Test all agents
```

**Dashboards :**
- Web Interface : `http://localhost:5000/agents`
- API Status : `http://localhost:5000/api/agents/status`

📚 **Documentation** :
- [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) — Complete system guide
- [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) — Architecture details
- [AGENT_INTEGRATION_GUIDE.md](AGENT_INTEGRATION_GUIDE.md) — Integration & API reference
- [agents/README.md](agents/README.md) — Individual agent documentation

## 🚀 Features

### AI & Intelligence Systems
- **Multi-AI Providers** : Groq (LLaMA 3 70B), Anthropic Claude, local models (Ollama)
- **AI Chat System** : Multi-mode AI chat interface (market analysis, code, general) — `/ai-chat`
- **AI Coder Bot** : AI-powered coding assistant with sessions — `/coder`
- **AI Orchestrator** : Central brain coordinating all AI agents 24/7
- **AI Memory System** : Persistent SQLite-based memory for all agents
- **AI Learning System** : Adaptive learning engine improving predictions over time
- **Multi-AI Coordinator** : Load balancing and caching across multiple AI workers
- **Meta Model** : Ensemble model combining multiple AI providers for consensus predictions
- **AI Optimizer** : Strategy and parameter optimization engine
- **AI Communication Hub** : Inter-agent messaging and knowledge sharing

### Market Analysis & Data
- **Real-time Market Scanning** : Stocks, crypto, forex, and indices simultaneously
- **Universal Market Analyzer** : Cross-market analysis spanning all asset classes
- **Crypto Gem Finder** : Discovery engine for high-potential low-cap cryptocurrencies
- **Whale Watcher v2.0** : Large transaction tracking via Etherscan, Blockchain.info, CoinPaprika
- **TradingView Integration** : Charting and technical analysis — `/tradingview`
- **SignalAI Strategy** : Custom trading strategy engine with performance tracking
- **Financial Data Provider** : Aggregates stock, crypto, and forex data from multiple sources
- **Live Price Provider** : Real-time price feeds with fallback mechanisms
- **Total Market Data Collector** : Complete market data aggregation across asset classes
- **Technical Analysis** : Advanced indicators, patterns, and signals
- **Sentiment Analysis** : AI-driven market sentiment evaluation

### Notification & Alert System
- **Notification Center** : Price alerts, whale movements, AI insights, market updates — `/notifications`
- **Notification AI** : AI-driven smart notifications with intelligent routing

### Payment & Subscriptions
- **Credit/Debit Card** : Secure processing with Luhn validation
- **PayPal** : Direct PayPal integration
- **Crypto (MetaMask)** : Ethereum, Polygon, BSC, Solana, Avalanche support
- **Bank Transfer** : Wire transfer payment handling
- **Coupon System** : Discount/coupon code management for promotions
- **Subscription Manager** : Flexible modular subscription system with usage enforcement
- **Limit Enforcer** : Usage quota management per subscription tier

### Cloud & Backup
- **Cloud Storage Manager** : AWS S3, Google Cloud, Azure, and local storage support
- **Auto Backup** : Automated backup scheduling and management
- **AI Cloud Backup** : Intelligent backup prioritization for AI data

### Admin Tools
- **Admin Dashboard** : System monitoring, agent control, backup management — `/admin/comm-hub`
- **Admin Payment Manager** : Transaction oversight and payment configuration — `/admin/payment-info`
- **API Key Manager** : Multi-API-key management with encryption and validation — `/api-manager`

### Viral Marketing AI Team
- **ContentCreatorAI** : Platform-specific content (Twitter, TikTok, Instagram, YouTube, Reddit)
- **SocialMediaManagerAI** : Scheduling, engagement, audience interaction
- **SEOOptimizerAI** : Hashtag selection, SEO optimization, competition analysis
- **AnalyticsAI** : Metrics tracking and campaign performance monitoring

### Platform
- **Progressive Web App (PWA)** : Installable on mobile with offline support
- **Responsive Design** : Modern UI for desktop and mobile
- **RESTful API** : 150+ API endpoints
- **Cross-Platform** : Windows, Linux, macOS
- **Production-Ready** : Gunicorn, Redis caching, Flask-Compress, Flask-Caching

## 📋 Requirements

### Standard Installation
- Python 3.11+ (see `runtime.txt`)
- pip (Python package manager)
- (Optional) Groq, Anthropic, or Ollama API key for AI features

### Multi-Agent System (Docker-based)
- Docker 20.10+ and Docker Compose v2.0+
- 4GB+ RAM recommended
- API keys for:
  - Groq (recommended for all agents)
  - CoinGecko (crypto data)
  - Alpha Vantage (stock data)
  - WhaleAlert (blockchain monitoring)
  - NewsCatcher (news aggregation)
  - Etherscan (on-chain data)

## 🔧 Installation

1. **Clone the repository** :
```bash
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner
```

2. **Install dependencies** :
```bash
pip install -r requirements.txt
```

3. **Configure environment** :
```bash
cp .env.example .env
nano .env
```

Add your AI provider key to `.env` :
```bash
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your-actual-api-key-here
GROQ_MODEL=llama3-70b-8192
```

📖 **Detailed Setup Guides** :
- [OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md) — AI provider configuration
- [GUIDE_VARIABLES_ENVIRONNEMENT.md](GUIDE_VARIABLES_ENVIRONNEMENT.md) — All environment variables
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) — Cloud deployment on Render

## 🎯 Quick Start

### Start the Web Application

**Linux/Mac :**
```bash
chmod +x start.sh
./start.sh
```

**Windows :**
```cmd
start.bat
```

**Cross-Platform (Python) :**
```bash
python3 start.py
```

The application will be available at : **http://localhost:5000**

### Default Administrator Account

- **Email :** signaltrustai@gmail.com
- **Password :** !Obiwan12!
- **User ID :** owner_admin_001
- **Access Level :** Enterprise (Full Access)

⚠️ **IMPORTANT** : Change this password immediately after first login in production. See [ADMIN_ACCESS.md](ADMIN_ACCESS.md).

The admin account has full access to :
- AI Chat System (all modes)
- Whale Watcher (unlimited access)
- Admin Communication Hub
- Admin Payment Manager
- All premium features and dashboards

### Deploy to Render (Production)

The project is pre-configured for Render deployment :
```bash
# render.yaml is already configured
# Procfile uses gunicorn with optimized settings
gunicorn app:app --bind 0.0.0.0:$PORT --workers 3 --worker-class gthread --threads 2
```

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) and [RENDER_CHECKLIST.md](RENDER_CHECKLIST.md) for details.

### Command Line Scanner (Legacy)

```bash
python3 scanner.py --help
python3 scanner.py -v myfile.txt
```

## 📚 Documentation

### Web Application Routes

#### Public Pages
| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/register` | User registration |
| `/login` | User login |
| `/pricing` | Subscription plans |
| `/payment` | Payment processing |

#### Protected Pages (Require Login)
| Route | Description |
|-------|-------------|
| `/dashboard` | User dashboard |
| `/scanner` | Market scanner interface |
| `/analyzer` | Technical analysis tools |
| `/predictions` | AI predictions |
| `/settings` | Account settings |
| `/profile` | User profile with avatar upload |
| `/ai-chat` | Multi-mode AI chat |
| `/coder` | AI coding assistant |
| `/ai-evolution` | AI Evolution System (10 agents) |
| `/agents` | Multi-agent system dashboard |
| `/api-manager` | API key management |
| `/ai-intelligence` | Market intelligence dashboard |
| `/whale-watcher` | Large transaction monitoring |
| `/tradingview` | TradingView charting |
| `/notifications` | Notification center |

#### Admin Pages
| Route | Description |
|-------|-------------|
| `/admin/comm-hub` | Agent coordination & communication hub |
| `/admin/payment-info` | Payment configuration dashboard |

### API Endpoints

#### Authentication
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login user
- `POST /api/auth/logout` — Logout user
- `GET /api/auth/verify` — Verify session

#### Market Data
- `GET /api/markets/overview` — Markets overview
- `POST /api/markets/scan` — Scan specific markets
- `GET /api/markets/trending` — Trending assets

#### Analysis
- `POST /api/analyze/technical` — Technical analysis
- `POST /api/analyze/sentiment` — Sentiment analysis
- `POST /api/analyze/patterns` — Pattern detection

#### Financial Data
- `POST /api/financial/stock` — Stock data
- `POST /api/financial/crypto` — Crypto data
- `POST /api/financial/fundamentals` — Fundamental analysis
- `POST /api/financial/prices` — Multi-asset prices
- `GET /api/financial/status` — Data provider status

#### AI Predictions
- `POST /api/predict/price` — Price predictions
- `POST /api/predict/signals` — Trading signals
- `POST /api/predict/risk` — Risk assessment

#### AI Chat & Coder
- `GET /api/ai-chat/modes` — Available chat modes
- `POST /api/ai-chat/message` — Send chat message
- `GET /api/ai-chat/history` — Chat history
- `GET /api/coder/status` — Coder bot status
- `POST /api/coder/chat` — Code generation

#### AI Evolution & Learning
- `GET /api/evolution/status` — Evolution system status
- `POST /api/evolution/learn` — Trigger learning
- `POST /api/evolution/evolve` — Trigger evolution
- `GET /api/ai/learning/summary` — Learning summary
- `GET /api/ai/learning/model-accuracy` — Model accuracy metrics

#### AI Coordinator & Optimizer
- `GET /api/ai/coordinator/status` — Coordinator status
- `POST /api/ai/coordinator/analyze` — AI-coordinated analysis
- `POST /api/ai/coordinator/deep` — Deep analysis
- `GET /api/optimizer/status` — Optimizer status
- `POST /api/optimizer/optimize` — Run optimization

#### Multi-Agent System
- `GET /api/agents/status` — All agents status
- `POST /api/agents/workflow` — Run agent workflow
- `POST /api/agents/crypto/analyze` — Crypto agent analysis
- `POST /api/agents/stock/analyze` — Stock agent analysis
- `GET /api/agents/whale/watch` — Whale monitoring
- `POST /api/agents/sentiment/analyze` — Sentiment analysis
- `POST /api/agents/onchain/analyze` — On-chain analysis
- `POST /api/agents/macro/indicators` — Macro indicators
- `POST /api/agents/portfolio/optimize` — Portfolio optimization
- `POST /api/agents/complete-analysis` — Full multi-agent analysis

#### Whale & Gems
- `GET /api/whale/transactions` — Whale transactions
- `GET /api/whale/alerts` — Whale alerts
- `GET /api/gems/discover` — Discover crypto gems
- `GET /api/gems/top` — Top gems
- `GET /api/gems/analyze/<symbol>` — Analyze specific gem

#### Universal & Total Market
- `GET /api/universal/analyze-all` — Cross-market analysis
- `GET /api/universal/summary` — Market summary
- `GET /api/universal/top-opportunities` — Top opportunities
- `GET /api/total/collect-all` — Complete market data
- `GET /api/total/coverage` — Data coverage

#### SignalAI Strategy
- `POST /api/signalai/generate` — Generate strategy signals
- `GET /api/signalai/strategies` — List strategies
- `POST /api/signalai/performance` — Strategy performance

#### TradingView
- `GET /api/tradingview/symbols` — Available symbols
- `POST /api/tradingview/search` — Symbol search

#### Cloud & Backup
- `GET /api/cloud/status` — Cloud storage status
- `POST /api/cloud/backup` — Trigger backup
- `POST /api/cloud/sync` — Sync data
- `GET /api/cloud/backups` — List backups

#### Notifications
- `GET /api/notifications` — Get notifications
- `POST /api/notifications/mark-read` — Mark as read
- `POST /api/notifications-ai/send` — AI smart notification
- `POST /api/notifications-ai/configure` — Configure AI notifications

#### Communication Hub
- `GET /api/hub/status` — Hub status
- `GET /api/hub/knowledge` — Shared knowledge base
- `GET /api/hub/collective-intelligence` — Collective intelligence data

#### Payment
- `GET /api/payment/plans` — Subscription plans
- `POST /api/payment/process` — Process payment
- `POST /api/payment/validate-card` — Validate card

#### Profile
- `GET /api/profile` — Get user profile
- `POST /api/profile` — Update profile
- `POST /api/profile/avatar` — Upload avatar

## 💳 Subscription Plans

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/month | Basic scanning, 10 scans/day, basic indicators, community support |
| **Basic** | $29.99/month | Unlimited scanning, advanced analysis, real-time alerts, 50 AI predictions/month |
| **Professional** ⭐ | $79.99/month | Everything in Basic + unlimited AI predictions, pattern recognition, portfolio management, API access |
| **Enterprise** | $299.99/month | Everything in Pro + custom AI models, dedicated support, white-label, 10 user accounts |

## 🏗️ Project Structure

```
SignalTrust-AI-Scanner/
├── app.py                        # Main Flask application (150+ routes)
├── market_scanner.py             # Market scanning module
├── market_analyzer.py            # Technical analysis module
├── ai_predictor.py               # AI prediction module
├── ai_provider.py                # Multi-provider AI abstraction (Groq/Anthropic/Ollama)
├── ai_chat_system.py             # Multi-mode AI chat interface
├── ai_coder_bot.py               # AI coding assistant
├── ai_orchestrator.py            # Central AI brain / coordinator
├── ai_memory_system.py           # Persistent AI memory (SQLite)
├── ai_learning_system.py         # Adaptive learning engine
├── ai_evolution_system.py        # AI evolution with 10 agents
├── ai_evolution_engine.py        # Evolution engine with checkpoints
├── ai_optimizer.py               # Strategy optimization
├── ai_market_intelligence.py     # Market intelligence agent
├── ai_communication_hub.py       # Inter-agent messaging
├── ai_cloud_backup.py            # Intelligent backup prioritization
├── ai_system_manager.py          # AI lifecycle management
├── ai_worker_service.py          # Background worker pool
├── multi_ai_coordinator.py       # Multi-AI load balancing & caching
├── meta_model.py                 # Ensemble AI model
├── notification_ai.py            # AI-driven notifications
├── notification_center.py        # Notification management
├── user_auth.py                  # User authentication
├── payment_processor.py          # Credit card payment processing
├── paypal_processor.py           # PayPal integration
├── crypto_payment_processor.py   # MetaMask/crypto payments
├── bank_transfer_processor.py    # Bank transfer handling
├── subscription_manager.py       # Subscription management
├── limit_enforcer.py             # Usage quota enforcement
├── coupon_manager.py             # Discount/coupon codes
├── admin_dashboard.py            # Admin interface
├── admin_payment_manager.py      # Admin payment management
├── whale_watcher.py              # Whale transaction tracker
├── crypto_gem_finder.py          # Low-cap gem discovery
├── universal_market_analyzer.py  # Cross-market analysis
├── total_market_data_collector.py # Complete market aggregation
├── financial_data_provider.py    # Multi-source financial data
├── live_price_provider.py        # Real-time price feeds
├── realtime_market_data.py       # Live market data streaming
├── tradingview_manager.py        # TradingView integration
├── signalai_strategy.py          # Trading strategy engine
├── cloud_storage_manager.py      # Cloud storage (S3/GCP/Azure/local)
├── auto_backup.py                # Automated backup scheduling
├── agent_client.py               # Agent communication client
├── api_processor.py              # Request batching & caching
├── viral_marketing_ai_team.py    # AI marketing team (4 agents)
├── scanner.py                    # CLI scanner (legacy)
├── config.json                   # Configuration
├── requirements.txt              # Dependencies
├── render.yaml                   # Render deployment config
├── Procfile                      # Production server config
├── Makefile                      # Docker management commands
├── docker-compose.yml            # Multi-agent Docker setup
├── templates/                    # HTML templates (29 pages)
│   ├── index.html                # Homepage
│   ├── register.html / login.html
│   ├── dashboard.html / profile.html / settings.html
│   ├── scanner.html / analyzer.html / predictions.html
│   ├── pricing.html / payment.html
│   ├── payment_methods_selector.html
│   ├── crypto_payment.html / paypal_card_payment.html / bank_transfer.html
│   ├── ai_chat.html / ai_coder.html / ai_intelligence.html
│   ├── ai_evolution.html / agents.html / api_manager.html
│   ├── whale_watcher.html / tradingview.html / notifications.html
│   ├── subscription_builder.html
│   ├── admin_dashboard.html / admin_comm_hub.html / admin_payment_info.html
│   └── partials/nav.html
├── static/                       # Static files
│   ├── css/style.css
│   ├── js/ (main.js, register.js, login.js, pricing.js, payment.js)
│   ├── icons/ (PWA icons, favicon)
│   ├── images/ (hero image, branding)
│   ├── manifest.json             # PWA manifest
│   └── service-worker.js         # PWA offline support
├── agents/                       # Multi-agent Docker services
│   ├── coordinator/              # CrewAI orchestrator
│   ├── crypto_agent/             # FinGPT crypto analysis
│   ├── stock_agent/              # Stock-GPT analysis
│   ├── whale_agent/              # Blockchain monitoring
│   ├── news_agent/               # News aggregation
│   ├── social_sentiment_agent/   # Social sentiment
│   ├── onchain_agent/            # On-chain metrics
│   ├── macro_economics_agent/    # Macro economics
│   ├── portfolio_optimizer_agent/ # Portfolio optimization
│   └── supervisor/               # Auto-GPT supervisor
├── config/                       # Configuration
│   ├── admin_config.py           # Admin settings
│   └── api_keys/                 # Encrypted API key storage
├── data/                         # Data storage (auto-created)
│   ├── users/ / users.json       # User data
│   ├── transactions/             # Payment transactions
│   ├── backups/ / unified_backups/
│   ├── ai_memory.db              # AI persistent memory
│   ├── ai_learning_data.json     # Learning data
│   └── ai_hub/ / ai_orchestrator/ / notification_ai/
├── start.sh / start.bat / start.py  # Startup scripts
└── build.sh / start-render.sh       # Build & deploy scripts
```

## 🔐 Security Features

- Password hashing with PBKDF2-HMAC-SHA256 (100,000 iterations)
- Unique salt generation for each user
- Secure session management
- HTTPS support
- Card validation (Luhn algorithm)
- XSS and CSRF protection
- Encrypted data storage
- API key encryption with `cryptography` library
- API key validation with pattern matching

### Admin Account Security

**For production deployments :**

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

Key environment variables (see `.env.example` for full list) :

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 5000 |
| `DEBUG` | Debug mode | False |
| `SECRET_KEY` | Flask secret key | auto-generated |
| `AI_PROVIDER` | AI engine (`groq`, `anthropic`, `local`) | groq |
| `GROQ_API_KEY` | Groq API key | — |
| `GROQ_MODEL` | Groq model | llama3-70b-8192 |
| `ANTHROPIC_API_KEY` | Anthropic API key | — |
| `COINGECKO_API_KEY` | CoinGecko API key | — |
| `ALPHAVANTAGE_API_KEY` | Alpha Vantage API key | — |
| `WHALEALERT_API_KEY` | WhaleAlert API key | — |
| `ETHERSCAN_API_KEY` | Etherscan API key | — |
| `CLOUD_PROVIDER` | Cloud storage (`local`, `aws`, `gcp`, `azure`) | local |

### AI Configuration

Configure your preferred AI provider in the `.env` file :

**Groq (Recommended — fast & powerful) :**
```bash
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your-key-here
GROQ_MODEL=llama3-70b-8192
USE_AI_PREDICTIONS=true
```

**Anthropic (Claude) :**
```bash
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
USE_AI_PREDICTIONS=true
```

**Local Models (Free) :**
```bash
# First install Ollama: https://ollama.ai
# Then run: ollama serve && ollama pull llama2

AI_PROVIDER=local
LOCAL_MODEL=llama2
LOCAL_API_URL=http://localhost:11434
USE_AI_PREDICTIONS=true
```

For detailed AI setup instructions, see **[AI_ENHANCEMENT_GUIDE.md](AI_ENHANCEMENT_GUIDE.md)**

### Docker (Multi-Agent System)

```bash
make up       # Start all Docker services
make down     # Stop Docker services
make logs     # View logs
```

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

### AI Chat

```bash
curl -X POST http://localhost:5000/api/ai-chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze BTC market trends",
    "mode": "market_analysis"
  }'
```

### Discover Crypto Gems

```bash
curl -X GET http://localhost:5000/api/gems/discover
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 🤖 AI Assistant Collaboration

Working with GitHub Copilot or other AI assistants? We've created comprehensive guides :

- **[AI_COPILOT_GUIDE.md](AI_COPILOT_GUIDE.md)** — Complete bilingual guide (French/English) for AI assistants
- **[.copilot-instructions.md](.copilot-instructions.md)** — Quick reference for project context
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** — GitHub Copilot-specific instructions

## 📚 Full Documentation Index

| Document | Description |
|----------|-------------|
| [AI_ENHANCEMENT_GUIDE.md](AI_ENHANCEMENT_GUIDE.md) | AI integration and setup guide |
| [AI_EVOLUTION_GUIDE.md](AI_EVOLUTION_GUIDE.md) | AI Evolution System guide |
| [AI_SYSTEM_24_7_GUIDE.md](AI_SYSTEM_24_7_GUIDE.md) | 24/7 AI system operation |
| [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) | Multi-agent system guide |
| [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) | Agent architecture details |
| [AGENT_INTEGRATION_GUIDE.md](AGENT_INTEGRATION_GUIDE.md) | Agent API reference |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [COMPREHENSIVE_ARCHITECTURE.md](COMPREHENSIVE_ARCHITECTURE.md) | Detailed architecture |
| [ADMIN_ACCESS.md](ADMIN_ACCESS.md) | Admin account and security |
| [CLOUD_STORAGE_GUIDE.md](CLOUD_STORAGE_GUIDE.md) | Cloud storage setup |
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Render deployment guide |
| [RENDER_CHECKLIST.md](RENDER_CHECKLIST.md) | Deployment checklist |
| [SUBSCRIPTION_LIMITS.md](SUBSCRIPTION_LIMITS.md) | Plan limits and features |
| [API_KEY_SYSTEM_COMPLETE.md](API_KEY_SYSTEM_COMPLETE.md) | API key management |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | Release notes |
| [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md) | Launch preparation |
| [BRAND_GUIDELINES.md](BRAND_GUIDELINES.md) | Brand and design guidelines |
| [INVESTOR_PITCH.md](INVESTOR_PITCH.md) | Investor presentation |
| [MARKETING_KIT.md](MARKETING_KIT.md) | Marketing resources |

## 📝 License

Copyright © 2026 SignalTrust AI. All rights reserved.

## 📧 Support

For support, email support@signaltrust.ai or visit our support portal.

## 🔗 Links

- **Website** : https://signaltrust.ai
- **GitHub** : https://github.com/signaltrustai/SignalTrust-AI-Scanner
- **Documentation** : https://docs.signaltrust.ai

## 📈 Version History

### v3.1.0 (2026-02-13) — Current
- 🔑 **API Key System** : Secure multi-API key management with encryption and validation
- 🌐 **Groq Integration** : Migrated from OpenAI to Groq (LLaMA 3 70B) as primary AI provider
- 🚀 **Launch Preparation** : Complete launch documentation, checklists, and marketing kit
- 📋 **Agent Architecture** : Detailed architecture documentation for all 10 agents
- 🎯 **Launch Readiness** : Full system verification and test coverage
- 📢 **Marketing & Growth** : Community growth plan, social media plan, brand guidelines, investor pitch
- 🔧 **Agent API Keys** : Individual API key configuration for all agents

### v3.0.0 (2026-02-07)
- 🤖 **Enhanced AI System** : Real AI models instead of simulations
- 🔌 **Multiple AI Providers** : Groq, Anthropic Claude, local models (Ollama)
- 💬 **AI Chat System** : Multi-mode AI chat interface
- 🖥️ **AI Coder Bot** : AI-powered coding assistant
- 🐋 **Whale Watcher v2.0** : Large transaction tracking
- 💎 **Crypto Gem Finder** : Low-cap cryptocurrency discovery
- ☁️ **Cloud Storage** : AWS S3, GCP, Azure, local backup support
- 🔔 **AI Notifications** : Intelligent notification system
- 📊 **TradingView Integration** : Charting and analysis
- 💰 **Multi-Payment** : Card, PayPal, Crypto (MetaMask), Bank Transfer
- 🧠 **AI Evolution** : 10 specialized AI agents with adaptive learning
- 🎯 **Multi-Agent System** : 10 Docker-based agents for comprehensive analysis
- 📱 **PWA Support** : Progressive Web App with offline capabilities
- 🏗️ **Render Deployment** : Production-ready cloud deployment
- 🧠 **AI Memory** : Persistent SQLite-based memory for all agents
- 📈 **SignalAI Strategy** : Custom trading strategy engine
- 🌍 **Universal Analyzer** : Cross-market analysis across all asset classes
- 🔄 **Auto-fallback** : Graceful degradation if AI not configured
- 🌍 **Multilingual** : Documentation in English and French

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

