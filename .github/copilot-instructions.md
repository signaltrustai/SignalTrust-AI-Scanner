# GitHub Copilot Instructions

> This file helps GitHub Copilot understand the SignalTrust AI Scanner project context

## Project Context
This is **SignalTrust AI Market Scanner** - an AI-powered financial market analysis platform combining real-time scanning, technical analysis, and multi-agent AI architecture.

**Stack**: Python 3.7+, Flask, Docker, OpenAI GPT-4, CrewAI multi-agents

## Code Conventions

### Python Style
- Follow PEP 8 strictly
- Use type hints for function parameters and returns
- Write docstrings with Args and Returns sections
- Prefer `snake_case` for functions/variables, `PascalCase` for classes

### Security First
- Hash passwords with PBKDF2-HMAC-SHA256 (100k iterations)
- Validate all user inputs (especially financial data)
- Never log sensitive data (passwords, API keys, card numbers)
- Use environment variables for secrets (`.env` file)

### Error Handling
```python
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Context: {str(e)}")
    return {"success": False, "error": str(e)}
```

## Project Architecture

### Core Modules
- `app.py` - Main Flask application with routes and API endpoints
- `market_scanner.py` - Real-time market scanning logic
- `market_analyzer.py` - Technical analysis and indicators
- `ai_predictor.py` - AI-based predictions using ML
- `ai_provider.py` - AI provider management (OpenAI/Anthropic/Local)
- `user_auth.py` - User authentication and session management
- `payment_processor.py` - Subscription and payment handling

### Multi-Agent System (Docker)
Located in `/agents/` directory:
- `coordinator/` - CrewAI orchestrator (Port 8000)
- `crypto_agent/` - FinGPT crypto analysis (Port 8001)
- `stock_agent/` - Stock-GPT stock analysis (Port 8002)
- `whale_agent/` - Blockchain whale monitoring (Port 8003)
- `news_agent/` - Market news aggregation (Port 8004)
- `supervisor/` - Auto-GPT task supervision

## API Patterns

### Flask REST Endpoints
```python
@app.route('/api/resource', methods=['POST'])
def handle_resource():
    """Handle resource creation/update."""
    data = request.get_json()
    
    # Validate input
    if not data or 'required_field' not in data:
        return jsonify({"success": False, "error": "Missing required field"}), 400
    
    # Process
    result = process_data(data)
    
    return jsonify({"success": True, "data": result})
```

### Multi-Agent Communication
```python
import requests

def call_crypto_agent(symbol: str, timeframe: str = "1d") -> dict:
    """Call the crypto analysis agent."""
    try:
        response = requests.post(
            'http://localhost:8001/predict',
            json={"symbol": symbol, "timeframe": timeframe},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Crypto agent error: {str(e)}")
        return {"success": False, "error": str(e)}
```

## Data Models

### User Object
```python
{
    "user_id": str,       # Unique identifier
    "email": str,         # Email address (unique)
    "password_hash": str, # PBKDF2-HMAC-SHA256 hash
    "salt": str,          # Random salt for password
    "full_name": str,     # User's full name
    "plan": str,          # free, basic, pro, enterprise
    "created_at": str,    # ISO format timestamp
    "last_login": str     # ISO format timestamp
}
```

### Market Analysis Response
```python
{
    "success": bool,
    "symbol": str,        # e.g., "AAPL", "BTC"
    "price": float,
    "change_24h": float,  # Percentage
    "indicators": {
        "rsi": float,     # 0-100
        "macd": float,
        "sma_50": float,
        "sma_200": float
    },
    "prediction": {
        "direction": str, # "up", "down", "neutral"
        "confidence": float, # 0-1
        "target_price": float
    }
}
```

## Important Patterns

### AI Provider Usage
```python
from ai_provider import AIProvider

# Initialize with config
ai = AIProvider()

# Generate analysis
analysis = ai.analyze_market(
    symbol="AAPL",
    market_data=market_data,
    user_context="Looking for long-term investment"
)

# Always handle fallback
if not analysis.get('success'):
    # Use traditional analysis as fallback
    analysis = traditional_analysis(symbol, market_data)
```

