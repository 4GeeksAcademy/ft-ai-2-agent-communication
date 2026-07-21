# Backend Rules (Python / FastAPI)

- Use `uv` for dependency and project management.
- Keep FastAPI structured as MVC: routes/controllers thin, business logic in services, persistence via SQLModel models/repositories.
- Define request/response schemas explicitly; do not leak ORM models directly as API contracts unless intentionally shared and safe.
- Use Alembic for every schema change — no ad-hoc production schema edits.
- Follow PEP8; keep functions small and typed where practical.
- Prefer dependency injection (`Depends`) for DB sessions, auth, and shared services.
- Return consistent HTTP errors with clear messages; log server-side details, not client-facing stack traces.
- Keep location-aware queries efficient (index geo fields; avoid loading all todos into memory to filter).
