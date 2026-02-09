# Palette Taxonomy

Problem classification system with 104 Reusable Intelligence Units (RIUs).

---

## What is the Taxonomy?

The taxonomy classifies problems into RIUs—discrete, reusable problem patterns that help route work to appropriate agents and solutions.

**Current Version**: v1.2 (104 RIUs)

---

## Structure

RIUs are organized into 6 categories matching Palette's prompt matrix:

1. **Intake and Convergence** (RIU-001 to RIU-041)
2. **Architecture and Design** (RIU-042 to RIU-077)
3. **Implementation** (RIU-078 to RIU-088)
4. **Quality and Safety** (RIU-089 to RIU-094)
5. **Operations and Delivery** (RIU-095 to RIU-100)
6. **Adoption and Change** (RIU-101 to RIU-104)

---

## Using the Taxonomy

### Find Your RIU
Browse `releases/v1.2/palette_taxonomy_v1.2.yaml` to find the RIU that matches your problem.

### Route to Agents
Each RIU suggests which agents are typically useful.

### Link to Library
RIUs reference Knowledge Library entries with validated solutions.

---

## Example RIU

```yaml
- riu_id: RIU-042
  name: "Architecture Decision"
  category: "Architecture and Design"
  description: "System design requiring ONE-WAY DOOR awareness"
  typical_agents: ["Argentavis", "Tyrannosaurus"]
  library_entries: ["LIB-015", "LIB-023"]
```

---

## Contributing

See `CONTRIBUTING.md` for how to propose taxonomy refinements based on real usage.
