# Quickstart — Run Palette in 5 Minutes

Palette is on-premise AI that compounds your judgment. It classifies every question, retrieves from governed knowledge, and uses Perplexity only for public research — your client data never leaves your machine.

## Requirements

- Python 3.10+
- A Perplexity API key (for external research — optional, system works without it)

## Setup

```bash
# Clone
git clone https://github.com/pretendhome/palette.git
cd palette

# Install dependencies
pip install numpy httpx pyyaml

# (Optional) Set Perplexity API key for external research
export PERPLEXITY_API_KEY="your-key-here"
```

## Run Your First Query

```bash
# Local-only query (no external calls)
python3 scripts/palette_query.py "What are the key criteria for evaluating AI systems?"

# With external research (governed — PII stripped before any external call)
python3 scripts/palette_query.py --external "What are the Delaware precedents for breach of fiduciary duty?"

# Demo mode (color-coded output for presentations)
python3 scripts/palette_query.py --demo --external "What are the Delaware precedents for breach of fiduciary duty?"
```

## What Happens

1. **RESOLVE** — Palette classifies your question against 121 problem types
2. **RETRIEVE** — Searches local knowledge library (183 entries, evidence-tiered)
3. **SANITIZE** — If external research is needed, strips all client identifiers
4. **EXTERNAL** — Queries Perplexity for public knowledge only (or blocks if PII detected)
5. **STORE** — Logs the decision locally. Future queries connect to prior decisions.

## The Privacy Boundary

When you use `--external`, Palette's gateway:
- Detects PII (case numbers, party names, SSNs, dollar amounts, emails)
- Blocks client-specific queries entirely
- Only allows public legal research through to Perplexity
- Caches results locally to avoid repeated external calls
- Logs every decision in an audit trail

Try it:
```bash
# This will be BLOCKED (client-specific)
python3 scripts/palette_query.py --demo --external "Should we advise Smith Corp to settle for \$2.5M?"

# This will go through (public legal research)
python3 scripts/palette_query.py --demo --external "What are the filing procedures for Delaware Chancery Court?"
```

## Run Tests

```bash
# Full system tests (49 tests)
python3 scripts/test_v3.py

# Gateway + sanitization tests (12 tests)
python3 -m unittest bdb/gateway/tests/test_gateway.py
```

## Architecture

```
Your question
    → Local retrieval (FTS5 + vector + keyword)
    → Classification (121 RIUs)
    → Governance check (ONE-WAY/TWO-WAY door)
    → If external needed: Sanitize → Perplexity → Sanitize response → Cache
    → Store decision locally
    → Connect to prior decisions (compounding)
```

Everything runs on your machine. Perplexity is used only as a controlled window to public knowledge.

## Learn More

- [Product thesis](docs/product/PALETTE_MOAT_ITERATIONS_2026-05-16.md)
- [Gateway spec](bdb/GATEWAY_SPEC.md)
- [System identity](docs/PALETTE_IDENTITY.md)
