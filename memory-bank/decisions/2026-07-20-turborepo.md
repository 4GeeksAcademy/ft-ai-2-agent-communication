# 2026-07-20 — Use Turborepo for monorepo orchestration

## Context

Area Todo is a polyglot monorepo (Next.js frontend + FastAPI backend). We need a single entry point for common tasks (`dev`, `build`, `lint`, `test`) across apps.

## Decision

Use **Turborepo** with **pnpm workspaces** to orchestrate the monorepo.

- Apps live under `apps/` (`web`, `api`).
- Shared JS/TS libraries and configs live under `packages/`.
- The Python API remains managed by `uv` inside `apps/api`; Turborepo invokes its scripts via a thin `package.json` so tasks stay uniform at the repo root.

## Consequences

- Root commands: `pnpm dev`, `pnpm build`, `pnpm lint`, `pnpm test`.
- Caching applies mainly to Node/Next.js outputs; Python scripts opt into the same task names for consistency.
- New apps/packages must include a `package.json` to be workspace members.
