# EAM System

A metadata-driven **Enterprise Asset Management** system built with **FastAPI + SQLAlchemy** (backend) and **Nuxt 4 + Nuxt UI** (frontend), following Clean Architecture principles.

## Features

- **Metadata-driven** — Entity definitions (`.json`) drive models, API, forms, and validation automatically.
- **Clean Architecture** — Domain → Application → Infrastructure → API layers with protocol-based DI.
- **Modular** — Entities grouped into domain modules (`core_eam`, `asset_management`, `maintenance_mgmt`, `work_mgmt`, `purchasing_stores`).
- **Generic CRUD API** — Single router set (`/api/entity/{name}`) handles all entities.
- **Workflow Engine** — State-machine workflows with role-based transition control.
- **RBAC** — Role-based entity-level permissions (read/create/update/delete/select/export/import).
- **Forge CLI** — Code generation, migrations, and system management from the terminal.
- **One-Command Install** — `./install.sh` prompts for credentials upfront, generates unique DB credentials, installs all dependencies, and creates the first administrator—ready to log in immediately.

## Prerequisites

| Dependency | Version | Notes                   |
| ---------- | ------- | ----------------------- |
| Python     | ≥ 3.10  |                         |
| Node.js    | ≥ 20    | via nvm recommended     |
| pnpm       | ≥ 10    | `npm i -g pnpm`         |
| PostgreSQL | ≥ 14    | Required for production |

## Quick Start

### 1. Clone and run the installer

```bash
git clone <repo-url> eam-system && cd eam-system
./install.sh
```

The installer will:

- Prompt for PostgreSQL superuser credentials (host, port, username, password)
- Prompt for administrator account details (username, email, full name, password)
- Generate unique database credentials and `.env` file
- Install backend and frontend dependencies
- Create the PostgreSQL role and database
- Create all database tables and seed core reference data
- Create the administrator account

**PostgreSQL prompt guidance:**

- Enter the PostgreSQL superuser credentials that are allowed to create roles and databases.
- On many servers this means: host `localhost`, port `5432`, username `postgres`, and the actual password for that PostgreSQL user.
- Do not just press Enter for everything unless you know the server is configured for passwordless peer or trust authentication.
- Leaving the password blank tells the installer to try OS peer auth via `postgresql:///postgres`, which usually works only on some local development machines or servers where the current Unix user is already mapped to a PostgreSQL superuser.
- If you do not know these credentials, ask the server or database administrator before continuing.

**Note:** Both credential prompts happen upfront so the install runs unattended.

### 2. Start the app

```bash
./run.sh
```

The browser will open to the login page. Log in with the administrator credentials you entered during install.

### 3. (Optional) Manual admin creation

If you prefer to create the administrator account in the browser after install:

```bash
./install.sh --skip-admin
```

Then access `/setup` directly to create the first admin. Note: `./run.sh` does **not** auto-redirect to `/setup` anymore — you must navigate to it manually.

### Non-interactive install (CI/automation)

To bypass the interactive prompts and provide credentials via command-line flags:

```bash
./install.sh \
	--admin-username admin \
	--admin-email admin@example.com \
	--admin-full-name "System Administrator" \
	--admin-password "MySecurePassword123"
```

Pre-supply the PostgreSQL bootstrap URL to skip that prompt:

```bash
DATABASE_BOOTSTRAP_URL=postgresql://postgres:password@localhost/postgres ./install.sh
```

### Production build

```bash
cd frontend
pnpm build
# Start the production server
node .output/server/index.mjs
```

## Data Seeding

Seed scripts live in `backend/scripts/seeds/`. Run from the `backend/` directory:

```bash
# 1. Seed masterfiles from Excel
python scripts/seeds/seed_masterfiles_workbooks.py

# 2. Reset workflow catalog
python scripts/seeds/reset_workflow_catalog.py

# 3. Seed workflows from Excel
python scripts/seeds/seed_workflows_from_excel.py

# 4. Seed roles & permissions
python scripts/seeds/seed_roles_permissions.py
```

See [docs/SEEDING_GUIDE.md](docs/SEEDING_GUIDE.md) for the full seeding order.

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Backend Coding Standards](docs/backend/CODING_STANDARDS.md)
- [Forge CLI Guide](backend/app/README.md)
- [Testing Guide](docs/TESTING_GUIDE.md)
- [Seeding Guide](docs/SEEDING_GUIDE.md)
- [Database Credentials](docs/DATABASE_CREDENTIALS.md)

## Environment Variables

The `./install.sh` script automatically generates `backend/.env` with unique database credentials each installation. You typically don't need to manually configure it.

For advanced scenarios, see [`.env.example`](.env.example) for all available variables. The only required variable is `DATABASE_URL`, which is auto-generated by the installer.

## Tech Stack

**Backend:** Python 3.10+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, Socket.IO, Jinja2, aiosmtplib

**Frontend:** Nuxt 4, Vue 3, Nuxt UI 4, Pinia, Tailwind CSS 4, VueUse, Cytoscape.js, Socket.IO Client
