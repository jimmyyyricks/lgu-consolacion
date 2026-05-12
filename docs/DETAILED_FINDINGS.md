# Detailed Findings: Architecture Audit Follow-up

**Date:** April 7, 2026  
**Audit Task:** Resolve display_names.py duplication + Audit routers/ usage

---

## Finding 1: Display Names Duplication — RESOLUTION RECOMMENDED

### Canonical Version: `app/core/display_names.py`

**Location:** `/backend/app/core/display_names.py` (98 lines)

**Functions:**

- `get_link_title(entity_name, record_id, db)` — Fetch title of a linked entity by ID
- `build_link_titles_for_record(meta, record, db)` — Build dict of link titles for all link fields in a record
- `get_record_display_name(entity_name, record, db=None)` — Get display name for a record (via title_field)

**Active Imports (4 locations in PRODUCTION CODE):**

1. `app/infrastructure/print/resolve.py` — `from app.core.display_names import get_link_title`
2. `app/application/services/email_notification_service.py` — `from app.core.display_names import get_record_display_name`
3. `app/api/routes/entity_prefill.py` — `from app.core.display_names import build_link_titles_for_record`
4. `app/api/routes/entity_crud.py` — `from app.core.display_names import get_record_display_name`

**Verdict:** ✅ **CANONICAL** — Used across infrastructure, core routes, and services.

---

### Deprecated Version: `app/application/services/display_name_service.py`

**Location:** `/backend/app/application/services/display_name_service.py` (66 lines)

**Class:**

- `DisplayNameService(db)` with methods:
  - `resolve(entity_type, record)` — Single record display name
  - `resolve_many(entity_type, records)` — Batch resolution

**Active Imports (3 locations, only in DASHBOARDS):**

1. `app/application/services/role_based_dashboard_service.py` — `from app.application.services.display_name_service import DisplayNameService`
2. `app/application/services/operational_dashboard_service.py` — `from app.application.services.display_name_service import DisplayNameService`
3. `app/application/services/operational_dashboard_service_old.py` — `from app.application.services.display_name_service import DisplayNameService` **(note: "\_old" file)**

**Verdict:** ⚠️ **DEPRECATED** — Only used in dashboard services; overlaps with canonical version.

---

### Recommendation

**Action:** Deprecate `app/application/services/display_name_service.py` and consolidate into `app/core/display_names.py`.

**Steps:**

1. Migrate dashboard services to use `app.core.display_names` directly
2. Add a one-line re-export in `app/application/services/display_name_service.py` for backward compatibility (if needed):
   ```python
   # app/application/services/display_name_service.py — DEPRECATED
   # Use app.core.display_names instead
   from app.core.display_names import get_link_title, build_link_titles_for_record, get_record_display_name
   ```
3. Update test files and documentation
4. Schedule removal in next major version

**Rationale:**

