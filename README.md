# FastAPI Nuxt Starter

A metadata-driven modular application framework built with **FastAPI** (Python) and **Nuxt 4** (Vue 3). Inspired by Frappe/ERPNext architecture — add entities, business logic, hooks, workflows, emails, and more through a modular plugin system.

## Architecture Overview

```
┌──────────────────────────────────────────┐
│  Frontend — Nuxt 4 + Nuxt UI             │
│  • Dynamic entity pages (list/detail)    │
│  • Metadata-driven forms and grids       │
│  • Composable-based API layer            │
│  • JWT auth with token refresh           │
├──────────────────────────────────────────┤
│  Backend — FastAPI (Clean Architecture)  │
│  • API Layer        — FastAPI routes     │
│  • Application      — Use-case services  │
│  • Infrastructure   — DB, email, storage │
│  • Core             — Config, framework  │
│  • Domain           — Protocols, errors  │
│  • Modules          — Feature units      │
└──────────────────────────────────────────┘
```

## Key Features

- **Metadata-Driven Entities** — Define entities via JSON; CRUD, forms, and lists auto-generate
- **Hook System** — Decorator-based lifecycle hooks (`@before_save`, `@after_save`, `@workflow`)
- **Workflow Engine** — State machine with transitions, actions, and progress tracking
- **Role-Based Access Control** — Granular entity-level permissions
- **Email Notifications** — Subscription-based email alerts for entity events
- **Print Templates** — Jinja2-based print/PDF generation per entity
- **Scheduler** — APScheduler integration for recurring jobs
- **Audit Trail** — Automatic mutation logging
- **Import/Export** — CSV-based bulk operations
- **Entity Editor** — Frappe-like model editor with schema migrations
- **Generic Endpoints** — All entities share a single CRUD kernel (`/api/entity/{name}/...`)

## Quick Start

### Prerequisites

| Dependency | Version | Notes |
|------------|---------|-------|
| Node.js    | ≥ 20    | via nvm recommended |
| pnpm       | ≥ 10    | `npm i -g pnpm` |
| Python     | ≥ 3.11  | |
| PostgreSQL | ≥ 14    | or SQLite for dev |

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env with your database URL, secret key, etc.

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8012
```

### Frontend Setup

```bash
cd frontend
pnpm install

# Configure .env
cat > .env <<'EOF'
NODE_ENV=development
NUXT_PUBLIC_API_URL=http://127.0.0.1:8012/api
NUXT_PUBLIC_WS_URL=ws://127.0.0.1:8012
EOF

# Start dev server
pnpm dev
```

Visit `http://localhost:3000` — the app redirects to setup on first run.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/               # FastAPI routes (entries, features, system)
│   │   ├── application/       # Business services, hooks, notifications
│   │   ├── core/              # Config, database, security, framework entities
│   │   ├── domain/            # Pure Python protocols and exceptions
│   │   ├── infrastructure/    # DB repos, email, storage, scheduler, cache
│   │   ├── modules/           # Domain feature units (plugins)
│   │   ├── meta/              # Metadata registry
│   │   ├── entities/          # Entity loader
│   │   └── templates/         # Email and print Jinja2 templates
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Test suite
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── components/        # Vue components
│   │   ├── composables/       # Reusable composition functions
│   │   ├── layouts/           # Layout components
│   │   ├── middleware/        # Route middleware
│   │   ├── pages/             # File-based routing
│   │   ├── plugins/           # Nuxt plugins
│   │   ├── stores/            # Pinia stores
│   │   └── types/             # TypeScript types
│   ├── nuxt.config.ts
│   └── package.json
├── run.sh
└── install.sh
```

## Forge CLI

The backend includes **Forge**, a CLI toolkit for scaffolding entities, syncing models to the database, and managing migrations. Run from `backend/` with the virtualenv active.

```
python -m app.forge <command> [options]
```

### Everyday Workflow

| Command | Description |
|---|---|
| `forge sync` | Push entity JSON → Models → DB in one shot |
| `forge sync -m "add field"` | Sync with a custom migration label |
| `forge status` | Show current DB revision |

### Entity Scaffolding

| Command | Description |
|---|---|
| `forge new-entity <name> --module <mod> --fields "n:t,n:t"` | Scaffold a new entity with fields |
| `forge add-field <entity> <field> <type>` | Add a field to an existing entity |
| `forge update-model <entity>` | Regenerate one model from its JSON |
| `forge update-model --all` | Regenerate every model (force) |
| `forge generate-types` | Generate TypeScript interfaces from entity metadata |

### Migrations

| Command | Description |
|---|---|
| `forge migrate` | Generate + apply pending migrations |
| `forge migrate --status` | Show current revision + history |
| `forge migrate --rollback [N]` | Roll back N steps (default 1) |

### Utilities

| Command | Description |
|---|---|
| `forge seed` | Run seed data |
| `forge console` | Interactive Python REPL with app context |

### Full Example

```bash
cd backend
python -m app.forge new-entity invoice --module accounting --fields "number:string,customer:link,amount:float,due_date:date"
python -m app.forge sync
```

The JSON definition drives API routing, list/detail views, form fields, workflow, and permissions. No route code is needed for standard CRUD.

## Documentation

| Layer | README |
|-------|--------|
| Backend Overview | [backend/app/README.md](backend/app/README.md) |
| API Layer | [backend/app/api/README.md](backend/app/api/README.md) |
| Application Layer | [backend/app/application/README.md](backend/app/application/README.md) |
| Core Layer | [backend/app/core/README.md](backend/app/core/README.md) |
| Domain Layer | [backend/app/domain/README.md](backend/app/domain/README.md) |
| Infrastructure | [backend/app/infrastructure/README.md](backend/app/infrastructure/README.md) |
| Modules | [backend/app/modules/README.md](backend/app/modules/README.md) |
| Frontend | [frontend/README.md](frontend/README.md) |
| Tests | [backend/tests/README_TESTS.md](backend/tests/README_TESTS.md) |

## Tech Stack

**Backend:** FastAPI, SQLAlchemy (async), Alembic, APScheduler, Jinja2, Pydantic

**Frontend:** Nuxt 4, Vue 3, Nuxt UI, Pinia, Tailwind CSS, TypeScript

**Infrastructure:** PostgreSQL, Redis (optional), SMTP, S3 (optional)
