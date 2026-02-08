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
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
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
            
            messages = [{"role": "user", "content": prompt}]
            
            if context and context.get('history'):
                messages = context['history'] + messages
            
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
            provider_type: Type of provider (openai, anthropic, local)
            **kwargs: Provider-specific arguments
            
        Returns:
            AIProvider instance
        """
        # Auto-detect provider if not specified
        if not provider_type:
            provider_type = os.environ.get('AI_PROVIDER', '').lower()
        
        if not provider_type:
            # Auto-detect based on available API keys
            if os.environ.get('OPENAI_API_KEY'):
                provider_type = 'openai'
            elif os.environ.get('ANTHROPIC_API_KEY'):
                provider_type = 'anthropic'
            else:
                provider_type = 'local'
        
        if provider_type == 'openai':
            return OpenAIProvider(**kwargs)
        elif provider_type == 'anthropic':
            return AnthropicProvider(**kwargs)
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
