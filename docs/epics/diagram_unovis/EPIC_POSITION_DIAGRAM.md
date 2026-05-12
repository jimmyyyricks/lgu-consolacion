# Epic: Position Diagram — Parallel Layout Redesign

**Status:** � Phase 1 Complete — Backend + Frontend + Tests done  
**Created:** 2026-04-21  
**Last Updated:** 2026-04-21  
**Tracker:** This file is the single source of truth for implementation status.

---

## 1. Problem Statement

The current diagram uses **ELK layout** (`GraphLayoutType.Elk`) via Unovis VisGraph. Two core problems:

1. **Panels overlap** — ELK does not leave space between panels, causing them to stack on top of each other with no way to move them out of the way.
2. **Nodes are too far apart** — ELK's spacing algorithm spreads nodes far from each other, making the diagram hard to navigate and read.

Additionally, the current grouping logic has a **critical bug** in the backend where `all_position_ids` is declared twice (the second declaration resets the set), causing ALL links to be dropped from the response.

---

## 2. Domain Understanding

### Positions

- Core entity representing a physical/logical slot in the system.
- Each position has an optional `location` (FK to Location).
- Positions link to each other via `position_relation` (fields: `position_a`, `position_b`).

### Locations

- Locations have a **parent_location** field → tree structure (parent-child nesting).
- A location can be a child of another location (e.g., Panel B is inside Room A).

### Grouping Taxonomy

| Category           | Condition                      | Group Value                                         | SubGroup Value     |
| ------------------ | ------------------------------ | --------------------------------------------------- | ------------------ |
| Placed & Connected | Has location + has ≥1 relation | `parent_location.name` (or `location.name` if root) | `location.name`    |
| No Connections     | Has location + NO relations    | `"No Connections"`                                  | `"No Connections"` |
| Unassigned         | Has NO location                | `"Unassigned"`                                      | `"Unassigned"`     |

**Priority rule:** If a position has no location → "Unassigned" (even if also connection-less).  
If a position has a location but NO relations → "No Connections".

### Panels (Unovis `GraphPanelConfig`)

- One panel per **location** (child level) for placed positions.
- One panel for **"Unassigned"**.
- One panel for **"No Connections"**.
- Panels reference the node IDs they contain.

---

## 3. Layout Strategy

### Why Parallel Layout

`GraphLayoutType.Parallel` in Unovis:

- Organizes nodes into **columns** (groups) and **sub-columns** (sub-groups).
- Panels are drawn automatically around sub-groups.
- **Panels are moveable** — the user can drag them anywhere.
- Spacing is controllable via `layoutParallelGroupSpacing`, `layoutParallelNodeSpacing`, `layoutParallelSubGroupSpacing`.
- No overlap issues like ELK.

### Column Mapping

```
Column (layoutNodeGroup)      SubGroup (layoutParallelNodeSubGroup)
─────────────────────────     ────────────────────────────────────
Parent Location A             Child Location A1
                              Child Location A2
Parent Location B             Child Location B1
"No Connections"              "No Connections"
"Unassigned"                  "Unassigned"
```

Each sub-group gets a **panel** drawn around it by Unovis.

### Group Ordering

```
layoutGroupOrder = [
  ...sorted_parent_location_names,
  "No Connections",
  "Unassigned",
]
```

Special groups go to the right/end of the diagram.

---

## 4. Backend Changes (`app/api/features/diagram.py`)

### Endpoint: `GET /api/features/diagram/locations`

**Changes:**

1. **Fix `all_position_ids` double-declaration bug** (line ~199 resets the set).
2. **Fetch ALL relations first** → build `connected_position_ids` set.
3. **Classify each position** using priority rule above.
4. **Build nodes** with correct `group` / `subGroup`.
5. **Build panels** per location + two special panels.
6. **Return `panels`** array (not `sites` object — frontend already expects `panels` array).

### Response Shape

```json
{
  "status": "success",
  "nodes": [
    {
      "id": "uuid",
      "group": "Building A",
      "subGroup": "Floor 1",
      "label": "[Pump] POS-001 (TAG-123)",
      "shape": "Square",
      "icon": "&#xf0ac;"
    }
  ],
  "links": [{ "source": "uuid-a", "target": "uuid-b" }],
  "panels": [
    {
      "nodes": ["uuid-1", "uuid-2"],
      "label": "Floor 1",
      "borderWidth": 4,
      "padding": 15,
      "dashedOutline": false
    },
    {
      "nodes": ["uuid-x"],
      "label": "No Connections",
      "borderWidth": 2,
      "padding": 15,
      "dashedOutline": true
    },
    {
      "nodes": ["uuid-y"],
      "label": "Unassigned",
      "borderWidth": 2,
      "padding": 15,
      "dashedOutline": true
    }
  ]
}
```

---

## 5. Frontend Changes

