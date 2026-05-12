# Plan: Backend Clean Architecture Restructuring

## TL;DR

Audit found 8.5/10 clean architecture score with 6 fixable critical violations, 7 sets of duplicated utility functions, dead code directories, and missing file headers. Plan reorganizes files to proper layers, consolidates duplicates, and adds developer-facing docstrings.

---

## Phase 1: Remove Dead Code & Deprecated Files

1.1 Delete `app/services/` directory — completely empty (only `__init__.py`), real services live in `app/application/services/`
1.2 Delete `core/display_names.py` — marked as legacy re-export with TODO to remove; update any remaining imports to point directly to `app/application/services/documents/link_title_service`
1.3 Check & remove `api/entries/entity_list_old.py` — suspected dead code; confirm no routes reference it before deleting

**Relevant files:**

- `backend/app/services/__init__.py`
- `backend/app/core/display_names.py`
- `backend/app/api/entries/entity_list_old.py` (verify first)

---

## Phase 2: Fix Critical Layer Boundary Violations

### 2.1 Move email notification factory from Application → Infrastructure

**Problem:** `application/email_notifications/factory.py` imports `SmtpEmailService` and `JinjaEmailTemplateRenderer` — infrastructure in application layer.
**Fix:** Move file to `infrastructure/email/notification_factory.py`. Update all callers (hooks, api/dependencies.py).

### 2.2 Remove socketio stub in Infrastructure layer

**Problem:** `infrastructure/realtime/socketio_manager.py` just re-exports from `application/services/notifications/socketio.py` — wrong direction (infra → app).
**Fix:** Delete the stub. Update all callers to import directly from `application/services/notifications/socketio`.

### 2.3 Move print resolver from Infrastructure → Application

**Problem:** `infrastructure/print/resolve.py` imports `DocumentAppService` from application layer — inverted dependency.
**Fix:** Move to `application/services/documents/print_resolver.py`. Update `infrastructure/print/` to depend only on repositories.

### 2.4 Extract business logic from Infrastructure print assemblers → Application

**Problem:** `infrastructure/print/assemblers/work_order.py` contains domain formatting logic (`_get_priority_description()`, display text constants) — business logic in infrastructure.
**Fix:** Create `application/services/documents/print_formatters.py` containing all display/formatting logic. `work_order.py` assembler delegates to it.

### 2.5 Create BrandingStoreProtocol in Domain layer

**Problem:** `application/services/branding_service.py` imports concrete `BrandingStore` from infrastructure — violates Dependency Inversion.
**Fix:** Create `domain/protocols/branding_store.py` with `BrandingStoreProtocol`. Update `BrandingService` to depend on the protocol. `infrastructure/settings/branding_store.py` implements it.

### 2.6 Move scheduler initialization out of main.py

**Problem:** `app/main.py` lifespan function directly instantiates `SchedulerAdapter` from infrastructure.
**Fix:** Create `application/services/scheduling/app_initialization_service.py` that wires the scheduler. `main.py` calls only the application service.

**Relevant files:**

- `backend/app/application/email_notifications/factory.py` → moves to `backend/app/infrastructure/email/notification_factory.py`
- `backend/app/infrastructure/realtime/socketio_manager.py` → delete
- `backend/app/infrastructure/print/resolve.py` → moves to `backend/app/application/services/documents/print_resolver.py`
- `backend/app/infrastructure/print/assemblers/work_order.py` — extract formatting logic
- `backend/app/domain/protocols/branding_store.py` — new file
- `backend/app/application/services/branding_service.py` — update import
- `backend/app/main.py` — scheduler wiring
- `backend/app/api/dependencies.py` — update factory imports

---

## Phase 3: Consolidate Duplicated Utility Functions

7 sets of private helper functions duplicated across module `apis/` files. Create two shared utility modules.

### 3.1 Create `application/utils/doc_utils.py`

Merge the following repeated helpers from `purchasing_stores/` and `maintenance_mgmt/`:

- `_get_id(doc)` — present in 6+ files
- `_get_attr(doc, attr)` — present in 6+ files
- `_to_float(val)` — present in 3+ files
- `_to_int(val)` — present in 2+ files
- `_display_label(*values)` — item_issue.py, item_return.py
- `_meta_title_value(entity, doc)` — item_issue.py, item_return.py
- `_fmt_qty(value)` — item_issue.py, item_return.py

