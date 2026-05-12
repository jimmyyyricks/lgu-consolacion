# Backend Application Directory Structure Audit

**Date:** April 7, 2026  
**Scope:** Complete analysis of `/backend/app/` directory (16,061 lines of Python code)  
**Purpose:** Explain why each folder exists, what it contains, and how they relate to architecture

---

## 📊 Quick Navigation

| Level | Folder            | Purpose                                        | Layer                     |
| ----- | ----------------- | ---------------------------------------------- | ------------------------- |
| Root  | `api/`            | Clean Architecture routes (entity-level)       | **API**                   |
| Root  | `apis/`           | Backward-compat re-export (deprecated pattern) | **Utility**               |
| Root  | `application/`    | Business orchestration services, hooks, DI     | **Application**           |
| Root  | `core/`           | Framework core (DB, config, security, seed)    | **Infrastructure/Shared** |
| Root  | `domain/`         | Domain protocols (abstract interfaces)         | **Domain**                |
| Root  | `entities/`       | Entity metadata generator from JSON            | **Config**                |
| Root  | `infrastructure/` | External service implementations               | **Infrastructure**        |
| Root  | `meta/`           | Global metadata registry                       | **Shared**                |
| Root  | `models/`         | Re-export convenience module                   | **Utility**               |
| Root  | `modules/`        | 5 autonomous domain modules                    | **Domain**                |
| Root  | `routers/`        | Framework-level routes (auth, admin, config)   | **API**                   |
| Root  | `schemas/`        | Pydantic request/response models               | **Schema**                |
| Root  | `services/`       | Cross-cutting shared services                  | **Application**           |
| Root  | `templates/`      | Jinja2 templates for email/print               | **Utility**               |

---

## 🔍 Detailed Directory Breakdown

---

## Top-Level Files

### `__init__.py`

- **Purpose:** Package marker (empty)
- **Contains:** Nothing (empty file)
- **Why:** Marks `/app/` as a Python package

### `main.py`

- **Purpose:** FastAPI application entry point
- **Contains:**
  - App lifespan management (`@asynccontextmanager`)
  - Module loader initialization
  - Entity metadata loading
  - Middleware registration (CORS, timing)
  - Router registration
- **Key responsibilities:**
  1. Initialize core framework during lifespan startup
  2. Load all dynamic modules (core_eam, purchasing_stores, etc.)
  3. Load entity metadata from JSON definitions
  4. Register all routers (legacy and new)
  5. Start APScheduler for background jobs
- **Called by:** `run.sh` or `uvicorn app.main:fastapi_app`

### `forge.py`

- **Purpose:** Developer CLI tool
- **Contains:** Commands for:
  - `forge sync` — Detect JSON changes, regenerate models, run migrations
  - `forge migrate` — Run Alembic migrations
  - `forge seed` — Populate database with initial data
  - `forge new-entity` — Scaffold new entity (JSON + model)
  - `forge console` — Python REPL with app context
- **Why it exists:** Automates common ERP developer workflows (Frappe-style)
- **Used by:** Developers during development and deployment

---

## 1️⃣ `api/` — Clean Architecture Routes (Entity-Level API)

**Purpose:** Generic, metadata-driven HTTP endpoints for all entities  
**Why separate from `routers/`:** Handles entity concerns only (CRUD, data manipulation); framework concerns are in `routers/`  
**Total files:** 22 route handlers + schemas

### Structure

```
api/
├── __init__.py                 [Marking comment: "API Layer"]
├── dependencies.py             [DI: FastAPI Depends() factories]
├── test_scheduler.py           [Internal: Testing APScheduler]
├── features/                   [Special endpoint groups]
│   ├── pm_calendar.py          [Preventive maintenance calendar endpoint]
│   ├── pm_calendar_seed.py     [PM calendar seed data]
│   └── diagram.py              [Entity relationship diagram endpoint]
├── routes/                     [22 generic entity route handlers]
│   ├── entity_crud.py          [POST/PUT DELETE — create, update, delete any entity]
│   ├── entity_list.py          [GET — paginated list with filters, batch link resolution]
│   ├── entity_workflow.py      [POST — state transitions (workflow actions)]
│   ├── entity_actions.py       [POST — custom server actions per entity]
│   ├── entity_attachments.py   [File upload/download per record]
│   ├── entity_audit.py         [GET — change history (before/after snapshots)]
│   ├── entity_print.py         [GET — HTML/PDF reports]
│   ├── entity_tree.py          [GET — hierarchical/tree views]
│   ├── entity_children.py      [Bulk save of child records + denormalization]
│   ├── entity_options.py       [GET — dropdown data for link fields]
│   ├── entity_prefill.py       [Form pre-population on create (magic tokens)]
│   ├── entity_fetch_from.py   [Dynamic field lookup (linked entity resolution)]
│   ├── profile.py              [GET/PUT /me — user profile + settings]
│   ├── reports.py              [Custom report generation]
│   ├── branding_settings.py    [GET/PUT — tenant branding/styling]
│   ├── email_notifications.py  [Email notification configuration]
│   ├── notification_subscriptions.py [User notification preferences]
│   ├── operational_dashboard.py [Dashboard data aggregation]
│   ├── reports_registry.py     [Report discovery/registry]
│   ├── setup.py                [Initial system setup endpoint]
│   ├── stock_count_routes.py   [Stock count specific routes]
│   └── __init__.py             [Route registration marker]
└── schemas/                    [Request/response Pydantic models]
    ├── __init__.py
    └── (Shared with /schemas/ directory)
```

