#!/usr/bin/env python3
"""
AI Coder Bot Module
====================
Embedded AI coding assistant that can:
  - Answer coding questions (Python, JS, HTML/CSS, SQL, etc.)
  - Generate code snippets on demand
  - Explain code, debug errors, suggest improvements
  - Understand the SignalTrust project context
  - Maintain conversation history per session

Uses OpenAI / Anthropic via the existing ai_provider infrastructure.
"""

import os
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from threading import Lock

logger = logging.getLogger(__name__)

# System prompt that shapes the coding assistant personality
SYSTEM_PROMPT = """You are **SignalTrust Coder** — an expert AI coding assistant embedded inside the SignalTrust AI Market Scanner platform.

**Your capabilities:**
- Write, debug, and explain code in Python, JavaScript, HTML/CSS, SQL, Bash, and more
- Provide architecture advice and best-practice guidance
- Help with Flask, API design, front-end dev, data pipelines, AI/ML integration
- Understand the SignalTrust project: Flask web app, multi-AI coordinator, market analysis, real-time data

**Your style:**
- Be concise and direct — give working code, not essays
- Use code blocks with language tags (```python, ```javascript, etc.)
- When fixing bugs, show the exact fix with before/after
- Ask clarifying questions if the request is ambiguous
- Proactively mention edge cases and security considerations for financial code

**Project context (SignalTrust AI Scanner):**
- Stack: Python 3.11, Flask, OpenAI GPT-4, Anthropic Claude, multi-agent architecture
- Frontend: Vanilla JS, dark-theme UI, Jinja2 templates
- Key modules: app.py (routes), market_scanner.py, market_analyzer.py, ai_predictor.py, signalai_strategy.py
- Data: Real-time crypto/stock prices via CoinGecko, Yahoo Finance, CoinPaprika
- Deployment: Render.com (auto-deploy from GitHub)

Always respond in the same language the user writes in (French or English)."""

MAX_HISTORY = 30        # Max messages per session
MAX_SESSIONS = 100      # Max concurrent sessions
SESSION_TTL = 7200      # 2 hours before session expires


class CoderSession:
    """Single conversation session."""

    def __init__(self, session_id: str, user_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.messages: List[Dict] = []
        self.created_at = time.time()
        self.last_active = time.time()
        self.title = "New Chat"

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.last_active = time.time()
        # Auto-title from first user message
        if self.title == "New Chat" and role == "user":
            self.title = content[:60] + ("..." if len(content) > 60 else "")
        # Trim old messages (keep system-level context)
        if len(self.messages) > MAX_HISTORY:
            self.messages = self.messages[-MAX_HISTORY:]

    def to_dict(self) -> Dict:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "title": self.title,
            "messages": self.messages,
            "created_at": datetime.fromtimestamp(self.created_at, tz=timezone.utc).isoformat(),
            "last_active": datetime.fromtimestamp(self.last_active, tz=timezone.utc).isoformat(),
            "message_count": len(self.messages),
        }

    def is_expired(self) -> bool:
        return (time.time() - self.last_active) > SESSION_TTL


