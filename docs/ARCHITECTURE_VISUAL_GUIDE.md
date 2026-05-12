# Backend Architecture Visualization & Quick Reference

**Companion to:** DIRECTORY_STRUCTURE_AUDIT.md  
**Purpose:** Visual diagrams and quick reference for developers

---

## 🗂️ Directory Hierarchy (ASCII Tree)

```
backend/app/
|
|-- __init__.py                 [Package marker - empty]
|-- main.py                     [FastAPI entry point + lifespan]
|-- forge.py                    [Developer CLI tool]
|
|-- api/                        [CONSOLIDATED API LAYER - Clean Architecture]
|   |-- dependencies.py         [DI: Depends() factories]
|   |-- router.py               [Master router hub]
|   |-- schemas/                [Request/response Pydantic]
|   |-- services/               [API-specific services]
|   |-- entries/                [Generic entity operations]
|   |   |-- entity_crud.py      [CRUD operations - REFACTORED]
|   |   |-- entity_list.py      [List + pagination - REFACTORED]
|   |   |-- entity_workflow.py  [Workflow transitions]
|   |   |-- entity_actions.py   [Custom actions]
|   |   |-- entity_audit.py     [Change history]
|   |   |-- entity_print.py     [HTML/PDF reports]
|   |   |-- entity_options.py   [Dropdowns]
|   |   |-- entity_prefill.py   [Form pre-population]
|   |   |-- entity_children.py   [Child entity operations]
|   |   |-- entity_attachments.py [File attachments]
|   |   |-- entity_tree.py      [Tree structure]
|   |   |-- entity_fetch_from.py [Fetch from entity]
|   |   `-- __init__.py
|   |-- system/                 [Framework/core logic routes]
|   |   |-- auth.py            [Login/logout]
|   |   |-- workflow.py        [Workflow configuration CRUD]
|   |   |-- import_export.py   [Bulk import/export]
|   |   |-- meta.py            [Metadata endpoints]
|   |   |-- profile.py         [User profile]
|   |   |-- branding_settings.py [UI branding]
|   |   |-- setup.py           [System setup]
|   |   |-- test_scheduler.py  [Internal testing]
|   |   |-- attachments.py     [Attachment management]
|   |   |-- audit_log.py       [Audit trail]
|   |   |-- feature_flags.py   [Feature toggles]
|   |   |-- health.py          [Health checks]
|   |   |-- version.py         [Version info]
|   |   |-- admin/             [Administration submodule]
|   |   |   |-- users.py       [User management]
|   |   |   |-- roles.py       [Role management]
|   |   |   |-- permissions.py [Permission matrix]
|   |   |   |-- ordering.py    [Module/entity ordering]
|   |   |   |-- model_editor.py [Entity metadata editor]
|   |   |   |-- api_keys.py    [API key management]
|   |   |   |-- sessions.py    [Session management]
|   |   |   |-- common.py      [Shared admin utilities]
|   |   |   `-- __init__.py
|   |   `-- __init__.py
|   |-- features/               [Business feature endpoints]
|   |   |-- comments.py        [Entity comments]
|   |   |-- diagram.py          [Entity diagram visualization]
|   |   |-- favorites.py        [User favorites]
|   |   |-- operational_dashboard.py [Dashboard operations]
|   |   |-- search.py           [Global search]
|   |   |-- stock_count.py      [Stock counting]
|   |   |-- tags.py             [Entity tagging]
|   |   |-- timeline.py         [Entity timeline]
|   |   |-- notifications/      [Notification system]
|   |   |   |-- inbox.py        [Notification inbox]
|   |   |   `-- __init__.py
|   |   |-- pm_calendar/        [Maintenance calendar]
|   |   |   |-- routes.py       [Calendar endpoints]
|   |   |   `-- __init__.py
|   |   |-- reports/            [Report system]
|   |   |   |-- routes.py       [Report endpoints]
|   |   |   |-- registry.py     [Report registry]
|   |   |   `-- __init__.py
|   |   `-- __init__.py
|   `-- __init__.py
|
|-- application/                [BUSINESS ORCHESTRATION LAYER]
|   |-- services/               [Business services]
|   |   |-- entity_service.py   [Entity CRUD orchestration]
|   |   |-- auth_service.py     [Authentication use cases]
|   |   |-- rbac_service.py     [Permission checks - REFACTORED]
|   |   |-- workflow_service.py [Workflow orchestration]
|   |   |-- link_title_service.py [NEW: Link title resolution]
|   |   |-- job_registry.py     [NEW: Job registry pattern]
|   |   |-- email_notification_service.py [Email notifications]
|   |   |-- metadata_sync_service.py [Metadata sync orchestrator]
|   |   |-- notification_subscription_service.py [Notification subs]
|   |   |-- operational_dashboard_service.py [Dashboard data]
|   |   |-- role_based_dashboard_service.py [Role-based dashboards]
|   |   |-- fetch_from_service.py [Fetch from entity]
|   |   |-- import_export_service.py [Bulk operations]
|   |   |-- branding_service.py [UI branding]
|   |   |-- display_name_service.py [Display names]
|   |   |-- base_entity_api.py  [Optional lifecycle hooks]
|   |   `-- ... (10 more services)
|   |-- hooks/                  [Lifecycle hook system]
|   |   |-- registry.py         [Hook registry & dispatch]
|   |   `-- context.py          [HookContext dataclass]
|   |-- email_notifications/    [Email notification system]
|   |   |-- factory.py, dispatcher.py, handlers/
|   |   `-- ...
|   |-- docs/                   [Internal service documentation]
|   |-- dto.py                  [Data transfer objects]
|   `-- __init__.py             [Layer marker]
|
|-- core/                      [FRAMEWORK CORE]
|   |-- database.py             [SQLAlchemy setup]
|   |-- config.py               [Pydantic Settings from env]
|   |-- security.py             [JWT + CurrentUser]
|   |-- display_names.py        [Link title resolution - REDIRECT]
|   |-- loader.py               [Module dynamic loader]
|   |-- seed.py                 [Database seeding]
|   |-- serialization.py        [ORM -> dict conversion]
|   |-- base_model.py           [Base SQLAlchemy model]
|   |-- framework/              [Core models & bootstrap]
|   |   |-- models/
|   |   |   |-- auth.py         [User, Role, EntityPermission]
|   |   |   |-- infrastructure.py [ErrorLog, AuditLog, Attachment]
|   |   |   |-- workflow.py     [Workflow, WorkflowState]
|   |   |   `-- ordering.py     [ModuleOrder, EntityOrder]
|   |   |-- contracts/          [Protocol definitions]
|   |   |-- entities/           [Core entity metadata]
|   |   `-- schemas/            [Pydantic schemas]
|   `-- entities/              [Entity metadata loaders]
|
|-- domain/                    [DOMAIN LAYER - ABSTRACT]
|   |-- protocols/              [Repository interfaces (NOT enforced)]
|   `-- exceptions.py           [Domain-level exceptions]
|
|-- entities/                  [ENTITY METADATA GENERATION]
|   |-- __init__.py             [load_all_entities()]
|   `-- generator.py            [EntityMeta from JSON]
|
|-- infrastructure/            [EXTERNAL SERVICES - CONCRETE]
|   |-- database/
|   |   `-- repositories/       [Data access layer]
|   |       |-- entity_repository.py [Generic CRUD]
|   |       |-- auth_repository.py [NEW: Auth data access]
|   |       |-- workflow_repository.py [Workflow data]
|   |       |-- naming_repository.py [Naming data]
|   |       `-- ... (4 more)
|   |-- auth/                   [Authentication]
|   |   |-- jwt_service.py      [JWT encode/decode]
|   |   `-- password_service.py [Bcrypt hash/verify]
|   |-- email/                  [SMTP]
|   |   |-- smtp_service.py
|   |   `-- template_renderer.py
|   |-- cache/                  [Caching]
|   |   |-- permission_cache.py [5-min TTL]
|   |   `-- ttl_cache.py
|   |-- print/                  [HTML->PDF]
|   |   |-- resolve.py          [Link resolution]
|   |   `-- assemblers/         [Per-entity templates]
|   |-- realtime/               [SocketIO WebSocket]
|   |-- logging/                [Error tracking]
|   |-- settings/               [Settings persistence]
|   |-- metadata/               [Model generation]
|   |   |-- adapters.py         [Metadata sync adapters]
|   |   `-- __init__.py
|   `-- events/                 [Event bus - unused]
|
|-- meta/                      [METADATA REGISTRY]
|   `-- registry.py             [MetaRegistry: entity_name -> EntityMeta]
|
|-- modules/                   [AUTONOMOUS DOMAIN MODULES]
|   |-- core_eam/              [Org data - base tier]
|   |   |-- entities/          [27 JSON definitions]
|   |   |-- apis/              [Business logic functions]
|   |   |-- hooks.py           [Lifecycle + job registrations]
|   |   `-- __init__.py
|   |
|   |-- purchasing_stores/     [Procurement & inventory]
|   |   |-- entities/          [32 JSON defs]
|   |   |-- apis/              [11 API files]
|   |   |-- hooks.py, workflow_router.py [Jobs registered]
|   |   `-- __init__.py
|   |
|   |-- asset_management/      [Fixed assets]
|   |   |-- entities/, apis/
|   |   |-- hooks.py, workflow_router.py
|   |   `-- __init__.py
|   |
|   |-- maintenance_mgmt/      [Preventive maintenance]
|   |   |-- entities/, apis/
|   |   |-- hooks.py, workflow_router.py [Jobs registered]
|   |   `-- __init__.py
|   |
|   `-- work_mgmt/             [Work execution]
|       |-- entities/, apis/
|       |-- hooks.py, workflow_router.py
|       `-- __init__.py
|
|-- services/                   [CROSS-CUTTING SHARED SERVICES]
|   |-- document.py             [FACADE: get_doc, save_doc, etc.]
|   |-- document_query.py       [Read ops: get_doc, get_list]
|   |-- document_mutation.py    [Write ops: new_doc, save_doc, delete_doc]
|   |-- naming.py               [ID generation: PO-0001]
|   |-- workflow.py             [Workflow state mgmt]
|   |-- rbac.py                 [Permission checks - REFACTORED to use AuthRepository]
|   |-- scheduler.py            [APScheduler jobs - REFACTORED to use JobRegistry]
|   |-- audit.py                [Change history]
|   |-- error_logger.py         [Exception tracking]
|   |-- server_actions.py       [Custom action registry]
|   |-- query_link_handlers.py  [Field lookup dispatch]
|   |-- socketio_manager.py     [WebSocket events]
|   |-- print_service.py        [HTML/PDF rendering]
|   |-- import_export.py        [Bulk import]
|   `-- __init__.py
|
|-- templates/                 [JINJA2 TEMPLATES]
|   |-- email/                  [Email notification templates]
|   |-- print/                  [Print/report templates]
|   `-- reports/                [Report generation templates]
|
`-- backups/                    [DATABASE BACKUPS]
    |-- metadata/
    |-- models/
    `-- database.sql
```

