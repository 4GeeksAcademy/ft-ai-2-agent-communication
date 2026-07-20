# Project Architecture

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

## Design Patterns
- MVC for backend
- Component-based UI with hooks
