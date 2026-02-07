#!/usr/bin/env python3
"""
Notification AI - Intelligent notification system that learns user preferences
Fully customizable alerts for everything the user wants
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import random


class NotificationAI:
    """AI-powered intelligent notification system."""
    
    def __init__(self):
        """Initialize Notification AI."""
        self.config_file = "data/notification_ai/config.json"
        self.preferences_file = "data/notification_ai/user_preferences.json"
        self.history_file = "data/notification_ai/notification_history.json"
        self.learning_file = "data/notification_ai/ai_learning.json"
        
        self._ensure_directories()
        
        # Load configuration
        self.config = self._load_config()
        self.preferences = self._load_preferences()
        self.history = []
        self.learning = self._load_learning()
        
        # AI Intelligence
        self.ai_iq = 80.0
        self.prediction_accuracy = 0.85
    
    def _ensure_directories(self):
        """Ensure directories exist."""
        directory = "data/notification_ai/"
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def _load_config(self) -> Dict:
        """Load notification configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default configuration
        return {
            "enabled": True,
            "ai_mode": "intelligent",  # intelligent, basic, aggressive, minimal
            "channels": {
                "push": True,
                "email": True,
                "sms": False,
                "webhook": False,
                "telegram": False,
                "discord": False
            },
            "intelligence_level": "high",  # low, medium, high, expert
            "auto_learn": True,
            "quiet_hours": {
                "enabled": False,
                "start": "22:00",
                "end": "08:00"
            }
        }
    
    def _load_preferences(self) -> Dict:
        """Load user notification preferences."""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default preferences - TOUT configurable!
        return {
            "version": "1.0",
            "user_id": "default",
            "created_at": datetime.now().isoformat(),
            
            # CRYPTO ALERTS
            "crypto": {
                "enabled": True,
                "price_change_threshold": 5.0,  # % change
                "volume_spike_threshold": 200.0,  # % increase
                "new_listings": True,
                "specific_coins": ["BTC", "ETH", "SOL", "AVAX"],
                "all_coins": False,
                "custom_conditions": []
            },
            
            # STOCK ALERTS
            "stocks": {
                "enabled": True,
                "price_change_threshold": 3.0,
                "volume_spike": True,
                "earnings_reports": True,
                "specific_stocks": ["AAPL", "TSLA", "NVDA"],
                "sectors": ["tech", "finance"],
                "all_stocks": False
            },
            
            # GEM ALERTS
            "gems": {
                "enabled": True,
                "min_gem_score": 85,
                "explosion_alerts": True,
                "new_discoveries": True,
                "instant_notification": True
            },
            
            # WHALE ALERTS
            "whales": {
                "enabled": True,
                "min_transaction_value": 1000000,  # USD
                "specific_wallets": [],
                "all_movements": False,
                "large_transfers_only": True
            },
            
            # NFT ALERTS
            "nfts": {
                "enabled": True,
                "floor_price_change": 10.0,  # %
                "volume_spike": True,
                "new_collections": True,
                "specific_collections": ["BAYC", "PUNK", "AZUKI"]
            },
            
            # MARKET ALERTS
            "market": {
                "enabled": True,
                "market_crash": True,  # >5% drop
                "market_rally": True,  # >5% gain
                "volatility_spike": True,
                "correlation_breaks": True
            },
            
            # AI PREDICTIONS
            "predictions": {
                "enabled": True,
                "high_confidence_only": True,  # >85%
                "all_predictions": False,
                "accuracy_threshold": 0.85
            },
            
            # NEWS ALERTS
            "news": {
                "enabled": True,
                "breaking_news": True,
                "sentiment_change": True,
                "specific_keywords": ["Bitcoin", "Ethereum", "Fed", "SEC"],
                "sources": ["all"]
            },
            
            # EVOLUTION ALERTS
            "ai_evolution": {
                "enabled": True,
                "level_up": True,
                "accuracy_milestone": True,
                "new_patterns": True
            },
            
            # PRIORITY SETTINGS
            "priorities": {
                "critical": ["whale_large", "gem_explosive", "market_crash"],
                "high": ["price_spike", "new_gem", "prediction_confident"],
                "medium": ["news_breaking", "nft_spike", "ai_evolution"],
                "low": ["general_update", "daily_summary"]
            },
            
            # FREQUENCY CONTROL
            "frequency": {
                "max_per_hour": 20,
                "max_per_day": 100,
                "batch_similar": True,
                "summary_mode": False
            },
            
            # CUSTOM RULES
            "custom_rules": [
                {
                    "name": "BTC_PUMP",
                    "condition": "BTC price > $50000 AND volume > 200%",
                    "action": "notify_instant",
                    "priority": "critical"
                }
            ]
        }
    
    def _load_learning(self) -> Dict:
        """Load AI learning data."""
        if os.path.exists(self.learning_file):
            try:
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "total_notifications_sent": 0,
            "notifications_read": 0,
            "notifications_acted_on": 0,
            "user_engagement_rate": 0.0,
            "learned_preferences": {},
            "optimal_times": [],
            "preferred_types": [],
            "ignored_types": []
        }
    
    def configure(self, preferences: Dict) -> Dict:
        """Configure notification preferences.
        
        Args:
            preferences: User preferences dictionary
            
        Returns:
            Success status
        """
        # Update preferences
        for key, value in preferences.items():
            if key in self.preferences:
                if isinstance(value, dict):
                    self.preferences[key].update(value)
                else:
                    self.preferences[key] = value
        
        self._save_preferences()
        
        return {
            "success": True,
            "message": "Preferences updated",
            "config": self.preferences
        }
    
    def should_notify(self, notification_type: str, data: Dict) -> Dict:
        """AI decides if notification should be sent.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            
        Returns:
            Decision with reasoning
        """
        # Check if enabled
        if not self.config["enabled"]:
            return {"notify": False, "reason": "Notifications disabled"}
        
        # Check quiet hours
        if self._is_quiet_hours():
            priority = self._get_priority(notification_type, data)
            if priority not in ["critical"]:
                return {"notify": False, "reason": "Quiet hours"}
        
        # Check frequency limits
        if self._exceeds_frequency_limit():
            return {"notify": False, "reason": "Frequency limit exceeded"}
        
        # AI intelligent decision
        decision = self._ai_decide(notification_type, data)
        
        return decision
    
    def send_notification(self, notification_type: str, data: Dict) -> Dict:
        """Send intelligent notification.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            
        Returns:
            Status of notification
        """
        # AI decision
        decision = self.should_notify(notification_type, data)
        
        if not decision["notify"]:
            return {
                "sent": False,
                "reason": decision["reason"]
            }
        
        # Get priority
        priority = self._get_priority(notification_type, data)
        
        # Format notification
        notification = self._format_notification(notification_type, data, priority)
        
        # Send through channels
        channels_sent = []
        for channel, enabled in self.config["channels"].items():
            if enabled:
                self._send_to_channel(channel, notification)
                channels_sent.append(channel)
        
        # Save to history
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "type": notification_type,
            "priority": priority,
            "data": data,
            "channels": channels_sent,
            "read": False,
            "acted_on": False
        })
        
        # Update learning
        self.learning["total_notifications_sent"] += 1
        self._save_learning()
        self._save_history()
        
        return {
            "sent": True,
            "priority": priority,
            "channels": channels_sent,
            "notification": notification
        }
    
    def _ai_decide(self, notification_type: str, data: Dict) -> Dict:
        """AI makes intelligent decision about notification.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            
        Returns:
            Decision with reasoning and confidence
        """
        # Base decision on preferences
        notify = False
        reason = ""
        confidence = 0.0
        
        # Check type-specific preferences
        if notification_type == "crypto_price":
            prefs = self.preferences["crypto"]
            if prefs["enabled"]:
                change = abs(data.get("price_change_percent", 0))
                if change >= prefs["price_change_threshold"]:
                    notify = True
                    reason = f"Price change {change}% exceeds threshold"
                    confidence = min(1.0, change / 20)  # Higher change = higher confidence
        
        elif notification_type == "gem_discovery":
            prefs = self.preferences["gems"]
            if prefs["enabled"]:
                score = data.get("gem_score", 0)
                if score >= prefs["min_gem_score"]:
                    notify = True
                    reason = f"Gem score {score} above threshold"
                    confidence = score / 100
        
        elif notification_type == "whale_transaction":
            prefs = self.preferences["whales"]
            if prefs["enabled"]:
                value = data.get("value_usd", 0)
                if value >= prefs["min_transaction_value"]:
                    notify = True
                    reason = f"Whale transaction ${value:,.0f}"
                    confidence = min(1.0, value / 10000000)
        
        elif notification_type == "ai_evolution":
            prefs = self.preferences["ai_evolution"]
            if prefs["enabled"] and prefs["level_up"]:
                notify = True
                reason = "AI evolution event"
                confidence = 0.95
        
        elif notification_type == "market_alert":
            prefs = self.preferences["market"]
            if prefs["enabled"]:
                notify = True
                reason = "Market alert"
                confidence = 0.90
        
        else:
            # Default: notify if enabled
            notify = True
            reason = "Default notification"
            confidence = 0.70
        
        # AI learning adjustment
        if self.config["auto_learn"]:
            # Check learned preferences
            learned_pref = self.learning["learned_preferences"].get(notification_type, 1.0)
            confidence *= learned_pref
            
            # Check engagement rate
            if self.learning["user_engagement_rate"] < 0.3:
                # User ignores many notifications, be more selective
                confidence *= 0.8
        
        # Final decision
        return {
            "notify": notify and confidence > 0.5,
            "reason": reason,
            "confidence": confidence,
            "ai_adjusted": self.config["auto_learn"]
        }
    
    def _get_priority(self, notification_type: str, data: Dict) -> str:
        """Determine notification priority.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            
        Returns:
            Priority level
        """
        priorities = self.preferences["priorities"]
        
        # Check critical conditions
        if notification_type in ["whale_transaction"]:
            value = data.get("value_usd", 0)
            if value > 10000000:  # > $10M
                return "critical"
        
        if notification_type in ["gem_discovery"]:
            score = data.get("gem_score", 0)
            if score > 95:
                return "critical"
        
        if notification_type in ["market_alert"]:
            if "crash" in str(data).lower():
                return "critical"
        
        # Check configured priorities
        for priority, types in priorities.items():
            if any(t in notification_type for t in types):
                return priority
        
        return "medium"
    
    def _format_notification(self, notification_type: str, data: Dict, priority: str) -> Dict:
        """Format notification for sending.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            priority: Priority level
            
        Returns:
            Formatted notification
        """
        # Priority emoji
        priority_emoji = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "📢",
            "low": "ℹ️"
        }
        
        emoji = priority_emoji.get(priority, "📢")
        
        # Create notification
        notification = {
            "id": f"notif_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "type": notification_type,
            "priority": priority,
            "title": f"{emoji} {notification_type.replace('_', ' ').title()}",
            "message": self._generate_message(notification_type, data),
            "data": data,
            "actions": self._generate_actions(notification_type, data)
        }
        
        return notification
    
    def _generate_message(self, notification_type: str, data: Dict) -> str:
        """Generate notification message.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            
        Returns:
            Notification message
        """
        if notification_type == "crypto_price":
            return f"{data.get('symbol')} price changed {data.get('price_change_percent')}% to ${data.get('price')}"
        
        elif notification_type == "gem_discovery":
            return f"💎 New gem discovered: {data.get('symbol')} with score {data.get('gem_score')}/100"
        
        elif notification_type == "whale_transaction":
            return f"🐋 Whale moved ${data.get('value_usd'):,.0f} worth of {data.get('symbol')}"
        
        elif notification_type == "ai_evolution":
            return f"🧠 AI evolved to level {data.get('level')} with IQ {data.get('iq'):.1f}"
        
        else:
            return str(data)
    
    def _generate_actions(self, notification_type: str, data: Dict) -> List[Dict]:
        """Generate actionable buttons for notification.
        
        Args:
            notification_type: Type of notification
            data: Notification data
            
        Returns:
            List of actions
        """
        actions = []
        
        if notification_type == "crypto_price":
            actions = [
                {"label": "View Chart", "action": "view_chart", "data": data.get('symbol')},
                {"label": "Buy", "action": "buy", "data": data.get('symbol')},
                {"label": "Ignore", "action": "ignore", "data": None}
            ]
        
        elif notification_type == "gem_discovery":
            actions = [
                {"label": "Analyze", "action": "analyze_gem", "data": data.get('symbol')},
                {"label": "Add to Watchlist", "action": "watchlist", "data": data.get('symbol')},
                {"label": "Dismiss", "action": "dismiss", "data": None}
            ]
        
        return actions
    
    def _send_to_channel(self, channel: str, notification: Dict):
        """Send notification to specific channel.
        
        Args:
            channel: Channel name
            notification: Notification data
        """
        # In real implementation, send to actual channels
        # For now, just log
        print(f"[{channel.upper()}] {notification['title']}: {notification['message']}")
    
    def _is_quiet_hours(self) -> bool:
        """Check if currently in quiet hours."""
        if not self.config["quiet_hours"]["enabled"]:
            return False
        
        # Simple time check (would be more sophisticated in production)
        current_hour = datetime.now().hour
        return 22 <= current_hour or current_hour < 8
    
    def _exceeds_frequency_limit(self) -> bool:
        """Check if frequency limit exceeded."""
        freq = self.preferences["frequency"]
        
        # Count recent notifications (last hour)
        recent = [h for h in self.history 
                 if (datetime.now() - datetime.fromisoformat(h["timestamp"])).total_seconds() < 3600]
        
        return len(recent) >= freq["max_per_hour"]
    
    def mark_read(self, notification_id: str):
        """Mark notification as read."""
        for notif in self.history:
            if notif.get("id") == notification_id:
                notif["read"] = True
                self.learning["notifications_read"] += 1
                break
        
        self._update_engagement()
        self._save_history()
        self._save_learning()
    
    def mark_acted_on(self, notification_id: str, action: str):
        """Mark notification as acted upon."""
        for notif in self.history:
            if notif.get("id") == notification_id:
                notif["acted_on"] = True
                notif["action_taken"] = action
                self.learning["notifications_acted_on"] += 1
                break
        
        self._update_engagement()
        self._save_history()
        self._save_learning()
    
    def _update_engagement(self):
        """Update user engagement metrics."""
        total = self.learning["total_notifications_sent"]
        if total > 0:
            self.learning["user_engagement_rate"] = self.learning["notifications_read"] / total
    
    def learn_from_feedback(self, notification_type: str, feedback: str):
        """Learn from user feedback.
        
        Args:
            notification_type: Type of notification
            feedback: User feedback (positive, negative, neutral)
        """
        learned = self.learning["learned_preferences"]
        
        current_pref = learned.get(notification_type, 1.0)
        
        if feedback == "positive":
            learned[notification_type] = min(1.5, current_pref * 1.1)
        elif feedback == "negative":
            learned[notification_type] = max(0.5, current_pref * 0.9)
        
        self._save_learning()
    
    def get_config(self) -> Dict:
        """Get current configuration."""
        return {
            "config": self.config,
            "preferences": self.preferences,
            "ai_metrics": {
                "iq": self.ai_iq,
                "prediction_accuracy": self.prediction_accuracy,
                "total_sent": self.learning["total_notifications_sent"],
                "engagement_rate": self.learning["user_engagement_rate"]
            }
        }
    
    def _save_preferences(self):
        """Save preferences."""
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def _save_learning(self):
        """Save learning data."""
        with open(self.learning_file, 'w') as f:
            json.dump(self.learning, f, indent=2)
    
    def _save_history(self):
        """Save notification history."""
        # Keep last 1000 notifications
        self.history = self.history[-1000:]
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)


