# Clean Architecture Refactoring — Follow-Up Plan

**Date:** April 20, 2026
**Status:** ✅ ALL TASKS COMPLETED — April 20, 2026
**Prerequisite:** Phases 1–6 from `plan.md` (100% complete)

---

## Priority 1: Fix Remaining Gaps from Original Plan

These are incomplete items from the original 6 phases that must be closed first.

### 1.1 Delete `core/display_names_old.py`

**Why:** Leftover legacy file. No app code imports it. Functionality lives in `application/services/documents/link_title_service.py`.

**Action:** Delete the file.

**Files:**

- Delete: `backend/app/core/display_names_old.py`

---

### 1.2 Fix `pm_calendar/routes.py` FREQUENCY_DAYS import

**Why:** API layer still imports directly from module internals. The constant was already centralized in Phase 4 but this caller was missed.

**Action:** Change line 22 from:

```python
from app.modules.maintenance_mgmt.apis.maintenance_job_common import FREQUENCY_DAYS
```

to:

```python
from app.application.services.maintenance.constants import FREQUENCY_DAYS
```

**Files:**

- Update: `backend/app/api/features/pm_calendar/routes.py`

---

### 1.3 Fix test files importing FREQUENCY_DAYS from module

**Why:** Tests should also use the centralized constant path for consistency.

**Action:** Update these files:

- `tests/test_pm_date_plotting_flow.py:56` → `from app.application.services.maintenance.constants import FREQUENCY_DAYS`
- `tests/test_pm_calendar_2026_04_16.py:50` → same

**Files:**

- Update: `backend/tests/test_pm_date_plotting_flow.py`
- Update: `backend/tests/test_pm_calendar_2026_04_16.py`

---

### 1.4 Update stale docstring example in `document.py`

**Why:** The usage example in the docstring references deleted `app.services.document`. Not a runtime error, but misleading for developers.

**Action:** Update the docstring in `application/services/documents/document.py` line 9:

```python
# Old:
#     from app.services.document import get_doc, new_doc, save_doc, get_meta, get_value
# New:
#     from app.application.services.documents.document import get_doc, new_doc, save_doc, get_meta, get_value
```

**Files:**

- Update: `backend/app/application/services/documents/document.py`

---

### 1.5 Add missing file header docstrings to core files

**Why:** Phase 6 added headers to new files but missed pre-existing core files.

**Action:** Add module-level docstrings to:

- `core/config.py` — "Core Layer: Application Settings. Pydantic-based configuration from environment variables."
- `core/security.py` — "Core Layer: Authentication & Security. JWT token handling, password hashing, current user extraction."
- `core/database.py` — "Core Layer: Database Setup. SQLAlchemy async engine, session factory, and Base model."
- `core/base_model.py` — "Core Layer: Base ORM Model. Common columns (id, created_at, updated_at) for all entities."
- `core/error_handlers.py` — "Core Layer: Error Handling. Decorator and utilities for consistent API error responses."
- `core/feature_flags.py` — "Core Layer: Feature Flags. Runtime feature toggles (e.g., Purchase Order module)."
- `core/sanitization.py` — "Core Layer: Input Sanitization. XSS prevention via regex-based string cleaning."
- `core/serialization.py` — "Core Layer: Serialization. Model-to-dict conversion with polymorphic field handling."
- `core/loader.py` — "Core Layer: Module Loader. Dynamic discovery and import of business modules."
- `core/seed.py` — "Core Layer: Seed Facade. Entry point for running all database seeders."

**Files:**

- Update: 10 files in `backend/app/core/`

---

## Priority 2: Deepen Module API Decoupling

The original plan partially decoupled `test_scheduler.py` from module internals. Three `run_*` functions are still imported directly from modules.

### 2.1 Wrap remaining scheduler functions in `MaintenanceJobService`

**Why:** `api/system/test_scheduler.py` still imports `run_maintenance_calendar_generation`, `run_maintenance_condition_generation`, and `run_maintenance_interval_generation` directly from `modules/maintenance_mgmt/apis/`. This bypasses the application service layer.

**Action:** Add methods to `application/services/maintenance/job_service.py`:

