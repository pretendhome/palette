#!/usr/bin/env python3
"""palette demo sarah — Run the full BDB 3-moment demo flow.

Usage:
  palette demo sarah

Runs 3 queries through the full orchestration loop (up to 7 steps each):
  Moment 1: Strategy question → BLOCKED by sanitizer → local only (Ollama)
  Moment 2: Public legal research → Perplexity → Claude synthesis → Mistral critique
  Moment 3: Adversarial challenge → compounding across all prior decisions

Models used: Ollama (on-device), Perplexity (governed research),
Claude (governed synthesis), Mistral (governed critique).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.palette_intents.infra import BOLD, CYAN, DIM, RESET, WHITE

# Moment 1: Contains "our exposure" (strategy language) → sanitizer blocks external.
# No ALLOWED_KEYWORDS (fiduciary/delaware) → fails public-research check → LOCAL ONLY.
MOMENT_1_QUERY = (
    "What's our exposure if the majority member was self-dealing "
    "through a related-party transaction?"
)

# Moment 2: Contains "fiduciary" + "Delaware" (ALLOWED_KEYWORDS) → passes sanitizer.
# Routes: Perplexity (research) → Claude (synthesis) → Mistral (critique).
MOMENT_2_QUERY = (
    "What fiduciary duty standards apply to LLC co-founders in Delaware?"
)

# Moment 3: Contains "fiduciary" + "Delaware" (ALLOWED_KEYWORDS), no blocked indicators.
# Routes externally again — but now [CONNECT] shows 2 prior decisions compounding.
MOMENT_3_QUERY = (
    "What are the strongest legal arguments against a fiduciary duty "
    "breach claim in a Delaware LLC dispute?"
)


def run_demo():
    """Run the full Sarah demo: 3 moments through the orchestration loop."""

    print()
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print(f"  {BOLD}{WHITE}  SARAH'S MORNING — Mission Canvas Demo{RESET}")
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print()
    print(f"  {DIM}3 moments. Up to 4 models. Zero client data leakage.{RESET}")
    print()

    from scripts.palette_orchestrate import orchestrate

    # ── Moment 1: Strategy question → BLOCKED → local only ──────────
    print(f"  {CYAN}{'━' * 20} MOMENT 1: PROTECT {'━' * 20}{RESET}")
    print(f"  {DIM}Sarah asks about case strategy. Watch what gets blocked.{RESET}")
    orchestrate(MOMENT_1_QUERY)

    print()
    input(f"  {DIM}[Press Enter for Moment 2...]{RESET}")

    # ── Moment 2: Public research → multi-model orchestration ───────
    print(f"  {CYAN}{'━' * 20} MOMENT 2: RESEARCH {'━' * 19}{RESET}")
    print(f"  {DIM}Same case, public question. Watch the models coordinate.{RESET}")
    orchestrate(MOMENT_2_QUERY)

    print()
    input(f"  {DIM}[Press Enter for Moment 3...]{RESET}")

    # ── Moment 3: Adversarial challenge → compounding chain ─────────
    print(f"  {CYAN}{'━' * 20} MOMENT 3: CRITIQUE {'━' * 19}{RESET}")
    print(f"  {DIM}Adversarial challenge. Watch the compounding chain grow.{RESET}")
    orchestrate(MOMENT_3_QUERY)

    # ── Close ───────────────────────────────────────────────────────
    print()
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print(f"  {BOLD}  DEMO COMPLETE{RESET}")
    print()
    print(f"  {DIM}  Three queries. Up to four AI models.{RESET}")
    print(f"  {BOLD}  None of them know the client exists.{RESET}")
    print()
    print(f"  {DIM}  Run: palette stats{RESET}")
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(prog="palette demo")
    parser.add_argument(
        "scenario", nargs="?", default="sarah",
        help="Demo scenario (default: sarah)",
    )
    args = parser.parse_args()

    if args.scenario != "sarah":
        print(f"Unknown demo scenario: {args.scenario}")
        print("Available: sarah")
        sys.exit(1)

    run_demo()


if __name__ == "__main__":
    main()
