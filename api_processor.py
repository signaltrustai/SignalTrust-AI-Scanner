#!/usr/bin/env python3
"""
Automatic API Processing System
=================================
Centralized API request handler with:
- Rate limiting (token bucket algorithm)
- Automatic retry with exponential backoff
- Response caching with TTL
- Request queue management
- Error handling and failover
- Usage tracking and analytics
- Health monitoring
"""

import os
import time
import json
import hashlib
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict, deque
from enum import Enum
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class Priority(Enum):
    """Request priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class APIStatus(Enum):
    """API health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: int, per_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            rate: Number of requests allowed
            per_seconds: Time window in seconds
        """
        self.rate = rate
        self.per_seconds = per_seconds
        self.tokens = rate
        self.max_tokens = rate
        self.last_update = time.time()
        self.lock = threading.Lock()
        
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False otherwise
        """
        with self.lock:
            now = time.time()
            # Refill tokens based on time passed
            time_passed = now - self.last_update
            self.tokens = min(
                self.max_tokens,
                self.tokens + (time_passed * self.rate / self.per_seconds)
            )
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_time(self) -> float:
        """Calculate wait time until next token is available"""
        with self.lock:
            if self.tokens >= 1:
                return 0.0
            tokens_needed = 1 - self.tokens
            return (tokens_needed * self.per_seconds / self.rate)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current rate limiter status"""
        return {
            "tokens_available": int(self.tokens),
            "max_tokens": self.max_tokens,
            "rate": f"{self.rate}/{self.per_seconds}s",
            "wait_time_seconds": self.wait_time()
        }


class CacheManager:
    """Response cache manager with TTL"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Initialize cache manager.
        
        Args:
            max_size: Maximum number of cached items
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, Dict] = {}
        self.access_times: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0
        
    def _make_key(self, method: str, url: str, params: Dict = None, data: Dict = None) -> str:
        """Generate cache key from request parameters"""
        key_data = f"{method}:{url}:{json.dumps(params, sort_keys=True)}:{json.dumps(data, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, method: str, url: str, params: Dict = None, data: Dict = None) -> Optional[Dict]:
        """Get cached response if available and not expired"""
        key = self._make_key(method, url, params, data)
        
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            entry = self.cache[key]
            if time.time() > entry["expires_at"]:
                # Expired
                del self.cache[key]
                del self.access_times[key]
                self.misses += 1
                return None
            
            # Update access time
            self.access_times[key] = time.time()
            self.hits += 1
            return entry["response"]
    
    def set(
        self,
        method: str,
        url: str,
        response: Dict,
        params: Dict = None,
        data: Dict = None,
        ttl: Optional[int] = None
    ):
        """Cache a response"""
        key = self._make_key(method, url, params, data)
        ttl = ttl or self.default_ttl
        
        with self.lock:
            # Evict oldest if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                oldest_key = min(self.access_times, key=self.access_times.get)
                del self.cache[oldest_key]
                del self.access_times[oldest_key]
            
            self.cache[key] = {
                "response": response,
                "expires_at": time.time() + ttl,
                "cached_at": time.time()
            }
            self.access_times[key] = time.time()
    
    def invalidate(self, method: str = None, url: str = None):
        """Invalidate cached entries"""
        with self.lock:
            if method is None and url is None:
                # Clear all
                self.cache.clear()
                self.access_times.clear()
            else:
                # Clear matching entries
                keys_to_delete = []
                for key in list(self.cache.keys()):
                    entry_method, entry_url = self.cache[key].get("method", ""), self.cache[key].get("url", "")
                    if (method is None or entry_method == method) and (url is None or entry_url in url):
                        keys_to_delete.append(key)
                
                for key in keys_to_delete:
                    del self.cache[key]
                    if key in self.access_times:
                        del self.access_times[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 3) if total > 0 else 0.0,
            "memory_usage_bytes": sum(
                len(json.dumps(entry["response"])) 
                for entry in self.cache.values()
            )
        }


