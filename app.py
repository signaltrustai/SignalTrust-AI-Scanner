from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import datetime
import json
import threading
import time
from functools import wraps
import subprocess
import sys
import uuid
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
from total_market_data_collector import TotalMarketDataCollector
from ai_evolution_system import AIEvolutionSystem
from ai_communication_hub import ai_hub
from notification_ai import notification_ai
from ai_chat_system import AIChatSystem
from cloud_storage_manager import cloud_storage
from tradingview_manager import tradingview_manager
from signalai_strategy import signalai_strategy
from multi_ai_coordinator import get_coordinator
from ai_learning_system import get_learning_system

# Load environment variables from .env (if present)
load_dotenv()

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
total_collector = TotalMarketDataCollector()
ai_evolution = AIEvolutionSystem()
ai_coordinator = get_coordinator()
ai_learning = get_learning_system()

# Initialize ASI1 and AI Chat System with dependencies
from asi1_integration import ASI1AIIntegration
asi1_integration = ASI1AIIntegration()
ai_chat = AIChatSystem(asi1_integration, ai_intelligence, whale_watcher)

# Initialize OpenAI client (for ChatKit sessions)
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
except Exception:
    openai_client = None

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
            except Exception as e:
                log_event("LEARNING_DATA_LOAD_ERROR", {"error": str(e)})
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
    # If no AGENT_API_KEY provided, return a mocked response for local testing
    if not AGENT_API_KEY:
        log_event("AGENT_MOCK", {"agent": agent_key, "message": message})
        return {"success": True, "agent": agent_key, "reply": f"(mock) received: {message}"}

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
# ChatKit session endpoint (OpenAI)
# -----------------------------
@app.route("/api/chatkit/session", methods=["POST"])
def create_chatkit_session():
    """Create a ChatKit session via OpenAI and return a client_secret to the frontend.

    The server must NOT expose its API key. The returned `client_secret` is safe
    for the client to use with @openai/chatkit-react.
    """
    # Allow bypassing authentication for quick local testing when ALLOW_UNAUTH_TESTING=true
    allow_unauth = os.getenv('ALLOW_UNAUTH_TESTING', 'false').lower() in ('1', 'true')
    if not allow_unauth and 'user_email' not in session:
        return redirect(url_for('login'))

    if not openai_client:
        return jsonify({"error": "OpenAI client not configured on server"}), 500
    try:
        chatkit_session = openai_client.chatkit.sessions.create({})
        return jsonify({"client_secret": getattr(chatkit_session, 'client_secret', None)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    is_admin = user.get('user_id') == 'owner_admin_001' or \
               user.get('email', '').lower() == 'signaltrustai@gmail.com'
    return render_template("dashboard.html", user=user, is_admin=is_admin)


@app.route("/api/worker/status")
def api_worker_status():
    """Get background worker status."""
    try:
        status = background_worker.get_worker_status()
        coordinator_stats = ai_coordinator.get_stats()
        learning_summary = ai_learning.get_learning_summary()
        hub_status = ai_hub.get_status()
        return jsonify({
            "success": True,
            "worker": status,
            "coordinator": coordinator_stats,
            "learning": learning_summary,
            "hub": hub_status,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/settings")
@login_required
def settings():
    user = get_current_user()
    return render_template("settings.html", user=user)

# ---------------------------------------------------------------------------
#  USER PROFILE
# ---------------------------------------------------------------------------

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads", "avatars")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/profile")
@login_required
def profile_page():
    user = get_current_user()
    is_admin = user.get('user_id') == 'owner_admin_001' or \
               user.get('email', '').lower() == 'signaltrustai@gmail.com'
    return render_template("profile.html", user=user, is_admin=is_admin)

@app.route("/api/profile", methods=["GET"])
@login_required
def api_get_profile():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    return jsonify({"success": True, "user": user})

@app.route("/api/profile", methods=["POST"])
@login_required
def api_update_profile():
    """Update user profile info (full_name, phone, bio, location)."""
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    data = request.get_json() or {}
    result = user_auth.update_user_profile(user["email"], data)
    return jsonify(result)

@app.route("/api/profile/avatar", methods=["POST"])
@login_required
def api_upload_avatar():
    """Upload profile picture."""
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    if "avatar" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["avatar"]
    if file.filename == "" or not _allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type. Use PNG, JPG, GIF, or WEBP"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{user['user_id']}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Remove old avatar if exists
    old_pic = user.get("profile_picture", "")
    if old_pic:
        old_path = os.path.join(os.path.dirname(__file__), "static", old_pic.lstrip("/static/").lstrip("/"))
        if os.path.exists(old_path) and "uploads/avatars" in old_path:
            try:
                os.remove(old_path)
            except Exception:
                pass

    file.save(filepath)
    avatar_url = f"/static/uploads/avatars/{filename}"
    user_auth.update_user_profile(user["email"], {"profile_picture": avatar_url})

    return jsonify({"success": True, "avatar_url": avatar_url})

# ---------------------------------------------------------------------------
#  ADMIN COMMUNICATION HUB (admin only)
# ---------------------------------------------------------------------------

def _require_admin(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        user = get_current_user()
        if not user:
            return redirect(url_for('login'))
        is_admin = user.get('user_id') == 'owner_admin_001' or \
                   user.get('email', '').lower() == 'signaltrustai@gmail.com'
        if not is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route("/admin/comm-hub")
@_require_admin
def admin_comm_hub():
    user = get_current_user()
    return render_template("admin_comm_hub.html", user=user, is_admin=True)

@app.route("/api/admin/comm-hub/status")
@_require_admin
def api_comm_hub_status():
    """Get full communication hub status + messages + knowledge."""
    try:
        status = ai_hub.get_status()
        knowledge = ai_hub.get_all_knowledge()
        collective = ai_hub.get_collective_intelligence()

        # Get recent messages from each agent
        agents = ["STOCK", "CRYPTO", "WHALE", "SITE", "SUPERVISOR", "DESIRE",
                  "coordinator", "learning_system", "predictor"]
        all_messages = []
        for agent in agents:
            msgs = ai_hub.get_messages(agent, limit=20)
            all_messages.extend(msgs)
        all_messages.sort(key=lambda m: m.get("timestamp", ""), reverse=True)

        # Recent insights per type
        insight_types = ["market_insights", "patterns", "predictions",
                         "whale_intelligence", "gem_discoveries", "news_sentiment"]
        insights = {}
        for itype in insight_types:
            insights[itype] = ai_hub.get_recent_insights(itype, limit=10)

        # Coordinator stats
        coordinator_stats = ai_coordinator.get_stats()

        return jsonify({
            "success": True,
            "status": status,
            "knowledge_types": list(knowledge.keys()),
            "knowledge_summary": {k: len(v) if isinstance(v, list) else 1
                                  for k, v in knowledge.items()},
            "collective": collective,
            "messages": all_messages[:100],
            "insights": insights,
            "coordinator": coordinator_stats,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/comm-hub/send", methods=["POST"])
@_require_admin
def api_comm_hub_send():
    """Admin sends a message/directive to an AI agent."""
    data = request.get_json() or {}
    to_ai = data.get("to_ai", "ALL")
    msg_type = data.get("msg_type", "admin_directive")
    content = data.get("content", "")
    priority = int(data.get("priority", 1))

    if not content:
        return jsonify({"success": False, "error": "Content is required"}), 400

    try:
        msg_id = ai_hub.send_message(
            from_ai="ADMIN",
            to_ai=to_ai,
            message_type=msg_type,
            data={"content": content, "from": "admin_dashboard", "type": msg_type},
            priority=priority,
        )
        return jsonify({"success": True, "msg_id": msg_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/comm-hub/share-data", methods=["POST"])
@_require_admin
def api_comm_hub_share_data():
    """Admin shares data/instruction into the knowledge base."""
    data = request.get_json() or {}
    data_type = data.get("data_type", "market_insights")
    content = data.get("content", {})

    if not content:
        return jsonify({"success": False, "error": "Content is required"}), 400

    try:
        ai_hub.share_data("ADMIN", data_type, content)
        return jsonify({"success": True, "message": f"Data shared as {data_type}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/comm-hub/evolve", methods=["POST"])
@_require_admin
def api_comm_hub_evolve():
    """Trigger collective evolution."""
    try:
        result = ai_hub.evolve_collectively()
        return jsonify({"success": True, "evolution": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/comm-hub/backup", methods=["POST"])
@_require_admin
def api_comm_hub_backup():
    """Create a backup of all hub data."""
    try:
        backup_path = ai_hub.create_backup()
        return jsonify({"success": True, "backup_path": backup_path})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/payment")
def payment_page():
    return render_template("payment.html")

@app.route("/whale-watcher")
def whale_watcher_page():
    return render_template("whale_watcher.html")

@app.route("/ai-intelligence")
def ai_intelligence_page():
    return render_template("ai_intelligence.html")

@app.route("/tradingview")
def tradingview_page():
    """TradingView charts page with SignalAI strategy"""
    return render_template("tradingview.html")

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

# Convenience aliases for common API paths
@app.route("/api/login", methods=["POST"])
def api_login_alias():
    """Alias for /api/auth/login."""
    return api_login()

@app.route("/api/register", methods=["POST"])
def api_register_alias():
    """Alias for /api/auth/register."""
    return api_register()

@app.route("/api/markets/analyze", methods=["POST"])
def api_markets_analyze_alias():
    """Alias for /api/analyze/technical."""
    return api_analyze_technical()

@app.route("/api/ai/predict", methods=["POST"])
def api_ai_predict_alias():
    """Alias for /api/predict/price."""
    return api_predict_price()

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
    """Technical analysis — uses multi-AI coordinator when available."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        timeframe = data.get("timeframe", "1d")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        analysis = market_analyzer.analyze_technical(symbol, timeframe)
        save_learning_data("technical_analysis", {"symbol": symbol, "analysis": analysis})

        # Record prediction in learning system
        direction = "BULLISH" if analysis.get("recommendation") == "BUY" else (
            "BEARISH" if analysis.get("recommendation") == "SELL" else "NEUTRAL"
        )
        confidence = (analysis.get("confidence", 50) or 50) / 100.0
        ai_learning.record_prediction(
            symbol=symbol,
            ai_worker="market_analyzer",
            strategy="technical",
            predicted_direction=direction,
            confidence=confidence,
            market_data_snapshot=analysis.get("indicators"),
        )
        
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

# -----------------------------
# API ROUTES - TOTAL DATA COLLECTION & AI EVOLUTION
# -----------------------------

@app.route("/api/total/collect-all", methods=["GET"])
def api_collect_all_data():
    """Collect ALL data from ALL markets - complete sweep."""
    try:
        log_event("TOTAL_DATA_COLLECTION_START", {})
        data = total_collector.collect_all_data()
        
        save_learning_data("total_collection", {
            "total_assets": data['data']['cryptocurrencies']['total_cryptos'] + 
                           data['data']['us_stocks']['total_stocks'] +
                           data['data']['canadian_stocks']['total_stocks'] +
                           data['data']['nfts']['total_collections']
        })
        
        return jsonify({"success": True, "data": {
            "timestamp": data['timestamp'],
            "total_cryptos": data['data']['cryptocurrencies']['total_cryptos'],
            "total_us_stocks": data['data']['us_stocks']['total_stocks'],
            "total_canadian_stocks": data['data']['canadian_stocks']['total_stocks'],
            "total_nfts": data['data']['nfts']['total_collections'],
            "total_whale_txs": data['data']['whales']['total_transactions'],
            "total_news": data['data']['news']['total_articles']
        }}), 200
    except Exception as e:
        log_event("TOTAL_COLLECTION_ERROR", {"error": str(e)})
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/total/coverage", methods=["GET"])
def api_total_coverage():
    """Get total market coverage statistics."""
    try:
        coverage = total_collector.get_total_coverage()
        return jsonify({"success": True, "data": coverage}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/evolve", methods=["POST"])
def api_ai_evolve():
    """Trigger AI evolution - learn from all collected data."""
    try:
        log_event("AI_EVOLUTION_START", {})
        report = ai_evolution.evolve()
        
        save_learning_data("ai_evolution", report)
        log_event("AI_EVOLUTION_COMPLETE", {
            "new_level": report.get('new_level'),
            "iq": report.get('intelligence_metrics', {}).get('overall_iq')
        })
        
        return jsonify({"success": True, "data": report}), 200
    except Exception as e:
        log_event("AI_EVOLUTION_ERROR", {"error": str(e)})
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/status", methods=["GET"])
def api_ai_status():
    """Get current AI evolution status."""
    try:
        status = ai_evolution.get_ai_status()
        return jsonify({"success": True, "data": status}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/predict-enhanced/<asset>", methods=["GET"])
def api_ai_predict_enhanced(asset):
    """Get AI-enhanced predictions using evolved intelligence."""
    try:
        asset_type = request.args.get("type", "crypto")
        prediction = ai_evolution.get_predictions_with_ai(asset, asset_type)
        
        save_learning_data("enhanced_prediction", {
            "asset": asset,
            "prediction": prediction
        })
        
        return jsonify({"success": True, "data": prediction}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - MULTI-AI COORDINATOR
# -----------------------------

@app.route("/api/ai/coordinator/status", methods=["GET"])
def api_coordinator_status():
    """Get multi-AI coordinator status and worker info."""
    try:
        return jsonify({
            "success": True,
            "workers": ai_coordinator.get_workers_status(),
            "stats": ai_coordinator.get_stats(),
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/coordinator/analyze", methods=["POST"])
def api_coordinator_analyze():
    """Run coordinated multi-AI analysis on a symbol."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        strategy = data.get("strategy")  # None → auto
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400

        result = ai_coordinator.quick_analysis(symbol, data)
        save_learning_data("coordinator_analysis", {"symbol": symbol, "result": result})

        # Record in learning system
        direction = result.get("analysis", {}).get("direction", "NEUTRAL")
        confidence = result.get("analysis", {}).get("confidence", 0.5)
        ai_learning.record_prediction(
            symbol=symbol,
            ai_worker=result.get("worker_used", "coordinator"),
            strategy=result.get("strategy_used", "auto"),
            predicted_direction=direction,
            confidence=confidence,
            market_data_snapshot=data,
        )

        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/coordinator/deep", methods=["POST"])
def api_coordinator_deep():
    """Run deep multi-AI analysis (slower, more accurate)."""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400

        result = ai_coordinator.deep_analysis(symbol, data)
        save_learning_data("deep_analysis", {"symbol": symbol, "result": result})
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - AI LEARNING SYSTEM
# -----------------------------

@app.route("/api/ai/learning/summary", methods=["GET"])
def api_learning_summary():
    """Get AI learning system summary."""
    try:
        return jsonify({"success": True, "data": ai_learning.get_learning_summary()}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/learning/model-accuracy", methods=["GET"])
def api_model_accuracy():
    """Get per-model accuracy stats."""
    try:
        worker = request.args.get("worker")
        return jsonify({"success": True, "data": ai_learning.get_model_accuracy(worker)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/learning/symbol/<symbol>", methods=["GET"])
def api_symbol_insights(symbol):
    """Get learning insights for a specific symbol."""
    try:
        return jsonify({"success": True, "data": ai_learning.get_symbol_insights(symbol)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai/learning/evolve", methods=["POST"])
def api_learning_evolve():
    """Trigger daily learning evolution cycle."""
    try:
        report = ai_learning.daily_evolution(coordinator=ai_coordinator)
        return jsonify({"success": True, "data": report}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - AI CHAT SYSTEM
# -----------------------------

@app.route("/api/ai-chat/modes", methods=["GET"])
def api_ai_chat_modes():
    """Get available AI chat modes."""
    try:
        modes = ai_chat.get_ai_modes()
        return jsonify({"success": True, "modes": modes}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai-chat/message", methods=["POST"])
def api_ai_chat_message():
    """Process AI chat message."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        ai_mode = data.get('mode', 'auto')
        
        # Get user info from session
        user = get_current_user()
        user_id = user.get('id', 'anonymous') if user else 'anonymous'
        user_email = user.get('email') if user else None
        
        # Process chat message
        response = ai_chat.chat(
            user_id=user_id,
            message=message,
            ai_mode=ai_mode,
            user_email=user_email
        )
        
        # Log successful chat
        if response.get('success'):
            log_event("AI_CHAT_MESSAGE", {
                "user_id": user_id,
                "ai_type": response.get('ai_type'),
                "message_length": len(message)
            })
        
        return jsonify(response), 200
    except Exception as e:
        log_event("AI_CHAT_ERROR", {"error": str(e)})
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to process chat message"
        }), 500

@app.route("/api/ai-chat/history", methods=["GET"])
def api_ai_chat_history():
    """Get conversation history."""
    try:
        user = get_current_user()
        user_id = user.get('id', 'anonymous') if user else 'anonymous'
        
        history = ai_chat.get_conversation_history(user_id)
        return jsonify({"success": True, "history": history}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ai-chat/clear-history", methods=["POST"])
def api_ai_chat_clear_history():
    """Clear conversation history."""
    try:
        user = get_current_user()
        user_id = user.get('id', 'anonymous') if user else 'anonymous'
        
        ai_chat.clear_history(user_id)
        log_event("AI_CHAT_HISTORY_CLEARED", {"user_id": user_id})
        return jsonify({"success": True, "message": "History cleared"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - AI HUB & COMMUNICATION
# -----------------------------

@app.route("/api/hub/status", methods=["GET"])
def api_hub_status():
    """Get AI communication hub status."""
    try:
        status = ai_hub.get_status()
        return jsonify({"success": True, "data": status}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/hub/knowledge", methods=["GET"])
def api_hub_knowledge():
    """Get all shared knowledge from AI hub."""
    try:
        knowledge = ai_hub.get_all_knowledge()
        return jsonify({"success": True, "data": knowledge}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/hub/collective-intelligence", methods=["GET"])
def api_collective_intelligence():
    """Get collective intelligence metrics."""
    try:
        collective = ai_hub.get_collective_intelligence()
        return jsonify({"success": True, "data": collective}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/hub/backup", methods=["POST"])
def api_create_backup():
    """Create manual backup of all AI data."""
    try:
        backup_file = ai_hub.create_backup()
        log_event("MANUAL_BACKUP_CREATED", {"file": backup_file})
        return jsonify({"success": True, "backup_file": backup_file}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - NOTIFICATION AI
# -----------------------------

@app.route("/api/notifications-ai/config", methods=["GET"])
def api_notification_ai_config():
    """Get Notification AI configuration."""
    try:
        config = notification_ai.get_config()
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/notifications-ai/configure", methods=["POST"])
def api_configure_notifications():
    """Configure notification preferences."""
    try:
        data = request.get_json()
        result = notification_ai.configure(data)
        log_event("NOTIFICATION_CONFIG_UPDATED", {"keys": list(data.keys())})
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/notifications-ai/send", methods=["POST"])
def api_send_intelligent_notification():
    """Send intelligent notification through AI."""
    try:
        data = request.get_json()
        notification_type = data.get("type")
        notification_data = data.get("data", {})
        
        result = notification_ai.send_notification(notification_type, notification_data)
        
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/notifications-ai/mark-read/<notification_id>", methods=["POST"])
def api_mark_notification_read_ai(notification_id):
    """Mark notification as read."""
    try:
        notification_ai.mark_read(notification_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/notifications-ai/feedback", methods=["POST"])
def api_notification_feedback():
    """Provide feedback on notification."""
    try:
        data = request.get_json()
        notification_type = data.get("type")
        feedback = data.get("feedback")  # positive, negative, neutral
        
        notification_ai.learn_from_feedback(notification_type, feedback)
        
        return jsonify({"success": True, "message": "Feedback recorded"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# API ROUTES - CLOUD STORAGE
# -----------------------------

@app.route("/api/cloud/status", methods=["GET"])
def api_cloud_status():
    """Get cloud storage status and statistics."""
    try:
        stats = cloud_storage.get_statistics()
        recent_backups = cloud_storage.list_backups(limit=10)
        
        return jsonify({
            "success": True,
            "statistics": stats,
            "recent_backups": recent_backups
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/cloud/backup", methods=["POST"])
def api_cloud_backup():
    """Create unified backup of all AI data."""
    try:
        log_event("CLOUD_BACKUP_START", {})
        
        backup = cloud_storage.backup_all_data()
        
        log_event("CLOUD_BACKUP_COMPLETE", {
            "backup_id": backup['backup_id'],
            "size_mb": backup['size_bytes'] / 1024 / 1024
        })
        
        return jsonify({
            "success": True,
            "backup": backup
        }), 200
    except Exception as e:
        log_event("CLOUD_BACKUP_ERROR", {"error": str(e)})
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/cloud/sync", methods=["POST"])
def api_cloud_sync():
    """Sync backup(s) to cloud storage."""
    try:
        data = request.get_json() or {}
        backup_id = data.get("backup_id")
        
        log_event("CLOUD_SYNC_START", {"backup_id": backup_id})
        
        results = cloud_storage.sync_to_cloud(backup_id)
        
        log_event("CLOUD_SYNC_COMPLETE", results)
        
        return jsonify({
            "success": True,
            "results": results
        }), 200
    except Exception as e:
        log_event("CLOUD_SYNC_ERROR", {"error": str(e)})
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/cloud/backups", methods=["GET"])
def api_cloud_list_backups():
    """List available backups."""
    try:
        limit = int(request.args.get("limit", 20))
        backups = cloud_storage.list_backups(limit=limit)
        
        return jsonify({
            "success": True,
            "backups": backups,
            "total": len(backups)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/cloud/backup/<backup_id>", methods=["GET"])
def api_cloud_get_backup(backup_id):
    """Get specific backup data."""
    try:
        from_cloud = request.args.get("from_cloud", "false").lower() == "true"
        
        data = cloud_storage.get_backup(backup_id, from_cloud=from_cloud)
        
        if data:
            # Don't return full data (too large), return metadata and structure
            response = {
                "backup_id": data.get('backup_id'),
                "timestamp": data.get('timestamp'),
                "version": data.get('version'),
                "metadata": data.get('metadata'),
                "data_sources": {
                    k: f"{len(v)} items" if isinstance(v, (list, dict)) else "data"
                    for k, v in data.get('data_sources', {}).items()
                }
            }
            
            return jsonify({
                "success": True,
                "backup": response
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Backup not found"
            }), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/cloud/query", methods=["POST"])
def api_cloud_query_backups():
    """Query backups with filters."""
    try:
        data = request.get_json() or {}
        filters = data.get("filters", {})
        
        backups = cloud_storage.query_backups(**filters)
        
        return jsonify({
            "success": True,
            "backups": backups,
            "total": len(backups)
        }), 200
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
# API ROUTES - TRADINGVIEW & SIGNALAI
# -----------------------------

@app.route("/api/tradingview/symbols", methods=["GET"])
def api_tradingview_symbols():
    """Get available TradingView symbols"""
    try:
        category = request.args.get("category", "all")
        symbols = tradingview_manager.get_popular_symbols(category)
        return jsonify({"success": True, "symbols": symbols}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/tradingview/search", methods=["POST"])
def api_tradingview_search():
    """Search TradingView symbols"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        limit = data.get("limit", 10)
        
        results = tradingview_manager.search_symbols(query, limit)
        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/signalai/generate", methods=["POST"])
def api_signalai_generate():
    """Generate SignalAI trading signals"""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        strategy = data.get("strategy", "SignalAI")
        
        if not symbol:
            return jsonify({"success": False, "error": "Symbol required"}), 400
        
        # Check access for SignalAI strategy
        if strategy == "SignalAI":
            user = get_current_user()
            if not user:
                return jsonify({"success": False, "error": "Login required"}), 401
            
            # Check if user is admin
            is_admin = user.get('user_id') == 'owner_admin_001' or user.get('email', '').lower() == 'signaltrustai@gmail.com'
            
            access = payment_processor.check_signalai_access(
                user.get('user_id', ''),
                user.get('email', ''),
                is_admin,
                user.get('plan', 'free')  # Pass user's plan
            )
            
            if not access['has_access']:
                return jsonify({
                    "success": False, 
                    "error": "SignalAI subscription required",
                    "requires_subscription": True
                }), 403
        
        # Generate signals
        signal = signalai_strategy.generate_signals(symbol, strategy)
        
        log_event("SIGNALAI_SIGNAL_GENERATED", {
            "symbol": symbol,
            "strategy": strategy,
            "signal": signal.get("signal")
        })
        
        return jsonify({"success": True, "signal": signal}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/signalai/check-access", methods=["POST"])
def api_signalai_check_access():
    """Check SignalAI subscription access"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"has_access": False, "reason": "Not logged in"}), 200
        
        # Check if user is admin
        is_admin = user.get('user_id') == 'owner_admin_001' or user.get('email', '').lower() == 'signaltrustai@gmail.com'
        
        access = payment_processor.check_signalai_access(
            user.get('user_id', ''),
            user.get('email', ''),
            is_admin,
            user.get('plan', 'free')  # Pass user's plan
        )
        
        return jsonify(access), 200
    except Exception as e:
        return jsonify({"has_access": False, "error": str(e)}), 500

@app.route("/api/signalai/start-trial", methods=["POST"])
def api_signalai_start_trial():
    """Start SignalAI 3-day free trial"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"success": False, "error": "Login required"}), 401
        
        result = payment_processor.start_signalai_trial(
            user.get('user_id', ''),
            user.get('email', '')
        )
        
        if result['success']:
            log_event("SIGNALAI_TRIAL_STARTED", {
                "user_id": user.get('user_id'),
                "email": user.get('email')
            })
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/signalai/subscribe", methods=["POST"])
def api_signalai_subscribe():
    """Subscribe to SignalAI strategy"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({"success": False, "error": "Login required"}), 401
        
        data = request.get_json()
        payment_method = data.get("payment_method", {})
        
        result = payment_processor.process_payment(
            user.get('user_id', ''),
            user.get('email', ''),
            'signalai',
            payment_method
        )
        
        if result['success']:
            log_event("SIGNALAI_SUBSCRIPTION", {
                "user_id": user.get('user_id'),
                "email": user.get('email')
            })
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/signalai/strategies", methods=["GET"])
def api_signalai_strategies():
    """Get available SignalAI strategies"""
    try:
        strategies = signalai_strategy.get_available_strategies()
        return jsonify({"success": True, "strategies": strategies}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/signalai/history", methods=["POST"])
def api_signalai_history():
    """Get SignalAI signal history"""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        limit = data.get("limit", 50)
        
        history = signalai_strategy.get_signal_history(symbol, limit)
        return jsonify({"success": True, "history": history}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/signalai/performance", methods=["POST"])
def api_signalai_performance():
    """Get SignalAI performance statistics"""
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        
        stats = signalai_strategy.get_performance_stats(symbol)
        return jsonify({"success": True, "stats": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# BACKGROUND WORKERS - 24/7 AI AGENTS (Optimized v2)
# -----------------------------

class BackgroundAIWorker:
    """
    24/7 Background AI worker with:
    - Exponential backoff on errors (max 10 min)
    - Per-task error isolation (one task failing doesn't stop others)
    - Health monitoring with auto-restart
    - Optimized cycle intervals
    - Data persistence saving on shutdown
    """

    CYCLE_INTERVAL = 300  # 5 minutes base cycle

    def __init__(self):
        self.running = False
        self.thread = None
        self.cycle_count = 0
        self.consecutive_errors = 0
        self.max_backoff = 600  # 10 minutes max
        self.start_time = None
        self.last_successful_cycle = None
        self.task_stats = {}  # task_name -> {success, fail, last_run}

    def start(self):
        """Start the background worker with auto-restart capability."""
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.thread.start()
            log_event("BACKGROUND_WORKER_STARTED", {
                "time": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })

    def stop(self):
        """Stop the background worker and save all data."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
        # Save all learning data on shutdown
        try:
            ai_learning.save_all()
            ai_hub.save_all()
        except Exception:
            pass
        log_event("BACKGROUND_WORKER_STOPPED", {
            "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total_cycles": self.cycle_count,
            "uptime_hours": round((time.time() - (self.start_time or time.time())) / 3600, 1)
        })

    def get_worker_status(self) -> dict:
        """Get detailed worker status for dashboard."""
        uptime = time.time() - (self.start_time or time.time())
        return {
            "running": self.running,
            "cycle_count": self.cycle_count,
            "uptime_hours": round(uptime / 3600, 1),
            "consecutive_errors": self.consecutive_errors,
            "last_successful_cycle": self.last_successful_cycle,
            "task_stats": self.task_stats,
        }

    def _run_task(self, name: str, fn, *args):
        """Run a single task with error isolation and stats tracking."""
        t0 = time.time()
        try:
            fn(*args)
            elapsed = round(time.time() - t0, 1)
            self.task_stats.setdefault(name, {"success": 0, "fail": 0, "last_run": None, "avg_time": 0})
            stats = self.task_stats[name]
            stats["success"] += 1
            stats["last_run"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            # Running average
            total = stats["success"] + stats["fail"]
            stats["avg_time"] = round((stats["avg_time"] * (total - 1) + elapsed) / total, 1)
        except Exception as e:
            self.task_stats.setdefault(name, {"success": 0, "fail": 0, "last_run": None, "avg_time": 0})
            self.task_stats[name]["fail"] += 1
            log_event(f"TASK_ERROR_{name.upper()}", {"error": str(e)})

    def _worker_loop(self):
        """Main worker loop — runs 24/7 with exponential backoff on errors."""
        while self.running:
            try:
                self.cycle_count += 1
                cycle_start = time.time()

                # ── Every cycle (5 min): market data ──
                self._run_task("market_data", self._collect_market_data)

                # ── Every 10 min: whale activity ──
                if self.cycle_count % 2 == 0:
                    self._run_task("whale_check", self._check_whale_activity)

                # ── Every 15 min: AI analysis ──
                if self.cycle_count % 3 == 0:
                    self._run_task("ai_analysis", self._run_ai_analysis)

                # ── Every 30 min: gem discovery ──
                if self.cycle_count % 6 == 0:
                    self._run_task("gem_discovery", self._discover_hidden_gems)

                # ── Every hour: predictions ──
                if self.cycle_count % 12 == 0:
                    self._run_task("predictions", self._generate_predictions)

                # ── Every 2 hours: universal analysis ──
                if self.cycle_count % 24 == 0:
                    self._run_task("universal_analysis", self._analyze_all_markets)

                # ── Every 4 hours: total data collection ──
                if self.cycle_count % 48 == 0:
                    self._run_task("total_collection", self._collect_total_data)

                # ── Every 6 hours: AI evolution + learning ──
                if self.cycle_count % 72 == 0:
                    self._run_task("ai_evolution", self._evolve_ai)
                    self._run_task("ai_learning", self._learn_from_data)

                # ── Every 12 hours: save all persistent data ──
                if self.cycle_count % 144 == 0:
                    self._run_task("data_save", self._save_all_data)

                # ── Every 24 hours: health check + cleanup ──
                if self.cycle_count % 288 == 0:
                    self._run_task("health_check", self._health_check, self.cycle_count)

                # Success — reset backoff
                self.consecutive_errors = 0
                self.last_successful_cycle = datetime.datetime.now(datetime.timezone.utc).isoformat()

                cycle_time = time.time() - cycle_start
                log_event("WORKER_CYCLE_COMPLETE", {
                    "cycle": self.cycle_count,
                    "duration_seconds": round(cycle_time, 1)
                })

                time.sleep(self.CYCLE_INTERVAL)

            except Exception as e:
                self.consecutive_errors += 1
                backoff = min(self.max_backoff, 60 * (2 ** min(self.consecutive_errors - 1, 4)))
                log_event("WORKER_ERROR", {
                    "error": str(e),
                    "cycle": self.cycle_count,
                    "consecutive_errors": self.consecutive_errors,
                    "backoff_seconds": backoff
                })
                time.sleep(backoff)

    def _collect_market_data(self):
        """Collect and save real-time market data."""
        summary = realtime_data.get_market_summary()
        save_learning_data("auto_market_data", summary)

        trending = market_scanner.get_trending_assets("crypto")
        save_learning_data("auto_trending", trending)

        ai_hub.share_data("MarketScanner", "market_insights", {
            "summary": summary,
            "trending": trending,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })

        log_event("AUTO_DATA_COLLECTION", {
            "summary": bool(summary),
            "trending": len(trending)
        })

    def _run_ai_analysis(self):
        """Run AI analysis on top assets."""
        top_assets = realtime_data.get_all_crypto(limit=None)

        analyses = []
        for asset in top_assets[:50]:
            try:
                analysis = market_analyzer.analyze_technical(asset["symbol"])
                analyses.append({"symbol": asset["symbol"], "analysis": analysis})
            except Exception:
                continue

        save_learning_data("auto_ai_analysis", analyses)
        ai_hub.share_data("Analyzer", "patterns", analyses)
        log_event("AUTO_AI_ANALYSIS", {"analyzed": len(analyses)})

    def _check_whale_activity(self):
        """Check for whale transactions and alert."""
        transactions = whale_watcher.get_recent_transactions(limit=100)
        save_learning_data("auto_whale_data", transactions)

        significant = [t for t in transactions if t.get("value_usd", 0) > 1000000]
        ai_hub.share_data("WhaleWatcher", "whale_intelligence", {
            "total_transactions": len(transactions),
            "significant_count": len(significant),
            "total_value": sum(t.get("value_usd", 0) for t in significant)
        })

        if significant:
            log_event("AUTO_WHALE_ALERT", {
                "count": len(significant),
                "total_value": sum(t.get("value_usd", 0) for t in significant)
            })
            for tx in significant[:10]:
                notification_center.send_whale_alert(
                    "all_pro_users",
                    tx.get("symbol"),
                    tx.get("value_usd"),
                    tx.get("type")
                )

    def _generate_predictions(self):
        """Generate AI predictions for popular assets."""
        top_assets = realtime_data.get_all_crypto(limit=None)

        predictions = []
        for asset in top_assets[:30]:
            try:
                prediction = ai_predictor.predict_price(asset["symbol"], days=7)
                predictions.append({"symbol": asset["symbol"], "prediction": prediction})
            except Exception:
                continue

        save_learning_data("auto_predictions", predictions)
        ai_hub.share_data("Predictor", "predictions", predictions)
        log_event("AUTO_PREDICTIONS", {"generated": len(predictions)})

    def _discover_hidden_gems(self):
        """Discover hidden gem cryptocurrencies."""
        gems = gem_finder.discover_new_gems(limit=100)
        top_gems = [g for g in gems if g.get('gem_score', 0) > 85]

        save_learning_data("auto_gem_discovery", {
            "total_discovered": len(gems),
            "top_gems": len(top_gems),
            "gems": top_gems[:10]
        })

        ai_hub.share_data("GemFinder", "gem_discoveries", top_gems)
        ai_hub.send_message("GemFinder", "ALL", "gem_discovery", {
            "total_gems": len(gems),
            "high_potential": len(top_gems)
        })

        log_event("AUTO_GEM_DISCOVERY", {
            "discovered": len(gems),
            "high_potential": len(top_gems)
        })

        alerts = gem_finder.get_gem_alerts()
        if alerts:
            for alert in alerts[:5]:
                notification_center.send_notification(
                    "all_users", "gem_alert",
                    f"New Gem Alert: {alert['symbol']} - {alert['message']}"
                )

    def _analyze_all_markets(self):
        """Analyze ALL markets."""
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

        top_opps = analysis['top_opportunities'][:10]
        if top_opps:
            notification_center.send_notification(
                "all_users", "market_opportunities",
                f"{len(top_opps)} new top opportunities discovered across all markets!"
            )

    def _collect_total_data(self):
        """Collect EVERYTHING from ALL markets."""
        log_event("TOTAL_COLLECTION_START", {})
        data = total_collector.collect_all_data()

        save_learning_data("auto_total_collection", {
            "total_cryptos": data['data']['cryptocurrencies']['total_cryptos'],
            "total_us_stocks": data['data']['us_stocks']['total_stocks'],
            "total_canadian_stocks": data['data']['canadian_stocks']['total_stocks'],
            "total_nfts": data['data']['nfts']['total_collections'],
            "total_whales": data['data']['whales']['total_transactions'],
            "total_news": data['data']['news']['total_articles']
        })

        total_assets = (data['data']['cryptocurrencies']['total_cryptos'] +
                      data['data']['us_stocks']['total_stocks'] +
                      data['data']['canadian_stocks']['total_stocks'] +
                      data['data']['nfts']['total_collections'])

        log_event("TOTAL_COLLECTION_COMPLETE", {
            "total_assets_collected": total_assets,
            "whale_transactions": data['data']['whales']['total_transactions'],
            "news_articles": data['data']['news']['total_articles']
        })

    def _evolve_ai(self):
        """Evolve AI using all collected data."""
        log_event("AUTO_AI_EVOLUTION_START", {})
        shared_knowledge = ai_hub.get_all_knowledge()
        report = ai_evolution.evolve()
        collective = ai_hub.evolve_collectively()

        save_learning_data("auto_ai_evolution", {
            "evolution_level": report.get('new_level'),
            "intelligence_iq": report.get('intelligence_metrics', {}).get('overall_iq'),
            "prediction_accuracy": report.get('prediction_accuracy', {}).get('overall'),
            "collective_iq": collective['collective_iq'],
            "collective_accuracy": collective['collective_accuracy'],
            "evolution_synergy": collective['evolution_synergy']
        })

        ai_hub.send_message("Evolution", "ALL", "evolution_complete", {
            "individual_level": report.get('new_level'),
            "collective_iq": collective['collective_iq'],
            "synergy": collective['evolution_synergy']
        })

        log_event("AUTO_AI_EVOLUTION_COMPLETE", {
            "new_level": report.get('new_level'),
            "overall_iq": report.get('intelligence_metrics', {}).get('overall_iq'),
            "collective_iq": collective['collective_iq'],
            "synergy": collective['evolution_synergy']
        })

    def _learn_from_data(self):
        """Learn and improve from collected data — runs daily evolution cycle."""
        evolution_report = ai_learning.daily_evolution(coordinator=ai_coordinator)
        save_learning_data("auto_learning_evolution", evolution_report)
        log_event("AUTO_LEARNING_EVOLUTION", {
            "predictions_evaluated": evolution_report.get("predictions_auto_evaluated", 0),
            "weight_changes": len(evolution_report.get("weight_changes", {})),
            "accuracy": evolution_report.get("summary", {}).get("accuracy", 0),
        })

        if os.path.exists(LEARNING_DATA_FILE):
            try:
                with open(LEARNING_DATA_FILE, 'r') as f:
                    learning_data = json.load(f)

                market_patterns = [d for d in learning_data if d.get("type") == "auto_market_data"]
                prediction_accuracy = [d for d in learning_data if d.get("type") == "auto_predictions"]

                insights = {
                    "total_data_points": len(learning_data),
                    "market_samples": len(market_patterns),
                    "predictions_made": len(prediction_accuracy),
                    "learning_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }

                save_learning_data("auto_learning_insights", insights)
                log_event("AUTO_LEARNING", insights)
            except Exception as e:
                log_event("LEARNING_DATA_READ_ERROR", {"error": str(e)})

    def _save_all_data(self):
        """Save all persistent data to disk."""
        try:
            ai_learning.save_all()
        except Exception as e:
            log_event("SAVE_LEARNING_ERROR", {"error": str(e)})
        try:
            ai_hub.save_all()
        except Exception as e:
            log_event("SAVE_HUB_ERROR", {"error": str(e)})
        log_event("AUTO_DATA_SAVE", {"time": datetime.datetime.now(datetime.timezone.utc).isoformat()})

    def _health_check(self, cycle_count):
        """Perform system health check and cleanup."""
        health = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "log_file_size": os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0,
            "learning_data_size": os.path.getsize(LEARNING_DATA_FILE) if os.path.exists(LEARNING_DATA_FILE) else 0,
            "uptime_hours": round((time.time() - (self.start_time or time.time())) / 3600, 1),
            "total_cycles": cycle_count,
            "task_stats": self.task_stats,
        }

        # Cleanup old logs if too large (> 50MB)
        if health["log_file_size"] > 50 * 1024 * 1024:
            try:
                with open(LOG_FILE, 'r') as f:
                    lines = f.readlines()
                with open(LOG_FILE, 'w') as f:
                    f.writelines(lines[-5000:])
            except Exception:
                pass

        # Cleanup learning data if too large (> 100MB)
        if health["learning_data_size"] > 100 * 1024 * 1024:
            try:
                with open(LEARNING_DATA_FILE, 'r') as f:
                    learning_data = json.load(f)
                # Keep only last 5000 entries
                with open(LEARNING_DATA_FILE, 'w') as f:
                    json.dump(learning_data[-5000:], f, indent=1, default=str)
            except Exception:
                pass

        # Create backups
        try:
            backup_file = ai_hub.create_backup()
            health["ai_hub_backup"] = backup_file
            log_event("AUTO_AI_HUB_BACKUP_CREATED", {"file": backup_file})
        except Exception as e:
            log_event("AI_HUB_BACKUP_ERROR", {"error": str(e)})

        try:
            unified_backup = cloud_storage.backup_all_data()
            health["unified_backup"] = unified_backup['backup_id']
            health["backup_size_mb"] = unified_backup['size_bytes'] / 1024 / 1024
            log_event("AUTO_UNIFIED_BACKUP_CREATED", {
                "backup_id": unified_backup['backup_id'],
                "size_mb": health["backup_size_mb"]
            })
        except Exception as e:
            log_event("UNIFIED_BACKUP_ERROR", {"error": str(e)})

        hub_status = ai_hub.get_status()
        health["ai_hub"] = hub_status

        try:
            cloud_stats = cloud_storage.get_statistics()
            health["cloud_storage"] = cloud_stats
        except Exception as e:
            log_event("CLOUD_STATS_ERROR", {"error": str(e)})

        log_event("AUTO_HEALTH_CHECK", health)

# Initialize background worker
background_worker = BackgroundAIWorker()

# -----------------------------
# LANCEMENT SERVEUR
# -----------------------------
# -----------------------------
# MAIN APPLICATION ENTRY POINT
# -----------------------------

def main():
    """Start the Flask application."""
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    
    print("=" * 70)
    print("SignalTrust AI Market Scanner")
    print("=" * 70)
    print(f"Server running on: http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print(f"AI Workers: {len(ai_coordinator.workers)} active")
    print(f"Learning System: {ai_learning.get_learning_summary()['total_predictions']} predictions tracked")
    print("Press CTRL+C to stop the server")
    print("=" * 70)
    
    # Start background AI worker for 24/7 operation
    background_worker.start()
    log_event("SERVER_STARTED", {
        "host": "0.0.0.0",
        "port": port,
        "background_worker": "enabled"
    })
    
    try:
        app.run(host="0.0.0.0", port=port, debug=debug)
    finally:
        background_worker.stop()
        log_event("SERVER_STOPPED", {"time": datetime.datetime.now(datetime.timezone.utc).isoformat()})

if __name__ == "__main__":
    main()

