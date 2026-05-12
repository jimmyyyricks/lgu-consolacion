This finalized report incorporates the **Frappe-inspired multi-root architecture**, integrates the **Metadata Sync Service (MSS)** requirements, and enforces the **"Developer-Only"** editing constraint for core entities.

---

# 🛠️ Finalized Core Framework Entity Audit Report

**Story:** 1. Audit & Map Current Entity Distribution  
**Date:** 2026-04-06  
**Status:** FINALIZED / READY FOR IMPLEMENTATION

## 1. Executive Summary

To achieve a Frappe-inspired architecture, we are decoupling **Core Framework Entities** (the "System App") from **Module-Specific Entities** (the "Installable Apps"). This consolidation moves core infrastructure out of the general `models` directory into a protected `core/framework` namespace.

While these entities remain visible to the system and accessible to the frontend, they are strictly **Developer-Only** for editing to prevent end-users from compromising system integrity.

---

## 2. Target Multi-Root Architecture

The **Metadata Sync Service (MSS)** and **MetaRegistry** will be updated to support a dual-root discovery pattern.

### **Root A: System Layer (Immutable for Users)**

- **Path:** `backend/app/core/framework/`
- **Purpose:** "Baked-in" entities required for system boot (Auth, Workflow, Logs).
- **Permissions:** `is_system: true`. Editable only when `DEVELOPER_MODE=1`.

### **Root B: Module Layer (Extendable)**

- **Path:** `backend/app/modules/{module_name}/entities/`
- **Purpose:** Domain-specific business logic (EAM, Maintenance, etc.).
- **Permissions:** Editable by System Administrators via Model Editor.

---

## 3. Consolidation Mapping

### **Core Framework (The "Baked-In" System)**

| Entity Group | Models (`.py`)                    | Metadata (`.json`)    | Status           |
| :----------- | :-------------------------------- | :-------------------- | :--------------- |
| **Auth**     | `User`, `Role`, `Permission`      | `auth.json`           | **Move to Core** |
| **Workflow** | `Workflow`, `State`, `Transition` | `workflow.json`       | **Move to Core** |
| **Infra**    | `Attachment`, `AuditLog`          | `infrastructure.json` | **Move to Core** |
| **System**   | `ScheduledJob`, `ModuleOrder`     | `system.json`         | **Move to Core** |

### **Module Entities (The "Apps")**

All 80+ entities (Assets, Work Orders, Purchase Requests) will remain within their respective module directories to ensure they are "pluggable."

---

## 4. Metadata Sync Service (MSS) Integration

The **9-Step Atomic Sync** must be modified to handle the new directory structure:

1.  **Path Resolution:** MSS will check the `is_system` flag. If true, it writes to `core/framework/`. If false, it writes to the module's path.
2.  **Developer Guard:** The `save_and_sync` method will implement a check:
    ```python
    if entity.is_system and not settings.DEVELOPER_MODE:
        raise PermissionError("Core Framework entities can only be edited in Developer Mode.")
    ```
3.  **Registry Reload:** The `RegistryManager` will perform a recursive scan of both the `core/framework` and `modules/` directories to build the global entity map.

---

## 5. Technical Safeguards & Refactoring

### **A. Automated Refactoring (The 45+ File Problem)**

To avoid manual errors, we will use **`ast-grep`** to rewrite import paths across the entire project.

- **Tool:** `ast-grep`
- **Action:** Find `from app.models.auth import User` -> Replace with `from app.core.framework import User`.

### **B. Database Integrity (Alembic)**

- **Naming Convention:** All core tables will be renamed to include a `core_` prefix (e.g., `users` -> `core_users`).
- **Registry Sync:** Alembic will be configured to detect models from the new `core/framework/models/` path specifically during the migration generation phase.

### **C. Dual Storage Resolution**

To eliminate the "Source of Truth" conflict, the **JSON metadata** will become the **Primary Source**. SQLAlchemy models will be decorated with a validation check that ensures they match the JSON definition upon application startup.

---

## 6. Implementation Phases

| Phase       | Task                                                          | Duration |
| :---------- | :------------------------------------------------------------ | :------- |
| **Phase 1** | Setup `core/framework` structure & update MSS Path Discovery. | 2 Days   |
| **Phase 2** | Migrate Auth & Workflow entities (Automated refactoring).     | 5 Days   |
| **Phase 3** | Implement `is_system` flags and Developer Mode UI locks.      | 3 Days   |
| **Phase 4** | Final Alembic schema standardization & Module Loader updates. | 4 Days   |

---

## 7. Success Criteria

- [ ] `MetadataSyncService` successfully handles multiple root directories.
- [ ] Model Editor UI "locks" core entities unless `DEVELOPER_MODE` is active.
- [ ] All 45+ high-dependency files updated via automated scripts.
- [ ] `forge migrate` successfully detects and applies changes to both core and module layers.

---