### Key Files Explained

#### `dependencies.py` (Dependency Injection)

```
Purpose: FastAPI Depends() factories
Contains:
  - get_db() — AsyncSession database connection
  - get_entity_repo() — EntityRepository instance
  - get_auth_repo() — AuthRepository instance
  - get_workflow_repo() — WorkflowRepository instance
  - get_naming_repo() — NamingRepository instance
  - get_entity_service() — EntityService instance
  - get_auth_service() — AuthService instance
  - get_rbac_service() — RBACService instance
  - get_jwt_service() — JWTService (singleton)
  - get_password_service() — PasswordService (singleton)

Why: Wires infrastructure repositories to application services
     Allows route handlers to receive injected dependencies
     Type-safe DI using FastAPI's Depends()
```

#### Route Handlers (`routes/entity_*.py` pattern)

**Design Pattern:** Each handler file is SINGLE-PURPOSE

- One file = one HTTP aspect (CRUD vs. Workflow vs. List)
- No fat routers (business logic delegated to services)
- All use same `dispatch(entity, action, user)` pattern

**Example: entity_crud.py**

```python
@router.post("/{entity}/action")
async def post_entity_action(
    entity: str,
    request: ActionRequest,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # Check RBAC permission
    # Call EntityService for business logic
    # Emit SocketIO event
    # Return response
```

**Key insight:** No database queries in this file.  
All queries are in `EntityRepository`. All business logic is in `EntityService`.  
Route handler is purely orchestration.

#### `schemas/` Subdirectory

**Note:** Actual schemas are in `/schemas/` root directory, not here.  
This is a symlink or re-export location for API request/response models.

#### `features/` Subdirectory

**Purpose:** Special-case endpoints that don't fit the generic entity pattern

- `pm_calendar.py` — Preventive maintenance calendar display
- `diagram.py` — Entity relationship diagram (for visualization)
- `pm_calendar_seed.py` — Seed data generator

**Why separated:** These endpoints:

1. Require cross-entity aggregation
2. Are read-only reporting endpoints
3. Don't map to a single entity's CRUD

---

## 2️⃣ `apis/` — Backward Compatibility Re-export

**Purpose:** Deprecated re-export location (for backward compatibility)  
**Contains:** Single file pointing to `application/services/base_entity_api.py`

### Files

```
apis/
├── __init__.py
└── base_entity_api.py    [RE-EXPORT: Canonical location is application/services/]
```

### Content

```python
# app/apis/base_entity_api.py
from app.application.services.base_entity_api import BaseEntityAPI, Context
__all__ = ["BaseEntityAPI", "Context"]
```

### Why This Exists

**Historical reason:** Early architecture had APIs in `apis/` folder  
**Current state:** Canonical location moved to `application/services/`  
**Kept for:** Backward compatibility (avoiding import breakage)  
**Status:** Deprecated (should be removed in v2.0)

### Note About "apis" vs "api"

These are NOT the same:

- **`api/`** = HTTP routes (Clean Architecture - entity-level endpoints)
- **`apis/`** = Old application layer (now moved to `application/services/`)

**Do not confuse.** Import from `application/services.base_entity_api` directly.

---

## 3️⃣ `application/` — Application Layer (Orchestration Services)

**Purpose:** Business logic orchestration (NOT HTTP, NOT ORM)  
**Principle:** Pure Python, no FastAPI, no SQLAlchemy imports  
**Total files:** ~30+ files

### Structure

```
application/
├── __init__.py                    [Layer marker]
├── dto.py                         [Data Transfer Objects (optional)]
├── docs/                          [Internal documentation]
│   ├── adr-001-core-framework-separation.md  [Architecture Decision Record]
│   ├── auth-service.md            [AuthService documentation]
│   ├── base-entity-api.md         [BaseEntityAPI documentation]
│   ├── branding-service.md
│   ├── display-name-service.md
│   ├── email-notifications.md
│   └── ... (12+ docs)
├── email_notifications/           [Email notification system]
│   ├── factory.py                 [Notification factory (pattern factory)]
│   ├── dispatcher.py              [SMTP dispatcher]
│   ├── document_notify.py         [Document-level notification trigger]
│   └── handlers/                  [Per-entity email handlers]
├── hooks/                         [Lifecycle hook system]
│   ├── registry.py                [Hook registry (before_save, after_save, workflow)]
│   ├── context.py                 [HookContext dataclass]
│   └── __init__.py
└── services/                      [Application-level Business Services]
    ├── __init__.py
    ├── auth_service.py            [Authentication orchestration]
    ├── base_entity_api.py         [BaseEntityAPI class - optional lifecycle hooks]
    ├── branding_service.py        [Tenant branding management]
    ├── display_name_service.py    [Display name resolution (deprecated - use core/display_names.py)]
    ├── entity_service.py          [Entity CRUD orchestration]
    ├── fetch_from_service.py      [Dynamic field fetch service]
    ├── import_export_service.py   [Import/export orchestration]
    ├── notification_subscription_service.py [Subscription management]
    ├── operational_dashboard_service.py [Dashboard aggregation]
    ├── operational_dashboard_service_old.py [Legacy version]
    ├── rbac_service.py            [Role-based access control]
    ├── role_based_dashboard_service.py [Role-specific dashboard data]
    ├── workflow_progress_service.py [Workflow progress tracking]
    ├── workflow_service.py        [Workflow orchestration]
    └── __init__.py
```

