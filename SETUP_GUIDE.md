# SignalTrust AI Scanner - Complete Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git

### Installation Steps

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
   cd SignalTrust-AI-Scanner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application**:
   ```bash
   # Using the start script (recommended)
   python3 start.py
   
   # OR directly with app.py
   python3 app.py
   ```

4. **Access the application**:
   - Open your browser and navigate to: `http://localhost:5000`
   - Default admin login:
     - Email: `signaltrustai@gmail.com`
     - Password: `!Obiwan12!`

## 🔧 Configuration

### Environment Variables
Create a `.env` file (based on `.env.example`) for:
- Cloud storage credentials (AWS S3, GCP, Azure)
- API keys for market data providers
- Agent IDs for SignalTrust AI agents

```bash
# Example .env file
AGENT_API_BASE_URL=https://api.signaltrust.ai
AGENT_API_KEY=your_api_key_here
AGENT_STOCK_ID=ASI1-STOCK-001
AGENT_CRYPTO_ID=ASI2-CRYPTO-002
```

### Admin Configuration
- Edit `config/admin_config.py` to change admin credentials
- **Security**: Change the default password before deploying to production!

## 💬 AI Chat System

### Features
The AI Chat system provides 5 specialized AI modes:
1. **Auto-Detect** 🤖 - Automatically selects the best AI
2. **ASI1 Agent** 🧠 - General market conversation
3. **Market Intelligence** 📊 - Deep market analysis
4. **Whale Watcher** 🐋 - Large transaction tracking
5. **Prediction AI** 🔮 - Price predictions

### Access Requirements
- **Owner/Admin Access**: Full access to all AI modes
- **Admin Email**: `signaltrustai@gmail.com`
- **Admin User ID**: `owner_admin_001`

### API Endpoints
```bash
# Get available AI modes
GET /api/ai-chat/modes

# Send a chat message
POST /api/ai-chat/message
Content-Type: application/json
{
  "message": "What is Bitcoin price prediction?",
  "mode": "prediction"  # or "auto", "asi1", "intelligence", "whale"
}

# Get conversation history
GET /api/ai-chat/history

# Clear conversation history
POST /api/ai-chat/clear-history
```

### Testing AI Chat
```bash
# Test modes endpoint
curl http://localhost:5000/api/ai-chat/modes | python3 -m json.tool

# Test chat message (requires login)
curl -X POST http://localhost:5000/api/ai-chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze BTC", "mode": "auto"}'
```

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
**Solution**: Change the port using environment variable
```bash
PORT=5001 python3 app.py
```

### Issue: "404 Not Found" for all routes
**Cause**: Flask app was being recreated, overwriting routes
**Solution**: This is now fixed in the latest version. Update your code.

### Issue: "Access restricted" when using AI Chat
**Cause**: User is not logged in or doesn't have admin access
**Solution**: 
1. Log in with admin credentials (signaltrustai@gmail.com)
2. Or modify `config/admin_config.py` to add your email

### Issue: Import errors or module not found
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Background worker errors
**Solution**: The background worker is optional. If it causes issues, you can disable it by commenting out lines in `app.py`:
```python
# background_worker.start()  # Comment this line
```

## 📝 Development

### File Structure
```
SignalTrust-AI-Scanner/
├── app.py                    # Main Flask application
├── start.py                  # Startup script
├── requirements.txt          # Python dependencies
├── config/
│   └── admin_config.py      # Admin credentials
├── templates/               # HTML templates
│   └── ai_chat.html        # AI Chat interface
├── static/                  # CSS, JS, images
├── data/                    # JSON data storage
├── ai_chat_system.py        # AI Chat backend
├── asi1_integration.py      # ASI1 AI integration
├── ai_market_intelligence.py
├── whale_watcher.py
└── [other modules...]
```

### Running Tests
```bash
# Test complete system
python3 test_complete_system.py

# Test AI chat PWA
python3 test_ai_chat_pwa.py

# Test admin account
python3 test_admin_account.py
```

## 🔒 Security

### Important Security Notes
1. **Change default admin password** before deployment
2. **Never commit `.env` files** with real credentials
3. **Use HTTPS** in production
4. **Enable CORS** only for trusted domains
5. **Regularly update dependencies**: `pip install -r requirements.txt --upgrade`

### Production Deployment
For production, use a proper WSGI server:
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📚 Additional Documentation
- [AI Chat PWA Documentation](./AI_CHAT_PWA_DOCUMENTATION.md)
- [Admin Access Guide](./ADMIN_ACCESS.md)
- [Cloud Storage Guide](./CLOUD_STORAGE_GUIDE.md)
- [Final Capabilities](./FINAL_CAPABILITIES.md)

## 🆘 Support
If you encounter issues not covered here:
1. Check the GitHub Issues
2. Review the documentation files
3. Ensure all dependencies are up to date
4. Check the logs in `signaltrust_events.log`

## ✅ Verification Checklist
After setup, verify:
- [ ] Application starts without errors
- [ ] Web interface loads at http://localhost:5000
- [ ] Can log in with admin credentials
- [ ] AI Chat page loads at http://localhost:5000/ai-chat
- [ ] API endpoints respond (test with curl)
- [ ] All 67 routes are registered (check Flask startup logs)

## 🎯 Known Issues Fixed
1. ✅ Flask app recreation bug (routes were being overwritten)
2. ✅ Duplicate route definitions causing startup failures
3. ✅ Missing AI chat API endpoints
4. ✅ Conflicting `if __name__ == "__main__"` blocks
5. ✅ Method name mismatch in AI chat system

---

**Version**: Updated February 2026  
**Status**: Fully functional and optimized
