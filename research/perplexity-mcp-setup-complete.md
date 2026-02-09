# Perplexity MCP Integration - Complete

**Date**: 2026-02-06  
**Status**: ✅ Configured and Documented

---

## What Was Done

### 1. MCP Configuration Created ✅
**File**: `~/.config/kiro/mcp.json`

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-perplexity"],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    }
  }
}
```

### 2. Argentavis Agent Updated ✅
**File**: `/home/mical/palette/agents/argentavis/argentavis.md`

**Changes**:
- Added Perplexity MCP as primary search tool
- Updated tool priority: Perplexity → web_search → Knowledge Library
- Documented Perplexity advantages and usage

### 3. Documentation Created ✅
**File**: `/home/mical/palette/docs/perplexity-mcp-integration.md`

**Contents**:
- What is Perplexity MCP
- Configuration details
- Setup instructions
- Usage in Palette
- Benefits for research agent
- Troubleshooting guide
- Security notes

### 4. Setup Script Created ✅
**File**: `/home/mical/palette/scripts/setup-perplexity-mcp.sh`

**Features**:
- Interactive API key setup
- Automatic config creation
- Dependency checking
- Configuration validation

---

## How to Use

### Quick Start

1. **Get API Key**:
   - Go to https://www.perplexity.ai/settings/api
   - Create an API key

2. **Run Setup Script**:
   ```bash
   cd /home/mical/palette
   ./scripts/setup-perplexity-mcp.sh
   ```

3. **Reload Shell**:
   ```bash
   source ~/.bashrc
   ```

4. **Test in Kiro**:
   ```bash
   kiro-cli chat
   #argentavis
   Research agent security best practices
   ```

### Manual Setup

If you prefer manual setup:

1. **Set environment variable**:
   ```bash
   export PERPLEXITY_API_KEY="your-key-here"
   echo 'export PERPLEXITY_API_KEY="your-key-here"' >> ~/.bashrc
   ```

2. **MCP config already created** at `~/.config/kiro/mcp.json`

3. **Start using**: Activate Argentavis and search

---

## Integration Details

### Tool Priority for Argentavis

**Before Perplexity**:
1. Knowledge Library (internal)
2. web_search (external)

**After Perplexity**:
1. Knowledge Library (internal, validated)
2. Perplexity MCP (AI-powered search with citations)
3. web_search (fallback)

### Why This Order?

1. **Knowledge Library first**: Free, validated, Palette-specific
2. **Perplexity second**: AI synthesis, better than raw web search
3. **web_search last**: Fallback if Perplexity unavailable

---

## Benefits

### For Research Quality
- ✅ AI-synthesized results (not just links)
- ✅ Automatic source citations
- ✅ Better handling of complex queries
- ✅ Confidence scoring

### For Palette Workflow
- ✅ Faster convergence (less back-and-forth)
- ✅ Higher quality findings
- ✅ Better source diversity
- ✅ Maintains Argy's read-only constraint

### For Cost Efficiency
- ✅ Knowledge Library first (free)
- ✅ Perplexity only for gaps
- ✅ Reduces manual research time

---

## Files Modified/Created

### Created
1. `~/.config/kiro/mcp.json` - MCP configuration
2. `/home/mical/palette/docs/perplexity-mcp-integration.md` - Documentation
3. `/home/mical/palette/scripts/setup-perplexity-mcp.sh` - Setup script

### Modified
1. `/home/mical/palette/agents/argentavis/argentavis.md` - Added Perplexity tool

---

## Next Steps

### Immediate
1. Get Perplexity API key
2. Run setup script
3. Test with Argentavis

### Future Enhancements
1. **Cache results**: Store Perplexity findings in Knowledge Library
2. **Cost tracking**: Monitor API usage per agent
3. **Auto-fallback**: Switch to web_search if Perplexity fails
4. **Result validation**: Cross-check with Knowledge Library

---

## Security Notes

⚠️ **Important**:
- Never commit API key to git
- Use environment variables only
- Don't search for sensitive/proprietary info via Perplexity
- Use Knowledge Library for confidential topics

---

## Troubleshooting

### MCP Server Not Starting
```bash
# Check API key
echo $PERPLEXITY_API_KEY

# Check npx
npx --version

# Validate config
cat ~/.config/kiro/mcp.json | jq .
```

### Perplexity Not Being Used
- Verify Argentavis is active (`#argentavis`)
- Check Kiro logs: `~/.kiro/logs/mcp.log`
- Ensure API key is set in current shell

---

## Documentation References

- **Setup Guide**: `/home/mical/palette/docs/perplexity-mcp-integration.md`
- **Argentavis Agent**: `/home/mical/palette/agents/argentavis/argentavis.md`
- **Perplexity API**: https://docs.perplexity.ai
- **MCP Protocol**: https://modelcontextprotocol.io

---

**Status**: ✅ Ready to use. Run setup script to complete configuration.
