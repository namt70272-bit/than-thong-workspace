# REFERENCE-INDEX.md

Guide to the reference material stored in `references/`.

**Last updated:** 2026-05-12

## Overview

The `references/` directory is the workspace knowledge shelf: imported docs, examples, and quick lookup material that support local work.

Current inventory: **4 reference collections / 10 files**.

## Reference collections

| Collection | Files | Purpose | Best used for |
| --- | ---: | --- | --- |
| `references/1password/` | 2 | 1Password CLI onboarding and usage examples | Local secret-management workflows and CLI usage patterns |
| `references/himalaya/` | 2 | Himalaya email client setup and composition notes | Email config and local mail workflow setup |
| `references/model-usage/` | 1 | CodexBar CLI usage notes | Inspecting or summarizing local model usage |
| `references/awesome-skills-catalog/` | 5 | Imported skill catalog and contribution docs | Discovering ideas, patterns, and examples for new skills |

## Detailed file index

### `references/1password/`
- `cli-examples.md` — example commands and usage patterns
- `get-started.md` — onboarding and setup notes

### `references/himalaya/`
- `configuration.md` — Himalaya configuration guidance
- `message-composition.md` — email composition notes

### `references/model-usage/`
- `codexbar-cli.md` — reference for CodexBar-related model usage inspection

### `references/awesome-skills-catalog/`
- `README.md` — main catalog landing page
- `README-VN.md` — Vietnamese-adapted/readability variant
- `INDEX.md` — quick catalog overview
- `USAGE.md` — how to use the catalog effectively
- `CONTRIBUTING.md` — adding or adapting skill entries

## How to use this folder

### When you need setup guidance
Start with:
- `references/1password/`
- `references/himalaya/`

### When you need skill inspiration
Start with:
- `references/awesome-skills-catalog/INDEX.md`
- then `references/awesome-skills-catalog/README.md`

### When you need model-usage help
Start with:
- `references/model-usage/codexbar-cli.md`
- then `scripts/model_usage.py`

## Placement rules

Put a document in `references/` when it is:
- imported knowledge, not authored workspace logic
- useful for repeated lookup
- stable enough to keep around
- better treated as source material than as active config

Do **not** put these in `references/`:
- generated reports (`reports/`)
- active helper code (`utils/`, `scripts/`)
- workspace policy files (`AGENTS.md`, `SOUL.md`, etc.)
- daily logs (`memory/`)

## Maintenance notes

- Add a short README inside any new reference collection if it grows beyond a couple files.
- Prefer grouped collections over dumping loose files into `references/`.
- If a reference becomes obsolete but still worth keeping, move it to `archive/`.
- Update this index whenever reference collections change.
