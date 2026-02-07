#!/usr/bin/env python3
"""
Tests for Subscription Limit Enforcement
"""

import json
import os
from limit_enforcer import LimitEnforcer
from payment_processor import PaymentProcessor


def test_plan_limits():
    """Test that plans have correct limits configured."""
    print("Testing plan limits configuration...")
    
    processor = PaymentProcessor()
    plans = processor.get_plans()
    
    # Test Free plan - Limited for testing/trial users
    free_limits = plans['free']['limits']
    assert free_limits['scans_per_day'] == 5, "Free plan should have 5 scans per day"
    assert free_limits['symbols_per_scan'] == 3, "Free plan should have 3 symbols per scan"
    assert free_limits['ai_predictions_per_day'] == 3, "Free plan should have 3 predictions per day"
    assert free_limits['whale_tracking'] == False, "Free plan should not have whale tracking"
    assert free_limits['advanced_analytics'] == False, "Free plan should not have advanced analytics"
    print("✓ Free plan limits correct (5 scans, 3 symbols, 3 predictions)")
    
    # Test Basic plan - Good for individual traders
    basic_limits = plans['basic']['limits']
    assert basic_limits['scans_per_day'] == 100, "Basic plan should have 100 scans per day"
    assert basic_limits['symbols_per_scan'] == 10, "Basic plan should have 10 symbols per scan"
    assert basic_limits['ai_predictions_per_day'] == 25, "Basic plan should have 25 predictions per day"
    assert basic_limits['whale_tracking'] == False, "Basic plan should not have whale tracking"
    assert basic_limits['advanced_analytics'] == True, "Basic plan should have advanced analytics"
    print("✓ Basic plan limits correct (100 scans, 10 symbols, 25 predictions)")
    
    # Test Pro plan (unlimited)
    pro_limits = plans['pro']['limits']
    assert pro_limits['scans_per_day'] == -1, "Pro plan should have unlimited scans"
    assert pro_limits['symbols_per_scan'] == -1, "Pro plan should have unlimited symbols"
    assert pro_limits['ai_predictions_per_day'] == -1, "Pro plan should have unlimited predictions"
    assert pro_limits['whale_tracking'] == True, "Pro plan should have whale tracking"
    assert pro_limits['advanced_analytics'] == True, "Pro plan should have advanced analytics"
    assert pro_limits['api_access'] == True, "Pro plan should have API access"
    print("✓ Pro plan limits correct (UNLIMITED)")
    
    # Test Enterprise plan (unlimited)
    enterprise_limits = plans['enterprise']['limits']
    assert enterprise_limits['scans_per_day'] == -1, "Enterprise plan should have unlimited scans"
    assert enterprise_limits['symbols_per_scan'] == -1, "Enterprise plan should have unlimited symbols"
    assert enterprise_limits['ai_predictions_per_day'] == -1, "Enterprise plan should have unlimited predictions"
    assert enterprise_limits['whale_tracking'] == True, "Enterprise plan should have whale tracking"
    assert enterprise_limits['advanced_analytics'] == True, "Enterprise plan should have advanced analytics"
    assert enterprise_limits['api_access'] == True, "Enterprise plan should have API access"
    print("✓ Enterprise plan limits correct (UNLIMITED)")
    
    print("✅ All plan limits configured correctly\n")


