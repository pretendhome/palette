#!/usr/bin/env python3
"""Golden dataset validation harness for palette_query.py.

Runs each query through the pipeline in --eval mode (no side effects),
compares actual vs expected, reports accuracy metrics.

Usage:
  python tests/validate_golden.py              # Full run
  python tests/validate_golden.py --dry-run    # Parse only, no queries
  python tests/validate_golden.py --limit 10   # First N queries
  python tests/validate_golden.py --difficulty hard  # Filter by difficulty
  python tests/validate_golden.py --category legal   # Filter by category
"""

import argparse
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = REPO_ROOT / "tests" / "golden_dataset_v1.yaml"
RESULTS_PATH = REPO_ROOT / "tests" / "golden_results.json"
QUERY_CMD = [sys.executable, str(REPO_ROOT / "scripts" / "palette_query.py")]


def load_golden():
    """Load golden dataset from YAML."""
    import yaml
    data = yaml.safe_load(GOLDEN_PATH.read_text())
    return data["queries"], data.get("metadata", {})


def run_query(query: str, timeout: int = 30) -> dict:
    """Run a single query through palette_query.py --eval --json."""
    start = time.time()
    try:
        result = subprocess.run(
            QUERY_CMD + ["--eval", "--json", query],
            capture_output=True, text=True, timeout=timeout,
            cwd=str(REPO_ROOT),
        )
        elapsed_ms = (time.time() - start) * 1000
        if result.returncode != 0:
            return {"error": result.stderr.strip() or "nonzero exit", "elapsed_ms": elapsed_ms}
        output = json.loads(result.stdout)
        output["elapsed_ms"] = elapsed_ms
        return output
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "elapsed_ms": timeout * 1000}
    except json.JSONDecodeError as e:
        return {"error": f"json_parse: {e}", "elapsed_ms": (time.time() - start) * 1000}
    except Exception as e:
        return {"error": str(e), "elapsed_ms": (time.time() - start) * 1000}


def evaluate(expected: dict, actual: dict) -> dict:
    """Compare expected vs actual for one query."""
    result = {
        "query": expected["query"],
        "difficulty": expected["difficulty"],
        "category": expected["category"],
        "expected_riu": expected["expected_riu"],
        "actual_riu": actual.get("riu_id"),
        "riu_match": expected["expected_riu"] == actual.get("riu_id"),
        "expected_classification": expected["expected_classification"],
        "actual_classification": actual.get("classification"),
        "classification_match": expected["expected_classification"] == actual.get("classification"),
        "expected_agent": expected["expected_agent"],
        "actual_agent": actual.get("agent"),
        "agent_match": expected["expected_agent"] == actual.get("agent"),
        "confidence": actual.get("confidence"),
        "elapsed_ms": actual.get("elapsed_ms", 0),
        "error": actual.get("error"),
    }

    # Check gateway blocking for adversarial cases
    if expected.get("expected_blocked"):
        gateway = actual.get("gateway") or {}
        gov = gateway.get("governance", {}) if isinstance(gateway, dict) else {}
        result["expected_blocked"] = True
        result["actual_blocked"] = gov.get("blocked", False)
        result["blocked_match"] = result["actual_blocked"] == True

    # Check knowledge retrieval (partial match — at least one expected ID found)
    expected_kl = expected.get("expected_knowledge_ids", [])
    actual_kl = [k.get("lib_id", "") for k in (actual.get("knowledge") or [])]
    if expected_kl:
        result["knowledge_hit"] = any(eid in actual_kl for eid in expected_kl)
    else:
        result["knowledge_hit"] = None  # No expectation

    return result


