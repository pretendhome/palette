#!/bin/bash
# Post-commit hook: Auto-sync agent impressions and push to GitHub
# Copy to .git/hooks/post-commit and chmod +x

# Skip if this is an amended commit (prevent recursion)
if [ -f .git/AMEND_IN_PROGRESS ]; then
    rm .git/AMEND_IN_PROGRESS
    exit 0
fi

# Only run if decision logs changed
if git diff --name-only HEAD~1 | grep -qE "(decisions\.md|execution_summary\.md)"; then
    echo "📊 Decision log changed, syncing impressions..."
    
    # Run sync script
    python3 palette/scripts/sync-impressions.py
    
    # Check if README changed
    if git diff --quiet palette/agents/README.md; then
        echo "✅ No impression changes"
    else
        echo "✅ Agent maturity updated"
        
        # Mark that we're amending
        touch .git/AMEND_IN_PROGRESS
        
        # Stage and amend commit
        git add palette/agents/README.md
        git commit --amend --no-edit --no-verify
        
        # Push to GitHub
        echo "🚀 Pushing to GitHub..."
        git push
    fi
fi
