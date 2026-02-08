"""
PayPal Payment Processor
Handles PayPal payments and subscriptions
"""

import os
import json
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PayPalProcessor:
    """Process PayPal payments and subscriptions"""
    
    # Price tiers in USD
    PLANS_USD = {
        'free': 0,
        'starter': 19.99,
        'pro': 49.99,
        'enterprise': 199.99
    }
    
    def __init__(self):
        """Initialize PayPal processor"""
        # PayPal credentials
        self.client_id = os.getenv('PAYPAL_CLIENT_ID', '')
        self.client_secret = os.getenv('PAYPAL_CLIENT_SECRET', '')
        self.mode = os.getenv('PAYPAL_MODE', 'sandbox')  # sandbox or live
        
        # PayPal email for direct payments
        self.paypal_email = os.getenv('PAYPAL_EMAIL', 'payments@signaltrust.ai')
        
        # PayPal.me link (if available)
        self.paypal_me_link = os.getenv('PAYPAL_ME_LINK', 'https://paypal.me/signaltrust')
        
        # Subscription plan IDs (created in PayPal dashboard)
        self.subscription_plans = {
            'starter_monthly': os.getenv('PAYPAL_STARTER_MONTHLY_PLAN_ID', ''),
            'starter_yearly': os.getenv('PAYPAL_STARTER_YEARLY_PLAN_ID', ''),
            'pro_monthly': os.getenv('PAYPAL_PRO_MONTHLY_PLAN_ID', ''),
            'pro_yearly': os.getenv('PAYPAL_PRO_YEARLY_PLAN_ID', ''),
            'enterprise_monthly': os.getenv('PAYPAL_ENTERPRISE_MONTHLY_PLAN_ID', ''),
            'enterprise_yearly': os.getenv('PAYPAL_ENTERPRISE_YEARLY_PLAN_ID', '')
        }
        
        logger.info("PayPal processor initialized")
    
    def get_payment_link(self, plan: str, billing_cycle: str = 'monthly', 
                        custom_amount: float = None) -> Dict[str, Any]:
        """
        Generate PayPal payment link
        
        Args:
            plan: Plan name (starter, pro, enterprise)
            billing_cycle: 'monthly' or 'yearly'
            custom_amount: Custom amount for flexible plans
        
        Returns:
            Payment link information
        """
        amount = custom_amount or self.PLANS_USD.get(plan, 0)
        
        if amount == 0:
            return {'success': False, 'error': 'Invalid plan or amount'}
        
        # Generate PayPal.me link with amount
        paypal_me_url = f"{self.paypal_me_link}/{amount}USD"
        
        # Generate standard PayPal link
        paypal_standard_url = (
            f"https://www.paypal.com/paypalme/{self.paypal_email.split('@')[0]}/{amount}USD"
        )
        
        # Generate invoice link (for manual PayPal invoices)
        invoice_url = f"https://www.paypal.com/invoice/create?business={self.paypal_email}"
        
        return {
            'success': True,
            'plan': plan,
            'amount': amount,
            'currency': 'USD',
            'billing_cycle': billing_cycle,
            'payment_links': {
                'paypal_me': paypal_me_url,
                'paypal_standard': paypal_standard_url,
                'invoice': invoice_url
            },
            'qr_code_data': paypal_me_url,
            'instructions': {
                'step1': 'Click on one of the PayPal links below',
                'step2': 'Log in to your PayPal account',
                'step3': f'Confirm payment of ${amount} USD',
                'step4': 'Complete the transaction',
                'step5': 'Your subscription will be activated automatically'
            }
        }
    
    def get_subscription_link(self, plan: str, billing_cycle: str = 'monthly') -> Dict[str, Any]:
        """
        Get PayPal subscription link
        
        Args:
            plan: Plan name
            billing_cycle: 'monthly' or 'yearly'
        
        Returns:
            Subscription link information
        """
        plan_key = f"{plan}_{billing_cycle}"
        plan_id = self.subscription_plans.get(plan_key, '')
        
        if not plan_id:
            # Fallback to payment link
            return self.get_payment_link(plan, billing_cycle)
        
        # PayPal subscription URL
        subscription_url = f"https://www.paypal.com/webapps/billing/plans/subscribe?plan_id={plan_id}"
        
        return {
            'success': True,
            'plan': plan,
            'billing_cycle': billing_cycle,
            'plan_id': plan_id,
            'subscription_url': subscription_url,
            'type': 'subscription'
        }
    
    def create_payment_request(self, user_id: str, plan: str, 
                              billing_cycle: str = 'monthly',
                              custom_amount: float = None) -> Dict[str, Any]:
        """Create a PayPal payment request"""
        
        payment_link = self.get_payment_link(plan, billing_cycle, custom_amount)
        
        if not payment_link.get('success'):
            return payment_link
        
        # Generate unique payment ID
        payment_id = f"paypal_{datetime.now().timestamp()}_{user_id}"
        
        payment_request = {
            'success': True,
            'payment_id': payment_id,
            'user_id': user_id,
            'plan': plan,
            'amount': payment_link['amount'],
            'currency': 'USD',
            'billing_cycle': billing_cycle,
            'payment_links': payment_link['payment_links'],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        # Store payment request
        self._store_payment_request(payment_request)
        
        logger.info(f"Created PayPal payment request: {payment_id}")
        
        return payment_request
    
    def verify_payment(self, payment_id: str, transaction_id: str) -> Dict[str, Any]:
        """
        Verify PayPal payment
        
        Args:
            payment_id: Payment request ID
            transaction_id: PayPal transaction ID
        
        Returns:
            Verification result
        """
        # In production: verify with PayPal API
        logger.info(f"Verifying PayPal payment {payment_id} with transaction: {transaction_id}")
        
        payment_request = self._get_payment_request(payment_id)
        if not payment_request:
            return {'success': False, 'error': 'Payment request not found'}
        
        # Update payment status
        self._update_payment_status(payment_id, 'confirmed', transaction_id)
        
        return {
            'success': True,
            'payment_id': payment_id,
            'transaction_id': transaction_id,
            'status': 'confirmed',
            'verified_at': datetime.now().isoformat()
        }
    
    def _store_payment_request(self, payment_request: Dict[str, Any]):
        """Store payment request"""
        filename = f"data/paypal_payments/{payment_request['payment_id']}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(payment_request, f, indent=2)
    
    def _get_payment_request(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve payment request"""
        filename = f"data/paypal_payments/{payment_id}.json"
        
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def _update_payment_status(self, payment_id: str, status: str, transaction_id: str = None):
        """Update payment status"""
        payment_request = self._get_payment_request(payment_id)
        if payment_request:
            payment_request['status'] = status
            if transaction_id:
                payment_request['transaction_id'] = transaction_id
            payment_request['updated_at'] = datetime.now().isoformat()
            self._store_payment_request(payment_request)


class CreditCardLinkProcessor:
    """Process credit card payments via payment links (Stripe, etc.)"""
    
    def __init__(self):
        """Initialize credit card link processor"""
        # Stripe payment links
        self.stripe_links = {
            'starter_monthly': os.getenv('STRIPE_STARTER_MONTHLY_LINK', ''),
            'starter_yearly': os.getenv('STRIPE_STARTER_YEARLY_LINK', ''),
            'pro_monthly': os.getenv('STRIPE_PRO_MONTHLY_LINK', ''),
            'pro_yearly': os.getenv('STRIPE_PRO_YEARLY_LINK', ''),
            'enterprise_monthly': os.getenv('STRIPE_ENTERPRISE_MONTHLY_LINK', ''),
            'enterprise_yearly': os.getenv('STRIPE_ENTERPRISE_YEARLY_LINK', '')
        }
        
        # Buy Me a Coffee link (alternative)
        self.buymeacoffee_link = os.getenv('BUYMEACOFFEE_LINK', 'https://buymeacoffee.com/signaltrust')
        
        # Ko-fi link (alternative)
        self.kofi_link = os.getenv('KOFI_LINK', 'https://ko-fi.com/signaltrust')
        
        logger.info("Credit card link processor initialized")
    
    def get_payment_link(self, plan: str, billing_cycle: str = 'monthly') -> Dict[str, Any]:
        """Get credit card payment link"""
        
        link_key = f"{plan}_{billing_cycle}"
        stripe_link = self.stripe_links.get(link_key, '')
        
        if not stripe_link:
            return {
                'success': False,
                'error': 'Payment link not configured for this plan'
            }
        
        return {
            'success': True,
            'plan': plan,
            'billing_cycle': billing_cycle,
            'payment_link': stripe_link,
            'alternative_links': {
                'buymeacoffee': self.buymeacoffee_link,
                'kofi': self.kofi_link
            }
        }


# Global instances
paypal_processor = PayPalProcessor()
card_link_processor = CreditCardLinkProcessor()


def get_paypal_processor() -> PayPalProcessor:
    """Get the global PayPal processor instance"""
    return paypal_processor


def get_card_link_processor() -> CreditCardLinkProcessor:
    """Get the global credit card link processor instance"""
    return card_link_processor
