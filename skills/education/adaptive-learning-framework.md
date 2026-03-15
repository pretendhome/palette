---
id: SKILL-EDU-001
name: Adaptive Learning Framework for Special Needs
domain: Education
for_agents: [Architect, Researcher, Builder, Validator]
triggers: [RIU-001, RIU-014, RIU-020]
impressions: 3
status: WORKING
validated_on: ARON pilot (La Scuola International School, 2026-03)
---

# Adaptive Learning Framework for Special Needs

Validated framework for designing AI-assisted, personalized learning programs for children with learning differences. Developed through the ARON pilot — a twice-exceptional (2e) child with phonological dyslexia at one of San Francisco's premier private schools.

## When to Use

- Designing personalized learning programs for children with specific learning disabilities
- Building AI-assisted educational tools for schools or families
- Creating adaptive intervention strategies that evolve with the learner
- Structuring handoff documents for educators implementing AI-augmented programs

## Privacy Architecture

All implementations MUST separate:
- **Publishable layer** (anonymized avatar): frameworks, protocols, exercise designs, handoff documents
- **Confidential layer** (real child data): evaluations, IEPs, progress reports, personally identifiable information

The avatar pattern (e.g., ARON) allows the framework to be shared, discussed, and improved without exposing the child.

## Core Components

### 1. Cognitive Profile (Anonymized)
Build a complete learning profile from available assessments:
- Cognitive strengths (e.g., verbal reasoning, working memory)
- Specific processing deficits (e.g., phonological, orthographic, rapid naming)
- Academic performance vs. cognitive potential gap
- Sensory and environmental preferences

### 2. Longitudinal Analysis
Analyze progress reports across multiple years to identify:
- Growth trajectories (what's improving)
- Persistent patterns (what isn't moving)
- Intervention effectiveness (what worked vs. what didn't)
- Environmental factors (which settings produce best results)

### 3. Exercise Protocols
Design interventions that:
- Target specific deficits with evidence-based methods
- Build on cognitive strengths as scaffolding
- Include AI-assisted tools (text-to-speech, speech-to-text, visual learning)
- Provide measurable progress indicators
- Can be implemented by a non-specialist facilitator

### 4. AI Toolkit Selection
Match tools to needs:
- Reading support: immersive reader, phonics apps with adaptive difficulty
- Writing support: speech-to-text, grammar assistants, visual organizers
- Math support: manipulative-based apps, multi-sensory approaches
- Executive function: timer tools, task decomposition, reward systems

### 5. Facilitator Handoff
Create a complete handoff document that enables a teacher or parent to:
- Understand the child's profile without reading raw assessments
- Implement daily exercises without specialized training
- Track progress using defined indicators
- Adjust difficulty based on clear criteria
- Know when to escalate to a specialist

## Quality Checks

- [ ] No personally identifiable information in publishable documents
- [ ] All interventions cite evidence-based research
- [ ] Exercise protocols are implementable by a non-specialist
- [ ] Progress indicators are measurable and time-bound
- [ ] Handoff document is self-contained (facilitator needs nothing else)

## Validated Patterns (ARON Pilot)

- Multi-sensory phonics intervention with AI-assisted repetition
- Strength-based scaffolding (using strong verbal reasoning to support weak decoding)
- Daily 15-minute structured exercise protocols with weekly progress checks
- AI toolkit: Speechify, Learning Ally, Bookshare, Google Read&Write
- Parent-as-facilitator model with educator oversight
