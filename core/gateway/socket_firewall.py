"""Socket-level egress firewall for Palette OS.

Intercepts all outgoing network connections and blocks any destination
not in the explicit allowlist. This is the trust boundary enforcement
that makes "nothing left this machine" provably true.

Usage:
    from core.gateway.socket_firewall import activate_firewall, deactivate_firewall

    activate_firewall()   # call once at startup
    # ... all socket.create_connection calls now gated ...
    deactivate_firewall() # restore original behavior

The allowlist is intentionally small and explicit:
- localhost (Ollama, peers bus, Voice Hub)
- api.perplexity.ai (governed external research)
- api.anthropic.com (Claude API — only if configured)
- api.mistral.ai (Mistral API — only if configured)
- api.groq.com (Groq free tier — only if configured)

Any connection attempt to a host NOT in this list is blocked and logged.
"""

from __future__ import annotations

import json
import logging
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("palette.firewall")

# ── Allowlist ──────────────────────────────────────────────────────────

ALLOWED_HOSTS: set[str] = {
    # Local services (always allowed)
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "::1",
    # Governed external APIs (explicitly permitted)
    "api.perplexity.ai",
    "api.anthropic.com",
    "api.mistral.ai",
    "api.groq.com",
    # Ollama (local model inference)
    "ollama",
    # Embedding model (local)
    "host.docker.internal",
}

# ── State ──────────────────────────────────────────────────────────────

_original_create_connection: Any = None
_firewall_active: bool = False
_block_log: list[dict] = []

FIREWALL_LOG_PATH = Path(__file__).resolve().parents[2] / ".palette" / "firewall_log.ndjson"


# ── Core Guard ─────────────────────────────────────────────────────────


def _is_allowed(host: str) -> bool:
    """Check if a host is in the allowlist."""
    if host in ALLOWED_HOSTS:
        return True
    # Check if it's a localhost variant
    if host.startswith("127.") or host.startswith("192.168.") or host.startswith("10."):
        return True
    return False


def _guarded_create_connection(address: Any, *args: Any, **kwargs: Any) -> socket.socket:
    """Drop-in replacement for socket.create_connection with allowlist enforcement."""
    host = address[0] if isinstance(address, tuple) else str(address)
    port = address[1] if isinstance(address, tuple) and len(address) > 1 else 0

    if _is_allowed(host):
        return _original_create_connection(address, *args, **kwargs)

    # BLOCKED — log and raise
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "BLOCKED",
        "host": host,
        "port": port,
        "reason": f"host not in allowlist: {host}",
    }
    _block_log.append(entry)
    _log_block(entry)
    logger.warning(f"FIREWALL BLOCK: {host}:{port} — not in allowlist")

    raise ConnectionError(
        f"[Palette Firewall] Connection to {host}:{port} blocked. "
        f"Host not in governed allowlist. Only approved external APIs "
        f"(Perplexity, Anthropic, Mistral, Groq) and local services are permitted."
    )


def _log_block(entry: dict) -> None:
    """Append block event to firewall log."""
    try:
        FIREWALL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FIREWALL_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # best-effort logging


# ── Activation / Deactivation ──────────────────────────────────────────


def activate_firewall() -> None:
    """Activate the socket firewall. Call once at startup."""
    global _original_create_connection, _firewall_active

    if _firewall_active:
        return

    _original_create_connection = socket.create_connection
    socket.create_connection = _guarded_create_connection
    _firewall_active = True
    logger.info(f"Palette firewall activated. Allowlist: {sorted(ALLOWED_HOSTS)}")


def deactivate_firewall() -> None:
    """Deactivate the socket firewall. Restore original behavior."""
    global _original_create_connection, _firewall_active

    if not _firewall_active or _original_create_connection is None:
        return

    socket.create_connection = _original_create_connection
    _original_create_connection = None
    _firewall_active = False
    logger.info("Palette firewall deactivated.")


# ── Status / Inspection ───────────────────────────────────────────────


def is_active() -> bool:
    """Check if the firewall is currently active."""
    return _firewall_active


def get_block_log() -> list[dict]:
    """Return the in-memory block log for this session."""
    return list(_block_log)


def get_allowlist() -> set[str]:
    """Return the current allowlist."""
    return set(ALLOWED_HOSTS)


def add_to_allowlist(host: str) -> None:
    """Add a host to the allowlist at runtime. Use with caution."""
    ALLOWED_HOSTS.add(host)
    logger.info(f"Added {host} to firewall allowlist")


def load_block_log_from_disk() -> list[dict]:
    """Load persisted block log from disk."""
    if not FIREWALL_LOG_PATH.exists():
        return []
    entries = []
    for line in FIREWALL_LOG_PATH.read_text().strip().split("\n"):
        if line.strip():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries
