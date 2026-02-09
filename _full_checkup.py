#!/usr/bin/env python3
"""
SignalTrust AI Scanner — Full System Checkup
=============================================
Tests: syntax, imports, routes, features, data integrity.
"""

import sys
import os
import glob
import json
import py_compile
import importlib
import traceback
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"
results = {"pass": 0, "fail": 0, "warn": 0, "details": []}


def log(status, category, message):
    icon = PASS if status == "pass" else (FAIL if status == "fail" else WARN)
    results[status] += 1
    results["details"].append(f"{icon} [{category}] {message}")
    print(f"  {icon} {message}")


print("=" * 60)
print("  SIGNALTRUST AI SCANNER — FULL SYSTEM CHECKUP")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ─── 1. SYNTAX CHECK ALL .PY FILES ─────────────────────────
print("\n📋 1. SYNTAX CHECK (all .py files)")
print("-" * 40)
py_files = sorted(glob.glob("*.py") + glob.glob("agents/*/*.py") + glob.glob("config/*.py"))
syntax_errors = []
for f in py_files:
    try:
        py_compile.compile(f, doraise=True)
        log("pass", "SYNTAX", f)
    except py_compile.PyCompileError as e:
        syntax_errors.append(f)
        log("fail", "SYNTAX", f"{f}: {e}")

print(f"\n  Checked {len(py_files)} files — {len(py_files) - len(syntax_errors)} OK, {len(syntax_errors)} errors")

# ─── 2. IMPORT TEST: CORE MODULES ──────────────────────────
print("\n📦 2. IMPORT TEST (core modules)")
print("-" * 40)

core_modules = [
    ("user_auth", "UserAuth"),
    ("payment_processor", "PaymentProcessor"),
    ("market_scanner", "MarketScanner"),
    ("market_analyzer", "MarketAnalyzer"),
    ("ai_predictor", "AIPredictor"),
    ("ai_provider", "AIProvider"),
    ("ai_market_intelligence", "AIMarketIntelligence"),
    ("ai_communication_hub", "ai_hub"),
    ("ai_learning_system", "get_learning_system"),
    ("multi_ai_coordinator", "get_coordinator"),
    ("signalai_strategy", "signalai_strategy"),
    ("realtime_market_data", "RealTimeMarketData"),
    ("crypto_gem_finder", "CryptoGemFinder"),
    ("notification_center", "NotificationCenter"),
    ("notification_ai", "notification_ai"),
    ("ai_evolution_system", "AIEvolutionSystem"),
    ("universal_market_analyzer", "UniversalMarketAnalyzer"),
    ("total_market_data_collector", "TotalMarketDataCollector"),
    ("cloud_storage_manager", "cloud_storage"),
    ("ai_chat_system", "AIChatSystem"),
    ("live_price_provider", None),
    ("meta_model", None),
    ("scanner", None),
    ("coupon_manager", None),
    ("limit_enforcer", None),
    ("admin_dashboard", None),
]

import_errors = []
for mod_name, attr_name in core_modules:
    try:
        mod = importlib.import_module(mod_name)
        if attr_name:
            obj = getattr(mod, attr_name)
            log("pass", "IMPORT", f"{mod_name}.{attr_name}")
        else:
            log("pass", "IMPORT", mod_name)
    except Exception as e:
        import_errors.append(mod_name)
        log("fail", "IMPORT", f"{mod_name}: {type(e).__name__}: {e}")

print(f"\n  {len(core_modules) - len(import_errors)}/{len(core_modules)} modules loaded OK")

# ─── 3. FLASK APP & ROUTES ─────────────────────────────────
print("\n🌐 3. FLASK APP & ROUTES")
print("-" * 40)

