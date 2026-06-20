# Palette Knowledge Library

Validated solutions to recurring problems (86 questions).

---

## What is the Library?

The Knowledge Library contains validated answers to questions that recur across engagements. Each entry is evidence-based and cites sources.

**Current Version**: v1.2 (86 questions)

---

## Structure

Library entries are linked to RIUs from the taxonomy:

```yaml
- id: LIB-015
  question: "How do I design a scalable API?"
  answer: "Use RESTful principles with versioning..."
  sources: ["Source 1", "Source 2"]
  applicable_rius: ["RIU-042"]
  when_to_use: "When building public-facing APIs"
  when_not_to_use: "For internal microservices with tight coupling"
```

---

## Using the Library

### Search by Question
Browse `v1.2/palette_knowledge_library_v1.2.yaml` for your question.

### Search by RIU
Find your RIU in the taxonomy, then check linked Library entries.

### Validate Applicability
Check "when to use" and "when not to use" sections.

---

## Contributing

See `CONTRIBUTING.md` for how to propose new Library entries.

**Requirements**:
- Evidence-based answer
- Clear applicability guidance
- Sources/citations
- Validated in real usage
