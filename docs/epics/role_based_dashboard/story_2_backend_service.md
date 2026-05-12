# Story 2: Backend Widget Data Fetchers Refactor

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P0 — Required before Story 3

## Story

As a backend developer, I need to refactor the widget data fetching layer so each widget type has a dedicated async fetcher that returns data conforming to the canonical metadata schema, making the orchestrator trivially composable.

## Context

The current `RoleBasedDashboardService` mixes widget resolution, data fetching, and response shaping into one class. Moving to a metadata-driven contract requires each fetcher to own its SQL queries and produce a typed `DashboardWidget` dict as output. The orchestrator (Story 3) will call these fetchers and assemble the response.

## Acceptance Criteria

- [ ] Each dashboard has its own fetcher module under `backend/app/application/fetchers/`
  - `procurement_fetchers.py` — PR status summary, PR attention list, PO activity bar chart
  - `work_management_fetchers.py` — work order summary, overdue stat card, activity by type bar chart
  - `inventory_fetchers.py` — inventory health stat cards, low stock table, movement bar chart
- [ ] Every fetcher function signature: `async def fetch_<widget_id>(db: AsyncSession, ...) -> dict`
- [ ] Every fetcher returns a fully-shaped `DashboardWidget` dict (widget_id, type, title, config, data)
- [ ] `data` field conforms to the Pydantic model defined in Story 1 for the declared `type`
- [ ] `RoleBasedDashboardService` is simplified to: resolve role → list of `(fetcher_fn, kwargs)` tuples
- [ ] All existing SQL logic is preserved; SQL queries are moved into the appropriate fetcher module
- [ ] `asyncio.gather()` is still used to run fetchers concurrently per dashboard

## Technical Notes

Each fetcher returns a complete widget dict, e.g.:
```python
async def fetch_pr_status_summary(db: AsyncSession, readonly: bool) -> dict:
    # SQL query here
    return {
        "widget_id": "pr_status_summary",
        "type": "donut_chart",
        "title": "PR Status Breakdown",
        "config": {"readonly": readonly},
        "data": {
            "segments": [...],
            "center_label": f"{total} Total"
        }
    }
```

`RoleBasedDashboardService` becomes a resolver that maps role → list of fetcher callables:
```python
ROLE_FETCHERS: dict[str, list[FetcherSpec]] = {
    "Purchasing Coordinator": [
        FetcherSpec(fn=fetch_pr_status_summary, dashboard="procurement"),
        FetcherSpec(fn=fetch_pr_attention_list, dashboard="procurement"),
        FetcherSpec(fn=fetch_inventory_health, dashboard="inventory"),
    ],
    ...
}
```

`FetcherSpec` is a lightweight dataclass carrying `fn`, `dashboard`, and any extra kwargs.

## Tasks

1. Create `backend/app/application/fetchers/__init__.py`
2. Create `procurement_fetchers.py` with the three procurement widget fetchers; move existing PR SQL queries
3. Create `work_management_fetchers.py` with work order fetchers; move existing WO SQL queries
4. Create `inventory_fetchers.py` with inventory fetchers; move existing inventory SQL queries
5. Define `FetcherSpec` dataclass in fetchers `__init__.py`
6. Rewrite `RoleBasedDashboardService` to use `ROLE_FETCHERS` map and `FetcherSpec` tuples
7. Validate: run `python -m py_compile` on all modified files

## Definition of Done

- [ ] Fetcher modules created with all widget fetchers
- [ ] Each fetcher returns a correctly shaped widget dict
- [ ] `RoleBasedDashboardService` simplified to a resolver + `asyncio.gather()` call
- [ ] All existing SQL queries preserved (moved, not rewritten) in fetcher modules
- [ ] `py_compile` passes on all changed Python files
