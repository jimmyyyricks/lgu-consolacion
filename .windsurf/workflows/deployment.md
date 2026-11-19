---
description: Deploy the LGU website using the GitHub Actions release workflow
---

# Deployment Workflow

Production builds and deployments are handled by `.github/workflows/ci.yml`.
Builds run in GitHub Actions; the deployment job remains skipped until the
`production` environment is configured and the repository Actions variable
`DEPLOY_ENABLED` is set to `true`.

Follow [`docs/deployment.md`](../../docs/deployment.md) for the one-time server
setup, required GitHub variables and secrets, and deployment behavior.
