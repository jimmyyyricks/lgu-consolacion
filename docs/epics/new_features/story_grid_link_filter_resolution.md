# Story: Grid Link Filter Resolution Across Form Surfaces

**Status:** Done
**Epic:** New Features
**Priority:** P1
**Date:** 2026-04-23

## Story

As a user editing child rows in form pages and header-detail modals, I need link filters that depend on sibling grid fields (for example `work_order_parts.item`) to resolve correctly so dependent link dropdowns (for example `inventory`) only show valid options.

## Problem Summary

In child/related NuGrid editors, link filters with dotted sibling references were intermittently unresolved in modal-driven flows. The selected source link field value was committed, but the editor-level row snapshot used by filter resolution could be stale, causing requests to be sent without filters.

Example:

- Source field: `work_order_parts`
- Dependent field: `inventory`
- Filter rule: `{"item": "work_order_parts.item"}`

Observed failure:

- `inventory/options` was called without `filters`.

## Scope

This story covers these form surfaces:

- `frontend/app/pages/[entity]/[id].vue`
- `frontend/app/components/entity/HeaderDetailModal.vue`

Both surfaces render child/related data entry through shared grid components (`EntityChildDataGrid` and `EntityRelatedDataGrid`), so the fix is centralized and reused.

## Implementation

1. Added shared resolver `frontend/app/composables/useGridLinkFilterResolver.ts`.
2. Implemented dotted link-filter resolution with fallback remote lookup via `getFetchFromFields`.
3. Added live-row reconciliation by row id (`gridRows`) to avoid stale editor snapshot issues.
4. Wired resolver into:
   - `frontend/app/components/entity/ChildDataGrid.vue`
   - `frontend/app/components/entity/RelatedDataGrid.vue`
5. Ensured link editors pass field context and filter metadata, and request options with resolved filters.
6. Added diagnostic console logs for:
   - editor open
   - filter resolution
   - remote filter fetch
   - options request and response
   - editor selection and cell change events

## Acceptance Criteria

- [x] Dotted sibling filter references resolve in child grid editors.
- [x] Dependent link options requests include resolved `filters` payload when source is selected.
- [x] Behavior works in standard form page (`[entity]/[id]`) child/related grid paths.
- [x] Behavior works in header-detail modal child grid path.
- [x] Child and related grid components compile with no new diagnostics.

## Validation Notes

Static/code-path validation completed:

- `[entity]/[id].vue` uses `EntityChildDataGrid` and `EntityRelatedDataGrid`.
- `HeaderDetailModal.vue` uses `EntityChildDataGrid`.
- Both grids share the same resolver and live-row fallback logic.

Runtime validation completed during debugging flow:

- `work_order_parts` selection captured.
- `inventory` filter resolution now reads from live row state.
- dependent options call includes filter payload (issue resolved).

## Risks / Follow-up

- Debug logs are currently verbose for troubleshooting. If desired, reduce log level or guard behind an environment flag in a cleanup story.
