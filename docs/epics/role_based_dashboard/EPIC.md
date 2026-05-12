# Epic: Metadata-Driven Role-Based Dashboard

**Status:** In Progress
**Created:** 2026-04-06
**Last Updated:** 2026-04-07

## Goal

Deliver a fully metadata-driven, role-based dashboard system where the backend owns the complete response contract — widget type, title, configuration, and data — while the frontend remains agnostic and renders any widget by delegating to a single generic `DashboardWidget` component.

## Problem

The current implementation couples the frontend to the backend response shape. `useDashboard.ts` declares concrete TypeScript types for each widget (`PRStatusSummaryData`, `PRAttentionListData`, `TopItem`, etc.) and the dashboard page directly switches on expected widget types. This means:

- Every new widget type requires parallel work on both backend and frontend TypeScript types
- The frontend must know the full set of possible widget types at compile time
- Dashboard rendering logic is spread across the page, composable, and API contract

The backend should be the single authority on what data to render and how. The frontend renders what the backend describes.

## Approach

### Backend

1. Define a canonical widget metadata schema: `{ widget_id, type, title, config, data }`.
2. Widget `type` is one of: `stat_card`, `donut_chart`, `table_list`, `bar_chart`.
3. The orchestrator returns this schema inside `selected_dashboard.widgets`.
4. Widget data fetchers are refactored into typed functions — one per widget — that each return the `data` shape expected by that widget type.
5. SQL queries stay close to the fetcher responsible for them.

### Frontend

1. `useDashboard.ts` is simplified: composable types mirror only the metadata schema, not individual widget data shapes.
2. A single `DashboardWidget.vue` component accepts `{ type, title, config, data }` and renders the appropriate sub-template using `v-if` branches per type.
3. `dashboard.vue` iterates `selected_dashboard.widgets` and renders `<DashboardWidget>` for each — no widget-specific code on the page.

## Widget Type Contract

| Type          | Frontend renderer branch | Backend `data` shape key fields                              |
| ------------- | ------------------------ | ------------------------------------------------------------ |
| `stat_card`   | StatCardWidget           | `value`, `label`, `trend?`, `color?`                         |
| `donut_chart` | DonutChartWidget         | `segments: [{label, value, color}]`, `center_label?`         |
| `table_list`  | TableListWidget          | `columns: [{key, label}]`, `rows: Record<string,unknown>[]`  |
| `bar_chart`   | BarChartWidget           | `x_key`, `y_keys`, `items: Record[]`, `x_label?`, `y_label?` |

## API Contract

```
GET /operations/dashboard/role-based?dashboard_key=procurement
Authorization: Bearer <token>
```

Response envelope:

```json
{
  "user_roles": ["Purchasing Coordinator"],
  "generated_at": "2026-04-07T08:30:00Z",
  "allowed_dashboards": [
    {
      "key": "procurement",
      "label": "Procurement",
      "description": "...",
      "icon": "i-lucide-shopping-cart"
    }
  ],
  "selected_dashboard": {
    "key": "procurement",
    "label": "Procurement",
    "description": "Purchase requests, approvals, and purchase order execution.",
    "icon": "i-lucide-shopping-cart",
    "widgets": [
      {
        "widget_id": "pr_status_summary",
        "type": "donut_chart",
        "title": "PR Status Breakdown",
        "config": { "readonly": false },
        "data": {
          "segments": [{ "label": "Draft", "value": 5, "color": "gray" }],
          "center_label": "42 Total"
        }
      }
    ]
  }
}
```

## Dashboard Definitions

| Key               | Label           | Primary purpose                                     |
| ----------------- | --------------- | --------------------------------------------------- |
| `procurement`     | Procurement     | PR and PO execution and approval visibility         |
| `work-management` | Work Management | Work orders, maintenance load, personal assignments |
| `inventory`       | Inventory       | Inventory health, low stock, stock count activity   |

## Role Access Model

| Role                   | Allowed Dashboards                      |
| ---------------------- | --------------------------------------- |
| Plant Manager          | Procurement, Work Management, Inventory |
| Maintenance Planner    | Work Management                         |
| Purchasing Coordinator | Procurement, Inventory                  |
| Purchaser              | Procurement                             |
| Requestor              | Procurement (readonly)                  |
| Warehouse Coordinator  | Inventory                               |
| Technician             | Work Management (readonly)              |
| Superuser              | Procurement, Work Management, Inventory |

## Story Map

| #   | Story                                        | Status |
| --- | -------------------------------------------- | ------ |
| 1   | Architecture and widget metadata contract    | To Do  |
| 2   | Backend widget data fetchers refactor        | To Do  |
| 3   | Backend orchestrator and API response        | To Do  |
| 4   | Frontend composable refactor                 | To Do  |
| 5   | Generic widget renderer component            | To Do  |
| 6   | Dashboard page integration                   | To Do  |
| 7   | Testing — backend pytest and frontend Vitest | To Do  |

## Definition of Done

- [ ] Widget metadata schema documented and agreed upon
- [ ] Backend returns `widget_id`, `type`, `title`, `config`, `data` for every widget
- [ ] Frontend composable types match the metadata schema only (no per-widget data types)
- [ ] `DashboardWidget.vue` renders all four widget types from metadata
- [ ] `dashboard.vue` contains no widget-specific rendering logic
- [ ] Backend pytest covers orchestrator selection and per-dashboard widget output
- [ ] Frontend Vitest covers `DashboardWidget.vue` rendering for each type
- [ ] Legacy dashboard endpoints remain available and unchanged
