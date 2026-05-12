# Role-Based Dashboard Orchestration

This epic folder documents the orchestrator-based dashboard implementation.

## Current Structure

- `EPIC.md`: initiative-level scope, contract, and story map
- `story_1_architecture.md` to `story_11_testing.md`: implementation stories aligned to the orchestrator flow
- `tests/test_role_based_dashboard.py`: requests-based integration checks for the orchestrator contract

## Implementation Summary

The backend now returns dashboard selectors plus the selected dashboard payload from one authenticated endpoint:

- `allowed_dashboards`: button metadata for the current user
- `selected_dashboard`: currently active dashboard payload with widgets

The frontend dashboard page renders those buttons, auto-loads the first allowed dashboard, and re-queries the backend on every dashboard switch.

## Key Backend Files

- `backend/app/application/services/role_based_dashboard_orchestrator.py`
- `backend/app/application/services/role_based_dashboard_service.py`
- `backend/app/api/routes/operational_dashboard.py`

## Key Frontend Files

- `frontend/app/composables/useDashboard.ts`
- `frontend/app/pages/dashboard.vue`

## Verification Focus

The remaining validation work is execution of the updated automated checks against a running backend and adding richer frontend interaction coverage for dashboard switching.
