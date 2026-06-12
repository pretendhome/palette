# SDK for Humans + Ontology as AI Memory
**Date**: 2026-05-22
**Purpose**: clarify the two deepest concepts in Palette and test them against the actual system artifacts

---

## Core Definitions

### SDK for Humans

`SDK for Humans` means Palette is not primarily a chatbot, assistant, or workflow wrapper.
It is a capability interface for people.

An SDK gives a developer:

- primitives
- structure
- reusable patterns
- guardrails
- a way to build correctly faster than from scratch

`SDK for Humans` applies that same logic to judgment.
The human is the builder.
The thing being built is better thinking, better decisions, and better reusable patterns of action.

In practical terms, `SDK for Humans` means:

- the system should help a person frame the problem before answering it
- the system should make good judgment easier to repeat
- the system should leave the human more capable after the interaction
- the system should expose structure, not hide it behind magic

### Ontology as AI Memory

`Ontology as AI Memory` means the system does not “remember” by storing chats.
It remembers by classifying reality into stable semantic objects and relationships.

In Palette, memory is not just:

- transcripts
- embeddings
- cached answers
- conversation history

Memory is primarily:

- taxonomy
- knowledge objects
- evidence tiers
- routing classes
- decision logs
- governance states
- repeatable joins across those structures

This matters because raw history is recall.
Ontology is reusable memory.

### The Relationship Between The Two

These two concepts are separate but inseparable:

- `SDK for Humans` is the user-facing purpose
- `Ontology as AI Memory` is the system-level mechanism

Without `SDK for Humans`, the ontology becomes an internal engineering model with weak product meaning.
Without `Ontology as AI Memory`, the SDK claim collapses into vague coaching language with no compounding substrate.

The product thesis is:

> Palette makes people more capable because it stores judgment in ontology-shaped memory rather than disposable chat.

---

## Artifact 1 — Product Thesis / Tagline

### Part 1 — SDK for Humans

The README already points in the right direction: `The Operating System for Human Judgment` and `Your judgment compounds here`.
That is much closer to `SDK for Humans` than “AI assistant.”

The strength:

- it frames the user as someone building judgment, not consuming outputs

The weakness:

- `Operating System for Human Judgment` is powerful but still abstract
- `SDK for Humans` is sharper for insiders but still needs a concrete behavior model

Required move:

- define the SDK in product language as `a system that helps you classify, ground, decide, remember, and reuse`

### Part 2 — Ontology as AI Memory

The thesis is already half-present in the README:

- taxonomy-first routing
- governed knowledge
- append-only decision history
- portable local state

That is essentially ontology-as-memory, even if the phrase is not used explicitly.

The strength:

- the repo already stores memory as typed objects, not only free text

The weakness:

- the business story still says “memory” more often than it says “semantic structure”

Required move:

- define memory publicly as `classified judgment with provenance`

### Part 3 — How They Work Together

This artifact is where the two concepts first fuse:

- `SDK for Humans` explains why the system exists
- `Ontology as AI Memory` explains why it compounds instead of resetting

If this relationship is made explicit, the product story becomes much cleaner:

- normal AI: answer engine
- Palette: capability engine built on structured judgment memory

---

## Artifact 2 — RIU Taxonomy

### Part 1 — SDK for Humans

The 121-node RIU taxonomy is not just internal routing.
In `SDK for Humans` terms, it is the hidden curriculum of better judgment.

It teaches the person:

- what kind of problem they are actually facing
- what class of mistake is likely
- what shape of response is appropriate

That is SDK behavior.
It gives the user primitives.

The weakness:

- most users do not yet experience the taxonomy as a learnable scaffold
- they experience it as internal system machinery

Required move:

- expose RIUs selectively as user-facing problem frames, not as raw IDs

### Part 2 — Ontology as AI Memory

This is the strongest ontology artifact in the entire system.
The taxonomy is the semantic compression layer that lets the system remember across sessions.

Without RIUs:

- each new query is a fresh string
- memory becomes fuzzy similarity
- retrieval becomes relevance without conceptual continuity