try:
    import logging
    logging.disable(logging.CRITICAL)
    from app import app
    log("pass", "FLASK", "app.py loaded successfully")

    rules = sorted([r.rule for r in app.url_map.iter_rules() if r.rule != "/static/<path:filename>"])
    log("pass", "FLASK", f"{len(rules)} routes registered")

    # Check critical routes exist
    critical_routes = [
        "/", "/login", "/register", "/dashboard", "/profile",
        "/ai-chat", "/scanner", "/analyzer", "/predictions",
        "/pricing", "/settings", "/payment", "/tradingview",
        "/whale-watcher", "/notifications",
        "/admin/comm-hub",
        "/api/profile", "/api/profile/avatar",
        "/api/admin/comm-hub/status", "/api/admin/comm-hub/send",
        "/api/admin/comm-hub/evolve", "/api/admin/comm-hub/backup",
        "/api/worker/status",
        "/api/login", "/api/register",
        "/api/markets/scan", "/api/markets/analyze",
        "/api/ai/predict",
    ]
    for route in critical_routes:
        if route in rules:
            log("pass", "ROUTE", route)
        else:
            log("fail", "ROUTE", f"MISSING: {route}")

    logging.disable(logging.NOTSET)
except Exception as e:
    log("fail", "FLASK", f"Failed to load app: {e}")
    traceback.print_exc()

# ─── 4. TEMPLATES CHECK ────────────────────────────────────
print("\n📄 4. TEMPLATES CHECK")
print("-" * 40)

required_templates = [
    "index.html", "login.html", "register.html", "dashboard.html",
    "profile.html", "admin_comm_hub.html",
    "ai_chat.html", "scanner.html", "analyzer.html", "predictions.html",
    "pricing.html", "settings.html", "payment.html", "tradingview.html",
    "whale_watcher.html", "notifications.html", "ai_intelligence.html",
]

for tmpl in required_templates:
    path = os.path.join("templates", tmpl)
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size > 100:
            log("pass", "TEMPLATE", f"{tmpl} ({size:,} bytes)")
        else:
            log("warn", "TEMPLATE", f"{tmpl} exists but seems empty ({size} bytes)")
    else:
        log("fail", "TEMPLATE", f"MISSING: {tmpl}")

# ─── 5. DATA DIRECTORIES & FILES ───────────────────────────
print("\n💾 5. DATA INTEGRITY")
print("-" * 40)

data_dirs = ["data", "data/ai_hub", "data/backups", "static/uploads/avatars"]
for d in data_dirs:
    if os.path.isdir(d):
        log("pass", "DIR", d)
    else:
        log("warn", "DIR", f"Missing directory: {d} (will be created on first use)")

json_files = glob.glob("data/*.json") + glob.glob("data/ai_hub/*.json")
# Skip encrypted files
encrypted_files = ['data/admin_payment_info.json']
json_files = [f for f in json_files if f not in encrypted_files]

for jf in sorted(json_files):
    try:
        with open(jf, "r") as f:
            data = json.load(f)
        if isinstance(data, (dict, list)):
            count = len(data) if isinstance(data, list) else len(data.keys())
            log("pass", "JSON", f"{jf} ({count} entries)")
        else:
            log("pass", "JSON", jf)
    except json.JSONDecodeError as e:
        log("fail", "JSON", f"{jf}: Invalid JSON — {e}")
    except Exception as e:
        log("warn", "JSON", f"{jf}: {e}")

# Check encrypted files separately
for ef in encrypted_files:
    if os.path.exists(ef):
        log("pass", "JSON", f"{ef} (encrypted)")
    else:
        log("warn", "JSON", f"{ef} (encrypted file missing)")

# ─── 6. FEATURE TESTS ──────────────────────────────────────
print("\n🧪 6. FEATURE TESTS")
print("-" * 40)

