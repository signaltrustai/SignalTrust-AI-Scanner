#!/usr/bin/env python3
"""
Test Navigation Menu Changes
Verify that TradingLive link appears in all navigation menus and logo is clickable
"""

import os
import sys


def test_tradingview_renamed():
    """Test that TradingView has been renamed to TradingLive"""
    print("🧪 Testing TradingView renamed to TradingLive...")
    
    template_files = [
        'templates/index.html',
        'templates/tradingview.html',
    ]
    
    all_passed = True
    for template in template_files:
        if not os.path.exists(template):
            print(f"❌ Template {template} not found")
            all_passed = False
            continue
            
        with open(template, 'r') as f:
            content = f.read()
            
        # Check for TradingLive
        if 'TradingLive' in content:
            print(f"✅ {template} contains 'TradingLive'")
        else:
            print(f"❌ {template} does not contain 'TradingLive'")
            all_passed = False
    
    return all_passed


def test_tradingview_in_all_menus():
    """Test that TradingLive link appears in all navigation menus"""
    print("\n🧪 Testing TradingLive link in all menus...")
    
    template_files = [
        'templates/index.html',
        'templates/dashboard.html',
        'templates/scanner.html',
        'templates/analyzer.html',
        'templates/predictions.html',
        'templates/settings.html',
        'templates/whale_watcher.html',
        'templates/ai_intelligence.html',
        'templates/notifications.html',
        'templates/ai_chat.html',
        'templates/pricing.html',
        'templates/tradingview.html',
    ]
    
    all_passed = True
    for template in template_files:
        if not os.path.exists(template):
            print(f"⚠️  Template {template} not found, skipping...")
            continue
            
        with open(template, 'r') as f:
            content = f.read()
        
        # Check if it has nav-menu and contains tradingview link
        if 'nav-menu' in content or 'nav-container' in content:
            if '/tradingview' in content:
                print(f"✅ {template} has TradingLive link")
            else:
                print(f"❌ {template} missing TradingLive link")
                all_passed = False
        else:
            print(f"⚠️  {template} has no navigation menu, skipping...")
    
    return all_passed


def test_logo_clickable():
    """Test that logo (nav-brand) is clickable"""
    print("\n🧪 Testing logo is clickable...")
    
    template_files = [
        'templates/index.html',
        'templates/dashboard.html',
        'templates/scanner.html',
        'templates/analyzer.html',
        'templates/predictions.html',
        'templates/settings.html',
        'templates/whale_watcher.html',
        'templates/ai_intelligence.html',
        'templates/notifications.html',
        'templates/pricing.html',
        'templates/tradingview.html',
    ]
    
    all_passed = True
    for template in template_files:
        if not os.path.exists(template):
            print(f"⚠️  Template {template} not found, skipping...")
            continue
            
        with open(template, 'r') as f:
            content = f.read()
        
        # Check if logo is wrapped in anchor tag
        if 'nav-brand' in content:
            if '<a href="/" class="nav-brand"' in content or '<a href="/" class="logo"' in content:
                print(f"✅ {template} has clickable logo")
            else:
                print(f"❌ {template} logo is not clickable")
                all_passed = False
        else:
            print(f"⚠️  {template} has no nav-brand, skipping...")
    
    return all_passed


def main():
    """Run all tests"""
    print("=" * 70)
    print("Navigation Menu Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_tradingview_renamed,
        test_tradingview_in_all_menus,
        test_logo_clickable,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test {test_func.__name__} failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    if all(results):
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