### Key Components

#### `application/services/entity_service.py`

**Purpose:** Core orchestration for entity operations  
**Responsibility:**

- Validate incoming data
- Coerce types (convert string IDs to integers, etc.)
- Call repositories for DB operations
- Emit events (SocketIO)
- Does NOT touch HTTP concerns

#### `application/services/auth_service.py`

**Purpose:** Authentication use cases  
**Responsibility:**

- Login & token generation
- User creation
- Password reset workflows

#### `application/services/rbac_service.py`

**Purpose:** Role-Based Access Control  
**Responsibility:**

- Check permissions (cached)
- Get user permissions (async with DB fallback)

#### `application/hooks/registry.py`

**Purpose:** Lifecycle hook system  
**How it works:**

```python
@hook_registry.before_save("entity_name")
async def hook_func(doc, ctx):
    # Runs BEFORE insert/update
    pass

@hook_registry.after_save("entity_name")
async def hook_func(doc, ctx):
    # Runs AFTER insert/update
    pass

@hook_registry.workflow("entity_name")
async def hook_func(ctx):
    # Runs ON state transition
    pass
```

**Used by:** Modules extend behavior without modifying shared code

#### `application/docs/`

**Purpose:** Internal ADRs and documentation  
**Contains:** 12+ markdown files explaining service behavior  
**Example:** `adr-001-core-framework-separation.md` — explains why core framework is separate

---

## 4️⃣ `core/` — Framework Core Services

**Purpose:** Lowest-level infrastructure and configuration  
**Layer:** Interface between application and infrastructure  
**Total files:** ~12 Python files + `framework/` subfolder

### Structure

```
core/
├── __init__.py                    [Empty]
├── base_model.py                  [SQLAlchemy BaseModel (id, created_at, updated_at)]
├── config.py                      [Pydantic Settings from environment]
├── database.py                    [AsyncSession, engine, migrations]
├── display_names.py               [Link title resolution functions (CANONICAL)]
├── error_handlers.py              [FastAPI exception handler registration]
├── exceptions.py                  [Custom HTTPException subclasses]
├── feature_flags.py               [Feature toggle lookup]
├── loader.py                      [Dynamic module loader (dependency-ordered)]
├── sanitization.py                [Input sanitization (drops unknown fields)]
├── security.py                    [JWT parsing, CurrentUser model]
├── seed.py                        [Database seeding (users, roles, permissions)]
├── serialization.py               [SQLAlchemy model → dict conversion]
├── entities/                      [Entity metadata loaders]
│   ├── __init__.py
│   └── ... (dynamic entity definitions)
└── framework/                     [Core framework models & bootstrap]
    ├── __init__.py                [initialize_core_framework()]
    ├── contracts/                 [Protocol definitions (abstract interfaces)]
    ├── entities/                  [Core entity metadata]
    ├── models/
    │   ├── __init__.py
    │   ├── auth.py                [User, Role, EntityPermission (SQLAlchemy)]
    │   ├── infrastructure.py      [ErrorLog, AuditLog, Attachment, EmailLog, NotificationSubscription]
    │   ├── workflow.py            [Workflow, WorkflowState, WorkflowAction, WorkflowTransition]
    │   └── ordering.py            [ModuleOrder, EntityOrder]
    └── schemas/                   [Pydantic schemas for auth endpoints]
```

### Key Files Explained

#### `core/database.py`

```
Contains:
  - SQLAlchemy Base (declarative)
  - async_engine setup
  - async_session_maker (AsyncSession factory)
  - get_db() dependency for FastAPI
  - init_db() — create all tables
```

#### `core/security.py`

```
Contains:
  - JWT token parsing
  - CurrentUser model (current authenticated user)
  - get_current_user_from_token()
```

#### `core/display_names.py` (CANONICAL VERSION)

```
Contains:
  - get_link_title() — fetch title of linked entity
  - build_link_titles_for_record() — batch link title resolution
  - get_record_display_name() — display name for any record

Used by: Infrastructure print, email notifications, routes
Note: Do NOT use display_name_service.py (deprecated)
```

#### `core/loader.py`

```
Purpose: Dynamic module loader
Module load order (dependency-based):
  1. core (framework)
  2. core_eam (org data)
  3. purchasing_stores (procurement)
  4. asset_management (assets)
  5. maintenance_mgmt (PM)
  6. work_mgmt (execution)

Why ordered: asset_management imports from core_eam, etc.
```

#### `core/framework/models/`

```
auth.py:
  - User, Role, EntityPermission
  - Core authentication models

infrastructure.py:
  - ErrorLog, AuditLog
  - Attachment, EmailLog
  - NotificationSubscription

workflow.py:
  - Workflow, WorkflowState, WorkflowAction
  - WorkflowStateLink, WorkflowTransition
  - Core workflow state machine models

ordering.py:
  - ModuleOrder, EntityOrder
  - Ordering/sorting configuration
```

---

