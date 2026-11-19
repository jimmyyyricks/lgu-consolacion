# CI/CD and Server Deployment

The production build runs in GitHub Actions, not on the 1 vCPU / 2 GB server. The workflow builds Nuxt's Node server output, packages the FastAPI source, runs checks, and stores a `lgu-release` artifact for 14 days. The server runs the built Nuxt output and Python backend; it does not run `pnpm build`.

On pushes to `main`, CI runs backend tests, frontend type checking and unit tests, and the production build. The SSH deploy job is skipped until the repository Actions variable `DEPLOY_ENABLED` is set to `true`. No server credentials are needed to build or download the artifact.

## One-time server setup

Before enabling automatic deployment, prepare an x86_64 Linux server with Node.js 22, Python 3.10+, `python3-venv`, `curl`, `tar`, and systemd. This matches the Linux x86_64 GitHub runner used to build Nuxt's native image dependencies; check the server with `uname -m` before enabling deploy. PostgreSQL may run on this server or elsewhere. Create an absolute deployment path such as `/srv/lgu-consolacion`, owned by the SSH deploy user. The deploy script writes versioned releases under `releases/`, the current symlink at `current`, and persistent files under `shared/`; it retains old releases for manual rollback.

Create two systemd services and configure them to follow the `current` symlink:

- Frontend: run `node` against `current/frontend/.output/server/index.mjs`, listening on `127.0.0.1:3010`, with `NODE_ENV=production` and `NUXT_PUBLIC_API_URL=/api`.
- Backend: use `shared/backend-venv/bin/uvicorn app.main:app` from `current/backend`, listening on `127.0.0.1:8010`. The deploy script creates this virtual environment and installs backend requirements when they change.

Configure the reverse proxy to serve the frontend and route `/api` to the backend. Give the backend service an environment file outside release directories; it must contain the production database URL and a strong `SECRET_KEY`. Set `UPLOAD_DIR` to the persistent path `shared/uploads` so uploaded files survive deployments. Do not commit production environment files or run schema migrations automatically; review and apply migrations separately when needed.

The deploy user needs write access to the deployment path and passwordless `sudo systemctl restart` access for the two service units. Those units must use the same deployment path configured in GitHub.

## GitHub configuration

In repository Settings → Environments, create `production`. Add these environment variables:

- `DEPLOY_HOST`, `DEPLOY_PORT` (normally `22`), `DEPLOY_USER`, and `DEPLOY_PATH`
- `DEPLOY_FRONTEND_SERVICE` and `DEPLOY_BACKEND_SERVICE`: exact systemd unit names
- Optionally, `FRONTEND_HEALTH_URL` and `BACKEND_HEALTH_URL`; defaults are `http://127.0.0.1:3010/` and `http://127.0.0.1:8010/health`

In Settings → Secrets and variables → Actions → Variables, set the repository variable `DEPLOY_ENABLED` to `true` only after the server setup is complete.

Add these environment secrets:

- `DEPLOY_SSH_PRIVATE_KEY`: private key for a dedicated deploy account whose public key is installed on the server
- `DEPLOY_KNOWN_HOSTS`: verified SSH host-key line(s) for the host and port

The deployment switches to the new release, restarts both services, and checks their health. If checks fail and a previous release exists, it restores the previous symlink and restarts the services. The first push only builds and publishes the artifact until the production environment variables and secrets are configured. After setup, deploy either on a later push to `main` or manually run the workflow on `main` with its `deploy` input enabled.

The separate scheduled database-backup workflow is still legacy EAM configuration and is not part of this deployment pipeline; review its host and database settings before relying on it.

Frontend lint is not currently a CI gate because the repository-wide `pnpm lint` command reports existing style errors. Add it as a required check after those are resolved.
