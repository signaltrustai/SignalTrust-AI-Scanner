#!/usr/bin/env python3
"""
Test Input Validation Helpers

Validates the _safe_int() and _valid_symbol() helper functions added to app.py
to prevent crashes from malformed request parameters.
"""

import sys
import os

# Ensure the project root is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import _safe_int, _valid_symbol


def test_safe_int_valid_values():
    """_safe_int returns the parsed integer when valid."""
    assert _safe_int("10", default=5) == 10
    assert _safe_int("1", default=5) == 1
    assert _safe_int("999", default=5) == 999
    print("  ✅ _safe_int: valid values parsed correctly")
    return True


def test_safe_int_default_on_bad_input():
    """_safe_int returns default for non-numeric or None input."""
    assert _safe_int("abc", default=50) == 50
    assert _safe_int("", default=50) == 50
    assert _safe_int(None, default=50) == 50
    assert _safe_int("12.5", default=50) == 50
    print("  ✅ _safe_int: bad input falls back to default")
    return True


def test_safe_int_clamping():
    """_safe_int clamps values within min/max bounds."""
    assert _safe_int("0", default=5, min_val=1, max_val=100) == 1
    assert _safe_int("-5", default=5, min_val=1, max_val=100) == 1
    assert _safe_int("999", default=5, min_val=1, max_val=100) == 100
    assert _safe_int("50", default=5, min_val=1, max_val=100) == 50
    print("  ✅ _safe_int: values clamped to bounds")
    return True


def test_valid_symbol_accepts_good_symbols():
    """_valid_symbol accepts valid ticker symbols."""
    assert _valid_symbol("BTC") is True
    assert _valid_symbol("AAPL") is True
    assert _valid_symbol("ETH") is True
    assert _valid_symbol("EUR/USD") is True
    assert _valid_symbol("BTC-USD") is True
    assert _valid_symbol("sol") is True
    print("  ✅ _valid_symbol: valid symbols accepted")
    return True


def test_valid_symbol_rejects_bad_symbols():
    """_valid_symbol rejects invalid or dangerous symbols."""
    assert _valid_symbol("") is False
    assert _valid_symbol(None) is False
    assert _valid_symbol("A" * 21) is False  # too long
    assert _valid_symbol("BTC;DROP TABLE") is False
    assert _valid_symbol("<script>") is False
    assert _valid_symbol("BTC & echo pwned") is False
    print("  ✅ _valid_symbol: invalid symbols rejected")
    return True


def run_all_tests():
    """Run all validation tests."""
    print(f"\n{'='*70}")
    print("Input Validation Helper Tests")
    print(f"{'='*70}")

    tests = [
        test_safe_int_valid_values,
        test_safe_int_default_on_bad_input,
        test_safe_int_clamping,
        test_valid_symbol_accepts_good_symbols,
        test_valid_symbol_rejects_bad_symbols,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  ❌ {test.__name__} returned False")
        except Exception as e:
            failed += 1
            print(f"  ❌ {test.__name__} raised {type(e).__name__}: {e}")

    print(f"\n{'='*70}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print(f"{'='*70}")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
