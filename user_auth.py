#!/usr/bin/env python3
"""
User Authentication Module
Handles user registration, login, and session management
"""

import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional


class UserAuth:
    """User authentication and management"""
    
    def __init__(self, users_file: str = 'data/users.json'):
        """Initialize user authentication.
        
        Args:
            users_file: Path to users database file
        """
        self.users_file = users_file
        self.sessions = {}
        self._ensure_data_dir()
        self._load_users()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.users_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_users(self):
        """Load users from file."""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, IOError, FileNotFoundError):
                self.users = {}
        else:
            self.users = {}
    
    def _save_users(self):
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash password with salt.
        
        Args:
            password: Plain text password
            salt: Salt for hashing (generated if None)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                        password.encode('utf-8'),
                                        salt.encode('utf-8'),
                                        100000)
        return pwd_hash.hex(), salt
    
    def register_user(self, email: str, password: str, full_name: str, 
                     plan: str = 'free') -> Dict:
        """Register a new user.
        
        Args:
            email: User email
            password: User password
            full_name: User's full name
            plan: Subscription plan
            
        Returns:
            Registration result
        """
        # Validate email
        if not email or '@' not in email:
            return {'success': False, 'error': 'Invalid email address'}
        
        # Check if user already exists
        if email in self.users:
            return {'success': False, 'error': 'User already exists'}
        
        # Validate password
        if len(password) < 8:
            return {'success': False, 'error': 'Password must be at least 8 characters'}
        
        # Hash password
        pwd_hash, salt = self._hash_password(password)
        
        # Create user
        user_id = secrets.token_hex(16)
        self.users[email] = {
            'user_id': user_id,
            'email': email,
            'full_name': full_name,
            'password_hash': pwd_hash,
            'salt': salt,
            'plan': plan,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'is_active': True,
            'payment_status': 'pending' if plan != 'free' else 'active'
        }
        
        self._save_users()
        
        return {
            'success': True,
            'user_id': user_id,
            'message': 'Registration successful'
        }
    
    def login_user(self, email: str, password: str) -> Dict:
        """Login user.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Login result with session token
        """
        # Check if user exists
        if email not in self.users:
            return {'success': False, 'error': 'Invalid credentials'}
        
        user = self.users[email]
        
        # Check if user is active
        if not user.get('is_active', True):
            return {'success': False, 'error': 'Account is inactive'}
        
        # Verify password
        pwd_hash, _ = self._hash_password(password, user['salt'])
        if pwd_hash != user['password_hash']:
            return {'success': False, 'error': 'Invalid credentials'}
        
        # Create session
        session_token = secrets.token_hex(32)
        self.sessions[session_token] = {
            'user_id': user['user_id'],
            'email': email,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        self._save_users()
        
        return {
            'success': True,
            'session_token': session_token,
            'user': {
                'user_id': user['user_id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'plan': user['plan'],
                'payment_status': user.get('payment_status', 'active')
            }
        }
    
    def verify_session(self, session_token: str) -> Optional[Dict]:
        """Verify session token.
        
        Args:
            session_token: Session token to verify
            
        Returns:
            User data if valid, None otherwise
        """
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check if session expired
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            del self.sessions[session_token]
            return None
        
        # Get user data
        email = session['email']
        if email in self.users:
            user = self.users[email]
            return {
                'user_id': user['user_id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'plan': user['plan'],
                'payment_status': user.get('payment_status', 'active')
            }
        
        return None
    
    def logout_user(self, session_token: str) -> Dict:
        """Logout user.
        
        Args:
            session_token: Session token
            
        Returns:
            Logout result
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return {'success': True, 'message': 'Logged out successfully'}
        
        return {'success': False, 'error': 'Invalid session'}
    
    def update_user_plan(self, email: str, plan: str, payment_status: str = 'active') -> Dict:
        """Update user subscription plan.
        
        Args:
            email: User email
            plan: New plan
            payment_status: Payment status
            
        Returns:
            Update result
        """
        if email not in self.users:
            return {'success': False, 'error': 'User not found'}
        
        self.users[email]['plan'] = plan
        self.users[email]['payment_status'] = payment_status
        self.users[email]['plan_updated_at'] = datetime.now().isoformat()
        
        self._save_users()
        
        return {'success': True, 'message': 'Plan updated successfully'}
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User data (without sensitive info)
        """
        if email not in self.users:
            return None
        
        user = self.users[email]
        return {
            'user_id': user['user_id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'plan': user['plan'],
            'created_at': user['created_at'],
            'payment_status': user.get('payment_status', 'active')
        }
