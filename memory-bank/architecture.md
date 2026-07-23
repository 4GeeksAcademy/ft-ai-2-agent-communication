# Project Architecture

**Current status:** Scaffold + devcontainer are in place. Feature work follows the hour-sized chunks in [`implementation-plan.md`](./implementation-plan.md).

## Tech Stack

- **Monorepo orchestration**: Turborepo + pnpm workspaces
- Python backend using `uv` for project management and the following modules:
    - `fastapi` for the framework
    - `sqlmodel` for the orm
    - `alembic` for database migrations
- NextJS frontend using TypeScript
    - Browser Geolocation API for location services
    - JWT for authentication
    - TailwindCSS for styling
- Postgres database hosted on Neon.tech

## Monorepo Layout

```
/
├── apps/
│   ├── web/          # Next.js frontend (@area-todo/web)
│   └── api/          # FastAPI backend (@area-todo/api), managed with uv
├── packages/         # Shared JS/TS libraries and tool configs
├── memory-bank/      # Persistent agent/project context
├── package.json      # Root workspace scripts
├── pnpm-workspace.yaml
└── turbo.json        # Turborepo task graph
```

- `apps/*` and `packages/*` are pnpm workspace packages.
- Root scripts (`pnpm dev`, `pnpm build`, `pnpm lint`, `pnpm test`) delegate to `turbo run`.
- The API keeps Python tooling (`uv`, FastAPI, Alembic) inside `apps/api`; a local `package.json` exposes the same script names so Turborepo can orchestrate it with the frontend.
- Shared UI, eslint/tsconfig presets, and other cross-app code belong in `packages/`.

## Frontend (`apps/web`)

- **Framework**: Next.js 16 (App Router) with TypeScript strict mode and Tailwind CSS v4.
- **Structure**: feature folders under `features/`; shared UI under `shared/`.
- **Styling**: BEM class names with Tailwind `@apply` in colocated CSS files.
- **Dev**: `pnpm --filter @area-todo/web dev` or `pnpm dev` from the repo root.

```
apps/web/
├── app/                 # Next.js routes and root layout
├── features/
│   ├── home/            # Landing / home screen
│   ├── location/        # Geolocation status and hooks
│   └── todos/           # Todo list UI
└── shared/
    └── components/      # App shell and cross-feature UI
```

## Design Patterns
- MVC for backend
- Component-based UI with hooks

## Backend (`apps/api`)

- **Framework**: FastAPI with SQLModel and Alembic, managed by `uv`.
- **Structure**: MVC-style layers — controllers, services, repositories, models, schemas.
- **Dev**: `pnpm --filter @area-todo/api dev` or `pnpm dev` from the repo root.
- **API base**: `http://127.0.0.1:8000`

```
apps/api/
├── src/area_todo_api/
│   ├── controllers/     # HTTP routes (thin)
│   ├── services/        # Business logic
│   ├── repositories/    # Data access
│   ├── models/          # SQLModel ORM tables
│   ├── schemas/         # Request/response contracts
│   ├── config.py        # Settings from environment
│   ├── db.py            # Engine and session dependency
│   └── main.py          # FastAPI app factory
├── alembic/             # Database migrations
├── tests/
└── pyproject.toml       # uv project config
```

**Endpoints (initial)**
- `GET /health` — service health check
- `POST /api/v1/auth/register` — register with email/password
- `POST /api/v1/auth/login` — login and receive JWT
- `POST /api/v1/auth/logout` — revoke current session
- `GET /api/v1/auth/me` — current user + session id
- `GET /api/v1/todos` — list todos
- `POST /api/v1/todos` — create a location-tagged todo

## Local Development (Dev Container)

Use the devcontainer for a reproducible local stack with Node, Python/uv, and Postgres.

```
.devcontainer/
├── devcontainer.json    # VS Code / Cursor devcontainer config
├── docker-compose.yml   # App + Postgres services
├── Dockerfile           # Node 22, pnpm, uv, Python
└── post-create.sh       # Install deps and run migrations
```

1. **Dev Containers: Reopen in Container** from VS Code or Cursor.
2. Wait for post-create to finish (`pnpm install`, `uv sync`, `alembic upgrade head`).
3. Run `pnpm dev` from the repo root.

| Service  | URL                   |
|----------|-----------------------|
| Web      | http://localhost:3000 |
| API      | http://localhost:8000 |
| Postgres | localhost:5432        |
