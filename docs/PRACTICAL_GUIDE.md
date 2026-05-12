# Backend Development: Practical Guide

**Filename:** `PRACTICAL_GUIDE.md`  
**Audience:** Developers working on the backend  
**Purpose:** Day-to-day reference for common tasks

---

## 🎯 Common Tasks & Where to Do Them

### Task 1: Add a New Entity Type

**Scenario:** Need to add a new entity (e.g., "Vendor")

**Steps:**

#### Step 1: Create Entity Definition (JSON)

```
File: modules/core_eam/entities/vendor.json

{
  "entity": "vendor",
  "title": "Vendor",
  "fields": [
    {
      "name": "name",
      "field_type": "text",
      "required": true,
      "title": "Vendor Name"
    },
    {
      "name": "contact_email",
      "field_type": "email",
      "title": "Contact Email"
    },
    {
      "name": "is_active",
      "field_type": "checkbox",
      "default": true
    }
  ],
  "naming": {
    "prefix": "VEN",
    "start_number": 1
  },
  "title_field": "name",
  "workflows": {
    "default": ["active", "inactive"]
  }
}
```

#### Step 2: Regenerate Models

```bash
python forge.py sync -m "add vendor entity"
```

This will:

- Generate `modules/core_eam/models/vendor.py`
- Create Alembic migration
- Run migration (create table)

#### Step 3: Entity is Live

All 22 route handlers work automatically:

- `POST /api/entity/vendor/action` — Create
- `PUT /api/entity/vendor/action` — Update
- `GET /api/entity/vendor/list` — List
- `POST /api/entity/vendor/workflow` — State transitions
- `GET /api/entity/vendor/{id}/audit` — Change history
- etc.

#### Step 4: Add Business Logic (Optional)

```
File: modules/core_eam/apis/vendor.py

async def validate_vendor(doc, db):
    """Validate vendor before save"""
    if not doc.get("name"):
        raise ValueError("Vendor name is required")

    # Check for duplicates
    existing = await db.execute(
        select(Vendor).where(Vendor.name == doc["name"])
    )
    if existing.scalar_one_or_none():
        raise ValueError("Vendor with this name already exists")
```

#### Step 5: Register Lifecycle Hooks (Optional)

```
File: modules/core_eam/hooks.py (add to existing file)

from app.application.hooks.registry import hook_registry

@hook_registry.before_save("vendor")
async def vendor_before_save(doc, ctx):
    await validate_vendor(doc, ctx.db)

@hook_registry.after_save("vendor")
async def vendor_after_save(doc, ctx):
    # Send notification
    await notify_vendor_created(doc, ctx.user)
```

**Result:** Fully functional entity with validation, notifications, audit trail, permissions

---

### Task 2: Create a Custom Endpoint

**Scenario:** Need a special endpoint for "Get vendor statistics"

**Steps:**

#### Step 1: Create Route Handler

```
File: api/routes/vendor_stats.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user_from_token, CurrentUser

router = APIRouter(prefix="/vendor-stats", tags=["vendor"])

@router.get("/")
async def get_vendor_statistics(
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user_from_token),
):
    """Get vendor statistics (total vendors, active, etc.)"""
    # Check permission
    if not await RBACService.check_permission_async(db, user, "vendor", "read"):
        raise HTTPException(status_code=403, detail="No permission")

    # Call service
    stats = await VendorStatsService(db).calculate()

    return ActionResponse(status="success", data=stats)
```

#### Step 2: Register in main.py

```
File: main.py (add to router registration)

from app.api.routes import vendor_stats

fastapi_app.include_router(vendor_stats.router, prefix="/api")
```

#### Step 3: Test

```bash
curl http://localhost:8000/api/vendor-stats/
```

**Key Points:**

- All routes must check RBAC permission
- Return `ActionResponse` for consistency
- Call application services, not repositories directly
- No business logic in the route handler

---

### Task 3: Add a Scheduled Background Job

**Scenario:** Generate vendor performance report every day at midnight

**Steps:**

#### Step 1: Implement Job Function