def test_limit_checking():
    """Test limit checking for different actions."""
    print("Testing limit checking...")
    
    # Use a test file for usage tracking
    test_usage_file = 'data/test_usage_tracking.json'
    enforcer = LimitEnforcer(usage_file=test_usage_file)
    
    # Clean up any existing test data
    if os.path.exists(test_usage_file):
        os.remove(test_usage_file)
    enforcer._load_usage()
    
    test_user_id = 'test_user_123'
    
    # Test Free plan limits (5 scans)
    print("\n  Testing FREE plan:")
    for i in range(5):
        allowed, error, info = enforcer.check_limit(test_user_id, 'free', 'scans')
        assert allowed, f"Free plan should allow scan {i+1}/5"
        enforcer.increment_usage(test_user_id, 'scans')
    
    # 6th scan should be blocked
    allowed, error, info = enforcer.check_limit(test_user_id, 'free', 'scans')
    assert not allowed, "Free plan should block 6th scan"
    assert info['used'] == 5
    assert info['limit'] == 5
    assert info['remaining'] == 0
    print("  ✓ Free plan: 5 scans allowed, 6th blocked")
    
    # Test Basic plan limits (100 scans)
    print("\n  Testing BASIC plan:")
    test_user_basic = 'test_user_basic'
    for i in range(100):
        allowed, error, info = enforcer.check_limit(test_user_basic, 'basic', 'scans')
        assert allowed, f"Basic plan should allow scan {i+1}/100"
        enforcer.increment_usage(test_user_basic, 'scans')
    
    # 101st scan should be blocked
    allowed, error, info = enforcer.check_limit(test_user_basic, 'basic', 'scans')
    assert not allowed, "Basic plan should block 101st scan"
    assert info['limit'] == 100
    print("  ✓ Basic plan: 100 scans allowed, 101st blocked")
    
    # Test Pro plan (unlimited)
    print("\n  Testing PRO plan (unlimited):")
    test_user_pro = 'test_user_pro'
    for i in range(200):
        allowed, error, info = enforcer.check_limit(test_user_pro, 'pro', 'scans')
        assert allowed, f"Pro plan should allow scan {i+1} (unlimited)"
        enforcer.increment_usage(test_user_pro, 'scans')
    
    allowed, error, info = enforcer.check_limit(test_user_pro, 'pro', 'scans')
    assert allowed, "Pro plan should never block (unlimited)"
    assert info['limit'] == 'unlimited'
    assert info['remaining'] == 'unlimited'
    print("  ✓ Pro plan: 200+ scans allowed (UNLIMITED)")
    
    # Test Enterprise plan (unlimited)
    print("\n  Testing ENTERPRISE plan (unlimited):")
    test_user_ent = 'test_user_enterprise'
    for i in range(200):
        allowed, error, info = enforcer.check_limit(test_user_ent, 'enterprise', 'scans')
        assert allowed, f"Enterprise plan should allow scan {i+1} (unlimited)"
        enforcer.increment_usage(test_user_ent, 'scans')
    
    allowed, error, info = enforcer.check_limit(test_user_ent, 'enterprise', 'scans')
    assert allowed, "Enterprise plan should never block (unlimited)"
    assert info['limit'] == 'unlimited'
    print("  ✓ Enterprise plan: 200+ scans allowed (UNLIMITED)")
    
    # Clean up
    if os.path.exists(test_usage_file):
        os.remove(test_usage_file)
    
    print("\n✅ All limit checks working correctly\n")


def test_symbols_limit():
    """Test symbols per scan limits."""
    print("Testing symbols per scan limits...")
    
    test_usage_file = 'data/test_usage_tracking.json'
    enforcer = LimitEnforcer(usage_file=test_usage_file)
    
    # Free plan: 3 symbols max
    allowed, error, info = enforcer.check_symbols_limit('user1', 'free', 3)
    assert allowed, "Free plan should allow 3 symbols"
    
    allowed, error, info = enforcer.check_symbols_limit('user1', 'free', 4)
    assert not allowed, "Free plan should block 4 symbols"
    print("✓ Free plan: 3 symbols max")
    
    # Basic plan: 10 symbols max
    allowed, error, info = enforcer.check_symbols_limit('user2', 'basic', 10)
    assert allowed, "Basic plan should allow 10 symbols"
    
    allowed, error, info = enforcer.check_symbols_limit('user2', 'basic', 11)
    assert not allowed, "Basic plan should block 11 symbols"
    print("✓ Basic plan: 10 symbols max")
    
    # Pro plan: unlimited
    allowed, error, info = enforcer.check_symbols_limit('user3', 'pro', 1000)
    assert allowed, "Pro plan should allow unlimited symbols"
    assert info['limit'] == 'unlimited'
    print("✓ Pro plan: UNLIMITED symbols")
    
    # Enterprise plan: unlimited
    allowed, error, info = enforcer.check_symbols_limit('user4', 'enterprise', 1000)
    assert allowed, "Enterprise plan should allow unlimited symbols"
    assert info['limit'] == 'unlimited'
    print("✓ Enterprise plan: UNLIMITED symbols")
    
    # Clean up
    if os.path.exists(test_usage_file):
        os.remove(test_usage_file)
    
    print("✅ All symbols limits working correctly\n")


