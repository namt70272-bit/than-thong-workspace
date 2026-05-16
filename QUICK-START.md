# QUICK-START.md

Fast path for a new operator or future-you.

## In the first 5 minutes

1. Read `README.md`.
2. Skim `WORKSPACE.md`.
3. Read `SOUL.md` and `AGENTS.md`.
4. Check `USER.md` and `TOOLS.md`.
5. Open `SKILL-REGISTRY.md` to see what is available.

## What each core file does

| File | Why it matters |
| --- | --- |
| `AGENTS.md` | Local workspace rules and operating norms |
| `SOUL.md` | Personality, tone, and behavioral center |
| `IDENTITY.md` | Name, vibe, emoji, avatar |
| `USER.md` | Human preferences and standing constraints |
| `TOOLS.md` | Environment-specific notes and shortcuts |
| `WORKSPACE.md` | Full workspace guide |
| `SKILL-REGISTRY.md` | Skills inventory |
| `REFERENCE-INDEX.md` | Reference inventory |
| `CHANGES.md` | What changed during restructure |

## Fast navigation by intent

### I need to do work
- Skills: `skills/`
- Shared code: `utils/`
- Runnable helpers: `scripts/`
- Config templates: `config/`

### I need context
- Human preferences: `USER.md`
- Local setup: `TOOLS.md`
- Prior reports: `reports/`
- Reference material: `references/`
- Daily notes: `memory/`

### I need to find older or retired material
- `archive/deprecated/`

## Skills at a glance

- `billing-guard` — stops accidental paid usage or billing actions
- `khai-thac` — safely extract only needed content from outside repos/folders
- `review-code` — structured local diff/code review workflow
- `skill-creator/` — helper scripts for building and packaging skills

See full details in `SKILL-REGISTRY.md`.

## Recommended daily workflow

1. Check `memory/` for the latest note.
2. Review `USER.md` for constraints.
3. Choose a skill if the task matches one.
4. Use `utils/` or `scripts/` only when they clearly help.
5. Write notable decisions back into `memory/YYYY-MM-DD.md`.
6. Move obsolete artifacts to `archive/` instead of deleting.

## Where to put new things

| If you have... | Put it here |
| --- | --- |
| A new reusable skill | `skills/<name>/` |
| A shared Python helper | `utils/` |
| A one-off runnable helper | `scripts/` |
| Imported knowledge or docs | `references/` |
| Generated analysis or audit output | `reports/` |
| Workflow sample or template | `examples/` |
| Old but potentially useful files | `archive/deprecated/` |
| Daily notes | `memory/` |

## Good defaults

- Prefer local/auth-first paths.
- Do not touch billing without explicit approval.
- Archive instead of deleting.
- Keep docs current when structure changes.
- Add memory notes when a decision is worth preserving.

## If you only read three files

1. `SOUL.md`
2. `AGENTS.md`
3. `SKILL-REGISTRY.md`