With RIUs:

- the system can remember by problem type
- patterns can accumulate
- decisions can be joined across time

This is not side infrastructure.
It is the backbone of memory.

### Part 3 — How They Work Together

The RIU taxonomy is where the two concepts most cleanly meet.

- as SDK: it teaches the human what sort of problem this is
- as memory: it lets the machine store judgment in reusable categories

This is the deepest reason Palette feels different from chat.
It does not merely store what was said.
It stores what kind of thing happened.

---

## Artifact 3 — Knowledge Library

### Part 1 — SDK for Humans

The knowledge library is not just retrieval content.
In `SDK for Humans` terms, it is the reusable reference layer that helps the human inherit prior structure.

It gives the user:

- grounded concepts
- known patterns
- evidence-backed answers
- a starting point richer than intuition

The weakness:

- the current library is still heavily AI/ML-weighted
- domain entry packs for legal, medical, financial, and accounting use are still thin

Required move:

- build domain starter packs that make the SDK useful on day one in a vertical

### Part 2 — Ontology as AI Memory

The knowledge library is memory only because it is structured and linked:

- entries connect to RIUs
- evidence tiers shape trust
- tags and metadata support joins

If it were only a markdown vault, it would be content.
Because it is typed and routed, it becomes memory.

The strength:

- memory is anchored to evidence, not just recency

The weakness:

- the ontology is stronger than the legal-domain content density right now

### Part 3 — How They Work Together

The SDK claim needs the knowledge library because people need grounded inheritance, not just classification.
The ontology claim needs it because classification without content is empty.

Together they produce:

- a human learning scaffold
- a machine-readable body of remembered judgment support

The library is where abstract ontology becomes usable memory.

---

## Artifact 4 — Hybrid Retrieval

### Part 1 — SDK for Humans

Hybrid retrieval is an invisible SDK primitive.
The user should not care about FTS5, vectors, and RRF.
They should care that the system finds the right precedent, pattern, or prior decision quickly and consistently.

In SDK terms, retrieval is the equivalent of:

- autocomplete
- docs lookup
- dependency resolution

It reduces the effort needed to build the next judgment correctly.

### Part 2 — Ontology as AI Memory

Retrieval is not the memory itself.
It is the recall mechanism over structured memory.

This distinction matters:

- embeddings alone are not memory
- keyword search alone is not memory
- retrieval is how the ontology gets reactivated

The current retrieval stack is good because it joins:

- semantic similarity
- lexical precision
- evidence-aware ranking

That makes ontology usable at runtime.

### Part 3 — How They Work Together

Without retrieval, the ontology is static.
Without the ontology, retrieval is just probabilistic search.

Together they enable the core product motion:

- classify the problem
- recall the right prior structure
- return a grounded starting point

That is exactly how an SDK should behave for a human operator.

---

## Artifact 5 — `palette query` CLI

### Part 1 — SDK for Humans

The CLI is the cleanest current expression of `SDK for Humans`.
It is not just a shell command.
It encodes a sequence:

- resolve
- retrieve
- route
- respond
- extract

That is a human capability loop.
It teaches that good answers come from process, not just model output.

The weakness:

- it is still a builder-facing surface
- most end users will need this same logic in a GUI

### Part 2 — Ontology as AI Memory

The CLI routes through ontology before response.
That is critical.

It means:

- memory is activated before output generation
- the system does not improvise first and rationalize later

The extract step also matters.
It hints at a write path where future memory can be proposed from successful or failed retrieval.

That is ontology trying to become living memory, not static reference.

### Part 3 — How They Work Together

The CLI is effectively a developer console for the product thesis.

- as SDK: it exposes the judgment pipeline explicitly
- as ontology memory: it forces every query through classification and grounded recall

This is why it feels real even before packaging.
It already embodies the theory operationally.

---

## Artifact 6 — Append-Only Decision History

### Part 1 — SDK for Humans

Decision history is one of the strongest `SDK for Humans` artifacts because it lets the user reuse not only answers, but reasoning.

That means the person can ask:

- what did we decide?
- why did we decide it?
- what evidence supported it?

