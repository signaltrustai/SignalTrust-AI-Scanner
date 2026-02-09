#!/usr/bin/env python3
"""
Multi-AI Coordinator — High-Performance Orchestration Engine
============================================================
Coordinates multiple AI providers (OpenAI, Anthropic, Ollama, Rule-Based)
with parallel execution, response caching, connection pooling, shared context,
priority queuing, and adaptive weight management.

Optimized for speed:
- Persistent HTTP sessions with connection pooling
- TTL-based response cache (avoid redundant API calls)
- Concurrent futures with aggressive timeouts
- Priority task queue for critical vs. background work
- Shared context memory so later AIs build on earlier results
"""

import os
import json
import time
import hashlib
import logging
import threading
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Any
from collections import OrderedDict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Response cache with TTL
# ---------------------------------------------------------------------------

class ResponseCache:
    """Thread-safe LRU cache with per-entry TTL."""

    def __init__(self, max_size: int = 500, default_ttl: int = 300):
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.Lock()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _make_key(self, task_type: str, prompt: str, data: dict) -> str:
        raw = f"{task_type}|{prompt}|{json.dumps(data, sort_keys=True, default=str)}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, task_type: str, prompt: str, data: dict) -> Optional[dict]:
        key = self._make_key(task_type, prompt, data)
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self.misses += 1
                return None
            if time.time() > entry["expires"]:
                del self._cache[key]
                self.misses += 1
                return None
            self._cache.move_to_end(key)
            self.hits += 1
            return entry["value"]

    def put(self, task_type: str, prompt: str, data: dict, value: dict, ttl: Optional[int] = None):
        key = self._make_key(task_type, prompt, data)
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires": time.time() + (ttl or self.default_ttl),
            }
            self._cache.move_to_end(key)
            while len(self._cache) > self.max_size:
                self._cache.popitem(last=False)

    def invalidate_all(self):
        with self._lock:
            self._cache.clear()

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 3) if total else 0,
        }


# ---------------------------------------------------------------------------
# Shared context memory
# ---------------------------------------------------------------------------

class SharedContext:
    """Thread-safe shared memory that lets AI workers build on each other's results."""

    def __init__(self, max_entries: int = 200):
        self._data: OrderedDict = OrderedDict()
        self._lock = threading.Lock()
        self.max_entries = max_entries

    def store(self, key: str, value: Any, ttl: int = 600):
        with self._lock:
            self._data[key] = {
                "value": value,
                "stored_at": time.time(),
                "expires": time.time() + ttl,
            }
            self._data.move_to_end(key)
            while len(self._data) > self.max_entries:
                self._data.popitem(last=False)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return None
            if time.time() > entry["expires"]:
                del self._data[key]
                return None
            return entry["value"]

    def get_recent(self, prefix: str, limit: int = 5) -> List[dict]:
        """Get recent entries matching a key prefix."""
        results = []
        with self._lock:
            for k, v in reversed(self._data.items()):
                if k.startswith(prefix) and time.time() <= v["expires"]:
                    results.append({"key": k, "value": v["value"]})
                    if len(results) >= limit:
                        break
        return results

    def get_symbol_context(self, symbol: str) -> dict:
        """Aggregate all recent context for a symbol."""
        analyses = self.get_recent(f"analysis:{symbol}", limit=3)
        predictions = self.get_recent(f"prediction:{symbol}", limit=3)
        signals = self.get_recent(f"signal:{symbol}", limit=3)
        return {
            "recent_analyses": [a["value"] for a in analyses],
            "recent_predictions": [p["value"] for p in predictions],
            "recent_signals": [s["value"] for s in signals],
        }

    def clear(self):
        with self._lock:
            self._data.clear()


# ---------------------------------------------------------------------------
# HTTP session pool
# ---------------------------------------------------------------------------

