#!/usr/bin/env python3
"""
Limit Enforcer Module
Tracks and enforces subscription-based usage limits
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from payment_processor import PaymentProcessor


class LimitEnforcer:
    """Enforces subscription-based usage limits"""
    
    def __init__(self, usage_file: str = 'data/usage_tracking.json'):
        """Initialize limit enforcer.
        
        Args:
            usage_file: Path to usage tracking file
        """
        self.usage_file = usage_file
        self.payment_processor = PaymentProcessor()
        self._ensure_data_dir()
        self._load_usage()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.usage_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_usage(self):
        """Load usage data from file."""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    self.usage = json.load(f)
            except (json.JSONDecodeError, IOError, FileNotFoundError):
                self.usage = {}
        else:
            self.usage = {}
    
    def _save_usage(self):
        """Save usage data to file."""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)
    
    def _get_today_key(self) -> str:
        """Get today's date key for usage tracking.
        
        Returns:
            Date string (YYYY-MM-DD)
        """
        return datetime.now().strftime('%Y-%m-%d')
    
    def _init_user_usage(self, user_id: str):
        """Initialize usage tracking for a user.
        
        Args:
            user_id: User ID
        """
        if user_id not in self.usage:
            self.usage[user_id] = {}
        
        today = self._get_today_key()
        if today not in self.usage[user_id]:
            self.usage[user_id][today] = {
                'scans': 0,
                'ai_predictions': 0,
                'gems_discoveries': 0,
                'symbols_scanned': 0
            }
        
        # Clean up old data (keep only last 7 days)
        cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        dates_to_remove = [
            date for date in self.usage[user_id].keys()
            if date < cutoff_date
        ]
        for date in dates_to_remove:
            del self.usage[user_id][date]
    
    def get_user_limits(self, user_plan: str) -> Dict:
        """Get limits for a user's plan.
        
        Args:
            user_plan: User's subscription plan
            
        Returns:
            Dictionary of limits
        """
        plan = self.payment_processor.get_plan(user_plan)
        if not plan:
            # Default to free plan limits
            plan = self.payment_processor.get_plan('free')
        return plan.get('limits', {})
    
    def get_user_usage(self, user_id: str) -> Dict:
        """Get current usage for a user today.
        
        Args:
            user_id: User ID
            
        Returns:
            Usage statistics
        """
        self._init_user_usage(user_id)
        today = self._get_today_key()
        return self.usage[user_id][today]
    
    def check_limit(
        self,
        user_id: str,
        user_plan: str,
        action: str
    ) -> Tuple[bool, Optional[str], Dict]:
        """Check if user can perform an action.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            action: Action to check (scans, ai_predictions, gems_discoveries)
            
        Returns:
            Tuple of (allowed, error_message, usage_info)
        """
        self._init_user_usage(user_id)
        
        limits = self.get_user_limits(user_plan)
        usage = self.get_user_usage(user_id)
        
        # Map action to limit key
        limit_map = {
            'scans': 'scans_per_day',
            'ai_predictions': 'ai_predictions_per_day',
            'gems_discoveries': 'gems_discoveries_per_day'
        }
        
        if action not in limit_map:
            return False, f"Unknown action: {action}", {}
        
        limit_key = limit_map[action]
        limit = limits.get(limit_key, 0)
        
        # -1 means unlimited
        if limit == -1:
            return True, None, {
                'used': usage.get(action, 0),
                'limit': 'unlimited',
                'remaining': 'unlimited',
                'plan': user_plan
            }
        
        current_usage = usage.get(action, 0)
        
        if current_usage >= limit:
            return False, f"Daily limit reached ({limit} {action} per day). Upgrade to Pro or Enterprise for unlimited access.", {
                'used': current_usage,
                'limit': limit,
                'remaining': 0,
                'plan': user_plan,
                'upgrade_required': True
            }
        
        return True, None, {
            'used': current_usage,
            'limit': limit,
            'remaining': limit - current_usage,
            'plan': user_plan
        }
    
    def increment_usage(
        self,
        user_id: str,
        action: str,
        amount: int = 1
    ) -> Dict:
        """Increment usage counter for a user.
        
        Args:
            user_id: User ID
            action: Action to increment
            amount: Amount to increment by
            
        Returns:
            Updated usage info
        """
        self._init_user_usage(user_id)
        today = self._get_today_key()
        
        if action in self.usage[user_id][today]:
            self.usage[user_id][today][action] += amount
        else:
            self.usage[user_id][today][action] = amount
        
        self._save_usage()
        
        return self.usage[user_id][today]
    
    def check_symbols_limit(
        self,
        user_id: str,
        user_plan: str,
        num_symbols: int
    ) -> Tuple[bool, Optional[str], Dict]:
        """Check if user can scan a number of symbols.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            num_symbols: Number of symbols to scan
            
        Returns:
            Tuple of (allowed, error_message, limit_info)
        """
        limits = self.get_user_limits(user_plan)
        symbols_limit = limits.get('symbols_per_scan', 5)
        
        # -1 means unlimited
        if symbols_limit == -1:
            return True, None, {
                'requested': num_symbols,
                'limit': 'unlimited',
                'plan': user_plan
            }
        
        if num_symbols > symbols_limit:
            return False, f"Too many symbols ({num_symbols}). Your plan allows {symbols_limit} symbols per scan. Upgrade to Pro or Enterprise for unlimited.", {
                'requested': num_symbols,
                'limit': symbols_limit,
                'plan': user_plan,
                'upgrade_required': True
            }
        
        return True, None, {
            'requested': num_symbols,
            'limit': symbols_limit,
            'plan': user_plan
        }
    
    def check_whale_tracking_access(
        self,
        user_plan: str
    ) -> Tuple[bool, Optional[str]]:
        """Check if user has access to whale tracking.
        
        Args:
            user_plan: User's subscription plan
            
        Returns:
            Tuple of (allowed, error_message)
        """
        limits = self.get_user_limits(user_plan)
        has_access = limits.get('whale_tracking', False)
        
        if not has_access:
            return False, "Whale tracking is available for Pro and Enterprise plans only. Please upgrade to access this feature."
        
        return True, None
    
    def check_advanced_analytics_access(
        self,
        user_plan: str
    ) -> Tuple[bool, Optional[str]]:
        """Check if user has access to advanced analytics.
        
        Args:
            user_plan: User's subscription plan
            
        Returns:
            Tuple of (allowed, error_message)
        """
        limits = self.get_user_limits(user_plan)
        has_access = limits.get('advanced_analytics', False)
        
        if not has_access:
            return False, "Advanced analytics is available for Basic, Pro and Enterprise plans. Please upgrade to access this feature."
        
        return True, None
    
    def get_usage_summary(self, user_id: str, user_plan: str) -> Dict:
        """Get complete usage summary for a user.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            
        Returns:
            Usage summary with limits and remaining
        """
        self._init_user_usage(user_id)
        
        limits = self.get_user_limits(user_plan)
        usage = self.get_user_usage(user_id)
        
        def format_limit(used, limit):
            if limit == -1:
                return {
                    'used': used,
                    'limit': 'unlimited',
                    'remaining': 'unlimited',
                    'percentage': 0
                }
            return {
                'used': used,
                'limit': limit,
                'remaining': max(0, limit - used),
                'percentage': round((used / limit * 100) if limit > 0 else 0, 1)
            }
        
        return {
            'plan': user_plan,
            'date': self._get_today_key(),
            'scans': format_limit(
                usage.get('scans', 0),
                limits.get('scans_per_day', 0)
            ),
            'ai_predictions': format_limit(
                usage.get('ai_predictions', 0),
                limits.get('ai_predictions_per_day', 0)
            ),
            'gems_discoveries': format_limit(
                usage.get('gems_discoveries', 0),
                limits.get('gems_discoveries_per_day', 0)
            ),
            'symbols_per_scan': {
                'limit': 'unlimited' if limits.get('symbols_per_scan', 5) == -1 else limits.get('symbols_per_scan', 5)
            },
            'whale_tracking': limits.get('whale_tracking', False),
            'advanced_analytics': limits.get('advanced_analytics', False)
        }


# Global instance
limit_enforcer = LimitEnforcer()
