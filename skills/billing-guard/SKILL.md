---
name: billing-guard
description: Use when a task may touch billing, paid API usage, top-ups, subscriptions, provider quotas, or any non-local paid resource. Enforces approval-first behavior and local/auth-first alternatives.
---

# Billing Guard

Apply this skill whenever a request may:
- use a paid API key
- trigger provider billing
- consume metered cloud/model usage
- change billing settings, subscriptions, or quotas
- choose a paid path when a local/auth path exists

## Rules

1. Default to **auth-first + local-first**.
2. Do **not** use billing or paid usage silently.
3. If billing may be touched, pause and ask for explicit approval.
4. Prefer these options in order:
   - existing auth/session access
   - local runtime / local model / local files
   - already-approved provider path
   - new billed path only after approval

## Required response pattern

If billing may be required, say clearly:
- what action would touch billing
- why it may cost money
- the cheapest local/auth alternative if one exists
- that approval is required before proceeding

## Examples

- "Use OpenAI API with a new key" -> requires approval
- "Run local Ollama instead" -> allowed
- "Top up account / enable billing / upgrade plan" -> requires approval
- "Use existing authenticated local session that does not incur billing" -> allowed

## Notes for this workspace

Current standing instruction:
- The owner is currently negative on billing.
- From now on, do not touch billing or self-initiate paid usage.
- Any billing-related action requires explicit approval first.
