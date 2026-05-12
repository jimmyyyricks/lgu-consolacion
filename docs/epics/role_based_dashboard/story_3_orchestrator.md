# Story 3: Backend Orchestrator and API Response

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P0 — Requires Story 2

## Story

As a backend developer, I need the orchestrator to assemble the metadata-driven response envelope so `GET /operations/dashboard/role-based` returns `allowed_dashboards` and `selected_dashboard.widgets` in the canonical widget metadata format.

## Context

The existing `RoleBasedDashboardOrchestrator` builds the response but passes through the old widget shapes. After Story 2 refactors the fetchers to return canonical widget dicts, the orchestrator needs only minor surgery: collect fetcher output keyed by dashboard, build `allowed_dashboards`, select the requested dashboard, and return its widgets.

## Acceptance Criteria

- [ ] `RoleBasedDashboardOrchestrator.orchestrate()` calls `RoleBasedDashboardService` to get `FetcherSpec` list
- [ ] Orchestrator groups fetcher specs by `dashboard` key to derive `allowed_dashboards`
- [ ] Orchestrator runs only the fetchers for the selected dashboard via `asyncio.gather()`
- [ ] Response `selected_dashboard.widgets` is a list of canonical widget dicts
- [ ] `widget_id`, `type`, `title`, `config`, `data` are all present and non-null on every widget
- [ ] Missing or invalid `dashboard_key` falls back to the first allowed dashboard key
- [ ] API route returns HTTP 200 with the full envelope; no widget-specific route parameters needed
- [ ] `GET /operations/dashboard/role-based` response passes JSON schema validation against the Epic contract

## Technical Notes

Orchestrator outline:
```python
class RoleBasedDashboardOrchestrator:
    async def orchestrate(
        self,
        db: AsyncSession,
        current_user: CurrentUser,
        dashboard_key: str | None,
    ) -> RoleBasedDashboardResponse:
        specs = self.service.resolve_fetchers(current_user.roles)
        allowed = self._derive_allowed_dashboards(specs)
        selected_key = dashboard_key if dashboard_key in allowed else allowed[0].key
        widgets = await self._run_fetchers(db, specs, selected_key, current_user)
        return RoleBasedDashboardResponse(
            user_roles=current_user.roles,
            generated_at=datetime.utcnow(),
            allowed_dashboards=allowed,
            selected_dashboard=SelectedDashboard(widgets=widgets, **allowed_by_key[selected_key]),
        )
```

Pydantic response models live in `backend/app/schemas/dashboard.py`:
- `DashboardWidgetSchema` — wraps `widget_id`, `type`, `title`, `config`, `data: Any`
- `SelectedDashboardSchema` — extends `DashboardOption` with `widgets: list[DashboardWidgetSchema]`
- `RoleBasedDashboardResponse` — envelope with `user_roles`, `generated_at`, `allowed_dashboards`, `selected_dashboard`

## Tasks

1. Add/update `backend/app/schemas/dashboard.py` with Pydantic response models
2. Rewrite `RoleBasedDashboardOrchestrator.orchestrate()` to call Story 2 fetchers and return canonical schema
3. Update route handler in `backend/app/api/routes/operational_dashboard.py` to use updated schema
4. Validate response shape with a manual `httpx` call or existing test harness

## Definition of Done

- [ ] Orchestrator returns canonical widget dicts for the selected dashboard
- [ ] `allowed_dashboards` list is derived from role-fetcher mapping (not hardcoded)
- [ ] Response validates against the schema defined in Story 1
- [ ] `py_compile` passes on all changed Python files
- [ ] `dashboard_key` fallback to first allowed dashboard works when key is absent or invalid