## LAST UPDATE: 2026-04-07 11:39PM UTC+08:00

## 🏗️ Layer Architecture Diagram

```
                    ┌──────────────────────────────────────┐
                    │      PRESENTATION (Frontend)         │
                    └──────────────────────────────────────┘
                                     ▲
                                     │ HTTP/WebSocket
                                     ▼
        ┌────────────────────────────────────────────────────┐
        │              API LAYER (routes)                     │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ api/routes/* (22 handlers)                  │  │
        │  │ - entity_crud.py    ─→ Generic CRUD        │  │
        │  │ - entity_workflow.py ─→ State transitions  │  │
        │  │ - entity_list.py    ─→ List + filters      │  │
        │  │ - entity_print.py   ─→ Reports            │  │
        │  │ - ... (18 more)                             │  │
        │  └─────────────────────────────────────────────┘  │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ routers/* (Framework-level)                 │  │
        │  │ - auth.py      ─→ Login/logout             │  │
        │  │ - workflow.py  ─→ Workflow config          │  │
        │  │ - admin/       ─→ User/Role/Permission     │  │
        │  │ - import_export.py ─→ Bulk operations      │  │
        │  └─────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────┘
                         │
                         │ (Dependency Injection)
                         ▼
        ┌────────────────────────────────────────────────────┐
        │        APPLICATION LAYER (Services)                │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ application/services/* (16 services)        │  │
        │  │ - entity_service.py ─→ CRUD logic          │  │
        │  │ - auth_service.py   ─→ Auth logic          │  │
        │  │ - rbac_service.py   ─→ Permission logic    │  │
        │  │ - workflow_service.py ─→ Workflow logic    │  │
        │  │ - ... (12 more)                             │  │
        │  └─────────────────────────────────────────────┘  │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ services/* (Cross-cutting utilities)        │  │
        │  │ - document.py ─→ FACADE for all doc ops    │  │
        │  │ - naming.py ─→ ID generation               │  │
        │  │ - rbac.py ─→ Permission caching            │  │
        │  │ - audit.py ─→ Change tracking              │  │
        │  │ - socketio_manager.py ─→ Real-time events  │  │
        │  │ - scheduler.py ─→ Background jobs          │  │
        │  │ - ... (10 more)                             │  │
        │  └─────────────────────────────────────────────┘  │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ application/hooks/* (Lifecycle)             │  │
        │  │ - registry.py ─→ Hook dispatch              │  │
        │  │ - Modules register hooks here               │  │
        │  └─────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────┘
                         │
                         │ (Call)
                         ▼
        ┌────────────────────────────────────────────────────┐
        │      INFRASTRUCTURE LAYER (Implementations)        │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ infrastructure/database/repositories/*      │  │
        │  │ - entity_repository.py ─→ Generic CRUD     │  │
        │  │ - auth_repository.py ─→ User/Role queries  │  │
        │  │ - workflow_repository.py ─→ Workflow state │  │
        │  │ - naming_repository.py ─→ Series seq       │  │
        │  │ - ... (3 more repositories)                 │  │
        │  └─────────────────────────────────────────────┘  │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ infrastructure/email/* ─→ SMTP service     │  │
        │  │ infrastructure/auth/*  ─→ JWT, passwords   │  │
        │  │ infrastructure/print/* ─→ HTML→PDF         │  │
        │  │ infrastructure/realtime/* ─→ WebSocket     │  │
        │  │ infrastructure/cache/* ─→ Permission cache │  │
        │  │ infrastructure/logging/* ─→ Error tracking │  │
        │  └─────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────┘
                         │
                         │ (ORM calls)
                         ▼
        ┌────────────────────────────────────────────────────┐
        │          CORE FRAMEWORK LAYER                      │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ core/database.py ─→ SQLAlchemy setup       │  │
        │  │ core/security.py ─→ JWT + User context     │  │
        │  │ core/framework/models/* ─→ Base models     │  │
        │  │ - auth.py (User, Role)                      │  │
        │  │ - workflow.py (Workflow, WorkflowState)     │  │
        │  │ - infrastructure.py (ErrorLog, AuditLog)    │  │
        │  │ core/loader.py ─→ Module initialization    │  │
        │  │ core/config.py ─→ Settings from env        │  │
        │  └─────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────┘
                         │
                         │ (SQLAlchemy)
                         ▼
        ┌────────────────────────────────────────────────────┐
        │              DATABASE LAYER                        │
        │  PostgreSQL/MySQL with Alembic migrations         │
        └────────────────────────────────────────────────────┘
```

