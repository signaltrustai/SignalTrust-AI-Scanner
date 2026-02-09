#!/usr/bin/env python3
"""
ASI Collaboration Invitation Generator
=======================================
Generates secure collaboration invitations for the ASI multi-agent system.
Allows users to initiate collaboration sessions with one or more AI agents.

Created by Michael Gallant.
"""

import json
import os
import secrets
import uuid
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# ── Agent registry ────────────────────────────────────────────────────────

AGENTS: Dict[str, Dict[str, str]] = {
    "ASI1": {"id": "ASI1-STOCK-001", "name": "ASI1-Stock", "role": "Stock Analysis"},
    "ASI2": {"id": "ASI2-CRYPTO-002", "name": "ASI2-Crypto", "role": "Crypto Analysis"},
    "ASI3": {"id": "ASI3-WHALE-003", "name": "ASI3-Whale", "role": "Whale Monitoring"},
    "ASI4": {"id": "ASI4-SITE-004", "name": "ASI4-Site", "role": "Site Optimization"},
    "ASI5": {"id": "ASI5-SUPERVISOR-005", "name": "ASI5-Supervisor", "role": "Supervisor"},
    "ASI6": {"id": "ASI6-DESIRE-006", "name": "ASI6-Desire", "role": "Coordinator"},
}

ALL_AGENT_IDS: List[str] = [a["id"] for a in AGENTS.values()]

# ── Data model ────────────────────────────────────────────────────────────


@dataclass
class CollaborationInvitation:
    """A secure collaboration invitation linking a user to one or more ASI agents."""

    invitation_id: str
    from_agent: str
    from_agent_name: str
    to_user: str
    participants: List[str]
    collaboration_type: str
    permissions: List[str]
    token: str
    created_at: str
    expires_at: str
    status: str = "PENDING"

    def to_dict(self) -> dict:
        """Serialize to a plain dict (JSON-safe)."""
        return asdict(self)

    @property
    def is_expired(self) -> bool:
        """Check if this invitation has expired."""
        try:
            exp = datetime.fromisoformat(self.expires_at)
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > exp
        except (ValueError, TypeError):
            return True


# ── Generator ─────────────────────────────────────────────────────────────


