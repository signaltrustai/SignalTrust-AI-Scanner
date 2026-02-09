# 🔐 Secure API Keys Management

This folder contains the secure API key management system for SignalTrust AI Scanner.

## 📁 Files

- `__init__.py` - Module initialization
- `key_manager.py` - Encrypted key storage and retrieval
- `key_validator.py` - Key validation and connection testing
- `keys.enc` - Encrypted keys file (gitignored)
- `.gitkeep` - Keep folder in git

## 🚀 Quick Start

### 1. Set Master Password

For encryption to work, set a master password:

```bash
export API_MASTER_PASSWORD="your-secure-password-here"
```

Add this to your `.env` file:
```
API_MASTER_PASSWORD=your-secure-password-here
```

### 2. Using the Key Manager

```python
from config.api_keys import KeyManager

# Initialize manager
manager = KeyManager()

# Store a key
manager.set_key('OPENAI_API_KEY', 'sk-proj-...', save=True)

# Retrieve a key
api_key = manager.get_key('OPENAI_API_KEY')

# List all keys
keys = manager.list_keys()

# Import from environment
manager.import_from_env()
```

### 3. Validating Keys

```python
from config.api_keys import KeyValidator

# Initialize validator
validator = KeyValidator()

# Validate format only
result = validator.validate_key('OPENAI_API_KEY', 'sk-proj-...', test_connection=False)
print(result['format_valid'])  # True/False

# Validate and test connection
result = validator.validate_key('OPENAI_API_KEY', 'sk-proj-...', test_connection=True)
print(result['connection_valid'])  # True/False
```

## 🔒 Security Features

### Encryption
- Uses **Fernet** (symmetric encryption) from cryptography library
- **PBKDF2** key derivation with 100,000 iterations
- Keys are encrypted at rest in `keys.enc` file

### Access Control
- Requires master password to encrypt/decrypt
- Falls back to environment variables if encryption not available
- Logs all access attempts

### Best Practices
- ✅ Never commit `keys.enc` file to git
- ✅ Use different master passwords for dev/prod
- ✅ Rotate keys regularly (every 90 days)
- ✅ Use environment variables for master password
- ✅ Keep master password in secure location (password manager)

## 📊 Supported API Providers

### AI Providers
- **OpenAI** - GPT-4, GPT-3.5
- **Anthropic** - Claude models
- **Local** - Ollama, etc.

### Market Data Providers
- **CoinGecko** - Crypto prices
- **Alpha Vantage** - Stock data
- **Whale Alert** - Large transactions
- **NewsCatcher** - Market news

## 🔧 Advanced Usage

### Rotating Keys

```python
manager = KeyManager()
manager.rotate_key('OPENAI_API_KEY', 'new-key-value')
```

### Exporting to Environment

```python
manager = KeyManager()
manager.export_to_env(['OPENAI_API_KEY', 'COINGECKO_API_KEY'])
```

### Batch Validation

```python
validator = KeyValidator()
results = validator.validate_all_keys({
    'OPENAI_API_KEY': 'sk-...',
    'COINGECKO_API_KEY': 'CG-...',
}, test_connection=True)
```

## 🛠️ Command Line Tools

### View all keys (masked)
```bash
python3 config/api_keys/key_manager.py
```

### Validate keys
```bash
python3 config/api_keys/key_validator.py
```

## 🔐 Environment Variables

The system supports both encrypted storage and environment variables:

1. **Master Password**: `API_MASTER_PASSWORD`
2. **AI Keys**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
3. **Market Data**: `COINGECKO_API_KEY`, `ALPHAVANTAGE_API_KEY`, etc.

Priority: Encrypted file > Environment variables > None

## 📝 File Structure

```
config/api_keys/
├── __init__.py          # Module exports
├── key_manager.py       # Encryption & storage
├── key_validator.py     # Validation & testing
├── keys.enc            # Encrypted keys (gitignored)
├── .gitkeep            # Keep folder in git
└── README.md           # This file
```

## 🚨 Troubleshooting

### Keys not loading
- Check if `API_MASTER_PASSWORD` is set
- Verify `keys.enc` file exists
- Check file permissions

### Validation failing
- Verify key format matches expected pattern
- Test connection manually
- Check API provider status

### Encryption errors
- Ensure master password is consistent
- Don't change master password without re-encrypting
- Backup `keys.enc` before rotating master password

## 📚 Documentation

For more information:
- See `.env.example` for all available keys
- Check `OPENAI_SETUP_GUIDE.md` for OpenAI setup
- Read `CLOUD_STORAGE_GUIDE.md` for cloud keys

## 🔗 Integration

This module integrates with:
- `app.py` - Main Flask application
- `ai_provider.py` - AI provider management
- `market_scanner.py` - Market data collection
- Multi-agent system (`agents/*/`)

## ⚠️ Important Notes

1. **Never commit** `keys.enc` to version control
2. **Backup** your keys regularly
3. **Rotate** keys every 90 days
4. **Use different** keys for dev/staging/prod
5. **Monitor** key usage and rate limits

---

**Made with 🔒 by SignalTrust AI**

For support: Check GitHub issues or documentation
