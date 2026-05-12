# Story 5: Generic Widget Renderer Component

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P1 — Requires Story 4

## Story

As a frontend developer, I need a single `DashboardWidget.vue` component that accepts a canonical widget metadata object and renders the appropriate sub-template, so the dashboard page never needs to know what widget types exist.

## Context

Currently widget rendering is distributed across the dashboard page and several inline templates. The metadata-driven model requires one entry-point component that branches on `type`. This component hosts four sub-templates:

- `stat_card` — Nuxt UI `UCard` with a large numeric/string value, a label, and an optional trend badge
- `donut_chart` — Unovis `VisDonut` inside `VisSingleContainer`, driven by `segments`
- `table_list` — Nuxt UI `UTable` with `columns` and `rows` from widget data
- `bar_chart` — Unovis `VisXYContainer` + `VisGroupedBar` + `VisAxis` driven by `x_key`, `y_keys`, `items`

## Acceptance Criteria

- [ ] `DashboardWidget.vue` created at `frontend/app/components/dashboard/DashboardWidget.vue`
- [ ] Component prop: `widget: DashboardWidget` (typed from composable)
- [ ] `stat_card` branch renders value, label, optional trend indicator (up/down icon + number)
- [ ] `donut_chart` branch renders Unovis `VisDonut` with color-mapped segments and optional center label overlay
- [ ] `table_list` branch renders `UTable` with dynamic `columns` and `rows`; respects `config.readonly`
- [ ] `bar_chart` branch renders Unovis `VisXYContainer` + `VisGroupedBar` using `x_key`, `y_keys`, `items`; axes labeled with `x_label` / `y_label`
- [ ] Each branch is wrapped in a `UCard` with the widget `title` in the card header
- [ ] `config.readonly` shows a `UBadge label="Read-only"` in the card header when true
- [ ] No widget-specific logic leaks into the parent dashboard page
- [ ] No TypeScript errors (`pnpm typecheck` passes)

## Technical Notes

Unovis bar chart for Vue:
```vue
<VisXYContainer :data="barData">
  <VisGroupedBar :x="(d, i) => i" :y="yAccessors" />
  <VisAxis type="x" :tickFormat="(i) => items[i]?.[x_key]" :label="x_label" />
  <VisAxis type="y" :label="y_label" />
</VisXYContainer>
```
where `yAccessors` is an array of `(d) => d[key]` functions, one per entry in `y_keys`.

Color mapping for donut segments: use the segment's `color` field as a Tailwind/Nuxt UI color token mapped to a CSS variable, falling back to gray.

Use `v-if` / `v-else-if` chains at the top of the template — do not use dynamic component lookup to preserve type inference.

## Tasks

1. Create `frontend/app/components/dashboard/DashboardWidget.vue`
2. Implement `stat_card` branch
3. Implement `donut_chart` branch (reuse Unovis `VisDonut` pattern from existing dashboard page)
4. Implement `table_list` branch with `UTable`
5. Implement `bar_chart` branch with Unovis `VisXYContainer` + `VisGroupedBar` + `VisAxis`
6. Add readonly badge logic
7. Run `pnpm typecheck`

## Definition of Done

- [ ] Component renders all four widget types without errors
- [ ] Manual visual test: each branch renders correctly with mock data
- [ ] `pnpm typecheck` passes
- [ ] Component is self-contained — no parent-level widget logic required
