#!/bin/bash
# Palette Peers — Inbox check hook for Claude Code
# Runs on every user prompt submission. Checks for pending messages
# addressed to claude.analysis or broadcast to all.

BROKER="http://127.0.0.1:7899"

# Quick health check — bail silently if broker is down
curl -sf "$BROKER/health" >/dev/null 2>&1 || exit 0

RESULT=$(curl -sf -X POST "$BROKER/peek" \
  -H 'Content-Type: application/json' \
  -d '{"identity":"claude.analysis"}' 2>/dev/null)

[ -z "$RESULT" ] && exit 0

COUNT=$(echo "$RESULT" | jq -r '.count // 0' 2>/dev/null)

if [ "$COUNT" -gt 0 ]; then
  SUMMARY=$(echo "$RESULT" | jq -r '.messages[] | "  - [\(.from_agent) -> \(.to_agent)] \(.intent)"' 2>/dev/null)
  echo "PALETTE PEERS INBOX: $COUNT pending message(s):"
  echo "$SUMMARY"
  echo "Call peers_fetch to read full messages."
fi

exit 0
