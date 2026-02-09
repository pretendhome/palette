#!/bin/bash
# Perplexity MCP Setup for Palette
# Run this script to configure Perplexity MCP integration

set -e

echo "🎨 Palette - Perplexity MCP Setup"
echo "=================================="
echo ""

# Check if API key is already set
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "⚠️  PERPLEXITY_API_KEY not found in environment"
    echo ""
    echo "To get an API key:"
    echo "1. Go to https://www.perplexity.ai/settings/api"
    echo "2. Create an API key"
    echo "3. Add to ~/.bashrc:"
    echo "   export PERPLEXITY_API_KEY='your-key-here'"
    echo ""
    read -p "Do you have an API key ready? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Perplexity API key: " api_key
        echo "export PERPLEXITY_API_KEY='$api_key'" >> ~/.bashrc
        export PERPLEXITY_API_KEY="$api_key"
        echo "✓ API key added to ~/.bashrc"
    else
        echo "❌ Setup cancelled. Get an API key first."
        exit 1
    fi
else
    echo "✓ PERPLEXITY_API_KEY found"
fi

# Create Kiro config directory
echo ""
echo "Creating Kiro config directory..."
mkdir -p ~/.config/kiro
echo "✓ Directory created"

# Create MCP configuration
echo ""
echo "Creating MCP configuration..."
cat > ~/.config/kiro/mcp.json << 'EOF'
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-perplexity"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    }
  }
}
EOF
echo "✓ MCP config created at ~/.config/kiro/mcp.json"

# Verify npx is available
echo ""
echo "Checking dependencies..."
if command -v npx &> /dev/null; then
    echo "✓ npx is available"
else
    echo "⚠️  npx not found. Install Node.js first:"
    echo "   https://nodejs.org/"
fi

# Test configuration
echo ""
echo "Testing configuration..."
if [ -f ~/.config/kiro/mcp.json ]; then
    if command -v jq &> /dev/null; then
        cat ~/.config/kiro/mcp.json | jq . > /dev/null 2>&1
        echo "✓ MCP config is valid JSON"
    else
        echo "ℹ️  Install 'jq' to validate JSON (optional)"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Reload your shell: source ~/.bashrc"
echo "2. Start Kiro CLI: kiro-cli chat"
echo "3. Activate Argentavis: #argentavis"
echo "4. Test search: 'Research agent security best practices'"
echo ""
echo "Documentation: ~/palette/docs/perplexity-mcp-integration.md"
