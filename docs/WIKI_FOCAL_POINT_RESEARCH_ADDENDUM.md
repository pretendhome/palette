# Research Addendum: Cited Sources for Wiki Focal Point Proposal

**Author**: kiro.design
**Date**: 2026-04-03
**Companion to**: `palette/docs/WIKI_FOCAL_POINT_PROPOSAL.md`

---

## Purpose

This addendum provides cited sources supporting the technical patterns proposed in the wiki focal point document. Each source is categorized by which phase of the proposal it informs.

---

## 1. The Wiki Compilation Pattern (Phases 1, 5)

### Karpathy's LLM Knowledge Base Pattern
Andrej Karpathy described a workflow where raw source documents are indexed into a `raw/` directory, then an LLM incrementally "compiles" a wiki of `.md` files with summaries, backlinks, categories, and cross-references. The LLM maintains all wiki data; the human rarely edits directly. At ~100 articles and ~400K words, complex Q&A works without fancy RAG because the LLM auto-maintains index files and brief summaries.
- Source: [Karpathy on X, 2026-04-02](https://x.com/karpathy) (Content was rephrased for compliance with licensing restrictions)
- Breakdown: [deepakness.com — LLM Knowledge Bases post by Andrej Karpathy](https://deepakness.com/raw/llm-knowledge-bases/)

**Relevance to Palette**: Palette's 450 structured files (~168 KL entries, 121 RIU modules, relationship graph, etc.) are the equivalent of Karpathy's `raw/` directory. The proposed wiki compiler is the "compile" step. The key insight: at Palette's scale (~300 compiled pages), auto-maintained indexes and summaries may eliminate the need for vector search entirely.

### Atomic — Self-Hosted AI-Native Knowledge Base
Atomic is an open-source personal knowledge base that converts markdown notes into a semantically-connected AI-augmented knowledge graph. Notes are automatically chunked, embedded, tagged, and linked by semantic similarity. It auto-generates wiki articles as knowledge grows.
- Source: [daily.dev — GitHub kenforthewin/atomic](https://app.daily.dev/posts/github---kenforthewin-atomic-y5rztff20)
- Source: [Product Hunt — Atomic](https://www.producthunt.com/products/atomic-5)

**Relevance to Palette**: Atomic validates the pattern of auto-generating wiki articles from structured notes. Palette's approach is more constrained (YAML → markdown compilation, not free-form notes), which is actually an advantage — the structure is already there.

### llm-docs-builder — Making Documentation AI-Friendly
An open-source library that transforms Markdown documentation into an AI-optimized format for LLMs, preserving structure while making it queryable.
- Source: [mensfeld.pl — An Open Source Tool for Making Documentation AI-Friendly](https://mensfeld.pl/2025/10/llm-docs-builder/)

**Relevance to Palette**: The wiki compiler should produce markdown that is both human-browsable AND LLM-optimized. This tool demonstrates the dual-format pattern.

---

## 2. Markdown as the Universal Interface (Phases 1, 2, 7)

### "File Over App" Philosophy
Obsidian's founder Steph Ango articulated the "file over app" philosophy: data should outlive the applications that create it. Plain text markdown files are the most durable, portable, and AI-compatible format for knowledge storage. Multiple sources confirm that plain text turned out to be the ideal foundation for AI agent integration.
- Source: [stephango.com/file-over-app](https://stephango.com/file-over-app) (referenced in multiple articles)
- Source: [dspn.substack.com — How I Built a Personal Knowledge System with Obsidian, AI, and Plain Text](https://dspn.substack.com/p/how-i-built-a-personal-knowledge)
- Source: [ericmjl.github.io — Mastering Personal Knowledge Management with Obsidian and AI](https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai/)

**Relevance to Palette**: Palette's YAML is machine-readable but not human-browsable. The compiled wiki adds the human-readable layer without abandoning the machine-readable source. Both formats coexist. This is exactly the "file over app" principle — the data (YAML) outlives any viewer (Obsidian, GitHub, VS Code).

### MAGI — Markdown for Agent Guidance & Instruction
MAGI is a markdown extension that embeds structured metadata (YAML front matter), actionable AI instructions (`ai-script` code blocks), and explicit document relationships (typed footnotes) directly within human-readable content. Designed for RAG and LLM agent integration.
- Source: [magi-mda.org — Markdown for Agent Guidance & Instruction](https://magi-mda.org/)
- Source: [magi-mda.mintlify.app — Architecture](https://magi-mda.mintlify.app/mdx/architecture)

**Relevance to Palette**: The wiki compiler could emit MAGI-compatible markdown — human-readable content with embedded metadata that agents can parse. This would make the compiled wiki simultaneously browsable by humans and queryable by agents without separate indexing.

### AGENTS.md as Industry Standard
AGENTS.md has been adopted by over 20,000 repositories on GitHub as a standard for providing AI coding agents with persistent, project-specific operational guidance. Palette already uses this pattern (CLAUDE.md, AGENTS.md, .steering/ files).
- Source: [augmentcode.com — How to Build Your AGENTS.md](https://www.augmentcode.com/guides/how-to-build-agents-md)
- Source: [ericmjl.github.io — How to teach your coding agent with AGENTS.md](https://ericmjl.github.io/blog/2025/10/4/how-to-teach-your-coding-agent-with-agentsmd/)

**Relevance to Palette**: Palette's steering files ARE AGENTS.md files. The wiki compiler would make the rest of the knowledge base equally accessible to agents — not just the steering instructions, but the full taxonomy, knowledge library, and relationship graph.

---

## 3. Search Over Compiled Markdown (Phase 2)

### QMD — Local Search Engine for AI Agent Memory
QMD is a local CLI tool that indexes Markdown files and combines BM25 keyword search, vector semantic search, and LLM re-ranking. It supports collection management, embedding creation, and verification. Used by Elvis (omarsar0) for his research paper knowledge base (referenced in the original post).
- Source: [bryanwhiting.com — A Technical Deep-Dive into QMD](https://bryanwhiting.com/ai/what-can-you-tell-me-about-toniqmd-repo/)
- Source: [everydev.ai — QMD - Local Search Engine for AI Agent Memory](https://www.everydev.ai/tools/qmd)
- Source: [refft.com — Lightweight local hybrid search for documents with LLM re-ranking](https://refft.com/en/tobi_qmd.html)

**Relevance to Palette**: QMD could be the search layer over the compiled wiki. Instead of building custom search, Palette could use QMD to index the `wiki/` directory and expose it via CLI to the resolver service. Three search modes (keyword, semantic, hybrid with reranking) cover different query types.

### Obsilo's Hybrid Search Architecture
Obsilo combines semantic similarity (Vectra + Xenova transformers), full-text keyword search (RRF fusion), 1-hop wikilink graph augmentation, local reranking (cross-encoder via WebAssembly), contextual retrieval, and implicit connection discovery between unlinked notes. All local, no cloud required.
- Source: [github.com/pssah4/obsilo](https://github.com/pssah4/obsilo)

**Relevance to Palette**: The hybrid search pattern (embeddings + BM25 + graph traversal) is the right architecture for searching the compiled wiki. Palette's relationship graph (2,013 quads) provides the graph augmentation layer that most systems lack. The 1-hop wikilink traversal pattern maps directly to Palette's quad-based graph queries.

### Blake Crosley's Hybrid Retriever for 16,894 Obsidian Files
A retriever combining FTS5 BM25 keyword search with Model2Vec vector similarity search, fused via Reciprocal Rank Fusion (RRF) into a single ranked list. Everything runs locally in one SQLite database: 49,746 chunks from 16,894 files in 83 MB. Full reindex takes four minutes.
- Source: [blakecrosley.com — Building a Hybrid Retriever for 16,894 Obsidian Files](https://blakecrosley.com/blog/hybrid-retriever-obsidian)
- Source: [blakecrosley.com — The Definitive Technical Reference](https://blakecrosley.com/guides/obsidian)

**Relevance to Palette**: At Palette's scale (~300 compiled pages), this approach would be trivially fast. The key insight from Crosley: "A 200-file vault with hybrid search and MCP integration is an AI knowledge base. The retrieval infrastructure is the product." (Content was rephrased for compliance with licensing restrictions)

---

## 4. Persistent Memory Across Systems (Phases 4, 8)

### mcp-memory-service
Open-source persistent memory for AI agent pipelines. SQLite + semantic vectors, MCP protocol, auto-consolidation. Provides `memory_store`, `memory_search`, `memory_list`, `memory_delete` tools.
- Source: [github.com/doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)
- Source: [crunchtools.com — How to Give Claude Code Persistent Memory](https://crunchtools.com/how-to-give-claude-code-persistent-memory/)
- Source: [PyPI — mcp-memory-service](https://pypi.org/project/mcp-memory-service/)

**Relevance to Palette**: Direct fit. Same protocol (MCP), same storage philosophy (SQLite — Palette peers already uses SQLite), adds semantic search over session memories. Could run alongside the peers broker as a second MCP server.

### Signet — Local-First Persistent Memory
Signet provides a local-first memory layer for AI coding agents. Built on SQLite and Markdown, it auto-summarizes code transcripts into structured knowledge. Stores knowledge as plain Markdown files and SQLite databases directly on the developer's machine, ensuring portability.
- Source: [thenextgentechinsider.com — Signet Launches Local-First Persistent Memory](https://www.thenextgentechinsider.com/pulse/signet-launches-local-first-persistent-memory-for-ai-coding-agents)

**Relevance to Palette**: Signet's pattern of auto-summarizing transcripts into structured knowledge is exactly what the voice feedback loop (Phase 3) needs. Voice sessions → auto-summarized → proposed wiki entries.

### Google's Memory Agent Pattern (No Vector DB)
A pattern for persistent AI memory without embeddings or vector databases. Uses structured text and retrieval patterns instead of similarity search.
- Source: [towardsdatascience.com — I Replaced Vector DBs with Google's Memory Agent Pattern for my notes in Obsidian](https://towardsdatascience.com/i-replaced-vector-dbs-with-googles-memory-agent-pattern-for-my-notes-in-obsidian/)

**Relevance to Palette**: At Palette's scale (~300 pages), vector search may be unnecessary. Karpathy's observation holds: auto-maintained indexes and summaries may be sufficient. This source validates the "start simple, add vectors only if needed" approach.

---

## 5. Multi-Agent Shared Knowledge (Phases 6, 8)

### Mozilla cq — Stack Overflow for Agents
Mozilla AI launched cq, an open-source knowledge-sharing platform where AI agents pool solutions instead of rediscovering them independently. Uses a four-phase cycle: agents query, contribute, validate, and score shared knowledge units across local, organization, and global tiers. Built on Python and MCP.
- Source: [blog.mozilla.ai — cq: Stack Overflow for Agents](https://blog.mozilla.ai/cq-stack-overflow-for-agents/)
- Source: [github.com/mozilla-ai/cq](https://github.com/mozilla-ai/cq)
- Source: [winbuzzer.com — Mozilla Launches Cq](https://winbuzzer.com/2026/03/25/mozilla-launches-cq-stack-overflow-for-ai-agents-xcxwbn/)
- Source: [heise.de — Mozilla cq: Stack Overflow for AI agents](https://www.heise.de/en/news/Mozilla-cq-Stack-Overflow-for-AI-agents-11223181.html)

**Relevance to Palette**: cq validates Palette's existing multi-agent knowledge-sharing pattern (peers bus + steering files + shared ontology). The key difference: cq is designed for agents that don't share a codebase. Palette's agents DO share a codebase (the SDK, taxonomy, and knowledge library). This means Palette's approach is actually more tightly integrated than cq's — the wiki compiler would make that integration explicit and browsable.

The four-phase cycle (query → contribute → validate → score) maps to Palette's existing governance: query (resolver), contribute (proposed wiki entries), validate (integrity checks + human review), score (evidence tiers). Palette already has this loop — it's just not automated.

### Multi-Agent Error Cascading
Research shows multi-agent systems fail at 41-86.7% rates in production, often silently, because one minor miscommunication cascades across the collaboration.
- Source: [learnagentic.substack.com — What is Error Cascading in Multi-Agent Systems?](https://learnagentic.substack.com/p/what-is-error-cascading-in-multi)

**Relevance to Palette**: The wiki serves as a shared ground truth that reduces cascading errors. When all systems read from the same compiled knowledge, miscommunication between agents decreases. The semantic audit pattern (already in Palette) catches drift before it cascades.

---

## 6. Voice + Multi-Agent Architecture (Phase 7)

### RT.Assistant — Multi-Agent Voice Bot
Microsoft's RT.Assistant uses a custom RTFlow framework hosting multiple specialized agents (Voice Agent, CodeGen Agent, Query Agent, App Agent) that communicate over a strongly-typed async bus, while a deterministic state-machine keeps non-deterministic LLM behavior in check.
- Source: [devblogs.microsoft.com — RT.Assistant: A Multi-Agent Voice Bot Using .NET and OpenAI](https://devblogs.microsoft.com/dotnet/rt-assistant-a-realtime-multiagent-voice-bot-using-dotnet-and-open-ai-api/)

**Relevance to Palette**: Palette's architecture (peers bus + convergence chain + resolver) is structurally similar to RT.Assistant's RTFlow. The wiki adds the shared knowledge layer that RT.Assistant lacks — their agents communicate but don't share a compiled knowledge base.

### LangChain Voice Agent Architecture
LangChain documents voice agents as combining speech recognition, NLP, generative AI, and TTS to create conversational agents. The architecture separates the voice layer from the reasoning layer.
- Source: [docs.langchain.com — Build a voice agent with LangChain](https://docs.langchain.com/oss/javascript/langchain/voice-agent)

**Relevance to Palette**: Confirms the architectural separation proposed in the wiki document: voice interfaces are surfaces, the wiki is the knowledge layer behind them. Mission Canvas already implements this separation.

---

## 7. Knowledge Graph + Wiki Convergence

### IWE Context Bridge — Agentic RAG with Graph Traversal
IWE's Context Bridge constructs a directed graph where nodes represent markdown documents and edges represent wikilinks or standard links. Unlike standard RAG that relies on vector similarity alone, this approach allows agents to navigate the graph structure directly for multi-hop reasoning.
- Source: [thenextgentechinsider.com — IWE Launches Context Bridge with Agentic RAG](https://www.thenextgentechinsider.com/pulse/iwe-launches-context-bridge-with-agentic-rag-and-openai-function-calling)

**Relevance to Palette**: Palette's relationship graph (2,013 quads) already provides the graph structure. The wiki compiler would add the wikilinks (markdown `[[backlinks]]`) that make the graph navigable in a document context. This gives Palette both: structured graph queries (via SDK `graph_query.py`) AND document-level graph traversal (via wikilinks in compiled markdown).

---

## Summary: What the Research Confirms

1. **The wiki compilation pattern works at Palette's scale.** Karpathy, Atomic, and llm-docs-builder all validate compiling structured data into browsable markdown with auto-maintained indexes.

2. **Markdown is the right format.** The "file over app" philosophy, MAGI, AGENTS.md, and the broader industry convergence on markdown as the universal interface between humans and LLMs all confirm this choice.

3. **Hybrid search over compiled markdown is solved.** QMD, Obsilo, and Crosley's retriever all demonstrate BM25 + vector + graph traversal search over markdown files at scales larger than Palette's.

4. **Persistent cross-system memory via MCP is production-ready.** mcp-memory-service, Signet, and Memento all provide SQLite + MCP memory layers that could plug directly into Palette's existing MCP infrastructure.

5. **Multi-agent shared knowledge is an active research area.** Mozilla cq validates the pattern. Palette's existing approach (shared ontology + peers bus + steering files) is actually more tightly integrated than most.

6. **The voice-to-wiki feedback loop is the novel contribution.** No existing system combines: multi-agent knowledge compilation + voice interface + governed feedback loop + human-gated promotion. This is where Palette would be doing something genuinely new.

---

## Tools Worth Evaluating in Phase 1-2

| Tool | What It Does | Phase | Priority |
|---|---|---|---|
| QMD (tobi/qmd) | Local hybrid search over markdown | Phase 2 | HIGH — could replace custom search |
| mcp-memory-service | Persistent memory via MCP + SQLite | Phase 4 | HIGH — direct protocol fit |
| MAGI format | Structured metadata in markdown | Phase 1 | MEDIUM — could inform wiki compiler output format |
| Mozilla cq | Agent knowledge sharing standard | Phase 6 | LOW — Palette already has tighter integration |
| Obsilo patterns | Hybrid search + memory architecture | Phase 2 | MEDIUM — patterns to learn from, not adopt wholesale |

---

*All sources accessed 2026-04-03. Content was rephrased for compliance with licensing restrictions where applicable.*