That is much closer to capability-building than ordinary chat history.

### Part 2 — Ontology as AI Memory

This is where memory becomes temporal rather than just semantic.
The ontology says what kind of thing happened.
The decision log says when it happened, why it happened, and how it resolved.

That combination is real memory.

The weakness:

- portability and export/import are not yet fully productized
- firm-level multi-user access control is not mature

### Part 3 — How They Work Together

An SDK without decision history teaches poorly.
Ontology without decision history remembers weakly.

Together they create the judgment trail:

- problem type
- evidence
- decision
- consequence
- reuse

That is the compounding loop.

---

## Artifact 7 — Governed Perplexity Gateway

### Part 1 — SDK for Humans

The gateway matters to `SDK for Humans` because it teaches the user an important discipline:

- not every question should go outside
- public knowledge and private context are different classes of information
- external research must be governed, not casually blended

That is a capability lesson, not just a privacy feature.

### Part 2 — Ontology as AI Memory

The gateway is not core memory, but it protects memory boundaries.

Its role in ontology is:

- preserve the distinction between local truth and external signal
- keep public research from mutating private memory implicitly
- maintain typed provenance between `[LOCAL]` and `[EXTERNAL]`

That separation is essential.
Otherwise memory becomes contaminated by uncontrolled merges.

### Part 3 — How They Work Together

This is a strong synthesis artifact.

- as SDK: it teaches safe externalization
- as ontology memory: it keeps the memory graph clean and source-aware

The gateway is not just a connector.
It is a governance membrane between local judgment memory and outside information.

---

## Artifact 8 — Peers Bus / Multi-Agent Convergence

### Part 1 — SDK for Humans

The peers bus is one of the least obvious but most important `SDK for Humans` artifacts.
Why?
Because it turns the system from “one answer engine” into “a room with roles.”

That helps the user learn:

- researcher and builder are different modes
- architecture and validation are different responsibilities
- disagreement is productive when bounded

This is a social model of thinking encoded as software.

### Part 2 — Ontology as AI Memory

The bus becomes memory when messages are typed, governed, and searchable.
Unstructured multi-agent chat would not be enough.

The important properties are:

- message identity
- message type
- risk tier
- thread grouping
- checkpoint state

That is ontology applied to collaboration itself.

### Part 3 — How They Work Together

The bus makes the SDK claim credible because it lets users think through differentiated roles.
It makes the memory claim credible because those interactions are not ephemeral chat fragments.
They become typed, inspectable units.

This is the architecture of structured deliberation.

---

## Artifact 9 — Voice Hub

### Part 1 — SDK for Humans

Voice Hub is the most emotionally legible expression of `SDK for Humans`.
It lowers the friction of entering the system and makes the “room of experts” metaphor intuitive.

This matters because an SDK for humans should not require terminal literacy.
It should meet people in natural interaction.

Voice also supports a deeper thesis:

- learning, coaching, and judgment are conversational acts

### Part 2 — Ontology as AI Memory

Voice by itself is not memory.
Voice becomes memory only because it is routed through taxonomy, retrieval, and governance before becoming output.

That is the critical distinction.

Without ontology, voice is just a pleasant interface.
With ontology, voice is a low-friction entrance into a structured memory system.

### Part 3 — How They Work Together

Voice is where the two concepts can become product-obvious:

- the user experiences a humane interface
- the machine still thinks through classified, grounded, durable structure

That is likely one of the strongest long-term product surfaces.

---

## Artifact 10 — Mission Canvas / Operator Surface

### Part 1 — SDK for Humans

Mission Canvas is the natural home for the `SDK for Humans` thesis.
It can become the place where people do three things:

- frame the problem
- inspect the reasoning
- carry forward the judgment trail

If built well, it is not a dashboard.
It is a capability workbench.

### Part 2 — Ontology as AI Memory

Canvas should be the visualizer of ontology memory.
It should show:

- the current problem class
- the supporting knowledge
- the prior related decisions
- the external signal boundary
- the recommended next action

That would make memory legible.

### Part 3 — How They Work Together

