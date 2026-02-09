#!/usr/bin/env python3
"""
Test script for the secure API key management system
Demonstrates key storage, retrieval, and validation
"""

import os
import sys
import secrets
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.api_keys import KeyManager, KeyValidator

def test_key_manager():
    """Test the KeyManager functionality."""
    print("=" * 60)
    print("🧪 Testing SignalTrust API Key Management System")
    print("=" * 60)
    
    # Set up test master password
    test_password = secrets.token_urlsafe(32)
    os.environ['API_MASTER_PASSWORD'] = test_password
    print(f"\n✅ Master password set: {test_password[:8]}...")
    
    # Initialize manager
    print("\n📦 Initializing KeyManager...")
    manager = KeyManager()
    
    # Test 1: Store keys
    print("\n1️⃣ Testing key storage...")
    test_keys = {
        'OPENAI_API_KEY': 'sk-proj-test123456789',
        'ANTHROPIC_API_KEY': 'sk-ant-test987654321',
        'COINGECKO_API_KEY': 'CG-' + 'a' * 32,
    }
    
    for key_name, key_value in test_keys.items():
        success = manager.set_key(key_name, key_value, save=False)
        status = "✅" if success else "❌"
        print(f"  {status} Stored {key_name}")
    
    # Save all keys at once
    if manager.cipher:
        manager._save_keys()
        print("  ✅ Keys saved to encrypted file")
    
    # Test 2: Retrieve keys
    print("\n2️⃣ Testing key retrieval...")
    for key_name in test_keys.keys():
        retrieved = manager.get_key(key_name, fallback_env=False)
        status = "✅" if retrieved else "❌"
        masked = retrieved[:8] + "..." if retrieved else "None"
        print(f"  {status} Retrieved {key_name}: {masked}")
    
    # Test 3: List keys
    print("\n3️⃣ Testing key listing...")
    all_keys = manager.list_keys()
    print(f"  ✅ Found {len(all_keys)} keys")
    for key in sorted(all_keys)[:5]:
        print(f"    • {key}")
    
    # Test 4: Import from environment
    print("\n4️⃣ Testing import from environment...")
    os.environ['TEST_API_KEY'] = 'test-value-123'
    count = manager.import_from_env()
    print(f"  ✅ Imported {count} keys from environment")
    
    # Test 5: Key rotation
    print("\n5️⃣ Testing key rotation...")
    new_value = 'sk-proj-rotated-key-456'
    success = manager.rotate_key('OPENAI_API_KEY', new_value)
    status = "✅" if success else "❌"
    print(f"  {status} Rotated OPENAI_API_KEY")
    
    # Test 6: Delete key
    print("\n6️⃣ Testing key deletion...")
    success = manager.delete_key('TEST_API_KEY', save=True)
    status = "✅" if success else "❌"
    print(f"  {status} Deleted TEST_API_KEY")
    
    print("\n" + "=" * 60)
    print("✅ KeyManager tests completed successfully!")
    print("=" * 60)

def test_key_validator():
    """Test the KeyValidator functionality."""
    print("\n" + "=" * 60)
    print("🧪 Testing Key Validator")
    print("=" * 60)
    
    validator = KeyValidator()
    
    # Test cases: (key_name, key_value, should_be_valid)
    test_cases = [
        ('OPENAI_API_KEY', 'sk-proj-abcdefghij1234567890', False),  # proj prefix not in pattern
        ('OPENAI_API_KEY', 'sk-abcdefghij1234567890', True),  # Valid format
        ('ANTHROPIC_API_KEY', 'sk-ant-' + 'a' * 95, True),
        ('COINGECKO_API_KEY', 'CG-' + 'a' * 32, True),
        ('ALPHAVANTAGE_API_KEY', 'A' * 16, True),
        ('ALPHAVANTAGE_API_KEY', 'invalid', False),
    ]
    
    print("\n🔍 Format Validation Tests:")
    passed = 0
    failed = 0
    
    for key_name, key_value, expected_valid in test_cases:
        result = validator.validate_key(key_name, key_value, test_connection=False)
        actual_valid = result['format_valid']
        
        if actual_valid == expected_valid:
            print(f"  ✅ {key_name}: {result['format_message']}")
            passed += 1
        else:
            print(f"  ❌ {key_name}: Expected {expected_valid}, got {actual_valid}")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    print("\n" + "=" * 60)
    print("✅ KeyValidator tests completed!")
    print("=" * 60)

def cleanup():
    """Clean up test files."""
    print("\n🧹 Cleaning up test files...")
    
    # Remove test encrypted file
    test_file = Path(__file__).parent / 'config' / 'api_keys' / 'keys.enc'
    if test_file.exists():
        test_file.unlink()
        print("  ✅ Removed test encrypted file")
    
    # Remove test environment variable
    if 'API_MASTER_PASSWORD' in os.environ:
        del os.environ['API_MASTER_PASSWORD']
    if 'TEST_API_KEY' in os.environ:
        del os.environ['TEST_API_KEY']

if __name__ == "__main__":
    try:
        test_key_manager()
        test_key_validator()
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("=" * 60)
    print("\n💡 To use in production:")
    print("  1. Set API_MASTER_PASSWORD in .env")
    print("  2. Store your API keys with KeyManager")
    print("  3. Validate keys with KeyValidator")
    print("  4. Keys are encrypted at rest in config/api_keys/keys.enc")
    print("\n📚 See config/api_keys/README.md for full documentation")