```
File: modules/core_eam/apis/vendor_report.py

async def generate_vendor_performance_report(db):
    """Generate daily vendor performance report

    This is called by APScheduler.
    """
    try:
        # Calculate metrics
        metrics = await calculate_vendor_metrics(db)

        # Store results
        await save_report(db, {
            "date": datetime.now(),
            "metrics": metrics,
            "generated_at": datetime.now()
        })

        logger.info(f"✅ Vendor report generated: {metrics}")
    except Exception as e:
        logger.error(f"❌ Vendor report failed: {e}")
        raise
```

#### Step 2: Register with Scheduler

```
File: services/scheduler.py (add to start_scheduler())

from app.modules.core_eam.apis.vendor_report import generate_vendor_performance_report

def start_scheduler():
    scheduler = BackgroundScheduler()

    # ... existing jobs ...

    # Add new job: Daily at 00:00
    scheduler.add_job(
        generate_vendor_performance_report,
        trigger="cron",
        hour=0,
        minute=0,
        kwargs={"db": db},
        id="vendor_performance_report"
    )

    scheduler.start()
```

**Result:** Job runs daily at midnight, generates report, stores in database

---

### Task 4: Send an Email Notification

**Scenario:** Send email when a vendor is created

**Steps:**

#### Step 1: Create Email Template

```
File: templates/email/vendor_created.html

<html>
  <body>
    <h1>New Vendor Created</h1>
    <p>A new vendor has been added to the system:</p>
    <p><strong>{{ vendor_name }}</strong></p>
    <p>Email: {{ vendor_email }}</p>
  </body>
</html>
```

#### Step 2: Register Hook

```
File: modules/core_eam/hooks.py

@hook_registry.after_save("vendor")
async def vendor_after_save(doc, ctx):
    # Send email notification
    from app.application.email_notifications.dispatcher import EmailDispatcher

    dispatcher = EmailDispatcher(ctx.db)
    await dispatcher.send(
        to=ctx.user.email,
        subject="New Vendor: {}".format(doc.get("name")),
        template="vendor_created.html",
        context={
            "vendor_name": doc.get("name"),
            "vendor_email": doc.get("contact_email")
        }
    )
```

**Result:** Email sent automatically when vendor is created

---

### Task 5: Add Validation to an Entity

**Scenario:** Ensure vendor email is unique, name is not empty

**Steps:**

#### Step 1: Update Business Logic

```
File: modules/core_eam/apis/vendor.py

async def validate_vendor_create(doc, db):
    """Validate vendor on create"""
    # Required field
    if not doc.get("name"):
        raise ValueError("Vendor name is required")

    # Unique email
    if doc.get("contact_email"):
        existing = await db.execute(
            select(Vendor).where(
                Vendor.contact_email == doc["contact_email"]
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("Email already registered to another vendor")

    return True

async def validate_vendor_update(doc, db):
    """Validate vendor on update"""
    # Same as create, but also check if updating same record
    ...
```

#### Step 2: Register Hook

```
File: modules/core_eam/hooks.py

@hook_registry.before_save("vendor")
async def vendor_before_save(doc, ctx):
    if ctx.action == "create":
        await validate_vendor_create(doc, ctx.db)
    elif ctx.action == "update":
        await validate_vendor_update(doc, ctx.db)
```

**Result:** Validation runs before save, errors returned to client

---

### Task 6: Add a Custom Action

**Scenario:** "Mark vendor as inactive" button on UI

**Steps:**

#### Step 1: Create Action Function

```
File: modules/core_eam/apis/vendor_actions.py

from app.services.server_actions import server_actions

@server_actions.register("vendor", "mark_inactive")
async def mark_vendor_inactive(ctx):
    """Custom action: Mark vendor as inactive"""
    vendor_id = ctx.record_id

    # Get vendor
    vendor = await get_doc("vendor", vendor_id, ctx.db, as_dict=True)

    # Update
    vendor["is_active"] = False
    await save_doc(vendor, ctx.db)

    return {
        "status": "success",
        "message": f"Vendor marked inactive"
    }
```

#### Step 2: Test from UI

