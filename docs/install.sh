#!/bin/sh
# Mission Canvas — One Command Install
# Usage: curl -fsSL https://missioncanvas.ai/install.sh | sh
# Tries binary first, falls back to source install if no release exists.
set -e

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   Mission Canvas Installer               ║"
echo "  ║   Governed AI for professionals          ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$ARCH" in
  x86_64|amd64) ARCH="x86_64" ;;
  arm64|aarch64) ARCH="arm64" ;;
  *) echo "  ✗ Unsupported architecture: $ARCH"; exit 1 ;;
esac

case "$OS" in
  darwin) PLATFORM="darwin" ;;
  linux) PLATFORM="linux" ;;
  *) echo "  ✗ Unsupported OS: $OS (use PowerShell on Windows)"; exit 1 ;;
esac

echo "  ✓ Detected: ${PLATFORM}-${ARCH}"

# ── Try binary install first ──
BINARY="mc-${PLATFORM}-${ARCH}"
VERSION=$(curl -fsSL https://api.github.com/repos/pretendhome/mission-canvas/releases/latest 2>/dev/null | grep '"tag_name"' | cut -d'"' -f4 || echo "")

if [ -n "$VERSION" ]; then
  URL="https://github.com/pretendhome/mission-canvas/releases/download/${VERSION}/${BINARY}"
  echo "  → Downloading binary (${VERSION})..."
  TMPFILE=$(mktemp)
  if curl -fsSL "$URL" -o "$TMPFILE" 2>/dev/null; then
    chmod +x "$TMPFILE"
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    mv "$TMPFILE" "$INSTALL_DIR/mc"
    echo "  ✓ Installed mc to $INSTALL_DIR/mc"
    case ":$PATH:" in
      *":$INSTALL_DIR:"*) ;;
      *) echo "  Add to PATH: export PATH=\"$INSTALL_DIR:\$PATH\"" ;;
    esac
    echo ""
    echo "  ╔══════════════════════════════════════════╗"
    echo "  ║   Installation complete!                 ║"
    echo "  ║   Run: mc shell                          ║"
    echo "  ║   Web: mc start → http://localhost:7891  ║"
    echo "  ║   Requires: Ollama (ollama.com/download) ║"
    echo "  ╚══════════════════════════════════════════╝"
    echo ""
    exit 0
  fi
  rm -f "$TMPFILE"
  echo "  ⚠ Binary not available — falling back to source install"
fi

# ── Source install (fallback) ──
echo "  → Installing from source..."

# Check Python
if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
  echo "  ✗ Python 3.10+ required. Install from https://python.org"
  echo "    Or: brew install python@3.12 (macOS)"
  exit 1
fi
echo "  ✓ Python $(python3 --version 2>&1 | cut -d' ' -f2)"

# Check Git
if ! git --version >/dev/null 2>&1; then
  echo "  ✗ Git required."
  echo "    macOS: xcode-select --install"
  echo "    Linux: sudo apt install git"
  exit 1
fi
echo "  ✓ Git"

# Clone or update
INSTALL_DIR="${HOME}/.mission-canvas"
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "  → Updating existing install..."
  (cd "$INSTALL_DIR" && git pull --quiet 2>/dev/null) || true
else
  echo "  → Cloning Mission Canvas..."
  git clone --quiet --depth 1 https://github.com/pretendhome/mission-canvas.git "$INSTALL_DIR"
fi
echo "  ✓ Source ready"

# Install Python deps
echo "  → Installing dependencies..."
cd "$INSTALL_DIR"
pip3 install --quiet pyyaml redis fastapi uvicorn websockets pytest httpx 2>/dev/null || \
  python3 -m pip install --quiet pyyaml redis fastapi uvicorn websockets pytest httpx 2>/dev/null || \
  echo "  ⚠ pip install failed — try: pip3 install pyyaml fastapi uvicorn httpx"
echo "  ✓ Dependencies"

# Make mc command available
if [ -f "$INSTALL_DIR/mc" ]; then
  mkdir -p "$HOME/.local/bin"
  ln -sf "$INSTALL_DIR/mc" "$HOME/.local/bin/mc" 2>/dev/null || true
fi

# Verify
echo ""
python3 "$INSTALL_DIR/src/mc_cli.py" status 2>/dev/null || echo "  (Run 'mc status' to verify)"

# Auto-start web server
echo ""
echo "  → Starting Mission Canvas web UI..."
cd "$INSTALL_DIR"
python3 src/api_server.py &
MC_PID=$!
sleep 2

# Open browser
if [ "$(uname -s)" = "Darwin" ]; then
  open "http://localhost:7891" 2>/dev/null
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "http://localhost:7891" 2>/dev/null
fi

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   Mission Canvas is running!             ║"
echo "  ╠══════════════════════════════════════════╣"
echo "  ║                                          ║"
echo "  ║  → http://localhost:7891 (open in browser)"
echo "  ║                                          ║"
echo "  ║  Stop:  kill $MC_PID                     ║"
echo "  ║  Restart: cd $INSTALL_DIR"
echo "  ║           python3 src/api_server.py      ║"
echo "  ║                                          ║"
echo "  ║  Requires: Ollama (ollama.com/download)  ║"
echo "  ║  Then: ollama pull qwen2.5:7b            ║"
echo "  ║                                          ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""
