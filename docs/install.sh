#!/bin/sh
# Mission Canvas — One Command Install
# Usage: curl -fsSL https://missioncanvas.ai/install.sh | sh
# Works on any Mac, Linux, or WSL with curl. No Python. No Git. No dependencies.
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

# Get latest release version
VERSION=$(curl -fsSL https://api.github.com/repos/pretendhome/mission-canvas/releases/latest 2>/dev/null | grep '"tag_name"' | cut -d'"' -f4)
if [ -z "$VERSION" ]; then
  VERSION="v1.2.0"  # Fallback to known version
fi
echo "  ✓ Version: $VERSION"

# Download binary
BINARY="mc-${PLATFORM}-${ARCH}"
URL="https://github.com/pretendhome/mission-canvas/releases/download/${VERSION}/${BINARY}"
echo "  → Downloading Mission Canvas..."

TMPFILE=$(mktemp)
if ! curl -fsSL "$URL" -o "$TMPFILE" 2>/dev/null; then
  echo "  ✗ Download failed. URL: $URL"
  echo "  Try: https://github.com/pretendhome/mission-canvas/releases"
  rm -f "$TMPFILE"
  exit 1
fi
chmod +x "$TMPFILE"

# Install to PATH
INSTALL_DIR=""
for dir in "$HOME/.local/bin" "/usr/local/bin"; do
  if [ -d "$dir" ] && [ -w "$dir" ]; then
    INSTALL_DIR="$dir"
    break
  fi
done

if [ -z "$INSTALL_DIR" ]; then
  INSTALL_DIR="$HOME/.local/bin"
  mkdir -p "$INSTALL_DIR"
fi

mv "$TMPFILE" "$INSTALL_DIR/mc"
echo "  ✓ Installed to $INSTALL_DIR/mc"

# Check if in PATH
case ":$PATH:" in
  *":$INSTALL_DIR:"*) ;;
  *)
    echo ""
    echo "  Add to your PATH:"
    echo "    export PATH=\"$INSTALL_DIR:\$PATH\""
    echo "  Or add to ~/.bashrc / ~/.zshrc for permanent access."
    ;;
esac

# Verify
echo ""
"$INSTALL_DIR/mc" status 2>/dev/null || true

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   Installation complete!                 ║"
echo "  ╠══════════════════════════════════════════╣"
echo "  ║                                          ║"
echo "  ║   Start:    mc shell                     ║"
echo "  ║   Web UI:   mc start                     ║"
echo "  ║   Status:   mc status                    ║"
echo "  ║                                          ║"
echo "  ║   Requires: Ollama (ollama.com/download)  ║"
echo "  ║   Then:     ollama pull qwen2.5:7b       ║"
echo "  ║                                          ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""
