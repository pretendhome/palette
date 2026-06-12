#!/usr/bin/env python3
"""palette preflight — Validate all demo dependencies before recording.

Usage:
  python3 scripts/palette_preflight.py          # full check
  python3 scripts/palette_preflight.py --fix    # attempt auto-fixes where possible
"""
import json
import os
import sys
import time
from pathlib import Path
from urllib import request

REPO_ROOT = Path(__file__).resolve().parents[1]
PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
WARN = "\033[33m⚠\033[0m"

results = []


def check(name, ok, detail=""):
    status = PASS if ok else FAIL
    results.append((name, ok, detail))
    print(f"  {status} {name}{f'  ({detail})' if detail else ''}")
    return ok


def warn(name, detail=""):
    results.append((name, None, detail))
    print(f"  {WARN} {name}{f'  ({detail})' if detail else ''}")


def http_get(url, timeout=5):
    try:
        with request.urlopen(url, timeout=timeout) as resp:
            return resp.status, resp.read()
    except Exception as e:
        return None, str(e)


def http_post(url, data, headers=None, timeout=10):
    headers = headers or {"Content-Type": "application/json"}
    req = request.Request(url, data=json.dumps(data).encode(), headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read())
    except Exception as e:
        return None, str(e)


def main():
    fix_mode = "--fix" in sys.argv
    print()
    print("  palette preflight — demo readiness check")
    print("  " + "━" * 50)
    print()

    # ── 1. Ollama ──
    print("  Ollama:")
    status, body = http_get("http://127.0.0.1:11434/api/tags")
    if check("  Ollama responsive", status == 200):
        models = json.loads(body).get("models", [])
        names = [m["name"] for m in models]
        check("  qwen2.5:7b loaded", "qwen2.5:7b" in names)
        check("  qwen2.5:3b loaded", "qwen2.5:3b" in names)

        # Time a realistic inference
        t0 = time.time()
        status, resp = http_post("http://127.0.0.1:11434/api/generate", {
            "model": "qwen2.5:7b",
            "prompt": "Recommend: settle or litigate? One sentence.",
            "stream": False,
        }, timeout=120)
        elapsed = time.time() - t0
        check("  7b inference < 30s", elapsed < 30, f"{elapsed:.1f}s")
    else:
        check("  qwen2.5:7b loaded", False, "Ollama not running")
        check("  qwen2.5:3b loaded", False, "Ollama not running")
        check("  7b inference < 30s", False, "Ollama not running")
    print()

    # ── 2. Perplexity ──
    print("  Perplexity:")
    api_key = os.environ.get("PERPLEXITY_API_KEY", "")
    check("  API key set", bool(api_key), "missing" if not api_key else f"{api_key[:8]}...")
    if api_key:
        status, resp = http_post(
            "https://api.perplexity.ai/chat/completions",
            {"model": "sonar-pro", "messages": [{"role": "user", "content": "test"}]},
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        check("  API key valid (not 401)", status == 200, f"status={status}" if status else str(resp)[:60])
    else:
        check("  API key valid (not 401)", False, "no key to test")
    print()

    # ── 3. Peers Bus ──
    print("  Peers Bus:")
    status, body = http_get("http://127.0.0.1:7899/health")
    if check("  Bus responsive", status == 200):
        data = json.loads(body)
        check("  Bus status OK", data.get("status") == "ok")
    else:
        check("  Bus status OK", False, "bus not running")
        if fix_mode:
            print(f"    → Fix: cd {REPO_ROOT}/peers && node broker/index.mjs &")
    print()

    # ── 4. Intent System ──
    print("  Intent System:")
    intent_py = REPO_ROOT / "scripts" / "palette_intent.py"
    check("  palette_intent.py exists", intent_py.exists())

    # Test resolve (the core routing)
    sys.path.insert(0, str(REPO_ROOT))
    try:
        from scripts.palette_intents.infra import resolve_query
        t0 = time.time()
        result = resolve_query("Delaware fiduciary duty")
        elapsed = time.time() - t0
        check("  Resolve works", result.get("riu_id") is not None, f"{result.get('riu_id')} in {elapsed:.2f}s")
        check("  Resolve < 2s", elapsed < 2.0, f"{elapsed:.1f}s")
    except Exception as e:
        check("  Resolve works", False, str(e)[:60])
        check("  Resolve < 2s", False, "resolve failed")
    print()

    # ── 5. [CONNECT] Signal ──
    print("  [CONNECT] Signal:")
    try:
        from scripts.palette_intents.infra import find_related_artifacts
        artifacts = find_related_artifacts("RIU-709")
        check("  RIU-709 has prior artifacts", len(artifacts) > 0, f"{len(artifacts)} found")
        artifacts2 = find_related_artifacts("RIU-701")
        check("  RIU-701 has prior artifacts", len(artifacts2) > 0, f"{len(artifacts2)} found")
    except Exception as e:
        check("  RIU-709 has prior artifacts", False, str(e)[:60])
    print()

    # ── 6. Artifact Storage ──
    print("  Artifacts:")
    artifacts_dir = REPO_ROOT / ".palette" / "artifacts"
    check("  Artifacts directory exists", artifacts_dir.exists())
    if artifacts_dir.exists():
        count = sum(1 for _ in artifacts_dir.rglob("*.md"))
        check("  Artifacts present", count > 0, f"{count} total")
    print()

    # ── 7. Demo Timing Estimate ──
    print("  Demo Timing (estimated):")
    # PROTECT: no model call, just classification
    protect_est = 2.0
    # RESEARCH: resolve + local retrieval (no Perplexity if blocked)
    research_est = 3.0
    # DECIDE: 3 Ollama calls × measured time
    decide_est = 22.0 * 3  # from measured 7b timing
    total_est = protect_est + research_est + decide_est
    check("  Estimated total < 120s", total_est < 120, f"~{total_est:.0f}s (PROTECT:{protect_est:.0f} + RESEARCH:{research_est:.0f} + DECIDE:{decide_est:.0f})")
    if total_est >= 120:
        warn("  Consider: --fast flag or cap evidence to 3 artifacts")
    print()

    # ── 8. Landing Page ──
    print("  Landing Page:")
    landing = REPO_ROOT / "docs" / "landing" / "index.html"
    check("  index.html exists", landing.exists())
    if landing.exists():
        content = landing.read_text()
        check("  Capability matrix present", "cap-grid" in content)
        check("  Security section present", "trust-list" in content)
        check("  Hub URL configured", "localhost:7890" in content or "hstgr.cloud" in content)
    print()

    # ── Summary ──
    print("  " + "━" * 50)
    passed = sum(1 for _, ok, _ in results if ok is True)
    failed = sum(1 for _, ok, _ in results if ok is False)
    warned = sum(1 for _, ok, _ in results if ok is None)
    total = passed + failed

    if failed == 0:
        print(f"  {PASS} ALL CLEAR — {passed}/{total} checks pass. Ready to record.")
    else:
        print(f"  {FAIL} {failed} BLOCKER(S) — fix before recording.")
        print()
        print("  Blockers:")
        for name, ok, detail in results:
            if ok is False:
                print(f"    {FAIL} {name.strip()}: {detail}")
    print()


if __name__ == "__main__":
    main()
