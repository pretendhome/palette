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

command -v python3 &>/dev/null && ok "Python $(python3 --version 2>&1 | cut -d' ' -f2)" || { warn "Python 3.10+ required"; MISSING=1; }
command -v node &>/dev/null && ok "Node.js $(node -v)" || { warn "Node.js 18+ required"; MISSING=1; }
command -v git &>/dev/null && ok "Git $(git --version | cut -d' ' -f3)" || { fail "Git is required"; }

if [ "$MISSING" -gt 0 ]; then
  echo ""
  echo -e "  ${Y}Install missing deps first:${NC}"
  echo "    Python: https://python.org or 'sudo apt install python3'"
  echo "    Node:   https://nodejs.org or 'nvm install 20'"
  exit 1
fi

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