### Authentication Check
```python
from functools import wraps

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@require_auth
def protected_route():
    user_id = session['user_id']
    # Your code here
```

### Payment Validation
```python
from payment_processor import PaymentProcessor

processor = PaymentProcessor()

# Validate card
is_valid = processor.validate_card_number(card_number)

# Process payment
result = processor.process_payment(
    user_id=user_id,
    amount=79.99,
    plan="pro",
    payment_method="card",
    card_info={
        "number": card_number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvv": cvv
    }
)
```

## Testing Patterns

### Unit Tests
```python
def test_market_scanner():
    """Test market scanner functionality."""
    scanner = MarketScanner()
    results = scanner.scan_markets(["AAPL", "GOOGL"])
    
    assert results is not None
    assert len(results) == 2
    assert "AAPL" in results
```

### API Tests
```python
def test_api_endpoint():
    """Test API endpoint."""
    response = client.post('/api/markets/scan', 
        json={"symbols": ["AAPL"]})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
```

## Common Tasks

### Adding a New API Endpoint
1. Define route in `app.py`
2. Add authentication decorator if needed
3. Validate input data
4. Process request using appropriate module
5. Return JSON response with success/error
6. Add tests in `test_*.py`

### Adding AI Analysis Feature
1. Add method to `ai_provider.py`
2. Create fallback for when AI unavailable
3. Add rate limiting per user plan
4. Cache results when appropriate
5. Update API documentation

### Adding New Agent
1. Create directory in `/agents/`
2. Add `main.py`, `Dockerfile`, `requirements.txt`
3. Update `docker-compose.yml`
4. Add health check endpoint
5. Update `MULTI_AGENT_SYSTEM.md` docs

## Environment Configuration

Required environment variables in `.env`:
```bash
# AI Providers
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4
AI_PROVIDER=openai

# Market Data
COINGECKO_API_KEY=...
ALPHA_VANTAGE_API_KEY=...
WHALE_ALERT_API_KEY=...
NEWSCATCHER_API_KEY=...

# Application
PORT=5000
DEBUG=False
SECRET_KEY=random-secret-key
```

## File Locations

### Static Files
- CSS: `/static/css/`
- JavaScript: `/static/js/`
- Images: `/static/images/`

### Templates
- HTML templates: `/templates/`
- Uses Jinja2 templating

### Data Storage
- User data: `/data/users/`
- Transaction data: `/data/transactions/`
- Backups: `/data/backups/`

### Configuration
- Main config: `/config/`
- Docker configs: `/agents/*/`
- Environment: `.env` (not committed)

## Dependencies

Key Python packages (from `requirements.txt`):
- Flask - Web framework
- requests - HTTP client
- pandas - Data analysis
- numpy - Numerical computing
- scikit-learn - Machine learning
- openai - OpenAI API
- anthropic - Anthropic API
- crewai - Multi-agent orchestration
- fastapi - API for agents
- docker - Container management

## Quick Commands
```bash
# Start application
./start.sh              # Linux/Mac
python3 start.py        # Cross-platform

# Multi-agent system
./setup_agents.sh       # Setup & start
make up                # Start Docker services
make down              # Stop Docker services
make logs              # View logs

# Testing
python3 test_complete_system.py
./test_agents.sh
```

## Documentation References
- `README.md` - Project overview and setup
- `ARCHITECTURE.md` - System architecture details
- `MULTI_AGENT_SYSTEM.md` - Multi-agent system guide
- `AI_ENHANCEMENT_GUIDE.md` - AI integration guide
- `OPENAI_SETUP_GUIDE.md` - OpenAI configuration
- `AI_COPILOT_GUIDE.md` - Full AI assistant guide
- `.copilot-instructions.md` - Quick reference

## Best Practices

1. **Security**: Always validate inputs, hash passwords, use HTTPS
2. **Error Handling**: Catch specific exceptions, log errors, return meaningful messages
3. **Testing**: Write tests for new features, run tests before committing
4. **Documentation**: Update docs when adding features, write clear docstrings
5. **Performance**: Cache expensive operations, use async where appropriate
6. **Code Quality**: Follow PEP 8, use type hints, keep functions focused

---

**Remember**: This is a financial application handling user data and payments. 
Security and data validation are paramount!
