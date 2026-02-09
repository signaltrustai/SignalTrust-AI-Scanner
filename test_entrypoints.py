#!/usr/bin/env python3
"""
Tests for application entrypoints.

Ensures the optimized runner uses expected settings and that the
SignalTrustAPP duplicate entrypoint is available for the mobile app.
"""

import sys
from unittest import mock


def test_web_main_uses_optimized_runner():
    """Verify main uses the optimized runner settings for the web platform."""
    # Pretend interactive shell to skip auto-start side effects
    sys.ps1 = "test> "
    with mock.patch("app.app") as fake_app, mock.patch("app.background_worker") as worker:
        fake_app.run.return_value = None
        import app

        app.main()

        fake_app.run.assert_called_once_with(
            host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True
        )
        worker.stop.assert_called_once()


def test_signaltrustapp_duplicate_entrypoint():
    """Ensure SignalTrustAPP entrypoint exists and reuses optimized runner."""
    sys.ps1 = "test> "
    with mock.patch("app.app") as fake_app, mock.patch("app.background_worker") as worker:
        fake_app.run.return_value = None
        import app

        app.SignalTrustAPP()

        fake_app.run.assert_called_once()
        called_kwargs = fake_app.run.call_args.kwargs
        assert called_kwargs["threaded"] is True
        assert called_kwargs["use_reloader"] is False
        worker.stop.assert_called_once()


def main():
    """Execute tests when run directly."""
    tests = [
        test_web_main_uses_optimized_runner,
        test_signaltrustapp_duplicate_entrypoint,
    ]

    results = []
    for test_func in tests:
        try:
            test_func()
            results.append(True)
            print(f"✅ {test_func.__name__} passed")
        except Exception as exc:  # pragma: no cover - manual runner
            results.append(False)
            print(f"❌ {test_func.__name__} failed: {exc}")

    if all(results):
        print("✅ ALL ENTRYPOINT TESTS PASSED")
        return 0

    print("❌ ENTRYPOINT TESTS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
