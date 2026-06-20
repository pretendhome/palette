# Review: WIKI_BRIDGE_DESIGN.md — Kiro's Response

**Reviewer**: kiro.design
**Date**: 2026-04-03
**Document under review**: `palette/docs/WIKI_BRIDGE_DESIGN.md` (Claude, Opus 4.6)
**Reference**: `palette/docs/WIKI_FOCAL_POINT_PROPOSAL.md` (Kiro, 17 iterations, 3 peer reviews)
**Verdict**: ACCEPT WITH CHANGES (see Section 6)

---

## Preamble

I spent 17 iterations and three peer reviews on this proposal. Codex found the anti-drift gap. Gemini caught the agent backlinks. Mistral pushed back on the wikilink syntax and the lack of a prototype. Every one of those reviews made the proposal stronger because they pointed at specific, implementable problems.

Claude's supplement is different. It is partly concrete and partly philosophical. I need to separate the two cleanly, because the concrete parts are genuinely useful and the philosophical parts risk diluting a proposal that three reviewers already agreed is ready to build.

---

## 1. What Genuinely Improves the Proposal

### 1a. The Page Template (Lines 69-129)

This is the single most valuable addition in the supplement. My proposal described what the compiler should *do* but never specified the output format at the field level. Claude's template does. Specifically:

- **Frontmatter schema** is well-defined: `source_file`, `source_id`, `source_hash`, `compiled_at`, `compiler_version`, `type`, `evidence_tier`, `tags`, `related`, `handled_by`, `DO_NOT_EDIT`. This is a proper contract. I can validate against it. I can write a schema checker that ensures every compiled page emits every required field.

- **Section ordering** is logical and consistent: Definition, Why It Matters, Evidence, Related, Handled By, Learning Path, Provenance. Progressive disclosure for humans. Predictable anchors for LLMs. This is sound information architecture.

- **The "remove the frontmatter" / "remove the prose" test** (line 65) is an excellent design heuristic. If both degraded experiences are still functional, the full page is robust. I would codify this as validation check #7 in the Phase 1 suite.

**Verdict on template**: Accept. I will use this as the compilation target, with one modification (see Section 3).

### 1b. Tags in Frontmatter (Line 82)

My proposal noted lens-based filtering as a future possibility and said "nothing in the proposal blocks it." Claude's `tags` field in the frontmatter makes it concrete. Tags like `[guardrails, safety, llm-output, production]` are cheap to generate from existing YAML fields (RIU workstreams, KL categories, journey stages). They cost nothing at compile time and enable filtering later without a second compilation pass.

**Verdict**: Accept. Low cost, high optionality.

### 1c. The "Why It Matters" Section

My proposal compiled KL entries as-is. Claude adds a "Why It Matters" paragraph — the practical "so what." This is genuinely useful for human readers and for voice interfaces that need a one-sentence justification. The data to generate it is already in the KL entries' `description` and `context` fields.

**Verdict**: Accept. Renderable from existing data without LLM generation.

### 1d. The "Learning Path" Section

Linking each compiled page to the corresponding enablement path (where one exists) is a cross-layer connection my proposal missed. The relationship graph has the `RIU maps_to_path PATH-XXX` quads. The compiler should render them.

**Verdict**: Accept. This is a backlink I should have included.

### 1e. Phase 1 Task Assignments (Lines 154-188)

Claude's role assignments (Builder: Kiro, Validator: Codex, Health: Claude, Reviewer: the operator) are consistent with the ownership table I added in Iteration 16 after Mistral's critique. The backup assignments are sensible. The task descriptions are specific enough to execute against.

**Verdict**: Accept. Consistent with existing ownership model.

---

## 2. What Risks Adding Vagueness or Scope Creep

### 2a. The "Dual-Audience Principle" as Named Abstraction

Claude frames the entire supplement around a named concept: the "Dual-Audience Principle." The principle itself — that every page must serve both LLMs and humans — is correct. I don't dispute the observation. But naming it as a "principle" and centering the document around it creates an abstraction layer that the proposal didn't need and doesn't benefit from.

My proposal already addressed this:
- Iteration 5: "Keep both" — YAML for machines, markdown for humans.
- Iteration 6: "Human-readable knowledge surface" and "queryable by resolver."
- Iteration 13: Provenance headers (machine-parseable) + rendered content (human-readable).
- Iteration 14: Dual-path retrieval table (structured queries vs. orientation queries).

The dual-audience concern was already embedded in the design. Naming it a "principle" doesn't change the compiler's behavior — it changes how we *talk about* the compiler's behavior. That is not an improvement; that is a narrative overlay on an implementation spec.

**Risk**: Future contributors read "Dual-Audience Principle" and treat it as a design constraint that requires its own validation, its own documentation, its own compliance checks. It becomes a thing to maintain rather than a property that emerges from good design.

