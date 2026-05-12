# Story 4: Frontend Composable Refactor

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P1 — Requires Story 1 schema; can run in parallel with Stories 2–3

## Story

As a frontend developer, I need `useDashboard.ts` to reflect the canonical widget metadata schema so the composable is agnostic to individual widget implementations and can be consumed by any rendering component.

## Context

The current composable declares TypeScript interfaces for every widget data shape (`PRStatusSummaryData`, `PRAttentionListData`, `WorkOrderDashboard`, etc.). Under the new model, the composable only needs to know about the four canonical widget types. Per-widget data types move to the rendering layer (`DashboardWidget.vue`) where they are inferred from the `type` discriminant.

## Acceptance Criteria

- [ ] All per-widget data interfaces removed from `useDashboard.ts`
- [ ] Four canonical data interfaces added: `StatCardData`, `DonutChartData`, `TableListData`, `BarChartData`
- [ ] `DashboardWidget` interface uses a discriminated union on `type`
- [ ] `RoleBasedDashboard`, `SelectedDashboard`, `DashboardOption` interfaces updated to match Epic contract
- [ ] `getRoleBasedDashboard(dashboardKey?)` fetch function signature unchanged
- [ ] `useDashboard()` composable reactive state: `allowedDashboards`, `selectedDashboard`, `isLoading`, `error`
- [ ] `loadDashboard(key: string)` action re-fetches with the given key and updates state
- [ ] No TypeScript errors after refactor (`vue-tsc --noEmit` passes)

## Technical Notes

New composable shape (abbreviated):
```typescript
// types
type WidgetType = 'stat_card' | 'donut_chart' | 'table_list' | 'bar_chart'

interface StatCardData { value: number | string; label: string; trend?: number; color?: string }
interface DonutChartData { segments: { label: string; value: number; color: string }[]; center_label?: string }
interface TableListData { columns: { key: string; label: string }[]; rows: Record<string, unknown>[] }
interface BarChartData { x_key: string; y_keys: string[]; items: Record<string, unknown>[]; x_label?: string; y_label?: string }

type WidgetData = StatCardData | DonutChartData | TableListData | BarChartData

interface DashboardWidget {
  widget_id: string
  type: WidgetType
  title: string
  config: { readonly: boolean }
  data: WidgetData
}

interface DashboardOption { key: string; label: string; description: string; icon: string }
interface SelectedDashboard extends DashboardOption { widgets: DashboardWidget[] }
interface RoleBasedDashboard {
  user_roles: string[]
  generated_at: string
  allowed_dashboards: DashboardOption[]
  selected_dashboard: SelectedDashboard | null
}
```

Keep `STATUS_COLORS` map if still used by the table renderer; remove it if not.

## Tasks

1. Remove all per-widget specific data interfaces and legacy dashboard types from `useDashboard.ts`
2. Add the four canonical data types and updated `DashboardWidget` interface
3. Update `RoleBasedDashboard` and `SelectedDashboard` interfaces
4. Ensure `getRoleBasedDashboard` return type uses `RoleBasedDashboard`
5. Run `pnpm typecheck` and fix any errors

## Definition of Done

- [ ] Per-widget interfaces removed
- [ ] Canonical four-type schema present in composable
- [ ] `DashboardWidget` discriminated union is correct
- [ ] `pnpm typecheck` passes with no new errors