---

## 📦 Data Flow for Typical Request

### Example: Create a Purchase Order

```
1. CLIENT REQUEST
   POST /api/entity/purchase_order/action
   {
     "action": "create",
     "data": {
       "vendor": "VEN-001",
       "date_ordered": "2026-04-07",
       ...
     }
   }
   ▼

2. API LAYER (api/routes/entity_crud.py)
   ├─ Deserialize ActionRequest
   ├─ Check RBAC permission
   ├─ Call EntityService.create()
   └─ Return ActionResponse
   ▼

3. APPLICATION LAYER (application/services/entity_service.py)
   ├─ Validate required fields
   ├─ Coerce types
   ├─ Call EntityService.save_doc()
   │  (which delegates to document_mutation.save_doc())
   ├─ Call before_save hooks
   ├─ Call database insert
   ├─ Call after_save hooks
   └─ Emit SocketIO event
   ▼

4. INFRASTRUCTURE LAYER
   ├─ EntityRepository.create()
   │  (calls SQLAlchemy model)
   ├─ NamingService.generate_id() (if needed)
   ├─ SocketIOManager.emit_created()
   └─ AuditService.log_create() (if enabled)
   ▼

5. CORE LAYER
   ├─ Database.execute(INSERT)
   ├─ Return new record with ID
   └─ Emit WebSocket event
   ▼

6. DATABASE
   ├─ Execute INSERT statement
   ├─ Commit transaction
   └─ Return record ID
   ▼

7. RESPONSE TO CLIENT
   {
     "status": "success",
     "data": {
       "id": "PO-0001",
       "vendor": "VEN-001",
       "created_at": "2026-04-07T10:30:00",
       ...
     }
   }
   ▼

8. FRONTEND UPDATES IN REAL-TIME
   ├─ WebSocket: purchase_order.created event
   ├─ UI receives new record
   └─ List view auto-refreshes
```

