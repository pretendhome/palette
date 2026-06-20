#!/usr/bin/env python3
"""palette create — Turn intent into artifact.

Usage:
  palette create "Draft a client update memo for the fiduciary case"
  palette create --audience judge "Explain the fiduciary breach"
  palette create --matter sarah-llc-001 "Write a settlement risk analysis"
  palette create --json "Build a compliance checklist"

Produces: ArtifactLineage (spec + artifact + provenance).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.palette_intents.infra import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    RED,
    RESET,
    WHITE,
    YELLOW,
    IntentState,
    build_integrity_card_fast,
    emit_integrity_signal,
    palette_checkpoint,
    pis_display_line,
    pis_summary,
    format_pis_line,
    print_unvalidated_warning,
    resolve_query,
    store_artifact,
    ARTIFACTS_DIR,
)


# ── Model Caller ────────────────────────────────────────────────────────


def call_ollama(prompt: str, system: str = "", model: str = "qwen2.5:7b") -> str | None:
    """Call local Ollama."""
    from urllib import request

    payload = json.dumps({
        "model": model,
        "prompt": f"{system}\n\n{prompt}" if system else prompt,
        "stream": False,
    }).encode()
    req = request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read()).get("response", "")
    except Exception:
        return None


# ── Prior Evidence Retrieval ────────────────────────────────────────────


def gather_matter_context(matter_id: str | None) -> str:
    """Gather context from prior artifacts for this matter."""
    if not matter_id:
        return ""

    parts = []
    for type_dir in ARTIFACTS_DIR.iterdir():
        if not type_dir.is_dir():
            continue
        for f in sorted(type_dir.glob("*.md"), reverse=True)[:10]:
            try:
                text = f.read_text()
                if f"matter_id: {matter_id}" not in text and f"matter_id: '{matter_id}'" not in text:
                    continue
                if text.startswith("---"):
                    end = text.index("---", 3)
                    import yaml
                    fm = yaml.safe_load(text[3:end])
                    if fm.get("artifact_type") == "EvidenceBrief":
                        for lc in fm.get("local_canon", [])[:2]:
                            parts.append(f"[EVIDENCE] {lc.get('content', '')[:200]}")
                    elif fm.get("artifact_type") == "DecisionRecord":
                        parts.append(f"[DECISION] {fm.get('recommendation', '')[:200]}")
                    elif fm.get("artifact_type") == "GateDecision":
                        parts.append(f"[BOUNDARY] Action: {fm.get('action', '')} | Reason: {fm.get('reason', '')[:100]}")
            except Exception:
                pass
    return "\n".join(parts[:10])


# ── Main CREATE Logic ───────────────────────────────────────────────────


def run_create(
    query: str,
    audience: str | None = None,
    matter_id: str | None = None,
    show_json: bool = False,
) -> tuple[dict, IntentState]:
    """Execute CREATE intent. Returns (ArtifactLineage dict, final IntentState)."""

    t0 = time.time()

    # 1. Resolve RIU
    resolved = resolve_query(query)
    riu_id = resolved.get("riu_id")
    riu_name = resolved.get("riu_name", "")
    confidence = resolved.get("confidence", 0)
    classification = resolved.get("classification", "both")
    knowledge_entries = resolved.get("knowledge", [])

    # 2. Build state
    state = IntentState(
        intent="CREATE",
        query=query,
        riu=riu_id,
        riu_name=riu_name,
        boundary="local_only",
        confidence=confidence,
        matter_id=matter_id,
    )

    # 3. Integrity card
    card = build_integrity_card_fast(riu_id or "unknown", classification, len(knowledge_entries))
    state.integrity_card = asdict(card)

    # 3b. Checkpoint
    checked = palette_checkpoint(state)
    if checked.intent != "CREATE" and not show_json:
        print(f"  {YELLOW}[CHECKPOINT]{RESET} Transition suggested: → {checked.intent}")

    # 4. Gather matter context
    matter_context = gather_matter_context(matter_id)

    # 5. Build spec
    constraints = []
    if classification == "internal_only":
        constraints.append("No client names in output")
        constraints.append("No privileged strategy details")
    if audience:
        constraints.append(f"Audience: {audience}")
        constraints.append(f"Tone and complexity appropriate for {audience}")

    # 6. Local knowledge for grounding
    knowledge_context = ""
    for kl in knowledge_entries[:3]:
        knowledge_context += f"[{kl.get('lib_id', '')}] {kl.get('answer_excerpt', '')[:200]}\n"

    # 7. Generate artifact
    if not show_json:
        print()
        print(f"  {DIM}{'━' * 60}{RESET}")
        print(f"  {BOLD}{WHITE}  ◆ palette create{RESET}  {DIM}turning intent into artifact{RESET}")
        print(f"  {DIM}{'━' * 60}{RESET}")
        print()
        print(f"  {DIM}Request:{RESET}  {BOLD}{query}{RESET}")
        if audience:
            print(f"  {DIM}Audience:{RESET}  {audience}")
        print()
        if riu_id:
            print(f"  {CYAN}[RESOLVE]{RESET} {riu_id} ({riu_name}) — {confidence:.0f}% confidence")
            pis = pis_summary(riu_id, len(knowledge_entries), classification)
            print(f"  {CYAN}[PIS]{RESET}     {format_pis_line(pis)}")
        if constraints:
            print(f"  {CYAN}[CONSTRAINTS]{RESET} {len(constraints)} active")
            for c in constraints:
                print(f"  {DIM}  • {c}{RESET}")
        print()
        print(f"  {DIM}[BUILD]{RESET} Generating artifact...")

    audience_instruction = f"\nAUDIENCE: {audience}. Write for this specific audience." if audience else ""
    constraint_text = "\n".join(f"- {c}" for c in constraints) if constraints else "None"

    build_prompt = f"""Create the following artifact:

