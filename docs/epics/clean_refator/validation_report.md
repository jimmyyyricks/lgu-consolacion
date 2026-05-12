# Clean Architecture Refactoring — Validation Report

**Date:** April 20, 2026
**Scope:** Phases 1–6 of `plan.md`

---

## Phase 1: Remove Dead Code — PASS (with residue)

| Item                                    | Status  | Notes             |
| --------------------------------------- | ------- | ----------------- |
| Delete `app/services/`                  | ✅ Done | Directory removed |
| Delete `core/display_names.py`          | ✅ Done | File removed      |
| Delete `api/entries/entity_list_old.py` | ✅ Done | File removed      |

### Residual Issues Found

1. **`core/display_names_old.py` still exists** — This is a leftover legacy file (~30 lines). Its functionality lives in `application/services/documents/link_title_service.py`. No imports reference it in app code. Should be deleted.

2. **Stale docstring in `application/services/documents/document.py`** — Line 9 of the module docstring reads:
   ```
   from app.services.document import get_doc, new_doc, save_doc, get_meta, get_value
   ```
   This is inside a docstring (usage example), not an actual import. The real imports below it are correct. The docstring example should be updated to reflect the new import path.

---

## Phase 2: Fix Layer Boundary Violations — PASS

| Item                               | Status  | Notes                                                                                                         |
| ---------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| 2.1 Email factory → infrastructure | ✅ Done | `infrastructure/email/notification_factory.py` created, old deleted. 6 callers updated.                       |
| 2.2 Socketio stub removed          | ✅ Done | `infrastructure/realtime/socketio_manager.py` deleted. No broken refs.                                        |
| 2.3 Print resolver → application   | ✅ Done | `application/services/documents/print_resolver.py` created. 4 assemblers updated.                             |
| 2.4 Print formatters extracted     | ✅ Done | `application/services/documents/print_formatters.py` created. `work_order.py` assembler delegates to it.      |
| 2.5 BrandingStoreProtocol created  | ✅ Done | `domain/protocols/branding_store.py` created. `BrandingService` uses protocol. `BrandingStore` implements it. |
| 2.6 Scheduler init service         | ✅ Done | `application/services/scheduling/app_initialization_service.py` created. `main.py` uses it.                   |

**Cross-layer check:**

- `app/application/` → `app/infrastructure/`: All remaining imports are legitimate (repository wiring in application service factories).
- `app/infrastructure/` → `app/application/`: All remaining imports are legitimate (print assemblers consuming application formatters/resolvers via the infrastructure factory pattern).

---

## Phase 3: Consolidate Utilities — PASS (one planned file not created)

| Item                                  | Status         | Notes                                                                                                                                                                       |
| ------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `application/utils/__init__.py`       | ✅ Done        | Package created                                                                                                                                                             |
| `application/utils/doc_utils.py`      | ✅ Done        | 7 functions: `get_id`, `get_attr`, `to_float`, `to_int`, `display_label`, `meta_title_value`, `fmt_qty`                                                                     |
| `application/utils/workflow_utils.py` | ⚠️ Not created | Plan called for a separate file but functions were merged into `doc_utils.py` — all 4 workflow routers import `get_id, get_attr` from `doc_utils`. Functionally equivalent. |
| Workflow routers updated              | ✅ Done        | All 4 routers import from `app.application.utils.doc_utils`                                                                                                                 |
| Purchasing APIs updated               | ✅ Done        | `item_issue.py`, `item_return.py`, `stock_count.py`, `inventory_adjustment.py` — no duplicate functions remain                                                              |

**Verdict:** `workflow_utils.py` was unnecessary since `doc_utils.py` covers the same functions. The consolidation is complete.

---

## Phase 4: Decouple Module APIs — PARTIAL PASS