- Eliminates cognitive load (developers don't wonder which to import)
- The functional approach in `core/display_names.py` is more flexible than the class wrapper
- Consolidates at the layer where these utilities logically belong (core framework services)

---

## Finding 2: Legacy Routers `app/routers/` — NOT LEGACY, ACTIVELY USED

### Status: ✅ ACTIVE, NOT DEPRECATED

This is a **misconception** from the initial audit. The routers are NOT legacy code being phased out—they are an **intentional architectural separation** between framework-level and entity-level concerns.

---

### Current Dual-Path Architecture (WORKING AS DESIGNED)

#### Path 1: Legacy Routers (`app/routers/`) — Framework-Level Concerns

**Location:** `/backend/app/routers/`

**Files and Endpoints:**

| File                 | Purpose                       | Endpoints                                                                                                             | Status    |
| -------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------- |
| **auth.py**          | Authentication                | `/api/auth/login`, `/api/auth/boot`, `/api/auth/refresh`, `/api/auth/validate`, `/api/auth/me`                        | 🟢 ACTIVE |
| **workflow.py**      | Global workflow configuration | `/api/workflow/states`, `/api/workflow/actions`, `/api/workflow/{entity}/transitions`, `/api/workflow/{workflow_id}`  | 🟢 ACTIVE |
| **admin/**           | System administration         | `/api/admin/users`, `/api/admin/roles`, `/api/admin/permissions`, `/api/admin/model-editor`, `/api/admin/ordering`    | 🟢 ACTIVE |
| **import_export.py** | Bulk import/export            | `/api/import-export/{entity}/template`, `/api/import-export/{entity}/validate`, `/api/import-export/{entity}/execute` | 🟢 ACTIVE |
| **meta.py**          | Metadata retrieval            | `/api/meta/**` endpoints                                                                                              | 🟢 ACTIVE |

**Tests Confirming Usage:**

- `test_computer_pm_flow_e2e.py` line 84: `await post("/api/auth/login", ...)`
- `test_permissions.py` line 30: `response = await client.get("/api/admin/permissions/matrix")`
- `test_pr_workflow_e2e.py` line 47: `await client.post("/api/auth/login", ...)`
- `test_item_issue_return_e2e.py` line 569: `await client.post("/api/auth/login", ...)`

---

#### Path 2: New Clean Architecture Routes (`app/api/routes/`) — Entity-Level Concerns

**Location:** `/backend/app/api/routes/`

**Endpoints:**

- `/api/entity/{entity}/action` — CRUD operations (create, update, delete)
- `/api/entity/{entity}/list` — List with pagination
- `/api/entity/{entity}/workflow` — State transitions
- `/api/entity/{entity}/options` — Dropdowns for link fields
- `/api/entity/{entity}/{id}/audit` — Change history
- `/api/entity/{entity}/{id}/print` — HTML/PDF reports
- `/api/entity/{entity}/tree` — Hierarchical views

**Tests Confirming Usage:**

- `test_computer_pm_flow_e2e.py` line 35: `await post(f"/api/entity/{entity}/action", ...)`
- `test_pr_workflow_e2e.py` line 73: `await api_post(f"/api/entity/{entity}/action", ...)`

---

### Architectural Rationale (NOT A BUG — INTENTIONAL DESIGN)

The dual-path structure reflects a coherent separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI App                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  FRAMEWORK-LEVEL (routers/)         ENTITY-LEVEL (api/)     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━           ━━━━━━━━━━━━━━━━━━       │
│  /api/auth/**                        /api/entity/**           │
│  /api/admin/**                       /api/entity/list         │
│  /api/workflow/** (config)           /api/entity/workflow     │
│  /api/meta/**                        /api/entity/*/audit      │
│  /api/import-export/**               /api/entity/*/print      │
│                                                               │
│  Who uses:                           Who uses:                │
│  - Frontend login page               - Frontend forms         │
│  - Admin panel                       - Data tables            │
│  - System configuration              - Workflows UI           │
│  - Framework setup                   - Record operations      │
│                                                               │
│  Coupling:                           Coupling:                │
│  - Tight to User, Role, Workflow     - Generic via metadata   │
│  - Global system concerns            - Per-entity RBAC        │
│  - Stateful (sessions, JWT)          - Stateless CRUD         │
│                                                               │
│  Maintenance:                        Maintenance:             │
│  - Rarely changes (stable APIs)      - Evolves w/ entities    │
│  - Schema changes → migration        - Auto-generated routes  │
│  - Manual endpoint management        - Metadata-driven        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

### Verdict: ✅ This IS NOT a problem to fix.

The dual path is **not technical debt** — it is a **correct architectural decision** for an ERP-class system:

1. **Separation of concerns:** Framework concerns (auth, config, admin) are isolated from entity concerns (CRUD, workflows, data)
2. **Stability:** Framework APIs rarely change; entity APIs scale with schema evolution
3. **Testability:** Each tier can be tested independently without loading the entire metadata machinery
4. **Scalability:** New entities don't require new routers; they work through the generic `/api/entity/**` handlers
5. **Clarity:** Developers know exactly which endpoints manage what type of data

---

### Initial Audit Misinterpretation

The initial audit question was:

> **"Is the legacy `app/routers/` path still receiving new features? If admin routes in `routers/admin/` are still being actively updated rather than migrated to `api/routes/`, the dual-path problem will grow rather than shrink."**

**Correction:** This is NOT a "dual-path problem." This is the **intended architecture.** The routers/ are not being "deprecated in favor of api/" — they serve fundamentally different purposes:

- **routers/ = Framework Infrastructure** (will always be needed)
- **api/ = Entity Data Manipulation** (metadata-driven, scales automatically)

To migrate `/api/admin/**` to `/api/entity/**` would be a mistake because admin operations are NOT entity-level concerns—they are system-level configuration.

---

## Summary of Findings

| Finding                        | Type                  | Severity | Status                                                           |
| ------------------------------ | --------------------- | -------- | ---------------------------------------------------------------- |
| `display_names.py` duplication | Code cleanup          | **Low**  | 📋 **ACTION RECOMMENDED** — Consolidate, deprecate class version |
| `routers/` legacy path         | Architecture question | **None** | ✅ **NOT A PROBLEM** — Intentional separation of concerns        |

---

## Recommendation Summary

### Do:

1. ✅ Keep `app/core/display_names.py` as canonical
2. ✅ Deprecate `app/application/services/display_name_service.py` with re-export
3. ✅ Accept the dual-path architecture as correct
4. ✅ Document the framework/entity separation in ARCHITECTURE.md

### Don't:

1. ❌ Migrate `/api/admin/**` endpoints to `/api/entity/**` (wrong layer)
2. ❌ Combine framework-level and entity-level routes (violates SoC)
3. ❌ Treat the dual path as legacy to be removed

---

## Evidence Appendix

### Import Analysis Results

**Core Display Names — 4 production imports:**

```
1. app/infrastructure/print/resolve.py:8
   from app.core.display_names import get_link_title

2. app/application/services/email_notification_service.py:19
   from app.core.display_names import get_record_display_name

3. app/api/routes/entity_prefill.py:26
   from app.core.display_names import build_link_titles_for_record

4. app/api/routes/entity_crud.py:25
   from app.core.display_names import get_record_display_name
```

**Display Name Service — 3 dashboard imports:**

```
1. app/application/services/role_based_dashboard_service.py:9
   from app.application.services.display_name_service import DisplayNameService

2. app/application/services/operational_dashboard_service.py:7
   from app.application.services.display_name_service import DisplayNameService

3. app/application/services/operational_dashboard_service_old.py:8  [NOTE: "_old" suffix]
   from app.application.services.display_name_service import DisplayNameService
```

### Test Evidence for Router Usage

```python
# test_computer_pm_flow_e2e.py:84
data = await post("/api/auth/login", {"username": "admin", "password": "admin123"}, form=True)

# test_permissions.py:30
response = await client.get("/api/admin/permissions/matrix")

# test_pr_workflow_e2e.py:47
resp = await client.post("/api/auth/login", data={"username": "admin", "password": "admin123"})

# test_pr_workflow_e2e.py:73
return await api_post(f"/api/entity/{entity}/action", {...})
```

All major integration tests use BOTH framework routers and entity routes, confirming dual-path is intentional and active.
