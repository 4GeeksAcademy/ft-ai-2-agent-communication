# User & Session Data Model

Persistence contracts for authentication. Auth behavior and HTTP endpoints live in [`auth.md`](./auth.md).

## User

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `email` | string | Unique, case-normalized (store lowercase) |
| `password_hash` | string | Argon2id hash; never returned in API responses |
| `created_at` | datetime (UTC) | Set on create |
| `updated_at` | datetime (UTC) | Updated on password or email change |

### Password rules

- Minimum length: **8** characters
- Maximum length: **128** characters (reject longer inputs before hashing)
- Hash with **Argon2id** (see [ADR](../../decisions/2026-07-23-auth-mvp.md))
- Never log plaintext passwords or hashes

### Public user (API shape)

Returned by auth endpoints. Never include `password_hash`.

| Field | Type |
|-------|------|
| `id` | UUID |
| `email` | string |
| `created_at` | datetime (UTC) |

## Session

A **login session** (not a SQLAlchemy/DB session). One row per successful register/login. JWT `sid` claim points at this row so logout can revoke and a future area-pin feature can attach location without changing auth claim shape.

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key; JWT `sid` |
| `user_id` | UUID | FK → User |
| `created_at` | datetime (UTC) | Set on create |
| `expires_at` | datetime (UTC) | Align with JWT `exp` |
| `revoked_at` | datetime (UTC), nullable | Set on logout; null means active |

### Area-pin hooks (MVP unused)

Reserved for a later area-pinning feature. Auth register/login/logout **ignore** these fields; leave them null.

| Field | Type | Notes |
|-------|------|--------|
| `pinned_lat` | float, nullable | Latitude of pinned place |
| `pinned_lng` | float, nullable | Longitude of pinned place |
| `pinned_label` | string, nullable | Human label (e.g. "office") |

Future area-pin work may add a dedicated Area entity and replace or complement these columns; until then they are the extension point on Session.

### Session validity

A session is **valid** when:

1. `revoked_at` is null, and
2. `expires_at` is in the future

Invalid sessions must reject authenticated requests (`401`).

## Relationships

- User **1 — N** Session
- Register and login each create a new Session
- Logout sets `revoked_at` on the Session identified by JWT `sid`
