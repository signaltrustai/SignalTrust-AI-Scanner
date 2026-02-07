from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import requests
import datetime
import json
import threading
import time
from functools import wraps

# Import local modules
from user_auth import UserAuth
from payment_processor import PaymentProcessor
from market_scanner import MarketScanner
from market_analyzer import MarketAnalyzer
from ai_predictor import AIPredictor
from ai_market_intelligence import AIMarketIntelligence
from whale_watcher import WhaleWatcher
from notification_center import NotificationCenter
from realtime_market_data import RealTimeMarketData
from crypto_gem_finder import CryptoGemFinder
from universal_market_analyzer import UniversalMarketAnalyzer
from ai_chat_system import AIChatSystem

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
CORS(app)

# -----------------------------
# CONFIGURATION AGENTS SIGNALTRUST
# -----------------------------

AGENT_API_BASE_URL = os.getenv("AGENT_API_BASE_URL", "https://api.signaltrust.ai")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")

# IDs des agents (chargés depuis Render)
AGENT_IDS = {
    "STOCK": os.getenv("AGENT_STOCK_ID"),            # ASI1-STOCK-001
    "CRYPTO": os.getenv("AGENT_CRYPTO_ID"),          # ASI2-CRYPTO-002
    "WHALE": os.getenv("AGENT_WHALE_ID"),            # ASI3-WHALE-003
    "SITE": os.getenv("AGENT_SITE_ID"),              # ASI4-SITE-004
    "SUPERVISOR": os.getenv("AGENT_SUPERVISOR_ID"),  # ASI5-SUPERVISOR-005
    "DESIRE": os.getenv("DESIRE_AGENT_ID"),          # ASI6-DESIRE-006
}

LOG_FILE = "signaltrust_events.log"
LEARNING_DATA_FILE = "data/ai_learning_data.json"

# Initialize system components
user_auth = UserAuth()
payment_processor = PaymentProcessor()
market_scanner = MarketScanner()
market_analyzer = MarketAnalyzer()
ai_predictor = AIPredictor()
ai_intelligence = AIMarketIntelligence()
whale_watcher = WhaleWatcher()
notification_center = NotificationCenter()
realtime_data = RealTimeMarketData()
gem_finder = CryptoGemFinder()
universal_analyzer = UniversalMarketAnalyzer()