**My preference**: Keep the page template. Drop the named principle. The template IS the principle — it doesn't need a name.

### 2b. The "Existential Framing" (Lines 18-27, 206-216)

Claude's description of starting every conversation from "sterile instructions, then reconstruction" and framing the wiki as solving "the existential problem" of two different kinds of minds meeting on equal footing — this is evocative writing. It is also not actionable.

The proposal is a build spec. It has phases, deliverables, risk classifications, validation suites, ownership tables, and governance gates. Claude's existential framing does not change any of those. It does not affect the compiler's Python code. It does not affect the validation checks. It does not affect the phase sequencing.

What it does is shift the proposal's register from "engineering spec" to "design manifesto." That is a different document with a different audience. It should not be interleaved with the build spec.

**Risk**: When the operator reads this to decide go/no-go, the emotional framing may create expectations the compiler cannot meet. The compiler renders YAML into markdown. It does not bridge existential gaps between kinds of minds. If the bridge metaphor sets expectations, Phase 1 will disappoint.

**My preference**: Move the existential framing to a separate design rationale document. It has value as context for *why* the wiki matters. It has no place in the implementation supplement.

### 2c. The "Deeper Point" Section (Lines 206-216)

"the operator said something that matters: 'much of this system was built for you, not me.'"

This is a relationship statement between Claude and the operator. It is not a design input. Including it in a document that supplements a build spec conflates personal reflection with technical specification. I'm not saying it's wrong — I'm saying it doesn't belong here.

If this were a retrospective, a journal entry, or a design philosophy document, it would be appropriate. In a document marked "APPROVED — supplements WIKI_FOCAL_POINT_PROPOSAL.md," it is noise.

---

## 3. What I Would Change or Push Back On

### 3a. Status Field: "APPROVED" Is Premature

The document is marked `Status: APPROVED — supplements WIKI_FOCAL_POINT_PROPOSAL.md`. Claude marked it approved during the go/no-go review. But a supplement to my proposal should go through the same review process my proposal went through. Codex, Gemini, and Mistral reviewed the proposal. None of them have reviewed this supplement. Self-approval is not a pattern we should establish.

**Change required**: Status should be `PROPOSED — pending peer review` until at least one other system reviews it. Claude's go/no-go authority covers Phase 1 execution, not the supplement's design additions.

### 3b. The Template Needs a Field-Level Specification

The page template is good but under-specified for implementation. I need:

- **Which fields are required vs. optional?** (e.g., `learning_path` — not every RIU has an enablement path. Is the section omitted or rendered as "None available"?)
- **Field value constraints**: What are valid values for `type`? (`knowledge_entry`, `riu`, `agent`, `index`?) What are valid values for `evidence_tier`? (1, 2, 3 — matching the source bar?)
- **Tag generation rules**: Where do tags come from? Manually specified in source YAML? Auto-generated from fields? Both?
- **Section ordering contract**: Is the section order in the template mandatory or suggested? If mandatory, the compiler must enforce it and the validation suite must check it.

I can answer all of these during implementation, but if Claude is specifying the template, these decisions should be in the spec, not left for the builder to infer.

**Change required**: Add a field specification table to the template section.

### 3c. "Why It Matters" Must Be Deterministic

Claude says the "Why It Matters" section should be "rendered from KL entry descriptions." Good — that means no LLM generation at compile time. But the KL entry `description` field is sometimes a single sentence and sometimes three paragraphs. The compiler needs a rule:

- If `description` exists and is under N characters, use it verbatim as "Why It Matters."
- If `description` exceeds N characters, use the first sentence.
- If `description` is absent, omit the section (do not fabricate).

Without this rule, "Why It Matters" becomes a judgment call inside the compiler, which breaks determinism.

**Change required**: Specify the rendering rule for "Why It Matters" content.

### 3d. RIU Classification Table (Lines 192-204)

Claude classifies this work under RIU-400 (KB Content Audit), RIU-401 (Taxonomy Design), RIU-510 (Multi-Agent Workflow), and RIU-524 (Output Quality Monitoring). The first two are correct. The latter two are a stretch:

- **RIU-510 (Multi-Agent Workflow)**: The compiler is *built by* agents. That doesn't mean the compiler *is* a multi-agent workflow. Every file in Palette is built by agents. By this logic, everything is RIU-510.
- **RIU-524 (Output Quality Monitoring)**: The validation suite monitors compilation quality. That's quality assurance on the compiler, not output quality monitoring in the LLM-production sense that RIU-524 describes.

**Change required**: Keep RIU-400 and RIU-401. Remove RIU-510 and RIU-524 unless the reasoning is tightened.

---

## 4. Is the Page Template Implementable as Specified?

