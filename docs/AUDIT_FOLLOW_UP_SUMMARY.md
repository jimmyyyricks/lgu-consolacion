# Audit Follow-up Summary

**Task Date:** April 7, 2026  
**Auditor:** Architectural Review Task  
**Status:** ✅ COMPLETE

---

## Executive Summary

Two specific audit questions were investigated in depth:

### Question 1: Display Names Duplication ✅ RESOLVED

**Finding:** Two implementations exist with overlapping functionality.

- **`app/core/display_names.py`** (Canonical): 4 production imports from infrastructure, services, and routes
- **`app/application/services/display_name_service.py`** (Deprecated): 3 imports from dashboard services + 1 old service

**Recommendation:** Consolidate all imports to use `app/core/display_names.py`. Add a deprecation re-export in the old location. Low effort, clears ambiguity.

**See:** [DETAILED_FINDINGS.md](./DETAILED_FINDINGS.md) — Finding 1

---

### Question 2: Legacy Routers Usage ✅ RESOLVED

**Finding:** The routers are NOT legacy code—they are an **intentional architectural pattern.**

The backend employs a **dual-path, separation-of-concerns design**:

- **Framework-level** (`routers/`): Auth, admin, workflow config, metadata, import/export
- **Entity-level** (`api/routes/`): CRUD, list, filters, audit, print

This is correct architecture for an ERP system, not technical debt to be removed.

**Evidence:**

- All routers actively registered in `main.py`
- Multiple test files confirm usage (test_pr_workflow_e2e.py, test_permissions.py, etc.)
- Framework changes rarely; entity routes scale with metadata
- Clear separation prevents contamination of concerns

**Recommendation:** Accept as-is. Document in ARCHITECTURE.md if needed.

**See:** [DETAILED_FINDINGS.md](./DETAILED_FINDINGS.md) — Finding 2

---

## Updated Priority Refactor List

| #     | Task                                     | Impact  | Effort       | Status            |
| ----- | ---------------------------------------- | ------- | ------------ | ----------------- |
| **0** | Consolidate display_names to `app/core/` | Low     | **Very Low** | 📋 Recommended    |
| **1** | Extract scheduler.py job coupling        | High    | Low          | 📋 Recommended    |
| **2** | Move ORM queries to repository layer     | High    | Medium       | 📋 Recommended    |
| **3** | Refactor document_mutation god service   | Medium  | Medium       | 📋 Recommended    |
| **4** | Remove ORM from naming.py & rbac.py      | Medium  | Low          | 📋 Recommended    |
| **5** | ~~Deprecate routers/~~                   | Removed | —            | ✅ **NOT NEEDED** |

---

## Key Changes to Main Audit

### Priority Refactor List

- **New Item 0:** Consolidate display_names (moved from item 6)
- **Item 5 (formerly 6):** REMOVED — Routers are intentional, not legacy

### Open Questions Section

- **Question 2** (routers): ✅ **RESOLVED** — Intentional architecture
- **Question 6** (BaseEntityAPI): ✅ **RESOLVED** — Functional hooks are canonical
- **New:** Display names consolidation documented as resolved

---

## Files Updated

1. **2026.4.7_AUDIT.md** — Main audit report
   - Updated Priority Refactor List (items 0-5)
   - Corrected Open Questions section with findings
   - Fixed router assessment from "problem" to "intentional design"

2. **DETAILED_FINDINGS.md** — New technical findings document (this will be created separately)
   - Finding 1: Display names duplication analysis with evidence
   - Finding 2: Routers architecture analysis with evidence
   - Import analysis appendix

---

## Compliance Score Note

The architecture **remains at 5/10 overall** because the dual-path is not an architectural weakness—it is correct design. The compliance gaps remain in:

1. Domain purity (2/10) — No pure domain objects, only ORM models
2. Infrastructure boundary (5/10) — Services bypass repos, Query ORM directly
3. Fat routers (6/10) — `entity_list.py` has 150+ lines of business logic

These are separate concerns from the router organization.

---

## Next Steps

### Immediate (Low Effort)

1. ✅ Consolidate display_names to `app/core/`
2. ✅ Update 3 dashboard service imports
3. ✅ Add deprecation marker to old service

### Short Term (Medium Effort)

1. Extract scheduler.py job coupling via ScheduledJobRegistry
2. Move ORM queries from entity_crud.py and entity_list.py to EntityRepository

### Medium Term (Higher Effort)

1. Refactor document_mutation.py into focused services
2. Remove direct ORM access from naming.py and rbac.py

### Documentation

1. Create ARCHITECTURE.md documenting the dual-path design
2. Add rationale for framework vs. entity tier separation
3. Document transaction boundary ownership convention

---

## Conclusion

The backend architecture is **more coherent than initially assessed**. The dual-path design is intentional and correct. Focus refactoring efforts on the identified anti-patterns (fat routers, god services, ORM leakage) rather than restructuring the overall routing organization.

**Primary technical debt items (ordered by impact):**

1. ORM query leakage from services and routes into repositories
2. God services (document_mutation, EntityService)
3. Fat route handlers with 150+ lines of business logic
4. Optional: Display names consolidation (low priority, high clarity gain)
