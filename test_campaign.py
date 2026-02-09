#!/usr/bin/env python3
"""
Test Viral Campaign & System Health endpoints.

Validates:
- Campaign launch, status, content generation, calendar, report
- System health check across all AI components
- Input validation (bad platform, bounds on duration/days)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _get_client():
    """Create a Flask test client."""
    os.environ.setdefault("TESTING", "1")
    from app import app
    app.config["TESTING"] = True
    return app.test_client()


def test_system_health():
    """GET /api/system/health returns component statuses."""
    client = _get_client()
    resp = client.get("/api/system/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["status"] in ("healthy", "degraded")
    assert data["components_ok"] >= data["components_total"] * 0.5
    assert "components" in data
    assert "viral_campaign" in data["components"]
    assert "market_scanner" in data["components"]
    print("  ✅ system health: returns component statuses")
    return True


def test_campaign_launch():
    """POST /api/campaign/launch creates a campaign."""
    client = _get_client()
    resp = client.post("/api/campaign/launch", json={"duration_days": 7})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True
    assert data["campaign"]["status"] == "launched"
    assert "platforms" in data["campaign"]
    print("  ✅ campaign launch: creates campaign successfully")
    return True


def test_campaign_status():
    """GET /api/campaign/status returns campaign info after launch."""
    client = _get_client()
    # Launch first
    client.post("/api/campaign/launch", json={"duration_days": 7})
    resp = client.get("/api/campaign/status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert "data" in data
    print("  ✅ campaign status: returns info after launch")
    return True


def test_campaign_generate_content():
    """POST /api/campaign/generate creates content for a platform."""
    client = _get_client()
    resp = client.post("/api/campaign/generate", json={
        "platform": "twitter",
        "topic": "new_feature",
        "style": "engaging",
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["post"]["platform"] == "twitter"
    print("  ✅ campaign generate: creates twitter content")
    return True


def test_campaign_generate_bad_platform():
    """POST /api/campaign/generate rejects invalid platform."""
    client = _get_client()
    resp = client.post("/api/campaign/generate", json={"platform": "myspace"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False
    assert "Invalid platform" in data["error"]
    print("  ✅ campaign generate: rejects invalid platform")
    return True


def test_campaign_calendar():
    """POST /api/campaign/calendar returns a content plan."""
    client = _get_client()
    resp = client.post("/api/campaign/calendar", json={"days": 3})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert data["days"] == 3
    assert data["total_posts"] > 0
    print("  ✅ campaign calendar: returns content plan")
    return True


def test_campaign_report():
    """GET /api/campaign/report returns a performance report."""
    client = _get_client()
    resp = client.get("/api/campaign/report")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert "report" in data
    print("  ✅ campaign report: returns performance report")
    return True


def test_campaign_duration_clamped():
    """Campaign duration is clamped to 1-90 days."""
    client = _get_client()
    # Negative → defaults to 30
    resp = client.post("/api/campaign/launch", json={"duration_days": -5})
    assert resp.status_code == 201
    # Huge → capped at 90
    resp2 = client.post("/api/campaign/launch", json={"duration_days": 999})
    assert resp2.status_code == 201
    print("  ✅ campaign launch: duration clamped to 1-90")
    return True


def run_all_tests():
    """Run all campaign tests."""
    print(f"\n{'='*70}")
    print("Viral Campaign & System Health Tests")
    print(f"{'='*70}")

    tests = [
        test_system_health,
        test_campaign_launch,
        test_campaign_status,
        test_campaign_generate_content,
        test_campaign_generate_bad_platform,
        test_campaign_calendar,
        test_campaign_report,
        test_campaign_duration_clamped,
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
