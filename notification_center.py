#!/usr/bin/env python3
"""
Notification Center Module
Manages all notifications including price alerts, whale movements, and AI insights
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum


class NotificationType(Enum):
    """Types of notifications"""
    PRICE_ALERT = "price_alert"
    WHALE_MOVEMENT = "whale_movement"
    AI_INSIGHT = "ai_insight"
    MARKET_UPDATE = "market_update"
    SYSTEM = "system"
    TRADE_SIGNAL = "trade_signal"


class NotificationPriority(Enum):
    """Notification priorities"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationCenter:
    """Centralized notification management system"""
    
    def __init__(self, notifications_file: str = 'data/notifications.json'):
        """Initialize notification center.
        
        Args:
            notifications_file: Path to notifications database
        """
        self.notifications_file = notifications_file
        self._ensure_data_dir()
        self._load_notifications()
        
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.notifications_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_notifications(self):
        """Load notifications from file."""
        if os.path.exists(self.notifications_file):
            try:
                with open(self.notifications_file, 'r') as f:
                    self.notifications = json.load(f)
            except (json.JSONDecodeError, IOError, FileNotFoundError):
                self.notifications = []
        else:
            self.notifications = []
    
    def _save_notifications(self):
        """Save notifications to file."""
        with open(self.notifications_file, 'w') as f:
            json.dump(self.notifications, f, indent=2)
    
    def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        data: Optional[Dict] = None
    ) -> Dict:
        """Create a new notification.
        
        Args:
            user_id: User ID to notify
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            priority: Priority level
            data: Additional data
            
        Returns:
            Created notification
        """
        notification = {
            'id': self._generate_id(),
            'user_id': user_id,
            'title': title,
            'message': message,
            'type': notification_type.value,
            'priority': priority.value,
            'data': data or {},
            'read': False,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        self.notifications.append(notification)
        self._save_notifications()
        
        return notification
    
    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict]:
        """Get notifications for a user.
        
        Args:
            user_id: User ID
            unread_only: Only return unread notifications
            limit: Maximum number of notifications
            
        Returns:
            List of notifications
        """
        user_notifications = [
            n for n in self.notifications
            if n['user_id'] == user_id
        ]
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n['read']]
        
        # Sort by created_at descending
        user_notifications.sort(key=lambda x: x['created_at'], reverse=True)
        
        return user_notifications[:limit]
    
    def mark_as_read(self, user_or_notif_id: str, notification_id: str = None) -> bool:
        """Mark notification as read.
        
        Supports both signatures:
          mark_as_read(notification_id)          — original
          mark_as_read(user_email, notification_id) — called by app.py
        
        Args:
            user_or_notif_id: User email (when 2 args) or notification_id (when 1 arg)
            notification_id: Notification ID (when 2 args)
            
        Returns:
            Success status
        """
        target_id = notification_id if notification_id else user_or_notif_id
        for notification in self.notifications:
            if notification['id'] == target_id:
                notification['read'] = True
                notification['read_at'] = datetime.now().isoformat()
                self._save_notifications()
                return True
        return False
    
    def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of notifications marked as read
        """
        count = 0
        for notification in self.notifications:
            if notification['user_id'] == user_id and not notification['read']:
                notification['read'] = True
                notification['read_at'] = datetime.now().isoformat()
                count += 1
        
        if count > 0:
            self._save_notifications()
        
        return count
    
    def delete_notification(self, notification_id: str) -> bool:
        """Delete a notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Success status
        """
        original_length = len(self.notifications)
        self.notifications = [
            n for n in self.notifications
            if n['id'] != notification_id
        ]
        
        if len(self.notifications) < original_length:
            self._save_notifications()
            return True
        return False
    
    def clear_old_notifications(self, days: int = 30) -> int:
        """Clear old notifications.
        
        Args:
            days: Age threshold in days
            
        Returns:
            Number of notifications cleared
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        original_length = len(self.notifications)
        
        self.notifications = [
            n for n in self.notifications
            if datetime.fromisoformat(n['created_at']) > cutoff_date
        ]
        
        cleared = original_length - len(self.notifications)
        if cleared > 0:
            self._save_notifications()
        
        return cleared
    
    def get_notification_stats(self, user_id: str) -> Dict:
        """Get notification statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Notification statistics
        """
        user_notifications = [
            n for n in self.notifications
            if n['user_id'] == user_id
        ]
        
        unread_count = len([n for n in user_notifications if not n['read']])
        
        by_type = {}
        by_priority = {}
        
        for notification in user_notifications:
            n_type = notification['type']
            n_priority = notification['priority']
            
            by_type[n_type] = by_type.get(n_type, 0) + 1
            by_priority[n_priority] = by_priority.get(n_priority, 0) + 1
        
        return {
            'total': len(user_notifications),
            'unread': unread_count,
            'read': len(user_notifications) - unread_count,
            'by_type': by_type,
            'by_priority': by_priority
        }
    
    def create_price_alert(self, user_id: str, symbol: str, price: float, condition: str) -> Dict:
        """Create a price alert notification.
        
        Args:
            user_id: User ID
            symbol: Asset symbol
            price: Alert price
            condition: Condition (above, below)
            
        Returns:
            Created notification
        """
        return self.create_notification(
            user_id=user_id,
            title=f"Price Alert: {symbol}",
            message=f"{symbol} is {condition} ${price}",
            notification_type=NotificationType.PRICE_ALERT,
            priority=NotificationPriority.HIGH,
            data={
                'symbol': symbol,
                'price': price,
                'condition': condition
            }
        )
    
    def create_whale_alert(self, user_id: str, transaction_data: Dict) -> Dict:
        """Create a whale movement alert.
        
        Args:
            user_id: User ID
            transaction_data: Transaction details
            
        Returns:
            Created notification
        """
        symbol = transaction_data.get('symbol', 'Unknown')
        amount = transaction_data.get('amount', 0)
        
        return self.create_notification(
            user_id=user_id,
            title=f"🐋 Whale Alert: {symbol}",
            message=f"Large transaction detected: {amount} {symbol}",
            notification_type=NotificationType.WHALE_MOVEMENT,
            priority=NotificationPriority.CRITICAL,
            data=transaction_data
        )
    
    def create_ai_insight(self, user_id: str, insight: str, symbol: Optional[str] = None) -> Dict:
        """Create an AI insight notification.
        
        Args:
            user_id: User ID
            insight: AI-generated insight
            symbol: Related symbol (optional)
            
        Returns:
            Created notification
        """
        title = f"AI Insight: {symbol}" if symbol else "AI Market Insight"
        
        return self.create_notification(
            user_id=user_id,
            title=title,
            message=insight,
            notification_type=NotificationType.AI_INSIGHT,
            priority=NotificationPriority.MEDIUM,
            data={'symbol': symbol} if symbol else {}
        )
    
    # ── Compatibility methods called by app.py ──────────────────────────

    def get_notifications(self, user_email: str, unread_only: bool = False, limit: int = 50) -> List[Dict]:
        """Get notifications by user email (alias used by app.py).

        Args:
            user_email: User email (used as user_id internally)
            unread_only: Only return unread notifications
            limit: Maximum number of notifications

        Returns:
            List of notifications
        """
        return self.get_user_notifications(user_email, unread_only=unread_only, limit=limit)

    def send_whale_alert(self, target: str, symbol: str, value_usd: float, tx_type: str) -> Dict:
        """Send a whale alert notification (called by app.py's background worker).

        Args:
            target: Target user id or 'all_pro_users'
            symbol: Token symbol
            value_usd: Transaction value in USD
            tx_type: Transaction type (transfer, swap, etc.)

        Returns:
            Created notification
        """
        transaction_data = {
            "symbol": symbol or "Unknown",
            "amount": value_usd,
            "value_usd": value_usd,
            "type": tx_type or "transfer",
        }
        if target == "all_pro_users":
            # Broadcast — store under a special user_id; the UI can filter
            return self.create_whale_alert("all_pro_users", transaction_data)
        return self.create_whale_alert(target, transaction_data)

    def send_notification(self, target: str, notification_type: str, message: str) -> Dict:
        """Send a generic notification (called by app.py's background worker).

        Args:
            target: Target user id or 'all_users'
            notification_type: Notification category string
            message: Notification message body

        Returns:
            Created notification
        """
        type_map = {
            "gem_alert": NotificationType.TRADE_SIGNAL,
            "market_opportunities": NotificationType.MARKET_UPDATE,
            "price_alert": NotificationType.PRICE_ALERT,
            "system": NotificationType.SYSTEM,
        }
        n_type = type_map.get(notification_type, NotificationType.SYSTEM)
        return self.create_notification(
            user_id=target,
            title=notification_type.replace("_", " ").title(),
            message=message,
            notification_type=n_type,
            priority=NotificationPriority.MEDIUM,
        )

    def _generate_id(self) -> str:
        """Generate unique notification ID."""
        import uuid
        return f"notif_{uuid.uuid4().hex[:12]}"