# Initialize ASI1 and AI Chat System with dependencies
from asi1_integration import ASI1AIIntegration
asi1_integration = ASI1AIIntegration()
ai_chat = AIChatSystem(asi1_integration, ai_intelligence, whale_watcher)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user."""
    if 'user_email' in session:
        return user_auth.get_user_by_email(session['user_email'])
    return None

def save_learning_data(data_type: str, data: dict):
    """Save learning data for AI improvement."""
    try:
        if not os.path.exists(os.path.dirname(LEARNING_DATA_FILE)):
            os.makedirs(os.path.dirname(LEARNING_DATA_FILE))
        
        # Load existing data
        learning_data = []
        if os.path.exists(LEARNING_DATA_FILE):
            try:
                with open(LEARNING_DATA_FILE, 'r') as f:
                    learning_data = json.load(f)
            except:
                learning_data = []
        
        # Add new entry
        learning_data.append({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "type": data_type,
            "data": data
        })
        
        # Keep last 10000 entries
        learning_data = learning_data[-10000:]
        
        # Save
        with open(LEARNING_DATA_FILE, 'w') as f:
            json.dump(learning_data, f)
    except Exception as e:
        log_event("LEARNING_DATA_ERROR", {"error": str(e)})

def log_event(event_type: str, payload: dict):
    """Enregistre les événements importants dans un fichier log."""
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "type": event_type,
        "data": payload,
    }
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass

def call_agent(agent_key: str, message: str):
    """Appelle un agent SignalTrust via son alias logique."""
    agent_id = AGENT_IDS.get(agent_key)
    if not agent_id:
        return {"error": f"Unknown agent key: {agent_key}"}

    url = f"{AGENT_API_BASE_URL}/agents/{agent_id}/run"
    headers = {
        "Authorization": f"Bearer {AGENT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"input": message}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def agent_router(message: str):
    """
    Router intelligent multi-agents pour :
    - marché actions
    - marché crypto
    - whales
    - gestion du site
    - supervision
    - liaison avec Desire
    """

    msg = message.lower()

    # --- Gestion du site + liaison Desire ---
    if "modifier le site" in msg or "change le site" in msg or "contenu du site" in msg:
        log_event("SITE_UPDATE_REQUEST", {"message": message})
        site_response = call_agent("SITE", message)
        try:
            call_agent("DESIRE", f"INFO_SITE_UPDATE: {message}")
        except Exception:
            pass
        return site_response

    if "parle avec desire" in msg or "desire" in msg or "désiré" in msg:
        log_event("DESIRE_INTERACTION", {"message": message})
        return call_agent("DESIRE", message)

    # --- Analyse marché actions ---
    if "stock" in msg or "bourse" in msg or "actions" in msg or "indice" in msg:
        log_event("MARKET_STOCK_QUERY", {"message": message})
        return call_agent("STOCK", message)

    # --- Analyse marché crypto ---
    if "crypto" in msg or "bitcoin" in msg or "btc" in msg or "eth" in msg or "altcoin" in msg:
        log_event("MARKET_CRYPTO_QUERY", {"message": message})
        return call_agent("CRYPTO", message)

    # --- Analyse whales ---
    if "whale" in msg or "gros mouvement" in msg or "on-chain" in msg or "onchain" in msg:
        log_event("MARKET_WHALE_QUERY", {"message": message})
        return call_agent("WHALE", message)

    # --- Sécurité / risque ---
    if "risque" in msg or "danger" in msg or "sécurité" in msg:
        log_event("SECURITY_CHECK", {"message": message})
        return call_agent("SUPERVISOR", f"[SECURITY_CHECK] {message}")

    # --- Fallback : superviseur ---
    log_event("SUPERVISOR_FALLBACK", {"message": message})
    return call_agent("SUPERVISOR", message)

# -----------------------------
# ROUTES FLASK - PAGE ROUTES
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ai-chat")
def ai_chat_page():
    return render_template("ai_chat.html")

@app.route("/scanner")
def scanner_page():
    return render_template("scanner.html")

@app.route("/analyzer")
def analyzer_page():
    return render_template("analyzer.html")

@app.route("/predictions")
def predictions_page():
    return render_template("predictions.html")

@app.route("/pricing")
def pricing_page():
    return render_template("pricing.html")

@app.route("/login")
def login():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template("login.html")

@app.route("/register")
def register():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    user = get_current_user()
    return render_template("dashboard.html", user=user)

@app.route("/settings")
@login_required
def settings():
    user = get_current_user()
    return render_template("settings.html", user=user)

@app.route("/payment")
def payment_page():
    return render_template("payment.html")

@app.route("/whale-watcher")
def whale_watcher_page():
    return render_template("whale_watcher.html")

@app.route("/ai-intelligence")
def ai_intelligence_page():
    return render_template("ai_intelligence.html")

@app.route("/notifications")
@login_required
def notifications_page():
    user = get_current_user()
    return render_template("notifications.html", user=user)

# -----------------------------
# API ROUTES - AUTHENTICATION
# -----------------------------

@app.route("/api/auth/register", methods=["POST"])
def api_register():
    """Register a new user."""
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        plan = data.get("plan", "free")
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        result = user_auth.register_user(email, password, full_name, plan)
        
        if result["success"]:
            log_event("USER_REGISTERED", {"email": email, "plan": plan})
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    """Login user."""
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        result = user_auth.login_user(email, password)
        
        if result["success"]:
            session['user_email'] = email
            session['session_token'] = result.get("session_token")
            log_event("USER_LOGIN", {"email": email})
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    """Logout user."""
    email = session.get('user_email')
    if email:
        log_event("USER_LOGOUT", {"email": email})
    session.clear()
    return jsonify({"success": True}), 200

@app.route("/api/auth/verify", methods=["GET"])
def api_verify():
    """Verify session."""
    if 'user_email' in session:
        user = get_current_user()
        if user:
            return jsonify({"authenticated": True, "user": {
                "email": user["email"],
                "full_name": user.get("full_name"),
                "plan": user.get("plan")
            }}), 200
    return jsonify({"authenticated": False}), 401

# -----------------------------
# API ROUTES - MARKET DATA
# -----------------------------

@app.route("/api/markets/overview", methods=["GET"])
def api_markets_overview():
    """Get markets overview."""
    try:
        overview = realtime_data.get_market_summary()
        save_learning_data("market_overview", overview)
        return jsonify({"success": True, "data": overview}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/markets/scan", methods=["POST"])
def api_markets_scan():
    """Scan specific markets."""
    try:
        data = request.get_json()
        market_type = data.get("market_type", "crypto")
        symbols = data.get("symbols", [])
        
        results = market_scanner.scan_market(market_type, symbols if symbols else [])
        
        save_learning_data("market_scan", {"type": market_type, "results": results})
        log_event("MARKET_SCAN", {"type": market_type})
        
        return jsonify({"success": True, "data": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/markets/trending", methods=["GET"])
def api_markets_trending():
    """Get trending assets."""
    try:
        market_type = request.args.get("market_type", "crypto")
        trending = market_scanner.get_trending_assets(market_type)
        return jsonify({"success": True, "data": trending}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - ANALYSIS
# -----------------------------

@app.route("/api/analyze/technical", methods=["POST"])
def api_analyze_technical():
    """Technical analysis."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        timeframe = data.get("timeframe", "1d")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        analysis = market_analyzer.analyze_technical(symbol, timeframe)
        save_learning_data("technical_analysis", {"symbol": symbol, "analysis": analysis})
        
        return jsonify({"success": True, "data": analysis}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/analyze/sentiment", methods=["POST"])
def api_analyze_sentiment():
    """Sentiment analysis."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        sentiment = market_analyzer.analyze_sentiment(symbol)
        save_learning_data("sentiment_analysis", {"symbol": symbol, "sentiment": sentiment})
        
        return jsonify({"success": True, "data": sentiment}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/analyze/patterns", methods=["POST"])
def api_analyze_patterns():
    """Pattern detection."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        patterns = market_analyzer.detect_patterns(symbol)
        save_learning_data("pattern_detection", {"symbol": symbol, "patterns": patterns})
        
        return jsonify({"success": True, "data": patterns}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - AI PREDICTIONS
# -----------------------------

@app.route("/api/predict/price", methods=["POST"])
def api_predict_price():
    """AI price predictions."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        days = data.get("days", 7)
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        prediction = ai_predictor.predict_price(symbol, days)
        save_learning_data("price_prediction", {"symbol": symbol, "prediction": prediction})
        log_event("AI_PREDICTION", {"symbol": symbol, "days": days})
        
        return jsonify({"success": True, "data": prediction}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/predict/signals", methods=["POST"])
def api_predict_signals():
    """AI trading signals."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        signals = ai_predictor.generate_signals(symbol)
        save_learning_data("trading_signals", {"symbol": symbol, "signals": signals})
        
        return jsonify({"success": True, "data": signals}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/predict/risk", methods=["POST"])
def api_predict_risk():
    """AI risk assessment."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        risk = ai_predictor.assess_risk(symbol)
        save_learning_data("risk_assessment", {"symbol": symbol, "risk": risk})
        
        return jsonify({"success": True, "data": risk}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - WHALE WATCHER
# -----------------------------

@app.route("/api/whale/transactions", methods=["GET"])
def api_whale_transactions():
    """Get whale transactions."""
    try:
        user = get_current_user()
        if not user or user.get("plan") not in ["pro", "enterprise"]:
            return jsonify({"success": False, "error": "Pro or Enterprise plan required"}), 403
        
        transactions = whale_watcher.get_recent_transactions()
        return jsonify({"success": True, "data": transactions}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/whale/alerts", methods=["GET"])
def api_whale_alerts():
    """Get whale alerts."""
    try:
        user = get_current_user()
        if not user or user.get("plan") not in ["pro", "enterprise"]:
            return jsonify({"success": False, "error": "Pro or Enterprise plan required"}), 403
        
        alerts = whale_watcher.get_whale_alerts()
        return jsonify({"success": True, "data": alerts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - PAYMENT
# -----------------------------

@app.route("/api/payment/plans", methods=["GET"])
def api_payment_plans():
    """Get subscription plans."""
    try:
        plans = payment_processor.get_plans()
        return jsonify({"success": True, "data": plans}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/payment/process", methods=["POST"])
def api_payment_process():
    """Process payment."""
    try:
        data = request.get_json()
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({"success": False, "error": "Authentication required"}), 401
        
        result = payment_processor.process_payment(
            user_email,
            data.get("plan"),
            data.get("payment_method"),
            data.get("card_details")
        )
        
        if result["success"]:
            log_event("PAYMENT_PROCESSED", {"email": user_email, "plan": data.get("plan")})
        
        return jsonify(result), 200 if result["success"] else 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/payment/validate-card", methods=["POST"])
def api_payment_validate_card():
    """Validate credit card."""
    try:
        data = request.get_json()
        card_number = data.get("card_number")
        
        if not card_number:
            return jsonify({"success": False, "error": "Card number required"}), 400
        
        result = payment_processor.validate_card_number(card_number)
        return jsonify({"success": True, "valid": result.get("valid", False)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - NOTIFICATIONS
# -----------------------------

@app.route("/api/notifications", methods=["GET"])
@login_required
def api_get_notifications():
    """Get user notifications."""
    try:
        user_email = session.get('user_email')
        notifications = notification_center.get_notifications(user_email)
        return jsonify({"success": True, "data": notifications}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/notifications/mark-read", methods=["POST"])
@login_required
def api_mark_notification_read():
    """Mark notification as read."""
    try:
        data = request.get_json()
        notification_id = data.get("notification_id")
        user_email = session.get('user_email')
        
        notification_center.mark_as_read(user_email, notification_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - CRYPTO GEMS & DISCOVERY
# -----------------------------

@app.route("/api/gems/discover", methods=["GET"])
def api_discover_gems():
    """Discover hidden gem cryptocurrencies."""
    try:
        limit = int(request.args.get("limit", 50))
        gems = gem_finder.discover_new_gems(limit=limit)
        
        save_learning_data("gems_discovered", {"count": len(gems), "gems": gems[:10]})
        log_event("GEMS_DISCOVERED", {"count": len(gems)})
        
        return jsonify({"success": True, "data": gems}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/gems/top", methods=["GET"])
def api_top_gems():
    """Get top-scored gem cryptocurrencies."""
    try:
        limit = int(request.args.get("limit", 10))
        gems = gem_finder.get_top_gems(limit=limit)
        return jsonify({"success": True, "data": gems}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/gems/analyze/<symbol>", methods=["GET"])
def api_analyze_gem(symbol):
    """Analyze explosion potential of a specific gem."""
    try:
        analysis = gem_finder.analyze_gem_potential(symbol)
        save_learning_data("gem_analysis", {"symbol": symbol, "analysis": analysis})
        return jsonify({"success": True, "data": analysis}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/gems/alerts", methods=["GET"])
def api_gem_alerts():
    """Get alerts for gems about to explode."""
    try:
        alerts = gem_finder.get_gem_alerts()
        return jsonify({"success": True, "data": alerts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - UNIVERSAL MARKET ANALYSIS
# -----------------------------

@app.route("/api/universal/analyze-all", methods=["GET"])
def api_analyze_all_markets():
    """Analyze ALL markets: stocks, crypto, NFTs, everything."""
    try:
        analysis = universal_analyzer.analyze_everything()
        
        save_learning_data("universal_analysis", {
            "total_assets": analysis['total_assets_analyzed'],
            "markets": len(analysis['markets'])
        })
        log_event("UNIVERSAL_ANALYSIS_COMPLETE", {
            "assets": analysis['total_assets_analyzed'],
            "opportunities": len(analysis['top_opportunities'])
        })
        
        return jsonify({"success": True, "data": analysis}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/universal/summary", methods=["GET"])
def api_universal_summary():
    """Get summary of latest universal analysis."""
    try:
        summary = universal_analyzer.get_analysis_summary()
        return jsonify({"success": True, "data": summary}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/universal/top-opportunities", methods=["GET"])
def api_top_opportunities():
    """Get top investment opportunities across ALL markets."""
    try:
        limit = int(request.args.get("limit", 50))
        summary = universal_analyzer.get_analysis_summary()
        opportunities = summary.get('top_opportunities', [])[:limit]
        return jsonify({"success": True, "data": opportunities}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """Route utilisée par ton interface AI Chat"""
    data = request.get_json()
    user_message = data.get("message", "")

    log_event("USER_MESSAGE", {"message": user_message})

    agent_response = agent_router(user_message)

    log_event("AGENT_RESPONSE", {"response": agent_response})

    return jsonify({"reply": agent_response})

# -----------------------------
# BACKGROUND WORKERS - 24/7 AI AGENTS
# -----------------------------

class BackgroundAIWorker:
    """24/7 Background AI worker for continuous learning and data collection."""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the background worker."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.thread.start()
            log_event("BACKGROUND_WORKER_STARTED", {"time": datetime.datetime.utcnow().isoformat()})
    
    def stop(self):
        """Stop the background worker."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        log_event("BACKGROUND_WORKER_STOPPED", {"time": datetime.datetime.utcnow().isoformat()})
    
    def _worker_loop(self):
        """Main worker loop - runs 24/7."""
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                log_event("WORKER_CYCLE", {"cycle": cycle_count})
                
                # 1. Collect market data every 5 minutes
                if cycle_count % 1 == 0:
                    self._collect_market_data()
                
                # 2. Run AI analysis every 15 minutes
                if cycle_count % 3 == 0:
                    self._run_ai_analysis()
                
                # 3. Check for whale activity every 10 minutes
                if cycle_count % 2 == 0:
                    self._check_whale_activity()
                
                # 4. Generate predictions every hour
                if cycle_count % 12 == 0:
                    self._generate_predictions()
                
                # 5. Discover hidden gems every 30 minutes
                if cycle_count % 6 == 0:
                    self._discover_hidden_gems()
                
                # 6. Analyze ALL markets every 2 hours
                if cycle_count % 24 == 0:
                    self._analyze_all_markets()
                
                # 7. Learn from collected data every 6 hours
                if cycle_count % 72 == 0:
                    self._learn_from_data()
                
                # 8. Health check and cleanup every 24 hours
                if cycle_count % 288 == 0:
                    self._health_check(cycle_count)
                
                # Sleep for 5 minutes between cycles
                time.sleep(300)
                
            except Exception as e:
                log_event("WORKER_ERROR", {"error": str(e), "cycle": cycle_count})
                time.sleep(60)  # Wait 1 minute on error
    
    def _collect_market_data(self):
        """Collect and save real-time market data."""
        try:
            # Get market summary
            summary = realtime_data.get_market_summary()
            save_learning_data("auto_market_data", summary)
            
            # Scan trending markets
            trending = market_scanner.get_trending_assets("crypto")
            save_learning_data("auto_trending", trending)
            
            log_event("AUTO_DATA_COLLECTION", {
                "summary": bool(summary),
                "trending": len(trending)
            })
        except Exception as e:
            log_event("DATA_COLLECTION_ERROR", {"error": str(e)})
    
    def _run_ai_analysis(self):
        """Run AI analysis on top assets."""
        try:
            # Get all crypto assets (no limit)
            top_assets = realtime_data.get_all_crypto(limit=None)
            
            analyses = []
            for asset in top_assets[:50]:  # Analyze top 50 instead of 10
                try:
                    analysis = market_analyzer.analyze_technical(asset["symbol"])
                    analyses.append({
                        "symbol": asset["symbol"],
                        "analysis": analysis
                    })
                except:
                    continue
            
            save_learning_data("auto_ai_analysis", analyses)
            log_event("AUTO_AI_ANALYSIS", {"analyzed": len(analyses)})
        except Exception as e:
            log_event("AI_ANALYSIS_ERROR", {"error": str(e)})
    
    def _check_whale_activity(self):
        """Check for whale transactions and alert."""
        try:
            transactions = whale_watcher.get_recent_transactions(limit=100)  # Increased from 20 to 100
            
            # Save whale data for learning
            save_learning_data("auto_whale_data", transactions)
            
            # Check for significant transactions
            significant = [t for t in transactions if t.get("value_usd", 0) > 1000000]
            
            if significant:
                log_event("AUTO_WHALE_ALERT", {
                    "count": len(significant),
                    "total_value": sum(t.get("value_usd", 0) for t in significant)
                })
                
                # Send notifications for major whale movements
                for tx in significant[:10]:  # Top 10 instead of 5
                    notification_center.send_whale_alert(
                        "all_pro_users",
                        tx.get("symbol"),
                        tx.get("value_usd"),
                        tx.get("type")
                    )
        except Exception as e:
            log_event("WHALE_CHECK_ERROR", {"error": str(e)})
    
    def _generate_predictions(self):
        """Generate AI predictions for popular assets."""
        try:
            # Get all assets (no limit)
            top_assets = realtime_data.get_all_crypto(limit=None)
            
            predictions = []
            for asset in top_assets[:30]:  # Top 30 instead of 10
                try:
                    prediction = ai_predictor.predict_price(asset["symbol"], days=7)
                    predictions.append({
                        "symbol": asset["symbol"],
                        "prediction": prediction
                    })
                except:
                    continue
            
            save_learning_data("auto_predictions", predictions)
            log_event("AUTO_PREDICTIONS", {"generated": len(predictions)})
        except Exception as e:
            log_event("PREDICTION_ERROR", {"error": str(e)})
    
    def _discover_hidden_gems(self):
        """Discover hidden gem cryptocurrencies every 30 minutes."""
        try:
            gems = gem_finder.discover_new_gems(limit=100)
            
            # Filter top gems
            top_gems = [g for g in gems if g.get('gem_score', 0) > 85]
            
            save_learning_data("auto_gem_discovery", {
                "total_discovered": len(gems),
                "top_gems": len(top_gems),
                "gems": top_gems[:10]
            })
            
            log_event("AUTO_GEM_DISCOVERY", {
                "discovered": len(gems),
                "high_potential": len(top_gems)
            })
            
            # Send alerts for exceptional gems
            alerts = gem_finder.get_gem_alerts()
            if alerts:
                for alert in alerts[:5]:
                    notification_center.send_notification(
                        "all_users",
                        "gem_alert",
                        f"💎 New Gem Alert: {alert['symbol']} - {alert['message']}"
                    )
        except Exception as e:
            log_event("GEM_DISCOVERY_ERROR", {"error": str(e)})
    
    def _analyze_all_markets(self):
        """Analyze ALL markets every 2 hours."""
        try:
            log_event("UNIVERSAL_ANALYSIS_START", {})
            
            analysis = universal_analyzer.analyze_everything()
            
            save_learning_data("auto_universal_analysis", {
                "total_assets": analysis['total_assets_analyzed'],
                "markets": len(analysis['markets']),
                "top_opportunities": len(analysis['top_opportunities'])
            })
            
            log_event("UNIVERSAL_ANALYSIS_COMPLETE", {
                "assets_analyzed": analysis['total_assets_analyzed'],
                "opportunities_found": len(analysis['top_opportunities']),
                "markets_covered": len(analysis['markets'])
            })
            
            # Send notifications for top opportunities
            top_opps = analysis['top_opportunities'][:10]
            if top_opps:
                notification_center.send_notification(
                    "all_users",
                    "market_opportunities",
                    f"🚀 {len(top_opps)} new top opportunities discovered across all markets!"
                )
        except Exception as e:
            log_event("UNIVERSAL_ANALYSIS_ERROR", {"error": str(e)})
    
    def _learn_from_data(self):
        """Learn and improve from collected data."""
        try:
            # Load learning data
            if not os.path.exists(LEARNING_DATA_FILE):
                return
            
            with open(LEARNING_DATA_FILE, 'r') as f:
                learning_data = json.load(f)
            
            # Analyze patterns
            market_patterns = [d for d in learning_data if d.get("type") == "auto_market_data"]
            prediction_accuracy = [d for d in learning_data if d.get("type") == "auto_predictions"]
            
            insights = {
                "total_data_points": len(learning_data),
                "market_samples": len(market_patterns),
                "predictions_made": len(prediction_accuracy),
                "learning_timestamp": datetime.datetime.utcnow().isoformat()
            }
            
            save_learning_data("auto_learning_insights", insights)
            log_event("AUTO_LEARNING", insights)
            
        except Exception as e:
            log_event("LEARNING_ERROR", {"error": str(e)})
    
    def _health_check(self, cycle_count):
        """Perform system health check and cleanup."""
        try:
            health = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "log_file_size": os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0,
                "learning_data_size": os.path.getsize(LEARNING_DATA_FILE) if os.path.exists(LEARNING_DATA_FILE) else 0,
                "uptime_hours": cycle_count * 5 / 60  # Approximate
            }
            
            # Cleanup old logs if too large (> 100MB)
            if health["log_file_size"] > 100 * 1024 * 1024:
                with open(LOG_FILE, 'r') as f:
                    lines = f.readlines()
                with open(LOG_FILE, 'w') as f:
                    f.writelines(lines[-10000:])  # Keep last 10000 lines
            
            log_event("AUTO_HEALTH_CHECK", health)
            
        except Exception as e:
            log_event("HEALTH_CHECK_ERROR", {"error": str(e)})

# Initialize background worker
background_worker = BackgroundAIWorker()

# -----------------------------
# LANCEMENT SERVEUR
# -----------------------------
if __name__ == "__main__":
    # Start background AI worker for 24/7 operation
    background_worker.start()
    log_event("SERVER_STARTED", {
        "host": "0.0.0.0",
        "port": 5000,
        "background_worker": "enabled"
    })
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    finally:
        background_worker.stop()
