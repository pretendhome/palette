#!/usr/bin/env bash
# palette-push: Push to both repos (monorepo + palette subtree)
# Usage: palette-push "commit message"
set -euo pipefail

MSG="${1:-$(git log --oneline -1 | cut -d' ' -f2-)}"
PALETTE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PALETTE_DIR"

echo "Pushing to origin (pretendhome)..."
git push origin main

echo "Syncing to palette repo (GitHub Pages)..."
# Copy key files to the palette clone if it exists
if [ -d /tmp/palette-fix ]; then
  cp docs/index.html /tmp/palette-fix/docs/index.html 2>/dev/null || true
  cp docs/install.sh /tmp/palette-fix/docs/install.sh 2>/dev/null || true
  cp setup.sh /tmp/palette-fix/setup.sh 2>/dev/null || true
  cd /tmp/palette-fix
  git add -A
  git diff --cached --quiet || git commit -m "$MSG"
  git push origin main
  echo "✓ Both repos pushed"
else
  echo "⚠ /tmp/palette-fix not found — push to palette repo manually"
  echo "  cd /tmp && git clone --depth 1 git@github.com:pretendhome/palette.git palette-fix"
fi
