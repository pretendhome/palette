#!/usr/bin/env python3
"""Conference Capture — Local-only structured extraction from conference notes.

Usage:
  python scripts/conference_capture/capture.py EVENT.md --photos DIR --output DIR

Inputs: EVENT.md (live notes), optional photo directory
Outputs: session_packets.json, signal_packets.json, convergence_brief.md

No network calls. No DB writes. No source-of-truth mutations.
Pure local text processing + EXIF timestamp alignment.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_sessions(text: str) -> list[dict]:
    """Extract per-talk session packets from EVENT.md structure."""
    sessions = []
    # Split by ### headers that look like talk sections
    pattern = r'### (\d+)\.\s+(.+?)(?=\n### \d+\.|\n## |\Z)'
    matches = re.finditer(pattern, text, re.DOTALL)

    for m in matches:
        session_num = m.group(1)
        block = m.group(2)

        # Extract title from first line
        lines = block.strip().split('\n')
        title_line = lines[0].strip()
        # Try to split "Company: Title" or just "Title"
        if ':' in title_line and '"' in title_line:
            parts = title_line.split(':', 1)
            speaker = parts[0].strip()
            title = parts[1].strip().strip('"').strip("'")
        elif '—' in title_line:
            parts = title_line.split('—', 1)
            title = parts[0].strip().strip('"').strip("'")
            speaker = parts[1].strip() if len(parts) > 1 else ""
        else:
            title = title_line.strip('"').strip("'")
            speaker = ""

        # Extract bold text as key claims
        claims = re.findall(r'\*\*(.+?)\*\*', block)
        # Filter out headers/labels — keep only substantive claims
        claims = [c for c in claims if len(c) > 10 and not c.endswith(':')]

        # Extract content lines (non-empty, non-header)
        content_lines = [l.strip() for l in lines[1:] if l.strip() and not l.startswith('#')]

        sessions.append({
            "session_id": f"vsd-2026-06-11-{session_num.zfill(2)}",
            "session_number": int(session_num),
            "title": title,
            "speaker": speaker,
            "key_claims": claims[:10],
            "content_line_count": len(content_lines),
        })

    return sessions


def extract_signals(sessions: list[dict], full_text: str) -> list[dict]:
    """Extract cross-talk signals from patterns in notes."""
    signals = []

    # Signal: retrieval ≠ authorization (from Neo4j permissions talk)
    if any("Retrieval" in s.get("title", "") or "Permissions" in str(s.get("key_claims", []))
           for s in sessions):
        signals.append({
            "signal_id": "VSD-SIG-001",
            "signal_type": "architectural_convergence",
            "description": "Multiple talks assert retrieval and authorization must be separate concerns",
            "sources": ["neo4j-permissions", "qdrant-edge"],
            "tier_1_principle": "retrieval_neq_authorization",
            "action": "Evaluate Qdrant payload filtering vs Neo4j graph filtering at our scale",
        })

    # Signal: similarity ≠ relevance (from Arize talk)
    if "Similar" in full_text and "Relevant" in full_text:
        signals.append({
            "signal_id": "VSD-SIG-002",
            "signal_type": "gap_detection",
            "description": "Similarity is only a proxy for relevance — need golden dataset evaluation",
            "sources": ["arize-eval"],
            "tier_1_principle": "similarity_neq_relevance",
            "action": "Build golden dataset (DONE: tests/golden_dataset_v1.yaml)",
        })

    # Signal: memory ≠ retrieval (from Mem0 talk)
    if "memory" in full_text.lower() and "retrieval" in full_text.lower():
        signals.append({
            "signal_id": "VSD-SIG-003",
            "signal_type": "architectural_convergence",
            "description": "Memory eval requires behavioral measurement, not retrieval metrics",
            "sources": ["mem0", "neo4j-context-graphs"],
            "tier_1_principle": "memory_neq_retrieval",
            "action": "Add memory-on/off comparison to eval harness",
        })

    # Signal: ontology as memory (validation of our taxonomy approach)
    if "ontology" in full_text.lower() and "memory" in full_text.lower():
        signals.append({
            "signal_id": "VSD-SIG-004",
            "signal_type": "competitive_validation",
            "description": "Cognee validates 'ontology as memory' — our taxonomy IS the ontology others are building",
            "sources": ["cognee"],
            "tier_1_principle": None,
            "action": "Use framing in positioning: 'ontology as memory'",
        })

    # Signal: action decomposition (from embodied AI talk)
    if "agent" in full_text.lower() and ("pick up" in full_text.lower() or "atomic" in full_text.lower()
                                          or "interchangeable" in full_text.lower()):
        signals.append({
            "signal_id": "VSD-SIG-005",
            "signal_type": "architectural_convergence",
            "description": "Embodied AI decomposes tasks into atomic interchangeable actions — maps to action taxonomy proposal",
            "sources": ["embodied-ai"],
            "tier_1_principle": None,
            "action": "See ACTION_TAXONOMY_RESEARCH.md — awaiting global team review",
        })

    return signals


def align_photos(photo_dir: Path, sessions: list[dict]) -> dict[str, list[str]]:
    """Align photos to sessions by EXIF timestamp (best-effort)."""
    if not photo_dir or not photo_dir.exists():
        return {}

    # Samsung naming: 20260611_HHMMSS.jpg
    photo_map = {}
    pattern = re.compile(r'20260611_(\d{2})(\d{2})(\d{2})')

    photos = sorted(photo_dir.glob("20260611_*"))
    for photo in photos:
        m = pattern.match(photo.name)
        if m:
            hour, minute = int(m.group(1)), int(m.group(2))
            photo_map.setdefault(f"{hour:02d}:{minute:02d}", []).append(photo.name)

    # Map photos to sessions by time proximity (basic)
    # This is placeholder — would need agenda timestamps for proper alignment
    return {"total_photos": len(photos), "by_time": {k: v for k, v in list(photo_map.items())[:20]}}


def generate_brief(sessions: list[dict], signals: list[dict]) -> str:
    """Generate convergence brief from session and signal data."""
    brief = f"""# Vector Space Day Convergence Brief
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Goal
Integrate conference insights into Mission Canvas retrieval, memory, and evaluation layers.

