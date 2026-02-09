#!/usr/bin/env python3
"""
Payment Processing Module
Handles subscription payments and billing
"""

import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List


class PaymentProcessor:
    """Payment processing and subscription management"""
    
    # Subscription plans
    PLANS = {
        'free': {
            'name': 'Starter',
            'price': 0,
            'currency': 'USD',
            'features': [
                '5 market scans per day',
                '3 symbols per scan',
                '3 AI predictions per day',
                'Basic price alerts',
                'Community support'
            ],
            'limits': {
                'scans_per_day': 5,
                'symbols_per_scan': 3,
                'ai_predictions_per_day': 3,
                'gems_discoveries_per_day': 3,
                'whale_tracking': False,
                'advanced_analytics': False,
                'api_access': False,
                'historical_data_days': 7
            }
        },
        'basic': {
            'name': 'Trader Plan',
            'price': 49.00,
            'currency': 'USD',
            'billing_period': 'monthly',
            'features': [
                '100 scans per day',
                '10 symbols per scan',
                '25 AI predictions per day',
                'Basic NFT tracking',
                'Real-time price alerts',
                'Technical analysis tools',
                'Email support',
                'TradingView charts',
                '30 days historical data'
            ],
            'limits': {
                'scans_per_day': 100,
                'symbols_per_scan': 10,
                'ai_predictions_per_day': 25,
                'gems_discoveries_per_day': 15,
                'whale_tracking': False,
                'advanced_analytics': True,
                'api_access': False,
                'historical_data_days': 30
            }
        },
        'pro': {
            'name': 'Professional Plan',
            'price': 149.00,
            'currency': 'USD',
            'billing_period': 'monthly',
            'features': [
                'Unlimited scans',
                'Unlimited symbols',
                'Unlimited AI predictions',
                'Advanced NFT whale tracking',
                'Smart contract analysis',
                'Multi-chain support',
                'Portfolio tracker',
                'Priority support',
                'Full API access',
                'Custom alerts',
                'Unlimited historical data',
                'SignalAI Strategy included'
            ],
            'limits': {
                'scans_per_day': -1,
                'symbols_per_scan': -1,
                'ai_predictions_per_day': -1,
                'gems_discoveries_per_day': -1,
                'whale_tracking': True,
                'advanced_analytics': True,
                'api_access': True,
                'historical_data_days': -1,
                'signalai_access': True
            }
        },
        'enterprise': {
            'name': 'Institution Plan',
            'price': 499.00,
            'currency': 'USD',
            'billing_period': 'monthly',
            'features': [
                'Everything Unlimited',
                'SignalAI Strategy included',
                'Custom AI models',
                'Dedicated account manager',
                'White-label solutions',
                '10 team accounts',
                'Advanced API (unlimited)',
                'Custom integrations',
                'OTC desk integration',
                '24/7 premium support',
                'Unlimited historical data'
            ],
            'limits': {
                'scans_per_day': -1,
                'symbols_per_scan': -1,
                'ai_predictions_per_day': -1,
                'ai_predictions': -1,
                'gems_discoveries_per_day': -1,
                'whale_tracking': True,
                'advanced_analytics': True,
                'api_access': True,
                'historical_data_days': -1,
                'users': 10,
                'signalai_access': True
            }
        },
        'signalai': {
            'name': 'SignalAI Strategy',
            'price': 9.99,
            'currency': 'USD',
            'billing_period': 'monthly',
            'trial_days': 3,
            'features': [
                'AI-powered trading strategy',
                'Live buy/sell signals',
                'EMA9 + EMA21 + RSI + MACD combination',
                'Real-time strategy adaptation',
                'Works with all TradingView symbols',
                'Optimized for stocks and crypto',
                'Risk management included',
                'Entry, stop-loss, and take-profit levels'
            ],
            'limits': {
                'signalai_access': True,
                'live_signals': True,
                'strategy_updates': 'realtime',
                'symbols': -1
            }
        }
    }
    
    def __init__(self, transactions_file: str = 'data/transactions.json'):
        """Initialize payment processor.
        
        Args:
            transactions_file: Path to transactions database
        """
        self.transactions_file = transactions_file
        self._ensure_data_dir()
        self._load_transactions()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.transactions_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_transactions(self):
        """Load transactions from file."""
        if os.path.exists(self.transactions_file):
            try:
                with open(self.transactions_file, 'r') as f:
                    self.transactions = json.load(f)
            except (json.JSONDecodeError, IOError, FileNotFoundError):
                self.transactions = []
        else:
            self.transactions = []
    
    def _save_transactions(self):
        """Save transactions to file."""
        with open(self.transactions_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def get_plans(self) -> Dict:
        """Get all available subscription plans.
        
        Returns:
            Dictionary of plans
        """
        return self.PLANS
    
    def get_plan(self, plan_id: str) -> Dict:
        """Get specific plan details.
        
        Args:
            plan_id: Plan identifier
            
        Returns:
            Plan details
        """
        return self.PLANS.get(plan_id, {})
    
    def process_payment(self, user_id: str, email: str, plan_id: str, 
                       payment_method: Dict) -> Dict:
        """Process a payment.
        
        Args:
            user_id: User ID
            email: User email
            plan_id: Plan to purchase
            payment_method: Payment method details
            
        Returns:
            Payment result
        """
        # Validate plan
        if plan_id not in self.PLANS:
            return {'success': False, 'error': 'Invalid plan'}
        
        plan = self.PLANS[plan_id]
        
        # Free plan doesn't require payment
        if plan_id == 'free':
            return {
                'success': True,
                'message': 'Free plan activated',
                'transaction_id': None
            }
        
        # Validate payment method
        if not self._validate_payment_method(payment_method):
            return {'success': False, 'error': 'Invalid payment method'}
        
        # Create transaction
        transaction_id = secrets.token_hex(16)
        transaction = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'email': email,
            'plan_id': plan_id,
            'plan_name': plan['name'],
            'amount': plan['price'],
            'currency': plan['currency'],
            'payment_method': {
                'type': payment_method['type'],
                'last4': payment_method.get('last4', '****')
            },
            'status': 'completed',
            'created_at': datetime.now().isoformat(),
            'next_billing_date': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        self.transactions.append(transaction)
        self._save_transactions()
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'message': 'Payment processed successfully',
            'next_billing_date': transaction['next_billing_date']
        }
    
    def _validate_payment_method(self, payment_method: Dict) -> bool:
        """Validate payment method.
        
        Args:
            payment_method: Payment method details
            
        Returns:
            True if valid
        """
        if not payment_method.get('type'):
            return False
        
        payment_type = payment_method['type']
        
        if payment_type == 'card':
            # Validate card details
            required_fields = ['card_number', 'exp_month', 'exp_year', 'cvv']
            return all(payment_method.get(f) for f in required_fields)
        
        elif payment_type == 'paypal':
            return payment_method.get('paypal_email') is not None
        
        elif payment_type == 'crypto':
            return payment_method.get('wallet_address') is not None
        
        return False
    
    def get_user_transactions(self, user_id: str) -> List[Dict]:
        """Get user's transaction history.
        
        Args:
            user_id: User ID
            
        Returns:
            List of transactions
        """
        return [t for t in self.transactions if t['user_id'] == user_id]
    
    def cancel_subscription(self, user_id: str) -> Dict:
        """Cancel user's subscription.
        
        Args:
            user_id: User ID
            
        Returns:
            Cancellation result
        """
        user_transactions = self.get_user_transactions(user_id)
        
        if not user_transactions:
            return {'success': False, 'error': 'No active subscription'}
        
        # Mark last transaction as cancelled
        last_transaction = user_transactions[-1]
        last_transaction['status'] = 'cancelled'
        last_transaction['cancelled_at'] = datetime.now().isoformat()
        
        self._save_transactions()
        
        return {
            'success': True,
            'message': 'Subscription cancelled',
            'access_until': last_transaction.get('next_billing_date')
        }
    
    def validate_card_number(self, card_number: str) -> Dict:
        """Validate credit card number using Luhn algorithm.
        
        Args:
            card_number: Card number to validate
            
        Returns:
            Validation result
        """
        # Remove spaces and dashes
        card_number = card_number.replace(' ', '').replace('-', '')
        
        # Check if all digits
        if not card_number.isdigit():
            return {'valid': False, 'error': 'Card number must contain only digits'}
        
        # Check length
        if len(card_number) < 13 or len(card_number) > 19:
            return {'valid': False, 'error': 'Invalid card number length'}
        
        # Luhn algorithm
        def luhn_check(number):
            digits = [int(d) for d in number]
            checksum = digits[-1]
            digits = digits[:-1]
            digits.reverse()
            
            for i in range(len(digits)):
                if i % 2 == 0:
                    digits[i] *= 2
                    if digits[i] > 9:
                        digits[i] -= 9
            
            return (sum(digits) + checksum) % 10 == 0
        
        if not luhn_check(card_number):
            return {'valid': False, 'error': 'Invalid card number'}
        
        # Determine card type
        card_type = 'Unknown'
        if card_number[0] == '4':
            card_type = 'Visa'
        elif card_number[0] == '5':
            card_type = 'Mastercard'
        elif card_number[:2] in ['34', '37']:
            card_type = 'American Express'
        elif card_number[:4] == '6011':
            card_type = 'Discover'
        
        return {
            'valid': True,
            'card_type': card_type,
            'last4': card_number[-4:]
        }
    
    def generate_invoice(self, transaction_id: str) -> Dict:
        """Generate invoice for a transaction.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Invoice data
        """
        # Find transaction
        transaction = None
        for t in self.transactions:
            if t['transaction_id'] == transaction_id:
                transaction = t
                break
        
        if not transaction:
            return {'success': False, 'error': 'Transaction not found'}
        
        invoice = {
            'invoice_number': f'INV-{transaction_id[:8].upper()}',
            'transaction_id': transaction_id,
            'date': transaction['created_at'],
            'user_id': transaction['user_id'],
            'email': transaction['email'],
            'items': [
                {
                    'description': transaction['plan_name'],
                    'amount': transaction['amount'],
                    'currency': transaction['currency']
                }
            ],
            'subtotal': transaction['amount'],
            'tax': round(transaction['amount'] * 0.1, 2),  # 10% tax
            'total': round(transaction['amount'] * 1.1, 2),
            'payment_status': transaction['status']
        }
        
        return {
            'success': True,
            'invoice': invoice
        }
    
    def check_signalai_access(self, user_id: str, user_email: str = None, 
                             is_admin: bool = False, user_plan: str = None) -> Dict:
        """Check if user has access to SignalAI strategy
        
        Args:
            user_id: User ID
            user_email: User email (optional)
            is_admin: Whether user is admin
            user_plan: User's current subscription plan (optional)
            
        Returns:
            Access status information
        """
        # Admin always has free access
        if is_admin:
            return {
                'has_access': True,
                'subscription_type': 'admin',
                'expires_at': None,
                'trial_active': False,
                'days_remaining': -1
            }
        
        # Check for Pro or Enterprise plan - SignalAI included
        if user_plan in ['pro', 'enterprise']:
            user_transactions = self.get_user_transactions(user_id)
            plan_transactions = [t for t in user_transactions 
                                if t.get('plan_id') in ['pro', 'enterprise']
                                and t.get('status') == 'active']
            
            if plan_transactions:
                last_transaction = plan_transactions[-1]
                next_billing = datetime.fromisoformat(last_transaction['next_billing_date'])
                days_remaining = (next_billing - datetime.now()).days
                
                return {
                    'has_access': True,
                    'subscription_type': 'included_in_plan',
                    'plan': user_plan,
                    'expires_at': last_transaction['next_billing_date'],
                    'trial_active': False,
                    'days_remaining': days_remaining
                }
        
        # Check for active SignalAI subscription
        user_transactions = self.get_user_transactions(user_id)
        signalai_transactions = [t for t in user_transactions 
                                if t.get('plan_id') == 'signalai' 
                                and t.get('status') == 'active']
        
        if signalai_transactions:
            last_transaction = signalai_transactions[-1]
            next_billing = datetime.fromisoformat(last_transaction['next_billing_date'])
            days_remaining = (next_billing - datetime.now()).days
            
            return {
                'has_access': True,
                'subscription_type': 'paid',
                'expires_at': last_transaction['next_billing_date'],
                'trial_active': last_transaction.get('is_trial', False),
                'days_remaining': days_remaining
            }
        
        return {
            'has_access': False,
            'subscription_type': None,
            'expires_at': None,
            'trial_active': False,
            'days_remaining': 0
        }
    
    def start_signalai_trial(self, user_id: str, email: str) -> Dict:
        """Start SignalAI 3-day free trial
        
        Args:
            user_id: User ID
            email: User email
            
        Returns:
            Trial activation result
        """
        # Check if user already had a trial
        user_transactions = self.get_user_transactions(user_id)
        had_trial = any(t.get('plan_id') == 'signalai' for t in user_transactions)
        
        if had_trial:
            return {
                'success': False,
                'error': 'Trial already used. Please subscribe to continue.'
            }
        
        # Create trial transaction
        transaction_id = secrets.token_hex(16)
        plan = self.PLANS['signalai']
        
        trial_end = datetime.now() + timedelta(days=3)
        
        transaction = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'email': email,
            'plan_id': 'signalai',
            'plan_name': plan['name'],
            'amount': 0,  # Free trial
            'currency': plan['currency'],
            'status': 'active',
            'is_trial': True,
            'created_at': datetime.now().isoformat(),
            'next_billing_date': trial_end.isoformat()
        }
        
        self.transactions.append(transaction)
        self._save_transactions()
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'message': 'SignalAI trial started - 3 days free access',
            'trial_ends': trial_end.isoformat()
        }
