# Academic Resource Telegram Bot

An async Telegram bot that gives students branch-aware access to academic resources.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the shared API server (port 5000)
- `python tel-bot/bot.py` — run the Telegram polling worker after adding `TELEGRAM_BOT_TOKEN`
- `cd tel-bot && python -m unittest test_suite.py` — run the bot checks
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env for the bot: `TELEGRAM_BOT_TOKEN` — stored as a Replit Secret

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `tel-bot/resources_data.py` — source of truth for academic structure and all resource links
- `tel-bot/bot.py` — Telegram handlers and in-place navigation
- `tel-bot/keep_alive.py` — Render health endpoint
- `tel-bot/keep_alive_bot.py` — ten-minute sentinel watchdog
- `tel-bot/render.yaml` — Render service definitions
- `tel-bot/test_suite.py` — data and callback contract checks

## Architecture decisions

- Resource URLs are kept exclusively in `resources_data.py`, so link updates do not touch navigation logic.
- Callback data uses compact prefixes and is checked against Telegram's 64-byte limit.
- Navigation edits the existing Telegram message instead of sending a new message for each button click.
- MI intentionally exposes only Year 1 as active; its other years show an alert and are not connected to resources.
- The bot refuses to start without a secret-backed replacement token.

## Product

Students choose MI or ST, then a year, specialty where applicable, and a resource category. ST Years 1–2 access resources directly, while ST Years 3–5 use the five engineering specialties.

## User preferences

- Keep resource links editable by non-programmers in the data module.

## Gotchas

- The old Telegram token was exposed and must not be used. Add the regenerated value through Replit Secrets.
- Empty resource URLs intentionally show a pending alert until club members populate them in `resources_data.py`.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
