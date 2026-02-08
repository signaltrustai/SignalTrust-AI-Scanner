"""
Bank Transfer Payment Processor
Handles bank wire transfer payments
"""

import os
import json
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class BankTransferProcessor:
    """Process bank wire transfer payments"""
    
    # Price tiers in USD
    PLANS_USD = {
        'basic': 29.99,
        'pro': 79.99,
        'enterprise': 299.99
    }
    
    # Supported currencies
    CURRENCIES = {
        'USD': {'symbol': '$', 'name': 'US Dollar'},
        'EUR': {'symbol': '€', 'name': 'Euro'},
        'GBP': {'symbol': '£', 'name': 'British Pound'},
        'CAD': {'symbol': '$', 'name': 'Canadian Dollar'}
    }
    
    def __init__(self):
        """Initialize bank transfer processor"""
        # Bank account details
        self.bank_accounts = {
            'USD': {
                'bank_name': os.getenv('BANK_NAME_USD', 'Chase Bank'),
                'account_holder': os.getenv('BANK_ACCOUNT_HOLDER', 'SignalTrust AI Inc.'),
                'account_number': os.getenv('BANK_ACCOUNT_NUMBER_USD', 'XXXXXXXXXX'),
                'routing_number': os.getenv('BANK_ROUTING_NUMBER_USD', 'XXXXXXXXX'),
                'swift_code': os.getenv('BANK_SWIFT_CODE_USD', 'CHASUS33'),
                'iban': os.getenv('BANK_IBAN_USD', ''),
                'bank_address': os.getenv('BANK_ADDRESS_USD', '270 Park Avenue, New York, NY 10017, USA'),
                'currency': 'USD'
            },
            'EUR': {
                'bank_name': os.getenv('BANK_NAME_EUR', 'Deutsche Bank'),
                'account_holder': os.getenv('BANK_ACCOUNT_HOLDER', 'SignalTrust AI Europe'),
                'iban': os.getenv('BANK_IBAN_EUR', 'DEXXXXXXXXXXXXXXXXXX'),
                'swift_code': os.getenv('BANK_SWIFT_CODE_EUR', 'DEUTDEFF'),
                'bic': os.getenv('BANK_BIC_EUR', 'DEUTDEFF'),
                'bank_address': os.getenv('BANK_ADDRESS_EUR', 'Taunusanlage 12, 60325 Frankfurt, Germany'),
                'currency': 'EUR'
            },
            'GBP': {
                'bank_name': os.getenv('BANK_NAME_GBP', 'HSBC UK'),
                'account_holder': os.getenv('BANK_ACCOUNT_HOLDER', 'SignalTrust AI UK Ltd'),
                'account_number': os.getenv('BANK_ACCOUNT_NUMBER_GBP', 'XXXXXXXX'),
                'sort_code': os.getenv('BANK_SORT_CODE_GBP', 'XX-XX-XX'),
                'swift_code': os.getenv('BANK_SWIFT_CODE_GBP', 'HBUKGB4B'),
                'iban': os.getenv('BANK_IBAN_GBP', 'GB'),
                'bank_address': os.getenv('BANK_ADDRESS_GBP', '8 Canada Square, London E14 5HQ, UK'),
                'currency': 'GBP'
            },
            'CAD': {
                'bank_name': os.getenv('BANK_NAME_CAD', 'Royal Bank of Canada'),
                'account_holder': os.getenv('BANK_ACCOUNT_HOLDER', 'SignalTrust AI Canada'),
                'account_number': os.getenv('BANK_ACCOUNT_NUMBER_CAD', 'XXXXXXXXXX'),
                'transit_number': os.getenv('BANK_TRANSIT_NUMBER_CAD', 'XXXXX'),
                'institution_number': os.getenv('BANK_INSTITUTION_NUMBER_CAD', 'XXX'),
                'swift_code': os.getenv('BANK_SWIFT_CODE_CAD', 'ROYCCAT2'),
                'bank_address': os.getenv('BANK_ADDRESS_CAD', '200 Bay Street, Toronto, ON M5J 2J5, Canada'),
                'currency': 'CAD'
            }
        }
        
        # Payment processing time
        self.processing_days = int(os.getenv('BANK_TRANSFER_PROCESSING_DAYS', '3'))
        
        logger.info("Bank transfer processor initialized")
    
    def get_bank_details(self, currency: str = 'USD') -> Dict[str, Any]:
        """
        Get bank account details for a specific currency
        
        Args:
            currency: Currency code (USD, EUR, GBP, CAD)
        
        Returns:
            Bank account details
        """
        if currency not in self.bank_accounts:
            return {
                'success': False,
                'error': f'Currency {currency} not supported'
            }
        
        return {
            'success': True,
            'currency': currency,
            'bank_details': self.bank_accounts[currency],
            'processing_time': f'{self.processing_days} business days'
        }
    
    def get_plan_price(self, plan: str, currency: str = 'USD') -> Dict[str, Any]:
        """
        Get plan price in specific currency
        
        Args:
            plan: Plan name (basic, pro, enterprise)
            currency: Currency code
        
        Returns:
            Price information
        """
        if plan not in self.PLANS_USD:
            return {'success': False, 'error': 'Invalid plan'}
        
        if currency not in self.CURRENCIES:
            return {'success': False, 'error': 'Unsupported currency'}
        
        # Get base price in USD
        base_price_usd = self.PLANS_USD[plan]
        
        # Convert to target currency (use exchange rates from API in production)
        exchange_rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'GBP': 0.79,
            'CAD': 1.35
        }
        
        price = base_price_usd * exchange_rates[currency]
        
        return {
            'success': True,
            'plan': plan,
            'price': round(price, 2),
            'currency': currency,
            'symbol': self.CURRENCIES[currency]['symbol'],
            'usd_equivalent': base_price_usd
        }
    
    def create_transfer_request(self, user_id: str, plan: str, 
                               currency: str = 'USD', 
                               user_info: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Create a new bank transfer payment request
        
        Args:
            user_id: User identifier
            plan: Subscription plan
            currency: Payment currency
            user_info: User information (name, email, etc.)
        
        Returns:
            Transfer request details
        """
        # Get price
        price_info = self.get_plan_price(plan, currency)
        if not price_info.get('success'):
            return price_info
        
        # Get bank details
        bank_info = self.get_bank_details(currency)
        if not bank_info.get('success'):
            return bank_info
        
        # Generate unique reference number
        reference = f"ST-{datetime.now().strftime('%Y%m%d')}-{user_id[:8].upper()}"
        
        # Calculate expiry date
        expiry_date = datetime.now() + timedelta(days=7)
        
        transfer_request = {
            'success': True,
            'transfer_id': f"wire_{datetime.now().timestamp()}_{user_id}",
            'reference_number': reference,
            'user_id': user_id,
            'plan': plan,
            'amount': price_info['price'],
            'currency': currency,
            'symbol': price_info['symbol'],
            'bank_details': bank_info['bank_details'],
            'processing_time': bank_info['processing_time'],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'expires_at': expiry_date.isoformat(),
            'user_info': user_info or {}
        }
        
        # Store transfer request
        self._store_transfer_request(transfer_request)
        
        logger.info(f"Created bank transfer request: {reference}")
        
        return transfer_request
    
    def verify_transfer(self, transfer_id: str, verification_code: str = None) -> Dict[str, Any]:
        """
        Verify a bank transfer (manual verification)
        
        Args:
            transfer_id: Transfer request ID
            verification_code: Optional verification code from bank statement
        
        Returns:
            Verification result
        """
        transfer_request = self._get_transfer_request(transfer_id)
        
        if not transfer_request:
            return {'success': False, 'error': 'Transfer request not found'}
        
        # In production: verify with bank API or manual admin approval
        logger.info(f"Verifying transfer {transfer_id}")
        
        return {
            'success': True,
            'transfer_id': transfer_id,
            'status': 'pending_verification',
            'message': 'Transfer submitted for verification. You will receive confirmation within 1-3 business days.',
            'estimated_confirmation': (datetime.now() + timedelta(days=self.processing_days)).isoformat()
        }
    
    def get_transfer_instructions(self, transfer_id: str, language: str = 'en') -> Dict[str, Any]:
        """
        Get detailed transfer instructions
        
        Args:
            transfer_id: Transfer request ID
            language: Language for instructions (en, fr, es, de)
        
        Returns:
            Detailed transfer instructions
        """
        transfer_request = self._get_transfer_request(transfer_id)
        
        if not transfer_request:
            return {'success': False, 'error': 'Transfer not found'}
        
        bank_details = transfer_request['bank_details']
        currency = transfer_request['currency']
        
        # Instructions in different languages
        instructions = {
            'en': {
                'title': 'Bank Wire Transfer Instructions',
                'steps': [
                    'Log in to your online banking or visit your bank branch',
                    f"Initiate a wire transfer to {bank_details['bank_name']}",
                    f"Amount: {transfer_request['symbol']}{transfer_request['amount']} {currency}",
                    f"Beneficiary: {bank_details['account_holder']}",
                    f"Reference: {transfer_request['reference_number']} (IMPORTANT!)",
                    'Include your email address in the transfer notes',
                    'Save the transfer receipt',
                    'Upload receipt or send confirmation email to payments@signaltrust.ai'
                ],
                'important_notes': [
                    f"⚠️ Always include reference number: {transfer_request['reference_number']}",
                    f"⏰ Payment must be received within 7 days",
                    f"⏱️ Processing time: {bank_details.get('processing_time', '2-3 business days')}",
                    f"📧 You will receive email confirmation once payment is verified"
                ]
            },
            'fr': {
                'title': 'Instructions de Virement Bancaire',
                'steps': [
                    'Connectez-vous à votre banque en ligne ou visitez votre agence',
                    f"Effectuez un virement vers {bank_details['bank_name']}",
                    f"Montant: {transfer_request['symbol']}{transfer_request['amount']} {currency}",
                    f"Bénéficiaire: {bank_details['account_holder']}",
                    f"Référence: {transfer_request['reference_number']} (IMPORTANT!)",
                    'Incluez votre adresse email dans les notes',
                    'Conservez le reçu de virement',
                    'Téléchargez le reçu ou envoyez confirmation à payments@signaltrust.ai'
                ],
                'important_notes': [
                    f"⚠️ Toujours inclure la référence: {transfer_request['reference_number']}",
                    f"⏰ Paiement doit être reçu sous 7 jours",
                    f"⏱️ Délai de traitement: {bank_details.get('processing_time', '2-3 jours ouvrables')}",
                    f"📧 Vous recevrez une confirmation par email"
                ]
            }
        }
        
        lang_instructions = instructions.get(language, instructions['en'])
        
        return {
            'success': True,
            'transfer_id': transfer_id,
            'reference_number': transfer_request['reference_number'],
            'instructions': lang_instructions,
            'bank_details': bank_details,
            'amount': transfer_request['amount'],
            'currency': currency,
            'expires_at': transfer_request['expires_at']
        }
    
    def _store_transfer_request(self, transfer_request: Dict[str, Any]):
        """Store transfer request"""
        filename = f"data/bank_transfers/{transfer_request['transfer_id']}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(transfer_request, f, indent=2)
    
    def _get_transfer_request(self, transfer_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve transfer request"""
        filename = f"data/bank_transfers/{transfer_id}.json"
        
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def list_pending_transfers(self, user_id: str = None) -> Dict[str, Any]:
        """List pending transfers, optionally filtered by user"""
        transfers_dir = "data/bank_transfers"
        
        if not os.path.exists(transfers_dir):
            return {'success': True, 'transfers': []}
        
        pending = []
        for filename in os.listdir(transfers_dir):
            if filename.endswith('.json'):
                with open(os.path.join(transfers_dir, filename), 'r') as f:
                    transfer = json.load(f)
                    if transfer.get('status') == 'pending':
                        if user_id is None or transfer.get('user_id') == user_id:
                            pending.append(transfer)
        
        return {
            'success': True,
            'count': len(pending),
            'transfers': pending
        }


# Global instance
bank_processor = BankTransferProcessor()


def get_bank_processor() -> BankTransferProcessor:
    """Get the global bank transfer processor instance"""
    return bank_processor
