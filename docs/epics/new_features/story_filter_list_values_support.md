# Story: Support List Values in Database Filters

## Summary
Enable database queries to accept list values for filters (e.g., `item_type IN ['Inventory Item', 'Non Inventory Item']`) instead of only single values.

## Problem
When calling `/api/entity/item/options?filters={"item_type": ["Inventory Item", "Non Inventory Item"]}`, the backend generated invalid SQL using equality operator with a list value:
```sql
WHERE item_type = ['Inventory Item', 'Non Inventory Item']  -- INVALID
```

This caused asyncpg error:
```
invalid input for query argument $1: ['Inventory Item', 'Non Inventory Item'] (expected str, got list)
```

## Root Cause
Filter building logic across the codebase used equality operator (`==`) for all filter values, not handling list values appropriately.

## Solution
Created a centralized `filter_builder.py` helper in the infrastructure layer that:
- Detects if a filter value is a list
- For lists: uses SQL `IN` operator (`field.in_([values])`)
- For single values: uses equality operator (`field == value`)

Refactored all filter building locations to use this helper:
- `document_repository.py` (Infrastructure layer)
- `entity_repository.py` (Infrastructure layer)
- `document_query.py` (Application layer)
- `entity_options.py` (API layer)

## Architecture Benefits
- **DRY**: Single source of truth for filter logic
- **SRP**: Filter building separated from query orchestration
- **Open/Closed**: Easy to extend for new filter types (ranges, null checks, etc.)
- **Consistent behavior**: All query building now handles lists uniformly

## Files Changed
- **Created**: `backend/app/infrastructure/database/query/filter_builder.py`
- **Modified**: 
  - `backend/app/infrastructure/database/repositories/document_repository.py`
  - `backend/app/infrastructure/database/repositories/entity_repository.py`
  - `backend/app/application/services/documents/document_query.py`
  - `backend/app/api/entries/entity_options.py`

## Testing
Test endpoint:
```
GET /api/entity/item/options?limit=5&filters={"item_type":["Inventory Item","Non Inventory Item"],"is_equipment":false}
```

Expected: Returns items matching either "Inventory Item" or "Non Inventory Item" types.

## Status
✅ Implemented
✅ Refactored to follow CLEAN/SOLID principles