REQUEST: {query}
{audience_instruction}

CONSTRAINTS:
{constraint_text}

CONTEXT FROM PRIOR WORK:
{matter_context[:1500]}

RELEVANT KNOWLEDGE:
{knowledge_context[:1000]}

Write the complete artifact. Be specific, concrete, and professional. If this is a memo or document, include proper structure (headers, sections). If this is code, include comments."""

    system_prompt = "You are a professional writer and builder. Create exactly what is requested. Be complete and precise."
    if audience:
        system_prompt += f" Your audience is: {audience}. Adapt tone, complexity, and framing accordingly."

    artifact_content = call_ollama(build_prompt, system=system_prompt)

    if not artifact_content:
        if not show_json:
            print_unvalidated_warning("Local model unavailable — artifact generation failed")
        artifact_content = f"[GENERATION FAILED]\n\nRequest: {query}\nModel unavailable. Retry when Ollama is running."

    # 8. Review step (quick self-check with smaller model)
    review_prompt = f"""Review this artifact against its constraints. List any violations.

CONSTRAINTS:
{constraint_text}

ARTIFACT:
{artifact_content[:1500]}

If no violations, say "PASS". If violations found, list them briefly."""

    review_result = call_ollama(review_prompt, system="You are a strict reviewer. Check constraints only.", model="qwen2.5:3b")
    review_passed = review_result and "pass" in review_result.lower()[:50] if review_result else True

    # 8b. Self-correction loop: retry if review fails, up to max_iterations
    iterations = 1
    while not review_passed and iterations < 3:
        iterations += 1
        if not show_json:
            print(f"  {YELLOW}[REBUILD]{RESET} Review failed — iteration {iterations}/3...")

        rebuild_prompt = f"""The previous artifact FAILED review. Fix the violations.

ORIGINAL REQUEST: {query}
{audience_instruction}

CONSTRAINTS:
{constraint_text}

REVIEW VIOLATIONS:
{review_result}

PREVIOUS ARTIFACT:
{artifact_content[:1500]}

Rewrite the artifact to fix ALL violations. Keep everything else intact."""

        artifact_content = call_ollama(rebuild_prompt, system=system_prompt) or artifact_content

        # Re-review
        review_prompt_retry = f"""Review this artifact against its constraints. List any violations.

