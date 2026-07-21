# Implementation Plan

Area Todo is a **demonstration project for adult students**. The product (a location-aware todo app) is the vehicle. The core lessons are:

1. Building **atomic memory banks** so agents get the right context without stuffing everything into one file.
2. Managing **agent-driven development workflows** — plan → prompt → verify → record decisions → update memory.

Work is split into **~1-hour chunks**. Complete one chunk per session. Prefer finishing a chunk cleanly over starting the next one.

## How to use this plan

Each chunk has four parts:

| Part | Purpose |
|------|---------|
| **Teaching focus** | The agent/memory skill students practice |
| **Memory bank work** | Docs to read, write, or update *before or during* coding |
| **Build work** | Concrete product changes |
| **Done when** | Exit criteria so the session can end on time |

**Session workflow (repeat every chunk):**

1. Read only the memory-bank files listed for that chunk (atomicity in practice).
2. Write or update the memory-bank artifacts *before* asking an agent to implement large changes.
3. Give the agent a narrow prompt scoped to this chunk’s “Build work.”
4. Verify by running the app (`pnpm dev`) and any listed checks.
5. If a lasting technical choice was made, add a short note under `memory-bank/decisions/`.
6. Mark the chunk complete in the checklist below.

Do **not** invent product requirements that contradict `product-context.md`. If something is ambiguous, ask rather than guess.

## Baseline (already done)

Students start here — do not rebuild these in later chunks:

- Turborepo + pnpm monorepo (`apps/web`, `apps/api`)
- Devcontainer with Node, uv, and Postgres
- FastAPI MVC skeleton: `GET /health`, `GET/POST /api/v1/todos` with lat/lng
- Next.js shell: home page, geolocation hook/banner, todo list placeholder
- Memory bank skeleton: product, architecture, conventions, rules, one Turborepo decision

## Progress checklist

- [ ] Chunk 1 — Orient the memory bank and the running app
- [ ] Chunk 2 — Spec proximity: user flows + data contracts
- [ ] Chunk 3 — Wire the web app to the API
- [ ] Chunk 4 — Proximity sort on the backend
- [ ] Chunk 5 — Complete, edit, and delete todos
- [ ] Chunk 6 — Auth with JWT (register / login)
- [ ] Chunk 7 — Session-pinned areas
- [ ] Chunk 8 — Harden workflow: rules, decisions, and demo polish

---

## Chunk 1 — Orient the memory bank and the running app (~1 hour)

**Teaching focus:** Why agents fail without persistent, *atomic* context; which file answers which question.

**Memory bank work:**

- Read: `README.md` (repo root — human lesson framing), `product-context.md`, `architecture.md`, `rules/README.md`, `rules/memory-bank.md`.
- Add `memory-bank/user-flows.md` with a short outline only (titles + 2–3 bullets per flow). Leave detail for Chunk 2.
  Suggested flow titles: *Enable location*, *Add a place-tagged todo*, *See nearby todos*, *Pin a session area* (desktop).
- Optionally add a one-line “Current status” section at the top of `architecture.md` pointing at this plan.

**Build work:**

- Open the repo in the **devcontainer** if not already.
- Run `pnpm dev`; confirm web (`:3000`), API (`:8000`), and `GET /health`.
- Create one todo via API docs or `curl` to confirm Postgres + migrations.

**Done when:**

- Students can explain what each top-level memory-bank file is for.
- App and API are running in the container.
- `user-flows.md` exists with flow titles (not full detail yet).

---

## Chunk 2 — Spec proximity: user flows + data contracts (~1 hour)

**Teaching focus:** Spec in the memory bank *before* code; agents follow written contracts better than chat history.

**Memory bank work:**

- Expand `user-flows.md` for *Enable location*, *Add a place-tagged todo*, and *See nearby todos* (happy path + denied location + empty list).
- Add `memory-bank/data-model.md` describing:
  - `Todo` fields (as implemented today)
  - Planned query params for proximity (`lat`, `lng`, optional `radius_m`)
  - Response shape including `distance_m` (or equivalent) for sorted lists
- Skim `rules/backend.md` and `rules/frontend.md` so upcoming prompts cite them.

**Build work:**

- No large feature code yet. Optionally add a short OpenAPI-friendly comment or schema stub only if it clarifies the contract — prefer documenting first.
- Draft the agent prompt you will use in Chunk 3–4 (save it in the chunk notes or a comment in this plan’s student notebook — not required in-repo).

**Done when:**

- Flows and data contracts are written clearly enough that a fresh agent session could implement without product improvisation.
- Team agrees on distance units and sort order (nearest first).

---

## Chunk 3 — Wire the web app to the API (~1 hour)

**Teaching focus:** Narrow agent prompts; one feature slice; verify against the memory bank, not against vibes.

**Memory bank work:**

- Read: `data-model.md`, `user-flows.md` (add/list), `conventions.md`, `rules/frontend.md`.
- After implementation: note the chosen API base URL / env pattern in `architecture.md` if not already accurate.

**Build work:**

- Replace `TodoListPlaceholder` with a real list that fetches `GET /api/v1/todos`.
- Add a simple form to create a todo using the current geolocation (disable submit until location is granted).
- Handle loading and error states in a touch-friendly way.
- Keep styling via BEM + Tailwind `@apply` per conventions.

**Done when:**

- From the phone-sized UI, a user can enable location, add a todo, and see it in the list (order can still be creation order).
- No secrets committed; CORS/env works in the devcontainer.

