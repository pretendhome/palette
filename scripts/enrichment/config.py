"""Centralized paths and thresholds for the enrichment pipeline."""
from __future__ import annotations

import os
from pathlib import Path

# ── Root paths ────────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
PALETTE_ROOT = _SCRIPT_DIR.parents[1]  # fde/palette/

# ── People library ────────────────────────────────────────────────────────────
PEOPLE_LIBRARY_PATH = (
    PALETTE_ROOT
    / "buy-vs-build"
    / "people-library"
    / "v1.1"
    / "people_library_v1.1.yaml"
)
CROSSREF_PATH = (
    PALETTE_ROOT
    / "buy-vs-build"
    / "people-library"
    / "v1.1"
    / "people_library_company_signals_v1.1.yaml"
)

# ── Enrichment outputs ───────────────────────────────────────────────────────
ENRICHMENT_LOG_PATH = _SCRIPT_DIR / "enrichment_log.jsonl"

# ── Validation ────────────────────────────────────────────────────────────────
VALIDATION_SCRIPT = PALETTE_ROOT / "scripts" / "validate_palette_state.py"

# ── Staleness ─────────────────────────────────────────────────────────────────
STALE_THRESHOLD_DAYS = 30

# ── GitHub API ────────────────────────────────────────────────────────────────
GITHUB_API_BASE = "https://api.github.com"
GITHUB_REPOS_LIMIT = 5
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"


def github_token() -> str | None:
    """Return the GitHub token from env, or None if unset."""
    return os.environ.get(GITHUB_TOKEN_ENV)