```python
async def run_calendar_generation(self):
    from app.modules.maintenance_mgmt.apis.maintenance_calendar import run_maintenance_calendar_generation
    await run_maintenance_calendar_generation()

async def run_condition_generation(self):
    from app.modules.maintenance_mgmt.apis.maintenance_condition import run_maintenance_condition_generation
    await run_maintenance_condition_generation()

async def run_interval_generation(self):
    from app.modules.maintenance_mgmt.apis.maintenance_interval import run_maintenance_interval_generation
    await run_maintenance_interval_generation()
```

Update `test_scheduler.py` to call `MaintenanceJobService` methods instead.

**Files:**

- Update: `backend/app/application/services/maintenance/job_service.py`
- Update: `backend/app/api/system/test_scheduler.py`

---

### 2.2 Move `create_work_package` and `log_job` to application service

**Why:** `maintenance_job_common.py` contains shared orchestration logic (`create_work_package`, `log_job`, `format_error_trace`) that is called by multiple module APIs. These are application-level orchestration concerns, not module-internal business logic.

**Action:** Move `create_work_package`, `log_job`, `format_error_trace` from `maintenance_job_common.py` into `MaintenanceJobService`. Update callers in:

- `modules/maintenance_mgmt/apis/maintenance_calendar.py`
- `modules/maintenance_mgmt/apis/maintenance_condition.py`
- `modules/maintenance_mgmt/apis/maintenance_interval.py`

After this, `maintenance_job_common.py` can be deleted (all its content will have been migrated).

**Files:**

- Update: `backend/app/application/services/maintenance/job_service.py`
- Update: 3 module API files
- Delete: `backend/app/modules/maintenance_mgmt/apis/maintenance_job_common.py` (after migration)

---

## Priority 3: Remaining Print Module Cleanup

### 3.1 Verify all print assemblers use application-layer formatters

**Why:** Phase 2.4 extracted formatters for work_order assembler. Other assemblers (incident, purchase_request, purchase_order) may also contain inline formatting logic.

**Action:** Audit these files for any remaining business logic:

- `infrastructure/print/assemblers/incident.py`
- `infrastructure/print/assemblers/purchase_request.py`
- `infrastructure/print/assemblers/purchase_order.py`

If formatting logic is found, extract to `print_formatters.py`.

**Files:**

- Audit: 3 files in `backend/app/infrastructure/print/assemblers/`
- Possibly update: `backend/app/application/services/documents/print_formatters.py`

---

## Priority 4: Architecture Documentation Updates

### 4.1 Update `ARCHITECTURE_VISUAL_GUIDE.md`

**Why:** The doc references `display_names_old.py` and old file locations. Should reflect the new structure.

**Files:**

- Update: `docs/ARCHITECTURE_VISUAL_GUIDE.md`

### 4.2 Update `.windsurf/rules/backend-dev-tools.md`

**Why:** Contains import examples using deleted `app.services.document` path.

**Files:**

- Update: `.windsurf/rules/backend-dev-tools.md`

---

## Priority 5: Verification

### 5.1 Run full test suite

```bash
cd backend && pytest tests/ -v --tb=short
```

### 5.2 Check import integrity

```bash
cd backend && python -c "import app.main"
```

### 5.3 Verify no cross-layer violations remain

```bash
cd backend
# Application should not import infrastructure directly (except via factory wiring)
grep -rn "from app.infrastructure" app/application/ | grep -v "__pycache__"

# Infrastructure should not import application (except print assemblers using formatters/resolver)
grep -rn "from app.application" app/infrastructure/ | grep -v "__pycache__"
```

### 5.4 Start the server

```bash
cd backend && uvicorn app.main:app --reload
# Hit GET /api/health
```

---

## Execution Order

1. **Priority 1** (1.1–1.5): Quick fixes, ~30 minutes. Can be done in a single commit.
2. **Priority 2** (2.1–2.2): Module decoupling deepening, ~1–2 hours.
3. **Priority 3** (3.1): Audit only, ~30 minutes. Code changes if needed.
4. **Priority 4** (4.1–4.2): Doc updates, ~15 minutes.
5. **Priority 5** (5.1–5.4): Verification, ~15 minutes.

**Total estimated effort: 3–4 hours**

---

## Out of Scope (Noted for Future)

- `_MODEL_CACHE` in `entity_repository.py` — use `WeakValueDictionary` if hot-reload is needed
- `domain_event_bus.py` — lacks retry/backoff for production (document as tech debt)
- `schemas/` directory — contains only re-export shims; could be deleted if all callers are updated
- `infrastructure/realtime/` directory — may now be empty after socketio stub removal; delete if so
