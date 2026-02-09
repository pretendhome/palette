# Knowledge Library → Taxonomy v1.2 Mapping Report

**Date**: 2026-01-29  
**Status**: MAPPING COMPLETE WITH ISSUES

---

## Summary

- **Library entries**: 86 questions
- **Taxonomy v1.2 RIUs**: 104 RIUs
- **Library references**: 67 unique RIUs
- **Phantom RIUs found**: 9 (referenced but don't exist in any taxonomy version)

---

## Phantom RIUs (Need Resolution)

These RIUs are referenced in library answers/mappings but don't exist in v1.0, v1.1, or v1.2:

| Phantom RIU | Referenced In | Context | Recommended Action |
|-------------|---------------|---------|-------------------|
| RIU-042 | LIB-001, LIB-005, LIB-006, LIB-007, LIB-008 | Stakeholder management | Remove (covered by RIU-002) |
| RIU-043 | Multiple entries | Unknown | Remove |
| RIU-044 | Multiple entries | Unknown | Remove |
| RIU-045 | Multiple entries | Unknown | Remove |
| RIU-055 | Multiple entries | Unknown | Remove |
| RIU-072 | Multiple entries | Unknown | Remove |
| RIU-074 | Multiple entries | Unknown | Remove |
| RIU-075 | Multiple entries | Unknown | Remove |
| RIU-141 | Multiple entries | Unknown | Remove |

---

## Analysis

**Root cause**: Library was created referencing RIUs that were either:
1. Planned but never implemented
2. Removed during taxonomy refinement
3. Incorrectly numbered during library creation

**Impact**: 
- Library entries are still valuable (answers are comprehensive)
- RIU mappings are incomplete but not broken
- Existing RIU references (RIU-001, RIU-002, etc.) are valid

---

## Recommended Actions

### Option A: Remove Phantom References (Quick Fix)
- Remove phantom RIUs from `related_rius` arrays
- Keep answers intact (they reference RIUs in text, which is fine)
- Result: Clean mappings, no broken references

### Option B: Map to Equivalent v1.2 RIUs (Comprehensive)
- Research what each phantom RIU was supposed to be
- Find equivalent RIUs in v1.2
- Update mappings
- Result: Tighter integration, more work

### Option C: Add Missing RIUs to v1.2 (Complete)
- Determine what phantom RIUs should be
- Add them to taxonomy v1.2 → v1.3
- Result: Perfect mapping, significant work

---

## Recommendation: Option A (Remove Phantom References)

**Rationale**:
- Library answers are comprehensive without phantom RIUs
- Existing RIU references (RIU-001, RIU-002, RIU-003, etc.) provide sufficient mapping
- Phantom RIUs add no value if they don't exist in taxonomy
- Quick fix enables immediate use

**Implementation**:
- Create `palette_knowledge_library_v1_0_v1.2_mapped.yaml`
- Remove phantom RIUs from `related_rius` arrays only
- Keep answer text unchanged (mentions of RIUs in prose are fine)
- Update metadata to indicate v1.2 mapping

---

## Validation

After cleanup:
- ✓ All `related_rius` references point to valid v1.2 RIUs
- ✓ 86 questions remain intact
- ✓ Answers unchanged
- ✓ Sources preserved
- ✓ Ready for production use

---

## Next Steps

1. Approve Option A (remove phantom references)
2. Create cleaned library file
3. Update library metadata (version, mapping date)
4. Move to `/home/mical/palette/knowledge-library/v1.2/`
5. Update README to reference v1.2 taxonomy

---

**Status**: AWAITING APPROVAL
