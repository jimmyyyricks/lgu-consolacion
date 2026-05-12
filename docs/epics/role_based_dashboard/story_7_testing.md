# Story 7: Testing — Backend pytest and Frontend Vitest

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P2 — Requires Stories 1–6

## Story

As a developer, I need automated tests that verify the canonical widget metadata schema is returned by the backend and that the frontend `DashboardWidget.vue` component correctly branches on each widget type, so regressions are caught before merging.

## Context

Testing two surfaces:
1. **Backend pytest** — unit tests for each fetcher function (data shape) and integration tests for the orchestrator (allowed dashboard selection, fallback, widget output).
2. **Frontend Vitest** — component tests for `DashboardWidget.vue` that mount it with mock widget metadata for each of the four types and assert the correct sub-template renders.

## Acceptance Criteria

### Backend

- [ ] `tests/test_widget_fetchers.py` — unit tests for each fetcher function: mocks DB session, asserts returned dict has `widget_id`, `type`, `title`, `config`, `data` keys and correct types
- [ ] `tests/test_orchestrator.py` — integration tests:
  - Role with access to procurement gets procurement in `allowed_dashboards`
  - Default `dashboard_key=None` returns first allowed dashboard
  - Invalid `dashboard_key` falls back to first allowed dashboard
  - Each widget in `selected_dashboard.widgets` conforms to widget metadata schema
- [ ] Tests use `pytest-asyncio` and `sqlalchemy.ext.asyncio` mock sessions

### Frontend

- [ ] `tests/components/DashboardWidget.spec.ts` — Vitest component tests:
  - `stat_card` widget mock: asserts value, label, and (optionally) trend text visible
  - `donut_chart` widget mock: asserts `VisDonut` is rendered, center label visible
  - `table_list` widget mock: asserts `UTable` renders with correct column headers and row count
  - `bar_chart` widget mock: asserts `VisXYContainer` is rendered
  - Readonly widget mock: asserts read-only badge visible
- [ ] Tests use `@nuxt/test-utils` or `@vue/test-utils` with `withSetup` from composable test helpers
- [ ] All tests pass with `pnpm test` (Vitest)

## Technical Notes

Backend test structure:
```python
@pytest.mark.asyncio
async def test_pr_status_summary_shape():
    db = AsyncMock()
    # mock query result
    result = await fetch_pr_status_summary(db, readonly=False)
    assert result["widget_id"] == "pr_status_summary"
    assert result["type"] == "donut_chart"
    assert "segments" in result["data"]
```

Frontend test structure:
```typescript
import { mountSuspended } from '@nuxt/test-utils/runtime'
import DashboardWidget from '~/components/dashboard/DashboardWidget.vue'
import { describe, it, expect } from 'vitest'

describe('DashboardWidget stat_card', () => {
  it('renders value and label', async () => {
    const widget = {
      widget_id: 'test_card',
      type: 'stat_card' as const,
      title: 'Open Work Orders',
      config: { readonly: false },
      data: { value: 42, label: 'Open' }
    }
    const wrapper = await mountSuspended(DashboardWidget, { props: { widget } })
    expect(wrapper.text()).toContain('42')
    expect(wrapper.text()).toContain('Open')
  })
})
```

## Tasks

1. Create `backend/app/epics/role_based_dashboard/tests/test_widget_fetchers.py`
2. Create `backend/app/epics/role_based_dashboard/tests/test_orchestrator.py`
3. Create `frontend/tests/components/DashboardWidget.spec.ts`
4. Run `pytest` and `pnpm test` and resolve any failures

## Definition of Done

- [ ] All backend unit tests pass for each widget fetcher function
- [ ] Orchestrator integration tests cover selection, fallback, and schema conformance
- [ ] Frontend component tests cover all four widget types and readonly
- [ ] `pytest` and `pnpm test` both exit with code 0