# Global Notification AI instance
notification_ai = NotificationAI()


if __name__ == "__main__":
    ai = NotificationAI()
    
    print("=" * 80)
    print("🔔 NOTIFICATION AI - Intelligent Alert System")
    print("=" * 80)
    
    # Get config
    config = ai.get_config()
    print(f"\n📊 AI Metrics:")
    print(f"   IQ: {config['ai_metrics']['iq']}")
    print(f"   Accuracy: {config['ai_metrics']['prediction_accuracy']*100:.1f}%")
    print(f"   Total Sent: {config['ai_metrics']['total_sent']}")
    print(f"   Engagement: {config['ai_metrics']['engagement_rate']*100:.1f}%")
    
    # Test notifications
    print("\n📢 Testing Notifications:")
    
    # Crypto price alert
    result = ai.send_notification("crypto_price", {
        "symbol": "BTC",
        "price": 48500,
        "price_change_percent": 8.5
    })
    print(f"   Crypto: {'✅ Sent' if result['sent'] else '❌ Not sent'}")
    
    # Gem discovery
    result = ai.send_notification("gem_discovery", {
        "symbol": "NEWGEM",
        "gem_score": 92
    })
    print(f"   Gem: {'✅ Sent' if result['sent'] else '❌ Not sent'}")
    
    # Whale transaction
    result = ai.send_notification("whale_transaction", {
        "symbol": "ETH",
        "value_usd": 5000000
    })
    print(f"   Whale: {'✅ Sent' if result['sent'] else '❌ Not sent'}")