# Test user_auth
try:
    from user_auth import UserAuth
    ua = UserAuth()
    admin = ua.get_user_by_email("signaltrustai@gmail.com")
    if admin:
        log("pass", "AUTH", f"Admin account exists: {admin['user_id']}")
        # Check new profile fields exist
        has_profile_fields = all(k in admin for k in ["phone", "bio", "location", "profile_picture"])
        if has_profile_fields:
            log("pass", "AUTH", "Profile fields (phone, bio, location, profile_picture) present")
        else:
            log("warn", "AUTH", "Some profile fields missing from admin user (will appear after first update)")
    else:
        log("warn", "AUTH", "Admin account not found (will be created on first run)")

    # Test update_user_profile method exists
    if hasattr(ua, 'update_user_profile'):
        log("pass", "AUTH", "update_user_profile method exists")
    else:
        log("fail", "AUTH", "update_user_profile method MISSING")
except Exception as e:
    log("fail", "AUTH", f"UserAuth test failed: {e}")

# Test payment processor pricing
try:
    from payment_processor import PaymentProcessor
    pp = PaymentProcessor()
    signalai_plan = pp.PLANS.get("signalai", {})
    price = signalai_plan.get("price", 0)
    if price == 9.99:
        log("pass", "PRICING", f"SignalAI price = ${price}")
    else:
        log("fail", "PRICING", f"SignalAI price = ${price} (expected $9.99)")
except Exception as e:
    log("fail", "PRICING", f"Payment processor test failed: {e}")

# Test SignalAI strategy
try:
    from signalai_strategy import signalai_strategy
    strats = signalai_strategy.get_available_strategies()
    log("pass", "STRATEGY", f"Strategies: {list(strats.keys())}")
    si = strats.get("SignalAI", {})
    ind_count = len(si.get("indicators", []))
    if ind_count >= 12:
        log("pass", "STRATEGY", f"SignalAI uses {ind_count} indicators (v3 optimized)")
    else:
        log("warn", "STRATEGY", f"SignalAI uses only {ind_count} indicators")
    if si.get("price") == 9.99:
        log("pass", "STRATEGY", "SignalAI price = $9.99")
    else:
        log("fail", "STRATEGY", f"SignalAI price = ${si.get('price')} (expected $9.99)")
except Exception as e:
    log("fail", "STRATEGY", f"Strategy test failed: {e}")

# Test multi_ai_coordinator
try:
    from multi_ai_coordinator import get_coordinator
    coord = get_coordinator()
    wcount = len(coord.workers)
    log("pass", "COORDINATOR", f"{wcount} AI workers registered")
    stats = coord.get_stats()
    log("pass", "COORDINATOR", f"get_stats() works — cache: {stats.get('cache', {}).get('size', 0)} entries")
except Exception as e:
    log("fail", "COORDINATOR", f"Coordinator test failed: {e}")

# Test ai_learning_system
try:
    from ai_learning_system import get_learning_system
    ls = get_learning_system()
    summary = ls.get_learning_summary()
    log("pass", "LEARNING", f"Learning system loaded — {summary.get('total_predictions', 0)} predictions tracked")
except Exception as e:
    log("fail", "LEARNING", f"Learning system test failed: {e}")

# Test ai_communication_hub
try:
    from ai_communication_hub import ai_hub
    status = ai_hub.get_status()
    log("pass", "HUB", f"Hub status: {status.get('status', '?')} — {status.get('data_exchanges', 0)} exchanges")
    knowledge = ai_hub.get_all_knowledge()
    log("pass", "HUB", f"Knowledge types: {list(knowledge.keys()) if knowledge else 'empty'}")
except Exception as e:
    log("fail", "HUB", f"Communication hub test failed: {e}")

# Test live strategy signal (with hardcoded price to avoid network dependency)
try:
    result = signalai_strategy.generate_signals("BTC", "SignalAI", current_price=104000)
    if "error" not in result:
        log("pass", "SIGNAL", f"BTC signal: {result['signal']} (confidence {result['confidence']}%, regime {result.get('regime', '?')})")
        if result.get("entry_price") and result.get("stop_loss") and result.get("take_profit"):
            log("pass", "SIGNAL", f"Entry={result['entry_price']}, SL={result['stop_loss']}, TP={result['take_profit']}, R:R={result.get('risk_reward')}")
        else:
            log("warn", "SIGNAL", "Missing entry/SL/TP levels")
        if result.get("mtf_consensus"):
            log("pass", "SIGNAL", f"Multi-timeframe consensus: {result['mtf_consensus']}")
    else:
        log("fail", "SIGNAL", f"Signal error: {result['error']}")
