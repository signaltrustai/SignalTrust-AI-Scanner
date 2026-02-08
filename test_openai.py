"""Test script for OpenAI integration.
Usage: python test_openai.py
"""
import os
import pytest
from dotenv import load_dotenv

# Skip entirely when no API key is configured to avoid hard failures in CI/offline runs
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

if not API_KEY:
    pytest.skip("OPENAI_API_KEY not set; skipping OpenAI integration test", allow_module_level=True)

from openai import OpenAI

client = OpenAI(api_key=API_KEY)

payload = "Donne-moi une phrase courte de salutation en français."

def test_openai_chat_completion():
    """Verify OpenAI chat completion returns content."""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": payload}],
        max_tokens=60,
        temperature=0.3,
    )
    # Extract content safely
    content = None
    try:
        content = resp.choices[0].message.content
    except Exception:
        try:
            content = resp.choices[0].message['content']
        except Exception:
            content = str(resp)
    assert content, "OpenAI response content should not be empty"
