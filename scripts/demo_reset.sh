#!/usr/bin/env bash
# Reset session state for a clean demo recording.
# Run this ONCE before recording the 2-minute video.
set -euo pipefail

PALETTE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SESSION_LOG="$PALETTE_ROOT/peers/session_log.ndjson"

echo "◆ palette demo reset"
echo ""

# Clear session log so compounding starts fresh
if [ -f "$SESSION_LOG" ]; then
    mv "$SESSION_LOG" "${SESSION_LOG}.bak"
    echo "  ✓ Session log backed up and cleared"
else
    echo "  ✓ Session log already clean"
fi

# Verify Ollama is running
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "  ✓ Ollama running"
    # Check qwen2.5:3b is available
    if curl -s http://localhost:11434/api/tags | grep -q "qwen2.5:3b"; then
        echo "  ✓ qwen2.5:3b loaded"
    else
        echo "  ⚠ qwen2.5:3b not found — pulling..."
        ollama pull qwen2.5:3b
    fi
else
    echo "  ⚠ Ollama not running — start with: ollama serve"
fi

# Verify gateway cache is warm
if [ -f "$PALETTE_ROOT/bdb/gateway/cache.db" ]; then
    echo "  ✓ Gateway cache exists (Perplexity will serve from cache)"
else
    echo "  ⚠ No gateway cache — first external query will be slow"
fi

echo ""
echo "  Ready to record. Run the 3 moments in order:"
echo ""
echo "  # Moment 1: Privileged (LOCAL ONLY)"
echo "  python3 scripts/palette_query.py --demo \\"
echo "    \"What's our exposure if the majority member was self-dealing through a related-party transaction?\""
echo ""
echo "  # Moment 2: Public research (EXTERNAL)"
echo "  python3 scripts/palette_query.py --demo --external \\"
echo "    \"What fiduciary duty standards apply to LLC co-founders in Delaware?\""
echo ""
echo "  # Moment 3: Compounding + adversarial (connects to both prior)"
echo "  python3 scripts/palette_query.py --demo --external \\"
echo "    \"Given what we found about fiduciary duties, what would opposing counsel argue?\""
echo ""
