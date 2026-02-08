#!/usr/bin/env python3
"""Quick diagnostic: which AI systems are alive."""
import os, subprocess
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("  AI SYSTEM STATUS DIAGNOSTIC")
print("=" * 60)

# 1. Coordinator workers
from multi_ai_coordinator import get_coordinator
coord = get_coordinator()
print(f"\n[Coordinator] {len(coord.workers)} workers registered:")
for w in coord.workers:
    print(f"  - {w.name} ({w.provider})")

# 2. Learning system
from ai_learning_system import get_learning_system
learn = get_learning_system()
s = learn.get_learning_summary()
print(f"\n[Learning] {s.get('total_predictions', 0)} predictions, {s.get('total_outcomes', s.get('verified_outcomes', 0))} outcomes")

# 3. Communication hub
from ai_communication_hub import ai_hub
st = ai_hub.get_status()
print(f"\n[Hub] Status: {st.get('status', 'unknown')}, Messages: {st.get('total_messages', st.get('total_exchanges', 0))}")
rw = st.get("registered_workers", st.get("workers", {}))
if rw:
    for name, info in rw.items():
        print(f"  - {name}: {info}")

# 4. AI Provider
print(f"\n[AI Provider] Managed by coordinator (3 providers)")

# 5. OpenAI key check
key = os.getenv("OPENAI_API_KEY", "")
if key and not key.startswith("your_"):
    print(f"[OpenAI] Key present ({key[:12]}...)")
else:
    print("[OpenAI] NO KEY — GPT-4 worker disabled")

anth = os.getenv("ANTHROPIC_API_KEY", "")
if anth and not anth.startswith("your_"):
    print(f"[Anthropic] Key present ({anth[:12]}...)")
else:
    print("[Anthropic] NO KEY — Claude worker disabled")

# 6. Docker agents
print()
try:
    r = subprocess.run(["docker", "ps", "--format", "{{.Names}}: {{.Status}}"],
                       capture_output=True, text=True, timeout=5)
    if r.returncode == 0 and r.stdout.strip():
        print("[Docker Agents]:")
        for line in r.stdout.strip().split("\n"):
            print(f"  {line}")
    else:
        print("[Docker Agents] No containers running")
except Exception as e:
    print(f"[Docker] Not available: {e}")

# 7. Background worker
print("\n[Background Worker] Only starts when server runs (python app.py)")

print("\n" + "=" * 60)
print(f"  TOTAL ACTIVE AI WORKERS: {len(coord.workers)}")
print("=" * 60)
