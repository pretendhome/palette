# Quickstart — Run Mission Canvas in 60 Seconds

Mission Canvas is local-first AI that compounds your professional judgment. It classifies every question, retrieves from governed knowledge, and uses Perplexity only for public research—ensuring client data never leaves your machine.

## One-Command Setup

```bash
curl -fsSL https://missioncanvas.ai/install.sh | bash
```

One command. Running locally. No cloud account required. No portal. Your keys, your machine.

**Requires**: macOS 12+ or Linux · Node.js 18+ · Python 3.10+ · Ollama (optional)

---

## Run Your First Query

```bash
# Local-only query (zero data leakage)
palette protect "What are the key criteria for evaluating fiduciary risk?"

# With governed external research
palette research "What are the Delaware precedents for breach of fiduciary duty?"

# Demo mode (3-moment legal story)
palette demo sarah
```

## What Happens Under the Hood

1.  **RESOLVE**: Palette classifies your question against **131 capability areas** (nodes).
2.  **RETRIEVE**: Searches the local knowledge library (**203 entries**, evidence-tiered).
3.  **SANITIZE**: If external research is needed, all client identifiers are stripped at the gate.
4.  **EXTERNAL**: Queries Perplexity for public knowledge only (or blocks if strategy detected).
5.  **STORE**: Logs the decision locally. Future queries **[CONNECT]** to prior work.

## Run Tests

Mission Canvas is built for reliability.

```bash
# Gateway + sanitization tests (12 tests)
python3 -m unittest bdb/gateway/tests/test_gateway.py

# Full PIS integration tests
python3 scripts/test_v3.py
```

## The 6 Governed Intents

```bash
palette protect   # Safety gate — blocks PII and strategy language.
palette research  # Evidence — sanitizes queries for safe external search.
palette decide    # Judgment — connects prior work and flags one-way doors.
palette create    # Documentation — generates artifacts with full provenance.
palette diagnose  # Recovery — captures failure patterns as reusable lessons.
palette reflect   # Audit — proposes improvements to the local knowledge base.
```

---

<div align="center">

*Your judgment compounds here. Never elsewhere.*

[Architecture](CLAUDE.md) · [missioncanvas.ai](https://missioncanvas.ai)

</div>