If the CLI is the engineering expression of the thesis, Mission Canvas should be the product expression.

- SDK for Humans becomes visible workflow
- Ontology as AI Memory becomes visible context continuity

This is the surface where the two ideas can become commercially understandable.

---

## Artifact 11 — Onboarding / Domain Packs / Setup

### Part 1 — SDK for Humans

This is where the current product is weakest.
An SDK for humans must have a first-run experience.

Right now, Palette behaves like a powerful internal system.
A real SDK-like product would ask:

- what domain are you in?
- what risks matter?
- what starter patterns should be loaded?
- what should stay local?

That would turn setup into capability scaffolding.

### Part 2 — Ontology as AI Memory

Domain packs are ontology memory bootloaders.
They provide:

- the starting taxonomy subset
- the starter knowledge base
- the relevant blocked/allowed patterns
- the initial decision vocabulary

Without them, memory exists architecturally but arrives too empty for real users.

### Part 3 — How They Work Together

Onboarding is where the product can turn ontology into immediate usefulness.

- the human gets a guided starting environment
- the machine gets a domain-shaped semantic scaffold

This is one of the most important bridges from demo to product.

---

## Artifact 12 — Packaging / Downloadable Local Product

### Part 1 — SDK for Humans

If this concept is real, it must eventually be installable like a toolchain.

That means:

- setup should feel like installing a trusted environment
- the local-first promise must be obvious
- permission boundaries must be explicit

Today, this artifact is mostly absent.
The concept is strong.
The packaging layer is not there yet.

### Part 2 — Ontology as AI Memory

Packaging is not memory, but it determines whether memory can become portable.

If the product is truly local-first and ontology-driven, then a user should ultimately be able to carry:

- taxonomy subsets
- knowledge packs
- decision history
- governed preferences

from one machine or deployment to another.

That is memory portability as a product feature.

### Part 3 — How They Work Together

Packaging is where the concepts stop being theory.

- SDK for Humans becomes a usable product
- Ontology as AI Memory becomes a portable local asset

Until this exists, Palette is a powerful system, not yet a downloadable category.

---

## Artifact 13 — Business Model

### Part 1 — SDK for Humans

The revenue model should not sell “AI answers.”
It should sell trusted capability infrastructure for professionals.

That means pricing should map to:

- depth of memory
- number of users sharing judgment space
- governance and audit requirements
- domain packs and support

The more the pricing feels like “assistant credits,” the weaker the SDK thesis becomes.

### Part 2 — Ontology as AI Memory

The business moat is not generic AI access.
It is memory ownership.

If firms accumulate:

- structured judgment history
- domain-specific ontology refinements
- internal patterns and precedents

inside a portable local system, then the real asset is the memory layer, not the model layer.

That is strategically important.

### Part 3 — How They Work Together

The clean commercial story is:

- subscription gives you a local capability environment
- continued use compounds a proprietary memory asset for your firm

That is stronger than selling “legal AI.”
It is closer to selling a governed judgment operating environment.

---

## Bottom Line

These two concepts are not parallel ideas.
They are the same system seen from two angles.

`SDK for Humans` is the product lens.
It says:

- the person is the builder
- the system should leave them more capable

`Ontology as AI Memory` is the architecture lens.
It says:

- memory must be structured, typed, and governable
- compounding requires stable semantic objects, not just stored text

The strongest version of the thesis is:

> Palette is an SDK for Humans because it stores judgment as ontology-shaped memory.

That is the conceptual center.

Everything else should be evaluated against it:

- Does this artifact make the human more capable?
- Does this artifact strengthen structured memory?
- Does it connect those two things, or does it drift into generic AI product behavior?

That should be the standard going forward.

---

## Next Moves

1. Rewrite the homepage and core pitch around this exact relationship.
2. Build the first-run flow as an SDK bootloader for a human domain.
3. Expose the ontology selectively in user-facing language instead of hiding it entirely.
4. Turn decision history into the visible proof of compounding.
5. Keep every new feature honest: if it does not strengthen capability or structured memory, it is probably noise.
