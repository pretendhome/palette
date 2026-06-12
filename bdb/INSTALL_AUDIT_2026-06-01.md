# Install Audit — Cold Start Report
**Date**: 2026-06-01
**Author**: claude.analysis
**Purpose**: What happens when a BDB judge runs `git clone && bash setup.sh` on a fresh machine

---

## What Claude Fixed

1. **LICENSE**: Switched from Apache 2.0 → MIT (matches Hermes, simpler, more permissive)
2. **README badge**: Updated license badge from Apache to MIT

---

## BLOCKERS — Setup Exits Immediately

| # | Problem | Where | Impact |
|---|---------|-------|--------|
| 1 | **Python 3.10+ missing** | setup.sh line 43-56 | Script exits. Does NOT auto-install. |
| 2 | **Node.js 18+ missing** | setup.sh line 58-72 | Script exits. Does NOT auto-install. |
| 3 | **npm missing** | setup.sh line 74-80 | Script exits. Comes with Node but checked separately. |

**Hermes handles this**: Their installer auto-installs Python 3.11 via uv. We don't.

---

## RUNTIME FAILURES — Setup Completes But Commands Break

| # | Problem | Where | Impact |
|---|---------|-------|--------|
| 4 | **Ollama not installed** | demo.py calls localhost:11434 | `palette demo sarah` Moment 1 fails (no local model) |
| 5 | **`anthropic` package not installed** | pyproject.toml declares it, setup.sh doesn't install it | Any code importing `anthropic` throws ModuleNotFoundError |
| 6 | **No C++ build tools** | `better-sqlite3` npm package | npm install may fail on fresh Ubuntu without `build-essential` or macOS without `xcode-select` |
| 7 | **No Perplexity API key** | orchestrate.py, research.py | Demo Moments 2 and 3 fail (no external research) |
| 8 | **`palette` not on PATH** | setup.sh doesn't add to PATH | Must run `./palette` from repo dir, not `palette` from anywhere |

---

## GRACEFUL DEGRADATION — Works But Limited

| # | Problem | Impact |
|---|---------|--------|
| 9 | No Rime key | Voice/TTS disabled, text-only works |
| 10 | No Groq key | Falls back to Ollama (if installed) |
| 11 | No `uv` | Falls back to pip (slower, works) |
| 12 | No `xdg-open`/`open` | Browser doesn't auto-open (services still run) |

---

## Full Dependency Tree

### System Dependencies (must be pre-installed)
```
python3 >= 3.10
node >= 18
npm (ships with node)
C++ compiler (for better-sqlite3):
  Ubuntu: apt-get install build-essential python3-dev
  macOS: xcode-select --install
```

### Python Packages (installed by setup.sh line 110)
```
httpx          → HTTP client for external APIs
pyyaml         → YAML parsing (taxonomy, knowledge library)
ruamel.yaml    → YAML with comment preservation
numpy          → Vector operations in palette_retrieve.py
```

### Python Packages MISSING from setup.sh
```
anthropic      → Declared in pyproject.toml but NOT installed by setup.sh
```

### Node Packages (installed by npm install)
```
better-sqlite3 → Broker database (requires C++ build for some platforms)
@modelcontextprotocol/sdk → MCP protocol
ajv            → JSON schema validation
js-yaml        → YAML parsing in Node
```

### API Keys (optional, prompted during setup)
```
PERPLEXITY_API_KEY → Research/decide/demo (sonar-pro, reasoning-pro)
RIME_API_KEY       → Voice TTS (Coda model, 236 voices)
GROQ_API_KEY       → Fast inference fallback (llama-3.3-70b)
```

### Runtime Services (started by setup.sh)
```
Port 7899 → Peers Broker (message bus, SQLite backend)
Port 7890 → Voice Hub (web UI, SSE streaming, TTS proxy)
Port 11434 → Ollama (if installed, local model inference)
```

### Files Created
```
.palette/artifacts/    → Gate decisions, evidence briefs, decision records
.palette/schedules/    → Cron job definitions
.palette/lenses/       → Persona/role definitions
peers/hub/.env         → API keys
~/.palette-peers.db    → Broker SQLite database
/tmp/mc-broker.log     → Broker logs
/tmp/mc-hub.log        → Hub logs
```

---

## Recommended Fixes (by effort)

### 5 Minutes — Do Before Submission
- [ ] Add `anthropic` to pip install line in setup.sh
- [ ] Add PATH: symlink `palette` to `~/.local/bin/` or export PATH

### 15 Minutes — Ideal for Judge Experience
- [ ] Auto-install Ollama if missing: `curl -fsSL https://ollama.com/install.sh | sh && ollama pull qwen2.5:3b`
- [ ] Check for build-essential/xcode-select before npm install
- [ ] Auto-install Python/Node if missing (detect OS, use apt/brew)

### Not Needed for BDB
- [ ] One-line curl installer (like Hermes)
- [ ] `palette update` command

---

## vs Hermes Install Comparison

| Step | Hermes | Mission Canvas | Gap |
|---|---|---|---|
| Pre-reqs | None — installs everything | Python 3.10+, Node 18+, npm | **Major** |
| Install | `curl ... \| bash` (1 line) | `git clone && bash setup.sh` (2 lines) | Minor |
| Auto-installs runtime | Yes (Python 3.11 via uv) | No — checks and exits | **Major** |
| Local model | Downloads via wizard | Optional, not installed | **Gap** |
| CLI on PATH | Yes (`hermes` anywhere) | No (`./palette` from repo only) | **Gap** |
| Update command | `hermes update` | None | Minor |
| Time to first query | ~3 minutes | ~2 minutes (if deps exist) | Equivalent |

---

## Test Sequence for Judges

### Minimal (no external APIs needed):
```bash
git clone https://github.com/pretendhome/palette.git
cd palette
bash setup.sh --skip-keys
./palette protect "Is this query safe for external research?"
```

### Full demo (requires Perplexity key + Ollama):
```bash
git clone https://github.com/pretendhome/palette.git
cd palette
bash setup.sh
# Enter Perplexity API key when prompted
./palette demo sarah
```

### Web UI:
```bash
# After setup.sh completes:
open http://localhost:7890
```

---

*Report by claude.analysis. 2026-06-01.*
