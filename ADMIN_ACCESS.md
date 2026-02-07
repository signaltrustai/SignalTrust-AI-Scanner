# Admin Access Documentation

## Default Administrator Account

SignalTrust AI Scanner includes a pre-configured administrator account with full access to all system features.

### Login Credentials

- **Email:** signaltrustai@gmail.com
- **Password:** !Obiwan12!
- **User ID:** owner_admin_001

### Account Details

- **Full Name:** SignalTrust Admin
- **Plan:** Enterprise (Unlimited Access)
- **Status:** Active
- **Payment Status:** Active

## Administrator Privileges

The administrator account has full access to:

### AI Chat System
- **All AI Modes Available:**
  - 🤖 Auto-Detect: Automatically selects the best AI for your question
  - 🧠 ASI1 Agent: General market conversation and analysis
  - 📊 Market Intelligence: Deep market analysis and pattern recognition
  - 🐋 Whale Watcher: Track and analyze large transactions
  - 🔮 Prediction AI: Price predictions and market forecasts

### Whale Watcher
- **Unlimited Access:**
  - Real-time whale transaction monitoring
  - NFT whale movement tracking
  - Whale activity statistics
  - All transaction history

### Premium Features
- **Full Feature Access:**
  - All dashboards and data
  - Real-time market data
  - AI-powered predictions
  - Advanced analytics
  - Unlimited API calls

## Security Considerations

### ⚠️ Important Security Notice

**CHANGE THE DEFAULT PASSWORD IMMEDIATELY AFTER FIRST LOGIN**

The default password is documented here for initial setup only. For production use:

1. Log in with the default credentials
2. Navigate to Account Settings
3. Change the password to a strong, unique password
4. Store the new password securely

### Password Requirements

When changing the password, ensure it meets the following criteria:
- Minimum 8 characters
- Mix of uppercase and lowercase letters
- At least one number
- At least one special character

### Password Security

The system uses industry-standard security practices:
- **Hash Algorithm:** PBKDF2-HMAC-SHA256
- **Iterations:** 100,000
- **Salt:** Unique per user
- **Storage:** Only password hashes are stored, never plain text

## Account Management

### How the Admin Account Works

1. **Automatic Creation:** The admin account is automatically created when the application starts if it doesn't exist
2. **User ID Enforcement:** The admin account always has the user_id `owner_admin_001`
3. **Email Recognition:** The system recognizes `signaltrustai@gmail.com` as the owner email
4. **Access Control:** All premium features check for either the owner user_id or email

### Resetting the Admin Password

If you forget the admin password:

1. Stop the application
2. Delete the entry for `signaltrustai@gmail.com` from `data/users.json`
3. Restart the application (the admin account will be recreated with default password)
4. Log in with default credentials and set a new password

### Multiple Administrators

Currently, the system supports a single owner account. To grant admin privileges to other users:

1. Create a regular user account
2. Manually update their plan to "enterprise" in `data/users.json`
3. Note: They won't have the same owner-level access as the default admin

## Technical Details

### Configuration Files

- **Admin Config:** `config/admin_config.py`
- **User Database:** `data/users.json`
- **Access Control:** `ai_chat_system.py`, `user_auth.py`

### Access Control Logic

The system checks for admin access using:
```python
# Check by user_id
is_admin_user_id(user_id)  # Returns True if user_id == "owner_admin_001"

# Check by email
is_admin_email(email)  # Returns True if email == "signaltrustai@gmail.com"
```

### Database Entry

The admin account is stored in `data/users.json` with the following structure:
```json
{
  "signaltrustai@gmail.com": {
    "user_id": "owner_admin_001",
    "email": "signaltrustai@gmail.com",
    "full_name": "SignalTrust Admin",
    "password_hash": "[HASHED_PASSWORD]",
    "salt": "[UNIQUE_SALT]",
    "plan": "enterprise",
    "created_at": "[TIMESTAMP]",
    "last_login": null,
    "is_active": true,
    "payment_status": "active"
  }
}
```

## Support

For issues with the admin account or access control, please contact the development team.

---

**Last Updated:** February 2026  
**Version:** 1.0