## 5️⃣ `domain/` — Domain Layer (Abstract Interfaces)

**Purpose:** Domain protocols — Define "what repositories must do" without implementation  
**Layer:** Defines contracts that infrastructure must satisfy  
**Total files:** 2 files + `protocols/` subfolder

### Structure

```
domain/
├── __init__.py
├── exceptions.py               [Domain-level exceptions]
└── protocols/                  [Abstract repository protocols]
    ├── __init__.py
    └── ... (repository interface definitions)
```

### Files Explained

#### `domain/protocols/`

**Purpose:** Abstract base classes (protocols) for repositories  
**Example:**

```python
class EntityRepositoryProtocol(Protocol):
    async def get_by_id(self, entity: str, id: Any) -> Optional[Any]:
        ...
    async def get_list(self, entity: str, filters: dict) -> List[Any]:
        ...
    async def create(self, entity: str, data: dict) -> Any:
        ...
```

**Current status:** Declared but NOT enforced via inheritance  
**Recommendation:** Enable mypy strict mode; have concrete repos inherit from these protocols

---

## 6️⃣ `entities/` — Entity Metadata Generator

**Purpose:** Convert JSON entity definitions into Python models at startup  
**Why separate:** Keeps model generation logic separate from models themselves

### Structure

```
entities/
├── __init__.py                    [load_all_entities() — startup loader]
└── generator.py                   [EntityMeta generator from JSON definitions]
```

### Files Explained

#### `entities/__init__.py`

```
Contains: load_all_entities()
Purpose:
  1. Scan modules/ for entities/ folders
  2. Read entity_name.json files
  3. Generate EntityMeta objects
  4. Store in global MetaRegistry

Called during: main.py lifespan startup
```

#### `entities/generator.py`

```
Purpose: Generate EntityMeta from JSON
Input: {
  "entity": "purchase_order",
  "title": "Purchase Order",
  "fields": [...],
  "workflows": [...],
  "naming": {...},
  ...
}

Output: EntityMeta object with:
  - fields (list of FieldMeta)
  - workflow (WorkflowMeta)
  - naming (NamingMeta)
  - permissions (PermissionMeta)
  - etc.
```

---

## 7️⃣ `infrastructure/` — External Service Implementations

**Purpose:** Concrete implementations of repositories and external integrations  
**Principle:** NO business logic — only technical implementations  
**Total files:** ~20+ Python modules

### Structure

```
infrastructure/
├── __init__.py
├── rate_limit.py                  [Rate limiting utility]
├── auth/                          [Authentication implementations]
│   ├── jwt_service.py             [JWT encode/decode]
│   └── password_service.py        [Bcrypt hash/verify]
├── cache/                         [Caching layer]
│   └── permission_cache.py        [TTL-based permission cache (5 min)]
├── database/                      [Data access layer]
│   ├── __init__.py
│   └── repositories/              [Repository implementations]
│       ├── entity_repository.py   [Generic CRUD via __tablename__ lookup]
│       ├── auth_repository.py     [User/Role queries]
│       ├── workflow_repository.py [Workflow state queries]
│       ├── naming_repository.py   [Series sequence (ID counters)]
│       ├── fetch_from_repository.py [Dynamic field fetch queries]
│       ├── notification_subscription_repository.py
│       └── tree.py                [Hierarchical structure queries]
├── email/                         [SMTP email service]
│   ├── smtp_service.py            [SMTP sender]
│   └── template_renderer.py       [Jinja2 template rendering]
├── logging/                       [Error logging]
├── metadata/                      [Model generation utilities]
├── print/                         [HTML→PDF print assemblers]
│   └── assemblers/                [Per-entity print templates]
├── realtime/                      [SocketIO WebSocket management]
├── settings/                      [Branding store (settings persistence)]
└── events/                        [Domain event bus (declared, unused)]
```

### Key Subdirectories

#### `infrastructure/database/repositories/`

**Purpose:** Data access layer — ALL SQLAlchemy queries live here  
**Pattern:**

```python
class EntityRepository:
    async def get_by_id(self, entity: str, id: Any):
        model = get_entity_model(entity)
        result = await db.execute(select(model).where(model.id == id))
        return result.scalar_one_or_none()
```

**Why centralized:**

1. No ORM leakage to services or routes
2. Easy to mock for testing
3. Consistent query patterns

#### `infrastructure/email/`

**Files:**

- `smtp_service.py` — Send email via SMTP
- `template_renderer.py` — Render Jinja2 templates

**Used by:** `application/email_notifications/dispatcher.py`

#### `infrastructure/auth/`

**Files:**

- `jwt_service.py` — Encode/decode JWT tokens
- `password_service.py` — Hash/verify passwords (bcrypt)

**Used by:** `application/services/auth_service.py`

#### `infrastructure/print/`

**Purpose:** HTML → PDF rendering for reports  
**Contains:** Per-entity print assemblers

**Example:** `infrastructure/print/assemblers/work_order_print.py`

---

## 8️⃣ `meta/` — Global Metadata Registry

**Purpose:** Runtime entity metadata lookup  
**Contains:** `MetaRegistry.get(entity_name) → EntityMeta`

### Structure

```
meta/
├── __init__.py
└── registry.py                    [MetaRegistry class]
```

### Files Explained

#### `meta/registry.py`