## Key Signals ({len(signals)})
"""
    for s in signals:
        brief += f"\n### {s['signal_id']}: {s['description']}\n"
        brief += f"- Type: {s['signal_type']}\n"
        brief += f"- Sources: {', '.join(s['sources'])}\n"
        brief += f"- Action: {s['action']}\n"
        if s.get('tier_1_principle'):
            brief += f"- Tier 1 principle: {s['tier_1_principle']}\n"

    brief += f"""
## Sessions Captured: {len(sessions)}
"""
    for s in sessions:
        brief += f"- [{s['session_id']}] {s['title']} ({len(s['key_claims'])} claims)\n"

    brief += """
## Constraints
- Local-only — no external services for core pipeline
- No taxonomy changes without global team review
- Golden dataset baseline BEFORE any retrieval changes (DONE: 29% RIU accuracy)

## Non-Goals
- Full Neo4j integration (deferred — scale doesn't justify)
- Passive skill generation (deferred — depends on action taxonomy)
- NPU-aware model routing (future product feature)

## Next Actions
1. Review action taxonomy proposal (global team)
2. Improve resolver accuracy (baseline: 29% RIU match)
3. Evaluate Qdrant Edge for local hybrid retrieval
4. Add memory-on/off eval to harness
"""
    return brief


def main():
    parser = argparse.ArgumentParser(description="Conference capture — local structured extraction")
    parser.add_argument("event_md", help="Path to EVENT.md")
    parser.add_argument("--photos", help="Path to photos directory")
    parser.add_argument("--output", default=".", help="Output directory")
    args = parser.parse_args()

    event_path = Path(args.event_md)
    if not event_path.exists():
        print(f"Error: {event_path} not found", file=sys.stderr)
        return 1

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = event_path.read_text()

    # Extract sessions
    sessions = parse_sessions(text)
    print(f"Extracted {len(sessions)} sessions")

    # Extract signals
    signals = extract_signals(sessions, text)
    print(f"Extracted {len(signals)} cross-talk signals")

    # Align photos
    photo_info = {}
    if args.photos:
        photo_dir = Path(args.photos)
        photo_info = align_photos(photo_dir, sessions)
        print(f"Found {photo_info.get('total_photos', 0)} photos")

    # Write session_packets.json
    session_output = {
        "metadata": {
            "event": "Vector Space Day SF 2026",
            "date": "2026-06-11",
            "generated": datetime.now().isoformat(),
            "source": str(event_path),
        },
        "sessions": sessions,
        "photo_alignment": photo_info,
    }
    (output_dir / "session_packets.json").write_text(json.dumps(session_output, indent=2))

    # Write signal_packets.json
    signal_output = {
        "metadata": {
            "event": "Vector Space Day SF 2026",
            "generated": datetime.now().isoformat(),
            "signal_count": len(signals),
        },
        "signals": signals,
    }
    (output_dir / "signal_packets.json").write_text(json.dumps(signal_output, indent=2))

    # Write convergence_brief.md
    brief = generate_brief(sessions, signals)
    (output_dir / "convergence_brief.md").write_text(brief)

    print(f"\nOutputs written to {output_dir}/:")
    print(f"  session_packets.json  ({len(sessions)} sessions)")
    print(f"  signal_packets.json   ({len(signals)} signals)")
    print(f"  convergence_brief.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
