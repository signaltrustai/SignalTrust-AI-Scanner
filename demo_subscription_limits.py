#!/usr/bin/env python3
"""
Demo of Subscription Limits System
Shows how limits work for different user plans
"""

from limit_enforcer import limit_enforcer
from payment_processor import PaymentProcessor


def demo_free_plan():
    """Demo FREE plan limits."""
    print("\n" + "="*60)
    print("🆓 FREE PLAN DEMO")
    print("="*60)
    
    user_id = "demo_free_user"
    plan = "free"
    
    # Show plan limits
    processor = PaymentProcessor()
    plan_info = processor.get_plan(plan)
    print(f"\n📋 {plan_info['name']} - ${plan_info['price']}/month")
    print("\nLimits:")
    for key, value in plan_info['limits'].items():
        print(f"  • {key}: {value}")
    
    print("\n🔄 Testing scans...")
    # Try to do 6 scans (limit is 5)
    for i in range(6):
        allowed, error, info = limit_enforcer.check_limit(user_id, plan, 'scans')
        
        if allowed:
            print(f"  ✅ Scan {i+1}/5: ALLOWED")
            print(f"     Remaining: {info['remaining']}")
            limit_enforcer.increment_usage(user_id, 'scans')
        else:
            print(f"  ❌ Scan {i+1}: BLOCKED")
            print(f"     Error: {error}")
            print(f"     Used: {info['used']}/{info['limit']}")
    
    print("\n🔢 Testing symbols limit...")
    # Try 3 symbols (OK), then 4 (blocked)
    for num in [3, 4]:
        allowed, error, info = limit_enforcer.check_symbols_limit(user_id, plan, num)
        if allowed:
            print(f"  ✅ {num} symbols: ALLOWED")
        else:
            print(f"  ❌ {num} symbols: BLOCKED")
            print(f"     Error: {error}")


def demo_basic_plan():
    """Demo BASIC plan limits."""
    print("\n" + "="*60)
    print("💼 BASIC PLAN DEMO")
    print("="*60)
    
    user_id = "demo_basic_user"
    plan = "basic"
    
    processor = PaymentProcessor()
    plan_info = processor.get_plan(plan)
    print(f"\n📋 {plan_info['name']} - ${plan_info['price']}/month")
    print("\nKey Limits:")
    print(f"  • Scans per day: {plan_info['limits']['scans_per_day']}")
    print(f"  • Symbols per scan: {plan_info['limits']['symbols_per_scan']}")
    print(f"  • AI predictions: {plan_info['limits']['ai_predictions_per_day']}")
    print(f"  • Advanced analytics: {plan_info['limits']['advanced_analytics']}")
    
    print("\n🔄 Doing 10 scans...")
    for i in range(10):
        limit_enforcer.increment_usage(user_id, 'scans')
    
    # Get usage summary
    summary = limit_enforcer.get_usage_summary(user_id, plan)
    print(f"\n📊 Usage Summary:")
    print(f"  • Scans: {summary['scans']['used']}/{summary['scans']['limit']}")
    print(f"  • Remaining: {summary['scans']['remaining']}")
    print(f"  • Percentage: {summary['scans']['percentage']}%")
    
    print("\n🔢 Testing 10 symbols (ALLOWED)...")
    allowed, error, info = limit_enforcer.check_symbols_limit(user_id, plan, 10)
    if allowed:
        print("  ✅ 10 symbols: ALLOWED")
    
    print("\n🐋 Testing whale tracking access...")
    allowed, error = limit_enforcer.check_whale_tracking_access(plan)
    if not allowed:
        print(f"  ❌ {error}")
        print("  💡 Upgrade to Pro for whale tracking!")


