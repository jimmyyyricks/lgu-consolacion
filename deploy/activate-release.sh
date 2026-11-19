#!/usr/bin/env bash
set -Eeuo pipefail

: "${DEPLOY_ROOT:?}"
: "${RELEASE_ID:?}"
: "${FRONTEND_SERVICE:?}"
: "${BACKEND_SERVICE:?}"
: "${FRONTEND_HEALTH_URL:?}"
: "${BACKEND_HEALTH_URL:?}"

if [[ ! "$RELEASE_ID" =~ ^[0-9a-f]{40}$ ]]; then
  echo "Invalid release ID." >&2
  exit 2
fi

archive="$DEPLOY_ROOT/incoming/$RELEASE_ID.tar.gz"
release_dir="$DEPLOY_ROOT/releases/$RELEASE_ID"
shared_dir="$DEPLOY_ROOT/shared"
venv="$shared_dir/backend-venv"

test -f "$archive"
mkdir -p "$release_dir" "$shared_dir/uploads"
tar -xzf "$archive" -C "$release_dir"
test -f "$release_dir/frontend/.output/server/index.mjs"
test -f "$release_dir/backend/app/main.py"

if [[ ! -x "$venv/bin/python" ]]; then
  python3 -m venv "$venv"
fi

if ! cmp -s "$release_dir/backend/requirements.txt" "$shared_dir/backend-requirements.txt"; then
  "$venv/bin/python" -m pip install \
    --disable-pip-version-check \
    -r "$release_dir/backend/requirements.txt"
  install -m 0644 "$release_dir/backend/requirements.txt" "$shared_dir/backend-requirements.txt"
fi

previous_release="$(readlink -f "$DEPLOY_ROOT/current" 2>/dev/null || true)"
next_link="$DEPLOY_ROOT/.current-$RELEASE_ID"
ln -sfn "$release_dir" "$next_link"
mv -Tf "$next_link" "$DEPLOY_ROOT/current"

restart_and_check() {
  sudo systemctl restart "$FRONTEND_SERVICE" "$BACKEND_SERVICE" || return 1

  for _ in {1..30}; do
    if curl -fsS "$FRONTEND_HEALTH_URL" >/dev/null 2>&1; then
      backend_health="$(curl -fsS "$BACKEND_HEALTH_URL" 2>/dev/null || true)"
      if printf '%s' "$backend_health" | grep -Eq '"connected"[[:space:]]*:[[:space:]]*true'; then
        return 0
      fi
    fi
    sleep 2
  done

  return 1
}

if ! restart_and_check; then
  echo "Release health check failed." >&2
  if [[ -n "$previous_release" ]]; then
    rollback_link="$DEPLOY_ROOT/.rollback-$RELEASE_ID"
    ln -sfn "$previous_release" "$rollback_link"
    mv -Tf "$rollback_link" "$DEPLOY_ROOT/current"
    sudo systemctl restart "$FRONTEND_SERVICE" "$BACKEND_SERVICE" || true
  fi
  exit 1
fi

echo "Activated release $RELEASE_ID."
