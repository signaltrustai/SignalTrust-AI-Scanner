#!/usr/bin/env python3
"""
AI Provider Module
Unified interface for multiple AI providers (OpenAI, Anthropic, local models, etc.)
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate AI response from prompt"""
        pass
    
    @abstractmethod
    def analyze_market_data(self, market_data: Dict) -> Dict:
        """Analyze market data with AI"""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4o, gpt-4o-mini, etc.)
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY', '')
        self.model = model
        self._client = None
        
    def _get_client(self):
        """Lazy load OpenAI client"""
        if self._client is None and self.api_key:
            try:
                import openai
                self._client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️ OpenAI library not installed. Install with: pip install openai")
                raise
        return self._client
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using OpenAI"""
        try:
            client = self._get_client()
            if not client:
                return self._fallback_response(prompt)
            
            system_msg = {
                "role": "system",
                "content": (
                    "You are SignalTrust AI, an expert financial market analyst and trading assistant. "
                    "You provide real-time market analysis, technical indicators, crypto and stock insights, "
                    "whale movement analysis, and actionable trading recommendations. "
                    "Be concise, accurate, and data-driven. Use markdown formatting for clarity. "
                    "Always include risk warnings when giving financial advice."
                )
            }
            messages = [system_msg, {"role": "user", "content": prompt}]
            
            if context and context.get('history'):
                messages = [system_msg] + context['history'] + [{"role": "user", "content": prompt}]
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ OpenAI error: {e}")
            return self._fallback_response(prompt)
    
    def analyze_market_data(self, market_data: Dict) -> Dict:
        """Analyze market data with OpenAI"""
        prompt = f"""Analyze the following market data and provide insights:

Market Data:
{json.dumps(market_data, indent=2)}

Please provide:
1. Key trends and patterns
2. Risk assessment (Low/Medium/High)
3. Trading opportunities
4. Price prediction direction (Bullish/Bearish/Neutral)
5. Recommended actions

Format your response as JSON with keys: trends, risk_level, opportunities, prediction, recommendations"""

        try:
            response = self.generate_response(prompt)
            # Try to parse JSON response
            try:
                return json.loads(response)
            except Exception as e:
                print(f"⚠️ OpenAIProvider: failed to parse JSON response: {e}")
                # If not JSON, return structured text
                return {
                    'analysis': response,
                    'success': True,
                    'provider': 'openai',
                    'model': self.model
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'openai'
            }
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when API fails"""
        return "AI analysis unavailable. Please check API configuration."


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key
            model: Model to use
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY', '')
        self.model = model
        self._client = None
        
    def _get_client(self):
        """Lazy load Anthropic client"""
        if self._client is None and self.api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                print("⚠️ Anthropic library not installed. Install with: pip install anthropic")
                raise
        return self._client
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using Anthropic Claude"""
        try:
            client = self._get_client()
            if not client:
                return self._fallback_response(prompt)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"⚠️ Anthropic error: {e}")
            return self._fallback_response(prompt)
    
    def analyze_market_data(self, market_data: Dict) -> Dict:
        """Analyze market data with Claude"""
        prompt = f"""Analyze this market data and provide insights in JSON format:

{json.dumps(market_data, indent=2)}

Return JSON with: trends, risk_level, opportunities, prediction, recommendations"""

        try:
            response = self.generate_response(prompt)
            try:
                return json.loads(response)
            except Exception as e:
                print(f"⚠️ AnthropicProvider: failed to parse JSON response: {e}")
                return {
                    'analysis': response,
                    'success': True,
                    'provider': 'anthropic',
                    'model': self.model
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'anthropic'
            }
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when API fails"""
        return "AI analysis unavailable. Please check API configuration."


class DeepSeekProvider(AIProvider):
    """DeepSeek AI provider — strong at reasoning and code analysis."""

    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat"):
        """Initialize DeepSeek provider.

        Args:
            api_key: DeepSeek API key
            model: Model to use (deepseek-chat, deepseek-reasoner)
        """
        self.api_key = api_key or os.environ.get('DEEPSEEK_API_KEY', '')
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"

    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using DeepSeek."""
        try:
            import requests as _requests

            system_msg = (
                "You are SignalTrust AI, an expert financial market analyst. "
                "Provide data-driven analysis with risk warnings. Use markdown."
            )
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ]
            if context and context.get('history'):
                messages = [{"role": "system", "content": system_msg}] + context['history'] + [{"role": "user", "content": prompt}]

            resp = _requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": messages, "temperature": 0.3, "max_tokens": 2000},
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"⚠️ DeepSeek error: {e}")
            return self._fallback_response(prompt)

    def analyze_market_data(self, market_data: Dict) -> Dict:
        """Analyze market data with DeepSeek."""
        prompt = (
            "Analyze this market data and return JSON with keys: "
            "trends, risk_level, opportunities, prediction, recommendations.\n\n"
            f"{json.dumps(market_data, indent=2)}"
        )
        try:
            response = self.generate_response(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {'analysis': response, 'success': True, 'provider': 'deepseek', 'model': self.model}
        except Exception as e:
            return {'success': False, 'error': str(e), 'provider': 'deepseek'}

    def _fallback_response(self, prompt: str) -> str:
        return "DeepSeek AI unavailable. Please check API configuration."


class GeminiProvider(AIProvider):
    """Google Gemini AI provider — strong at multimodal analysis."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        """Initialize Gemini provider.

        Args:
            api_key: Google AI API key
            model: Model to use (gemini-2.0-flash, gemini-2.5-pro, etc.)
        """
        self.api_key = api_key or os.environ.get('GOOGLE_AI_API_KEY', os.environ.get('GEMINI_API_KEY', ''))
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using Google Gemini."""
        try:
            import requests as _requests

            contents = []
            if context and context.get('history'):
                for msg in context['history']:
                    role = "model" if msg.get("role") == "assistant" else "user"
                    contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            contents.append({"role": "user", "parts": [{"text": prompt}]})

            resp = _requests.post(
                f"{self.base_url}/models/{self.model}:generateContent",
                params={"key": self.api_key},
                headers={"Content-Type": "application/json"},
                json={
                    "contents": contents,
                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2000},
                    "systemInstruction": {
                        "parts": [{"text": (
                            "You are SignalTrust AI, an expert financial market analyst. "
                            "Provide data-driven analysis with risk warnings."
                        )}]
                    },
                },
                timeout=30,
            )
            resp.raise_for_status()
            body = resp.json()
            return body["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"⚠️ Gemini error: {e}")
            return self._fallback_response(prompt)

    def analyze_market_data(self, market_data: Dict) -> Dict:
        """Analyze market data with Gemini."""
        prompt = (
            "Analyze this market data and return JSON with keys: "
            "trends, risk_level, opportunities, prediction, recommendations.\n\n"
            f"{json.dumps(market_data, indent=2)}"
        )
        try:
            response = self.generate_response(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {'analysis': response, 'success': True, 'provider': 'gemini', 'model': self.model}
        except Exception as e:
            return {'success': False, 'error': str(e), 'provider': 'gemini'}

    def _fallback_response(self, prompt: str) -> str:
        return "Google Gemini AI unavailable. Please check API configuration."


class LocalModelProvider(AIProvider):
    """Local model provider using Ollama or similar"""
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        """Initialize local model provider.
        
        Args:
            model: Local model name
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using local model"""
        try:
            import requests
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return self._fallback_response(prompt)
                
        except Exception as e:
            print(f"⚠️ Local model error: {e}")
            return self._fallback_response(prompt)
    
    def analyze_market_data(self, market_data: Dict) -> Dict:
        """Analyze market data with local model"""
        prompt = f"""Analyze this market data:

{json.dumps(market_data, indent=2)}

Provide: trends, risk assessment, opportunities, prediction, recommendations"""

        try:
            response = self.generate_response(prompt)
            return {
                'analysis': response,
                'success': True,
                'provider': 'local',
                'model': self.model
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'local'
            }
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when local model fails"""
        return "Local AI model unavailable. Please check Ollama is running."


class AIProviderFactory:
    """Factory for creating AI providers"""
    
    @staticmethod
    def create_provider(provider_type: str = None, **kwargs) -> AIProvider:
        """Create AI provider instance.
        
        Args:
            provider_type: Type of provider (openai, anthropic, deepseek, gemini, local)
            **kwargs: Provider-specific arguments
            
        Returns:
            AIProvider instance
        """
        # Auto-detect provider if not specified
        if not provider_type:
            provider_type = os.environ.get('AI_PROVIDER', '').lower()
        
        if not provider_type:
            # Auto-detect based on available API keys (priority order)
            if os.environ.get('OPENAI_API_KEY'):
                provider_type = 'openai'
            elif os.environ.get('ANTHROPIC_API_KEY'):
                provider_type = 'anthropic'
            elif os.environ.get('DEEPSEEK_API_KEY'):
                provider_type = 'deepseek'
            elif os.environ.get('GOOGLE_AI_API_KEY') or os.environ.get('GEMINI_API_KEY'):
                provider_type = 'gemini'
            else:
                provider_type = 'local'
        
        if provider_type == 'openai':
            return OpenAIProvider(**kwargs)
        elif provider_type == 'anthropic':
            return AnthropicProvider(**kwargs)
        elif provider_type == 'deepseek':
            return DeepSeekProvider(**kwargs)
        elif provider_type == 'gemini':
            return GeminiProvider(**kwargs)
        elif provider_type == 'local':
            return LocalModelProvider(**kwargs)
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")


class EnhancedAIEngine:
    """Enhanced AI engine with multiple provider support"""
    
    def __init__(self, provider: Optional[AIProvider] = None):
        """Initialize enhanced AI engine.
        
        Args:
            provider: AI provider instance (auto-detected if None)
        """
        self.provider = provider or AIProviderFactory.create_provider()
        self.conversation_history = {}
        
    def analyze_market(self, market_data: Dict, context: Optional[str] = None) -> Dict:
        """Analyze market data with AI.
        
        Args:
            market_data: Market data to analyze
            context: Additional context
            
        Returns:
            Analysis results
        """
        analysis = self.provider.analyze_market_data(market_data)
        
        return {
            'success': analysis.get('success', True),
            'analysis': analysis,
            'timestamp': datetime.now().isoformat(),
            'provider': type(self.provider).__name__
        }
    
    def generate_prediction(self, symbol: str, data: Dict) -> Dict:
        """Generate AI prediction for symbol.
        
        Args:
            symbol: Asset symbol
            data: Historical and current data
            
        Returns:
            Prediction results
        """
        prompt = f"""Analyze {symbol} and provide a price prediction:

Current Data:
{json.dumps(data, indent=2)}

Provide:
1. Short-term prediction (24h): Bullish/Bearish/Neutral with confidence %
2. Medium-term prediction (7 days): Expected price range
3. Key support and resistance levels
4. Risk factors
5. Trading recommendation

Format as JSON."""

        try:
            response = self.provider.generate_response(prompt)
            return {
                'success': True,
                'symbol': symbol,
                'prediction': response,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def chat(self, user_id: str, message: str) -> str:
        """Chat with AI.
        
        Args:
            user_id: User identifier
            message: User message
            
        Returns:
            AI response
        """
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Get response
        context = {'history': self.conversation_history[user_id][-10:]}  # Last 10 messages
        response = self.provider.generate_response(message, context)
        
        # Update history
        self.conversation_history[user_id].append({
            'role': 'user',
            'content': message
        })
        self.conversation_history[user_id].append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def get_market_summary(self, markets: Dict) -> Dict:
        """Get comprehensive AI market summary.
        
        Args:
            markets: All market data
            
        Returns:
            Market summary
        """
        prompt = f"""Provide a comprehensive market summary:

Markets Data:
{json.dumps(markets, indent=2)}

Include:
1. Overall market sentiment
2. Best opportunities today
3. Assets to watch
4. Risk factors
5. Recommended actions"""

        try:
            response = self.provider.generate_response(prompt)
            return {
                'success': True,
                'summary': response,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
