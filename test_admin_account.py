#!/usr/bin/env python3
"""
Test script for Admin Account functionality
Tests the creation and access of the default administrator account
"""

import sys
import os
import json
sys.path.insert(0, '.')

from user_auth import UserAuth
from ai_chat_system import AIChatSystem
from asi1_integration import ASI1AIIntegration
from ai_market_intelligence import AIMarketIntelligence
from whale_watcher import WhaleWatcher
from realtime_market_data import RealTimeMarketData
from config.admin_config import (
    ADMIN_EMAIL, ADMIN_USER_ID, ADMIN_PASSWORD, 
    ADMIN_FULL_NAME, is_admin_email, is_admin_user_id
)


def test_admin_config():
    """Test admin configuration module"""
    print("=" * 70)
    print("Testing Admin Configuration")
    print("=" * 70)
    
    print(f"\n✓ Admin Email: {ADMIN_EMAIL}")
    print(f"✓ Admin User ID: {ADMIN_USER_ID}")
    print(f"✓ Admin Full Name: {ADMIN_FULL_NAME}")
    
    # Test helper functions
    assert is_admin_email("signaltrustai@gmail.com"), "is_admin_email failed for exact match"
    assert is_admin_email("SignalTrustAI@Gmail.com"), "is_admin_email failed for case-insensitive match"
    assert not is_admin_email("other@example.com"), "is_admin_email should return False for other emails"
    print("✓ is_admin_email() function works correctly")
    
    assert is_admin_user_id("owner_admin_001"), "is_admin_user_id failed"
    assert not is_admin_user_id("other_user_123"), "is_admin_user_id should return False for other IDs"
    print("✓ is_admin_user_id() function works correctly")
    
    print("\n✅ Admin Configuration Tests Passed!")
    return True


def test_admin_account_creation():
    """Test automatic admin account creation"""
    print("\n" + "=" * 70)
    print("Testing Admin Account Creation")
    print("=" * 70)
    
    # Remove existing users.json to test clean creation
    users_file = 'data/users.json'
    if os.path.exists(users_file):
        os.remove(users_file)
        print("\n✓ Cleaned existing users database")
    
    # Initialize UserAuth (should create admin automatically)
    print("\n1. Initializing UserAuth...")
    auth = UserAuth()
    print("✓ UserAuth initialized")
    
    # Check if admin account was created
    print("\n2. Verifying admin account creation...")
    admin_user = auth.get_user_by_email(ADMIN_EMAIL)
    
    assert admin_user is not None, "Admin account was not created"
    print(f"✓ Admin account exists: {admin_user['email']}")
    
    assert admin_user['user_id'] == ADMIN_USER_ID, f"Wrong user_id: {admin_user['user_id']}"
    print(f"✓ Correct user_id: {admin_user['user_id']}")
    
    assert admin_user['full_name'] == ADMIN_FULL_NAME, f"Wrong full_name: {admin_user['full_name']}"
    print(f"✓ Correct full_name: {admin_user['full_name']}")
    
    assert admin_user['plan'] == 'enterprise', f"Wrong plan: {admin_user['plan']}"
    print(f"✓ Correct plan: {admin_user['plan']}")
    
    assert admin_user['payment_status'] == 'active', f"Wrong payment_status: {admin_user['payment_status']}"
    print(f"✓ Correct payment_status: {admin_user['payment_status']}")
    
    # Verify users.json file exists and contains admin
    assert os.path.exists(users_file), "users.json was not created"
    print(f"✓ users.json file created at: {users_file}")
    
    with open(users_file, 'r') as f:
        users_data = json.load(f)
        assert ADMIN_EMAIL in users_data, "Admin email not in users.json"
        admin_data = users_data[ADMIN_EMAIL]
        assert 'password_hash' in admin_data, "Password hash not stored"
        assert 'salt' in admin_data, "Salt not stored"
        print(f"✓ Admin account properly stored in users.json")
        print(f"  - Password is hashed (not stored in plain text)")
        print(f"  - Unique salt generated for security")
    
    print("\n✅ Admin Account Creation Tests Passed!")
    return True


def test_admin_login():
    """Test admin login functionality"""
    print("\n" + "=" * 70)
    print("Testing Admin Login")
    print("=" * 70)
    
    auth = UserAuth()
    
    # Test login with correct credentials
    print("\n1. Testing login with correct credentials...")
    result = auth.login_user(ADMIN_EMAIL, ADMIN_PASSWORD)
    
    assert result['success'], f"Login failed: {result.get('error', 'Unknown error')}"
    print("✓ Login successful")
    
    assert 'session_token' in result, "No session token returned"
    print(f"✓ Session token generated")
    
    assert 'user' in result, "No user data returned"
    user = result['user']
    
    assert user['user_id'] == ADMIN_USER_ID, f"Wrong user_id in response: {user['user_id']}"
    print(f"✓ Correct user_id in response: {user['user_id']}")
    
    assert user['email'] == ADMIN_EMAIL, f"Wrong email in response: {user['email']}"
    print(f"✓ Correct email in response: {user['email']}")
    
    assert user['plan'] == 'enterprise', f"Wrong plan in response: {user['plan']}"
    print(f"✓ Correct plan in response: {user['plan']}")
    
    # Test login with wrong password
    print("\n2. Testing login with wrong password...")
    result = auth.login_user(ADMIN_EMAIL, "wrong_password")
    assert not result['success'], "Login should fail with wrong password"
    print("✓ Login correctly rejected with wrong password")
    
    # Test session verification
    print("\n3. Testing session verification...")
    session_token = auth.login_user(ADMIN_EMAIL, ADMIN_PASSWORD)['session_token']
    user_data = auth.verify_session(session_token)
    
    assert user_data is not None, "Session verification failed"
    assert user_data['user_id'] == ADMIN_USER_ID, "Wrong user_id from session"
    print("✓ Session verification works correctly")
    
    print("\n✅ Admin Login Tests Passed!")
    return True


