#!/usr/bin/env python3
"""
AI Chat System Module
Unified AI chat interface integrating all AI systems
Owner-only access for now, with subscriber restrictions
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from asi1_integration import ASI1AIIntegration
from ai_market_intelligence import AIMarketIntelligence
from whale_watcher import WhaleWatcher
from config.admin_config import is_admin_email, is_admin_user_id, ADMIN_USER_ID


class AIChatSystem:
    """Unified AI chat system for owner-only access"""
    
    # Owner access control
    OWNER_ID = "owner_admin_001"
    
    def __init__(self, asi1_integration, ai_intelligence, whale_watcher):
        """Initialize AI chat system.
        
        Args:
            asi1_integration: ASI1 AI integration instance
            ai_intelligence: AI Market Intelligence instance
            whale_watcher: Whale Watcher instance
        """
        self.asi1 = asi1_integration
        self.ai_intelligence = ai_intelligence
        self.whale_watcher = whale_watcher
        self.conversation_history = {}
        
    def check_access(self, user_id: str, user_email: str = None) -> bool:
        """Check if user has access to AI chat.
        
        Currently restricted to owner only.
        
        Args:
            user_id: User ID to check
            user_email: User email to check (optional)
            
        Returns:
            True if user has access, False otherwise
        """
        # Check if user_id matches owner
        if is_admin_user_id(user_id):
            return True
        
        # Check if email matches admin email
        if user_email and is_admin_email(user_email):
            return True
        
        # Legacy check for backward compatibility
        return user_id == self.OWNER_ID
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of conversation messages
        """
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def add_to_history(self, user_id: str, role: str, content: str, ai_type: str = "general"):
        """Add message to conversation history.
        
        Args:
            user_id: User ID
            role: Message role (user/assistant)
            content: Message content
            ai_type: Type of AI that generated the response
        """
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'role': role,
            'content': content,
            'ai_type': ai_type,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 50 messages to avoid memory issues
        if len(self.conversation_history[user_id]) > 50:
            self.conversation_history[user_id] = self.conversation_history[user_id][-50:]
    
    def chat(self, user_id: str, message: str, ai_mode: str = "auto", user_email: str = None) -> Dict:
        """Process chat message with AI system.
        
        Args:
            user_id: User ID
            message: User message
            ai_mode: AI mode to use (auto, asi1, intelligence, whale, prediction)
            user_email: User email (optional, for access verification)
            
        Returns:
            AI response with metadata
        """
        # Check access
        if not self.check_access(user_id, user_email):
            return {
                'success': False,
                'error': 'Access restricted',
                'message': 'AI Chat is currently restricted. Contact administrator for access.',
                'ai_type': 'system'
            }
        
        # Add user message to history
        self.add_to_history(user_id, 'user', message)
        
        # Determine which AI to use
        ai_response = None
        ai_type_used = "general"
        
        try:
            if ai_mode == "auto":
                # Auto-detect based on message content
                ai_mode = self._detect_ai_mode(message)
            
            if ai_mode == "asi1":
                # Use ASI1 for general market analysis and conversation
                ai_response = self._chat_with_asi1(message, user_id)
                ai_type_used = "asi1"
                
            elif ai_mode == "intelligence":
                # Use AI Intelligence for market predictions
                ai_response = self._chat_with_intelligence(message)
                ai_type_used = "intelligence"
                
            elif ai_mode == "whale":
                # Use Whale Watcher AI for whale analysis
                ai_response = self._chat_with_whale_ai(message)
                ai_type_used = "whale"
                
            elif ai_mode == "prediction":
                # Use prediction AI
                ai_response = self._chat_with_prediction_ai(message)
                ai_type_used = "prediction"
                
            else:
                # Default to ASI1
                ai_response = self._chat_with_asi1(message, user_id)
                ai_type_used = "asi1"
            
            # Add AI response to history
            self.add_to_history(user_id, 'assistant', ai_response, ai_type_used)
            
            return {
                'success': True,
                'response': ai_response,
                'ai_type': ai_type_used,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error processing chat: {str(e)}"
            return {
                'success': False,
                'error': error_msg,
                'ai_type': ai_type_used
            }
    
    def _detect_ai_mode(self, message: str) -> str:
        """Auto-detect which AI mode to use based on message.
        
        Args:
            message: User message
            
        Returns:
            Detected AI mode
        """
        message_lower = message.lower()
        
        # Whale-related keywords
        if any(word in message_lower for word in ['whale', 'large transaction', 'big transfer', 'nft sale']):
            return "whale"
        
        # Prediction keywords
        if any(word in message_lower for word in ['predict', 'forecast', 'future', 'price target', 'will it']):
            return "prediction"
        
        # Intelligence/analysis keywords
        if any(word in message_lower for word in ['analyze', 'analysis', 'market', 'trend', 'pattern']):
            return "intelligence"
        
        # Default to ASI1 for general conversation
        return "asi1"
    
    def _chat_with_asi1(self, message: str, user_id: str) -> str:
        """Chat with ASI1 AI.
        
        Args:
            message: User message
            user_id: User ID for context
            
        Returns:
            ASI1 response
        """
        # Get conversation context
        history = self.get_conversation_history(user_id)
        recent_messages = history[-5:] if len(history) > 5 else history
        
        # Format context for ASI1
        context = {}
        if recent_messages:
            context['conversation_history'] = [
                {'role': msg['role'], 'content': msg['content']} 
                for msg in recent_messages
            ]
        
        # Chat with ASI1
        result = self.asi1.communicate_with_agent(message, agent_context=context)
        
        if result.get('success'):
            return result.get('response', result.get('content', 'No response from ASI1'))
        else:
            # Provide a helpful fallback response
            return f"I understand your question about: '{message}'. I'm your AI assistant powered by ASI1 technology. How can I help you with market analysis, trading insights, or crypto predictions?"
    
    def _chat_with_intelligence(self, message: str) -> str:
        """Chat with AI Intelligence system.
        
        Args:
            message: User message
            
        Returns:
            Intelligence AI response
        """
        # Perform comprehensive scan
        intelligence = self.ai_intelligence.comprehensive_market_scan()
        
        # Generate predictions through learn_and_predict
        result = self.ai_intelligence.learn_and_predict()
        
        # Format response
        response = f"""🤖 **Market Intelligence AI Analysis**

📊 **Current Market State:**
- Markets Analyzed: {intelligence.get('markets_scanned', {}).get('total', 0)}
- Data Points: {intelligence.get('data_points_processed', 0)}
- Confidence: {result.get('confidence_score', 0)*100:.1f}%

🎯 **AI Predictions:**
"""
        
        # Add predictions
        predictions = result.get('predictions', {})
        short_term = predictions.get('short_term', []) if isinstance(predictions.get('short_term'), list) else []
        medium_term = predictions.get('medium_term', []) if isinstance(predictions.get('medium_term'), list) else []
        
        if short_term:
            response += "\n**24-48h Outlook:**\n"
            for pred in short_term[:3]:
                asset = pred.get('asset', 'N/A') if isinstance(pred, dict) else 'N/A'
                prediction = pred.get('prediction', 'N/A') if isinstance(pred, dict) else 'N/A'
                confidence = pred.get('confidence', 0) if isinstance(pred, dict) else 0
                response += f"• {asset}: {prediction} (Confidence: {confidence}%)\n"
        
        if medium_term:
            response += "\n**7-14d Forecast:**\n"
            for pred in medium_term[:2]:
                trend = pred.get('trend', 'N/A') if isinstance(pred, dict) else str(pred)
                response += f"• {trend}\n"
        
        # Add key insights
        insights = intelligence.get('key_insights', [])
        if insights:
            response += f"\n💡 **AI Insight:** {insights[0] if insights else 'Markets showing normal activity patterns.'}"
        
        return response
    
    def _chat_with_whale_ai(self, message: str) -> str:
        """Chat with Whale Watcher AI.
        
        Args:
            message: User message
            
        Returns:
            Whale AI response
        """
        # Get whale data (owner has full access)
        tx_result = self.whale_watcher.get_whale_transactions(
            user_id='owner_admin_001',
            user_plan='enterprise',
            limit=5
        )
        
        nft_result = self.whale_watcher.get_nft_whale_movements(
            user_id='owner_admin_001',
            user_plan='enterprise',
            limit=3
        )
        
        stats_result = self.whale_watcher.get_whale_statistics(
            user_id='owner_admin_001',
            user_plan='enterprise'
        )
        
        response = """🐋 **Whale Watcher AI**

"""
        
        try:
            if stats_result.get('success'):
                stats = stats_result.get('statistics', {})
                response += f"""📈 **24h Whale Activity:**
- Total Transactions: {stats.get('total_transactions_24h', 0)}
- Total Volume: ${stats.get('total_volume_24h', 0):,.0f}
- Buy Pressure: {stats.get('buy_percentage', 0):.1f}%
- Sell Pressure: {stats.get('sell_percentage', 0):.1f}%

"""
            
            if tx_result.get('success'):
                transactions = tx_result.get('transactions', [])
                if transactions:
                    response += "🔥 **Recent Large Transactions:**\n"
                    for tx in transactions[:3]:
                        if isinstance(tx, dict):
                            amount = tx.get('amount_usd', 0)
                            asset = tx.get('asset', 'Unknown')
                            tx_type = tx.get('type', 'Unknown').upper()
                            chain = tx.get('chain', 'Unknown')
                            time_ago = tx.get('time_ago', 'Recently')
                            response += f"\n• **${amount:,.0f}** {asset} - {tx_type} on {chain} ({time_ago})"
            
            if nft_result.get('success'):
                nft_activity = nft_result.get('movements', [])
                if nft_activity:
                    response += "\n\n🎨 **NFT Whale Activity:**\n"
                    for nft in nft_activity[:2]:
                        if isinstance(nft, dict):
                            collection = nft.get('collection', 'Unknown')
                            price = nft.get('price_eth', 0)
                            response += f"• {collection}: {price} ETH\n"
            
            if stats_result.get('success'):
                stats = stats_result.get('statistics', {})
                sentiment = stats.get('sentiment', 'Neutral')
                response += f"\n🎯 **AI Analysis:** {sentiment} whale sentiment detected."
            
        except Exception as e:
            response += f"\nError analyzing whale data: {str(e)}"
        
        return response
    
    def _chat_with_prediction_ai(self, message: str) -> str:
        """Chat with Prediction AI.
        
        Args:
            message: User message
            
        Returns:
            Prediction AI response
        """
        result = self.ai_intelligence.learn_and_predict()
        
        response = """🔮 **Prediction AI**

Based on comprehensive market analysis, here are my predictions:

"""
        
        if result.get('success'):
            predictions = result.get('predictions', {})
            recommendations = result.get('recommendations', [])
            
            # Add predictions by timeframe
            short_term = predictions.get('short_term', []) if isinstance(predictions.get('short_term'), list) else []
            medium_term = predictions.get('medium_term', []) if isinstance(predictions.get('medium_term'), list) else []
            
            if short_term:
                response += "**Next 24-48 Hours:**\n"
                for pred in short_term[:5]:
                    if isinstance(pred, dict):
                        response += f"• {pred.get('asset', 'N/A')}: {pred.get('prediction', 'N/A')}\n"
                        response += f"  Confidence: {pred.get('confidence', 0)}% | Target: {pred.get('target', 'N/A')}\n"
            
            if medium_term:
                response += "\n**7-14 Day Forecast:**\n"
                for pred in medium_term[:3]:
                    if isinstance(pred, dict):
                        response += f"• {pred.get('trend', 'N/A')}\n"
                    else:
                        response += f"• {str(pred)}\n"
            
            # Add recommendations
            if recommendations and isinstance(recommendations, list):
                response += "\n💡 **AI Recommendations:**\n"
                for rec in recommendations[:3]:
                    if isinstance(rec, dict):
                        response += f"• {rec.get('action', 'N/A')}: {rec.get('asset', 'N/A')}\n"
                        response += f"  Reason: {rec.get('reason', 'N/A')}\n"
            
            response += f"\n📊 **Overall Confidence:** {result.get('confidence_score', 0)*100:.1f}%"
        else:
            response += "Unable to generate predictions at this time. Please try again later."
        
        return response
    
    def get_ai_modes(self) -> List[Dict]:
        """Get available AI modes.
        
        Returns:
            List of AI modes with descriptions
        """
        return [
            {
                'id': 'auto',
                'name': 'Auto-Detect',
                'icon': '🤖',
                'description': 'Automatically selects the best AI for your question'
            },
            {
                'id': 'asi1',
                'name': 'ASI1 Agent',
                'icon': '🧠',
                'description': 'General market conversation and analysis with ASI1'
            },
            {
                'id': 'intelligence',
                'name': 'Market Intelligence',
                'icon': '📊',
                'description': 'Deep market analysis and pattern recognition'
            },
            {
                'id': 'whale',
                'name': 'Whale Watcher',
                'icon': '🐋',
                'description': 'Track and analyze large transactions and whale movements'
            },
            {
                'id': 'prediction',
                'name': 'Prediction AI',
                'icon': '🔮',
                'description': 'Price predictions and market forecasts'
            }
        ]
    
    def clear_history(self, user_id: str):
        """Clear conversation history for user.
        
        Args:
            user_id: User ID
        """
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
