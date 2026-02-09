#!/usr/bin/env python3
"""
Test ASI Collaboration Module

Validates:
- Invitation creation, acceptance, expiry
- Token security (constant-time comparison)
- Input validation (missing user, empty participants)
- Listing and filtering
- Available agents registry
"""

import os
import sys
import shutil
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Use a temp directory for test storage
TEST_STORAGE = os.path.join(tempfile.gettempdir(), "test_collaborations")


def _fresh_generator():
    """Create a CollaborationGenerator with a clean test directory."""
    if os.path.isdir(TEST_STORAGE):
        shutil.rmtree(TEST_STORAGE)
    from asi_collaboration import CollaborationGenerator
    return CollaborationGenerator(storage_dir=TEST_STORAGE)


def test_create_invitation():
    """Creating an invitation returns a valid CollaborationInvitation."""
    gen = _fresh_generator()
    inv = gen.create_invitation(
        from_agent="ASI6",
        to_user="alice@example.com",
        participants=["ASI1-STOCK-001", "ASI2-CRYPTO-002"],
        collaboration_type="market_analysis",
    )
    assert inv.invitation_id.startswith("INV-")
    assert inv.to_user == "alice@example.com"
    assert inv.from_agent == "ASI6"
    assert inv.status == "PENDING"
    assert len(inv.token) == 64  # 32 bytes hex
    assert len(inv.participants) == 2
    print("  ✅ create_invitation: returns valid invitation")
    return True


def test_accept_invitation():
    """Accepting with correct token changes status to ACCEPTED."""
    gen = _fresh_generator()
    inv = gen.create_invitation(
        from_agent="ASI1",
        to_user="bob@example.com",
        participants=["ASI1-STOCK-001"],
    )
    assert gen.accept_invitation(inv.invitation_id, inv.token) is True
    assert inv.status == "ACCEPTED"
    print("  ✅ accept_invitation: correct token -> ACCEPTED")
    return True


def test_reject_wrong_token():
    """Accepting with wrong token is rejected."""
    gen = _fresh_generator()
    inv = gen.create_invitation(
        from_agent="ASI2",
        to_user="carol@example.com",
        participants=["ASI2-CRYPTO-002"],
    )
    assert gen.accept_invitation(inv.invitation_id, "wrong_token") is False
    assert inv.status == "PENDING"  # unchanged
    print("  ✅ accept_invitation: wrong token -> rejected")
    return True


def test_expired_invitation():
    """An expired invitation cannot be accepted."""
    gen = _fresh_generator()
    inv = gen.create_invitation(
        from_agent="ASI3",
        to_user="dave@example.com",
        participants=["ASI3-WHALE-003"],
        expiry_hours=1,
    )
    # Manually expire it
    from datetime import datetime, timezone, timedelta
    inv.expires_at = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

    assert gen.accept_invitation(inv.invitation_id, inv.token) is False
    assert inv.status == "EXPIRED"
    print("  ✅ expired invitation: cannot be accepted")
    return True


def test_list_invitations_filtering():
    """list_invitations filters by user and status."""
    gen = _fresh_generator()
    gen.create_invitation("ASI1", "user_a@example.com", ["ASI1-STOCK-001"])
    gen.create_invitation("ASI2", "user_b@example.com", ["ASI2-CRYPTO-002"])
    inv3 = gen.create_invitation("ASI3", "user_a@example.com", ["ASI3-WHALE-003"])
    gen.accept_invitation(inv3.invitation_id, inv3.token)

    all_inv = gen.list_invitations()
    assert len(all_inv) == 3

    user_a = gen.list_invitations(user="user_a@example.com")
    assert len(user_a) == 2

    accepted = gen.list_invitations(status="ACCEPTED")
    assert len(accepted) == 1

    # Verify tokens are NOT exposed in list output
    for inv_dict in all_inv:
        assert "token" not in inv_dict

    print("  ✅ list_invitations: filters by user/status, hides tokens")
    return True


def test_validation_rejects_bad_input():
    """create_invitation rejects empty user and empty participants."""
    gen = _fresh_generator()

    try:
        gen.create_invitation("ASI1", "", ["ASI1-STOCK-001"])
        print("  ❌ Should have raised ValueError for empty user")
        return False
    except ValueError:
        pass

    try:
        gen.create_invitation("ASI1", "user@example.com", [])
        print("  ❌ Should have raised ValueError for empty participants")
        return False
    except ValueError:
        pass

    print("  ✅ validation: rejects empty user and empty participants")
    return True


def test_get_available_agents():
    """get_available_agents returns all 6 agents."""
    gen = _fresh_generator()
    agents = gen.get_available_agents()
    assert len(agents) == 6
    keys = [a["key"] for a in agents]
    assert "ASI1" in keys and "ASI6" in keys
    print("  ✅ get_available_agents: returns all 6 agents")
    return True


def test_permissions_sanitized():
    """Invalid permissions are stripped; at least 'read' is kept."""
    gen = _fresh_generator()
    inv = gen.create_invitation(
        from_agent="ASI1",
        to_user="eve@example.com",
        participants=["ASI1-STOCK-001"],
        permissions=["delete", "admin", "hack"],  # all invalid
    )
    assert inv.permissions == ["read"]  # fallback to read
    print("  ✅ permissions: invalid perms stripped, fallback to ['read']")
    return True


def run_all_tests():
    """Run all collaboration tests."""
    print(f"\n{'='*70}")
    print("ASI Collaboration Module Tests")
    print(f"{'='*70}")

    tests = [
        test_create_invitation,
        test_accept_invitation,
        test_reject_wrong_token,
        test_expired_invitation,
        test_list_invitations_filtering,
        test_validation_rejects_bad_input,
        test_get_available_agents,
        test_permissions_sanitized,
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

    # Cleanup
    if os.path.isdir(TEST_STORAGE):
        shutil.rmtree(TEST_STORAGE)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
