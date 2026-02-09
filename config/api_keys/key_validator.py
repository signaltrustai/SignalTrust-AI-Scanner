#!/usr/bin/env python3
"""
API Key Validator
Validates API keys format and tests connectivity

Features:
- Format validation for different API providers
- Connection testing
- Rate limit checking
- Key health monitoring
"""

import os
import re
import requests
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class KeyValidator:
    """Validates API keys and tests connectivity."""
    
    # API key format patterns
    KEY_PATTERNS = {
        'OPENAI_API_KEY': r'^sk-[a-zA-Z0-9]{20,}$',
        'ANTHROPIC_API_KEY': r'^sk-ant-[a-zA-Z0-9\-_]{95,}$',
        'COINGECKO_API_KEY': r'^CG-[a-zA-Z0-9]{32}$',
        'ALPHAVANTAGE_API_KEY': r'^[A-Z0-9]{16}$',
        'WHALEALERT_API_KEY': r'^[a-zA-Z0-9]{32,64}$',
        'NEWS_CATCHER_API_KEY': r'^[a-zA-Z0-9_-]{32,}$',
    }
    
    # API test endpoints
    TEST_ENDPOINTS = {
        'OPENAI_API_KEY': {
            'url': 'https://api.openai.com/v1/models',
            'method': 'GET',
            'headers': lambda key: {'Authorization': f'Bearer {key}'},
        },
        'ANTHROPIC_API_KEY': {
            'url': 'https://api.anthropic.com/v1/messages',
            'method': 'POST',
            'headers': lambda key: {
                'x-api-key': key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            'json': {
                'model': 'claude-3-haiku-20240307',
                'max_tokens': 10,
                'messages': [{'role': 'user', 'content': 'Hi'}]
            }
        },
        'COINGECKO_API_KEY': {
            'url': 'https://api.coingecko.com/api/v3/ping',
            'method': 'GET',
            'headers': lambda key: {'x-cg-pro-api-key': key},
        },
        'ALPHAVANTAGE_API_KEY': {
            'url': 'https://www.alphavantage.co/query',
            'method': 'GET',
            'params': lambda key: {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'IBM',
                'apikey': key,
            },
        },
    }
    
    def __init__(self, timeout: int = 10):
        """
        Initialize validator.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.last_validation = {}
    
    def validate_format(self, key_name: str, key_value: str) -> Tuple[bool, str]:
        """
        Validate API key format.
        
        Args:
            key_name: Name of the key (e.g., 'OPENAI_API_KEY')
            key_value: The key value to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not key_value:
            return False, "Key value is empty"
        
        # Check if we have a pattern for this key
        if key_name not in self.KEY_PATTERNS:
            # Generic validation for unknown keys
            if len(key_value) < 10:
                return False, "Key seems too short"
            return True, "Format unknown, but length OK"
        
        # Validate against pattern
        pattern = self.KEY_PATTERNS[key_name]
        if re.match(pattern, key_value):
            return True, "Format valid"
        else:
            return False, f"Format invalid (expected pattern: {pattern})"
    
    def test_connection(self, key_name: str, key_value: str) -> Tuple[bool, str]:
        """
        Test API key by making a test request.
        
        Args:
            key_name: Name of the key
            key_value: The key value to test
            
        Returns:
            Tuple of (is_valid, message)
        """
        if key_name not in self.TEST_ENDPOINTS:
            return True, "No test endpoint available"
        
        endpoint_config = self.TEST_ENDPOINTS[key_name]
        
        try:
            # Prepare request
            url = endpoint_config['url']
            method = endpoint_config['method']
            
            # Build headers
            headers = endpoint_config['headers'](key_value)
            
            # Build params if any
            params = None
            if 'params' in endpoint_config:
                params = endpoint_config['params'](key_value)
            
            # Build JSON if any
            json_data = endpoint_config.get('json')
            
            # Make request
            if method == 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    json=json_data,
                    timeout=self.timeout
                )
            else:
                return False, f"Unsupported method: {method}"
            
            # Check response
            if response.status_code in [200, 201]:
                self.last_validation[key_name] = datetime.now()
                return True, "Connection successful"
            elif response.status_code == 401:
                return False, "Invalid API key (401 Unauthorized)"
            elif response.status_code == 403:
                return False, "Access forbidden (403)"
            elif response.status_code == 429:
                return False, "Rate limit exceeded (429)"
            else:
                return False, f"Unexpected response: {response.status_code}"
        
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as e:
            logger.error(f"Error testing {key_name}: {str(e)}")
            return False, f"Test failed: {str(e)}"
    
    def validate_key(self, key_name: str, key_value: str, test_connection: bool = False) -> Dict:
        """
        Complete validation of an API key.
        
        Args:
            key_name: Name of the key
            key_value: The key value to validate
            test_connection: Whether to test actual API connection
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'key_name': key_name,
            'valid': False,
            'format_valid': False,
            'format_message': '',
            'connection_valid': None,
            'connection_message': '',
            'tested_at': datetime.now().isoformat(),
        }
        
        # Validate format
        format_valid, format_msg = self.validate_format(key_name, key_value)
        result['format_valid'] = format_valid
        result['format_message'] = format_msg
        
        # Test connection if requested and format is valid
        if test_connection and format_valid:
            conn_valid, conn_msg = self.test_connection(key_name, key_value)
            result['connection_valid'] = conn_valid
            result['connection_message'] = conn_msg
            result['valid'] = format_valid and conn_valid
        else:
            result['valid'] = format_valid
        
        return result
    
    def validate_all_keys(self, keys: Dict[str, str], test_connection: bool = False) -> Dict[str, Dict]:
        """
        Validate multiple keys.
        
        Args:
            keys: Dictionary of key_name -> key_value
            test_connection: Whether to test connections
            
        Returns:
            Dictionary of key_name -> validation_result
        """
        results = {}
        for key_name, key_value in keys.items():
            results[key_name] = self.validate_key(key_name, key_value, test_connection)
        return results
    
    def get_key_health(self, key_name: str) -> Optional[str]:
        """
        Get health status of a key.
        
        Args:
            key_name: Name of the key
            
        Returns:
            'healthy', 'unknown', or error message
        """
        if key_name not in self.last_validation:
            return 'unknown'
        
        last_check = self.last_validation[key_name]
        elapsed = (datetime.now() - last_check).total_seconds()
        
        if elapsed < 3600:  # Less than 1 hour
            return 'healthy'
        elif elapsed < 86400:  # Less than 1 day
            return 'needs_check'
        else:
            return 'stale'


def validate_openai_key(key: str, test: bool = False) -> bool:
    """Quick validation for OpenAI key."""
    validator = KeyValidator()
    result = validator.validate_key('OPENAI_API_KEY', key, test_connection=test)
    return result['valid']


def validate_anthropic_key(key: str, test: bool = False) -> bool:
    """Quick validation for Anthropic key."""
    validator = KeyValidator()
    result = validator.validate_key('ANTHROPIC_API_KEY', key, test_connection=test)
    return result['valid']


if __name__ == "__main__":
    # Example usage
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    print("SignalTrust AI Key Validator")
    print("=" * 50)
    
    validator = KeyValidator()
    
    # Test with environment variables
    test_keys = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'COINGECKO_API_KEY',
        'ALPHAVANTAGE_API_KEY',
    ]
    
    print("\nValidating keys from environment:")
    for key_name in test_keys:
        key_value = os.getenv(key_name)
        if key_value:
            result = validator.validate_key(key_name, key_value, test_connection=False)
            status = "✓" if result['valid'] else "✗"
            print(f"{status} {key_name}: {result['format_message']}")
        else:
            print(f"- {key_name}: Not set in environment")
    
    print("\nTo test connections, set test_connection=True")