class HealthMonitor:
    """API health monitoring"""
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize health monitor.
        
        Args:
            check_interval: Seconds between health checks
        """
        self.check_interval = check_interval
        self.api_status: Dict[str, APIStatus] = {}
        self.last_check: Dict[str, float] = {}
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.response_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.lock = threading.Lock()
    
    def record_request(self, api_name: str, success: bool, response_time: float):
        """Record API request result"""
        with self.lock:
            if success:
                self.error_counts[api_name] = max(0, self.error_counts[api_name] - 1)
                self.api_status[api_name] = APIStatus.HEALTHY
            else:
                self.error_counts[api_name] += 1
                # Determine status based on error count
                if self.error_counts[api_name] > 10:
                    self.api_status[api_name] = APIStatus.DOWN
                elif self.error_counts[api_name] > 3:
                    self.api_status[api_name] = APIStatus.DEGRADED
            
            self.response_times[api_name].append(response_time)
            self.last_check[api_name] = time.time()
    
    def get_status(self, api_name: str) -> APIStatus:
        """Get API health status"""
        with self.lock:
            return self.api_status.get(api_name, APIStatus.UNKNOWN)
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get all API statuses"""
        with self.lock:
            result = {}
            for api_name in self.api_status:
                times = list(self.response_times[api_name])
                avg_time = sum(times) / len(times) if times else 0
                
                result[api_name] = {
                    "status": self.api_status[api_name].value,
                    "error_count": self.error_counts[api_name],
                    "avg_response_time": round(avg_time, 3),
                    "last_check": self.last_check.get(api_name, 0),
                    "requests_tracked": len(times)
                }
            return result


