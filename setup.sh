#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Mission Canvas — Setup                                         ║
# ║  From zero to running in 60 seconds.                            ║
# ║                                                                  ║
# ║  Usage:  bash setup.sh                                           ║
# ║          bash setup.sh --skip-keys    # non-interactive          ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKIP_KEYS="${1:-}"

# ── Colors ──
R='\033[0;31m'
G='\033[0;32m'
Y='\033[1;33m'
B='\033[0;34m'
DIM='\033[0;90m'
BOLD='\033[1m'
NC='\033[0m'

ok()   { echo -e "  ${G}✓${NC} $1"; }
warn() { echo -e "  ${Y}⚠${NC} $1"; }
fail() { echo -e "  ${R}✗${NC} $1"; }
info() { echo -e "  ${DIM}$1${NC}"; }

# ── Header ──
echo ""
echo -e "${BOLD}mission canvas${NC}"
echo -e "${DIM}Your judgment compounds here.${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ════════════════════════════════════════════════════════════════════
# 1. Check dependencies
# ════════════════════════════════════════════════════════════════════
echo -e "${BOLD}Checking dependencies...${NC}"
ERRORS=0

# Python
if command -v python3 &>/dev/null; then
  PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
  PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
  if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
    ok "Python $PY_VER"
  else
    fail "Python $PY_VER (need 3.10+)"
    ERRORS=$((ERRORS + 1))
  fi
else
  fail "Python not found (need 3.10+)"
  ERRORS=$((ERRORS + 1))
fi

# Node.js
if command -v node &>/dev/null; then
  NODE_VER=$(node -v | sed 's/v//')
  NODE_MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 18 ]; then
    ok "Node.js $NODE_VER"
  else
    fail "Node.js $NODE_VER (need 18+)"
    ERRORS=$((ERRORS + 1))
  fi
else
  fail "Node.js not found (need 18+)"
  info "Install: https://nodejs.org or 'nvm install 20'"
  ERRORS=$((ERRORS + 1))
fi

# npm
if command -v npm &>/dev/null; then
  ok "npm $(npm -v)"
else
  fail "npm not found"
  ERRORS=$((ERRORS + 1))
fi

# Ollama (optional — auto-install if missing)
if command -v ollama &>/dev/null; then
  ok "Ollama (local models available)"
else
  echo -e "  ${Y}?${NC} Ollama not found — install for fully local AI? (recommended)"
  read -rp "    Install Ollama? [Y/n]: " INSTALL_OLLAMA
  if [ "${INSTALL_OLLAMA:-Y}" != "n" ] && [ "${INSTALL_OLLAMA:-Y}" != "N" ]; then
    curl -fsSL https://ollama.com/install.sh | sh 2>/dev/null && ok "Ollama installed" || warn "Ollama install failed — continuing without it"
    if command -v ollama &>/dev/null; then
      info "Pulling small local model (qwen2.5:3b)..."
      ollama pull qwen2.5:3b 2>/dev/null && ok "Local model ready" || warn "Model pull failed — you can run 'ollama pull qwen2.5:3b' later"
    fi
  else
    info "Skipped — PROTECT intent will use external models"
  fi
fi

# uv (optional, speeds up Python)
if command -v uv &>/dev/null; then
  ok "uv $(uv --version 2>/dev/null | head -1)"
  PIP_CMD="uv pip install"
else
  PIP_CMD="pip install"
fi

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  fail "Fix $ERRORS missing dependencies and re-run."
  exit 1
fi

echo ""

# ════════════════════════════════════════════════════════════════════
# 2. Install Python dependencies
# ════════════════════════════════════════════════════════════════════
echo -e "${BOLD}Installing Python packages...${NC}"
$PIP_CMD -q httpx pyyaml ruamel.yaml numpy anthropic 2>/dev/null && ok "Core packages" || warn "Some packages may need manual install"

echo ""

# ════════════════════════════════════════════════════════════════════
# 3. Install Node dependencies
# ════════════════════════════════════════════════════════════════════
echo -e "${BOLD}Installing Node packages...${NC}"

if [ -f "$SCRIPT_DIR/peers/package.json" ]; then
  (cd "$SCRIPT_DIR/peers" && npm install --silent 2>/dev/null) && ok "Peers bus" || warn "Peers install had warnings"
fi

if [ -f "$SCRIPT_DIR/peers/hub/package.json" ]; then
  (cd "$SCRIPT_DIR/peers/hub" && npm install --silent 2>/dev/null) && ok "Voice Hub" || warn "Hub install had warnings"
else
  ok "Voice Hub (uses peers/ dependencies)"
fi

if [ -f "$SCRIPT_DIR/mission-canvas/package.json" ]; then
  (cd "$SCRIPT_DIR/mission-canvas" && npm install --silent 2>/dev/null) && ok "Mission Canvas" || warn "MC install had warnings"
fi

echo ""

# ════════════════════════════════════════════════════════════════════
# 4. API Key Setup (interactive)
# ════════════════════════════════════════════════════════════════════
ENV_FILE="$SCRIPT_DIR/peers/hub/.env"

if [ "$SKIP_KEYS" = "--skip-keys" ]; then
  warn "Skipping API key setup (--skip-keys)"
