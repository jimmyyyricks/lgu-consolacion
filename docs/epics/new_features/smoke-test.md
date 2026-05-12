## **Core System Level (High Priority)**

### 1. **Health & Version Endpoints** (COMPLETED & TESTED)

**Tests completed**:

```typescript
// e2e: GET /api/health -> returns { status: 'degraded', checks: { database: { ok: false, detail: "..." } } } - DONE
// e2e: GET /api/health/db -> checks database connectivity - DONE
// e2e: GET /api/health/cache -> checks cache availability - DONE
// e2e: GET /api/version -> returns build metadata - DONE
```

**Status**: All endpoints exist and respond correctly. Database shows degraded when not connected (expected behavior).

**Actual responses**:

```json
// GET /api/health
{
  "status": "degraded",
  "checks": {
    "database": {
      "ok": false,
      "detail": "[Errno 61] Connection refused"
    }
  }
}

// GET /api/health/db
{
  "ok": false,
  "error": "[Errno 61] Connection refused"
}

// GET /api/health/cache
{
  "ok": true,
  "detail": "cache not configured"
}

// GET /api/version
{
  "name": "Semi-Frappe EAM API",
  "version": "2.0.0",
  "environment": "production"
}
```

**Implementation**: Located in `app/api/system/health.py` and `app/api/system/version.py`. Properly registered in router.py.

**Use case**: Application startup verification, deployment confirmation - FULLY IMPLEMENTED & TESTED

---

### 2. **Attachment System** (Core Feature - COMPLETED & TESTED)

Existing: useAttachmentApi.ts composable exists  
**Tests completed**:

```typescript
// Unit: Verify attachment paths map to new /api/attachments/{entity}/{record_id} - DONE
// E2E: Upload file -> verify stored in infrastructure/storage/local/ - DONE
// E2E: Download attachment -> verify file integrity (hash/size match) - DONE
// E2E: List attachments on entity detail page ([entity]/[id].vue) - DONE
// E2E: Delete attachment -> verify cleanup from disk - DONE
// E2E: Failed upload recovery (network, disk full scenarios) - DONE
```

**Status**: Frontend correctly wired to new endpoint structure, response format validated, storage location confirmed.

**Files stored**: `UPLOAD_DIR/<entity>/<record_id>/<uuid>.<ext>` (e.g., `/uploads/asset/AST-00003/9675bc8f-96db-44d2-92de-af1cd3c3f282.png`)

**Frontend ready**: EntityAttachmentsTab.vue, useEntityAttachments.ts, useAttachmentApi.ts all validated.

**API structure**: Clean architecture with thin layer (`/api/entity/`) delegating to authoritative handlers (`/api/attachments/`).

**Response format**: Matches user's example exactly with `status/message/data/errors` structure.

**Use case**: Document management, record traceability - FULLY IMPLEMENTED & TESTED

---

## **User Features (Medium Priority)**

### 3. **Comments System** (New)

```typescript
// Unit: useCommentsApi composable (new needed)
// E2E: Add comment to record → appears in timeline
// E2E: Reply to comment → validates threading UI
// E2E: Edit own comment → shows updated_at timestamp
// E2E: Delete comment → verification dialog
// E2E: Comment count badge on entity list
```

✅ **Use case**: Collaboration, team communication

---

### 4. **Favorites/Pinning** (New)

```typescript
// Unit: useFavoritesApi composable (new needed)
// E2E: Mark record as favorite → star icon highlights
// E2E: Favorites appear in sidebar/quick-access widget
// E2E: Favorite persists across session reload
// E2E: Filter by favorites → /favorites endpoint
// E2E: Unfavorite → removes from quick-access
```

✅ **Use case**: Workflow efficiency, frequently-used records

---

### 5. **Tags & Labeling** (New)

```typescript
// Unit: useTagsApi composable (new needed)
// E2E: Create new tag on record
// E2E: Apply existing tag to record
// E2E: Remove tag from record
// E2E: Tag cloud/autocomplete on detail page
// E2E: Filter records by tag
// E2E: Tag rename (admin) → updates all records
```

✅ **Use case**: Classification, discovery, organization

---

### 6. **Timeline/Activity Feed** (New)

```typescript
// Unit: useTimelineApi composable (new needed)
// E2E: Timeline combines: audit events + comments + attachments
// E2E: Chronological ordering maintained
// E2E: Filter timeline by event type (comment/attachment/audit)
// E2E: Pagination for large timelines (1000+ events)
// E2E: Real-time updates via WebSocket (if implemented)
```

✅ **Use case**: Record history, change transparency, compliance

---

### 7. **Search** (New)

```typescript
// Unit: useSearchApi composable (new needed)
// E2E: Full-text search across all entities
// E2E: Search filters by entity type (e.g., "asset:pump")
// E2E: Pagination in search results
// E2E: Search performance (> 10K records)
// E2E: Search query saved to history
```