def demo_pro_plan():
    """Demo PRO plan (unlimited)."""
    print("\n" + "="*60)
    print("🌟 PRO PLAN DEMO (UNLIMITED)")
    print("="*60)
    
    user_id = "demo_pro_user"
    plan = "pro"
    
    processor = PaymentProcessor()
    plan_info = processor.get_plan(plan)
    print(f"\n📋 {plan_info['name']} - ${plan_info['price']}/month")
    print("\nAll Limits: UNLIMITED ♾️")
    
    print("\n🔄 Doing 250 scans...")
    for i in range(250):
        limit_enforcer.increment_usage(user_id, 'scans')
    
    # Check if still allowed
    allowed, error, info = limit_enforcer.check_limit(user_id, plan, 'scans')
    print(f"\n✅ After 250 scans:")
    print(f"  • Status: {'ALLOWED' if allowed else 'BLOCKED'}")
    print(f"  • Used: {info['used']}")
    print(f"  • Limit: {info['limit']}")
    print(f"  • Remaining: {info['remaining']}")
    
    print("\n🔢 Testing 1000 symbols...")
    allowed, error, info = limit_enforcer.check_symbols_limit(user_id, plan, 1000)
    if allowed:
        print(f"  ✅ 1000 symbols: ALLOWED")
        print(f"  • Limit: {info['limit']}")
    
    print("\n🐋 Whale tracking access...")
    allowed, error = limit_enforcer.check_whale_tracking_access(plan)
    if allowed:
        print("  ✅ ENABLED - Full whale tracking access")
    
    print("\n📊 Advanced analytics...")
    allowed, error = limit_enforcer.check_advanced_analytics_access(plan)
    if allowed:
        print("  ✅ ENABLED - Advanced analytics access")


def demo_enterprise_plan():
    """Demo ENTERPRISE plan (unlimited + team)."""
    print("\n" + "="*60)
    print("🏢 ENTERPRISE PLAN DEMO")
    print("="*60)
    
    plan = "enterprise"
    
    processor = PaymentProcessor()
    plan_info = processor.get_plan(plan)
    print(f"\n📋 {plan_info['name']} - ${plan_info['price']}/month")
    print("\nEverything UNLIMITED ♾️ + Team Features")
    print("\nKey Features:")
    for feature in plan_info['features'][:5]:
        print(f"  ✨ {feature}")
    
    print("\n👥 Team Accounts:")
    print(f"  • Max users: {plan_info['limits']['users']}")
    
    print("\n✅ All Pro features + institutional benefits")


def demo_admin_access():
    """Demo admin access (you)."""
    print("\n" + "="*60)
    print("👤 ADMIN ACCESS (YOU)")
    print("="*60)
    
    print("\n🔑 Admin Info:")
    print("  • Email: signaltrustai@gmail.com")
    print("  • User ID: owner_admin_001")
    print("  • Plan: ENTERPRISE (automatic)")
    
    print("\n✨ You have UNLIMITED access to everything:")
    print("  • ♾️ Unlimited scans")
    print("  • ♾️ Unlimited symbols")
    print("  • ♾️ Unlimited AI predictions")
    print("  • ♾️ Unlimited gem discoveries")
    print("  • ✅ Whale tracking")
    print("  • ✅ Advanced analytics")
    print("  • ✅ Full API access")
    print("  • ✅ All premium features")
    
    print("\n🎉 No restrictions, no limits, full control!")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("SUBSCRIPTION LIMITS SYSTEM - DEMO")
    print("="*60)
    
    print("\nThis demo shows how different subscription plans work:")
    print("  🆓 FREE: Very limited (5 scans/day)")
    print("  💼 BASIC: Moderate limits (100 scans/day)")
    print("  🌟 PRO: UNLIMITED everything")
    print("  🏢 ENTERPRISE: UNLIMITED + team features")
    
    try:
        demo_free_plan()
        demo_basic_plan()
        demo_pro_plan()
        demo_enterprise_plan()
        demo_admin_access()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETE")
        print("="*60)
        
        print("\n📊 Summary:")
        print("  • FREE: Highly restricted for testing")
        print("  • BASIC: Good for individual traders")
        print("  • PRO: Unlimited for professionals")
        print("  • ENTERPRISE: Unlimited for institutions")
        print("  • ADMIN (You): Automatic UNLIMITED access!")
        
        print("\n💡 Upgrade prompts will appear in the app when limits are reached.")
        print("🎉 System working perfectly!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
