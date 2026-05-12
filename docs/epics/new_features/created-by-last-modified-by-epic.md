## Ownership Tracking Epic

### Goal

Add forward-looking ownership tracking to all domain records created through the unified CRUD flow.

This epic adds two new system fields to domain entities:

- `created_by`: immutable actor reference for the user who created the record
- `last_modified_by`: mutable actor reference for the user who last updated the record

Historical rows are out of scope. Existing records will remain `null` for both fields.

### Why

The system already captures `created_at` and `updated_at`, but not who performed the action. That makes operational tracing, accountability, and support investigations slower than they need to be.

The correct model here is:

- store `user.id`, not `username`
- keep the fields nullable
- inject the actor at the application boundary where request identity already exists
- protect `created_by` from later mutation

`user.id` is the stable industry-standard identifier. `username` is a mutable display attribute and belongs in audit snapshots, not in long-lived ownership columns.

### Scope

In scope:

- extend the shared SQLAlchemy `BaseModel`
- set actor IDs in the main entity create/update route
- set actor IDs in child bulk-save routes
- add an Alembic migration for all domain tables that already carry `created_at` and `updated_at`
- expose the fields automatically through the existing serializer

Out of scope:

- backfilling historical data
- frontend display changes
- strict database foreign key constraints to `core_users`
- replacing the existing audit log design

### Architecture

#### Domain / Core

`BaseModel` is the correct abstraction point because all trackable business entities inherit from it. Adding the fields here keeps the change open for extension and closed for per-entity duplication.

Fields:

- `created_by: String(36) | None`
- `last_modified_by: String(36) | None`

Both fields store `core_users.id` as a soft reference.

#### Application Boundary

The unified entity action route already resolves `CurrentUser` before `create` and `update`. That makes the API entrypoint the correct composition boundary for injecting ownership metadata.

Rules:

- create: set both `created_by` and `last_modified_by`
- update: preserve `created_by`, overwrite `last_modified_by`
- anonymous request: store `null`

The child bulk-save route must follow the same rules so nested writes do not drift from parent writes.

#### Infrastructure

The generic repository update path must block writes to `created_by` so callers cannot bypass immutability by sending a crafted payload.

#### Database

Migration strategy:

- inspect all tables
- target only non-core domain tables that already include `id`, `created_at`, and `updated_at`
- add `created_by` and `last_modified_by` when missing
- make the migration idempotent

This avoids per-table boilerplate and keeps the migration resilient across slightly divergent local databases.

### SOLID / Clean Architecture Notes

- Single Responsibility: `BaseModel` owns shared persistence metadata; routes compose request identity; repositories guard persistence invariants.
- Open/Closed: one base-model change extends all entities without touching each module model.
- Liskov Substitution: all `BaseModel` subclasses remain valid with nullable ownership fields.
- Interface Segregation: no repository protocol changes are required because the actor is composed before persistence.
- Dependency Inversion: request identity stays in the application layer; lower layers receive normalized data only.

### Implementation Steps

1. Extend `backend/app/core/base_model.py` with `created_by` and `last_modified_by`.
2. Update `backend/app/api/entries/entity_crud.py` to inject actor IDs in create/update flows.
3. Update `backend/app/api/entries/entity_children.py` to apply the same rules for child bulk saves.
4. Update `backend/app/infrastructure/database/repositories/entity_repository.py` to keep `created_by` immutable.
5. Add an Alembic migration to append both columns to domain tables.
6. Validate that the serializer exposes the new fields without schema changes.

### Verification

Functional checks:

- create a record with an authenticated user and confirm both fields equal that `user.id`
- update the same record and confirm only `last_modified_by` changes
- create a child row through bulk-save and confirm both fields are set
- update a child row through bulk-save and confirm `created_by` stays unchanged
- create anonymously and confirm both fields are `null`

Migration checks:

- upgrade applies cleanly on the current schema
- downgrade removes both fields cleanly
- pre-existing records remain untouched

### Risks

- Some custom write paths outside the unified routes may still bypass ownership injection.
- The backend currently runs on a Python 3.13 environment where Alembic import execution is broken; migration graph validation may require a compatible interpreter in CI or a downgraded local runtime.

### Follow-up

Separate follow-up work can surface the new fields in list/detail views by resolving `core_users.id` to a display name.
