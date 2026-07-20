# Frontend Rules (Next.js / TypeScript)

- Use TypeScript in strict mode; avoid `any` unless there is no better option and it is documented.
- Organize UI by feature folders, not by diffuse type-only dumps (`components/`, `hooks/` only when shared).
- Prefer functional components and custom hooks for reusable logic.
- Style with Tailwind via CSS BEM class names and `@apply` so markup stays readable.
- Design mobile-first and touch-friendly (large tap targets, minimal dense chrome).
- Keep proximity/location UX clear: show when location is missing, denied, or session-pinned.
- Use JWT auth flows consistently; store tokens securely and handle expiry with a clear re-auth path.
- Do not put business rules that belong on the server solely in the client.
