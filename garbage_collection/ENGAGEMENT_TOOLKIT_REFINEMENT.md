# Palette Toolkit Refinement Engagement

**Date**: 2026-01-29  
**Engagement ID**: TOOLKIT-REFINEMENT-001  
**Status**: CONVERGENCE PHASE

---

## Semantic Blueprint (Convergence Brief)

### Goal (What success looks like)
1. **Taxonomy v1.1 validated and installed** as canonical version (115+ RIUs, refined structure)
2. **Knowledge library validated and enhanced** with reliable sources, correctly mapped to taxonomy v1.1
3. **New agents designed, researched, and implemented** based on agents_guide_for_kiro_to_research.md

### Roles (Human vs Agent responsibilities)

**Human (Mical)**:
- Final approval on ONE-WAY DOOR decisions
- Validation of agent implementations
- Confirmation of taxonomy/library mappings

**Agents**:
- **Argentavis (Argy)**: Research and validate knowledge library sources, research agent solutions
- **Tyrannosaurus (Rex)**: Analyze taxonomy v1.1 superiority, architect new agent positioning
- **Therizinosaurus (Theri)**: Build new agent implementations
- **Velociraptor (Raptor)**: Debug agent implementations
- **Orchestrator (Kiro)**: Coordinate multi-phase execution, enforce convergence

### Capabilities (Agents/tools needed)

**Available**:
- Taxonomy v1.1 (new file to analyze)
- Knowledge library raw.md (source material)
- Knowledge library v1.0 FINAL.yaml (current prod)
- Agents guide (architecture research)
- File system operations
- Web research (for source validation)

**Constraints**:
- Only use VERY reliable sources (GitHub repos, well-trafficked, trusted)
- Verify sources before making changes
- Maintain context when updating library entries
- Preserve existing links (needed for updates/verification)
- Tight mapping between library and taxonomy required
- Agents must be built iteratively (bootstrapping problem)

### Non-Goals (Explicitly out of scope)
- ❌ Not building all agents in one pass (iterative approach)
- ❌ Not changing library entries without verified sources
- ❌ Not using unreliable or unverifiable sources
- ❌ Not breaking existing taxonomy/library mappings

---

## THREE PHASES (Sequential Execution)

### 🚨 ONE-WAY DOOR DECISIONS (Require Approval Before Proceeding)

**Decision 1**: Replace taxonomy v1.0 with v1.1 as canonical version
- **Why irreversible**: All RIU references, agent assignments, library mappings depend on taxonomy structure
- **Impact**: Requires remapping knowledge library, updating all documentation
- **Status**: PENDING ANALYSIS (Phase 1, Task 1)

**Decision 2**: Modify production knowledge library entries
- **Why irreversible**: Changes affect agent retrieval, demo content, customer-facing information
- **Impact**: Must maintain backward compatibility, verify all sources
- **Status**: PENDING VALIDATION (Phase 2)

**Decision 3**: Add new agent archetypes to assumptions.md
- **Why irreversible**: Changes agent maturity tracking, RIU routing, system architecture
- **Impact**: Requires updating decisions.md, agent definitions, fixture creation
- **Status**: PENDING ARCHITECTURE (Phase 3)

---

## PHASE 1: Taxonomy v1.1 Migration

### Task 1.1: Analyze Taxonomy v1.1 Superiority (Rex)

**Objective**: Understand why v1.1 is superior to v1.0

**Analysis Required**:
- Compare RIU count (v1.0: 115, v1.1: ?)
- Compare structure/organization
- Identify refinements and improvements
- Assess completeness
- Flag any concerns or gaps

**Deliverable**: Analysis report with recommendation

**Status**: READY TO EXECUTE

---

### Task 1.2: Move Taxonomy v1.1 to Canonical Location

**Actions**:
```bash
# Move v1.1 to taxonomy folder
mv /home/mical/palette/palette_taxonomy_v1.1.yaml /home/mical/palette/taxonomy/releases/v1.1/

# Move old versions to garbage
mv /home/mical/palette/taxonomy/releases/v1.0/* /home/mical/palette/garbage_collection/
```

**ONE-WAY DOOR**: This replaces the canonical taxonomy

**Status**: PENDING APPROVAL (after Task 1.1 analysis)

---

## PHASE 2: Knowledge Library Validation & Enhancement

### Task 2.1: Sweep Current Library vs Raw File

**Objective**: Ensure no information lost from raw file

**Process**:
1. Read knowledge_library_raw.md (source material)
2. Read palette_knowledge_library_v1_0_FINAL.yaml (current prod)
3. Compare entry by entry (86 entries)
4. Verify links are preserved
5. Flag any missing information

**Deliverable**: Gap analysis report

**Status**: READY TO EXECUTE (after Phase 1 complete)

---

### Task 2.2: Validate Sources with Argy Research

**Objective**: Verify each library entry with reliable sources