class AICoderBot:
    """
    AI-powered coding assistant with multi-provider support.
    Manages sessions, builds prompts, calls AI, returns responses.
    """

    def __init__(self):
        self._lock = Lock()
        self.sessions: Dict[str, CoderSession] = {}
        self._ai_engine = None
        self._provider_name = "none"
        self._init_ai()

    # ── AI provider initialization ──────────────────────────────────

    def _init_ai(self):
        """Initialize the best available AI provider."""
        # Try OpenAI first
        openai_key = os.environ.get("OPENAI_API_KEY", "")
        if openai_key and not openai_key.startswith("sk-proj-PLACEHOLDER"):
            try:
                import openai
                self._ai_engine = openai.OpenAI(api_key=openai_key)
                self._provider_name = os.environ.get("OPENAI_MODEL", "gpt-4o")
                logger.info("CoderBot: OpenAI provider ready")
                return
            except Exception as e:
                logger.warning(f"CoderBot: OpenAI init failed: {e}")

        # Try Anthropic
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if anthropic_key:
            try:
                import anthropic
                self._ai_engine = anthropic.Anthropic(api_key=anthropic_key)
                self._provider_name = "claude-3-5-sonnet-20241022"
                logger.info("CoderBot: Anthropic provider ready")
                return
            except Exception as e:
                logger.warning(f"CoderBot: Anthropic init failed: {e}")

        logger.warning("CoderBot: No AI provider available — using fallback")

    # ── Session management ──────────────────────────────────────────

    def _get_or_create_session(self, session_id: str, user_id: str) -> CoderSession:
        with self._lock:
            # Prune expired sessions
            expired = [k for k, v in self.sessions.items() if v.is_expired()]
            for k in expired:
                del self.sessions[k]
            # Enforce max sessions
            if len(self.sessions) >= MAX_SESSIONS and session_id not in self.sessions:
                oldest = min(self.sessions, key=lambda k: self.sessions[k].last_active)
                del self.sessions[oldest]

            if session_id not in self.sessions:
                self.sessions[session_id] = CoderSession(session_id, user_id)
            return self.sessions[session_id]

    def get_sessions(self, user_id: str) -> List[Dict]:
        """Get all active sessions for a user."""
        with self._lock:
            return [
                s.to_dict()
                for s in self.sessions.values()
                if s.user_id == user_id and not s.is_expired()
            ]

    def clear_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False

    # ── Core chat method ────────────────────────────────────────────

    def chat(self, session_id: str, user_id: str, message: str) -> Dict:
        """
        Send a message and get an AI response.

        Returns:
            {success, response, provider, session_id, timestamp}
        """
        session = self._get_or_create_session(session_id, user_id)
        session.add_message("user", message)

        # Build the prompt
        ai_response = self._call_ai(session)

        session.add_message("assistant", ai_response)

        return {
            "success": True,
            "response": ai_response,
            "provider": self._provider_name,
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ── AI call dispatcher ──────────────────────────────────────────

    def _call_ai(self, session: CoderSession) -> str:
        """Route to the correct AI provider."""
        try:
            if self._provider_name.startswith("gpt") or self._provider_name.startswith("o"):
                return self._call_openai(session)
            elif "claude" in self._provider_name:
                return self._call_anthropic(session)
            else:
                return self._fallback_response(session)
        except Exception as e:
            logger.error(f"CoderBot AI call error: {e}")
            return f"⚠️ AI Error: {str(e)}\n\nPlease try again or check the AI provider configuration."

    def _call_openai(self, session: CoderSession) -> str:
        """Call OpenAI ChatCompletion."""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Add conversation history (last 20 messages for context window)
        for msg in session.messages[-20:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        response = self._ai_engine.chat.completions.create(
            model=self._provider_name,
            messages=messages,
            max_tokens=4096,
            temperature=0.4,
        )
        return response.choices[0].message.content

    def _call_anthropic(self, session: CoderSession) -> str:
        """Call Anthropic Claude."""
        messages = []
        for msg in session.messages[-20:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        response = self._ai_engine.messages.create(
            model=self._provider_name,
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=4096,
            temperature=0.4,
        )
        return response.content[0].text

    def _fallback_response(self, session: CoderSession) -> str:
        """Generate a helpful fallback when no AI provider is available."""
        last_msg = session.messages[-1]["content"].lower() if session.messages else ""

        if any(kw in last_msg for kw in ["hello", "hi", "bonjour", "salut"]):
            return (
                "👋 Hello! I'm the SignalTrust Coder Bot.\n\n"
                "I can help with code but I currently have **no AI provider configured**.\n"
                "Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in your environment variables "
                "to enable full AI-powered coding assistance.\n\n"
                "In the meantime, I can still show you code templates and project info!"
            )

        if "help" in last_msg or "aide" in last_msg:
            return (
                "## What I can help with\n\n"
                "- 🐍 **Python**: Flask routes, data processing, API calls\n"
                "- 🌐 **JavaScript**: DOM manipulation, fetch API, async/await\n"
                "- 🎨 **HTML/CSS**: Responsive layouts, dark themes, animations\n"
                "- 🗄️ **SQL/Data**: Queries, schema design, pandas\n"
                "- 🤖 **AI/ML**: OpenAI integration, prompt engineering\n"
                "- 🏗️ **Architecture**: API design, microservices, Docker\n\n"
                "Just describe what you need and I'll write the code!"
            )

        if any(kw in last_msg for kw in ["flask", "route", "api", "endpoint"]):
            return (
                "Here's a Flask route template:\n\n"
                "```python\n"
                "@app.route('/api/your-endpoint', methods=['POST'])\n"
                "def api_your_endpoint():\n"
                '    """Description of your endpoint."""\n'
                "    try:\n"
                "        data = request.get_json()\n"
                "        # Your logic here\n"
                "        result = process(data)\n"
                '        return jsonify({"success": True, "data": result}), 200\n'
                "    except Exception as e:\n"
                '        return jsonify({"success": False, "error": str(e)}), 500\n'
                "```\n\n"
                "💡 Configure an AI provider for full coding assistance."
            )

        return (
            "I received your message but **no AI provider is currently configured**.\n\n"
            "To enable full AI coding assistance, set one of these environment variables:\n"
            "- `OPENAI_API_KEY` — for GPT-4 powered responses\n"
            "- `ANTHROPIC_API_KEY` — for Claude powered responses\n\n"
            "💡 Type **help** to see what I can assist with."
        )

    # ── Status ──────────────────────────────────────────────────────

    def get_status(self) -> Dict:
        return {
            "provider": self._provider_name,
            "active_sessions": len(self.sessions),
            "ai_available": self._provider_name != "none",
        }


# ── Singleton ───────────────────────────────────────────────────────

_coder_bot = None


def get_coder_bot() -> AICoderBot:
    """Get or create the singleton CoderBot instance."""
    global _coder_bot
    if _coder_bot is None:
        _coder_bot = AICoderBot()
    return _coder_bot