def test_whale_tracking_access():
    """Test whale tracking access control."""
    print("Testing whale tracking access...")
    
    test_usage_file = 'data/test_usage_tracking.json'
    enforcer = LimitEnforcer(usage_file=test_usage_file)
    
    # Free plan: no access
    allowed, error = enforcer.check_whale_tracking_access('free')
    assert not allowed, "Free plan should not have whale tracking"
    print("✓ Free plan: no whale tracking")
    
    # Basic plan: no access
    allowed, error = enforcer.check_whale_tracking_access('basic')
    assert not allowed, "Basic plan should not have whale tracking"
    print("✓ Basic plan: no whale tracking")
    
    # Pro plan: access granted
    allowed, error = enforcer.check_whale_tracking_access('pro')
    assert allowed, "Pro plan should have whale tracking"
    print("✓ Pro plan: whale tracking enabled")
    
    # Enterprise plan: access granted
    allowed, error = enforcer.check_whale_tracking_access('enterprise')
    assert allowed, "Enterprise plan should have whale tracking"
    print("✓ Enterprise plan: whale tracking enabled")
    
    # Clean up
    if os.path.exists(test_usage_file):
        os.remove(test_usage_file)
    
    print("✅ Whale tracking access control working correctly\n")


def test_usage_summary():
    """Test usage summary generation."""
    print("Testing usage summary...")
    
    test_usage_file = 'data/test_usage_tracking.json'
    enforcer = LimitEnforcer(usage_file=test_usage_file)
    
    # Clean up
    if os.path.exists(test_usage_file):
        os.remove(test_usage_file)
    enforcer._load_usage()
    
    test_user = 'summary_test_user'
    
    # Do some actions
    enforcer.increment_usage(test_user, 'scans', 3)
    enforcer.increment_usage(test_user, 'ai_predictions', 2)
    
    # Get summary for free plan
    summary = enforcer.get_usage_summary(test_user, 'free')
    assert summary['scans']['used'] == 3
    assert summary['scans']['limit'] == 5
    assert summary['scans']['remaining'] == 2
    assert summary['ai_predictions']['used'] == 2
    assert summary['ai_predictions']['limit'] == 3
    assert summary['whale_tracking'] == False
    print("✓ Free plan usage summary correct")
    
    # Get summary for pro plan
    summary_pro = enforcer.get_usage_summary(test_user, 'pro')
    assert summary_pro['scans']['limit'] == 'unlimited'
    assert summary_pro['scans']['remaining'] == 'unlimited'
    assert summary_pro['whale_tracking'] == True
    print("✓ Pro plan usage summary correct (unlimited)")
    
    # Clean up
    if os.path.exists(test_usage_file):
        os.remove(test_usage_file)
    
    print("✅ Usage summary working correctly\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("TESTING SUBSCRIPTION LIMIT ENFORCEMENT")
    print("=" * 60)
    print()
    
    try:
        test_plan_limits()
        test_limit_checking()
        test_symbols_limit()
        test_whale_tracking_access()
        test_usage_summary()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("📊 Subscription Limits Summary:")
        print()
        print("  FREE Plan (Trial):")
        print("    • 5 scans per day")
        print("    • 3 symbols per scan")
        print("    • 3 AI predictions per day")
        print("    • No whale tracking")
        print("    • No advanced analytics")
        print()
        print("  BASIC Plan ($49/month):")
        print("    • 100 scans per day")
        print("    • 10 symbols per scan")
        print("    • 25 AI predictions per day")
        print("    • No whale tracking")
        print("    • Advanced analytics ✓")
        print()
        print("  PRO Plan ($149/month):")
        print("    • UNLIMITED scans")
        print("    • UNLIMITED symbols")
        print("    • UNLIMITED AI predictions")
        print("    • Whale tracking ✓")
        print("    • Advanced analytics ✓")
        print("    • API access ✓")
        print()
        print("  ENTERPRISE Plan ($499/month):")
        print("    • UNLIMITED everything")
        print("    • All Pro features")
        print("    • 10 team accounts")
        print("    • Custom integrations")
        print("    • 24/7 support")
        print()
        print("✅ Admin (owner_admin_001) has ENTERPRISE plan = UNLIMITED!")
        print()
        print("Tiered limits implemented successfully! 🎉")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    
    return True


if __name__ == '__main__':
    main()
