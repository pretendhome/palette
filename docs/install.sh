#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Mission Canvas Installer                                        ║
# ║  Usage: curl -fsSL https://missioncanvas.ai/install.sh | bash    ║
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

# ── Check dependencies ──
echo -e "\n${B}Checking dependencies...${NC}"
MISSING=0

# Python
if ! command -v python3 &>/dev/null || [ "$(python3 -c 'import sys;print(sys.version_info.minor)')" -lt 10 ]; then
  warn "Python 3.10+ not found — installing..."
  if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq && sudo apt-get install -y -qq python3 python3-pip python3-venv >/dev/null 2>&1 && ok "Python installed" || { fail "Could not install Python"; }
  elif command -v brew &>/dev/null; then
    brew install python@3.12 >/dev/null 2>&1 && ok "Python installed" || { fail "Could not install Python"; }
  else
    fail "Install Python 3.10+ manually: https://python.org"
  fi
else
  ok "Python $(python3 --version 2>&1 | cut -d' ' -f2)"
fi

# Node.js
if ! command -v node &>/dev/null || [ "$(node -v | sed 's/v//' | cut -d. -f1)" -lt 18 ]; then
  warn "Node.js 18+ not found — installing..."
  if command -v apt-get &>/dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - >/dev/null 2>&1 && sudo apt-get install -y -qq nodejs >/dev/null 2>&1 && ok "Node.js installed" || { fail "Could not install Node.js"; }
  elif command -v brew &>/dev/null; then
    brew install node@20 >/dev/null 2>&1 && ok "Node.js installed" || { fail "Could not install Node.js"; }
  else
    fail "Install Node.js 18+: https://nodejs.org"
  fi
else
  ok "Node.js $(node -v)"
fi

# Build tools (for better-sqlite3)
if command -v apt-get &>/dev/null && ! dpkg -s build-essential &>/dev/null 2>&1; then
  warn "Installing build tools..."
  sudo apt-get install -y -qq build-essential python3-dev >/dev/null 2>&1 && ok "Build tools" || warn "Build tools install failed — npm may have issues"
elif command -v xcode-select &>/dev/null && ! xcode-select -p &>/dev/null 2>&1; then
  warn "Installing Xcode CLI tools..."
  xcode-select --install 2>/dev/null || true
fi

command -v git &>/dev/null && ok "Git $(git --version | cut -d' ' -f3)" || { fail "Git is required"; }

# ── Install location ──
INSTALL_DIR="${MISSION_CANVAS_HOME:-$HOME/.mission-canvas}"
echo -e "\n${B}Installing to ${INSTALL_DIR}...${NC}"

if [ -d "$INSTALL_DIR/.git" ]; then
  ok "Existing install found — updating..."
  (cd "$INSTALL_DIR" && git pull --quiet)
else
  git clone --quiet --depth 1 https://github.com/pretendhome/palette.git "$INSTALL_DIR"
fi
ok "Repository ready"

# ── Run setup ──
echo ""
cd "$INSTALL_DIR"
bash setup.sh "$@"