**Constraints**:
- ONLY use very reliable sources
- Prefer: GitHub repos (well-trafficked, trusted)
- Verify source before making changes
- Ensure same context (don't add unrelated info)

**Process** (for each of 86 entries):
1. Argy researches entry topic
2. Validates existing sources
3. Finds additional reliable sources (if available)
4. Adds to sources section (if verified)
5. Flags entries that need human review

**Deliverable**: Enhanced library with verified sources

**Status**: PENDING (after Task 2.1)

---

### Task 2.3: Map Library to Taxonomy v1.1

**Objective**: Ensure tight mapping between library and taxonomy

**Process**:
1. For each library entry, identify applicable RIUs from v1.1
2. Update metadata to reference correct RIUs
3. Verify bidirectional mapping (RIU → Library, Library → RIU)
4. Flag unmapped entries or RIUs

**Deliverable**: Library with correct v1.1 RIU mappings

**Status**: PENDING (after Task 2.2)

---

## PHASE 3: New Agent Design & Implementation

### Task 3.1: Analyze Agent Architecture (Rex)

**Objective**: Determine how new agents should be positioned

**Input**: agents_guide_for_kiro_to_research.md

**Analysis Required**:
- What new agent archetypes are proposed?
- How do they relate to existing agents (Argy, Theri, Raptor, Rex, Yuty, Anky, Para, Orch)?
- What RIUs would they handle?
- What constraints/capabilities do they need?
- Are there conflicts or overlaps?

**Deliverable**: Architecture recommendation for new agents

**Status**: PENDING (after Phase 2 complete)

---

### Task 3.2: Research Agent Solutions (Argy)

**Objective**: Research each proposed agent solution

**Process**:
1. For each proposed agent in guide
2. Research implementation patterns
3. Find reliable sources (GitHub, trusted repos)
4. Validate feasibility
5. Recommend refinements

**Deliverable**: Research report per agent

**Status**: PENDING (after Task 3.1)

---

### Task 3.3: Build Agent Implementations (Theri)

**Objective**: Implement new agents

**Process** (iterative, one agent at a time):
1. Create agent definition in assumptions.md
2. Create agent directory structure
3. Implement agent logic
4. Create fixtures for testing
5. Log first impression in decisions.md

**Deliverable**: Working agent implementations

**Status**: PENDING (after Task 3.2)

**Note**: Bootstrapping challenge - we need agents to build agents. Will be iterative.

---

### Task 3.4: Debug Agent Implementations (Raptor)

**Objective**: Debug and refine new agents

**Process**:
1. Run agent fixtures
2. Identify failures
3. Debug and fix
4. Re-test
5. Update maturity tracking

**Deliverable**: Debugged, working agents

**Status**: PENDING (after Task 3.3)

---

## Execution Order

```
Phase 1: Taxonomy Migration
├─ 1.1: Rex analyzes v1.1 superiority → READY
├─ 1.2: Move v1.1 to canonical location → PENDING APPROVAL
└─ ONE-WAY DOOR: Approve taxonomy replacement

Phase 2: Library Validation (after Phase 1)
├─ 2.1: Sweep library vs raw file → READY
├─ 2.2: Argy validates sources (86 entries) → PENDING
├─ 2.3: Map library to taxonomy v1.1 → PENDING
└─ ONE-WAY DOOR: Approve library modifications

Phase 3: Agent Implementation (after Phase 2)
├─ 3.1: Rex analyzes agent architecture → READY
├─ 3.2: Argy researches agent solutions → PENDING
├─ 3.3: Theri builds agents (iterative) → PENDING
├─ 3.4: Raptor debugs agents → PENDING
└─ ONE-WAY DOOR: Approve new agent archetypes
```

---

## Open Questions

1. **Taxonomy v1.1**: How many RIUs does it contain? What are the key improvements?
2. **Knowledge library**: Are there entries in raw.md that aren't in prod library?
3. **Agent guide**: What specific agents are proposed? How many?
4. **Bootstrapping**: How do we build agents when we need agents to build agents? (Iterative approach)
5. **Timeline**: This is multi-day work. What's the priority order?

---

## Next Checks (Concrete Verifications)

- [ ] Verify taxonomy v1.1 file is valid YAML
- [ ] Count RIUs in v1.1
- [ ] Verify knowledge_library_raw.md is readable
- [ ] Verify agents_guide_for_kiro_to_research.md is readable
- [ ] Confirm all three files are in /home/mical/palette/

---

## Estimated Effort

**Phase 1**: 1-2 hours (analysis + migration)  
**Phase 2**: 4-6 hours (86 entries × research + validation + mapping)  
**Phase 3**: 8-12 hours (depends on number of agents, iterative debugging)

**Total**: 13-20 hours of work

---

## Approval Checkpoint

**Before proceeding, I need confirmation**:

1. ✓ Is this semantic blueprint accurate?
2. ✓ Do you approve starting with Phase 1, Task 1.1 (Rex analyzes taxonomy v1.1)?
3. ✓ Do you understand this is multi-day, iterative work?
4. ✓ Are the THREE ONE-WAY DOOR decisions correctly identified?

**Type "APPROVED" to begin Phase 1, or provide corrections.**