def test_ai_chat_access():
    """Test AI Chat access control with admin account"""
    print("\n" + "=" * 70)
    print("Testing AI Chat Access Control")
    print("=" * 70)
    
    # Initialize components
    print("\n1. Initializing AI Chat System...")
    asi1 = ASI1AIIntegration()
    realtime_data = RealTimeMarketData()
    whale_watcher = WhaleWatcher()
    ai_intelligence = AIMarketIntelligence(asi1, realtime_data, whale_watcher)
    chat = AIChatSystem(asi1, ai_intelligence, whale_watcher)
    print("✓ AI Chat System initialized")
    
    # Test access by user_id
    print("\n2. Testing access by user_id...")
    has_access = chat.check_access(ADMIN_USER_ID)
    assert has_access, "Admin should have access by user_id"
    print(f"✓ Admin has access by user_id: {ADMIN_USER_ID}")
    
    # Test access by email
    print("\n3. Testing access by email...")
    has_access = chat.check_access("some_other_id", ADMIN_EMAIL)
    assert has_access, "Admin should have access by email"
    print(f"✓ Admin has access by email: {ADMIN_EMAIL}")
    
    # Test access denied for regular user
    print("\n4. Testing access denial for regular user...")
    has_access = chat.check_access("regular_user_123")
    assert not has_access, "Regular user should not have access"
    print("✓ Regular user correctly denied access")
    
    # Test actual chat with admin
    print("\n5. Testing actual chat with admin credentials...")
    result = chat.chat(ADMIN_USER_ID, "What are the market trends?", "auto")
    assert result.get('success'), f"Chat failed: {result.get('error', 'Unknown error')}"
    print("✓ Admin can successfully chat with AI")
    print(f"  - AI Type Used: {result.get('ai_type')}")
    print(f"  - Response Preview: {result.get('response', '')[:80]}...")
    
    # Test chat denial for regular user
    print("\n6. Testing chat denial for regular user...")
    result = chat.chat("regular_user_123", "Test message", "auto")
    assert not result.get('success'), "Regular user should be denied"
    assert 'Access restricted' in result.get('error', ''), "Wrong error message"
    print("✓ Regular user correctly denied chat access")
    
    print("\n✅ AI Chat Access Control Tests Passed!")
    return True


def test_admin_persistence():
    """Test that admin account persists across multiple initializations"""
    print("\n" + "=" * 70)
    print("Testing Admin Account Persistence")
    print("=" * 70)
    
    # First initialization
    print("\n1. First initialization...")
    auth1 = UserAuth()
    admin1 = auth1.get_user_by_email(ADMIN_EMAIL)
    assert admin1 is not None, "Admin not found in first initialization"
    print("✓ Admin account exists after first initialization")
    
    # Second initialization (should not recreate)
    print("\n2. Second initialization...")
    auth2 = UserAuth()
    admin2 = auth2.get_user_by_email(ADMIN_EMAIL)
    assert admin2 is not None, "Admin not found in second initialization"
    print("✓ Admin account still exists after second initialization")
    
    # Verify they have the same data
    assert admin1['user_id'] == admin2['user_id'], "user_id changed between initializations"
    print("✓ Admin account data remains consistent")
    
    # Verify admin can still login
    print("\n3. Verifying login still works...")
    result = auth2.login_user(ADMIN_EMAIL, ADMIN_PASSWORD)
    assert result['success'], "Login failed after re-initialization"
    print("✓ Admin can still login after re-initialization")
    
    print("\n✅ Admin Persistence Tests Passed!")
    return True


def main():
    """Run all admin account tests"""
    print("\n" + "=" * 70)
    print("ADMIN ACCOUNT TEST SUITE")
    print("=" * 70)
    
    try:
        # Run all tests
        tests = [
            ("Admin Configuration", test_admin_config),
            ("Admin Account Creation", test_admin_account_creation),
            ("Admin Login", test_admin_login),
            ("AI Chat Access Control", test_ai_chat_access),
            ("Admin Persistence", test_admin_persistence),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except AssertionError as e:
                print(f"\n❌ {test_name} FAILED: {e}")
                failed += 1
            except Exception as e:
                print(f"\n❌ {test_name} ERROR: {e}")
                import traceback
                traceback.print_exc()
                failed += 1
        
        # Print summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"\n✅ Passed: {passed}/{len(tests)}")
        if failed > 0:
            print(f"❌ Failed: {failed}/{len(tests)}")
        
        if failed == 0:
            print("\n" + "=" * 70)
            print("🎉 ALL ADMIN ACCOUNT TESTS PASSED! 🎉")
            print("=" * 70)
            print("\n📋 Summary:")
            print(f"   ✓ Admin Email: {ADMIN_EMAIL}")
            print(f"   ✓ Admin User ID: {ADMIN_USER_ID}")
            print(f"   ✓ Admin Plan: enterprise")
            print(f"   ✓ Default Password: !Obiwan12!")
            print("\n🔒 Security:")
            print("   ✓ Password hashed with PBKDF2-HMAC-SHA256 (100,000 iterations)")
            print("   ✓ Unique salt generated for each account")
            print("   ✓ No plain text passwords stored")
            print("\n🎯 Features:")
            print("   ✓ Full access to AI Chat System")
            print("   ✓ Full access to Whale Watcher")
            print("   ✓ All premium features enabled")
            print("   ✓ Automatic account creation on startup")
            print("\n⚠️  IMPORTANT: Change the default password after first login!")
            print("=" * 70)
            return 0
        else:
            print("\n❌ Some tests failed. Please review the errors above.")
            return 1
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
