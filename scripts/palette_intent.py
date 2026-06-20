#!/usr/bin/env python3
"""palette — Unified CLI for Palette OS intents.

Usage:
  palette protect "What's our exposure?"
  palette research "Delaware fiduciary duty cases"
  palette decide "Should Sarah settle or litigate?"
  palette create "Draft client update memo"
  palette diagnose "Why did the privileged query route externally?"
  palette fix "Why did the privileged query route externally?"  # alias for diagnose
  palette reflect "What did we learn today?"
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def main():
    # Activate socket firewall before any intent runs.
    # Only governed external APIs (Perplexity, Anthropic, Mistral, Groq)
    # and local services (Ollama, bus) are permitted.
    try:
        from core.gateway.socket_firewall import activate_firewall
        activate_firewall()
    except Exception:
        pass  # firewall module may not exist in all environments

    if len(sys.argv) < 2:
        print("  ◆ palette  the operating system for professional judgment")
        print()
        print("  Usage: palette <intent> <query>")
        print()
        print("  Intents:")
        print("    protect   — Governance gate (is this safe for external?)")
        print("    research  — Governed evidence gathering")
        print("    decide    — Turn ambiguity into judgment")
        print("    create    — Turn intent into artifact")
        print("    diagnose  — Find failure, repair, remember lesson")
        print("    fix       — Alias for diagnose")
        print("    reflect   — Turn experience into memory")
        print()
        print("  Options:")
        print("    --matter, -m   Link artifacts to a matter")
        print("    --json, -j     JSON output")
        print("    --local-only   Skip external (research only)")
        print("    --audience, -a Target audience (create only)")
        sys.exit(1)

    intent = sys.argv[1].lower()
    # Remove the intent from argv so argparse in sub-commands works
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    if intent == "protect":
        from scripts.palette_intents.protect import main as protect_main
        protect_main()
    elif intent == "research":
        from scripts.palette_intents.research import main as research_main
        research_main()
    elif intent == "decide":
        from scripts.palette_intents.decide import main as decide_main
        decide_main()
    elif intent == "create":
        from scripts.palette_intents.create import main as create_main
        create_main()
    elif intent in ("diagnose", "fix"):
        from scripts.palette_intents.diagnose import main as diagnose_main
        diagnose_main()
    elif intent == "reflect":
        from scripts.palette_intents.reflect import main as reflect_main
        reflect_main()
    elif intent == "stats":
        from scripts.palette_stats import run as stats_run
        stats_run(as_json="--json" in sys.argv or "-j" in sys.argv)
    elif intent == "query":
        # Legacy: forward to palette_query
        from scripts.palette_query import main as query_main
        query_main()
    elif intent == "orchestrate":
        # Legacy: forward to palette_orchestrate
        from scripts.palette_orchestrate import main as orchestrate_main
        orchestrate_main()
    else:
        print(f"Unknown intent: {intent}")
        print("Available: protect, research, decide, create, diagnose (fix), reflect")
        sys.exit(1)


if __name__ == "__main__":
    main()
