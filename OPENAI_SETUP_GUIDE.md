# OpenAI Integration Setup Guide

## Overview

SignalTrust AI Scanner now uses **OpenAI** (GPT-4/GPT-3.5) for advanced market analysis, price predictions, and AI-powered insights.

## 🔐 Security First

**⚠️ CRITICAL: Never commit API keys to your repository!**

All API keys should be stored in a `.env` file that is listed in `.gitignore`.

## Setup Instructions

### 1. Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Navigate to "API Keys" section
4. Click "Create new secret key"
5. Copy your API key (starts with `sk-proj-...` or `sk-...`)
6. **Important**: Store it securely - you won't be able to see it again!

### 2. Configure Environment Variables

Create a `.env` file in the root directory of the project:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
OPENAI_MODEL=gpt-4  # Options: gpt-4, gpt-3.5-turbo, gpt-4-turbo

# Optional: AI Provider Selection
AI_PROVIDER=openai
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `openai>=1.0.0` - OpenAI Python library
- All other required dependencies

### 4. Verify Installation

Run the test script to verify your OpenAI integration:

```bash
python test_ai_system.py
```

## Available Models

### GPT-4 (Recommended)
- **Model**: `gpt-4`
- **Best for**: Complex analysis, detailed predictions
- **Cost**: Higher but more accurate
- **Max tokens**: 8,192

### GPT-4 Turbo
- **Model**: `gpt-4-turbo`
- **Best for**: Fast, accurate responses
- **Cost**: Lower than GPT-4
- **Max tokens**: 128,000

### GPT-3.5 Turbo
- **Model**: `gpt-3.5-turbo`
- **Best for**: Quick analysis, lower cost
- **Cost**: Most economical
- **Max tokens**: 16,384

## Usage Examples

### Basic Market Analysis

```python
from asi1_integration import ASI1AIIntegration

# Initialize with your API key (or use environment variable)
ai = ASI1AIIntegration(api_key="your-api-key")

# Analyze market data
market_data = {
    "symbol": "BTC",
    "price": 45000,
    "volume": 1000000000,
    "change_24h": 5.2
}

result = ai.analyze_market_with_ai(market_data, context="Bitcoin price movement")
print(result['analysis'])
```

### Price Prediction

```python
# Predict price movement
historical_data = [
    {"timestamp": "2024-01-01", "price": 42000},
    {"timestamp": "2024-01-02", "price": 43000},
    # ... more data
]

prediction = ai.predict_price_movement("BTC", historical_data)
print(prediction['prediction'])
```

### Whale Transaction Analysis

```python
# Analyze whale movements
whale_data = {
    "transaction_hash": "0x123...",
    "amount": 1000,
    "from": "0xabc...",
    "to": "0xdef..."
}

analysis = ai.whale_watch_analysis(whale_data)
print(f"Alert Level: {analysis['alert_level']}")
print(analysis['whale_analysis'])
```

## Multiple API Keys for Different Services

If you have different OpenAI API keys for different services (market, crypto, whale watching, etc.), you can:

1. **Option 1: Environment Variables (Recommended)**

```bash
# .env file
OPENAI_API_KEY_MARKET=sk-proj-...
OPENAI_API_KEY_CRYPTO=sk-proj-...
OPENAI_API_KEY_WHALE=sk-proj-...
```

Then in your code:
```python
# Use specific keys for different services
market_ai = ASI1AIIntegration(api_key=os.getenv('OPENAI_API_KEY_MARKET'))
crypto_ai = ASI1AIIntegration(api_key=os.getenv('OPENAI_API_KEY_CRYPTO'))
```

2. **Option 2: Configuration File (For Multiple Instances)**

Create a `config/api_keys.json` (add to .gitignore!):
```json
{
  "market": "sk-proj-...",
  "crypto": "sk-proj-...",
  "whale": "sk-proj-..."
}
```

## Cost Management

### Monitoring Usage

OpenAI provides usage dashboards:
- Visit: https://platform.openai.com/usage
- Monitor: Daily/monthly costs
- Set: Usage limits and alerts

### Optimize Costs

1. **Choose the right model**:
   - Development: `gpt-3.5-turbo`
   - Production: `gpt-4` or `gpt-4-turbo`

2. **Reduce token usage**:
   - Limit response length with `max_tokens`
   - Send only necessary context
   - Cache common responses

3. **Set usage limits**:
   ```python
   # In your .env
   AI_MAX_TOKENS=1000  # Reduce from default 2000
   AI_TEMPERATURE=0.5  # More focused responses
   ```

## Troubleshooting

### Error: "OPENAI_API_KEY not configured"

**Solution**: Ensure your `.env` file contains a valid API key:
```bash
OPENAI_API_KEY=sk-proj-your-key-here
```

### Error: "OpenAI library not installed"

**Solution**: Install the OpenAI package:
```bash
pip install openai
```

### Error: "Invalid API Key"

**Causes**:
1. API key is incorrect
2. API key has been revoked
3. Billing issue on OpenAI account

**Solution**:
1. Verify the key at https://platform.openai.com/api-keys
2. Generate a new key if needed
3. Check billing status

### Error: "Rate limit exceeded"

**Solution**:
1. Upgrade your OpenAI plan
2. Implement request throttling
3. Add retry logic with exponential backoff

## Security Best Practices

### ✅ DO:
- Store API keys in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys regularly
- Monitor usage for anomalies
- Set usage limits on OpenAI dashboard

### ❌ DON'T:
- Commit API keys to Git
- Share API keys in chat/email
- Use the same key for dev and prod
- Expose keys in client-side code
- Store keys in plain text files (that are tracked)

## Migration from ASI1

If you're migrating from ASI1 experimental AI:

1. **Update environment variables**:
   ```bash
   # Remove (if present)
   # ASI_ONE_API_KEY=...
   
   # Add
   OPENAI_API_KEY=your-openai-key
   ```

2. **No code changes needed**: The `ASI1AIIntegration` class now uses OpenAI under the hood

3. **Test thoroughly**: Run your existing tests to ensure compatibility

## Support

For issues or questions:
- OpenAI Documentation: https://platform.openai.com/docs
- OpenAI Support: https://help.openai.com
- SignalTrust AI Issues: https://github.com/signaltrustai/SignalTrust-AI-Scanner/issues

## Additional Resources

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Pricing](https://openai.com/pricing)
- [Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