```
Contains:
  - MetaRegistry class
  - get(entity_name): EntityMeta
  - set(entity_name, meta): void
  - get_list_of_entities(): list

Initialized at startup by: entities/load_all_entities()

Used everywhere:
  - Routes: check permissions, field types, workflows
  - Services: validate data, get field definitions
  - Hooks: determine which hooks to run
```

---

## 9️⃣ `models/` — Re-export Convenience

**Purpose:** Convenience module for importing core models  
**Contains:** Re-exports from `core/framework/models/`

### Structure

```
models/
├── __init__.py
```

### Content

```python
from app.core.framework.models.auth import User, Role, EntityPermission
from app.core.framework.models.infrastructure import ErrorLog, AuditLog, ...
from app.core.framework.models.workflow import Workflow, WorkflowState, ...
```

**Why:** Allows developers to use:

```python
from app.models import User, Role
# Instead of:
from app.core.framework.models.auth import User, Role
```

**Status:** Optional convenience (using full path is fine)

---

## 🔟 `modules/` — Autonomous Domain Modules

**Purpose:** Five self-contained business domain modules  
**Principle:** Each module owns its models, business logic, and hooks  
**Pattern:** Each module has same vertical-slice structure

### Structure

```
modules/
├── __init__.py
├── core_eam/                      [Organizational data - base tier]
│   ├── __init__.py
│   ├── models/                    [27 SQLAlchemy models]
│   │   ├── site.py, department.py, employee.py, labor.py, trade.py, ...
│   │   └── series.py              [ID sequence counters]
│   ├── entities/                  [JSON entity definitions]
│   │   ├── site.json, department.json, ...
│   │   └── ... (27 entity definitions)
│   ├── apis/                      [Business logic functions]
│   │   ├── site.py, department.py, ...
│   │   └── ... (business validation and operations)
│   └── hooks.py                   [Lifecycle hook registrations]
│
├── purchasing_stores/             [Procurement & inventory]
│   ├── models/                    [32 SQLAlchemy models]
│   │   ├── purchase_request.py, purchase_order.py, purchase_receipt.py
│   │   ├── inventory.py, item.py, stock_count.py, transfer.py, ...
│   │   └── ... (32 models)
│   ├── entities/                  [32 JSON entity definitions]
│   ├── apis/                      [11 business logic files]
│   │   ├── purchase_order.py      [create_po_from_pr(), create_po_from_rfq()]
│   │   ├── purchase_request.py    [PR approval workflow]
│   │   ├── stock_count.py, item_issue.py, item_return.py, ...
│   │   └── ... (11 API files)
│   ├── hooks.py
│   └── workflow_router.py         [Centralized workflow handler]
│
├── asset_management/              [Fixed assets]
│   ├── models/                    [21 SQLAlchemy models]
│   ├── entities/                  [21 JSON definitions]
│   ├── apis/                      [6 business files]
│   ├── hooks.py
│   └── workflow_router.py
│
├── maintenance_mgmt/              [Preventive maintenance]
│   ├── models/                    [Auto-generated]
│   ├── entities/                  [JSON definitions]
│   ├── apis/                      [7 business files]
│   │   ├── maintenance_request.py, maintenance_order.py
│   │   ├── maintenance_calendar.py [Scheduled job]
│   │   ├── maintenance_condition.py [Scheduled job]
│   │   ├── maintenance_interval.py [Scheduled job]
│   │   └── ... (7 files)
│   ├── hooks.py
│   └── workflow_router.py
│
└── work_mgmt/                     [Work execution]
    ├── models/                    [15 SQLAlchemy models]
    ├── entities/                  [15 JSON definitions]
    ├── apis/                      [8 business files]
    │   ├── work_order.py, work_order_activity.py
    │   ├── work_order_labor.py, work_order_parts.py, ...
    │   └── ... (8 files)
    ├── hooks.py
    └── workflow_router.py
```

### Module Anatomy

Every module has:

1. **`models/`** — SQLAlchemy ORM classes
   - Auto-generated from JSON entity definitions
   - Inherit from `BaseModel` (has id, created_at, updated_at)
   - Zero business logic

2. **`entities/`** — JSON entity definitions

   ```json
   {
     "entity": "purchase_order",
     "fields": [...],
     "workflows": [...],
     "naming": {"prefix": "PO", "start_number": 1},
     "title_field": "name"
   }
   ```

3. **`apis/`** — Business logic functions (Frappe-style)

   ```python
   async def create_po_from_pr(doc, db, user):
       # Validation, grouping, DB operations, side effects
       return {"status": "success", "po_id": "PO-0001"}
   ```

4. **`hooks.py`** — Lifecycle hook registrations

   ```python
   from app.application.hooks.registry import hook_registry

   @hook_registry.before_save("purchase_order")
   async def po_before_save(doc, ctx):
       # Validate
       pass

   @hook_registry.after_save("purchase_order")
   async def po_after_save(doc, ctx):
       # Side effects (email, notifications)
       pass
   ```

5. **`workflow_router.py`** (optional) — Centralized workflow handler
   ```python
   async def route_workflow(entity, doc, action, db, user):
       if action == "approve":
           # Validate approval conditions
           # Set workflow_state
           # Emit event
   ```

### Module Dependencies (Load Order)

Modules must load in dependency order:

```
1. core                  ← Framework (no dependencies)
2. core_eam              ← Organization data (dependency for all)
3. purchasing_stores     ← Procurement (depends on core_eam)
4. asset_management      ← Assets (depends on core_eam, purchasing_stores)
5. maintenance_mgmt      ← Maintenance (depends on asset_management, core_eam, purchasing_stores)
6. work_mgmt             ← Execution (depends on ALL above)
7. project_management    ← Projects
8. todo                  ← Todo items
```

**Enforced by:** `core/loader.py` — MODULE_LOAD_ORDER array

---

## 1️⃣1️⃣ `routers/` — Framework-Level Routes (Legacy Naming)

**Purpose:** Authentication, administration, and framework configuration endpoints  
**Why "legacy":** This naming is confusing, but these routes are NOT legacy — they're active framework-level concerns  
**Key distinction:** These handle framework setup, NOT entity CRUD

### Structure

```
routers/
├── __init__.py
├── auth.py                        [Login, logout, token refresh (5 endpoints)]
├── workflow.py                    [Global workflow configuration (CRUD workflows)]
├── import_export.py               [Bulk CSV/XLSX/Google Sheets import-export]
├── meta.py                        [Metadata endpoints]
└── admin/                         [Administration submodule]
    ├── __init__.py
    ├── routers/
    │   ├── users.py              [User management CRUD]
    │   ├── roles.py              [Role management CRUD]
    │   ├── permissions.py        [Permission matrix/configuration]
    │   ├── ordering.py           [Module/entity ordering config]
    │   └── model_editor.py       [Dynamic model editing]
    └── (registration in __init__)
```

### Key Files Explained

#### `routers/auth.py`

```
Endpoints:
  - POST /api/auth/login                  [OAuth2 form: username, password]
  - POST /api/auth/boot                   [Initial app load: permissions, metadata]
  - POST /api/auth/refresh                [Token refresh]
  - GET /api/auth/validate                [Validate current token]
  - GET /api/auth/me                      [Current user profile]

Purpose: NOT part of generic entity CRUD.
Why separate: Authentication is a framework concern, not an entity.
```

#### `routers/workflow.py`

```
Endpoints:
  - GET /api/workflow/states              [List all workflow states]
  - POST /api/workflow/states             [Create workflow state]
  - PUT /api/workflow/states/{id}         [Update state]
  - DELETE /api/workflow/states/{id}      [Delete state]
  - GET /api/workflow/actions             [List actions]
  - GET /api/workflow/{entity}/transitions [Get valid transitions from current state]

Purpose: Configure the workflow state machine (global configuration).
NOT the same as entity_workflow.py (which applies state transitions to records).
Why separate: Workflow configuration is system-level, not entity-level.
```

#### `routers/admin/`

```
Subendpoints:
  - /api/admin/users/**               [User CRUD]
  - /api/admin/roles/**               [Role CRUD + role assignments]
  - /api/admin/permissions/matrix     [Permission matrix editor]
  - /api/admin/ordering/**            [Module/entity ordering]
  - /api/admin/model-editor/**        [Dynamic model editing]

Purpose: System administration (users, roles, permissions, configuration).
Why separate: Admin features are platform-level, not domain entity-level.
```

#### `routers/import_export.py`

```
Endpoints:
  - GET /api/import-export/{entity}/template      [Download template .xlsx]
  - POST /api/import-export/{entity}/validate     [Validate import file]
  - POST /api/import-export/{entity}/validate/sheets [Validate Google Sheets]
  - POST /api/import-export/{entity}/execute      [Execute import]
  - POST /api/import-export/{entity}/export       [Export to .xlsx]

Purpose: Bulk data operations (framework feature, not entity-specific).
Why separate: Import/export is infrastructure, not core CRUD.
```

---

## 1️⃣2️⃣ `schemas/` — Pydantic Request/Response Models

**Purpose:** Type definitions for FastAPI request/response contracts  
**Layer:** Schema/Presentation layer

### Structure

```
schemas/
├── __init__.py
├── base.py                        [ActionRequest, ActionResponse]
├── role.py                        [Role creation/update schemas]
└── user.py                        [User registration/login schemas]
```

### Files Explained

#### `schemas/base.py`

```python
class ActionRequest(BaseModel):
    action: str                     # "create", "update", "delete", or custom action name
    data: dict[str, Any]            # Entity data to create/update
    id: Optional[str] = None        # Record ID (for update/delete)
    children: Optional[dict] = None # Bulk child records

class ActionResponse(BaseModel):
    status: str                     # "success", "error", "warning"
    message: str
    data: Optional[dict] = None
```

**Used by:** All entity\_\*.py route handlers  
**Why centralized:** Single contract for all entity operations

#### `schemas/role.py`

```python
class RoleCreate(BaseModel):
    name: str
    description: str

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
```

#### `schemas/user.py`

```python
class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class UserLogin(OAuth2PasswordRequestForm):
    [Uses FastAPI's OAuth2PasswordRequestForm]
```

---

## 1️⃣3️⃣ `services/` — Cross-Cutting Shared Services

**Purpose:** Services used by multiple modules and routes  
**Principle:** Framework-level utilities (NOT business logic)  
**Total files:** 16 Python modules

### Structure