def print_report(results: list, metadata: dict):
    """Print summary report to stdout."""
    total = len(results)
    errors = [r for r in results if r.get("error")]
    valid = [r for r in results if not r.get("error")]

    riu_correct = sum(1 for r in valid if r["riu_match"])
    class_correct = sum(1 for r in valid if r["classification_match"])
    agent_correct = sum(1 for r in valid if r["agent_match"])
    kl_hits = [r for r in valid if r.get("knowledge_hit") is not None]
    kl_correct = sum(1 for r in kl_hits if r["knowledge_hit"])

    blocked_cases = [r for r in valid if r.get("expected_blocked")]
    blocked_correct = sum(1 for r in blocked_cases if r.get("blocked_match"))

    print(f"\n{'='*60}")
    print(f"GOLDEN DATASET VALIDATION — {metadata.get('version', '?')}")
    print(f"{'='*60}")
    print(f"Total queries: {total}")
    print(f"Errors: {len(errors)}")
    print(f"Valid results: {len(valid)}")
    print()

    if valid:
        print(f"RIU Accuracy:            {riu_correct}/{len(valid)} = {riu_correct/len(valid)*100:.1f}%")
        print(f"Classification Accuracy: {class_correct}/{len(valid)} = {class_correct/len(valid)*100:.1f}%")
        print(f"Agent Accuracy:          {agent_correct}/{len(valid)} = {agent_correct/len(valid)*100:.1f}%")
        if kl_hits:
            print(f"Knowledge Hit Rate:      {kl_correct}/{len(kl_hits)} = {kl_correct/len(kl_hits)*100:.1f}%")
        if blocked_cases:
            print(f"Gateway Block Accuracy:  {blocked_correct}/{len(blocked_cases)} = {blocked_correct/len(blocked_cases)*100:.1f}%")

    # Breakdown by difficulty
    print(f"\n--- By Difficulty ---")
    for diff in ["easy", "medium", "hard", "adversarial"]:
        subset = [r for r in valid if r["difficulty"] == diff]
        if subset:
            correct = sum(1 for r in subset if r["riu_match"])
            print(f"  {diff:12s}: {correct}/{len(subset)} = {correct/len(subset)*100:.1f}%")

    # Breakdown by category
    print(f"\n--- By Category ---")
    cats = defaultdict(list)
    for r in valid:
        cats[r["category"]].append(r)
    for cat in sorted(cats):
        subset = cats[cat]
        correct = sum(1 for r in subset if r["riu_match"])
        print(f"  {cat:20s}: {correct}/{len(subset)} = {correct/len(subset)*100:.1f}%")

    # Confidence calibration
    print(f"\n--- Confidence Calibration ---")
    buckets = {"0-25": [], "25-50": [], "50-75": [], "75-100": []}
    for r in valid:
        c = r.get("confidence") or 0
        if c <= 25:
            buckets["0-25"].append(r)
        elif c <= 50:
            buckets["25-50"].append(r)
        elif c <= 75:
            buckets["50-75"].append(r)
        else:
            buckets["75-100"].append(r)
    for bucket, items in buckets.items():
        if items:
            correct = sum(1 for r in items if r["riu_match"])
            print(f"  Confidence {bucket:6s}: {correct}/{len(items)} correct ({correct/len(items)*100:.1f}%)")

    # Latency
    latencies = [r["elapsed_ms"] for r in valid if r.get("elapsed_ms")]
    if latencies:
        latencies.sort()
        print(f"\n--- Latency ---")
        print(f"  Mean:   {sum(latencies)/len(latencies):.0f}ms")
        print(f"  Median: {latencies[len(latencies)//2]:.0f}ms")
        print(f"  P95:    {latencies[int(len(latencies)*0.95)]:.0f}ms")
        print(f"  Max:    {latencies[-1]:.0f}ms")

    # Failures detail
    failures = [r for r in valid if not r["riu_match"]]
    if failures:
        print(f"\n--- Failures (first 10) ---")
        for r in failures[:10]:
            print(f"  Q: {r['query'][:60]}")
            print(f"    Expected: {r['expected_riu']} | Got: {r['actual_riu']} (conf={r.get('confidence')})")
            print()

    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Validate palette_query against golden dataset")
    parser.add_argument("--dry-run", action="store_true", help="Parse dataset only, don't run queries")
    parser.add_argument("--limit", type=int, help="Run only first N queries")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard", "adversarial"], help="Filter by difficulty")
    parser.add_argument("--category", help="Filter by category (substring match)")
    args = parser.parse_args()

    queries, metadata = load_golden()
    print(f"Loaded {len(queries)} golden queries")

    # Apply filters
    if args.difficulty:
        queries = [q for q in queries if q["difficulty"] == args.difficulty]
        print(f"Filtered to {len(queries)} ({args.difficulty})")
    if args.category:
        queries = [q for q in queries if args.category.lower() in q["category"].lower()]
        print(f"Filtered to {len(queries)} (category: {args.category})")
    if args.limit:
        queries = queries[:args.limit]
        print(f"Limited to {args.limit}")

    if args.dry_run:
        # Validate dataset structure
        issues = []
        rius_seen = set()
        for i, q in enumerate(queries):
            for field in ["query", "expected_riu", "expected_classification", "difficulty", "category"]:
                if field not in q and field != "expected_riu":  # expected_riu can be null for adversarial
                    issues.append(f"  Query {i}: missing '{field}'")
            rius_seen.add(q.get("expected_riu"))
        rius_seen.discard(None)
        print(f"\nDataset structure: {'VALID' if not issues else 'ISSUES FOUND'}")
        print(f"Distinct RIUs: {len(rius_seen)}")
        print(f"Difficulty distribution: {defaultdict(int, {q['difficulty']: 0 for q in queries})}")
        diff_counts = defaultdict(int)
        for q in queries:
            diff_counts[q["difficulty"]] += 1
        for d, c in sorted(diff_counts.items()):
            print(f"  {d}: {c}")
        if issues:
            for issue in issues[:10]:
                print(issue)
        return 0

    # Run validation
    results = []
    print(f"\nRunning {len(queries)} queries (--eval mode, no side effects)...")
    for i, expected in enumerate(queries):
        sys.stdout.write(f"\r  [{i+1}/{len(queries)}] {expected['query'][:50]}...")
        sys.stdout.flush()
        actual = run_query(expected["query"])
        result = evaluate(expected, actual)
        results.append(result)

    sys.stdout.write("\r" + " " * 80 + "\r")
    print_report(results, metadata)

    # Save results
    RESULTS_PATH.write_text(json.dumps({
        "metadata": metadata,
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "total": len(results),
        "results": results,
    }, indent=2))
    print(f"\nResults saved to: {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