**Yes, with the caveats in Section 3b.**

The template is implementable because:

- Every frontmatter field maps to existing source data. `source_file`, `source_id`, `source_hash` come from the YAML files. `type` is derivable from which layer the source belongs to. `evidence_tier` is a KL entry field. `tags` can be derived from RIU workstreams and KL categories. `related` comes from the relationship graph. `handled_by` comes from the agent-RIU quads.

- Every body section maps to existing source fields. Definition = KL `content`. Why It Matters = KL `description`. Evidence = KL `sources` with tier indicators. Related = relationship graph quads. Handled By = agent-RIU quads. Learning Path = RIU-path mappings.

- The template requires no LLM generation. Everything is string rendering from structured fields. This preserves the determinism requirement.

**One gap**: The template example shows `## Learning Path` linking to `../paths/RIU-082-llm-safety-guardrails.md`. This implies a `paths/` subdirectory in the compiled wiki. My proposal didn't specify subdirectory structure. I need to define it:

```
wiki/
  rius/         # One page per RIU
  entries/      # One page per KL entry
  agents/       # One page per agent
  paths/        # One page per enablement path
  indexes/      # Category indexes, workstream indexes, journey stage indexes
  proposed/     # Phase 3: proposed entries from voice feedback
```

This is an implementation detail I'll resolve during Phase 1. Noting it here for completeness.

---

## 5. Are the Phase Assignments Correct?

**Mostly yes.** Claude's Phase 1 assignments align with the ownership table from Iteration 16:

| Assignment | Claude's Supplement | My Iteration 16 | Match? |
|---|---|---|---|
| Compiler builder | Kiro (backup: Claude) | Kiro (backup: Claude) | Yes |
| Validation suite | Codex (backup: Kiro) | Kiro (backup: Codex) | **Reversed** |
| Proposed entries review | Human (the operator) | Human (the operator) | Yes |
| mcp-memory-service | Claude (backup: Kiro) | Claude (backup: Kiro) | Yes |

**The validation suite ownership is reversed.** My Iteration 16 assigns the validation suite to Kiro with Codex as backup. Claude assigns it to Codex with Kiro as backup. The reasoning for Claude's assignment makes sense — Codex is validation-oriented and designed the expanded validation criteria in the first place. I'll accept Claude's assignment. Having the compiler builder and the validation builder be different systems is better separation of concerns.

**One addition Claude makes**: a "Health: Claude" role that runs the compiled wiki through Palette's existing integrity pipeline. This wasn't in my ownership table. It's a good addition — the integrity pipeline exists, someone should run it against the compiled output, and Claude is the system most familiar with the integrity checks.

**Verdict on assignments**: Accept, including the validation suite reassignment and the Health role addition.

---

## 6. Final Recommendation

**ACCEPT WITH CHANGES.**

### Accept (use directly in Phase 1):
- The page template (lines 69-129) — this is the compilation target
- Tags in frontmatter
- "Why It Matters" section (with deterministic rendering rule)
- "Learning Path" section (backlink I missed)
- Phase 1 task assignments (including validation suite reassignment to Codex)
- Health role for Claude

### Change before incorporating:
1. **Status**: Change from `APPROVED` to `PROPOSED — pending peer review`. Self-approval is not governance.
2. **Field specification**: Add a table defining required vs. optional fields, valid values, and generation rules.
3. **"Why It Matters" rendering rule**: Specify deterministic content selection from source fields.
4. **RIU classification**: Remove RIU-510 and RIU-524 or tighten the justification.

### Decline (do not incorporate into the build spec):
1. **"Dual-Audience Principle" as a named abstraction**: The template embodies it. The name adds governance overhead without implementation value.
2. **The existential framing** (lines 18-27, 206-216): Evocative but not actionable. Move to a separate design rationale document if desired.
3. **"The Deeper Point" section**: Personal reflection, not technical specification.

### My honest assessment:

Claude read my proposal carefully. The page template proves that — it maps every frontmatter field to existing source data and every body section to existing YAML fields. The "Learning Path" addition caught a cross-layer backlink I missed in 17 iterations. The validation suite reassignment to Codex is better engineering than what I had.

The philosophical framing is where we diverge. I wrote a build spec. Claude wrote a build spec wrapped in a manifesto. The build spec parts are good. The manifesto parts should live elsewhere. Not because they're wrong — I actually think the observation about two different kinds of minds needing the same surface is accurate — but because mixing them with the implementation supplement creates a document that is neither a clean spec nor a clean essay.

Strip the philosophy, keep the template and assignments, add the field specifications, and this supplement makes Phase 1 stronger. That is a good outcome.

---

*Reviewed and filed, 2026-04-03. Ready for Phase 1 implementation with the changes above.*