```
POST /api/entity/vendor/{vendor_id}/action/mark_inactive

Response:
{
  "status": "success",
  "message": "Vendor marked inactive"
}
```

**Result:** Custom action available in UI

---

## 📚 Layered Design in Practice

### DO: Follow Clean Architecture

✅ **GOOD:**

```python
# In api/routes/entity_list.py (Route handler)
@router.get("/{entity}/list")
async def get_entity_list(
    entity: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # Check permission
    # Call service
    # Return response

    service = EntityListService(db, user)
    records = await service.get_list(entity, page=1, page_size=20)
    return ActionResponse(status="success", data=records)
```

❌ **BAD:**

```python
# DO NOT do business logic in route
@router.get("/vendor/list")
async def get_vendor_list(db: AsyncSession):
    # Don't query directly here!
    result = await db.execute(select(Vendor))

    # Don't transform here!
    vendors = []
    for v in result.scalars():
        vendors.append({
            "id": v.id,
            "name": v.name,
            "custom_calc": complex_calculation(v)  # Wrong layer!
        })

    return vendors
```

### DO: Use Services, Not Repositories, in Routes

✅ **GOOD:**

```python
# In application/services/entity_service.py
class EntityService:
    async def get_list(self, entity, filters):
        repo = EntityRepository(self.db)
        records = await repo.get_list(entity, filters)
        return records

# In api/routes/entity_list.py
@router.get("/{entity}/list")
async def get_entity_list(
    entity: str,
    service: EntityService = Depends(get_entity_service),
):
    records = await service.get_list(entity, {})
    return ActionResponse(status="success", data=records)
```

❌ **BAD:**

```python
# Route calling repository directly
@router.get("/{entity}/list")
async def get_entity_list(
    entity: str,
    repo: EntityRepository = Depends(get_entity_repo),  # Direct repo access
):
    records = await repo.get_list(entity, {})
    return ActionResponse(status="success", data=records)
```

### DO: Keep Repositories ORM-Only

✅ **GOOD:**

```python
# In infrastructure/database/repositories/entity_repository.py
class EntityRepository:
    async def get_by_id(self, entity: str, id: Any):
        model = get_entity_model(entity)
        result = await self.db.execute(
            select(model).where(model.id == id)
        )
        return result.scalar_one_or_none()
```

❌ **BAD:**

```python
# Repository doing business logic
class EntityRepository:
    async def get_by_id(self, entity: str, id: Any):
        # Wrong: mixing ORM and business logic
        model = get_entity_model(entity)
        result = await self.db.execute(
            select(model).where(model.id == id)
        )

        # Applying business logic here
        if result.workflow_state == "draft":
            # check permissions
            # calculate derived fields
            # apply transformations

        return result
```

---

## 🐛 Debugging Tips

### "My route doesn't work"

**Check:**

1. Is the route registered in `main.py`?
2. Is the prefix correct?
3. Did you check the RBAC permission?
4. Is the service being injected correctly?

### "My hook isn't running"

**Check:**

1. Did you register it in `hooks.py`?
   ```python
   @hook_registry.before_save("entity_name")
   async def my_hook(doc, ctx):
       pass
   ```
2. Is the module being loaded? Check `core/loader.py`
3. Is the entity name spelled correctly?
4. Is the action correct (before_save, after_save, etc.)?

### "My permission always fails"

**Check:**

1. Is the entity in the permission matrix?
   - Admin panel → /api/admin/permissions/matrix
2. Is the user assigned the correct role?
3. Is the role assigned the action permission?
4. Did you clear the permission cache?
   ```python
   # Cache TTL is 5 minutes
   # Or restart the app
   ```

### "Entity not found"

**Check:**

1. Run `forge.py sync` to regenerate models
2. Check entity name (case-sensitive): `"purchase_order"` not `"PurchaseOrder"`
3. Is the entity JSON in `modules/{module}/entities/{entity}.json`?
4. Is the module loaded? Check console output at startup

---

## 📋 File Creation Checklist

### Adding a New Entity Type

