# Contributing to Palette

Thank you for considering contributing to Palette! This toolkit improves through validated real-world use.

---

## How to Contribute

Palette accepts five types of contributions:

### 1. Agent Failure Reports
**When**: An agent failed to meet expectations  
**Template**: `.github/ISSUE_TEMPLATE/agent-failure.md`  
**Requirements**:
- Which agent failed (name + version)
- What you expected vs. what happened
- Context (problem, constraints, inputs)
- Post-mortem analysis (root cause)

### 2. Validated Use Cases
**When**: You successfully used Palette for a real problem  
**Template**: `.github/ISSUE_TEMPLATE/use-case-submission.md`  
**Requirements**:
- Problem description
- Which agents used
- Execution steps
- Outcome (success criteria met)
- Evidence (logs, artifacts, results)

### 3. Library Entry Proposals
**When**: You discovered a reusable solution to a recurring problem  
**Template**: `.github/ISSUE_TEMPLATE/library-entry.md`  
**Requirements**:
- RIU this solves (from taxonomy)
- Question being answered
- Validated solution (with evidence)
- When to use / when not to use
- Source/citation

### 4. Taxonomy Refinements
**When**: RIU routing could be improved based on experience  
**Template**: `.github/ISSUE_TEMPLATE/taxonomy-refinement.md`  
**Requirements**:
- Which RIU needs refinement
- Current routing vs. proposed routing
- Evidence from real usage
- Impact assessment

### 5. Documentation Improvements
**When**: Docs are unclear, incomplete, or incorrect  
**Template**: Standard GitHub issue  
**Requirements**:
- Which file/section
- What's unclear/wrong
- Proposed improvement
- Why it matters

---

## Contribution Workflow

### Step 1: Create an Issue
Use the appropriate issue template from `.github/ISSUE_TEMPLATE/`

**Quality gates**:
- ✅ Evidence required (cite sources, provide validation data)
- ✅ Rationale required (why this improves Palette)
- ✅ Validation required (for use cases and Library entries)

### Step 2: Discussion
Maintainer will review and may:
- Approve for implementation
- Request clarification
- Suggest modifications
- Decline (with reasoning)

### Step 3: Fork and Implement
If approved:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-contribution`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages

### Step 4: Submit Pull Request
Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)

**PR must include**:
- Link to approved issue
- Summary of changes
- Evidence of validation (if applicable)
- Impact assessment (what changes, what stays the same)

### Step 5: Review and Merge
Maintainer will:
- Review changes
- Test if applicable
- Request modifications if needed
- Merge when approved
- Acknowledge in CHANGELOG.md

---

## Contribution Standards

### Evidence-Based
All contributions must be grounded in evidence:
- **Use cases**: Show it worked (logs, artifacts, outcomes)
- **Library entries**: Cite sources, provide validation
- **Agent improvements**: Post-mortem analysis with root cause
- **Taxonomy refinements**: Real usage data, not speculation

### Rationale-Driven
Explain why this improves Palette:
- ❌ "I think this is better"
- ✅ "This solves [problem] because [reasoning], validated by [evidence]"

### Quality-Focused
Maintain high standards:
- Clear writing (no jargon without explanation)
- Complete examples (not fragments)
- Tested solutions (not untested ideas)
- Aligned with Palette principles (convergence, glass-box, human-in-the-loop)

---

## What We're Looking For

### High-Value Contributions
- **Production use cases**: Real FDE scenarios with evidence
- **Cross-domain patterns**: Insights applicable beyond single problem
- **Agent maturity data**: Impressions that advance agents toward PRODUCTION tier
- **Library entries**: Validated solutions to recurring problems

### Medium-Value Contributions
- **Documentation clarity**: Improvements that reduce confusion
- **Example enhancements**: Better explanations, more context
- **Taxonomy refinements**: Better RIU routing based on experience

### Lower-Priority Contributions
- **Cosmetic changes**: Formatting, style (unless blocking usability)
- **Speculative ideas**: Untested theories without validation
- **Scope expansion**: New features without proven need

---

## What We're NOT Looking For

### Out of Scope
- ❌ Autonomous operation (Palette requires human-AI alignment)
- ❌ Platform-specific implementations (toolkit must work with any AI)
- ❌ Complexity for complexity's sake (simplicity is a feature)
- ❌ Unvalidated theories (evidence required)

### Quality Issues
- ❌ Incomplete examples (fragments without context)
- ❌ Unsourced claims (no citations or validation)
- ❌ Vague improvements ("make it better")
- ❌ Breaking changes without migration path

---

## Governance

### Decision Authority
- **Maintainer** (Mical): Final approval on all contributions
- **Contributors** (You): Submit improvements via PR
- **Reviewers** (Future): Delegated review authority for specific areas

### Approval Process
- **Tier 1 changes** (palette-core.md): Maintainer only
- **Tier 2 changes** (assumptions.md): Maintainer approval required
- **Agent improvements**: Maintainer approval
- **Examples/docs**: Maintainer approval
- **Bug fixes**: Maintainer approval (fast turnaround)

### Delegation Path
As community grows, maintainer may delegate review authority:
- "Agent expert" role for agent improvements
- "Documentation lead" role for docs/examples
- Maintainer retains veto power on all decisions

---

## Recognition

### Acknowledgment
Contributors are acknowledged in:
- **CHANGELOG.md**: Listed by contribution
- **Contributors section**: Added to README.md (future)
- **Issue/PR comments**: Public thanks from maintainer

### Impact Tracking
High-value contributions may be featured:
- **Case studies**: Detailed write-ups of successful use cases
- **Pattern library**: Cross-domain insights promoted to documentation
- **Agent maturity**: Impressions that advance agents to PRODUCTION tier

---

## Code of Conduct

### Expected Behavior
- **Respectful**: Disagree professionally, no personal attacks
- **Evidence-based**: Ground claims in data, not opinion
- **Collaborative**: Work together to improve Palette
- **Quality-focused**: Maintain high standards

### Unacceptable Behavior
- Personal attacks or harassment
- Unsourced claims presented as fact
- Low-effort contributions without validation
- Scope creep without justification

### Enforcement
Maintainer reserves right to:
- Close issues/PRs that don't meet standards
- Request modifications before approval
- Decline contributions that don't align with Palette principles
- Ban contributors who violate code of conduct

---

## Questions?

- **General questions**: Open a GitHub issue
- **Contribution ideas**: Use issue templates to propose
- **Urgent issues**: [Add contact method when available]

---

## Getting Started

1. **Browse examples**: See `examples/` for validated use cases
2. **Read documentation**: Understand Palette principles in `docs/`
3. **Identify opportunity**: Find something to improve
4. **Create issue**: Use appropriate template
5. **Wait for approval**: Maintainer will review
6. **Submit PR**: Follow workflow above

**Thank you for helping Palette improve!**

---

**Remember**: Palette exists to turn ambiguity into clarity through disciplined collaboration. Your contributions make that possible.
