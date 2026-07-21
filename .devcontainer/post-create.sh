#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/area-todo

# Next.js/Turbopack can hit EPERM writing .next on Windows 9p bind mounts.
# docker-compose mounts a named volume over this path; if that volume is not
# present yet (e.g. before rebuild), fall back to a Linux-native symlink.
NEXT_DIR="apps/web/.next"
if ! findmnt -n --target "$NEXT_DIR" >/dev/null 2>&1; then
  echo "Redirecting $NEXT_DIR to /tmp (Windows bind-mount workaround)..."
  rm -rf "$NEXT_DIR"
  mkdir -p /tmp/area-todo-web-next
  ln -sfn /tmp/area-todo-web-next "$NEXT_DIR"
fi

# Named volumes are often created as root; ensure the app user can write.
NEXT_REAL="$(readlink -f "$NEXT_DIR" 2>/dev/null || true)"
if [ -n "${NEXT_REAL}" ] && [ -d "${NEXT_REAL}" ]; then
  if [ ! -w "${NEXT_REAL}" ]; then
    echo "Fixing ownership on ${NEXT_REAL}..."
    sudo chown -R "$(id -u):$(id -g)" "${NEXT_REAL}"
  fi
fi

echo "Installing Node dependencies..."
pnpm install

echo "Installing Python dependencies..."
cd apps/api
uv sync

if [ ! -f .env ]; then
  echo "Creating apps/api/.env from .env.example..."
  cp .env.example .env
  sed -i 's/@localhost:/@db:/' .env
fi

echo "Running database migrations..."
uv run alembic upgrade head

echo "Dev container setup complete."
echo "Run 'pnpm dev' from the repo root to start the web and API servers."