```
services/
├── __init__.py
├── document.py                    [FACADE: Re-exports document operations]
├── document_query.py              [Read-only: get_doc, get_list, get_value]
├── document_mutation.py           [Write ops: new_doc, save_doc, delete_doc, apply_workflow_state]
├── naming.py                      [ID generation: PO-0001, WO-0042]
├── workflow.py                    [Workflow state management]
├── rbac.py                        [Role-based access control checks]
├── audit.py                       [Change history logging]
├── error_logger.py                [Exception tracking]
├── server_actions.py              [Registry for custom action functions]
├── query_link_handlers.py         [Dynamic field lookup dispatch]
├── socketio_manager.py            [Real-time WebSocket events]
├── print_service.py               [HTML/PDF rendering]
├── export_service.py              [CSV/XLSX export]
├── import_export.py               [Bulk CSV/XLSX/Google Sheets import]
└── scheduler.py                   [APScheduler wrapper for cron jobs]
```

### Key Services Explained

#### `services/document.py` (THE FACADE)

```python
# Central gateway for all document operations
from app.services.document_query import get_doc, get_list, get_value, get_meta
from app.services.document_mutation import new_doc, save_doc, delete_doc, apply_workflow_state

__all__ = [
    "get_doc", "get_list", "get_value", "get_meta",
    "new_doc", "save_doc", "delete_doc", "apply_workflow_state"
]
```

**Why this exists:** Single import point for all modules and routes  
**Used by:** ~60+ files across infrastructure, routers, hooks, services

#### `services/naming.py`

```
Purpose: Generate unique IDs for records
Example calls:
  - generate_id(db, NamingMeta(prefix="PO", start=1)) → "PO-0001"
  - generate_id(db, NamingMeta(prefix="WO", start=100)) → "WO-0100"

Used by: document_mutation.py (on new_doc)
         purchase_order.py API (manual ID generation)
         import_export.py (batch ID generation)
```

#### `services/scheduler.py`

```
Purpose: APScheduler wrapper for background jobs
Jobs scheduled:
  1. run_maintenance_calendar_generation() — Generate PM schedule (hourly)
  2. run_maintenance_condition_generation() — Check asset conditions
  3. run_maintenance_interval_generation() — Check time-based intervals
  4. inventory_low_stock_notification() — Alert on low inventory

Started during: main.py lifespan startup
Stopped during: main.py lifespan shutdown
```

#### `services/socketio_manager.py`

```
Purpose: Real-time WebSocket event broadcasting
Methods:
  - emit_created(entity, record_dict)
  - emit_updated(entity, record_dict)
  - emit_deleted(entity, record_id)
  - emit_post_save(entity, record_dict, action)
  - notify_user(user_id, message_type, data)

Used by: All CRUD routes (on success)
         Hooks (on side effects)
Result: Frontend lists auto-refresh in real-time
```

#### `services/rbac.py`

```
Purpose: Permission checking (cached)
Methods:
  - check_permission(user, entity, action) → bool
  - check_permission_async(db, user, entity, action) → bool  [with DB fallback]
  - get_permissions(role_id, entity) → dict[action: bool]

Cache: uses permission_cache.py (5-min TTL)
Result: Fast permission checks without DB roundtrip
```

#### `services/print_service.py`

```
Purpose: Render HTML and convert to PDF
Input: entity_name, record_id, format (html or pdf)
Output: HTML string or PDF bytes
Process:
  1. Load print assembler for entity
  2. Render Jinja2 template
  3. If PDF: convert HTML → PDF
  4. Return result
```

---

## 1️⃣4️⃣ `templates/` — Jinja2 Templates

**Purpose:** Email and print templates (Jinja2 format)

### Structure

```
templates/
├── email/                         [Email templates]
│   ├── purchase_request_created.html
│   ├── work_order_created.html
│   ├── maintenance_request_assigned.html
│   └── ... (notification templates)
├── print/                         [Print/report templates]
│   ├── work_order.html
│   ├── purchase_order.html
│   ├── inventory_report.html
│   └── ... (report templates)
└── reports/                       [Report generation templates]
    ├── stock_count_summary.html
    ├── maintenance_schedule.html
    └── ... (report templates)
```

### Usage

**Email templates:**

```python
# app/infrastructure/email/template_renderer.py
renderer = JinjaEmailTemplateRenderer()
html = renderer.render("purchase_request_created", {
    "pr_number": "PR-0001",
    "requester": "John Doe",
    "items": [...]
})
```

**Print templates:**

```python
# app/services/print_service.py
html = renderer.render("work_order", {
    "work_order": wo_dict,
    "assignee": user_dict,
    "tasks": tasks_list
})
pdf = convert_html_to_pdf(html)
```

---

## Other Folders (Briefly)

### `backups/` — Database Backups

```
Purpose: Store database dumps and metadata backups
Contains:
  - eam_db_full_20260206_185851.dump [Full DB backup]
  - metadata/ [Metadata snapshots]
  - models/ [Model snapshots]
```

### `domain/exceptions.py`

```
Purpose: Define domain-level exceptions
Example: BusinessValidationError, InvalidWorkflowTransition
Why separate: Exceptions are part of domain contract
```

---

## 📈 Architecture Summary

### Layer Stack (Bottom to Top)

