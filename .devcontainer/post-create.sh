#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/area-todo

# Next.js/Turbopack can hit EPERM writing .next on Windows 9p bind mounts.
# docker-compose mounts a named volume over this path; if that volume is not
# present yet (e.g. before rebuild), fall back to a Linux-native symlink.
if ! findmnt -n --target apps/web/.next >/dev/null 2>&1; then
  echo "Redirecting apps/web/.next to /tmp (Windows bind-mount workaround)..."
  rm -rf apps/web/.next
  mkdir -p /tmp/area-todo-web-next
  ln -sfn /tmp/area-todo-web-next apps/web/.next
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
