#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${1:-}"
MODE="${2:-}"  # --voice or empty (web)

# ── Usage ──
if [ -z "$WORKSPACE" ]; then
  echo "Usage: ./start.sh <workspace-id> [--voice]"
  echo ""
  echo "  ./start.sh rossi          # Web UI at http://localhost:8787/rossi"
  echo "  ./start.sh oil-investor --voice  # CLI voice bridge"
  echo ""
  # List available workspaces
  if [ -d "$SCRIPT_DIR/workspaces" ]; then
    echo "Available workspaces:"
    for d in "$SCRIPT_DIR"/workspaces/*/; do
      [ -d "$d" ] && echo "  - $(basename "$d")"
    done
  fi
  exit 1
fi

# ── Validate workspace exists ──
if [ ! -d "$SCRIPT_DIR/workspaces/$WORKSPACE" ]; then
  echo "Error: workspace '$WORKSPACE' not found in $SCRIPT_DIR/workspaces/"
  exit 1
fi

# ── Dependency check ──
MISSING=()
command -v node >/dev/null 2>&1 || MISSING+=("node")

if [ "$MODE" = "--voice" ]; then
  command -v arecord >/dev/null 2>&1 || command -v sox >/dev/null 2>&1 || MISSING+=("arecord or sox (audio recording)")
  command -v whisper >/dev/null 2>&1 || echo "⚠  whisper not found — voice will fall back to text input"
fi

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "Missing required dependencies:"
  for m in "${MISSING[@]}"; do echo "  ✗ $m"; done
  exit 1
fi

PORT="${MISSIONCANVAS_PORT:-8787}"

# ── Launch ──
if [ "$MODE" = "--voice" ]; then
  # Voice mode: start server if not already running, then launch voice bridge
  SERVER_PID=""
  if curl -s "http://localhost:$PORT/v1/missioncanvas/workspace-welcome" \
    -X POST -H 'Content-Type: application/json' \
    -d "{\"workspace_id\":\"$WORKSPACE\"}" >/dev/null 2>&1; then
    echo "Server already running on port $PORT."
  else
    echo "Starting MissionCanvas server on port $PORT..."
    node "$SCRIPT_DIR/server.mjs" &
    SERVER_PID=$!
    trap "kill $SERVER_PID 2>/dev/null" EXIT
    for i in $(seq 1 20); do
      if curl -s "http://localhost:$PORT/v1/missioncanvas/workspace-welcome" \
        -X POST -H 'Content-Type: application/json' \
        -d "{\"workspace_id\":\"$WORKSPACE\"}" >/dev/null 2>&1; then
        break
      fi
      sleep 0.25
    done
  fi

  echo "Launching voice bridge for workspace: $WORKSPACE"
  exec node "$SCRIPT_DIR/terminal_voice_bridge.mjs" "$WORKSPACE"
else
  # Web mode: start server, print URL
  echo "Starting MissionCanvas for workspace: $WORKSPACE"
  echo "Open: http://localhost:$PORT/$WORKSPACE"
  echo ""
  exec node "$SCRIPT_DIR/server.mjs"
fi