elif [ -f "$ENV_FILE" ]; then
  ok "API keys already configured ($ENV_FILE)"
  info "Edit $ENV_FILE to update keys"
else
  echo -e "${BOLD}API Keys${NC} ${DIM}(all optional — press Enter to skip)${NC}"
  echo ""

  KEYS=""

  read -rp "  Perplexity API key (for external research): " PPLX_KEY
  if [ -n "$PPLX_KEY" ]; then
    KEYS="${KEYS}PERPLEXITY_API_KEY=$PPLX_KEY\n"
    ok "Perplexity key set"
  else
    info "Skipped — system works locally without it"
  fi

  read -rp "  Rime API key (for voice/TTS — optional): " RIME_KEY
  if [ -n "$RIME_KEY" ]; then
    KEYS="${KEYS}RIME_API_KEY=$RIME_KEY\n"
    ok "Rime key set"
  else
    info "Skipped — text-only mode"
  fi

  read -rp "  Groq API key (free local-quality models — optional): " GROQ_KEY
  if [ -n "$GROQ_KEY" ]; then
    KEYS="${KEYS}GROQ_API_KEY=$GROQ_KEY\n"
    ok "Groq key set"
  else
    info "Skipped — get free key at console.groq.com"
  fi

  if [ -n "$KEYS" ]; then
    echo -e "$KEYS" > "$ENV_FILE"
    ok "Keys written to $ENV_FILE"
  else
    touch "$ENV_FILE"
    warn "No keys set — system runs in local-only mode"
  fi

  echo ""
fi

# ════════════════════════════════════════════════════════════════════
# 5. Create default directories + PATH
# ════════════════════════════════════════════════════════════════════
mkdir -p "$SCRIPT_DIR/.palette/artifacts"
mkdir -p "$SCRIPT_DIR/.palette/schedules"
mkdir -p "$SCRIPT_DIR/.palette/lenses"
ok "Workspace directories ready"

# Add palette to PATH
mkdir -p "$HOME/.local/bin"
ln -sf "$SCRIPT_DIR/scripts/palette_intents/palette" "$HOME/.local/bin/palette" 2>/dev/null || true
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc" 2>/dev/null || true
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
  export PATH="$HOME/.local/bin:$PATH"
  ok "Added palette to PATH (restart shell or: source ~/.bashrc)"
else
  ok "PATH configured"
fi

echo ""

# ════════════════════════════════════════════════════════════════════
# 6. Start services
# ════════════════════════════════════════════════════════════════════
echo -e "${BOLD}Starting Mission Canvas...${NC}"

# Kill any existing instances
pkill -f "node.*broker/index" 2>/dev/null || true
pkill -f "node.*hub/server" 2>/dev/null || true
sleep 0.5

# Start peers broker
if [ -f "$SCRIPT_DIR/peers/broker/index.mjs" ]; then
  (cd "$SCRIPT_DIR/peers/broker" && node index.mjs > /tmp/mc-broker.log 2>&1 &)
  sleep 1
  if curl -s http://127.0.0.1:7899/health >/dev/null 2>&1; then
    ok "Peers bus (port 7899)"
  else
    warn "Peers bus may not have started — check /tmp/mc-broker.log"
  fi
fi

# Start Voice Hub
if [ -f "$SCRIPT_DIR/peers/hub/server.mjs" ]; then
  (cd "$SCRIPT_DIR/peers/hub" && node server.mjs > /tmp/mc-hub.log 2>&1 &)
  sleep 2
  if curl -s http://localhost:7890/ >/dev/null 2>&1; then
    ok "Voice Hub (port 7890)"
  else
    warn "Voice Hub may be starting — check /tmp/mc-hub.log"
  fi
fi

echo ""

# ════════════════════════════════════════════════════════════════════
# 7. Done
# ════════════════════════════════════════════════════════════════════
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BOLD}Mission Canvas is running.${NC}"
echo ""
echo -e "  ${G}Open:${NC}  http://localhost:7890"
echo ""
echo -e "  ${DIM}Voice Hub:${NC}    http://localhost:7890"
echo -e "  ${DIM}Peers Bus:${NC}    http://localhost:7899"
echo -e "  ${DIM}Logs:${NC}         /tmp/mc-broker.log, /tmp/mc-hub.log"
echo ""
echo -e "  ${DIM}CLI:${NC}          palette query \"your question\""
echo -e "  ${DIM}Intents:${NC}      palette protect | research | decide | create | diagnose | reflect"
echo -e "  ${DIM}Demo:${NC}         palette demo sarah"
echo ""
echo -e "  ${DIM}Stop:${NC}         pkill -f 'node.*server.mjs'; pkill -f 'node.*index.mjs'"
echo ""
echo -e "${DIM}Your judgment compounds here.${NC}"
echo ""

# Open browser (unless running non-interactively)
if [ -t 0 ]; then
  if command -v xdg-open &>/dev/null; then
    xdg-open "http://localhost:7890" 2>/dev/null &
  elif command -v open &>/dev/null; then
    open "http://localhost:7890" 2>/dev/null &
  fi
fi
