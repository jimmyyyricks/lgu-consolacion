# Story 1: Architecture and Widget Metadata Contract

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P0 — Blocker for all other stories

## Story

As a tech lead, I need to define the canonical widget metadata schema so that backend and frontend teams share a single, version-stable contract before any implementation begins.

## Context

The current backend returns heterogeneous widget shapes that the frontend must know about in advance. The goal is a uniform envelope where each widget carries its own rendering instructions (`type`) alongside its `data`. Once the schema is agreed upon, all downstream stories implement to it without further design work.

## Acceptance Criteria

- [ ] A written schema specification exists in `docs/dashboard/widget_metadata_schema.md`
- [ ] Schema defines four widget types: `stat_card`, `donut_chart`, `table_list`, `bar_chart`
- [ ] Each widget type specifies the required and optional fields of its `data` object
- [ ] `config.readonly` field is defined at the widget level and controls frontend edit affordances
- [ ] `widget_id` field is a stable string identifier (snake_case, no spaces) used for keying and testing
- [ ] Schema document includes a JSON example for each widget type
- [ ] Frontend TypeScript interfaces in `useDashboard.ts` are updated to match the schema (no per-widget data types)

## Technical Notes

Widget metadata envelope (all types share this outer shape):
```typescript
interface DashboardWidget {
  widget_id: string            // stable snake_case key, e.g. "pr_status_summary"
  type: WidgetType             // "stat_card" | "donut_chart" | "table_list" | "bar_chart"
  title: string
  config: { readonly: boolean }
  data: StatCardData | DonutChartData | TableListData | BarChartData
}
```

Type-specific `data` shapes:
```typescript
interface StatCardData {
  value: number | string
  label: string
  trend?: number        // positive = up, negative = down
  color?: string        // Nuxt UI color token
}

interface DonutChartData {
  segments: Array<{ label: string; value: number; color: string }>
  center_label?: string
}

interface TableListData {
  columns: Array<{ key: string; label: string }>
  rows: Record<string, unknown>[]
}

interface BarChartData {
  x_key: string
  y_keys: string[]
  items: Record<string, unknown>[]
  x_label?: string
  y_label?: string
}
```

Python Pydantic counterparts will mirror these shapes in `app/schemas/dashboard_widgets.py`.

## Tasks

1. Create `docs/dashboard/widget_metadata_schema.md` with full schema spec and JSON examples
2. Create `backend/app/schemas/dashboard_widgets.py` with Pydantic models for each widget type
3. Update `frontend/app/composables/useDashboard.ts` — remove per-widget data interfaces, add the four canonical data type interfaces and the shared `DashboardWidget` interface

## Definition of Done

- [ ] Schema doc created at `docs/dashboard/widget_metadata_schema.md`
- [ ] Pydantic models added in `backend/app/schemas/dashboard_widgets.py`
- [ ] `useDashboard.ts` updated with canonical interfaces and no legacy per-widget types
- [ ] No TypeScript errors after composable update
