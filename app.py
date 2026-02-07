from flask import Flask, render_template, request, jsonify
import os
import requests
import datetime
import json

app = Flask(__name__)

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

def log_event(event_type: str, payload: dict):
    """Enregistre les événements importants dans un fichier log."""
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
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
# ROUTES FLASK
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ai-chat")
def ai_chat():
    return render_template("ai_chat.html")

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
# LANCEMENT SERVEUR
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
