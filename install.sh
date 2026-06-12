#!/usr/bin/env bash
# ┌──────────────────────────────────────────┐
# │  Mission Canvas — One-Line Installer      │
# │                                            │
# │  curl -fsSL https://raw.githubusercontent.com/pretendhome/palette/main/install.sh | bash
# └──────────────────────────────────────────┘
set -euo pipefail

INSTALL_DIR="${MISSION_CANVAS_DIR:-$HOME/.mission-canvas}"

echo ""
echo -e "\033[1m┌──────────────────────────────────────────┐\033[0m"
echo -e "\033[1m│  Mission Canvas Installer                │\033[0m"
echo -e "\033[1m│  The governed agent OS for professionals  │\033[0m"
echo -e "\033[1m└──────────────────────────────────────────┘\033[0m"
echo ""

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
  echo "  → Updating existing installation..."
  (cd "$INSTALL_DIR" && git pull --quiet origin main 2>/dev/null) && echo -e "  \033[32m✓\033[0m Updated" || echo -e "  \033[33m⚠\033[0m Update failed — continuing with existing"
else
  echo "  → Cloning Mission Canvas..."
  git clone --quiet https://github.com/pretendhome/palette.git "$INSTALL_DIR" && echo -e "  \033[32m✓\033[0m Cloned to $INSTALL_DIR" || { echo -e "  \033[31m✗\033[0m Clone failed"; exit 1; }
fi

# Run setup
cd "$INSTALL_DIR"
exec bash setup.sh "$@"
