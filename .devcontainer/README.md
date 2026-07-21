# Dev Container

Local development environment for the Area Todo monorepo.

## Includes

- Node.js 22 + pnpm 8
- Python 3 + uv
- Postgres 16 (via Docker Compose)

## Getting started

1. Open the repo in VS Code or Cursor.
2. Run **Dev Containers: Reopen in Container**.
3. Wait for `post-create.sh` to install dependencies and run migrations.
4. From the repo root, run:

```bash
pnpm dev
```

## Services

| Service  | URL                     |
|----------|-------------------------|
| Web      | http://localhost:3000   |
| API      | http://localhost:8000   |
| Postgres | localhost:5432          |

The API reads `DATABASE_URL` from the devcontainer environment (`db` host). A local `apps/api/.env` is created on first setup if missing.

## Windows / WSL notes

If the workspace is bind-mounted from a Windows drive (9p), Next.js Turbopack can fail with `Operation not permitted` when writing under `apps/web/.next`. The compose file mounts a Docker volume over that path; `post-create.sh` also falls back to a `/tmp` symlink when needed.

After changing `docker-compose.yml`, rebuild the container (**Dev Containers: Rebuild Container**) so the `web-next` volume is applied.
