# skills/README.md

Guide to the `skills/` directory.

## What lives here

This folder contains:
- formal skills with `SKILL.md`
- skill-specific support material
- local tooling for creating and packaging skills

## Current contents

| Entry | Type | Purpose |
| --- | --- | --- |
| `billing-guard/` | Formal skill | Prevent accidental billing or paid-usage actions |
| `khai-thac/` | Formal skill | Safe extraction and selective reuse from outside repos/folders |
| `review-code/` | Formal skill | Structured local code review workflow |
| `skill-creator/` | Tooling | Scripts for initializing, packaging, and validating skills |
| `SKILL-REGISTRY.md` | Index | Local mirror of the workspace skill inventory |

## How to use

1. Pick a matching skill.
2. Open `skills/<name>/SKILL.md`.
3. Follow the workflow described there.
4. Update `SKILL-REGISTRY.md` if you add or archive anything.

## Naming convention

- Formal skill: `skills/<skill-name>/SKILL.md`
- Support files: keep them inside the skill folder
- Tooling-only folders should be labeled clearly in docs so they are not mistaken for formal skills

## Maintenance

- Keep one skill per folder.
- Keep descriptions action-oriented.
- Archive retired skills instead of deleting them outright.
- If a tooling folder becomes a true skill, add `SKILL.md` and register it.