```
┌─────────────────────────────────────────────────┐
│ API Layer (HTTP)                                │
│ ├─ api/routes/* [Entity CRUD - 22 handlers]    │
│ └─ routers/* [Framework - Auth, Admin, Config] │
├─────────────────────────────────────────────────┤
│ Schema Layer                                    │
│ └─ schemas/* [Pydantic request/response]        │
├─────────────────────────────────────────────────┤
│ Application Layer                               │
│ ├─ application/services/* [Orchestration]      │
│ ├─ application/hooks/* [Lifecycle management]  │
│ └─ services/* [Cross-cutting utilities]        │
├─────────────────────────────────────────────────┤
│ Infrastructure Layer                            │
│ ├─ infrastructure/database/repositories/* [ORM]│
│ ├─ infrastructure/email/* [SMTP]               │
│ ├─ infrastructure/auth/* [JWT, passwords]      │
│ ├─ infrastructure/print/* [PDF rendering]      │
│ └─ infrastructure/* [External services]        │
├─────────────────────────────────────────────────┤
│ Core Framework Layer                            │
│ ├─ core/framework/models/* [Base models]       │
│ ├─ core/database.py [DB setup]                 │
│ ├─ core/security.py [JWT parsing]              │
│ ├─ core/loader.py [Dynamic loading]            │
│ └─ core/* [Config, seeding, exceptions]        │
├─────────────────────────────────────────────────┤
│ Domain Layer                                    │
│ └─ domain/protocols/* [Abstract contracts]     │
├─────────────────────────────────────────────────┤
│ Module Layer (Autonomous)                       │
│ ├─ modules/core_eam/* [Org data]               │
│ ├─ modules/purchasing_stores/* [Procurement]  │
│ ├─ modules/asset_management/* [Assets]        │
│ ├─ modules/maintenance_mgmt/* [PM]             │
│ └─ modules/work_mgmt/* [Execution]            │
├─────────────────────────────────────────────────┤
│ Config/Utility Layer                            │
│ ├─ entities/* [Entity metadata generation]     │
│ ├─ meta/registry.py [Runtime metadata lookup]  │
│ ├─ templates/* [Jinja2 templates]              │
│ └─ models/__init__.py [Re-exports]             │
└─────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision                 | Why                                              | Implementation                          |
| ------------------------ | ------------------------------------------------ | --------------------------------------- |
| Dual API paths           | Separate framework concerns from entity concerns | `routers/` + `api/`                     |
| Generic entity routes    | Scale with metadata, no per-entity router        | 22 route handlers serve 100+ entities   |
| Metadata-driven          | No hardcoded entity knowledge                    | `meta/registry.py` + JSON definitions   |
| Hook system              | Extend behavior without modifying shared code    | `application/hooks/registry.py`         |
| Module load order        | Respect module dependencies                      | `core/loader.py` MODULE_LOAD_ORDER      |
| Centralized repositories | All ORM queries in one place                     | `infrastructure/database/repositories/` |

---

## ⚠️ Common Confusions Clarified

### "Why both `api/` and `routers/`?"

- **`api/`** = Entity CRUD routes (generic, metadata-driven)
- **`routers/`** = Framework routes (auth, admin, config, specific use cases)
- **Not redundant.** They serve different architectural layers.

### "Why both `api/routes/` and `api/schemas/`?"

- **`routes/`** = HTTP endpoint handlers
- **`schemas/`** = Pydantic request/response models (referenced by routes)
- **Common pattern.** Separates concerns: routing logic vs. data validation.

### "Why is `apis/` a re-export?"

- **Historical.** Early design had APIs in `apis/`
- **Current.** Moved to `application/services/`
- **Kept for.** Backward compatibility (don't break old imports)
- **Status.** Deprecated. Use canonical location: `application/services/base_entity_api.py`

### "Why both `core/display_names.py` and `application/services/display_name_service.py`?"

- **Canonical.** `core/display_names.py` (4 production imports)
- **Deprecated.** `application/services/display_name_service.py` (3 dashboard imports)
- **Recommendation.** Consolidate to `core/display_names.py`

### "Why separate `services/` and `application/services/`?"

- **`services/`** = Cross-cutting utilities (naming, RBAC, audit, SocketIO)
- **`application/services/`** = Business orchestration (entity_service, auth_service, workflows)
- **Different purposes.** One is framework layer, one is application layer

---

## Total Metrics

| Metric                    | Count                                        |
| ------------------------- | -------------------------------------------- |
| Total Python files        | 380+                                         |
| Total lines of code       | 16,061                                       |
| Top-level directories     | 14                                           |
| API route handlers        | 22                                           |
| Router modules            | 7                                            |
| Application services      | 16                                           |
| Infrastructure services   | 20+                                          |
| Domain modules            | 5                                            |
| Entities (auto-generated) | 100+                                         |
| Framework core models     | 4 (Auth, Infrastructure, Workflow, Ordering) |

---

## ✅ Conclusion

The `/backend/app` directory structure is **intentional and coherent**:

1. **Separation of concerns** — Layers are cleanly separated (API, Application, Infrastructure, Domain)
2. **Modularity** — 5 standalone domain modules with consistent vertical slicing
3. **Metadata-driven** — New entities added without touching routers
4. **Scalable** — 22 generic route handlers serve 100+ entities
5. **Extensible** — Hook system allows modules to extend behavior

**No redundancy.** Every folder and file serves a specific architectural purpose.
