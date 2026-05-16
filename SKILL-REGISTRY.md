# SKILL-REGISTRY.md

Master inventory of skills and skill-related tooling in this workspace.

**Last updated:** 2026-05-12

## Summary

This workspace currently contains:
- **3 formal skills** with `SKILL.md`
- **1 skill tooling directory** (`skills/skill-creator/`)
- **1 external skill-source note area** at root (`khai-thac/`)

## Formal skills

| Skill | Location | Type | What it is for | Key notes |
| --- | --- | --- | --- | --- |
| `billing-guard` | `skills/billing-guard/SKILL.md` | Guardrail | Any task that could touch billing, paid API usage, quotas, subscriptions, or metered provider usage | Approval-first, auth-first, local-first |
| `khai-thac` | `skills/khai-thac/SKILL.md` | Extraction workflow | Safely review and selectively reuse content from outside repos/folders without importing entire trees | Emphasizes inventory, selective import, isolation, and testing |
| `review-code` | `skills/review-code/SKILL.md` | Review workflow | Generate structured code review feedback from local diffs or staged changes | Local-first; adapted from Agent365 review workflow |

## Skill details

### 1. billing-guard
**Use when:**
- a request may trigger paid model/API usage
- a task may change billing, quotas, subscriptions, or top-ups
- there is a local/authenticated alternative and you need to decide safely

**Core rules:**
- default to auth-first + local-first
- do not silently choose a billed path
- stop and request approval if billing may be touched

### 2. khai-thac
**Use when:**
- source material lives outside the active workspace
- you need to inspect, extract, and adapt only the useful parts
- copying a whole repo would be risky, noisy, or likely to create conflicts

**Core workflow:**
1. inventory
2. read high-value docs first
3. select only what is needed
4. build a minimal candidate
5. test in isolation
6. connect later only if safe

### 3. review-code
**Use when:**
- reviewing a PR, staged changes, or local diffs
- checking design, testing, security, and code quality together
- you want structured feedback without relying on GitHub auth

**Review focus:**
- architecture
- security
- testing
- code quality
- dependency choices
- documentation gaps

## Skill-related tooling

These are not formal skills with `SKILL.md`, but they support skill work.

| Tooling dir | Contents | Purpose |
| --- | --- | --- |
| `skills/skill-creator/` | `init_skill.py`, `package_skill.py`, `quick_validate.py` | Create, package, and validate skills locally |

### `skills/skill-creator/` scripts
- `init_skill.py` — scaffold a new skill from a template
- `package_skill.py` — bundle a skill for sharing/release
- `quick_validate.py` — run a lightweight validation pass

## Related utilities that support skill work

| Path | Purpose |
| --- | --- |
| `utils/prompt_utils.py` | Load prompts, render templates, sanitize input/output |
| `utils/rate_limiter.py` | Token-bucket rate limiter for LLM-style workflows |
| `config/prompts-template.yaml` | Prompt template collection for LLM tasks |

## Where to start

- Want the short version? Open `skills/README.md`.
- Want the full workspace picture? Open `WORKSPACE.md`.
- Need reference material for skill design? Check `references/awesome-skills-catalog/`.

## Recommended maintenance

- Add new formal skills under `skills/<name>/SKILL.md`.
- Update this registry whenever a skill or tooling directory is added, renamed, archived, or removed.
- Keep skill descriptions action-oriented so future-you can route tasks quickly.