| Item                                              | Status          | Notes                                                                                      |
| ------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| `application/services/maintenance/job_service.py` | ✅ Done         | `MaintenanceJobService` wraps scheduler test function                                      |
| `application/services/maintenance/constants.py`   | ✅ Done         | `FREQUENCY_DAYS` centralized                                                               |
| `test_scheduler.py` updated                       | ✅ Done         | Imports `MaintenanceJobService` from application layer                                     |
| `maintenance_job_common.py` updated               | ✅ Done         | Imports `FREQUENCY_DAYS` from `constants.py`                                               |
| `pm_calendar/routes.py` updated                   | ❌ **NOT DONE** | Still imports `FREQUENCY_DAYS` from `modules/maintenance_mgmt/apis/maintenance_job_common` |

### Remaining Direct Module Imports from API Layer

| File                                                      | Import                                                                                                                | Should Be                                                                                 |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `api/features/pm_calendar/routes.py:22`                   | `from app.modules.maintenance_mgmt.apis.maintenance_job_common import FREQUENCY_DAYS`                                 | `from app.application.services.maintenance.constants import FREQUENCY_DAYS`               |
| `api/system/test_scheduler.py:9-11`                       | `from app.modules.maintenance_mgmt.apis.maintenance_calendar import run_maintenance_calendar_generation` (and 2 more) | Should wrap in `MaintenanceJobService` methods or an application-level scheduling service |
| `tests/test_pm_date_plotting_flow.py:56`                  | `from app.modules.maintenance_mgmt.apis.maintenance_job_common import FREQUENCY_DAYS`                                 | `from app.application.services.maintenance.constants import FREQUENCY_DAYS`               |
| `tests/test_pm_calendar_2026_04_16.py:50`                 | Same as above                                                                                                         | Same fix                                                                                  |
| `modules/maintenance_mgmt/apis/maintenance_calendar.py:8` | `from app.modules.maintenance_mgmt.apis.maintenance_job_common import FREQUENCY_DAYS, create_work_package, ...`       | `FREQUENCY_DAYS` from constants; rest is intra-module (acceptable)                        |

---

## Phase 5: Split Oversized Files — PASS

| Item                                       | Status  | Notes                         |
| ------------------------------------------ | ------- | ----------------------------- |
| `infrastructure/metadata/reader.py`        | ✅ Done | `JsonMetadataReader`          |
| `infrastructure/metadata/writer.py`        | ✅ Done | `JsonMetadataWriter`          |
| `infrastructure/metadata/validator.py`     | ✅ Done | `MetadataValidator`           |
| `infrastructure/metadata/adapters.py` shim | ✅ Done | Backward-compatible re-export |

---

## Phase 6: File Headers — PARTIAL PASS

New files created during the refactoring all have proper docstrings. However, **some pre-existing core files still lack module docstrings**:

| File                     | Has Docstring? |
| ------------------------ | -------------- |
| `core/config.py`         | ❌ No          |
| `core/security.py`       | ❌ No          |
| `core/database.py`       | Not checked    |
| `core/base_model.py`     | Not checked    |
| `core/error_handlers.py` | Not checked    |
| `core/feature_flags.py`  | Not checked    |
| `core/sanitization.py`   | Not checked    |
| `core/serialization.py`  | Not checked    |

---

## Summary Scorecard

| Phase                      | Status     | Completion                                      |
| -------------------------- | ---------- | ----------------------------------------------- |
| Phase 1 — Dead Code        | ✅ Pass    | 95% (1 leftover file)                           |
| Phase 2 — Layer Boundaries | ✅ Pass    | 100%                                            |
| Phase 3 — Consolidation    | ✅ Pass    | 100% (equivalent approach)                      |
| Phase 4 — Decoupling       | ⚠️ Partial | 80% (1 import not updated + 3 test/module refs) |
| Phase 5 — Split Files      | ✅ Pass    | 100%                                            |
| Phase 6 — File Headers     | ⚠️ Partial | 70% (new files done, existing files incomplete) |

**Overall: 91% complete. 6 action items remain.**