### `app/pages/diagram.vue`

**Changes:**

1. Replace `GraphLayoutType.Elk` with `GraphLayoutType.Parallel`.
2. Remove `layoutElkNodeGroups`.
3. Add `layoutNodeGroup`: `(n) => n.group`
4. Add `layoutParallelNodeSubGroup`: `(n) => n.subGroup`
5. Add `layoutParallelNodesPerColumn`: `6` (positions per column before wrapping)
6. Add `layoutParallelSubGroupsPerRow`: `2` (sub-groups per row in a column)
7. Add `layoutParallelGroupSpacing`: `150`
8. Add `layoutParallelNodeSpacing`: `[20, 20]`
9. Add `layoutParallelSubGroupSpacing`: `40`
10. Add `layoutGroupOrder` from backend response (or compute locally).
11. Add node color coding:
    - Normal (placed + connected): Unovis default
    - "No Connections": amber/orange fill
    - "Unassigned": grey fill
12. Add `nodeDisabled` for "No Connections" nodes.
13. Add link arrows (`linkArrow: true`).
14. Add `linkFlow` for connected links (visual traffic particles).
15. Add `zoomScaleExtent: [0.1, 2]` for better zoom range.

### `app/composables/usePositionDiagram.ts`

**Changes:**

1. Update `DiagramNodeDatum` to include `nodeType?: 'placed' | 'no-connections' | 'unassigned'`.
2. Pass through `nodeType` from backend response.

---

## 6. Tests (`tests/api/test_diagram_20260420.py`)

### New test cases to add:

| Test                                                             | Description                                                                               |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `test_unassigned_group_exists_when_positions_lack_location`      | If any position has no location, an "Unassigned" node/panel must exist                    |
| `test_no_connections_group_exists_when_positions_lack_relations` | If any position has a location but no relations, a "No Connections" node/panel must exist |
| `test_group_order_places_special_groups_last`                    | Ensures "Unassigned" and "No Connections" are at end of group ordering                    |
| `test_panels_nodes_are_non_empty`                                | Every panel in the response has at least one node                                         |
| `test_nodes_without_location_go_to_unassigned`                   | Cross-check that node.group == "Unassigned" for locationless positions                    |
| `test_all_connected_positions_in_location_groups`                | Positions with location + relations are NOT in special groups                             |

---

## 7. Implementation Checklist

### Backend

- [x] Read and understand existing `/diagram/locations` endpoint
- [x] Fix `all_position_ids` double-declaration bug
- [x] Fetch relations BEFORE classifying positions
- [x] Implement 3-tier classification logic
- [x] Build `nodes[]` with correct group/subGroup
- [x] Build `panels[]` for each location + special groups
- [x] Remove old `sites` dict (not needed by frontend)
- [x] Verify response matches frontend `DiagramNodeDatum` type
- [x] Return `groupOrder[]` for frontend column ordering

### Frontend

- [x] Switch `diagram.vue` to `GraphLayoutType.Parallel`
- [x] Wire `layoutNodeGroup` and `layoutParallelNodeSubGroup`
- [x] Configure spacing parameters
- [x] Add `layoutGroupOrder`
- [x] Add node color coding for special groups
- [x] Add link arrows
- [ ] Test in browser with real data

### Composable

- [x] Add `nodeType` to `DiagramNodeDatum`
- [x] Add `groupOrder` to `DiagramOverview`
- [x] Pass `nodeType` and `groupOrder` through in `loadOverview()`

### Tests

- [x] Run existing tests — confirmed all pass after backend fix
- [x] Add new test cases for "Unassigned" group
- [x] Add new test cases for "No Connections" group
- [x] Add test for panels referencing valid node IDs
- [x] 24/24 tests passing

---

## 8. Open Questions / Decisions

| #   | Question                                         | Decision                                                                |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------- |
| 1   | What if a location has no parent?                | Use the location itself as both group AND subGroup                      |
| 2   | Priority: no location + no connections?          | → "Unassigned" (location is primary concern)                            |
| 3   | Should "No Connections" nodes be `nodeDisabled`? | YES — grey them out visually                                            |
| 4   | Max nodes per column before wrapping?            | 6 (configurable)                                                        |
| 5   | Which layout column order?                       | Alphabetical parent locations, then "No Connections", then "Unassigned" |

---

## 9. Reference

- Unovis Graph Docs: https://unovis.dev/docs/networks-and-flows/Graph
- Parallel Layout anatomy: https://unovis.dev/assets/images/graph-layout-parallel-c93f7743b0b5685be1b678687a121605.svg
- Backend endpoint: `GET /api/features/diagram/locations`
- Frontend page: `frontend/app/pages/diagram.vue`
- Composable: `frontend/app/composables/usePositionDiagram.ts`
- Tests: `backend/tests/api/test_diagram_20260420.py`
