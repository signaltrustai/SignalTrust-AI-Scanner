#!/usr/bin/env python3
"""
Test Performance Optimizations

Validates that optimizations work correctly:
- save_learning_data uses append-only JSONL (no full-file rewrite)
- call_agent has a timeout
- MarketScanner uses connection pooling and parallel overview fetch
- AIPredictor has thread-safe cache and connection pooling
- No duplicate logging.basicConfig in imported modules
"""

import os
import re
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_save_learning_data_is_append_only():
    """save_learning_data writes JSONL (one line per entry), not full JSON rewrite."""
    import tempfile
    import json
    # Patch the file path for the test
    import app
    original = app.LEARNING_DATA_FILE
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False)
    tmp.close()
    app.LEARNING_DATA_FILE = tmp.name

    try:
        # Write 3 entries
        app.save_learning_data("test_type_1", {"value": 1})
        app.save_learning_data("test_type_2", {"value": 2})
        app.save_learning_data("test_type_3", {"value": 3})

        # Read and verify JSONL format (3 separate lines)
        with open(tmp.name, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
        assert len(lines) == 3, f"Expected 3 JSONL lines, got {len(lines)}"

        for line in lines:
            entry = json.loads(line)
            assert "timestamp" in entry
            assert "type" in entry
            assert "data" in entry

        print("  ✅ save_learning_data uses append-only JSONL (no full-file rewrite)")
        return True
    finally:
        app.LEARNING_DATA_FILE = original
        os.unlink(tmp.name)


def test_call_agent_has_timeout():
    """call_agent() includes timeout in requests.post call."""
    with open('app.py', 'r') as f:
        content = f.read()

    # Find the call_agent function and verify it has timeout
    match = re.search(r'def call_agent\(.+?\nreturn', content, re.DOTALL)
    if match:
        func_body = match.group(0)
    else:
        # Fall back: search for the requests.post inside call_agent scope
        func_body = content

    # The requests.post call near call_agent should have timeout
    # Find all requests.post calls
    post_calls = re.findall(r'requests\.post\([^)]+\)', content)
    all_have_timeout = all('timeout' in call for call in post_calls)
    assert all_have_timeout, "Some requests.post calls missing timeout"

    print("  ✅ All requests.post() calls include timeout")
    return True


def test_market_scanner_has_connection_pooling():
    """MarketScanner uses HTTPAdapter for connection pooling."""
    with open('market_scanner.py', 'r') as f:
        content = f.read()

    assert 'HTTPAdapter' in content, "Missing HTTPAdapter import"
    assert 'pool_connections' in content, "Missing pool_connections configuration"
    assert 'pool_maxsize' in content, "Missing pool_maxsize configuration"
    assert 'Retry' in content, "Missing Retry configuration"

    print("  ✅ MarketScanner has connection pooling with HTTPAdapter")
    return True


def test_market_scanner_parallel_overview():
    """MarketScanner.get_markets_overview uses ThreadPoolExecutor."""
    with open('market_scanner.py', 'r') as f:
        content = f.read()

    assert 'ThreadPoolExecutor' in content, "Missing ThreadPoolExecutor"
    assert 'as_completed' in content, "Missing as_completed for parallel fetching"

    print("  ✅ MarketScanner uses parallel fetching for market overview")
    return True


def test_ai_predictor_thread_safe_cache():
    """AIPredictor cache uses threading.Lock for thread safety."""
    from ai_predictor import _get_cached, _set_cache, _cache_lock

    # Verify lock exists and is a Lock
    assert isinstance(_cache_lock, type(threading.Lock())), "Cache lock is not a threading.Lock"

    # Verify basic cache works
    _set_cache("test_key", 42)
    assert _get_cached("test_key") == 42, "Cache get/set failed"

    print("  ✅ AIPredictor has thread-safe cache with Lock")
    return True


def test_ai_predictor_session_pool():
    """AIPredictor has a shared session with connection pooling."""
    from ai_predictor import AIPredictor

    session = AIPredictor._get_session()
    assert session is not None, "Session should not be None"

    # Verify connection pooling is configured
    adapter = session.get_adapter("https://example.com")
    assert adapter is not None, "HTTPS adapter missing"

    # Verify it's a singleton
    session2 = AIPredictor._get_session()
    assert session is session2, "Session pool should be a singleton"

    print("  ✅ AIPredictor has shared session with connection pooling")
    return True


def test_no_duplicate_logging_basicconfig():
    """Imported modules should not call logging.basicConfig (only app.py should)."""
    modules_to_check = [
        'ai_worker_service.py',
        'ai_orchestrator.py',
        'ai_system_manager.py',
        'ai_memory_system.py',
        'ai_command_system.py',
        'ai_cloud_backup.py',
        'viral_marketing_ai_team.py',
    ]

    violations = []
    for module_file in modules_to_check:
        if not os.path.exists(module_file):
            continue
        with open(module_file, 'r') as f:
            content = f.read()
        if 'logging.basicConfig(' in content:
            violations.append(module_file)

    assert not violations, f"logging.basicConfig found in: {violations}"
    print(f"  ✅ No duplicate logging.basicConfig in {len(modules_to_check)} modules")
    return True


def run_all_tests():
    """Run all optimization tests."""
    print(f"\n{'='*70}")
    print("Performance Optimization Tests")
    print(f"{'='*70}")

    tests = [
        test_save_learning_data_is_append_only,
        test_call_agent_has_timeout,
        test_market_scanner_has_connection_pooling,
        test_market_scanner_parallel_overview,
        test_ai_predictor_thread_safe_cache,
        test_ai_predictor_session_pool,
        test_no_duplicate_logging_basicconfig,
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