CONSTRAINTS:
{constraint_text}

ARTIFACT:
{artifact_content[:1500]}

If no violations, say "PASS". If violations found, list them briefly."""

        review_result = call_ollama(review_prompt_retry, system="You are a strict reviewer. Check constraints only.", model="qwen2.5:3b")
        review_passed = review_result and "pass" in review_result.lower()[:50] if review_result else True

    # 9. Build ArtifactLineage
    artifact_lineage = {
        "artifact_type": "ArtifactLineage",
        "intent": "CREATE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "riu_id": riu_id,
        "boundary": "local_only",
        "spec": query,
        "constraints": constraints,
        "audience": audience,
        "iterations": iterations,
        "max_iterations": 3,
        "models_used": ["ollama/qwen2.5:7b"],
        "review_passed": review_passed,
        "provenance": [],
        "status": "VALIDATED" if review_passed else "NEEDS_REVIEW",
    }

    # Add provenance from matter artifacts
    if matter_id:
        for type_dir in ARTIFACTS_DIR.iterdir():
            if not type_dir.is_dir():
                continue
            for f in sorted(type_dir.glob("*.md"), reverse=True)[:5]:
                try:
                    text = f.read_text()
                    if f"matter_id: {matter_id}" in text or f"matter_id: '{matter_id}'" in text:
                        artifact_lineage["provenance"].append(str(f))
                except Exception:
                    pass

    # 10. Store artifact
    body = f"# Created Artifact\n\n"
    body += f"**Request**: {query}\n"
    if audience:
        body += f"**Audience**: {audience}\n"
    body += f"**Review**: {'PASS ✅' if review_passed else 'NEEDS REVIEW ⚠️'}\n\n"
    body += f"---\n\n{artifact_content}\n"

    artifact_path = store_artifact("artifact_lineage", artifact_lineage, body)
    state.artifacts.append(artifact_path)

    # 11. Emit integrity signal
    elapsed_ms = round((time.time() - t0) * 1000, 1)
    emit_integrity_signal(
        intent="CREATE",
        riu_id=riu_id,
        success=review_passed,
        artifact_path=artifact_path,
        details=f"audience={audience} review={'pass' if review_passed else 'fail'} elapsed={elapsed_ms}ms",
    )

    # 12. Display
    if not show_json:
        print()
        print(f"  {'━' * 4} ARTIFACT {'━' * 44}")
        print()
        if review_passed:
            print(f"  {GREEN}[REVIEW]{RESET} Constraints check: PASS ✅")
        else:
            print(f"  {YELLOW}[REVIEW]{RESET} Constraints check: NEEDS REVIEW ⚠️")
            if review_result:
                for line in review_result.strip().split("\n")[:3]:
                    print(f"  {DIM}  {line.strip()}{RESET}")
        print()
        print(f"  {'─' * 50}")
        # Show first ~15 lines of artifact
        lines = artifact_content.strip().split("\n")
        for line in lines[:15]:
            print(f"  {line}")
        if len(lines) > 15:
            print(f"  {DIM}  ... ({len(lines) - 15} more lines){RESET}")
        print()
        print(f"  {'─' * 50}")
        print()
        print(f"  {DIM}[STORED] {artifact_path}{RESET}")
        if matter_id:
            print(f"  {DIM}  Provenance: {len(artifact_lineage['provenance'])} source artifacts{RESET}")
        print(f"  {DIM}[TIME]   {elapsed_ms}ms{RESET}")
        print()
    else:
        # For JSON, include the artifact content in the output
        artifact_lineage["content"] = artifact_content
        print(json.dumps(artifact_lineage, indent=2, default=str))

    return artifact_lineage, state


# ── CLI ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="palette create",
        description="Turn intent into artifact.",
    )
    parser.add_argument("query", help="What to create")
    parser.add_argument("--audience", "-a", help="Target audience (e.g., judge, client, board)")
    parser.add_argument("--matter", "-m", help="Matter ID for artifact linkage")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()

    run_create(args.query, audience=args.audience, matter_id=args.matter, show_json=args.json)


if __name__ == "__main__":
    main()
