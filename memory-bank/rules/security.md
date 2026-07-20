# Security Rules

- Treat JWT secrets and database credentials as secrets; never hardcode them.
- Validate and authorize on the server for every mutating endpoint; do not trust client role or user id claims alone beyond verified tokens.
- Scope data access to the authenticated user (and their session area when relevant).
- Be careful with location data: collect only what is needed, and respect browser permission denials gracefully.
- Sanitize/validate all inputs (coords, todo text, area labels) before persistence.
- Prefer HTTPS-only cookie or secure storage patterns appropriate to the chosen JWT delivery method.
- Do not log tokens, passwords, or precise location dumps in production logs.