def _build_session() -> requests.Session:
    """Create a requests.Session with connection pooling and retry logic."""
    session = requests.Session()
    retry = Retry(
        total=2,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(
        pool_connections=10,
        pool_maxsize=20,
        max_retries=retry,
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


# ---------------------------------------------------------------------------
# AI Worker
# ---------------------------------------------------------------------------

class AIWorker:
    """Wraps a single AI provider with stats tracking and pooled HTTP."""

    PROVIDER_PRIORITY = {
        "openai": 1,
        "anthropic": 2,
        "deepseek": 3,
        "gemini": 4,
        "ollama": 5,
        "rule_based": 6,
    }

    def __init__(self, name: str, provider: str, config: dict, session: requests.Session):
        self.name = name
        self.provider = provider
        self.config = config
        self.session = session
        self.priority = self.PROVIDER_PRIORITY.get(provider, 5)

        # Stats
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_latency_ms = 0.0
        self._lock = threading.Lock()

    # ---- public -----------------------------------------------------------

    def execute(self, task_type: str, prompt: str, data: dict, context: Optional[dict] = None) -> dict:
        """Execute a task and return the result dict."""
        t0 = time.time()
        try:
            result = self._dispatch(task_type, prompt, data, context)
            latency = (time.time() - t0) * 1000
            with self._lock:
                self.tasks_completed += 1
                self.total_latency_ms += latency
            result["worker"] = self.name
            result["provider"] = self.provider
            result["latency_ms"] = round(latency, 1)
            return result
        except Exception as exc:
            latency = (time.time() - t0) * 1000
            with self._lock:
                self.tasks_failed += 1
                self.total_latency_ms += latency
            return {
                "success": False,
                "error": str(exc),
                "worker": self.name,
                "provider": self.provider,
                "latency_ms": round(latency, 1),
            }

    @property
    def avg_latency(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return round(self.total_latency_ms / total, 1) if total else 0

    @property
    def success_rate(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return round(self.tasks_completed / total, 3) if total else 1.0

    def get_stats(self) -> dict:
        return {
            "name": self.name,
            "provider": self.provider,
            "priority": self.priority,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "avg_latency_ms": self.avg_latency,
            "success_rate": self.success_rate,
        }

    # ---- dispatch ---------------------------------------------------------

    def _dispatch(self, task_type: str, prompt: str, data: dict, context: Optional[dict] = None) -> dict:
        ctx_block = ""
        if context:
            parts = []
            for cat in ("recent_analyses", "recent_predictions", "recent_signals"):
                items = context.get(cat, [])
                if items:
                    parts.append(f"[{cat}]: {json.dumps(items[:2], default=str)}")
            if parts:
                ctx_block = "\n\n--- Prior AI Context ---\n" + "\n".join(parts) + "\n---"

        full_prompt = f"{prompt}{ctx_block}"

        if self.provider == "openai":
            return self._call_openai(task_type, full_prompt, data)
        elif self.provider == "anthropic":
            return self._call_anthropic(task_type, full_prompt, data)
        elif self.provider == "deepseek":
            return self._call_deepseek(task_type, full_prompt, data)
        elif self.provider == "gemini":
            return self._call_gemini(task_type, full_prompt, data)
        elif self.provider == "ollama":
            return self._call_ollama(task_type, full_prompt, data)
        elif self.provider == "rule_based":
            return self._rule_based_analysis(task_type, prompt, data)
        else:
            return {"success": False, "error": f"Unknown provider: {self.provider}"}

    # ---- OpenAI -----------------------------------------------------------

    def _call_openai(self, task_type: str, prompt: str, data: dict) -> dict:
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY", "")
        model = self.config.get("model") or os.getenv("OPENAI_MODEL", "gpt-4o")
        if not api_key:
            return {"success": False, "error": "No OpenAI API key"}

        system_msg = (
            "You are SignalTrust AI — an elite financial market analyst. "
            "Respond ONLY with valid JSON. Include: direction (BULLISH/BEARISH/NEUTRAL), "
            "confidence (0-1), key_factors (list), risk_level (LOW/MEDIUM/HIGH), "
            "summary (one paragraph)."
        )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Task: {task_type}\n\nData: {json.dumps(data, default=str)}\n\nPrompt: {prompt}"},
        ]

        resp = self.session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "temperature": 0.3, "max_tokens": 1500},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"raw_response": content}

        return {
            "success": True,
            "analysis": parsed,
            "model": model,
            "tokens_used": body.get("usage", {}).get("total_tokens", 0),
        }

    # ---- Anthropic --------------------------------------------------------

    def _call_anthropic(self, task_type: str, prompt: str, data: dict) -> dict:
        api_key = self.config.get("api_key") or os.getenv("ANTHROPIC_API_KEY", "")
        model = self.config.get("model", "claude-sonnet-4-20250514")
        if not api_key:
            return {"success": False, "error": "No Anthropic API key"}

        system_msg = (
            "You are SignalTrust AI — an elite financial market analyst. "
            "Respond ONLY with valid JSON. Include: direction, confidence, "
            "key_factors, risk_level, summary."
        )

        resp = self.session.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 1500,
                "system": system_msg,
                "messages": [
                    {"role": "user", "content": f"Task: {task_type}\nData: {json.dumps(data, default=str)}\nPrompt: {prompt}"}
                ],
            },
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body["content"][0]["text"]

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"raw_response": content}

        return {
            "success": True,
            "analysis": parsed,
            "model": model,
            "tokens_used": body.get("usage", {}).get("input_tokens", 0) + body.get("usage", {}).get("output_tokens", 0),
        }

    # ---- Ollama (local) ---------------------------------------------------

    def _call_ollama(self, task_type: str, prompt: str, data: dict) -> dict:
        base_url = self.config.get("base_url", "http://localhost:11434")
        model = self.config.get("model", "llama3")

        full = (
            f"You are a financial analyst AI. Respond with JSON only.\n"
            f"Task: {task_type}\nData: {json.dumps(data, default=str)}\nPrompt: {prompt}"
        )
        resp = self.session.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": full, "stream": False},
            timeout=60,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body.get("response", "")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"raw_response": content}

        return {"success": True, "analysis": parsed, "model": model}

    # ---- DeepSeek ---------------------------------------------------------

    def _call_deepseek(self, task_type: str, prompt: str, data: dict) -> dict:
        api_key = self.config.get("api_key") or os.getenv("DEEPSEEK_API_KEY", "")
        model = self.config.get("model", "deepseek-chat")
        if not api_key:
            return {"success": False, "error": "No DeepSeek API key"}

        system_msg = (
            "You are SignalTrust AI — an elite financial market analyst. "
            "Respond ONLY with valid JSON. Include: direction (BULLISH/BEARISH/NEUTRAL), "
            "confidence (0-1), key_factors (list), risk_level (LOW/MEDIUM/HIGH), "
            "summary (one paragraph)."
        )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Task: {task_type}\n\nData: {json.dumps(data, default=str)}\n\nPrompt: {prompt}"},
        ]

        resp = self.session.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "temperature": 0.3, "max_tokens": 1500},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"raw_response": content}

        return {
            "success": True,
            "analysis": parsed,
            "model": model,
            "tokens_used": body.get("usage", {}).get("total_tokens", 0),
        }

    # ---- Google Gemini ----------------------------------------------------

    def _call_gemini(self, task_type: str, prompt: str, data: dict) -> dict:
        api_key = self.config.get("api_key") or os.getenv("GOOGLE_AI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        model = self.config.get("model", "gemini-2.0-flash")
        if not api_key:
            return {"success": False, "error": "No Google AI / Gemini API key"}

        system_msg = (
            "You are SignalTrust AI — an elite financial market analyst. "
            "Respond ONLY with valid JSON. Include: direction (BULLISH/BEARISH/NEUTRAL), "
            "confidence (0-1), key_factors (list), risk_level (LOW/MEDIUM/HIGH), "
            "summary (one paragraph)."
        )

        contents = [
            {"role": "user", "parts": [{"text": f"Task: {task_type}\nData: {json.dumps(data, default=str)}\nPrompt: {prompt}"}]},
        ]

        resp = self.session.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json={
                "contents": contents,
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1500},
                "systemInstruction": {"parts": [{"text": system_msg}]},
            },
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body["candidates"][0]["content"]["parts"][0]["text"]

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"raw_response": content}

        return {
            "success": True,
            "analysis": parsed,
            "model": model,
            "tokens_used": body.get("usageMetadata", {}).get("totalTokenCount", 0),
        }

    # ---- Rule-based (instant, zero cost) ----------------------------------

    def _rule_based_analysis(self, task_type: str, prompt: str, data: dict) -> dict:
        """Deterministic rule engine — always available, fast fallback."""
        analysis: Dict[str, Any] = {
            "direction": "NEUTRAL",
            "confidence": 0.5,
            "risk_level": "MEDIUM",
            "key_factors": [],
            "summary": "",
        }

        # Technical rules
        rsi = data.get("rsi") or data.get("indicators", {}).get("rsi")
        macd = data.get("macd") or data.get("indicators", {}).get("macd")
        price_change = data.get("change_24h") or data.get("price_change_24h", 0)
        volume_change = data.get("volume_change_24h", 0)
        sma50 = data.get("sma_50") or data.get("indicators", {}).get("sma_50")
        sma200 = data.get("sma_200") or data.get("indicators", {}).get("sma_200")

        score = 0  # -100 to +100

        if rsi is not None:
            if rsi < 30:
                score += 25
                analysis["key_factors"].append(f"RSI oversold ({rsi:.1f})")
            elif rsi > 70:
                score -= 25
                analysis["key_factors"].append(f"RSI overbought ({rsi:.1f})")
            elif rsi < 45:
                score += 10
            elif rsi > 55:
                score -= 10

        if macd is not None:
            if isinstance(macd, dict):
                macd_val = macd.get("macd", macd.get("value", 0))
                signal_val = macd.get("signal", 0)
                if macd_val > signal_val:
                    score += 15
                    analysis["key_factors"].append("MACD bullish cross")
                else:
                    score -= 15
                    analysis["key_factors"].append("MACD bearish cross")
            elif isinstance(macd, (int, float)):
                score += 15 if macd > 0 else -15

        if price_change:
            if price_change > 5:
                score += 20
                analysis["key_factors"].append(f"Strong momentum +{price_change:.1f}%")
            elif price_change > 2:
                score += 10
            elif price_change < -5:
                score -= 20
                analysis["key_factors"].append(f"Sharp decline {price_change:.1f}%")
            elif price_change < -2:
                score -= 10

        if volume_change:
            if volume_change > 50:
                score += 10
                analysis["key_factors"].append(f"Volume surge +{volume_change:.0f}%")
            elif volume_change < -30:
                score -= 5

        if sma50 and sma200:
            if sma50 > sma200:
                score += 15
                analysis["key_factors"].append("Golden cross (SMA50 > SMA200)")
            else:
                score -= 15
                analysis["key_factors"].append("Death cross (SMA50 < SMA200)")

        # Sentiment rules
        sentiment = data.get("sentiment") or data.get("market_sentiment")
        if sentiment:
            if isinstance(sentiment, str):
                if sentiment.lower() in ("bullish", "positive", "greed", "extreme greed"):
                    score += 10
                elif sentiment.lower() in ("bearish", "negative", "fear", "extreme fear"):
                    score -= 10
            elif isinstance(sentiment, (int, float)):
                score += int((sentiment - 50) / 5)

        # Map score to direction
        score = max(-100, min(100, score))
        if score >= 20:
            analysis["direction"] = "BULLISH"
        elif score <= -20:
            analysis["direction"] = "BEARISH"
        else:
            analysis["direction"] = "NEUTRAL"

        analysis["confidence"] = round(min(0.95, 0.4 + abs(score) / 120), 2)
        analysis["risk_level"] = "LOW" if abs(score) < 25 else ("HIGH" if abs(score) > 60 else "MEDIUM")
        analysis["rule_score"] = score

        symbol = data.get("symbol", "asset")
        analysis["summary"] = (
            f"Rule-based analysis for {symbol}: score {score}/100 -> {analysis['direction']} "
            f"with {analysis['confidence']:.0%} confidence. "
            f"Factors: {', '.join(analysis['key_factors'][:5]) or 'insufficient data'}."
        )

        return {"success": True, "analysis": analysis, "model": "rule_engine_v3"}


