# Memory Bank Usage

- Before planning or editing, read only the relevant memory-bank files for the task (see `memory-bank/README.md`). Prefer atomic reads over loading the entire bank.
- For sequenced feature work, follow `memory-bank/implementation-plan.md` and stay inside the current chunk unless asked otherwise.
- Prefer memory-bank documents over assumptions when they conflict with guesses.
- When you make a lasting technical choice, record it under `memory-bank/decisions/` with a short title, date, context, decision, and consequences.
- Do not invent product requirements that contradict `product-context.md`. Ask if something is unclear.
- Keep memory-bank docs concise and current; update them when architecture or conventions change.
- After shipping a chunk, update the plan checklist and any contracts (`data-model`, `user-flows`, `auth`) that drifted.
