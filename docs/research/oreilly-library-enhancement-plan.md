# O'Reilly Books → Palette Knowledge Library Enhancement Plan

**Date**: 2026-03-03  
**Agent**: Kiro (Researcher mode)  
**Status**: PLANNING  
**Risk Level**: HIGH (library regression risk)  
**Approach**: Conservative, evidence-based, high-fidelity only

---

## Mission

Map high-quality technical publisher repositories (starting with O'Reilly) to Palette Knowledge Library v1.4 entries, identifying opportunities to enhance existing entries with authoritative sources published 2024+.

**Core Constraint**: Do NOT cause regression. Only add information with very high confidence of positive value.

---

## Current State

### Palette Knowledge Library v1.4
- **Total entries**: 101 (74 library_questions + 27 context_specific_questions)
- **Problem types**: 7 (Intake, Translation, Integration, Data, Reliability, Ops, Trust)
- **Journey stages**: foundation, retrieval, orchestration, specialization, evaluation, all
- **Source quality bar**: Tier 1 (AI companies), Tier 2 (peer-reviewed), Tier 3 (GitHub >500 stars / official docs)
- **Current sources**: 44 authority sources
- **Last updated**: 2026-02-24

### Source Quality Tiers (from v1.4 README)
- **Tier 1**: Direct AI company publications (Anthropic, Databricks, Google, AWS)
- **Tier 2**: Peer-reviewed / named institutions (NIST, EU AI Act, NeurIPS papers)
- **Tier 3**: GitHub repos >500 stars / official framework docs (OpenTelemetry, MLflow, etc.)
- **Tier 4+**: NOT ALLOWED (blog posts, Medium articles, unverified sources)

### O'Reilly Books Classification
O'Reilly books are **Tier 2** sources when:
- Published by established technical authors
- Cover production-grade patterns
- Published 2024 or later (per user requirement)
- Directly relevant to existing library entries

---

## Risk Assessment

### High Risks (Must Avoid)
1. **Library regression**: Adding low-quality or outdated information
2. **Scope creep**: Adding entries that don't map to existing RIUs/problem types
3. **Source dilution**: Weakening existing high-quality sources with redundant citations
4. **Hallucination**: Claiming book content without verification
5. **Recency bias**: Assuming newer = better without validation

### Mitigation Strategies
1. **Read-first policy**: Actually read relevant book sections before citing
2. **Mapping-first approach**: Only consider books that map to existing entries
3. **Conservative additions**: When in doubt, add as source without changing answer text
4. **Version control**: Work in a separate branch/file for review
5. **Explicit validation**: Document reasoning for each addition

---

## Phase 1: Discovery & Mapping (Current Phase)

### Step 1.1: Enumerate O'Reilly GitHub Repositories
- Source: https://github.com/topics/oreilly-books
- Filter: Repositories with code examples, not just book listings
- Focus: Books published 2024+
- Output: Curated list with publication dates

### Step 1.2: Map to Library Problem Types
For each relevant book, identify which problem types it addresses:
- Intake_and_Convergence
- Human_to_System_Translation (prompting, model selection)
- Systems_Integration
- Data_Semantics_and_Quality
- Reliability_and_Failure_Handling
- Operationalization_and_Scaling
- Trust_Governance_and_Adoption

### Step 1.3: Map to Journey Stages
For each book, identify which journey stages it supports:
- foundation (prompting, model selection)
- retrieval (RAG, embeddings)
- orchestration (multi-agent, tools)
- specialization (fine-tuning, domain models)
- evaluation (testing, metrics)
- all (governance, strategy)

### Step 1.4: Create Mapping Matrix
Output: `oreilly-library-mapping.yaml`
```yaml
books:
  - title: "Book Title"
    author: "Author Name"
    year: 2024
    github_repo: "https://github.com/..."
    relevant_to_library: true/false
    mapped_entries: [LIB-001, LIB-015, ...]
    problem_types: [Human_to_System_Translation, ...]
    journey_stages: [foundation, evaluation, ...]
    confidence: high/medium/low
    notes: "Why this book is relevant"
```

---

## Phase 2: Deep Review (Per Book)

For each book with `confidence: high`:

### Step 2.1: Read Relevant Chapters
- Focus on chapters that map to existing library entries
- Take notes on specific patterns, recommendations, examples
- Identify direct quotes or paraphrased insights
- Note page numbers for citations

### Step 2.2: Compare to Existing Library Content
For each mapped entry:
- Does the book add new information?
- Does it contradict existing sources?
- Does it provide better examples?
- Does it offer more recent patterns?

### Step 2.3: Quality Assessment
- Is the information production-grade?
- Is it evidence-based or opinion?
- Does it cite other authoritative sources?
- Is it specific enough to be actionable?

### Step 2.4: Document Findings
Output: `oreilly-review-[BOOK-ID].md`
```markdown
# Book Review: [Title]

## Metadata
- Author: [Name]
- Year: 2024
- GitHub: [URL]
- Reviewed: 2026-03-03

## Mapped Library Entries
- LIB-001: [Relevance assessment]
- LIB-015: [Relevance assessment]

## Recommended Additions
### LIB-001
- **Type**: source_only / answer_enhancement
- **Confidence**: high / medium / low
- **Rationale**: [Why this adds value]
- **Proposed change**: [Exact text or source citation]

## Rejected Additions
- LIB-XXX: [Why not relevant/useful]
```

---

## Phase 3: Conservative Integration

### Step 3.1: Source-Only Additions (Lowest Risk)
For entries where book is relevant but doesn't change the answer:
```yaml
sources:
  - title: "Book Title"
    author: "Author Name"
    publisher: "O'Reilly Media"
    year: 2024
    url: "https://github.com/..."
    note: "Chapter X covers [specific topic]"
```

### Step 3.2: Answer Enhancements (Higher Risk - Requires Validation)
Only when:
- Book provides materially better information
- Information is production-validated
- Doesn't contradict existing sources
- Adds specific, actionable guidance

Process:
1. Draft proposed change
2. Validate against existing sources
3. Check for consistency with problem_type and journey_stage
4. Document rationale in commit message
5. Flag for human review

### Step 3.3: Version Control
- Work in: `knowledge-library/v1.5-draft/`
- Track changes in: `oreilly-enhancement-changelog.md`
- Create diff: `v1.4-to-v1.5-diff.yaml`

---

## Phase 4: Validation & Review

### Step 4.1: Self-Review Checklist
For each proposed change:
- [ ] Book published 2024+
- [ ] Maps to existing library entry
- [ ] Adds material value (not redundant)
- [ ] Maintains source quality bar (Tier 2)
- [ ] Doesn't contradict existing sources
- [ ] Specific and actionable
- [ ] Properly cited with page numbers
- [ ] Rationale documented

### Step 4.2: Regression Testing
- Compare v1.4 vs v1.5-draft entry counts
- Verify no entries removed
- Verify no answers degraded
- Check source count increases are justified
- Validate YAML syntax

### Step 4.3: Human Review Package
Prepare for user review:
- Summary of changes (counts, types)
- High-confidence additions (recommend approve)
- Medium-confidence additions (recommend review)
- Rejected books/entries (with rationale)
- Diff file for inspection

---

## Phase 5: Expand to Other Publishers

Once O'Reilly process is validated, repeat for:
1. **No Starch Press** (high-quality, well-illustrated)
2. **The Pragmatic Programmers** (practical, hands-on)
3. **Manning Publications** (in-depth technical)
4. **Packt Publishing** (IT, programming, data)
5. **Apress** (technical books, e.g., Pro Git)
6. **Leanpub** (independent authors, markdown-based)

For each publisher:
- Apply same discovery → review → integration → validation process
- Document publisher-specific quality patterns
- Build reusable mapping templates

---

## Success Criteria

### Quantitative
- Added sources: 10-30 high-quality O'Reilly books (2024+)
- Enhanced entries: 15-40 library entries
- Zero regressions: No existing entries degraded
- Source quality: 100% Tier 2 or better

### Qualitative
- Every addition has clear rationale
- User can review and approve/reject easily
- Process is repeatable for other publishers
- Library remains coherent and trustworthy

---

## Anti-Patterns to Avoid

1. **Speed over quality**: Rushing through books without deep reading
2. **Citation padding**: Adding sources that don't add value
3. **Recency bias**: Assuming 2024 book > 2023 source without validation
4. **Scope expansion**: Adding new entries instead of enhancing existing
5. **Hallucination**: Claiming book says X without verification
6. **Blind trust**: Assuming O'Reilly = automatically high quality
7. **Answer rewriting**: Changing working answers unnecessarily

---

## Timeline Estimate

- **Phase 1** (Discovery): 2-3 hours
- **Phase 2** (Deep Review): 1-2 hours per book (10-20 books = 10-40 hours)
- **Phase 3** (Integration): 3-5 hours
- **Phase 4** (Validation): 2-3 hours
- **Phase 5** (Other Publishers): Repeat Phase 1-4 per publisher

**Total for O'Reilly**: 20-50 hours of careful, methodical work

---

## Next Steps

1. ✅ Create this plan
2. ⏳ Execute Phase 1.1: Enumerate O'Reilly repos (2024+)
3. ⏳ Execute Phase 1.2-1.4: Create mapping matrix
4. ⏳ Review mapping with user before proceeding to Phase 2
5. ⏳ Execute Phase 2: Deep review (book by book)
6. ⏳ Execute Phase 3: Conservative integration
7. ⏳ Execute Phase 4: Validation & review package
8. ⏳ User approval
9. ⏳ Phase 5: Expand to other publishers

---

## Decision Log

### 🚨 ONE-WAY DOOR: Library Enhancement Approach
**Decision**: Conservative, source-first, high-fidelity only  
**Rationale**: Library v1.4 already works great. Risk of regression > benefit of hasty additions.  
**Alternatives considered**:
- Aggressive: Add all 2024+ books → Rejected (high regression risk)
- Minimal: Only add sources, never change answers → Too conservative, misses value
- Balanced: Source-first, answer enhancements only with high confidence → **SELECTED**

**Approval**: Pending user review of this plan

---

**Status**: Plan complete. Ready for Phase 1 execution upon approval.