except Exception as e:
    log("fail", "SIGNAL", f"Signal generation failed: {e}")

# ─── 7. SECURITY CHECKS ────────────────────────────────────
print("\n🔒 7. SECURITY CHECKS")
print("-" * 40)

# Check .env exists
if os.path.exists(".env"):
    log("pass", "SEC", ".env file exists")
    with open(".env", "r") as f:
        env_content = f.read()
    if "SECRET_KEY" in env_content:
        log("pass", "SEC", "SECRET_KEY configured")
    else:
        log("warn", "SEC", "SECRET_KEY not in .env (will use random)")
else:
    log("warn", "SEC", "No .env file (app will use defaults)")

# Check no hardcoded secrets in code
import re
secret_patterns = [
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API key"),
    (r'password\s*=\s*["\'][^"\']{8,}', "hardcoded password"),
]
code_files = glob.glob("*.py")
for pattern, desc in secret_patterns:
    for f in code_files:
        try:
            with open(f, "r", errors="ignore") as fp:
                content = fp.read()
            matches = re.findall(pattern, content)
            if matches and f not in ("test_openai.py",):
                log("warn", "SEC", f"Potential {desc} in {f}")
        except Exception:
            pass

# Check .gitignore
if os.path.exists(".gitignore"):
    with open(".gitignore", "r") as f:
        gi = f.read()
    for item in [".env", "__pycache__", "*.pyc"]:
        if item in gi:
            log("pass", "SEC", f".gitignore contains: {item}")
        else:
            log("warn", "SEC", f".gitignore missing: {item}")
else:
    log("warn", "SEC", "No .gitignore file")

# ─── 8. RANDOM/FAKE DATA CHECK ─────────────────────────────
print("\n🎲 8. RANDOM/FAKE DATA CHECK")
print("-" * 40)

critical_files = [
    "signalai_strategy.py", "multi_ai_coordinator.py", "ai_learning_system.py",
    "ai_communication_hub.py", "market_analyzer.py", "market_scanner.py",
    "ai_predictor.py", "ai_market_intelligence.py", "realtime_market_data.py",
    "crypto_gem_finder.py", "whale_watcher.py", "universal_market_analyzer.py",
    "total_market_data_collector.py",
]

for f in critical_files:
    if not os.path.exists(f):
        log("warn", "RANDOM", f"{f} not found")
        continue
    with open(f, "r", errors="ignore") as fp:
        content = fp.read()
    has_random = "random.uniform" in content or "random.randint" in content or "random.choice" in content
    has_fake = "fake_" in content.lower() or "dummy_data" in content.lower()
    if has_random:
        log("fail", "RANDOM", f"{f} contains random.uniform/randint/choice")
    elif has_fake:
        log("warn", "RANDOM", f"{f} contains fake/dummy references")
    else:
        log("pass", "RANDOM", f"{f} — clean (no random/fake)")

# ─── FINAL REPORT ──────────────────────────────────────────
print("\n" + "=" * 60)
print("  FINAL REPORT")
print("=" * 60)
print(f"  {PASS} Passed:   {results['pass']}")
print(f"  {WARN} Warnings: {results['warn']}")
print(f"  {FAIL} Failed:   {results['fail']}")
print(f"  Total checks: {results['pass'] + results['warn'] + results['fail']}")
print()
if results["fail"] == 0:
    print("  🎉 ALL CHECKS PASSED — App is production ready!")
elif results["fail"] <= 3:
    print("  ⚠️  Minor issues found — review failures above")
else:
    print("  🚨 Critical issues found — fix failures before deploying")
print("=" * 60)