---

## Chunk 4 — Proximity sort on the backend (~1 hour)

**Teaching focus:** Record architectural decisions when choosing an approach; update atomic docs so the next session inherits truth.

**Memory bank work:**

- Read: `data-model.md`, `rules/backend.md`, `architecture.md`.
- After choosing an approach (e.g. Haversine in SQL/Python vs PostGIS), add `memory-bank/decisions/YYYY-MM-DD-proximity-sorting.md` (context / decision / consequences).
- Update `data-model.md` and `architecture.md` endpoints section to match what shipped.

**Build work:**

- Extend `GET /api/v1/todos` to accept location query params and return todos sorted by distance.
- Keep MVC boundaries: controller thin, logic in service/repository.
- Add or extend API tests for sort order with known fixtures.
- Update the web list to send current lat/lng and display distance.

**Done when:**

- Nearby todos sort correctly for at least two known points.
- Decision doc exists; architecture/data-model match the code.

---

## Chunk 5 — Complete, edit, and delete todos (~1 hour)

**Teaching focus:** Keep rules and schemas in sync when expanding an existing feature; avoid “agent drift” on patterns.

**Memory bank work:**

- Update `user-flows.md` with *Complete a todo* and *Edit / delete a todo*.
- Update `data-model.md` for patch/delete contracts.
- Read `rules/general.md` — prefer small, focused changes.

**Build work:**

- Backend: `PATCH` (or equivalent) to toggle complete / edit fields; `DELETE` by id.
- Frontend: mark complete, edit title, delete — large tap targets.
- Tests for the new endpoints.

**Done when:**

- Full basic CRUD works end-to-end with location still attached on create.
- Memory-bank contracts match the live API.

---

## Chunk 6 — Auth with JWT (register / login) (~1 hour)

**Teaching focus:** Security context is its own atomic doc; agents must be pointed at `rules/security.md` for auth work.

**Memory bank work:**

- Read: `rules/security.md`, `product-context.md` (sessions), `architecture.md`.
- Add `memory-bank/auth.md` covering: register/login endpoints, JWT claims, where the client stores the token, and that todos become user-scoped.
- Add a decision if choosing cookie vs `Authorization` header storage for this demo.

**Build work:**

- User model + Alembic migration; password hashing; register/login endpoints; JWT issue/verify dependency.
- Scope todo list/create/mutate to the authenticated user.
- Minimal login/register UI; attach token on API calls.
- Do not log tokens or passwords.

**Done when:**

- Two users cannot see each other’s todos.
- `auth.md` and security rules still accurately describe the system.

**Scope guard:** Session-pinned *areas* wait for Chunk 7. Auth alone is enough for this hour.

---

## Chunk 7 — Session-pinned areas (~1 hour)

**Teaching focus:** Product context drives features — “desktop pinned to office” comes from `product-context.md`, not from agent invention.

**Memory bank work:**

- Expand `user-flows.md` for *Pin a session area* and *Use pinned area instead of GPS*.
- Update `auth.md` / `data-model.md` for area fields on the session or user-device concept (keep the model as simple as the hour allows).
- Decision doc if the pin is stored server-side vs client-only for the demo.

**Build work:**

- Allow a logged-in session to set a named area (label + lat/lng), e.g. “Office.”
- When a pin is active, use it for create/sort instead of live GPS; show clear UI state (pinned vs live).
- Respect geolocation denial by offering pin-as-fallback messaging.

**Done when:**

- A “desktop” style flow works: pin Office, add todos, see proximity relative to the pin.
- Product-context requirement for area-pinned sessions is demonstrably met.

---

## Chunk 8 — Harden workflow: rules, decisions, and demo polish (~1 hour)

**Teaching focus:** Memory banks rot unless updated; close the loop by tightening rules from real agent mistakes observed in class.

**Memory bank work:**

- Audit all memory-bank docs against the running app; fix drift in `architecture.md`, `data-model.md`, `user-flows.md`, `auth.md`.
- Update `rules/*` with 1–3 concrete lessons learned (e.g. “always pass lat/lng on list,” “never create todos without user id”).
- Ensure `decisions/README.md` indexes every decision file.
- Check this plan’s checklist — mark completed chunks.

**Build work:**

- Light polish only: empty states, error copy, disable broken controls, README quickstart accuracy.
- Confirm `pnpm lint` / `pnpm test` (or the project’s equivalent) pass for the paths touched in class.
- Prepare a 5-minute demo script: location → add → sort → login boundary → pinned area.

**Done when:**

- A new agent session, given only the memory bank + a short prompt, could continue maintenance without rediscovering architecture from scratch.
- Students can explain *which* atomic file they would open for a frontend vs auth vs proximity change.

---

## Out of scope (unless a future cohort extends the plan)

- Native mobile apps
- Real-time multi-user collaboration
- Production Neon deployment and CI/CD hardening
- PostGIS / map tiles beyond what Chunk 4 needs
- Social features, sharing lists, or notifications

## Facilitation notes (instructors)

- Protect the hour: if build work slips, finish the **memory bank work** and a thin vertical slice rather than a wide half-done feature.
- Prefer students writing the agent prompt from the chunk’s docs over pasting large generated specs.
- After each chunk, ask: “Which file would you @-mention for the next change?” — that is the atomicity check.
- Celebrate decision docs; they are part of the deliverable, not bureaucracy.
