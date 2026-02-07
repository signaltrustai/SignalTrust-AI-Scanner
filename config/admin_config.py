#!/usr/bin/env python3
"""
Admin Configuration Module
Contains default administrator account settings and initialization

⚠️ SECURITY WARNING: This file contains a default password for development purposes.
In production, the password should be changed immediately after first deployment,
and this file should be modified to load credentials from environment variables
or a secure secrets management system.
"""

# Default admin account constants
# ⚠️ FOR DEVELOPMENT ONLY - Change in production!
ADMIN_USER_ID = "owner_admin_001"
ADMIN_EMAIL = "signaltrustai@gmail.com"
ADMIN_PASSWORD = "!Obiwan12!"  # TODO: Load from secure source in production
ADMIN_FULL_NAME = "SignalTrust Admin"
ADMIN_PLAN = "enterprise"
ADMIN_PAYMENT_STATUS = "active"


def get_admin_config():
    """Get default admin configuration.
    
    Returns:
        Dictionary with admin account configuration
    """
    return {
        'user_id': ADMIN_USER_ID,
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD,
        'full_name': ADMIN_FULL_NAME,
        'plan': ADMIN_PLAN,
        'payment_status': ADMIN_PAYMENT_STATUS,
        'is_active': True
    }


def is_admin_email(email: str) -> bool:
    """Check if email is the admin email.
    
    Args:
        email: Email to check
        
    Returns:
        True if email matches admin email
    """
    return email.lower() == ADMIN_EMAIL.lower()


def is_admin_user_id(user_id: str) -> bool:
    """Check if user_id is the admin user_id.
    
    Args:
        user_id: User ID to check
        
    Returns:
        True if user_id matches admin user_id
    """
    return user_id == ADMIN_USER_ID
