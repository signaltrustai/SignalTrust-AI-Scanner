#!/usr/bin/env python3
"""
Test Flask App Initialization

This test ensures that there is only ONE Flask app initialization in app.py,
preventing the bug where duplicate app initialization overwrites all previously
defined routes.

Issue: Lines 1548-1552 previously had duplicate Flask app initialization that
caused only routes after that line to work, while all previous 64 routes
returned 404 errors.
"""

import re
import sys


def test_single_flask_app_initialization():
    """Verify there is only one Flask app initialization."""
    with open('app.py', 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Find all Flask app initializations
    flask_inits = []
    for i, line in enumerate(lines, 1):
        if re.search(r'app\s*=\s*Flask\(__name__\)', line):
            flask_inits.append((i, line.strip()))
    
    print(f"\n{'='*70}")
    print("Flask App Initialization Test")
    print(f"{'='*70}")
    print(f"Found {len(flask_inits)} Flask app initialization(s):")
    
    for line_num, line in flask_inits:
        print(f"  Line {line_num}: {line}")
    
    # There should be exactly ONE initialization
    if len(flask_inits) == 1:
        print(f"\n✅ PASS: Exactly one Flask app initialization found (line {flask_inits[0][0]})")
        return True
    elif len(flask_inits) == 0:
        print("\n❌ FAIL: No Flask app initialization found!")
        return False
    else:
        print(f"\n❌ FAIL: Multiple Flask app initializations found!")
        print("This will cause all routes before the second initialization to fail!")
        return False


def test_no_duplicate_flask_imports():
    """Verify Flask is imported only once at the top of the file."""
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    flask_imports = []
    for i, line in enumerate(lines, 1):
        if re.search(r'from\s+flask\s+import\s+Flask', line):
            flask_imports.append((i, line.strip()))
    
    print(f"\n{'='*70}")
    print("Flask Import Test")
    print(f"{'='*70}")
    print(f"Found {len(flask_imports)} Flask import(s):")
    
    for line_num, line in flask_imports:
        print(f"  Line {line_num}: {line}")
    
    # There should be exactly ONE import at the top
    if len(flask_imports) == 1:
        line_num = flask_imports[0][0]
        if line_num < 10:  # Should be in first 10 lines
            print(f"\n✅ PASS: Flask imported once at the beginning (line {line_num})")
            return True
        else:
            print(f"\n⚠️  WARNING: Flask imported at line {line_num} (expected in first 10 lines)")
            return True
    elif len(flask_imports) == 0:
        print("\n❌ FAIL: No Flask import found!")
        return False
    else:
        print(f"\n❌ FAIL: Multiple Flask imports found!")
        print("Flask should only be imported once at the top of the file.")
        return False


def test_route_count():
    """Count total number of routes defined."""
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find all route decorators
    routes = re.findall(r'@app\.route\(["\']([^"\']+)["\']', content)
    
    print(f"\n{'='*70}")
    print("Route Count Test")
    print(f"{'='*70}")
    print(f"Total routes defined: {len(routes)}")
    
    if len(routes) > 50:
        print(f"✅ PASS: Found {len(routes)} routes (healthy application)")
        print("\nSample routes:")
        for route in routes[:5]:
            print(f"  - {route}")
        print(f"  ... and {len(routes) - 5} more")
        return True
    elif len(routes) > 0:
        print(f"⚠️  WARNING: Only {len(routes)} routes found (expected more)")
        return True
    else:
        print("❌ FAIL: No routes found!")
        return False


def test_no_test_backup_route():
    """Verify the problematic test-backup route was removed."""
    with open('app.py', 'r') as f:
        content = f.read()
    
    print(f"\n{'='*70}")
    print("Test-Backup Route Check")
    print(f"{'='*70}")
    
    # Check for test-backup route
    if re.search(r'["\']/?test-backup["\']', content):
        print("❌ FAIL: Found 'test-backup' route - this should have been removed!")
        return False
    else:
        print("✅ PASS: No 'test-backup' route found (correctly removed)")
        return True


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("Flask App Structure Validation")
    print("Prevents regression of the duplicate Flask app initialization bug")
    print("="*70)
    
    tests = [
        ("Single Flask App Initialization", test_single_flask_app_initialization),
        ("No Duplicate Flask Imports", test_no_duplicate_flask_imports),
        ("Route Count", test_route_count),
        ("No Test-Backup Route", test_no_test_backup_route),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*70}")
    print("Test Summary")
    print(f"{'='*70}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Flask app structure is correct.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
