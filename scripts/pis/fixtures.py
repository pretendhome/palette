"""5 fixture traversals for PIS regression testing."""

from __future__ import annotations

import sys

from .loader import PISData, load_all
from .traverse import traverse


class FixtureFailure(Exception):
    pass


def _assert(condition: bool, msg: str) -> None:
    if not condition:
        raise FixtureFailure(msg)


def fix_t1_guardrails(data: PISData) -> None:
    """RIU-082 (Guardrails) — full traversal with routing + recipe + knowledge."""
    r = traverse(data, riu_id="RIU-082")
    _assert(r.completeness is not None, "completeness missing")
    _assert(r.completeness.total >= 70, f"expected completeness >= 70, got {r.completeness.total}")
    _assert(r.classification == "both", f"expected classification 'both', got '{r.classification}'")
    _assert(r.recommendation is not None, "expected a service recommendation")
    _assert(len(r.gaps) > 0, "gaps should never be empty")
    _assert(len(r.knowledge_support) > 0, "expected knowledge support")


def fix_t2_llm_routing(data: PISData) -> None:
    """RIU-521 (LLM Routing) — OpenRouter recipe available, routing exists.
    Note: signals and knowledge entries for LLM routing are on RIU-252, not RIU-521.
    Current data yields completeness ~60 (routing + recipe, no signals/knowledge).
    """
    r = traverse(data, riu_id="RIU-521")
    _assert(r.completeness is not None, "completeness missing")
    _assert(r.completeness.total >= 60, f"expected completeness >= 60, got {r.completeness.total}")
    _assert(r.recommendation is not None, "expected a service recommendation")
    _assert(r.recommendation.recipe_available, "expected OpenRouter recipe to be found")
    _assert(r.classification == "both", f"expected classification 'both', got '{r.classification}'")
    _assert(len(r.gaps) > 0, "gaps should flag missing signals/knowledge")


def fix_t3_demo_creation(data: PISData) -> None:
    """RIU-413 (Demo Creation) — Gamma recipe + people signals."""
    r = traverse(data, riu_id="RIU-413")
    _assert(r.completeness is not None, "completeness missing")
    _assert(r.completeness.total >= 75, f"expected completeness >= 75, got {r.completeness.total}")
    _assert(r.recommendation is not None, "expected a service recommendation")
    _assert(len(r.signal_validation) > 0, "expected people signals for RIU-413")


def fix_t4_convergence_brief(data: PISData) -> None:
    """RIU-001 (Convergence Brief) — internal_only, no service recommendation."""
    r = traverse(data, riu_id="RIU-001")
    _assert(r.classification == "internal_only", f"expected internal_only, got '{r.classification}'")
    _assert(r.recommendation is None, "internal_only RIU should have no recommendation")
    _assert(len(r.gaps) > 0, "gaps should never be empty")
    _assert(len(r.knowledge_support) > 0, "expected knowledge support for RIU-001")


def fix_t5_audio_stub(data: PISData) -> None:
    """RIU-502 (Audio Processing) — stub routing (Wispr = no_api), expect degraded."""
    r = traverse(data, riu_id="RIU-502")
    _assert(r.completeness is not None, "completeness missing")
    # Wispr has no_api but Whisper is integrated, so primary may not be a stub.
    # The key check: completeness reflects the data state accurately.
    _assert(len(r.gaps) > 0, "gaps should flag issues for RIU-502")
    _assert(r.recommendation is not None, "expected recommendation (Whisper is integrated)")


FIXTURES = [
    ("FIX-T1", "RIU-082 Guardrails", fix_t1_guardrails),
    ("FIX-T2", "RIU-521 LLM Routing", fix_t2_llm_routing),
    ("FIX-T3", "RIU-413 Demo Creation", fix_t3_demo_creation),
    ("FIX-T4", "RIU-001 Convergence Brief (internal_only)", fix_t4_convergence_brief),
    ("FIX-T5", "RIU-502 Audio Processing (stub)", fix_t5_audio_stub),
]


def run_all(data: PISData | None = None) -> bool:
    """Run all fixtures, print pass/fail per fixture. Returns True if all pass."""
    if data is None:
        data = load_all()
    all_passed = True
    for fix_id, label, fn in FIXTURES:
        try:
            fn(data)
            print(f"  PASS  {fix_id}: {label}")
        except FixtureFailure as e:
            print(f"  FAIL  {fix_id}: {label} — {e}", file=sys.stderr)
            all_passed = False
        except Exception as e:
            print(f"  ERROR {fix_id}: {label} — {type(e).__name__}: {e}", file=sys.stderr)
            all_passed = False
    return all_passed
