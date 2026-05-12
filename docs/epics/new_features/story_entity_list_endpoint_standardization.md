# Story: Entity List Endpoint Standardization with Smart Field Filtering

**Status:** Done
**Epic:** New Features
**Priority:** P1
**Date:** 2026-04-23

## Story

As a system architect, I want to standardize the entity list endpoints by removing the redundant `/list-view` endpoint and consolidating its functionality into `/list` with smart field filtering, so that we reduce API surface area, improve payload efficiency, and maintain conditional logic support.

## Problem Summary

The system had two nearly identical endpoints for listing entity records:

- `/api/entity/{entity}/list` - returned raw record data
- `/api/entity/{entity}/list-view` - returned enriched data with link titles and all fields

This created:
- Code duplication between endpoints
- Confusion about which endpoint to use
- Larger payloads than necessary (all fields always returned)
- No field-level filtering based on `in_list_view` metadata

The frontend used both endpoints inconsistently across components.

## Scope

This story covers:

**Backend:**
- `backend/app/api/entries/entity_list.py` - merge endpoints, add smart filtering
- Entity metadata JSON files - ensure workflow_state has `in_list_view: true`

**Frontend:**
- `frontend/app/composables/useEntityApi.ts` - remove getEntityListView, update getEntityList
- `frontend/app/pages/[entity]/index.vue` - use unified endpoint
- `frontend/app/components/entity/RelatedDataGrid.vue` - use unified endpoint, add workflow_state styling
- `frontend/app/components/entity/HeaderDetailRelatedTable.vue` - use unified endpoint, add workflow_state styling
- `frontend/app/components/entity/ChildDataGrid.vue` - use unified endpoint, add workflow_state styling
- `frontend/e2e/app-smoke.spec.ts` - update test patterns

## Implementation

### Backend Changes

1. **Removed** `get_entity_list_view` endpoint entirely from `entity_list.py`

2. **Updated** `get_entity_list` endpoint with new query parameters:
   - `enrich_links: bool = Query(True)` - whether to fetch and inject link field display names
   - `fields: str = Query("smart", pattern="^(smart|all)$")` - field filtering mode

3. **Added** helper functions to `entity_list.py`:
   - `_extract_referenced_fields(meta)` - parses show_when, editable_when, display_depends_on, mandatory_depends_on, list_view_depends_on to find field dependencies
   - `_get_fields_to_return(meta, mode, selectable_columns)` - determines which fields to return based on mode
   - `_record_to_dict_filtered(record, fields)` - converts record to dict with field filtering

4. **Smart filtering logic** (mode="smart"):
   - Includes fields where `in_list_view=true`
   - Includes fields where `required=true`
   - Includes fields referenced in conditional logic (show_when, editable_when, etc.)
   - Always includes system fields (id, created_at, updated_at)

5. **Updated entity metadata** to add `in_list_view: true` to workflow_state:
   - `work_order_activity.json`
   - `work_order_labor.json`
   - `work_order_equipment_assignment.json`

### Frontend Changes

1. **Updated** `useEntityApi.ts`:
   - Removed `getEntityListView` function
   - Updated `getEntityList` to accept optional `enrichLinks` and `fields` parameters
   - Moved link title caching logic into `getEntityList`
   - Default behavior: `enrichLinks=true, fields="smart"` (equivalent to old list-view)

2. **Updated** all consuming components to use `getEntityList`:
   - `pages/[entity]/index.vue`
   - `components/entity/RelatedDataGrid.vue`
   - `components/entity/HeaderDetailRelatedTable.vue`

3. **Enhanced** child grid components:
   - Changed field filter from `!f.hidden` to `f.in_list_view || f.required` to display required fields even if hidden
   - Renamed `workflow_state` column header to "Status"
   - Sorted `workflow_state` column to always appear as the last column
   - Applied to: RelatedDataGrid, HeaderDetailRelatedTable, ChildDataGrid

4. **Updated** E2E test to remove list-view pattern from regex

## Acceptance Criteria

- [x] `/api/entity/{entity}/list-view` endpoint removed
- [x] `/api/entity/{entity}/list` accepts `enrich_links` and `fields` query parameters
- [x] Smart filtering includes `in_list_view=true`, `required=true`, and conditionally referenced fields
- [x] All mode returns all table columns for programmatic access
- [x] Frontend `getEntityListView` function removed
- [x] Frontend `getEntityList` updated with new parameters
- [x] All frontend components use unified `getEntityList` endpoint
- [x] Child grids display workflow_state with "Status" label and as last column
- [x] E2E tests updated to only match `/list` endpoint
- [x] No references to deprecation or backward compatibility

## Validation Notes

**Backend validation:**
- Smart filtering correctly identifies fields with `in_list_view=true`
- Smart filtering includes fields referenced in show_when conditions
- Link enrichment only occurs when `enrich_links=true`
- Required fields included in smart mode (user-added enhancement)

**Frontend validation:**
- List pages load and display data correctly
- Child grids display workflow_state column
- workflow_state column labeled "Status" and positioned last
- Link titles cached correctly from unified endpoint

**Entity metadata validation:**
- workflow_state has `in_list_view: true` in work management child entities
- Purchase Request Line already had correct configuration

## API Specification

### Endpoint

```
GET /api/entity/{entity}/list
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number (1-indexed) |
| `page_size` | int | 20 | Number of records per page (max 100) |
| `sort_field` | string | null | Field to sort by |
| `sort_order` | string | desc | Sort direction (asc or desc) |
| `filter_field` | string | null | Field to filter on |
| `filter_value` | string | null | Filter value |
| `enrich_links` | bool | true | Whether to fetch and inject link field display names |
| `fields` | string | smart | Field mode - "smart" or "all" |

### Response

```json
{
  "status": "success",
  "data": [
    {
      "id": "...",
      "field1": "...",
      "field2": "...",
      "_link_titles": {  // only if enrich_links=true
        "link_field": "Display Name"
      }
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

## Benefits

1. **Reduced API surface** - Single endpoint instead of two
2. **Smaller payloads** - Smart filtering only returns necessary fields
3. **Consistent behavior** - All components use the same endpoint
4. **Conditional logic preserved** - Fields referenced in conditions always included
5. **Better UX** - workflow_state displayed as "Status" in child grids