class CollaborationGenerator:
    """Creates, stores, and retrieves ASI collaboration invitations."""

    VALID_PERMISSIONS = {"read", "write", "coordinate", "execute", "monitor"}

    def __init__(self, storage_dir: str = "data/collaborations"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self._invitations: Dict[str, CollaborationInvitation] = {}
        self._load_existing()

    # ── public API ────────────────────────────────────────────────────

    def create_invitation(
        self,
        from_agent: str,
        to_user: str,
        participants: List[str],
        collaboration_type: str = "full_collaboration",
        permissions: Optional[List[str]] = None,
        expiry_hours: int = 24,
    ) -> CollaborationInvitation:
        """Create a new collaboration invitation.

        Args:
            from_agent: Agent ID initiating the invitation.
            to_user: User identifier (email or user_id).
            participants: List of agent IDs included in the collaboration.
            collaboration_type: Label for the kind of collaboration.
            permissions: Granted permissions (defaults to read+execute).
            expiry_hours: Hours until the invitation expires (1-168).

        Returns:
            The newly created CollaborationInvitation.
        """
        if not to_user or not to_user.strip():
            raise ValueError("to_user is required")

        if not participants:
            raise ValueError("At least one participant agent is required")

        expiry_hours = max(1, min(168, expiry_hours))  # clamp 1h–7d

        if permissions is None:
            permissions = ["read", "execute"]
        permissions = [p for p in permissions if p in self.VALID_PERMISSIONS]
        if not permissions:
            permissions = ["read"]

        now = datetime.now(timezone.utc)
        invitation = CollaborationInvitation(
            invitation_id=self._make_id(),
            from_agent=from_agent,
            from_agent_name=AGENTS.get(from_agent, {}).get("name", from_agent),
            to_user=to_user,
            participants=participants,
            collaboration_type=collaboration_type,
            permissions=permissions,
            token=secrets.token_hex(32),
            created_at=now.isoformat(),
            expires_at=(now + timedelta(hours=expiry_hours)).isoformat(),
        )

        self._invitations[invitation.invitation_id] = invitation
        self._save(invitation)
        logger.info("Collaboration invitation %s created for %s", invitation.invitation_id, to_user)
        return invitation

    def get_invitation(self, invitation_id: str) -> Optional[CollaborationInvitation]:
        """Retrieve an invitation by ID."""
        return self._invitations.get(invitation_id)

    def accept_invitation(self, invitation_id: str, token: str) -> bool:
        """Accept an invitation if the token is valid and it hasn't expired.

        Args:
            invitation_id: The invitation to accept.
            token: The secure token that was issued.

        Returns:
            True if accepted, False otherwise.
        """
        inv = self._invitations.get(invitation_id)
        if inv is None:
            return False
        if not secrets.compare_digest(inv.token, token):
            return False
        if inv.is_expired:
            inv.status = "EXPIRED"
            self._save(inv)
            return False
        if inv.status != "PENDING":
            return False

        inv.status = "ACCEPTED"
        self._save(inv)
        logger.info("Invitation %s accepted", invitation_id)
        return True

    def list_invitations(self, user: Optional[str] = None, status: Optional[str] = None) -> List[dict]:
        """List invitations, optionally filtered by user and/or status.

        Args:
            user: Filter to invitations for this user.
            status: Filter by status (PENDING, ACCEPTED, EXPIRED).

        Returns:
            List of invitation dicts (token field excluded for security).
        """
        results = []
        for inv in self._invitations.values():
            if user and inv.to_user != user:
                continue
            if status and inv.status != status:
                continue
            d = inv.to_dict()
            d.pop("token", None)  # never expose token in list views
            results.append(d)
        return results

    def get_available_agents(self) -> List[dict]:
        """Return the list of agents available for collaboration."""
        return [
            {"key": key, **info}
            for key, info in AGENTS.items()
        ]

    # ── helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _make_id() -> str:
        return f"INV-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"

    def _save(self, invitation: CollaborationInvitation) -> None:
        path = os.path.join(self.storage_dir, f"{invitation.invitation_id}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(invitation.to_dict(), f, indent=2, ensure_ascii=False)
        except OSError as exc:
            logger.error("Failed to save invitation %s: %s", invitation.invitation_id, exc)

    def _load_existing(self) -> None:
        """Load previously saved invitations from disk."""
        if not os.path.isdir(self.storage_dir):
            return
        for fname in os.listdir(self.storage_dir):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(self.storage_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                inv = CollaborationInvitation(**data)
                self._invitations[inv.invitation_id] = inv
            except Exception as exc:
                logger.warning("Could not load %s: %s", fname, exc)


# ── convenience constructors ──────────────────────────────────────────────


def create_full_collaboration(user: str, expiry_hours: int = 72) -> CollaborationInvitation:
    """Create a collaboration invitation with all 6 agents.

    Args:
        user: User identifier.
        expiry_hours: Hours until expiry.

    Returns:
        CollaborationInvitation
    """
    gen = CollaborationGenerator()
    return gen.create_invitation(
        from_agent="ASI6",
        to_user=user,
        participants=ALL_AGENT_IDS,
        collaboration_type="full_market_analysis",
        permissions=["read", "write", "coordinate", "execute", "monitor"],
        expiry_hours=expiry_hours,
    )


def create_single_agent_collaboration(user: str, agent_key: str, expiry_hours: int = 24) -> CollaborationInvitation:
    """Create a collaboration invitation with a single agent.

    Args:
        user: User identifier.
        agent_key: Agent key (ASI1–ASI6).
        expiry_hours: Hours until expiry.

    Returns:
        CollaborationInvitation
    """
    agent = AGENTS.get(agent_key)
    if agent is None:
        raise ValueError(f"Unknown agent key: {agent_key}. Valid: {list(AGENTS.keys())}")

    gen = CollaborationGenerator()
    return gen.create_invitation(
        from_agent=agent_key,
        to_user=user,
        participants=[agent["id"]],
        collaboration_type="single_agent_collaboration",
        permissions=["read", "execute"],
        expiry_hours=expiry_hours,
    )
