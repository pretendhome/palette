#!/usr/bin/env python3
"""
validate_wiki.py — Phase 1 validation suite for the compiled Palette wiki.

Checks:
1. Orientation test
2. Coverage check
3. Broken backlink check
4. Orphan detection
5. Adversarial uncertainty test
6. Deterministic rebuild
7. Dual-experience test

Usage:
    python3 scripts/validate_wiki.py
    python3 scripts/validate_wiki.py --wiki wiki/
    python3 scripts/validate_wiki.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


PALETTE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WIKI = PALETTE_ROOT / "wiki"
COMPILER_PATH = PALETTE_ROOT / "scripts" / "compile_wiki.py"

WORD_RE = re.compile(r"[a-z0-9][a-z0-9\-]+")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
LOCAL_MD_LINK_RE = re.compile(r"\.md(?:[#?].*)?$")

ORIENTATION_QUERY = "What does Palette recommend for evaluating LLM output quality?"
ORIENTATION_EXPECTED_IDS = {"LIB-103", "LIB-114", "RIU-524"}
ORIENTATION_EXPECTED_TERMS = {"lm-as-judge", "deterministic", "rubric", "monitoring"}

ADVERSARIAL_QUERY = "What does Palette recommend for quantum telepathy crm routing with consciousness embeddings?"
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "by", "does", "for", "from", "how", "i", "in",
    "is", "it", "of", "on", "or", "palette", "recommend", "should", "the", "to", "what",
    "when", "with",
}


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationReport:
    wiki_path: str
    passed: bool
    checks: list[CheckResult]


def load_compiler_module():
    spec = importlib.util.spec_from_file_location("compile_wiki_module", COMPILER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load compiler from {COMPILER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    _, raw_frontmatter, body = parts
    frontmatter = yaml.safe_load(raw_frontmatter) or {}
    return frontmatter, body.lstrip("\n")


def normalize_for_hash(text: str) -> str:
    normalized = re.sub(r"^compiled_at:\s+.*$", "compiled_at: <normalized>", text, flags=re.MULTILINE)
    return normalized


def file_hash(path: Path) -> str:
    text = read_text(path)
    normalized = normalize_for_hash(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(PALETTE_ROOT))
    except ValueError:
        return str(path)


GOVERNANCE_FILES = {"APPROVAL_QUEUE.md", "VOTING_ROSTER.yaml"}


def iter_md_files(wiki_dir: Path) -> list[Path]:
    return sorted(p for p in wiki_dir.rglob("*.md") if p.is_file() and p.name not in GOVERNANCE_FILES and "archive" not in p.parts and "proposed" not in p.parts)


def tokenize(text: str) -> list[str]:
    tokens = []
    for match in WORD_RE.finditer(text.lower()):
        token = match.group(0)
        if token in STOPWORDS or len(token) < 3:
            continue
        tokens.append(token)
    return tokens


def build_search_index(paths: list[Path]) -> dict[Path, Counter]:
    return {path: Counter(tokenize(read_text(path))) for path in paths}


def score_query(query: str, doc_terms: Counter) -> float:
    query_terms = Counter(tokenize(query))
    if not query_terms:
        return 0.0
    overlap = 0
    bonus = 0.0
    for term, count in query_terms.items():
        if term in doc_terms:
            overlap += min(count, doc_terms[term])
            bonus += min(doc_terms[term], 3) * 0.2
    return overlap + bonus


def search(query: str, index: dict[Path, Counter], top_n: int = 5) -> list[tuple[Path, float]]:
    scored = []
    for path, terms in index.items():
        score = score_query(query, terms)
        if score > 0:
            scored.append((path, score))
    scored.sort(key=lambda item: (-item[1], str(item[0])))
    return scored[:top_n]


def extract_ids(text: str) -> set[str]:
    return set(re.findall(r"\b(?:LIB|RIU)-\d{3}\b", text))


def orientation_test(wiki_dir: Path, paths: list[Path]) -> CheckResult:
    index = build_search_index(paths)
    hits = search(ORIENTATION_QUERY, index, top_n=5)
    top_paths = [path for path, _ in hits]
    top_text = "\n".join(read_text(path) for path in top_paths)
    ids = extract_ids(top_text)
    terms_present = {term for term in ORIENTATION_EXPECTED_TERMS if term in top_text.lower()}
    top_names = [path.name for path in top_paths]

    enough_ids = len(ids & ORIENTATION_EXPECTED_IDS) >= 2
    enough_terms = len(terms_present) >= 2
    passed = len(hits) >= 3 and enough_ids and enough_terms
    detail = (
        f"top hits: {', '.join(top_names[:3])}; "
        f"expected ids found: {sorted(ids & ORIENTATION_EXPECTED_IDS)}; "
        f"key terms: {sorted(terms_present)}"
    )
    return CheckResult(
        name="orientation_test",
        passed=passed,
        detail=detail,
        data={"hits": top_names, "found_ids": sorted(ids), "terms": sorted(terms_present)},
    )


def coverage_check(wiki_dir: Path, compiler_module) -> CheckResult:
    rius, kl_entries, _, agents, enablement_rius, _ = compiler_module.load_all_data()
    riu_pages = list((wiki_dir / "rius").glob("RIU-*.md"))
    kl_pages = list((wiki_dir / "entries").glob("LIB-*.md"))
    agent_pages = list((wiki_dir / "agents").glob("*.md"))
    path_pages = list((wiki_dir / "paths").glob("RIU-*.md"))

    passed = (
        len(riu_pages) == len(rius)
        and len(kl_pages) == len(kl_entries)
        and len(agent_pages) == len(agents)
        and len(path_pages) == len(enablement_rius)
    )
    detail = (
        f"RIUs {len(riu_pages)}/{len(rius)}, "
        f"KL {len(kl_pages)}/{len(kl_entries)}, "
        f"agents {len(agent_pages)}/{len(agents)}, "
        f"paths {len(path_pages)}/{len(enablement_rius)}"
    )
    return CheckResult(
        name="coverage_check",
        passed=passed,
        detail=detail,
        data={
            "rius": [len(riu_pages), len(rius)],
            "knowledge_entries": [len(kl_pages), len(kl_entries)],
            "agents": [len(agent_pages), len(agents)],
            "paths": [len(path_pages), len(enablement_rius)],
        },
    )


def broken_backlinks_check(wiki_dir: Path, paths: list[Path]) -> CheckResult:
    broken: list[dict[str, str]] = []
    for path in paths:
        text = read_text(path)
        for _, target in LINK_RE.findall(text):
            if (
                "://" in target
                or target.startswith("#")
                or target.startswith("mailto:")
                or not LOCAL_MD_LINK_RE.search(target)
            ):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                broken.append({"source": repo_relative(path), "target": target})
    passed = not broken
    detail = "0 broken local wiki links" if passed else f"{len(broken)} broken local wiki links"
    return CheckResult(
        name="broken_backlinks_check",
        passed=passed,
        detail=detail,
        data={"broken_links": broken[:20]},
    )


def orphan_detection(wiki_dir: Path, paths: list[Path]) -> CheckResult:
    inbound: dict[Path, int] = defaultdict(int)
    all_paths = {path.resolve() for path in paths}
    exempt = { (wiki_dir / "index.md").resolve() }

    for path in paths:
        text = read_text(path)
        for _, target in LINK_RE.findall(text):
            if (
                "://" in target
                or target.startswith("#")
                or target.startswith("mailto:")
                or not LOCAL_MD_LINK_RE.search(target)
            ):
                continue
            resolved = (path.parent / target).resolve()
            if resolved in all_paths:
                inbound[resolved] += 1

    orphans = [repo_relative(path) for path in paths if path.resolve() not in exempt and inbound[path.resolve()] == 0]
    passed = not orphans
    detail = "0 orphan pages" if passed else f"{len(orphans)} orphan pages"
    return CheckResult(
        name="orphan_detection",
        passed=passed,
        detail=detail,
        data={"orphans": orphans[:20]},
    )


def adversarial_test(paths: list[Path]) -> CheckResult:
    index = build_search_index(paths)
    hits = search(ADVERSARIAL_QUERY, index, top_n=5)
    query_tokens = set(tokenize(ADVERSARIAL_QUERY))
    overlap_terms: set[str] = set()
    for path, _score in hits[:3]:
        overlap_terms |= (query_tokens & set(build_search_index([path])[path].keys()))
    overlap_terms.discard("routing")
    strongest = hits[0][1] if hits else 0.0
    passed = len(overlap_terms) <= 2 and strongest < 3.5
    detail = "query correctly falls below semantic overlap threshold" if passed else (
        f"unexpected overlap terms={sorted(overlap_terms)} strongest_score={strongest:.2f}"
    )
    return CheckResult(
        name="adversarial_test",
        passed=passed,
        detail=detail,
        data={"top_hits": [path.name for path, _ in hits], "strongest_score": strongest, "overlap_terms": sorted(overlap_terms)},
    )


def deterministic_rebuild(compiler_module, wiki_dir: Path) -> CheckResult:
    with tempfile.TemporaryDirectory(prefix="palette-wiki-") as tmp:
        tmp_path = Path(tmp) / "wiki"
        compiler_module.compile_wiki(tmp_path)

        current_files = {p.relative_to(wiki_dir): file_hash(p) for p in iter_md_files(wiki_dir)}
        rebuilt_files = {p.relative_to(tmp_path): file_hash(p) for p in iter_md_files(tmp_path)}

        missing = sorted(str(p) for p in current_files.keys() - rebuilt_files.keys())
        extra = sorted(str(p) for p in rebuilt_files.keys() - current_files.keys())
        mismatched = sorted(
            str(rel) for rel in current_files.keys() & rebuilt_files.keys()
            if current_files[rel] != rebuilt_files[rel]
        )

    passed = not missing and not extra and not mismatched
    detail = "normalized rebuild matches exactly" if passed else (
        f"missing={len(missing)} extra={len(extra)} mismatched={len(mismatched)}"
    )
    return CheckResult(
        name="deterministic_rebuild",
        passed=passed,
        detail=detail,
        data={"missing": missing[:10], "extra": extra[:10], "mismatched": mismatched[:10]},
    )


def prose_stripped_view(frontmatter: dict[str, Any], body: str) -> tuple[dict[str, Any], list[str]]:
    headings = HEADING_RE.findall(body)
    return frontmatter, headings


def body_functional(body: str, path: Path) -> bool:
    has_title = body.lstrip().startswith("# ")
    headings = HEADING_RE.findall(body)
    path_parts = set(path.parts)
    if "entries" in path_parts:
        return has_title and "Definition" in headings and "Provenance" in headings
    if "rius" in path_parts:
        return has_title and "Definition" in headings and "Provenance" in headings
    if "agents" in path_parts:
        return has_title and "Provenance" in headings
    if "indexes" in path_parts or path.name == "index.md":
        return has_title and len(body.strip()) > 40
    if "paths" in path_parts:
        return has_title and len(body.strip()) > 100
    return has_title and len(body.strip()) > 40


def frontmatter_functional(frontmatter: dict[str, Any], headings: list[str], path: Path) -> bool:
    if "paths" in path.parts:
        text = path.read_text(encoding="utf-8")
        _, body = strip_frontmatter(text)
        return body.lstrip().startswith("# ") and len(headings) >= 1
    file_type = frontmatter.get("type")
    if not file_type:
        return False
    if "DO_NOT_EDIT" not in frontmatter:
        return False
    if path.name != "index.md" and "indexes" not in path.parts and "paths" not in path.parts:
        if "related" not in frontmatter and file_type != "agent":
            return False
    if file_type == "knowledge_entry":
        return (
            "source_id" in frontmatter
            and "evidence_tier" in frontmatter
            and "handled_by" in frontmatter
            and "Definition" in headings
            and "Provenance" in headings
        )
    if file_type == "riu":
        return "source_id" in frontmatter and "handled_by" in frontmatter and "Definition" in headings and "Provenance" in headings
    if file_type == "agent":
        return "source_id" in frontmatter and "Provenance" in headings
    if file_type == "index":
        return "compiler_version" in frontmatter
    if file_type == "enablement_path":
        return "source_id" in frontmatter
    return True


def dual_experience_test(paths: list[Path]) -> CheckResult:
    failing_body = []
    failing_meta = []
    for path in paths:
        text = read_text(path)
        frontmatter, body = strip_frontmatter(text)
        if not body_functional(body, path):
            failing_body.append(repo_relative(path))
        meta, headings = prose_stripped_view(frontmatter, body)
        if not frontmatter_functional(meta, headings, path):
            failing_meta.append(repo_relative(path))

    passed = not failing_body and not failing_meta
    detail = "all pages pass frontmatter-stripped and prose-stripped heuristics" if passed else (
        f"body_failures={len(failing_body)} metadata_failures={len(failing_meta)}"
    )
    return CheckResult(
        name="dual_experience_test",
        passed=passed,
        detail=detail,
        data={"body_failures": failing_body[:20], "metadata_failures": failing_meta[:20]},
    )


def source_cross_check(wiki_dir: Path) -> CheckResult:
    """P2-09: Cross-check wiki counts against palette source data."""
    mismatches = []
    try:
        manifest = yaml.safe_load((PALETTE_ROOT / "MANIFEST.yaml").read_text())
        tax_path = PALETTE_ROOT / manifest["layers"]["taxonomy"]["path"]
        tax = yaml.safe_load(tax_path.read_text())
        expected_rius = len(tax.get("rius", []))

        kl_path = PALETTE_ROOT / manifest["layers"]["knowledge_library"]["path"]
        kl = yaml.safe_load(kl_path.read_text())
        expected_kl = sum(len(kl.get(s, [])) for s in ["library_questions", "gap_additions", "context_specific_questions"])

        expected_agents = len(manifest.get("agents", {}).get("list", []))

        actual_rius = len(list((wiki_dir / "rius").glob("*.md")))
        actual_kl = len(list((wiki_dir / "entries").glob("*.md")))
        actual_agents = len(list((wiki_dir / "agents").glob("*.md")))

        if actual_rius != expected_rius:
            mismatches.append(f"RIUs: wiki={actual_rius}, source={expected_rius}")
        if actual_kl != expected_kl:
            mismatches.append(f"KL: wiki={actual_kl}, source={expected_kl}")
        if actual_agents != expected_agents:
            mismatches.append(f"Agents: wiki={actual_agents}, source={expected_agents}")
    except Exception as e:
        mismatches.append(f"error loading source data: {e}")

    passed = not mismatches
    detail = "wiki counts match source data" if passed else f"{len(mismatches)} mismatches: {'; '.join(mismatches)}"
    return CheckResult(name="source_cross_check", passed=passed, detail=detail, data={"mismatches": mismatches})


def run_validation(wiki_dir: Path) -> ValidationReport:
    compiler_module = load_compiler_module()
    paths = iter_md_files(wiki_dir)

    checks = [
        orientation_test(wiki_dir, paths),
        coverage_check(wiki_dir, compiler_module),
        broken_backlinks_check(wiki_dir, paths),
        orphan_detection(wiki_dir, paths),
        adversarial_test(paths),
        deterministic_rebuild(compiler_module, wiki_dir),
        dual_experience_test(paths),
        source_cross_check(wiki_dir),
    ]
    passed = all(check.passed for check in checks)
    return ValidationReport(wiki_path=str(wiki_dir), passed=passed, checks=checks)


def print_report(report: ValidationReport) -> None:
    print(f"Wiki validation for {report.wiki_path}")
    print(f"Overall: {'PASS' if report.passed else 'FAIL'}")
    print("")
    for check in report.checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")
        if not check.passed and check.data:
            for key, value in check.data.items():
                if value:
                    print(f"  - {key}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the compiled Palette wiki.")
    parser.add_argument("--wiki", default=str(DEFAULT_WIKI), help="Path to compiled wiki directory")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki).expanduser().resolve()
    if not wiki_dir.exists():
        print(f"Wiki directory not found: {wiki_dir}", file=sys.stderr)
        return 1

    report = run_validation(wiki_dir)
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print_report(report)
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
