"""Test script for OpenAI integration.
Usage: python test_openai.py
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

if not API_KEY:
    print("ERROR: OPENAI_API_KEY not set in environment (.env)")
    print("Please add your key to the .env file in the project root.")
    raise SystemExit(1)

client = OpenAI(api_key=API_KEY)

payload = "Donne-moi une phrase courte de salutation en français."

try:
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
    print("OpenAI response:\n", content)

except Exception as e:
    # Provide clearer guidance on API errors
    err_text = str(e)
    print("OpenAI client error:", err_text)
    if 'invalid_api_key' in err_text or '401' in err_text:
        print("→ 401 Invalid API key: check your .env value or regenerate the key at https://platform.openai.com/account/api-keys")
    raise SystemExit(2)
