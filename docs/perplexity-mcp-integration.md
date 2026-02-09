# Perplexity MCP Integration for Palette

**Date**: 2026-02-06  
**Purpose**: Enable Argentavis (research agent) to use Perplexity AI for enhanced search capabilities  
**Status**: Configured

---

## What is Perplexity MCP?

Perplexity MCP (Model Context Protocol) server provides AI-powered search capabilities through the Perplexity API. It offers:

- AI-synthesized search results with automatic source citations
- Better understanding of complex technical queries
- Built-in confidence scoring
- Real-time web search with LLM-powered synthesis

---

## Configuration

### Location
`~/.config/kiro/mcp.json`

### Configuration File
```json
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
```

---

## Setup Instructions

### 1. Get Perplexity API Key

1. Go to https://www.perplexity.ai/settings/api
2. Create an API key
3. Copy the key

### 2. Set Environment Variable

Add to your `~/.bashrc` or `~/.bash_profile`:

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

Then reload:
```bash
source ~/.bashrc
```

### 3. Verify Installation

Start Kiro CLI and check if Perplexity MCP is available:

```bash
kiro-cli chat
```

The MCP server should auto-start when Kiro initializes.

---

## Usage in Palette

### Argentavis (Research Agent)

When Argentavis is active (`#argentavis` or `#argy`), it will automatically use Perplexity MCP for searches if available.

**Search priority**:
1. Knowledge Library (internal validated knowledge)
2. Perplexity MCP (AI-powered search)
3. web_search (fallback)

**Example**:
```
User: Research best practices for agent security

Argy: Checking knowledge library first...
✓ Found LIB-089, LIB-090, LIB-091

Searching via Perplexity for additional sources...
[Perplexity results with citations]
```

---

## Benefits for Palette

### 1. Enhanced Research Quality
- AI synthesis reduces manual source aggregation
- Automatic citation tracking
- Better handling of complex queries

### 2. Faster Convergence
- Reduces back-and-forth clarification
- Provides structured results immediately
- Confidence scores help prioritize findings

### 3. Better Source Quality
- Perplexity prioritizes authoritative sources
- Real-time web access (not limited to training data)
- Automatic fact-checking across sources

---

## Integration with Palette Agents

### Argentavis (Argy) - Primary User
- Uses Perplexity for external research
- Combines with Knowledge Library for comprehensive findings
- Maintains read-only constraint (no decisions)

### Other Agents
- **Rex (Architecture)**: Can request Argy to research via Perplexity
- **Anky (Validation)**: Can use Perplexity to validate claims
- **Yuty (Narrative)**: Can request Argy to research communication best practices

---

## Troubleshooting

### MCP Server Not Starting

**Check 1**: Verify API key is set
```bash
echo $PERPLEXITY_API_KEY
```

**Check 2**: Verify npx is available
```bash
npx --version
```

**Check 3**: Check MCP config syntax
```bash
cat ~/.config/kiro/mcp.json | jq .
```

### Perplexity Not Being Used

**Check 1**: Verify Argentavis is active
```
Current agent should show: Argentavis (Argy)
```

**Check 2**: Check Kiro logs
```bash
tail -f ~/.kiro/logs/mcp.log
```

---

## Cost Considerations

Perplexity API is usage-based:
- Free tier: Limited queries per month
- Pro tier: Higher limits

**Recommendation**: Use Knowledge Library first (free), Perplexity for gaps.

---

## Security Notes

### API Key Protection
- Never commit API key to git
- Use environment variables only
- Rotate keys periodically

### Data Privacy
- Perplexity searches are logged by Perplexity
- Don't search for sensitive/proprietary information
- Use internal Knowledge Library for confidential topics

---

## Future Enhancements

### Potential Additions
1. **Caching**: Cache Perplexity results in Knowledge Library
2. **Cost tracking**: Monitor API usage per agent
3. **Fallback logic**: Auto-fallback to web_search if Perplexity unavailable
4. **Result validation**: Cross-check Perplexity results with Knowledge Library

---

## References

- Perplexity API Docs: https://docs.perplexity.ai
- MCP Protocol: https://modelcontextprotocol.io
- Palette Tier 2 (Agent Archetypes): `.kiro/steering/assumptions.md`
- Argentavis Agent: `agents/argentavis/argentavis.md`

---

**Status**: ✅ Configured and ready to use