---

## 🎯 Why Folders Are Organized This Way

| Principle                  | Implementation                    | Benefit                                |
| -------------------------- | --------------------------------- | -------------------------------------- |
| **Separation of Concerns** | 14 independent directories        | Each folder has one responsibility     |
| **Layered Architecture**   | API → App → Infra → Core          | Clean dependencies (top→down only)     |
| **Metadata-Driven**        | Entities as JSON, meta/registry   | 100+ entities without code changes     |
| **Module Independence**    | 5 standalone modules              | Add new business domain without impact |
| **Extensibility**          | Hook system in application/hooks/ | Extend behavior without modifying core |
| **Testability**            | Services decouple from HTTP       | Unit test without mocking FastAPI      |
| **Scalability**            | Generic repositories              | 22 routes handle unlimited entities    |

---

## 🚀 Developer Workflows

### Adding a New Entity

```
1. Create JSON definition
   modules/core_eam/entities/employee.json

2. Run forge sync
   → Generates models/employee.py
   → Runs Alembic migration
   → Updates MetaRegistry

3. Write business logic (optional)
   modules/core_eam/apis/employee.py

4. Register hooks (optional)
   modules/core_eam/hooks.py

5. New entity is live
   → All 22 routes work automatically
   → Permissions checked via RBAC
   → Workflows available if defined in JSON
```

