#!/usr/bin/env python3
"""Test all API keys with real calls."""
import os, requests, time
from dotenv import load_dotenv
load_dotenv()

print("=" * 50)
print("  TEST API KEYS EN LIVE")
print("=" * 50)

results = []

# 1. Etherscan
print("\n[1] Etherscan...")
key = os.getenv("ETHERSCAN_API_KEY", "")
try:
    r = requests.get(
        f"https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist"
        f"&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
        f"&page=1&offset=3&sort=desc&apikey={key}",
        timeout=10
    )
    d = r.json()
    if d.get("status") == "1":
        print(f"   ✅ OK — {len(d['result'])} transactions ETH")
        results.append(True)
    else:
        print(f"   ❌ ERREUR: {d.get('message', 'unknown')}")
        results.append(False)
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    results.append(False)

# 2. Whale Alert
print("\n[2] Whale Alert...")
key2 = os.getenv("WHALE_ALERT_API_KEY", "")
try:
    ts = int(time.time()) - 3600
    r = requests.get(
        f"https://api.whale-alert.io/v1/transactions?api_key={key2}&min_value=500000&start={ts}",
        timeout=10
    )
    d = r.json()
    if d.get("result") == "success":
        txs = d.get("transactions", [])
        print(f"   ✅ OK — {len(txs)} whale transactions (dernière heure)")
        results.append(True)
    else:
        print(f"   ❌ ERREUR: {d.get('message', d)}")
        results.append(False)
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    results.append(False)

# 3. Groq
print("\n[3] Groq LLM...")
try:
    r = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '')}"},
        timeout=10
    )
    if r.status_code == 200:
        models = [m["id"] for m in r.json().get("data", []) if "llama" in m["id"]]
        print(f"   ✅ OK — {len(models)} modèles Llama disponibles")
        results.append(True)
    else:
        print(f"   ❌ ERREUR: HTTP {r.status_code}")
        results.append(False)
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    results.append(False)

# 4. Anthropic
print("\n[4] Anthropic Claude...")
try:
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": os.getenv("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Say OK"}],
        },
        timeout=15
    )
    if r.status_code == 200:
        txt = r.json().get("content", [{}])[0].get("text", "")
        print(f'   ✅ OK — Claude répond: "{txt}"')
        results.append(True)
    else:
        err = r.json().get("error", {}).get("message", f"HTTP {r.status_code}")
        print(f"   ❌ ERREUR: {err}")
        results.append(False)
except Exception as e:
    print(f"   ❌ FAIL: {e}")
    results.append(False)

# Summary
print("\n" + "=" * 50)
ok = sum(results)
print(f"  RÉSULTAT: {ok}/4 API keys fonctionnelles")
print("=" * 50)
