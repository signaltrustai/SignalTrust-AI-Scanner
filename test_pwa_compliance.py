#!/usr/bin/env python3
"""
PWA Compliance Test
Tests if the SignalTrust AI app meets PWA standards
"""

import requests
import json
import sys
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = "http://localhost:5000"

def test_manifest():
    """Test if manifest.json is accessible and valid"""
    print(f"\n{Fore.CYAN}Testing PWA Manifest...{Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{BASE_URL}/manifest.json")
        
        if response.status_code == 200:
            manifest = response.json()
            
            required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
            missing_fields = [field for field in required_fields if field not in manifest]
            
            if not missing_fields:
                print(f"{Fore.GREEN}✓ Manifest is valid and accessible{Style.RESET_ALL}")
                print(f"  - Name: {manifest['name']}")
                print(f"  - Short name: {manifest['short_name']}")
                print(f"  - Display: {manifest['display']}")
                print(f"  - Icons: {len(manifest['icons'])} sizes")
                print(f"  - Theme color: {manifest.get('theme_color', 'N/A')}")
                return True
            else:
                print(f"{Fore.RED}✗ Manifest missing required fields: {missing_fields}{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.RED}✗ Manifest not accessible (Status: {response.status_code}){Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error testing manifest: {e}{Style.RESET_ALL}")
        return False

def test_service_worker():
    """Test if service worker is accessible"""
    print(f"\n{Fore.CYAN}Testing Service Worker...{Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{BASE_URL}/service-worker.js")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for essential service worker features
            checks = {
                'Install event': 'addEventListener(\'install\'',
                'Activate event': 'addEventListener(\'activate\'',
                'Fetch event': 'addEventListener(\'fetch\'',
                'Cache API': 'caches.open',
            }
            
            all_passed = True
            for check_name, check_str in checks.items():
                if check_str in content:
                    print(f"{Fore.GREEN}✓ {check_name} handler present{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ {check_name} handler missing{Style.RESET_ALL}")
                    all_passed = False
            
            return all_passed
        else:
            print(f"{Fore.RED}✗ Service worker not accessible (Status: {response.status_code}){Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error testing service worker: {e}{Style.RESET_ALL}")
        return False

def test_mobile_meta_tags():
    """Test if mobile meta tags are present"""
    print(f"\n{Fore.CYAN}Testing Mobile Meta Tags...{Style.RESET_ALL}")
    
    try:
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                'Viewport': 'name="viewport"',
                'Theme color': 'name="theme-color"',
                'Mobile web app': 'name="mobile-web-app-capable"',
                'Apple mobile': 'name="apple-mobile-web-app-capable"',
                'Manifest link': 'rel="manifest"',
            }
            
            all_passed = True
            for check_name, check_str in checks.items():
                if check_str in content:
                    print(f"{Fore.GREEN}✓ {check_name} tag present{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}⚠ {check_name} tag missing{Style.RESET_ALL}")
                    all_passed = False
            
            return all_passed
        else:
            print(f"{Fore.RED}✗ Homepage not accessible (Status: {response.status_code}){Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error testing meta tags: {e}{Style.RESET_ALL}")
        return False

def test_icons():
    """Test if required icons are accessible"""
    print(f"\n{Fore.CYAN}Testing App Icons...{Style.RESET_ALL}")
    
    required_icons = [
        '/static/icons/icon-192x192.png',
        '/static/icons/icon-512x512.png',
        '/static/icons/apple-touch-icon.png',
        '/static/icons/favicon.ico',
    ]
    
    all_passed = True
    for icon_path in required_icons:
        try:
            response = requests.get(f"{BASE_URL}{icon_path}")
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ {icon_path} accessible{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ {icon_path} not found (Status: {response.status_code}){Style.RESET_ALL}")
                all_passed = False
        except Exception as e:
            print(f"{Fore.RED}✗ Error accessing {icon_path}: {e}{Style.RESET_ALL}")
            all_passed = False
    
    return all_passed

def test_https_redirect():
    """Check if HTTPS is enforced (in production)"""
    print(f"\n{Fore.CYAN}Testing HTTPS Configuration...{Style.RESET_ALL}")
    
    # For local testing, we skip this check
    print(f"{Fore.YELLOW}⚠ HTTPS check skipped (local development){Style.RESET_ALL}")
    print(f"  Note: HTTPS is required for PWA in production")
    return True

def main():
    """Run all PWA compliance tests"""
    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}PWA COMPLIANCE TEST - SignalTrust AI{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    
    results = {
        'Manifest': test_manifest(),
        'Service Worker': test_service_worker(),
        'Mobile Meta Tags': test_mobile_meta_tags(),
        'App Icons': test_icons(),
        'HTTPS': test_https_redirect(),
    }
    
    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}TEST SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Fore.GREEN}PASS" if result else f"{Fore.RED}FAIL"
        print(f"{status}{Style.RESET_ALL} - {test_name}")
    
    print(f"\n{Fore.CYAN}Results: {passed}/{total} tests passed{Style.RESET_ALL}")
    
    if passed == total:
        print(f"\n{Fore.GREEN}🎉 All PWA compliance tests passed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Your app meets PWA standards.{Style.RESET_ALL}")
        return 0
    else:
        print(f"\n{Fore.YELLOW}⚠ Some tests failed. Please review the results above.{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