# ---------------------------------------------------------------------------
# Multi-AI Coordinator
# ---------------------------------------------------------------------------

class MultiAICoordinator:
    """
    Orchestrates multiple AI workers with 5 strategies + caching + shared context.

    Strategies:
        consensus   - All workers vote, weighted aggregation
        fastest     - First successful result wins
        pipeline    - Sequential: each AI builds on prior AI's output
        specialist  - Best worker for the task type
        redundant   - All workers, take highest-confidence result
    """

    # Optimal AI assignment: each task type routed to the best-suited model
    TASK_SPECIALISTS = {
        "technical_analysis": "rule_based",     # instant, deterministic
        "sentiment_analysis": "openai",         # GPT-4o: best for nuanced sentiment
        "price_prediction": "deepseek",         # DeepSeek: strong reasoning for forecasts
        "risk_assessment": "rule_based",        # instant, deterministic
        "market_overview": "gemini",            # Gemini: fast, great for broad summaries
        "whale_analysis": "rule_based",         # instant, deterministic
        "gem_analysis": "deepseek",             # DeepSeek: deep reasoning for hidden gems
        "portfolio_analysis": "openai",         # GPT-4o: complex multi-asset analysis
        "news_analysis": "gemini",              # Gemini: fast news processing
        "deep_analysis": "anthropic",           # Claude: careful, thorough analysis
        "correlation_analysis": "deepseek",     # DeepSeek: quantitative reasoning
        "pattern_recognition": "openai",        # GPT-4o: strong pattern recognition
    }

    def __init__(self, max_workers: int = 8, cache_ttl: int = 300):
        self.workers: List[AIWorker] = []
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._session = _build_session()
        self.cache = ResponseCache(max_size=500, default_ttl=cache_ttl)
        self.shared_context = SharedContext(max_entries=300)
        self._weights: Dict[str, float] = {}  # worker_name -> weight (0-1)
        self._lock = threading.Lock()

        self._auto_register()

    # ---- registration -----------------------------------------------------

    def _auto_register(self):
        """Detect and register available AI providers."""
        # Rule-based (always available, instant)
        self._register("RuleEngine", "rule_based", {})

        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key and not openai_key.startswith("your_"):
            self._register("OpenAI-GPT4", "openai", {
                "api_key": openai_key,
                "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
            })

        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        if anthropic_key and not anthropic_key.startswith("your_"):
            self._register("Anthropic-Claude", "anthropic", {
                "api_key": anthropic_key,
                "model": "claude-sonnet-4-20250514",
            })

        # DeepSeek
        deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
        if deepseek_key and not deepseek_key.startswith("your_"):
            self._register("DeepSeek-R1", "deepseek", {
                "api_key": deepseek_key,
                "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            })

        # Gemini
        gemini_key = os.getenv("GOOGLE_AI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        if gemini_key and not gemini_key.startswith("your_"):
            self._register("Gemini-Flash", "gemini", {
                "api_key": gemini_key,
                "model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            })

        # Ollama (local)
        try:
            r = self._session.get("http://localhost:11434/api/tags", timeout=2)
            if r.status_code == 200:
                models = r.json().get("models", [])
                if models:
                    self._register("Ollama-Local", "ollama", {
                        "base_url": "http://localhost:11434",
                        "model": models[0]["name"],
                    })
        except Exception:
            pass

        logger.info("MultiAICoordinator: %d workers registered: %s",
                     len(self.workers), [w.name for w in self.workers])

    def _register(self, name: str, provider: str, config: dict):
        worker = AIWorker(name, provider, config, self._session)
        self.workers.append(worker)
        self._weights[name] = 1.0

    # ---- public API -------------------------------------------------------

    def analyze(
        self,
        task_type: str,
        prompt: str,
        data: dict,
        strategy: str = "consensus",
        timeout: int = 30,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None,
    ) -> dict:
        """
        Run an analysis task through the AI system.

        Args:
            task_type: Category of task (technical_analysis, sentiment, etc.)
            prompt: The question / instruction
            data: Market data dict
            strategy: consensus | fastest | pipeline | specialist | redundant
            timeout: Max seconds to wait
            use_cache: Whether to check/store cache
            cache_ttl: Override default cache TTL for this call

        Returns:
            Combined result dict with 'success', 'analysis', metadata
        """
        # 1. Cache check
        if use_cache:
            cached = self.cache.get(task_type, prompt, data)
            if cached:
                cached["from_cache"] = True
                return cached

        # 2. Build shared context for the symbol
        symbol = data.get("symbol", "")
        context = self.shared_context.get_symbol_context(symbol) if symbol else None

        # 3. Execute strategy
        strategy_fn = {
            "consensus": self._consensus_strategy,
            "fastest": self._fastest_strategy,
            "pipeline": self._pipeline_strategy,
            "specialist": self._specialist_strategy,
            "redundant": self._redundant_strategy,
        }.get(strategy, self._consensus_strategy)

        result = strategy_fn(task_type, prompt, data, timeout, context)

        # 4. Store in cache + shared context
        if result.get("success") and use_cache:
            self.cache.put(task_type, prompt, data, result, ttl=cache_ttl)

        if result.get("success") and symbol:
            self.shared_context.store(
                f"analysis:{symbol}:{task_type}",
                {
                    "direction": result.get("analysis", {}).get("direction"),
                    "confidence": result.get("analysis", {}).get("confidence"),
                    "task": task_type,
                    "time": datetime.now(timezone.utc).isoformat(),
                },
                ttl=900,
            )

        result["strategy"] = strategy
        result["timestamp"] = datetime.now(timezone.utc).isoformat()
        result["workers_available"] = len(self.workers)
        return result

    def quick_analysis(self, symbol: str, data: dict) -> dict:
        """Fast analysis — specialist strategy, short timeout."""
        prompt = f"Quick technical analysis for {symbol}. Key levels, trend, action."
        return self.analyze("technical_analysis", prompt, {**data, "symbol": symbol},
                            strategy="specialist", timeout=15, cache_ttl=120)

    def deep_analysis(self, symbol: str, data: dict) -> dict:
        """Deep analysis — consensus strategy, longer timeout."""
        prompt = (
            f"Comprehensive analysis for {symbol}. "
            "Cover technicals, sentiment, risk, catalysts, and trajectory."
        )
        return self.analyze("deep_analysis", prompt, {**data, "symbol": symbol},
                            strategy="consensus", timeout=45, cache_ttl=600)

    # ---- strategies -------------------------------------------------------

    def _consensus_strategy(self, task_type, prompt, data, timeout, context):
        """All workers vote; weighted aggregation."""
        if not self.workers:
            return {"success": False, "error": "No AI workers available"}

        futures = {}
        for w in self.workers:
            f = self._executor.submit(w.execute, task_type, prompt, data, context)
            futures[f] = w

        results = []
        for f in as_completed(futures, timeout=timeout):
            try:
                r = f.result(timeout=2)
                if r.get("success"):
                    results.append(r)
            except Exception:
                pass

        if not results:
            return {"success": False, "error": "All workers failed in consensus"}

        return self._aggregate_consensus(results)

    def _fastest_strategy(self, task_type, prompt, data, timeout, context):
        """Return the first successful result."""
        if not self.workers:
            return {"success": False, "error": "No AI workers available"}

        # Sort workers by avg latency to submit fastest first
        sorted_workers = sorted(self.workers, key=lambda w: w.avg_latency)

        futures = {}
        for w in sorted_workers:
            f = self._executor.submit(w.execute, task_type, prompt, data, context)
            futures[f] = w

        for f in as_completed(futures, timeout=timeout):
            try:
                r = f.result(timeout=2)
                if r.get("success"):
                    r["strategy_note"] = "fastest_winner"
                    return r
            except Exception:
                continue

        return {"success": False, "error": "All workers failed in fastest"}

    def _specialist_strategy(self, task_type, prompt, data, timeout, context):
        """Use the best-suited worker for this task type."""
        preferred = self.TASK_SPECIALISTS.get(task_type)

        # Find specialist
        specialist = None
        fallback = None
        for w in self.workers:
            if w.provider == preferred:
                specialist = w
                break
            if fallback is None:
                fallback = w

        chosen = specialist or fallback
        if not chosen:
            return {"success": False, "error": "No specialist available"}

        try:
            result = chosen.execute(task_type, prompt, data, context)
            if result.get("success"):
                result["specialist_used"] = chosen.name
                return result
        except Exception:
            pass

        # Fallback to rule engine
        for w in self.workers:
            if w.provider == "rule_based":
                return w.execute(task_type, prompt, data, context)

        return {"success": False, "error": "Specialist and fallback failed"}

    def _redundant_strategy(self, task_type, prompt, data, timeout, context):
        """All workers run, take highest-confidence result."""
        if not self.workers:
            return {"success": False, "error": "No AI workers available"}

        futures = {}
        for w in self.workers:
            f = self._executor.submit(w.execute, task_type, prompt, data, context)
            futures[f] = w

        results = []
        for f in as_completed(futures, timeout=timeout):
            try:
                r = f.result(timeout=2)
                if r.get("success"):
                    results.append(r)
            except Exception:
                pass

        if not results:
            return {"success": False, "error": "All workers failed in redundant"}

        best = max(results, key=lambda r: r.get("analysis", {}).get("confidence", 0))
        best["alternatives_count"] = len(results) - 1
        return best

    def _pipeline_strategy(self, task_type, prompt, data, timeout, context):
        """Sequential: each worker builds on the previous worker's result."""
        if not self.workers:
            return {"success": False, "error": "No AI workers available"}

        sorted_workers = sorted(self.workers, key=lambda w: w.priority)

        accumulated_context = dict(context) if context else {}
        last_result = None

        for w in sorted_workers:
            try:
                result = w.execute(task_type, prompt, data, accumulated_context)
                if result.get("success"):
                    last_result = result
                    # Feed this result into context for next worker
                    analysis = result.get("analysis", {})
                    accumulated_context.setdefault("recent_analyses", [])
                    accumulated_context["recent_analyses"].insert(0, {
                        "worker": w.name,
                        "direction": analysis.get("direction"),
                        "confidence": analysis.get("confidence"),
                        "key_factors": analysis.get("key_factors", [])[:3],
                    })
            except Exception:
                continue

        if last_result:
            last_result["pipeline_stages"] = len(sorted_workers)
            return last_result

        return {"success": False, "error": "Pipeline: all stages failed"}

    # ---- aggregation ------------------------------------------------------

    def _aggregate_consensus(self, results: List[dict]) -> dict:
        """Weighted voting on direction + confidence merge."""
        direction_scores = {"BULLISH": 0.0, "BEARISH": 0.0, "NEUTRAL": 0.0}
        total_weight = 0.0
        all_factors = []
        confidences = []
        summaries = []

        for r in results:
            analysis = r.get("analysis", {})
            worker_name = r.get("worker", "")
            weight = self._weights.get(worker_name, 1.0)

            # Adjust weight by success rate
            for w in self.workers:
                if w.name == worker_name:
                    weight *= (0.5 + 0.5 * w.success_rate)
                    break

            direction = analysis.get("direction", "NEUTRAL").upper()
            if direction not in direction_scores:
                direction = "NEUTRAL"

            conf = analysis.get("confidence", 0.5)
            direction_scores[direction] += conf * weight
            total_weight += weight
            confidences.append(conf)
            all_factors.extend(analysis.get("key_factors", []))
            if analysis.get("summary"):
                summaries.append(analysis["summary"])

        # Winning direction
        winning_dir = max(direction_scores, key=direction_scores.get)
        winning_score = direction_scores[winning_dir]
        total_score = sum(direction_scores.values())
        agreement = winning_score / total_score if total_score else 0.5

        # Merged confidence
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.5
        merged_conf = round(min(0.98, avg_conf * (0.7 + 0.3 * agreement)), 2)

        # Risk
        risk = "LOW" if merged_conf > 0.75 else ("HIGH" if merged_conf < 0.45 else "MEDIUM")

        # Dedupe factors
        seen = set()
        unique_factors = []
        for f in all_factors:
            if f not in seen:
                seen.add(f)
                unique_factors.append(f)

        merged_analysis = {
            "direction": winning_dir,
            "confidence": merged_conf,
            "risk_level": risk,
            "key_factors": unique_factors[:10],
            "agreement_ratio": round(agreement, 2),
            "voters": len(results),
            "summary": summaries[0] if summaries else f"Consensus: {winning_dir} ({merged_conf:.0%})",
        }

        return {
            "success": True,
            "analysis": merged_analysis,
            "consensus_details": {
                "direction_scores": {k: round(v, 2) for k, v in direction_scores.items()},
                "individual_results": [
                    {
                        "worker": r.get("worker"),
                        "direction": r.get("analysis", {}).get("direction"),
                        "confidence": r.get("analysis", {}).get("confidence"),
                        "latency_ms": r.get("latency_ms"),
                    }
                    for r in results
                ],
            },
        }

    # ---- weights ----------------------------------------------------------

    def set_weight(self, worker_name: str, weight: float):
        """Set the weight of a worker (used by learning system)."""
        self._weights[worker_name] = max(0.1, min(2.0, weight))

    def get_weights(self) -> Dict[str, float]:
        return dict(self._weights)

    # ---- stats & lifecycle ------------------------------------------------

    def get_stats(self) -> dict:
        worker_stats = [w.get_stats() for w in self.workers]
        return {
            "workers": worker_stats,
            "weights": self._weights,
            "cache": self.cache.stats(),
            "shared_context_size": len(self.shared_context._data),
            "total_tasks": sum(w.tasks_completed + w.tasks_failed for w in self.workers),
        }

    def shutdown(self):
        """Clean shutdown."""
        self._executor.shutdown(wait=False)
        self._session.close()
        self.cache.invalidate_all()
        self.shared_context.clear()
        logger.info("MultiAICoordinator shut down.")


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_coordinator: Optional[MultiAICoordinator] = None
_coordinator_lock = threading.Lock()


def get_coordinator() -> MultiAICoordinator:
    """Get or create the global coordinator instance."""
    global _coordinator
    if _coordinator is None:
        with _coordinator_lock:
            if _coordinator is None:
                _coordinator = MultiAICoordinator()
    return _coordinator
