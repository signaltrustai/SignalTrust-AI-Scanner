# 🎯 Admin Payment Section - Quick Reference

## 🔒 Access Your Payment Information

### URL
```
https://signaltrust-ai-scanner.onrender.com/admin/payment-info
```

### Login Credentials
- **Email**: `signaltrustai@gmail.com`
- **Password**: Set in environment variable `ADMIN_PASSWORD`
- **User ID**: `owner_admin_001`

---

## 💳 Your Payment Methods

### 🔐 Cryptocurrency Wallets (6 Networks)

| Network | Address | Network Fee |
|---------|---------|-------------|
| **Ethereum** | `0xFDAf80b517993A3420E96Fb11D01e959EE35A419` | ~$5-50 |
| **Polygon** | `0xFDAf80b517993A3420E96Fb11D01e959EE35A419` | ~$0.01 ⭐ |
| **Binance SC** | `0xFDAf80b517993A3420E96Fb11D01e959EE35A419` | ~$0.10 |
| **Arbitrum** | `0xFDAf80b517993A3420E96Fb11D01e959EE35A419` | ~$0.50 |
| **Bitcoin** | `bc1qz4kq6hu05j6rdnzv2xe325wf0404smhsaxas86` | ~$1-10 |
| **Solana** | `BATM5MQZxeNaJGPGdUsRGD5mputbCkHheckcm1y8Vt6r` | ~$0.001 |

⭐ **Recommended**: Use Polygon for lowest fees!

### 💙 PayPal
- **Email**: `payments@signaltrust.ai`
- **PayPal.me**: `https://paypal.me/signaltrust`

### 🏦 Bank Transfer
- Configure in `.env` file
- Supports: USD, EUR, GBP, CAD

### 💳 Card Payments (Stripe)
- Configure payment links in `.env`
- Fast 1-click checkout

---

## 🚀 Quick Start

### 1. Access Admin Panel
```bash
# Navigate to:
https://signaltrust-ai-scanner.onrender.com/admin/payment-info

# Or from dashboard:
Dashboard → Informations de Paiement
```

### 2. View Payment Info
- All crypto addresses displayed
- Click "Copy" to copy any address
- Bank details (if configured)
- PayPal information
- Stripe links

### 3. Share with Clients
You can share:
- ✅ Crypto wallet addresses
- ✅ PayPal email
- ✅ Stripe payment links
- ❌ Bank account details (keep private)

---

## 🔐 Security Features

1. **Encrypted Storage**: All data encrypted with AES-256
2. **Admin-Only**: Only you can access this section
3. **No Public Access**: Protected by authentication
4. **Secure Keys**: Stored in environment variables
5. **HTTPS**: All traffic encrypted

---

## 📱 Client Payment Instructions

### For Crypto Payments

**Ethereum/Polygon/BSC/Arbitrum**:
```
Send USDT, USDC, ETH, or other tokens to:
0xFDAf80b517993A3420E96Fb11D01e959EE35A419

✅ Use Polygon network for lowest fees ($0.01)
✅ Confirm transaction on blockchain explorer
✅ Send transaction hash for confirmation
```

**Bitcoin**:
```
Send BTC to:
bc1qz4kq6hu05j6rdnzv2xe325wf0404smhsaxas86

✅ Use SegWit address (lower fees)
✅ Wait for 3 confirmations (~30 min)
✅ Send transaction ID for verification
```

**Solana**:
```
Send SOL or SPL tokens to:
BATM5MQZxeNaJGPGdUsRGD5mputbCkHheckcm1y8Vt6r

✅ Fastest network (~400ms)
✅ Lowest fees ($0.001)
✅ Send signature for confirmation
```

### For PayPal

```
Send payment to:
payments@signaltrust.ai

OR use PayPal.me:
https://paypal.me/signaltrust

✅ Add note: "SignalTrust AI - [Your Email]"
✅ Screenshot confirmation
✅ Email us transaction ID
```

### For Card Payments

```
Use Stripe payment link:
[Configure in admin panel]

✅ Instant confirmation
✅ Secure checkout
✅ Automatic receipt
```

---

## 🛠️ Configuration

### Environment Variables

Add to `.env` or Render environment:

```bash
# Crypto Wallets (Already configured)
ETHEREUM_WALLET_ADDRESS=0xFDAf80b517993A3420E96Fb11D01e959EE35A419
POLYGON_WALLET_ADDRESS=0xFDAf80b517993A3420E96Fb11D01e959EE35A419
BINANCE_WALLET_ADDRESS=0xFDAf80b517993A3420E96Fb11D01e959EE35A419
ARBITRUM_WALLET_ADDRESS=0xFDAf80b517993A3420E96Fb11D01e959EE35A419
BITCOIN_WALLET_ADDRESS=bc1qz4kq6hu05j6rdnzv2xe325wf0404smhsaxas86
SOLANA_WALLET_ADDRESS=BATM5MQZxeNaJGPGdUsRGD5mputbCkHheckcm1y8Vt6r

# PayPal (Configure yours)
PAYPAL_EMAIL=payments@signaltrust.ai
PAYPAL_ME_LINK=https://paypal.me/signaltrust

# Bank Accounts (Optional - Add your details)
BANK_NAME_USD=Your Bank Name
BANK_ACCOUNT_NUMBER_USD=Your Account Number
BANK_ROUTING_NUMBER_USD=Your Routing Number
BANK_SWIFT_CODE_USD=Your SWIFT Code

# Stripe Links (Optional)
STRIPE_STARTER_MONTHLY_LINK=https://buy.stripe.com/...
STRIPE_PRO_MONTHLY_LINK=https://buy.stripe.com/...
STRIPE_ENTERPRISE_MONTHLY_LINK=https://buy.stripe.com/...
```

---

## 📊 Payment Tracking

### Crypto Payments
Use blockchain explorers:
- **Ethereum/Polygon/BSC/Arbitrum**: https://etherscan.io (or equivalent)
- **Bitcoin**: https://blockstream.info
- **Solana**: https://explorer.solana.com

### PayPal
- Check PayPal account activity
- Download transaction history
- Export to CSV for accounting

### Stripe
- Check Stripe dashboard
- View all payments
- Download invoices

---

## 🎯 Pricing Reference

### Subscription Plans
- **Free**: $0/month
- **Starter**: $19.99/month
- **Pro**: $49.99/month
- **Enterprise**: $199.99/month

### Features À la Carte
- AI Predictions: $19.99/mo
- Whale Watcher: $29.99/mo
- Portfolio Optimizer: $24.99/mo
- Custom features: Contact for pricing

---

## 💡 Tips for Clients

### Best Payment Methods by Region

**USA** 🇺🇸:
1. Stripe/Card (instant)
2. PayPal (instant)
3. Crypto - Polygon (fast + cheap)

**Europe** 🇪🇺:
1. SEPA Bank Transfer (1-2 days)
2. PayPal (instant)
3. Crypto - Polygon (fast + cheap)

**Asia** 🌏:
1. Crypto - Polygon (best option)
2. PayPal (if available)
3. Wire transfer (slow)

**Global** 🌍:
1. Crypto (universal, fast)
2. PayPal (widely accepted)
3. Stripe (card payments)

### Recommended Networks by Amount

**< $50**:
- ✅ Polygon ($0.01 fee)
- ✅ Solana ($0.001 fee)
- ⚠️ Bitcoin (fees may exceed amount)

**$50-$500**:
- ✅ Polygon (best value)
- ✅ PayPal (familiar)
- ✅ Stripe/Card (instant)

**> $500**:
- ✅ Any network works
- ✅ Bank transfer (lowest %)
- ✅ Bitcoin (secure + final)

---

## 🔧 Troubleshooting

### Payment Not Received

**Crypto**:
1. Check transaction on blockchain explorer
2. Verify correct address used
3. Wait for confirmations (varies by network)
4. Contact if not visible after 1 hour

**PayPal**:
1. Check spam folder for receipt
2. Verify correct email used
3. Check PayPal account for hold
4. Contact PayPal support if needed

**Card/Stripe**:
1. Check email for receipt
2. Verify card was charged
3. Check bank statement
4. Contact if issue persists

### Wrong Network Used

If client sends to wrong network:
- Ethereum tokens can be recovered
- Cross-chain recovery may be possible
- Contact immediately with transaction details

### Refund Requests

Process:
1. Verify original payment
2. Issue refund via same method
3. Deduct platform fees if applicable
4. Provide refund confirmation

---

## 📞 Support

### For You (Admin)
- **Dashboard**: `/admin/payment-info`
- **Update Info**: Edit `.env` file
- **Security**: Keep admin password secure

### For Clients
- **Payment Issues**: signaltrustai@gmail.com
- **Transaction Verification**: Provide TX hash
- **Refunds**: Contact via email with details

---

## ✅ Checklist for Each Payment

### When Client Pays

- [ ] Verify payment received
- [ ] Check transaction details
- [ ] Activate subscription
- [ ] Send confirmation email
- [ ] Add to accounting system
- [ ] Thank the client!

### Monthly

- [ ] Review all transactions
- [ ] Check for pending payments
- [ ] Process any refunds
- [ ] Update payment notes
- [ ] Backup payment records

---

## 🎉 Summary

**You now have a complete, secure payment management system!**

✅ **6 Crypto Networks**: Industry-leading coverage  
✅ **PayPal**: Instant, familiar payments  
✅ **Stripe**: Professional card processing  
✅ **Bank Transfers**: Traditional option  
✅ **Encrypted Storage**: Secure data protection  
✅ **Admin-Only**: Private and confidential  

**Your payment information is ready to share with clients!**

---

**Last Updated**: 2026-02-08  
**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Access**: Admin Only 🔒
