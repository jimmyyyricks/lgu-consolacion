# Backend

The backend is a Python FastAPI application with SQLAlchemy persistence.

## Relevant structure

- `backend/app/api/` — HTTP route modules and request/response schemas.
- `backend/app/application/` — application services.
- `backend/app/domain/` — domain protocols and contracts.
- `backend/app/infrastructure/database/repositories/` — database repositories.
- `backend/app/core/framework/models/` — shared framework models, including public content.

`backend/app/main.py` mounts the API router under `/api`. The public-content router is in `backend/app/api/content.py`; persistence is handled by `PublicContentRepository`.

## Content endpoints

- `GET /api/content` — list published records.
- `GET /api/content/archive` — filtered archive page with count and publication years.
- `GET /api/content/{slug}` — published record detail.
- `GET /api/content/admin/all` — editor-only record list.
- `POST /api/content` — create a record.
- `PATCH /api/content/{slug}` — update a record.

CMS write/list routes require an authenticated content editor or administrator. Frontend integration details are in [Public content logic](../business-logic/public-content.md).
