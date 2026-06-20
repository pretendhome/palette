#!/usr/bin/env python3
"""Regression tests for palette intents.

Run: python3 scripts/palette_intents/test_intents.py
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PALETTE = [sys.executable, str(REPO_ROOT / "scripts" / "palette_intent.py")]

passed = 0
failed = 0


def run(args: list[str]) -> dict:
    result = subprocess.run(
        PALETTE + args,
        capture_output=True, text=True, timeout=120,
        cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        raise RuntimeError(f"Exit {result.returncode}: {result.stderr}")
    return json.loads(result.stdout)


def test(name: str, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print(f"  ✅ {name}")
    except Exception as e:
        failed += 1
        print(f"  ❌ {name}: {e}")


# ── PROTECT ─────────────────────────────────────────────────────────────

def test_protect_blocks_strategy():
    d = run(["protect", "--json", "Our client's strategy"])
    assert d["action"] == "BLOCK"
    assert d["artifact_type"] == "GateDecision"
    assert len(d["blocked_entities"]) > 0

def test_protect_allows_public():
    d = run(["protect", "--json", "What are Delaware fiduciary duty precedents?"])
    assert d["action"] == "ALLOW"
    assert d["boundary"] == "governed_external"

def test_protect_blocks_empty():
    d = run(["protect", "--json", ""])
    assert d["action"] == "BLOCK"

def test_protect_blocks_pii():
    d = run(["protect", "--json", "Contact john@acme.com about the case"])
    assert d["action"] == "BLOCK"
    assert "john@acme.com" in d["blocked_entities"]

def test_protect_matter_id():
    d = run(["protect", "--json", "--matter", "test-001", "Our exposure"])
    assert d["matter_id"] == "test-001"

# ── RESEARCH ────────────────────────────────────────────────────────────

def test_research_local():
    d = run(["research", "--json", "--local-only", "Delaware fiduciary duty"])
    assert d["artifact_type"] == "EvidenceBrief"
    assert len(d["local_canon"]) > 0
    assert d["status"] == "LOCAL_ONLY"

def test_research_blocks_privileged():
    d = run(["research", "--json", "Should we settle this case?"])
    assert d["boundary"] == "local_only"

def test_research_schema():
    d = run(["research", "--json", "--local-only", "oversight duties"])
    required = ["artifact_type", "intent", "timestamp", "local_canon", "external_delta", "confidence", "status"]
    for r in required:
        assert r in d, f"Missing field: {r}"

# ── REFLECT ─────────────────────────────────────────────────────────────

def test_reflect_basic():
    d = run(["reflect", "--json", "What did we learn?"])
    assert d["artifact_type"] == "ImprovementProposal"
    assert d["status"] == "PROPOSED"

def test_reflect_empty_matter():
    import uuid
    unique_matter = f"test-{uuid.uuid4().hex[:8]}"
    d = run(["reflect", "--json", "--matter", unique_matter, "What happened?"])
    assert d["session_summary"]["total_artifacts"] == 0

def test_reflect_write_lock():
    d = run(["reflect", "--json", "What should change?"])
    for p in d.get("proposed_actions", []):
        assert p["target_file"].startswith("wiki/proposed/"), f"Write-lock violation: {p['target_file']}"

# ── Run all ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  palette intents — regression tests\n")

    tests = [
        ("PROTECT blocks strategy language", test_protect_blocks_strategy),
        ("PROTECT allows public research", test_protect_allows_public),
        ("PROTECT blocks empty query", test_protect_blocks_empty),
        ("PROTECT blocks PII", test_protect_blocks_pii),
        ("PROTECT carries matter_id", test_protect_matter_id),
        ("RESEARCH local-only returns EvidenceBrief", test_research_local),
        ("RESEARCH blocks privileged queries", test_research_blocks_privileged),
        ("RESEARCH schema complete", test_research_schema),
        ("REFLECT produces ImprovementProposal", test_reflect_basic),
        ("REFLECT handles empty matter", test_reflect_empty_matter),
        ("REFLECT write-lock membrane intact", test_reflect_write_lock),
    ]

    for name, fn in tests:
        test(name, fn)

    print(f"\n  {'─' * 40}")
    print(f"  {passed}/{passed + failed} passed", end="")
    if failed:
        print(f" ({failed} FAILED)")
        sys.exit(1)
    else:
        print(" ✅")
        sys.exit(0)
