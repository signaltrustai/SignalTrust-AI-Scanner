#!/usr/bin/env python3
"""
ASI1 AI Integration Module
Integrates with Groq for advanced market analysis
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class ASI1AIIntegration:
    """AI Integration for market analysis using Groq
    
    Note: Despite the class name 'ASI1AIIntegration', this now uses Groq.
    The name is kept for backward compatibility with existing code.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq integration.
        
        Args:
            api_key: Groq API key (defaults to environment variable)
        """
        self.api_key = api_key or os.environ.get('GROQ_API_KEY', '')
        self.model = os.environ.get('GROQ_MODEL', 'llama3-70b-8192')
        self._client = None
        self.session_id = self._generate_session_id()
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        return f"signaltrust-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _get_client(self):
        """Lazy load Groq client (uses OpenAI-compatible SDK)."""
        if self._client is None and self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
            except ImportError:
                print("⚠️ OpenAI library not installed. Install with: pip install openai")
                raise
        return self._client
    
    def analyze_market_with_ai(self, market_data: Dict, context: str = "") -> Dict:
        """Analyze market data using ASI1 AI.
        
        Args:
            market_data: Market data to analyze
            context: Additional context for analysis
            
        Returns:
            AI analysis results
        """
        try:
            prompt = f"""Analyze the following market data and provide insights:

Market Data: {json.dumps(market_data, indent=2)}

Context: {context}

Please provide:
1. Key trends and patterns
2. Risk assessment
3. Trading opportunities
4. Price predictions
5. Recommended actions"""

            response = self._chat_completion(prompt)
            
            return {
                'success': True,
                'analysis': response.get('content', ''),
                'timestamp': datetime.now().isoformat(),
                'model': response.get('model', self.model),
                'provider': 'groq'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def whale_watch_analysis(self, whale_data: Dict) -> Dict:
        """Analyze whale transactions using AI.
        
        Args:
            whale_data: Whale transaction data
            
        Returns:
            Whale movement analysis
        """
        try:
            prompt = f"""Analyze these whale transactions and assess market impact:

Whale Data: {json.dumps(whale_data, indent=2)}

Provide:
1. Transaction significance
2. Potential market impact
3. Whether this indicates bullish or bearish sentiment
4. Recommended investor actions
5. Risk level assessment"""

            response = self._chat_completion(prompt)
            
            return {
                'success': True,
                'whale_analysis': response.get('content', ''),
                'alert_level': self._determine_alert_level(response.get('content', '')),
                'timestamp': datetime.now().isoformat(),
                'provider': 'groq'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_price_movement(self, symbol: str, historical_data: List[Dict]) -> Dict:
        """Predict price movement using AI.
        
        Args:
            symbol: Asset symbol
            historical_data: Historical price data
            
        Returns:
            Price prediction
        """
        try:
            prompt = f"""Analyze historical price data for {symbol} and predict future movement:

Historical Data: {json.dumps(historical_data[-50:], indent=2)}

Provide:
1. Short-term prediction (24h)
2. Medium-term prediction (7 days)
3. Long-term prediction (30 days)
4. Confidence levels
5. Key support and resistance levels
6. Risk factors"""

            response = self._chat_completion(prompt)
            
            return {
                'success': True,
                'symbol': symbol,
                'prediction': response.get('content', ''),
                'timestamp': datetime.now().isoformat(),
                'provider': 'groq'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def communicate_with_agent(self, message: str, agent_context: Dict = None) -> Dict:
        """Communicate with AI for agent-like responses.
        
        Args:
            message: Message to send
            agent_context: Additional context
            
        Returns:
            AI response
        """
        try:
            full_message = f"""Message: {message}

Context: {json.dumps(agent_context, indent=2) if agent_context else 'None'}

Please provide an expert analysis."""

            response = self._chat_completion(full_message)
            
            return {
                'success': True,
                'response': response.get('content', ''),
                'timestamp': datetime.now().isoformat(),
                'provider': 'groq'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _chat_completion(self, user_message: str, enable_agent_protocol: bool = False) -> Dict:
        """Make chat completion request to Groq API (OpenAI-compatible).
        
        Args:
            user_message: User message
            enable_agent_protocol: Enable agent-to-agent communication (not used with Groq)
            
        Returns:
            API response
        """
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not configured. Please set it in your .env file")
        
        try:
            client = self._get_client()
            if not client:
                return {'content': 'Groq client not initialized', 'model': '', 'usage': {}}
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert AI assistant for cryptocurrency and stock market analysis. Provide detailed, accurate insights.'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                'content': response.choices[0].message.content,
                'model': response.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
            
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            return {'content': f'Error: {str(e)}', 'model': '', 'usage': {}}
    
    def _determine_alert_level(self, analysis: str) -> str:
        """Determine alert level from analysis text.
        
        Args:
            analysis: Analysis text
            
        Returns:
            Alert level (low, medium, high, critical)
        """
        analysis_lower = analysis.lower()
        
        if any(word in analysis_lower for word in ['critical', 'urgent', 'immediate', 'major selloff']):
            return 'critical'
        elif any(word in analysis_lower for word in ['high risk', 'significant', 'important', 'substantial']):
            return 'high'
        elif any(word in analysis_lower for word in ['moderate', 'notable', 'considerable']):
            return 'medium'
        else:
            return 'low'
    
    def get_ai_market_summary(self, markets: Dict) -> Dict:
        """Get comprehensive AI-powered market summary.
        
        Args:
            markets: All market data
            
        Returns:
            Market summary with AI insights
        """
        try:
            prompt = f"""Provide a comprehensive market summary based on this data:

{json.dumps(markets, indent=2)}

Include:
1. Overall market sentiment
2. Best opportunities today
3. Assets to watch
4. Risk factors
5. Recommended portfolio allocation
6. Key events impacting markets"""

            response = self._chat_completion(prompt)
            
            return {
                'success': True,
                'summary': response.get('content', ''),
                'timestamp': datetime.now().isoformat(),
                'provider': 'groq'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
