#!/usr/bin/env python3
"""
SignalTrust AI Market Scanner - Web Application
Main Flask application with routes and API endpoints
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Import market scanner modules
from market_scanner import MarketScanner
from market_analyzer import MarketAnalyzer
from ai_predictor import AIPredictor
from user_auth import UserAuth
from payment_processor import PaymentProcessor
from coupon_manager import CouponManager
from asi1_integration import ASI1AIIntegration
from realtime_market_data import RealTimeMarketData
from notification_center import NotificationCenter, NotificationType, NotificationPriority
from whale_watcher import WhaleWatcher
from ai_market_intelligence import AIMarketIntelligence

app = Flask(__name__)
CORS(app)

# Initialize components
market_scanner = MarketScanner()
market_analyzer = MarketAnalyzer()
ai_predictor = AIPredictor()
user_auth = UserAuth()
payment_processor = PaymentProcessor()
coupon_manager = CouponManager()
asi1_ai = ASI1AIIntegration()
realtime_data = RealTimeMarketData()
notification_center = NotificationCenter()
whale_watcher = WhaleWatcher()

# Initialize Advanced AI Intelligence System
ai_intelligence = AIMarketIntelligence(
    asi1_integration=asi1_ai,
    realtime_data=realtime_data,
    whale_watcher=whale_watcher
)

# Configuration
app.config['SECRET_KEY'] = 'signaltrust-ai-scanner-2026'
app.config['JSON_SORT_KEYS'] = False


# ============================================================================
# Web Pages Routes
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/scanner')
def scanner_page():
    """Market scanner page."""
    return render_template('scanner.html')


@app.route('/analyzer')
def analyzer_page():
    """Market analyzer page."""
    return render_template('analyzer.html')


@app.route('/predictions')
def predictions_page():
    """AI predictions page."""
    return render_template('predictions.html')


@app.route('/settings')
def settings_page():
    """Settings page."""
    return render_template('settings.html')


@app.route('/register')
def register_page():
    """Registration page."""
    return render_template('register.html')


@app.route('/login')
def login_page():
    """Login page."""
    return render_template('login.html')


@app.route('/pricing')
def pricing_page():
    """Pricing plans page."""
    return render_template('pricing.html')


@app.route('/payment')
def payment_page():
    """Payment page."""
    return render_template('payment.html')


@app.route('/dashboard')
def dashboard_page():
    """User dashboard page."""
    return render_template('dashboard.html')


@app.route('/whale-watcher')
def whale_watcher_page():
    """Whale watcher page (restricted access)."""
    return render_template('whale_watcher.html')


@app.route('/notifications')
def notifications_page():
    """Notifications center page."""
    return render_template('notifications.html')


@app.route('/ai-intelligence')
def ai_intelligence_page():
    """AI Market Intelligence page."""
    return render_template('ai_intelligence.html')


# ============================================================================
# API Routes - Market Data
# ============================================================================

@app.route('/api/markets/overview', methods=['GET'])
def get_markets_overview():
    """Get overview of all markets."""
    try:
        overview = market_scanner.get_markets_overview()
        return jsonify({
            'success': True,
            'data': overview,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/scan', methods=['POST'])
def scan_market():
    """Scan a specific market."""
    try:
        data = request.get_json()
        market_type = data.get('market_type', 'stocks')
        symbols = data.get('symbols', [])
        
        results = market_scanner.scan_market(market_type, symbols)
        
        return jsonify({
            'success': True,
            'data': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/trending', methods=['GET'])
def get_trending():
    """Get trending stocks/assets."""
    try:
        market_type = request.args.get('type', 'stocks')
        trending = market_scanner.get_trending_assets(market_type)
        
        return jsonify({
            'success': True,
            'data': trending,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Analysis
# ============================================================================

@app.route('/api/analyze/technical', methods=['POST'])
def analyze_technical():
    """Perform technical analysis on a symbol."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        timeframe = data.get('timeframe', '1d')
        
        analysis = market_analyzer.technical_analysis(symbol, timeframe)
        
        return jsonify({
            'success': True,
            'data': analysis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze market sentiment."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        sentiment = market_analyzer.sentiment_analysis(symbol)
        
        return jsonify({
            'success': True,
            'data': sentiment,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze/patterns', methods=['POST'])
def detect_patterns():
    """Detect chart patterns."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        patterns = market_analyzer.detect_patterns(symbol)
        
        return jsonify({
            'success': True,
            'data': patterns,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - AI Predictions
# ============================================================================

@app.route('/api/predict/price', methods=['POST'])
def predict_price():
    """Predict future price using AI."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        days_ahead = data.get('days', 7)
        
        prediction = ai_predictor.predict_price(symbol, days_ahead)
        
        return jsonify({
            'success': True,
            'data': prediction,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predict/signals', methods=['POST'])
def generate_signals():
    """Generate trading signals using AI."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        signals = ai_predictor.generate_signals(symbol)
        
        return jsonify({
            'success': True,
            'data': signals,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predict/risk', methods=['POST'])
def assess_risk():
    """Assess risk using AI."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        risk_assessment = ai_predictor.assess_risk(symbol)
        
        return jsonify({
            'success': True,
            'data': risk_assessment,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Watchlist & Portfolio
# ============================================================================

@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """Get user's watchlist."""
    try:
        watchlist = market_scanner.get_watchlist()
        return jsonify({
            'success': True,
            'data': watchlist
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/watchlist/add', methods=['POST'])
def add_to_watchlist():
    """Add symbol to watchlist."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        result = market_scanner.add_to_watchlist(symbol)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/watchlist/remove', methods=['POST'])
def remove_from_watchlist():
    """Remove symbol from watchlist."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        result = market_scanner.remove_from_watchlist(symbol)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Authentication
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register_user():
    """Register new user."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        plan = data.get('plan', 'free')
        
        result = user_auth.register_user(email, password, full_name, plan)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """Login user."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        result = user_auth.login_user(email, password)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout_user():
    """Logout user."""
    try:
        data = request.get_json()
        session_token = data.get('session_token')
        
        result = user_auth.logout_user(session_token)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auth/verify', methods=['POST'])
def verify_session():
    """Verify user session."""
    try:
        data = request.get_json()
        session_token = data.get('session_token')
        
        user = user_auth.verify_session(session_token)
        
        if user:
            return jsonify({
                'success': True,
                'user': user
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Payment & Subscription
# ============================================================================

@app.route('/api/payment/plans', methods=['GET'])
def get_payment_plans():
    """Get all subscription plans."""
    try:
        plans = payment_processor.get_plans()
        return jsonify({
            'success': True,
            'plans': plans
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    """Process a payment."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        email = data.get('email')
        plan_id = data.get('plan_id')
        payment_method = data.get('payment_method')
        
        result = payment_processor.process_payment(user_id, email, plan_id, payment_method)
        
        if result['success']:
            # Update user plan
            user_auth.update_user_plan(email, plan_id, 'active')
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/validate-card', methods=['POST'])
def validate_card():
    """Validate credit card number."""
    try:
        data = request.get_json()
        card_number = data.get('card_number')
        
        result = payment_processor.validate_card_number(card_number)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/transactions', methods=['GET'])
def get_transactions():
    """Get user's transaction history."""
    try:
        user_id = request.args.get('user_id')
        
        transactions = payment_processor.get_user_transactions(user_id)
        
        return jsonify({
            'success': True,
            'transactions': transactions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/invoice/<transaction_id>', methods=['GET'])
def get_invoice(transaction_id):
    """Get invoice for a transaction."""
    try:
        result = payment_processor.generate_invoice(transaction_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/payment/cancel', methods=['POST'])
def cancel_subscription():
    """Cancel user subscription."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        result = payment_processor.cancel_subscription(user_id)
        
        if result['success']:
            # Update user to free plan
            email = data.get('email')
            if email:
                user_auth.update_user_plan(email, 'free', 'cancelled')
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Coupon Codes
# ============================================================================

@app.route('/api/coupons/validate', methods=['POST'])
def validate_coupon():
    """Validate a coupon code."""
    try:
        data = request.get_json()
        code = data.get('code')
        plan_id = data.get('plan_id')
        
        result = coupon_manager.validate_coupon(code, plan_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/coupons/apply', methods=['POST'])
def apply_coupon():
    """Apply coupon and get discounted price."""
    try:
        data = request.get_json()
        code = data.get('code')
        plan_id = data.get('plan_id')
        original_price = data.get('original_price')
        
        result = coupon_manager.apply_coupon(code, plan_id, original_price)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/coupons/list', methods=['GET'])
def list_coupons():
    """Get list of active public coupons."""
    try:
        result = coupon_manager.list_active_coupons()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/coupons/generate-referral', methods=['POST'])
def generate_referral():
    """Generate a referral code for user."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        code = coupon_manager.generate_referral_code(user_id)
        
        return jsonify({
            'success': True,
            'referral_code': code
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Real-Time Market Data
# ============================================================================

@app.route('/api/markets/canadian-stocks', methods=['GET'])
def get_canadian_stocks():
    """Get Canadian stock market data."""
    try:
        limit = int(request.args.get('limit', 20))
        stocks = realtime_data.get_canadian_stocks(limit)
        
        return jsonify({
            'success': True,
            'data': stocks,
            'total': len(stocks),
            'market': 'TSX',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/us-stocks', methods=['GET'])
def get_us_stocks():
    """Get US stock market data."""
    try:
        limit = int(request.args.get('limit', 50))
        stocks = realtime_data.get_us_stocks(limit)
        
        return jsonify({
            'success': True,
            'data': stocks,
            'total': len(stocks),
            'markets': ['NYSE', 'NASDAQ'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/all-crypto', methods=['GET'])
def get_all_crypto():
    """Get all cryptocurrency data."""
    try:
        limit = int(request.args.get('limit', 60))
        cryptos = realtime_data.get_all_crypto(limit)
        
        return jsonify({
            'success': True,
            'data': cryptos,
            'total': len(cryptos),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/defi-tokens', methods=['GET'])
def get_defi_tokens():
    """Get DeFi token data."""
    try:
        tokens = realtime_data.get_defi_tokens()
        
        return jsonify({
            'success': True,
            'data': tokens,
            'total': len(tokens),
            'category': 'DeFi',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/nft-tokens', methods=['GET'])
def get_nft_tokens():
    """Get NFT/Metaverse token data."""
    try:
        tokens = realtime_data.get_nft_tokens()
        
        return jsonify({
            'success': True,
            'data': tokens,
            'total': len(tokens),
            'category': 'NFT/Metaverse',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/summary', methods=['GET'])
def get_complete_market_summary():
    """Get comprehensive market summary."""
    try:
        summary = realtime_data.get_market_summary()
        
        return jsonify({
            'success': True,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/markets/search', methods=['GET'])
def search_markets():
    """Search markets by symbol or name."""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query required'
            }), 400
        
        results = realtime_data.search_symbol(query)
        
        return jsonify({
            'success': True,
            'results': results,
            'query': query,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - ASI1 AI Integration
# ============================================================================

@app.route('/api/ai/analyze-market', methods=['POST'])
def ai_analyze_market():
    """Analyze market data using ASI1 AI."""
    try:
        data = request.get_json()
        market_data = data.get('market_data', {})
        context = data.get('context', '')
        
        analysis = asi1_ai.analyze_market_with_ai(market_data, context)
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/whale-analysis', methods=['POST'])
def ai_whale_analysis():
    """Analyze whale transactions using AI."""
    try:
        data = request.get_json()
        whale_data = data.get('whale_data', {})
        
        analysis = asi1_ai.whale_watch_analysis(whale_data)
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/predict-price', methods=['POST'])
def ai_predict_price():
    """Predict price movement using AI."""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        historical_data = data.get('historical_data', [])
        
        prediction = asi1_ai.predict_price_movement(symbol, historical_data)
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/agent-communicate', methods=['POST'])
def ai_agent_communicate():
    """Communicate with ASI1 agent."""
    try:
        data = request.get_json()
        message = data.get('message')
        agent_context = data.get('context', {})
        
        response = asi1_ai.communicate_with_agent(message, agent_context)
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/market-summary', methods=['POST'])
def ai_market_summary():
    """Get AI-powered market summary."""
    try:
        data = request.get_json()
        markets = data.get('markets', {})
        
        summary = asi1_ai.get_ai_market_summary(markets)
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Advanced AI Intelligence System
# ============================================================================

@app.route('/api/ai-intelligence/comprehensive-scan', methods=['GET'])
def ai_comprehensive_scan():
    """Perform comprehensive AI market scan of all markets."""
    try:
        intelligence = ai_intelligence.comprehensive_market_scan()
        
        return jsonify({
            'success': True,
            'intelligence': intelligence,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai-intelligence/learn-and-predict', methods=['POST'])
def ai_learn_and_predict():
    """AI learns from all data and generates predictions."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        result = ai_intelligence.learn_and_predict(user_id)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai-intelligence/learning-stats', methods=['GET'])
def ai_learning_stats():
    """Get AI learning statistics."""
    try:
        stats = ai_intelligence.get_learning_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai-intelligence/market-predictions', methods=['GET'])
def get_market_predictions():
    """Get comprehensive market predictions from AI."""
    try:
        user_id = request.args.get('user_id')
        
        # Get predictions
        result = ai_intelligence.learn_and_predict(user_id)
        
        if result['success']:
            # Create notification for user if provided
            if user_id:
                notification_center.create_ai_insight(
                    user_id=user_id,
                    insight=f"New AI predictions available with {result['confidence_score']*100}% confidence",
                    symbol=None
                )
            
            return jsonify({
                'success': True,
                'predictions': result['predictions'],
                'recommendations': result['recommendations'],
                'confidence': result['confidence_score'],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Whale Watcher
# ============================================================================

@app.route('/api/whale/transactions', methods=['GET'])
def get_whale_transactions():
    """Get whale transactions (restricted access)."""
    try:
        user_id = request.args.get('user_id', '')
        user_plan = request.args.get('user_plan', 'free')
        limit = int(request.args.get('limit', 20))
        min_value = float(request.args.get('min_value', 100000))
        
        result = whale_watcher.get_whale_transactions(user_id, user_plan, limit, min_value)
        
        if not result['success']:
            return jsonify(result), 403
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/whale/track-wallet', methods=['POST'])
def track_whale_wallet():
    """Track a whale wallet (restricted access)."""
    try:
        data = request.get_json()
        user_id = data.get('user_id', '')
        user_plan = data.get('user_plan', 'free')
        wallet_address = data.get('wallet_address')
        label = data.get('label', '')
        
        result = whale_watcher.track_wallet(user_id, user_plan, wallet_address, label)
        
        if not result['success']:
            return jsonify(result), 403
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/whale/nft-movements', methods=['GET'])
def get_nft_whale_movements():
    """Get NFT whale movements (restricted access)."""
    try:
        user_id = request.args.get('user_id', '')
        user_plan = request.args.get('user_plan', 'free')
        limit = int(request.args.get('limit', 15))
        
        result = whale_watcher.get_nft_whale_movements(user_id, user_plan, limit)
        
        if not result['success']:
            return jsonify(result), 403
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/whale/statistics', methods=['GET'])
def get_whale_statistics():
    """Get whale activity statistics (restricted access)."""
    try:
        user_id = request.args.get('user_id', '')
        user_plan = request.args.get('user_plan', 'free')
        
        result = whale_watcher.get_whale_statistics(user_id, user_plan)
        
        if not result['success']:
            return jsonify(result), 403
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - Notifications
# ============================================================================

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Get user notifications."""
    try:
        user_id = request.args.get('user_id')
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 50))
        
        notifications = notification_center.get_user_notifications(user_id, unread_only, limit)
        stats = notification_center.get_notification_stats(user_id)
        
        return jsonify({
            'success': True,
            'notifications': notifications,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notifications/mark-read', methods=['POST'])
def mark_notification_read():
    """Mark notification as read."""
    try:
        data = request.get_json()
        notification_id = data.get('notification_id')
        
        success = notification_center.mark_as_read(notification_id)
        
        return jsonify({
            'success': success,
            'message': 'Notification marked as read' if success else 'Notification not found'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    """Mark all notifications as read for a user."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        count = notification_center.mark_all_as_read(user_id)
        
        return jsonify({
            'success': True,
            'marked_count': count,
            'message': f'{count} notifications marked as read'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notifications/delete', methods=['POST'])
def delete_notification():
    """Delete a notification."""
    try:
        data = request.get_json()
        notification_id = data.get('notification_id')
        
        success = notification_center.delete_notification(notification_id)
        
        return jsonify({
            'success': success,
            'message': 'Notification deleted' if success else 'Notification not found'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# API Routes - System
# ============================================================================

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status."""
    return jsonify({
        'success': True,
        'status': 'operational',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# Main
# ============================================================================

def main():
    """Run the Flask application."""
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("=" * 70)
    print("SignalTrust AI Market Scanner v2.0.0")
    print("=" * 70)
    print(f"Starting web server on http://localhost:{port}")
    print("Press CTRL+C to stop")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
