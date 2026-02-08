"""Integration test for agent calls and ChatKit session endpoint (local).
Usage: python test_agent_integration.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Enable unauthenticated testing
os.environ['ALLOW_UNAUTH_TESTING'] = 'true'

from app import app, create_chatkit_session, call_agent

print("Running local integration test...")

# Test call_agent mock behavior (when AGENT_API_KEY not set)
resp = call_agent('STOCK', 'Salut agent de test')
print("call_agent response:")
print(resp)

# Test ChatKit session creation (requires Flask app context)
with app.app_context():
    try:
        result = create_chatkit_session()
        print("create_chatkit_session returned:")
        if hasattr(result, 'get_data'):
            print(result.get_data(as_text=True))
        else:
            print(result)
    except Exception as e:
        print("create_chatkit_session error:", e)

print("Integration test complete.")
