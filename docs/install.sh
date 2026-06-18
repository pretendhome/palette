#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Mission Canvas Installer                                        ║
# ║  Usage: curl -fsSL https://missioncanvas.ai/install.sh | bash    ║
# ║  Works on fresh Mac, Linux, or any system with curl + bash.      ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

G='\033[0;32m'; Y='\033[1;33m'; R='\033[0;31m'; B='\033[1m'; D='\033[0;90m'; NC='\033[0m'
ok()   { echo -e "  ${G}✓${NC} $1"; }
warn() { echo -e "  ${Y}⚠${NC} $1"; }
fail() { echo -e "  ${R}✗${NC} $1"; exit 1; }

echo ""
echo -e "${B}  ╔══════════════════════════════════╗${NC}"
echo -e "${B}  ║   Mission Canvas Installer       ║${NC}"
echo -e "${B}  ║   Governed AI for professionals  ║${NC}"
echo -e "${B}  ╚══════════════════════════════════╝${NC}"
echo ""

# ── Detect OS ──
OS="$(uname -s)"
case "$OS" in
  Linux*)  ok "Detected: Linux" ;;
  Darwin*) ok "Detected: macOS" ;;
  *)       fail "Unsupported OS: $OS" ;;
esac

# ── Helper: check if a command actually works (not just an xcode-select stub) ──
real_cmd() {
  command -v "$1" &>/dev/null && "$1" --version &>/dev/null 2>&1
}

# ── macOS fresh install: install Homebrew if needed ──
if [ "$OS" = "Darwin" ]; then
  # Check if python3 and git are real or just xcode-select stubs
  NEED_BREW=false
  if ! python3 -c 'import sys; print(sys.version_info.minor)' &>/dev/null 2>&1; then
    NEED_BREW=true
  fi
  if ! git --version &>/dev/null 2>&1; then
    NEED_BREW=true
  fi

  if [ "$NEED_BREW" = true ] && ! command -v brew &>/dev/null; then
    echo -e "\n${B}Fresh Mac detected — installing Homebrew (this gets you Python + Git)...${NC}"
    echo -e "${D}  Homebrew may ask for your password and take a few minutes.${NC}"
    echo ""
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add brew to PATH for this session (Apple Silicon vs Intel)
    if [ -f "/opt/homebrew/bin/brew" ]; then
      eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -f "/usr/local/bin/brew" ]; then
      eval "$(/usr/local/bin/brew shellenv)"
    fi
    ok "Homebrew installed"
  fi
fi

# ── Check dependencies ──
echo -e "\n${B}Checking dependencies...${NC}"

# Python
PYTHON_OK=false
if python3 -c 'import sys; exit(0 if sys.version_info >= (3,10) else 1)' &>/dev/null 2>&1; then
  ok "Python $(python3 --version 2>&1 | cut -d' ' -f2)"
  PYTHON_OK=true
else
  warn "Python 3.10+ not found — installing..."
  if command -v brew &>/dev/null; then
    brew install python@3.12 >/dev/null 2>&1 && ok "Python installed" && PYTHON_OK=true || warn "Could not install Python via Homebrew"
  elif command -v apt-get &>/dev/null; then
    sudo apt-get update -qq && sudo apt-get install -y -qq python3 python3-pip python3-venv >/dev/null 2>&1 && ok "Python installed" && PYTHON_OK=true || warn "Could not install Python"
  fi
  if [ "$PYTHON_OK" = false ]; then
    fail "Python 3.10+ required. Install from https://python.org"
  fi
fi

# Git
GIT_OK=false
if git --version &>/dev/null 2>&1; then
  ok "Git $(git --version 2>&1 | cut -d' ' -f3)"
  GIT_OK=true
else
  warn "Git not found — installing..."
  if command -v brew &>/dev/null; then
    brew install git >/dev/null 2>&1 && ok "Git installed" && GIT_OK=true || true
  elif command -v apt-get &>/dev/null; then
    sudo apt-get install -y -qq git >/dev/null 2>&1 && ok "Git installed" && GIT_OK=true || true
  fi
fi

# Node.js (optional — only needed for Voice Hub)
if node -v &>/dev/null 2>&1 && [ "$(node -v | sed 's/v//' | cut -d. -f1)" -ge 18 ]; then
  ok "Node.js $(node -v)"
else
  warn "Node.js 18+ not found — Voice Hub will be unavailable. Install later: https://nodejs.org"
fi

# ── Install location ──
INSTALL_DIR="${MISSION_CANVAS_HOME:-$HOME/.mission-canvas}"
echo -e "\n${B}Installing to ${INSTALL_DIR}...${NC}"

if [ -d "$INSTALL_DIR/.git" ] && [ "$GIT_OK" = true ]; then
  ok "Existing install found — updating..."
  (cd "$INSTALL_DIR" && git pull --quiet 2>/dev/null) || true
elif [ "$GIT_OK" = true ]; then
  git clone --quiet --depth 1 https://github.com/pretendhome/mission-canvas.git "$INSTALL_DIR"
else
  # No git available — download as tarball (curl is always available)
  warn "Git not available — downloading as archive..."
  mkdir -p "$INSTALL_DIR"
  curl -fsSL https://github.com/pretendhome/mission-canvas/archive/refs/heads/main.tar.gz | tar xz -C "$INSTALL_DIR" --strip-components=1
fi
ok "Repository ready"

# ── Python dependencies ──
echo -e "\n${B}Installing Python dependencies...${NC}"
cd "$INSTALL_DIR"
pip3 install --quiet pyyaml redis fastapi uvicorn websockets pytest 2>/dev/null || python3 -m pip install --quiet pyyaml redis fastapi uvicorn websockets pytest 2>/dev/null || warn "pip install failed — try: pip3 install pyyaml fastapi uvicorn"
ok "Python dependencies"

# ── Run setup if available ──
if [ -f "setup.sh" ]; then
  bash setup.sh "$@" 2>/dev/null || true
fi

# ── Verify ──
echo ""
if [ -f "src/mc_cli.py" ]; then
  python3 src/mc_cli.py health 2>/dev/null || true
fi

# ── Done ──
echo ""
echo -e "${B}  ╔══════════════════════════════════════════╗${NC}"
echo -e "${B}  ║     Installation complete                ║${NC}"
echo -e "${B}  ╠══════════════════════════════════════════╣${NC}"
echo -e "${B}  ║                                          ║${NC}"
echo -e "${B}  ║  Start the web UI:                       ║${NC}"
echo -e "${B}  ║    cd $INSTALL_DIR ${NC}"
echo -e "${B}  ║    python3 src/api_server.py              ║${NC}"
echo -e "${B}  ║    → http://localhost:7891                ║${NC}"
echo -e "${B}  ║                                          ║${NC}"
echo -e "${B}  ║  Or use the CLI:                         ║${NC}"
echo -e "${B}  ║    python3 src/mc_cli.py health           ║${NC}"
echo -e "${B}  ║    python3 src/mc_cli.py status           ║${NC}"
echo -e "${B}  ║                                          ║${NC}"
echo -e "${B}  ╚══════════════════════════════════════════╝${NC}"
echo ""