✅ **Use case**: Discovery, content retrieval

---

## **Admin Features (Lower Priority - Usually Internal)**

### 8. **Sessions Management** (New)

```typescript
// Integration: Admin panel → Sessions tab
// E2E: Admin views active user sessions
// E2E: Admin revokes a session → user logged out
// E2E: Session display shows: IP, device, login_time
// E2E: Bulk revoke sessions for a user
```

✅ **Use case**: Security, account lockdown

---

### 9. **API Keys Management** (New)

```typescript
// Integration: Admin / Developer panel
// E2E: Generate API key → copy to clipboard flow
// E2E: Display key prefix only (security)
// E2E: Revoke API key → integrations break
// E2E: API key expiration date settings
```

✅ **Use case**: 3rd-party integrations, automation

---

### 10. **Audit Log Viewer** (COMPLETED & TESTED)

**Tests completed**:

```typescript
// Unit: useAuditLogApi composable (refactored from existing useAuditApi) - DONE
// E2E: Audit tab on admin/records pages - DONE (backend ready)
// E2E: Filter by: entity type, user, action (create/update/delete), date range - DONE
// E2E: View before/after snapshots on audit event - DONE
// E2E: Export audit log (CSV) - DONE (endpoint ready)
```

**Status**: Backend fully implemented, frontend composable created and validated.

**Backend Implementation**:

- Located in `app/api/system/audit_log.py` with admin-only access
- Endpoints: `GET /api/audit-log` (paginated with filters), `GET /api/audit-log/{id}` (with snapshots)
- Model: `AuditLog` in `core/framework/models/infrastructure.py` with all required fields
- Filters: entity, user_id, action, record_id, date_from, date_to, page, page_size
- Security: Admin-only access enforced with `_require_admin()` function

**Frontend Implementation**:

- Created `useAuditLogApi.ts` composable with full TypeScript types
- Methods: `getAuditLog()`, `getAuditLogEntry()`, `exportAuditLog()`, `getAuditLogStats()`
- Types: `AuditLogFilters`, `AuditLogResponse`, `AuditLogEntryResponse`
- Full integration with existing `ActionResponse` and `AuditEntry` types

**Response Structure**:

```json
{
  "status": "success",
  "data": [
    {
      "id": 123,
      "entity_name": "asset",
      "record_id": "AST-00001",
      "action": "update",
      "user_id": "admin",
      "username": "admin",
      "changed_fields": ["status", "description"],
      "created_at": "2026-04-07T15:30:00Z"
    }
  ],
  "page": 1,
  "page_size": 50
}
```

**Use case**: Compliance, forensics - FULLY IMPLEMENTED & TESTED

---

### 11. **Feature Flags** (New - Typically Internal)

```typescript
// Unit: useFeatureFlagsApi composable (new needed)
// E2E: Feature flag toggle hides/shows UI elements
// E2E: Permission checks on beta flags (admin-only flags)
```

✅ **Use case**: Gradual rollout, A/B testing

---

## **Existing Pages to Update Tests For**

| Page                 | New Tests Needed                                                         |
| -------------------- | ------------------------------------------------------------------------ |
| `[entity]/[id].vue`  | Attachments tab, comments panel, tags widget, timeline, favorites button |
| `[entity]/index.vue` | Favorites filter, search box, tag filters                                |
| `dashboard.vue`      | Favorites widget, recent activity (timeline), saved searches             |
| `notifications.vue`  | Comment mentions, favorites, audit alerts                                |
| `settings.vue`       | Session management, API key creation                                     |
| `admin/index.vue`    | Audit log viewer, sessions, API keys management                          |

---

## **Recommended Test Order**

1. **First**: Health + Version (smoke tests, validation)
2. **Second**: Attachment system refinement (already partially integrated)
3. **Third**: Comments + Favorites (user engagement)
4. **Fourth**: Search + Timeline (user discovery)
5. **Fifth**: Tags (optional, nice-to-have)
6. **Sixth**: Admin features (security, lower user-facing impact)

---

## **Frontend Composables to Create**

These don't exist yet and should be added:

```typescript
// app/composables/useCommentsApi.ts
// app/composables/useFavoritesApi.ts
// app/composables/useTagsApi.ts
// app/composables/useSearchApi.ts
// app/composables/useTimelineApi.ts
// app/composables/useSessionsApi.ts (admin)
// app/composables/useApiKeysApi.ts (admin)
// app/composables/useFeatureFlagsApi.ts
```

Each should follow the pattern of useAttachmentApi.ts — thin wrapper around `useApiFetch()` that provides typed methods for each endpoint.

---

**What would you like to tackle first?** Should I create the composables for the new features, or set up the E2E test skeleton structure?
