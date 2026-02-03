#!/usr/bin/env python3
"""
Coupon Code System
Handles promotional codes, discounts, and special subscription offers
"""

import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional


class CouponManager:
    """Manager for promotional codes and discounts"""
    
    # Pre-defined coupon codes
    DEFAULT_COUPONS = {
        'CRYPTO2026': {
            'code': 'CRYPTO2026',
            'type': 'percentage',
            'value': 50,  # 50% off
            'description': 'New Year Crypto Special - 50% off',
            'valid_plans': ['basic', 'pro'],
            'max_uses': 1000,
            'used_count': 0,
            'expires_at': '2026-12-31',
            'is_active': True
        },
        'WHALE50': {
            'code': 'WHALE50',
            'type': 'percentage',
            'value': 50,
            'description': 'Whale Watcher Special - 50% off first month',
            'valid_plans': ['pro'],
            'max_uses': 500,
            'used_count': 0,
            'expires_at': '2026-06-30',
            'is_active': True
        },
        'NFT25': {
            'code': 'NFT25',
            'type': 'percentage',
            'value': 25,
            'description': 'NFT Trader Discount - 25% off',
            'valid_plans': ['basic', 'pro'],
            'max_uses': -1,  # Unlimited
            'used_count': 0,
            'expires_at': '2026-12-31',
            'is_active': True
        },
        'FOUNDER100': {
            'code': 'FOUNDER100',
            'type': 'percentage',
            'value': 100,
            'description': 'Founder Member - Free for life',
            'valid_plans': ['basic', 'pro', 'enterprise'],
            'max_uses': 100,
            'used_count': 0,
            'expires_at': '2027-12-31',
            'is_active': True,
            'lifetime': True
        },
        'EARLYBIRD': {
            'code': 'EARLYBIRD',
            'type': 'fixed',
            'value': 30,  # $30 off
            'description': 'Early Bird Special - $30 off',
            'valid_plans': ['basic', 'pro'],
            'max_uses': 200,
            'used_count': 0,
            'expires_at': '2026-03-31',
            'is_active': True
        },
        'VIP500': {
            'code': 'VIP500',
            'type': 'fixed',
            'value': 500,  # $500 off enterprise
            'description': 'VIP Enterprise Discount',
            'valid_plans': ['enterprise'],
            'max_uses': 50,
            'used_count': 0,
            'expires_at': '2026-12-31',
            'is_active': True
        },
        'TRIAL30': {
            'code': 'TRIAL30',
            'type': 'trial',
            'value': 30,  # 30 days free trial
            'description': '30-Day Free Trial',
            'valid_plans': ['basic', 'pro'],
            'max_uses': -1,
            'used_count': 0,
            'expires_at': '2026-12-31',
            'is_active': True
        }
    }
    
    def __init__(self, coupons_file: str = 'data/coupons.json'):
        """Initialize coupon manager.
        
        Args:
            coupons_file: Path to coupons database
        """
        self.coupons_file = coupons_file
        self._ensure_data_dir()
        self._load_coupons()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.coupons_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_coupons(self):
        """Load coupons from file."""
        if os.path.exists(self.coupons_file):
            try:
                with open(self.coupons_file, 'r') as f:
                    self.coupons = json.load(f)
            except (json.JSONDecodeError, IOError, FileNotFoundError):
                self.coupons = self.DEFAULT_COUPONS.copy()
                self._save_coupons()
        else:
            self.coupons = self.DEFAULT_COUPONS.copy()
            self._save_coupons()
    
    def _save_coupons(self):
        """Save coupons to file."""
        with open(self.coupons_file, 'w') as f:
            json.dump(self.coupons, f, indent=2)
    
    def validate_coupon(self, code: str, plan_id: str) -> Dict:
        """Validate a coupon code.
        
        Args:
            code: Coupon code to validate
            plan_id: Plan ID to apply coupon to
            
        Returns:
            Validation result with coupon details
        """
        code = code.upper().strip()
        
        if code not in self.coupons:
            return {
                'valid': False,
                'error': 'Invalid coupon code'
            }
        
        coupon = self.coupons[code]
        
        # Check if active
        if not coupon.get('is_active', True):
            return {
                'valid': False,
                'error': 'This coupon is no longer active'
            }
        
        # Check expiration
        expires_at = datetime.fromisoformat(coupon['expires_at'])
        if datetime.now() > expires_at:
            return {
                'valid': False,
                'error': 'This coupon has expired'
            }
        
        # Check max uses
        max_uses = coupon.get('max_uses', -1)
        if max_uses > 0 and coupon.get('used_count', 0) >= max_uses:
            return {
                'valid': False,
                'error': 'This coupon has reached maximum redemptions'
            }
        
        # Check valid plans
        if plan_id not in coupon.get('valid_plans', []):
            return {
                'valid': False,
                'error': f'This coupon is not valid for the {plan_id} plan'
            }
        
        return {
            'valid': True,
            'coupon': coupon,
            'discount_type': coupon['type'],
            'discount_value': coupon['value'],
            'description': coupon['description']
        }
    
    def apply_coupon(self, code: str, plan_id: str, original_price: float) -> Dict:
        """Apply coupon and calculate discounted price.
        
        Args:
            code: Coupon code
            plan_id: Plan ID
            original_price: Original price
            
        Returns:
            Price calculation with discount
        """
        validation = self.validate_coupon(code, plan_id)
        
        if not validation['valid']:
            return validation
        
        coupon = validation['coupon']
        discount_amount = 0
        final_price = original_price
        
        if coupon['type'] == 'percentage':
            discount_amount = original_price * (coupon['value'] / 100)
            final_price = original_price - discount_amount
        elif coupon['type'] == 'fixed':
            discount_amount = min(coupon['value'], original_price)
            final_price = original_price - discount_amount
        elif coupon['type'] == 'trial':
            # Free trial - price becomes 0
            discount_amount = original_price
            final_price = 0
        
        return {
            'valid': True,
            'original_price': original_price,
            'discount_amount': round(discount_amount, 2),
            'final_price': round(max(0, final_price), 2),
            'coupon_code': code,
            'description': coupon['description'],
            'is_lifetime': coupon.get('lifetime', False),
            'is_trial': coupon['type'] == 'trial',
            'trial_days': coupon['value'] if coupon['type'] == 'trial' else 0
        }
    
    def use_coupon(self, code: str) -> Dict:
        """Mark coupon as used.
        
        Args:
            code: Coupon code
            
        Returns:
            Result of operation
        """
        code = code.upper().strip()
        
        if code not in self.coupons:
            return {'success': False, 'error': 'Invalid coupon code'}
        
        self.coupons[code]['used_count'] = self.coupons[code].get('used_count', 0) + 1
        self._save_coupons()
        
        return {
            'success': True,
            'message': 'Coupon redeemed successfully',
            'remaining_uses': self.coupons[code].get('max_uses', -1) - self.coupons[code]['used_count']
        }
    
    def create_coupon(self, code: str, coupon_data: Dict) -> Dict:
        """Create a new coupon code.
        
        Args:
            code: Coupon code
            coupon_data: Coupon configuration
            
        Returns:
            Creation result
        """
        code = code.upper().strip()
        
        if code in self.coupons:
            return {'success': False, 'error': 'Coupon code already exists'}
        
        # Validate required fields
        required = ['type', 'value', 'description', 'valid_plans', 'expires_at']
        if not all(field in coupon_data for field in required):
            return {'success': False, 'error': 'Missing required fields'}
        
        self.coupons[code] = {
            'code': code,
            'type': coupon_data['type'],
            'value': coupon_data['value'],
            'description': coupon_data['description'],
            'valid_plans': coupon_data['valid_plans'],
            'max_uses': coupon_data.get('max_uses', -1),
            'used_count': 0,
            'expires_at': coupon_data['expires_at'],
            'is_active': True,
            'created_at': datetime.now().isoformat()
        }
        
        self._save_coupons()
        
        return {
            'success': True,
            'message': 'Coupon created successfully',
            'code': code
        }
    
    def generate_referral_code(self, user_id: str) -> str:
        """Generate a unique referral code for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Referral code
        """
        code = f"REF{secrets.token_hex(4).upper()}"
        
        coupon_data = {
            'type': 'percentage',
            'value': 20,
            'description': f'Referral Discount - 20% off',
            'valid_plans': ['basic', 'pro'],
            'max_uses': -1,
            'expires_at': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
            'referrer_id': user_id
        }
        
        self.create_coupon(code, coupon_data)
        
        return code
    
    def list_active_coupons(self) -> Dict:
        """Get list of all active public coupons.
        
        Returns:
            List of active coupons
        """
        active = []
        
        for code, coupon in self.coupons.items():
            if not coupon.get('is_active', True):
                continue
            
            expires_at = datetime.fromisoformat(coupon['expires_at'])
            if datetime.now() > expires_at:
                continue
            
            # Don't show referral codes or fully used codes
            if code.startswith('REF'):
                continue
            
            max_uses = coupon.get('max_uses', -1)
            if max_uses > 0 and coupon.get('used_count', 0) >= max_uses:
                continue
            
            active.append({
                'code': code,
                'description': coupon['description'],
                'type': coupon['type'],
                'value': coupon['value'],
                'valid_plans': coupon['valid_plans']
            })
        
        return {'coupons': active}
    
    def get_coupon_stats(self) -> Dict:
        """Get coupon usage statistics.
        
        Returns:
            Statistics about coupon usage
        """
        total_coupons = len(self.coupons)
        active_coupons = sum(1 for c in self.coupons.values() if c.get('is_active', True))
        total_uses = sum(c.get('used_count', 0) for c in self.coupons.values())
        
        return {
            'total_coupons': total_coupons,
            'active_coupons': active_coupons,
            'total_redemptions': total_uses
        }