### Adding a Custom Endpoint

```
1. Create route handler
   api/routes/my_custom.py

2. Add to main.py router registration
   fastapi_app.include_router(my_custom.router)

3. Implementation
   ├─ Receive HTTP request
   ├─ Call application service
   ├─ Return response
   └─ No business logic in route
```

### Adding a Background Job

```
1. Implement job function
   modules/maintenance_mgmt/apis/my_job.py
   async def run_my_job(db):
       ...

2. Register with scheduler
   services/scheduler.py
   scheduler.add_job(run_my_job, trigger="interval", hours=1)

3. Job runs every hour
   ├─ APScheduler triggers
   ├─ Function executes
   └─ Database updated
```

---

## ✅ File Naming Conventions

| Pattern                  | Folder                                  | Purpose           | Example                       |
| ------------------------ | --------------------------------------- | ----------------- | ----------------------------- |
| `{entity}.py`            | `modules/{module}/models/`              | SQLAlchemy model  | `purchase_order.py`           |
| `{entity}.json`          | `modules/{module}/entities/`            | Entity definition | `purchase_order.json`         |
| `{entity}.py`            | `modules/{module}/apis/`                | Business logic    | `purchase_order.py`           |
| `entity_{aspect}.py`     | `api/routes/`                           | Route handler     | `entity_crud.py`              |
| `{service}_service.py`   | `application/services/`                 | Business service  | `entity_service.py`           |
| `{domain}_repository.py` | `infrastructure/database/repositories/` | Data access       | `auth_repository.py`          |
| `{entity}_{action}.html` | `templates/email/`                      | Email template    | `purchase_order_created.html` |

---

## 🔍 Quick Lookup: "Where do I find...?"

| Looking for...           | Location                                | File                   |
| ------------------------ | --------------------------------------- | ---------------------- |
| How to create a record   | `application/services/`                 | `entity_service.py`    |
| How to check permissions | `application/services/`                 | `rbac_service.py`      |
| How to send an email     | `application/email_notifications/`      | `dispatcher.py`        |
| Database queries         | `infrastructure/database/repositories/` | `entity_repository.py` |
| JWT parsing              | `core/`                                 | `security.py`          |
| Workflow configuration   | `routers/`                              | `workflow.py`          |
| Scheduled jobs           | `services/`                             | `scheduler.py`         |
| User authentication      | `routers/`                              | `auth.py`              |
| Admin panel              | `routers/admin/`                        | `routers/*.py`         |
| Entity list endpoint     | `api/routes/`                           | `entity_list.py`       |
| Metadata for an entity   | `meta/`                                 | `registry.py`          |
| Module initialization    | `core/`                                 | `loader.py`            |
| Hook registration        | `application/hooks/`                    | `registry.py`          |