class APIProcessor:
    """
    Automatic API processing system with rate limiting, caching, retry logic, and monitoring.
    """
    
    def __init__(
        self,
        default_rate_limit: int = 60,
        default_cache_ttl: int = 300,
        max_retries: int = 3,
        retry_backoff: float = 2.0
    ):
        """
        Initialize API processor.
        
        Args:
            default_rate_limit: Default requests per minute
            default_cache_ttl: Default cache TTL in seconds
            max_retries: Maximum retry attempts
            retry_backoff: Exponential backoff multiplier
        """
        self.default_rate_limit = default_rate_limit
        self.default_cache_ttl = default_cache_ttl
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        
        # Components
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.cache_manager = CacheManager(default_ttl=default_cache_ttl)
        self.health_monitor = HealthMonitor()
        
        # Request tracking
        self.request_count = defaultdict(int)
        self.error_count = defaultdict(int)
        self.total_requests = 0
        self.lock = threading.Lock()
        
        # HTTP session with connection pooling
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_backoff,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        logger.info("APIProcessor initialized")
    
    def register_api(
        self,
        api_name: str,
        rate_limit: Optional[int] = None,
        per_seconds: int = 60
    ):
        """
        Register an API with specific rate limit.
        
        Args:
            api_name: Name of the API
            rate_limit: Requests allowed per time window
            per_seconds: Time window in seconds
        """
        rate_limit = rate_limit or self.default_rate_limit
        self.rate_limiters[api_name] = RateLimiter(rate_limit, per_seconds)
        logger.info(f"Registered API: {api_name} with limit {rate_limit}/{per_seconds}s")
    
    def request(
        self,
        method: str,
        url: str,
        api_name: str = "default",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 30,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None,
        priority: Priority = Priority.NORMAL,
        retry_on_error: bool = True
    ) -> Dict[str, Any]:
        """
        Make an API request with automatic processing.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            api_name: API identifier for rate limiting
            params: Query parameters
            data: Request body data
            headers: Request headers
            timeout: Request timeout in seconds
            use_cache: Whether to use caching
            cache_ttl: Cache TTL override
            priority: Request priority
            retry_on_error: Whether to retry on errors
            
        Returns:
            Response dictionary with success status and data/error
        """
        start_time = time.time()
        
        # Check cache first for GET requests
        if method.upper() == "GET" and use_cache:
            cached = self.cache_manager.get(method, url, params, data)
            if cached:
                logger.debug(f"Cache hit for {url}")
                return {
                    "success": True,
                    "data": cached,
                    "cached": True,
                    "response_time": 0
                }
        
        # Ensure API is registered
        if api_name not in self.rate_limiters:
            self.register_api(api_name)
        
        # Wait for rate limit
        rate_limiter = self.rate_limiters[api_name]
        while not rate_limiter.consume():
            wait_time = rate_limiter.wait_time()
            logger.debug(f"Rate limit reached for {api_name}, waiting {wait_time:.2f}s")
            time.sleep(min(wait_time, 1.0))  # Sleep in 1s increments
        
        # Make request with retries
        attempts = 0
        last_error = None
        
        while attempts < (self.max_retries if retry_on_error else 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=timeout
                )
                
                response_time = time.time() - start_time
                
                # Track request
                with self.lock:
                    self.request_count[api_name] += 1
                    self.total_requests += 1
                
                # Record health
                self.health_monitor.record_request(api_name, True, response_time)
                
                # Handle response
                if response.status_code < 400:
                    try:
                        result_data = response.json()
                    except Exception:
                        result_data = {"text": response.text}
                    
                    # Cache successful GET requests
                    if method.upper() == "GET" and use_cache:
                        self.cache_manager.set(
                            method, url, result_data, params, data, cache_ttl
                        )
                    
                    return {
                        "success": True,
                        "data": result_data,
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "cached": False
                    }
                else:
                    # HTTP error
                    last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                    
                    if response.status_code in [429, 503]:  # Rate limit or service unavailable
                        # Exponential backoff
                        backoff_time = self.retry_backoff ** attempts
                        logger.warning(f"API error {response.status_code}, backing off {backoff_time}s")
                        time.sleep(backoff_time)
                        attempts += 1
                        continue
                    else:
                        # Don't retry on other errors
                        break
                        
            except requests.Timeout:
                last_error = "Request timeout"
                logger.warning(f"Timeout for {url} (attempt {attempts + 1})")
            except requests.ConnectionError as e:
                last_error = f"Connection error: {str(e)}"
                logger.warning(f"Connection error for {url} (attempt {attempts + 1})")
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                logger.error(f"Error making request to {url}: {e}")
            
            # Increment attempt counter
            attempts += 1
            if attempts < self.max_retries and retry_on_error:
                backoff_time = self.retry_backoff ** (attempts - 1)
                time.sleep(backoff_time)
        
        # All retries failed
        response_time = time.time() - start_time
        
        with self.lock:
            self.error_count[api_name] += 1
        
        self.health_monitor.record_request(api_name, False, response_time)
        
        return {
            "success": False,
            "error": last_error,
            "attempts": attempts,
            "response_time": response_time
        }
    
    def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for GET requests"""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for POST requests"""
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for PUT requests"""
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """Convenience method for DELETE requests"""
        return self.request("DELETE", url, **kwargs)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        with self.lock:
            return {
                "total_requests": self.total_requests,
                "requests_by_api": dict(self.request_count),
                "errors_by_api": dict(self.error_count),
                "cache": self.cache_manager.get_stats(),
                "rate_limiters": {
                    name: limiter.get_status()
                    for name, limiter in self.rate_limiters.items()
                },
                "health": self.health_monitor.get_all_status()
            }
    
    def clear_cache(self):
        """Clear response cache"""
        self.cache_manager.invalidate()
        logger.info("Cache cleared")
    
    def reset_stats(self):
        """Reset statistics"""
        with self.lock:
            self.request_count.clear()
            self.error_count.clear()
            self.total_requests = 0
        logger.info("Statistics reset")


# Global instance
_processor = None


def get_api_processor() -> APIProcessor:
    """Get or create global API processor instance"""
    global _processor
    if _processor is None:
        _processor = APIProcessor(
            default_rate_limit=int(os.getenv("API_RATE_LIMIT", "60")),
            default_cache_ttl=int(os.getenv("API_CACHE_TTL", "300")),
            max_retries=int(os.getenv("API_MAX_RETRIES", "3"))
        )
        
        # Register known APIs with their rate limits
        _processor.register_api("openai", rate_limit=60, per_seconds=60)
        _processor.register_api("coingecko", rate_limit=50, per_seconds=60)
        _processor.register_api("alphavantage", rate_limit=5, per_seconds=60)
        _processor.register_api("coinpaprika", rate_limit=100, per_seconds=60)
        _processor.register_api("binance", rate_limit=1200, per_seconds=60)
        _processor.register_api("newsapi", rate_limit=100, per_seconds=86400)  # Daily limit
        
    return _processor
