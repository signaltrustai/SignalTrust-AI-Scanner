"""
Flexible Subscription System
Pay-per-feature and modular subscription management
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class SubscriptionManager:
    """Manage flexible subscription plans and features"""
    
    # Base Plans (Foundation)
    BASE_PLANS = {
        'free': {
            'name': 'Free',
            'price_monthly': 0,
            'price_yearly': 0,
            'description': 'Basic market scanning',
            'included_features': ['basic_scanner', 'market_overview'],
            'limits': {
                'daily_scans': 10,
                'ai_requests': 5,
                'watchlist_assets': 10,
                'alerts': 5
            }
        },
        'starter': {
            'name': 'Starter',
            'price_monthly': 19.99,
            'price_yearly': 199.99,  # 2 months free
            'description': 'Essential tools for traders',
            'included_features': [
                'basic_scanner', 'market_overview', 'price_alerts',
                'basic_charts', 'portfolio_tracker'
            ],
            'limits': {
                'daily_scans': 100,
                'ai_requests': 50,
                'watchlist_assets': 50,
                'alerts': 50
            }
        },
        'pro': {
            'name': 'Professional',
            'price_monthly': 49.99,
            'price_yearly': 499.99,
            'description': 'Advanced trading tools',
            'included_features': [
                'basic_scanner', 'market_overview', 'price_alerts',
                'basic_charts', 'portfolio_tracker', 'advanced_scanner',
                'ai_predictions', 'whale_watcher', 'gem_finder',
                'tradingview_integration'
            ],
            'limits': {
                'daily_scans': 500,
                'ai_requests': 200,
                'watchlist_assets': 200,
                'alerts': 200
            }
        },
        'enterprise': {
            'name': 'Enterprise',
            'price_monthly': 199.99,
            'price_yearly': 1999.99,
            'description': 'Unlimited everything + API access',
            'included_features': ['all'],
            'limits': {
                'daily_scans': -1,  # Unlimited
                'ai_requests': -1,
                'watchlist_assets': -1,
                'alerts': -1
            }
        }
    }
    
    # Add-on Features (À la carte)
    ADDON_FEATURES = {
        'ai_predictions': {
            'name': 'AI Predictions',
            'description': 'Advanced AI-powered price predictions',
            'price_monthly': 19.99,
            'icon': '🤖',
            'category': 'AI Tools'
        },
        'ai_chat': {
            'name': 'AI Trading Assistant',
            'description': '24/7 AI chat for trading advice',
            'price_monthly': 14.99,
            'icon': '💬',
            'category': 'AI Tools'
        },
        'ai_portfolio_optimizer': {
            'name': 'AI Portfolio Optimizer',
            'description': 'AI-optimized portfolio recommendations',
            'price_monthly': 24.99,
            'icon': '📊',
            'category': 'AI Tools'
        },
        'whale_watcher': {
            'name': 'Whale Watcher',
            'description': 'Track large wallet movements',
            'price_monthly': 29.99,
            'icon': '🐋',
            'category': 'Analytics'
        },
        'gem_finder': {
            'name': 'Gem Finder',
            'description': 'Discover hidden opportunities',
            'price_monthly': 19.99,
            'icon': '💎',
            'category': 'Analytics'
        },
        'sentiment_analysis': {
            'name': 'Sentiment Analysis',
            'description': 'Social media & news sentiment tracking',
            'price_monthly': 14.99,
            'icon': '📰',
            'category': 'Analytics'
        },
        'advanced_charts': {
            'name': 'Advanced Charts',
            'description': 'Professional charting tools',
            'price_monthly': 9.99,
            'icon': '📈',
            'category': 'Trading Tools'
        },
        'tradingview_integration': {
            'name': 'TradingView Integration',
            'description': 'Full TradingView charts integration',
            'price_monthly': 19.99,
            'icon': '📊',
            'category': 'Trading Tools'
        },
        'auto_trading': {
            'name': 'Auto Trading Bots',
            'description': 'Automated trading strategies',
            'price_monthly': 49.99,
            'icon': '🤖',
            'category': 'Trading Tools'
        },
        'api_access': {
            'name': 'API Access',
            'description': 'Full REST API access',
            'price_monthly': 39.99,
            'icon': '🔌',
            'category': 'Developer'
        },
        'webhook_alerts': {
            'name': 'Webhook Alerts',
            'description': 'Custom webhook notifications',
            'price_monthly': 9.99,
            'icon': '🔔',
            'category': 'Developer'
        },
        'historical_data': {
            'name': 'Historical Data Access',
            'description': '10 years of historical market data',
            'price_monthly': 29.99,
            'icon': '📚',
            'category': 'Data'
        },
        'export_tools': {
            'name': 'Data Export Tools',
            'description': 'Export data to CSV, Excel, PDF',
            'price_monthly': 9.99,
            'icon': '📥',
            'category': 'Data'
        },
        'priority_support': {
            'name': 'Priority Support',
            'description': '24/7 priority customer support',
            'price_monthly': 19.99,
            'icon': '🎯',
            'category': 'Support'
        },
        'custom_indicators': {
            'name': 'Custom Indicators',
            'description': 'Create and save custom indicators',
            'price_monthly': 14.99,
            'icon': '⚙️',
            'category': 'Trading Tools'
        }
    }
    
    # Feature Bundles (Packs)
    FEATURE_BUNDLES = {
        'ai_bundle': {
            'name': 'AI Power Pack',
            'description': 'All AI features included',
            'features': ['ai_predictions', 'ai_chat', 'ai_portfolio_optimizer'],
            'price_monthly': 49.99,  # Save $9.97
            'savings': 9.97,
            'icon': '🤖'
        },
        'analytics_bundle': {
            'name': 'Analytics Pro Bundle',
            'description': 'Complete analytics suite',
            'features': ['whale_watcher', 'gem_finder', 'sentiment_analysis'],
            'price_monthly': 54.99,  # Save $9.98
            'savings': 9.98,
            'icon': '📊'
        },
        'trading_bundle': {
            'name': 'Advanced Trading Bundle',
            'description': 'Professional trading tools',
            'features': ['advanced_charts', 'tradingview_integration', 'auto_trading', 'custom_indicators'],
            'price_monthly': 79.99,  # Save $13.97
            'savings': 13.97,
            'icon': '📈'
        },
        'developer_bundle': {
            'name': 'Developer Pack',
            'description': 'API and integration tools',
            'features': ['api_access', 'webhook_alerts', 'historical_data', 'export_tools'],
            'price_monthly': 69.99,  # Save $18.97
            'savings': 18.97,
            'icon': '🔌'
        },
        'ultimate_bundle': {
            'name': 'Ultimate Everything Pack',
            'description': 'All features included',
            'features': 'all',
            'price_monthly': 149.99,  # Huge savings
            'savings': 200.00,
            'icon': '👑'
        }
    }
    
    # Usage-based pricing tiers
    USAGE_TIERS = {
        'ai_requests': {
            'name': 'AI API Requests',
            'tiers': [
                {'max': 100, 'price': 0, 'included_in': ['starter', 'pro', 'enterprise']},
                {'max': 500, 'price': 9.99, 'per': 'month'},
                {'max': 2000, 'price': 29.99, 'per': 'month'},
                {'max': -1, 'price': 99.99, 'per': 'month'}  # Unlimited
            ]
        },
        'market_scans': {
            'name': 'Daily Market Scans',
            'tiers': [
                {'max': 100, 'price': 0, 'included_in': ['starter', 'pro', 'enterprise']},
                {'max': 1000, 'price': 9.99, 'per': 'month'},
                {'max': 5000, 'price': 29.99, 'per': 'month'},
                {'max': -1, 'price': 79.99, 'per': 'month'}
            ]
        }
    }
    
    def __init__(self):
        """Initialize subscription manager"""
        self.storage_dir = "data/subscriptions"
        os.makedirs(self.storage_dir, exist_ok=True)
        logger.info("Subscription manager initialized")
    
    def get_all_plans(self) -> Dict[str, Any]:
        """Get all available plans and features"""
        return {
            'base_plans': self.BASE_PLANS,
            'addon_features': self.ADDON_FEATURES,
            'feature_bundles': self.FEATURE_BUNDLES,
            'usage_tiers': self.USAGE_TIERS
        }
    
    def calculate_custom_price(self, base_plan: str, addons: List[str] = None, 
                               bundles: List[str] = None, billing_cycle: str = 'monthly') -> Dict[str, Any]:
        """
        Calculate price for custom subscription
        
        Args:
            base_plan: Base plan name
            addons: List of addon feature IDs
            bundles: List of bundle IDs
            billing_cycle: 'monthly' or 'yearly'
        
        Returns:
            Price breakdown
        """
        if base_plan not in self.BASE_PLANS:
            return {'success': False, 'error': 'Invalid base plan'}
        
        addons = addons or []
        bundles = bundles or []
        
        # Base plan price
        plan = self.BASE_PLANS[base_plan]
        base_price = plan[f'price_{billing_cycle}']
        
        # Calculate addon prices
        addon_total = 0
        addon_details = []
        
        for addon_id in addons:
            if addon_id in self.ADDON_FEATURES:
                addon = self.ADDON_FEATURES[addon_id]
                addon_price = addon['price_monthly']
                if billing_cycle == 'yearly':
                    addon_price *= 10  # 2 months free
                
                addon_total += addon_price
                addon_details.append({
                    'id': addon_id,
                    'name': addon['name'],
                    'price': addon_price
                })
        
        # Calculate bundle prices
        bundle_total = 0
        bundle_details = []
        bundle_savings = 0
        
        for bundle_id in bundles:
            if bundle_id in self.FEATURE_BUNDLES:
                bundle = self.FEATURE_BUNDLES[bundle_id]
                bundle_price = bundle['price_monthly']
                if billing_cycle == 'yearly':
                    bundle_price *= 10
                
                bundle_total += bundle_price
                bundle_savings += bundle.get('savings', 0)
                bundle_details.append({
                    'id': bundle_id,
                    'name': bundle['name'],
                    'price': bundle_price,
                    'savings': bundle.get('savings', 0)
                })
        
        # Total calculation
        subtotal = base_price + addon_total + bundle_total
        total_savings = bundle_savings
        if billing_cycle == 'yearly':
            # Calculate yearly savings (2 months free)
            monthly_equivalent = (base_price / 10 * 12) + ((addon_total + bundle_total) / 10 * 12)
            total_savings += (monthly_equivalent - subtotal)
        
        total = subtotal
        
        return {
            'success': True,
            'base_plan': {
                'name': plan['name'],
                'price': base_price
            },
            'addons': addon_details,
            'addons_total': addon_total,
            'bundles': bundle_details,
            'bundles_total': bundle_total,
            'subtotal': round(subtotal, 2),
            'savings': round(total_savings, 2),
            'total': round(total, 2),
            'billing_cycle': billing_cycle,
            'currency': 'USD'
        }
    
    def create_subscription(self, user_id: str, base_plan: str, 
                           addons: List[str] = None, bundles: List[str] = None,
                           billing_cycle: str = 'monthly') -> Dict[str, Any]:
        """Create a new subscription"""
        pricing = self.calculate_custom_price(base_plan, addons, bundles, billing_cycle)
        
        if not pricing.get('success'):
            return pricing
        
        # Create subscription
        subscription = {
            'subscription_id': f"sub_{datetime.now().timestamp()}_{user_id}",
            'user_id': user_id,
            'base_plan': base_plan,
            'addons': addons or [],
            'bundles': bundles or [],
            'billing_cycle': billing_cycle,
            'price': pricing['total'],
            'currency': 'USD',
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'renews_at': self._calculate_renewal_date(billing_cycle),
            'features': self._get_subscription_features(base_plan, addons, bundles)
        }
        
        # Store subscription
        self._store_subscription(subscription)
        
        logger.info(f"Created subscription {subscription['subscription_id']} for user {user_id}")
        
        return {
            'success': True,
            'subscription': subscription
        }
    
    def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's active subscription"""
        filename = f"{self.storage_dir}/{user_id}.json"
        
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def check_feature_access(self, user_id: str, feature: str) -> bool:
        """Check if user has access to a feature"""
        subscription = self.get_user_subscription(user_id)
        
        if not subscription:
            # Free plan
            return feature in self.BASE_PLANS['free']['included_features']
        
        features = subscription.get('features', [])
        return feature in features or 'all' in features
    
    def _calculate_renewal_date(self, billing_cycle: str) -> str:
        """Calculate subscription renewal date"""
        if billing_cycle == 'monthly':
            renewal = datetime.now() + timedelta(days=30)
        else:  # yearly
            renewal = datetime.now() + timedelta(days=365)
        
        return renewal.isoformat()
    
    def _get_subscription_features(self, base_plan: str, addons: List[str], 
                                   bundles: List[str]) -> List[str]:
        """Get all features included in subscription"""
        features = set()
        
        # Base plan features
        plan_features = self.BASE_PLANS[base_plan]['included_features']
        if 'all' in plan_features:
            return ['all']
        
        features.update(plan_features)
        
        # Addon features
        features.update(addons)
        
        # Bundle features
        for bundle_id in bundles:
            if bundle_id in self.FEATURE_BUNDLES:
                bundle = self.FEATURE_BUNDLES[bundle_id]
                if bundle['features'] == 'all':
                    return ['all']
                features.update(bundle['features'])
        
        return list(features)
    
    def _store_subscription(self, subscription: Dict[str, Any]):
        """Store subscription"""
        filename = f"{self.storage_dir}/{subscription['user_id']}.json"
        
        with open(filename, 'w') as f:
            json.dump(subscription, f, indent=2)


# Global instance
subscription_manager = SubscriptionManager()


def get_subscription_manager() -> SubscriptionManager:
    """Get the global subscription manager instance"""
    return subscription_manager