---

## 📋 Comparison: `api/` vs `routers/`

| Aspect              | `api/`                         | `routers/`                      |
| ------------------- | ------------------------------ | ------------------------------- |
| **Purpose**         | Entity CRUD operations         | Framework setup & config        |
| **Pattern**         | Generic (serves 100+ entities) | Specific (one per concern)      |
| **Scope**           | Data manipulation              | System administration           |
| **Examples**        | Create, update, list, workflow | Login, user mgmt, permissions   |
| **Routes**          | `/api/entity/**`               | `/api/auth/**`, `/api/admin/**` |
| **Total**           | 22 handlers                    | 7 modules                       |
| **Metadata-driven** | Yes                            | No                              |
| **Depends on**      | Meta registry, RBAC            | Core models only                |
| **Lifetime**        | Grows with new entities        | Stable, rarely changes          |

---

## 📊 Module Dependencies (Load Order)

```
                ┌─────────────────┐
                │   core (base)   │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │    core_eam     │
                │  (org data)     │
                └────────┬────────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
       purchasing_  asset_mgmt   (other)
       stores       (assets)
            │            │
            └────────┬───┘
                     │
            ┌────────▼─────────┐
            │  maintenance_    │
            │  mgmt (PM)       │
            └────────┬─────────┘
                     │
            ┌────────▼────────┐
            │   work_mgmt     │
            │  (execution)    │
            └─────────────────┘

Load order enforced in: core/loader.py (MODULE_LOAD_ORDER)
```

---

## 🎓 Key Takeaways

1. **14 independent folders** with clear responsibilities
2. **Two API tiers:** `api/` (entity) + `routers/` (framework)
3. **Metadata-driven:** Entity definitions in JSON, no hardcoded routes
4. **Modular:** 5 autonomous domains with consistent vertical slicing
5. **Layered:** API → App → Infra → Core → Database
6. **Extensible:** Hooks system for behavior injection
7. **No redundancy:** Each folder serves specific architectural need

**Everything is intentional. Nothing is wasted.**

---

## 📅 Changelog

### 2026-04-07 - API Structure Reorganization

**Major restructuring of `/api` directory:**

#### Removed:

- `routers/` directory (merged into `api/system/`)
- `api/modules/` (empty directory)
- `api/entries/` route files moved to better categorization:
  - `profile.py` → `api/system/profile.py`
  - `branding_settings.py` → `api/system/branding_settings.py`
  - `setup.py` → `api/system/setup.py`
  - `operational_dashboard.py` → `api/features/operational_dashboard.py`
  - `reports.py` + `reports_registry.py` → `api/features/`
  - `stock_count_routes.py` → `api/features/stock_count.py`
  - `notification_subscriptions.py` → moved to features (removed)
  - `email_notifications.py` → moved to features (removed)

#### Added:

- `api/features/` - Special business feature endpoints
  - `diagram.py` - Entity diagram visualization
  - `pm_calendar.py` - Maintenance calendar UI
  - `pm_calendar_seed.py` - Calendar seeding utilities
  - `operational_dashboard.py` - Dashboard operations
  - `reports.py` - Report generation
  - `reports_registry.py` - Report registry
  - `stock_count.py` - Stock counting

#### Restructured:

- `api/system/` - Core system and framework routes
  - `admin/` - All administration functions
  - Framework routes (auth, workflow, meta, import_export)
  - User-specific routes (profile, branding, setup)

#### New Router Pattern:

```python
# Old: Arbitrary categorization
ENTRY_ROUTE_MODULES = [...]  # Mixed concerns
SYSTEM_ROUTE_MODULES = [...] # Mixed concerns
FEATURE_ROUTE_MODULES = [...] # Inconsistent

# New: Clear separation
api/entries/    # Core entity operations only
api/system/     # Framework and core system concerns
api/features/   # Business-specific features
```

**Impact:**

- Cleaner separation of concerns
- More intuitive navigation for developers
- Consistent routing patterns
- Removed duplicate/empty directories
- Better alignment with Clean Architecture principles

**Files affected:** 23 route files reorganized