Update all callers to `from app.application.utils.doc_utils import get_id, get_attr, ...`

### 3.2 Create `application/utils/workflow_utils.py`

Extract `_get_id()` and `_get_attr()` that are duplicated across all 4 workflow routers:

- `modules/maintenance_mgmt/workflow_router.py`
- `modules/asset_management/workflow_router.py`
- `modules/purchasing_stores/workflow_router.py`
- `modules/work_mgmt/workflow_router.py`

**Relevant files:**

- New: `backend/app/application/utils/__init__.py`
- New: `backend/app/application/utils/doc_utils.py`
- New: `backend/app/application/utils/workflow_utils.py`
- Update: all `modules/*/apis/` files and `modules/*/workflow_router.py`

---

## Phase 4: Decouple Module APIs from API Layer

### 4.1 Create `application/services/maintenance/job_service.py`

**Problem:** `api/system/test_scheduler.py` imports directly from `modules/maintenance_mgmt/apis/` — API layer bypassing application service.
**Fix:** Wrap `maintenance_job_common` utilities in a proper `MaintenanceJobService`. API layer calls the service.

### 4.2 Move `FREQUENCY_DAYS` constant to proper location

**Problem:** `api/features/pm_calendar/routes.py` imports `FREQUENCY_DAYS` constant from `modules/maintenance_mgmt/apis/maintenance_job_common.py` — API leaks into module internals.
**Fix:** Move constant to `application/services/maintenance/constants.py` or `domain/` enum. Both pm_calendar route and maintenance_job_common import from there.

**Relevant files:**

- New: `backend/app/application/services/maintenance/job_service.py`
- New: `backend/app/application/services/maintenance/constants.py`
- Update: `backend/app/api/system/test_scheduler.py`
- Update: `backend/app/api/features/pm_calendar/routes.py`
- Update: `backend/app/modules/maintenance_mgmt/apis/maintenance_job_common.py`

---

## Phase 5: Split Oversized Files

### 5.1 Split `infrastructure/metadata/adapters.py` (~600 lines)

Single file combines JsonMetadataReader + JsonMetadataWriter + MetadataValidator.
Split into:

- `infrastructure/metadata/reader.py` — `JsonMetadataReader`
- `infrastructure/metadata/writer.py` — `JsonMetadataWriter`
- `infrastructure/metadata/validator.py` — `MetadataValidator`
- `infrastructure/metadata/adapters.py` — keep as re-export shim for backward compat

**Relevant files:**

- `backend/app/infrastructure/metadata/adapters.py` → split into 3
- All callers of `from app.infrastructure.metadata.adapters import ...`

---

## Phase 6: Add File Header Comments

Add module-level docstrings to all Python files that are missing them. Each docstring should state:

1. What the file is (layer, responsibility)
2. What it does (key classes/functions)
3. Clean Architecture layer it belongs to

Priority order: domain/, application/, infrastructure/ core files, api/dependencies.py, modules/_/apis/_.py

---

## Verification Steps

1. Run existing test suite: `cd backend && pytest tests/ -v --tb=short` — all tests should pass after each phase
2. Check for import cycles: `python -c "import app.main"` — no ImportError
3. Verify no remaining cross-layer imports: `grep -r "from app.infrastructure" app/application/` should only show factory.py (after move) and protocol implementations
4. Verify `grep -r "from app.application" app/infrastructure/` returns 0 results after Phase 2
5. Confirm dead code removed: `python -c "from app.services import *"` should fail (directory deleted)
6. Run application startup: `uvicorn app.main:app --reload` and hit `/health`

---

## Decisions

- **Scope**: Restructuring plan only — no new features, no schema changes, no Alembic migrations
- **Excluded**: Frontend, alembic migrations, test files (tests may need import path updates)
- **`entity_list_old.py`**: Verify before deleting (may have active references)
- **`socketio_manager.py` stub**: Delete (inverse dependency anti-pattern); callers update imports
- **Phase order matters**: Phase 2 must complete before Phase 3/4 to avoid chasing moving targets

## Further Considerations

1. **Test import updates**: After Phase 2-4, test files that import from moved modules will need updating — recommend doing a global import path search per phase
2. **`_MODEL_CACHE` in entity_repository.py**: Noted as potential memory risk but low priority — add a comment noting to use WeakValueDictionary if models are hot-reloaded
3. **Event bus production readiness**: `domain_event_bus.py` lacks retry/backoff — document as technical debt comment in file header