- [ ] Create `modules/{module}/entities/{entity}.json`
- [ ] Run `forge sync` to generate model
- [ ] Create `modules/{module}/apis/{entity}.py` (optional business logic)
- [ ] Add hooks in `modules/{module}/hooks.py` (optional)
- [ ] Test via `/api/entity/{entity}/list`
- [ ] Set up permissions in `/api/admin/permissions/matrix`

### Adding a Custom Endpoint

- [ ] Create `api/routes/{feature}.py`
- [ ] Register router in `main.py`
- [ ] Check RBAC permission in endpoint
- [ ] Call application service (not repository)
- [ ] Return `ActionResponse`
- [ ] Test endpoint manually

### Adding Validation

- [ ] Create validation function in `modules/{module}/apis/{entity}.py`
- [ ] Register `@hook_registry.before_save("{entity}")` in `hooks.py`
- [ ] Raise `ValueError` with clear error message
- [ ] Test: try invalid data, should get error in response

### Adding Business Logic

- [ ] Implement function in `modules/{module}/apis/{entity}.py`
- [ ] Register as hook or server action
- [ ] Call `get_doc()` and `save_doc()` from facade
- [ ] No direct repository calls
- [ ] Handle errors gracefully

---

## 🏃 Quick Start: 5-Minute Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Initialize Database

```bash
python forge.py migrate
python forge.py seed
```

### 4. Start Server

```bash
python -m uvicorn app.main:fastapi_app --reload
```

### 5. Test API

```bash
curl http://localhost:8000/api/entity/site/list

# Response:
{
  "status": "success",
  "data": [...sites...]
}
```

---

## 🎓 Learning Path

**Week 1: Understand Structure**

- Read DIRECTORY_STRUCTURE_AUDIT.md
- Read ARCHITECTURE_VISUAL_GUIDE.md
- Explore folders with `ls -la`

**Week 2: Build Something**

- Add a simple entity (JSON + validation)
- Add a custom endpoint
- Send an email notification

**Week 3: Deep Dive**

- Study `application/services/entity_service.py`
- Study `infrastructure/database/repositories/entity_repository.py`
- Implement custom business logic

**Week 4: Advanced**

- Add scheduled background job
- Implement complex workflow
- Optimize queries

---

## ✅ Code Review Checklist

When reviewing backend PRs, check:

- [ ] No business logic in route handlers
- [ ] Services called via dependency injection
- [ ] All ORM queries in repositories only
- [ ] RBAC permission checked in route
- [ ] No direct `db.execute()` in routes
- [ ] Hooks registered correctly
- [ ] Validation happens in business logic
- [ ] Errors return `ActionResponse` with status="error"
- [ ] Entity names match JSON definitions
- [ ] Tests pass: `pytest tests/`

---

## 📞 Common Questions

**Q: Where do I put a utility function?**  
A: If framework-wide → `core/`, if cross-module → `services/`, if module-specific → `modules/{module}/apis/`

**Q: How do I access the current user?**  
A: Inject `user: CurrentUser = Depends(get_current_user_from_token)`

**Q: How do I get an entity's metadata?**  
A: Use `MetaRegistry.get("entity_name")` (returns EntityMeta)

**Q: How do I run a SQL query directly?**  
A: Don't. Use repositories instead. If absolutely needed → `infrastructure/database/repositories/`

**Q: How do I create multiple records in a transaction?**  
A: Use `async with db.begin():` block (auto-rollback on error)

**Q: How do I debug a hook?**  
A: Add `print()` or use `logger.info()`, then check console output

---

## 📚 Further Reading

1. DIRECTORY_STRUCTURE_AUDIT.md — What each folder does
2. ARCHITECTURE_VISUAL_GUIDE.md — Visual diagrams
3. DETAILED_FINDINGS.md — Deep technical analysis
4. test files in `tests/` — Real examples of usage
5. `application/services/entity_service.py` — Core orchestration logic
6. `infrastructure/database/repositories/entity_repository.py` — Generic CRUD

---

## 🚀 Ready to Code!

You now understand:

- ✅ Why each folder exists
- ✅ What files go in each folder
- ✅ How data flows through layers
- ✅ How to add entities, endpoints, validations
- ✅ How to follow Clean Architecture principles

**Happy coding!**
