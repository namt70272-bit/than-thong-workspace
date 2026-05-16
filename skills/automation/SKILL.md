---
name: automation
description: >
  Consolidated automation & workflow skill. Covers TaskFlow (durable multi-step jobs, state, child tasks, waits),
  TaskFlow Inbox Triage (example routing pattern), Browser Use (Playwright web automation),
  Healthcheck (SSH/firewall/OS hardening), Billing Guard (approval-first paid usage), and
  Find Skills / ClawHub (search, install, publish agent skills).
metadata:
  { "openclaw": { "emoji": "⚙️" } }
---

# Automation & Workflow — Consolidated Skill

This skill merges all automation and workflow tooling into one reference:

1. [TaskFlow](#1-taskflow) — durable multi-step jobs with state, child tasks, and waits
2. [TaskFlow Inbox Triage](#2-taskflow-inbox-triage) — concrete inbox routing example
3. [Browser Use](#3-browser-use) — Playwright-based web automation
4. [Healthcheck](#4-healthcheck) — host audit and OS hardening
5. [Billing Guard](#5-billing-guard) — approval-first billing protection
6. [Find Skills / ClawHub](#6-find-skills--clawhub) — search, install, and publish skills

---

## 1. TaskFlow

> Original skill: `taskflow` 🪝

Use TaskFlow when a job needs to outlive one prompt or one detached run, but you still want one owner session, one return context, and one place to inspect or resume the work.

### When to use it

- Multi-step background work with one owner
- Work that waits on detached ACP or subagent tasks
- Jobs that may need to emit one clear update back to the owner
- Jobs that need small persisted state between steps
- Plugin or tool work that must survive restarts and revision conflicts cleanly

### What TaskFlow owns

- Flow identity
- Owner session and requester origin
- `currentStep`, `stateJson`, and `waitJson`
- Linked child tasks and their parent flow id
- Finish, fail, cancel, waiting, and blocked state
- Revision tracking for conflict-safe mutations

It does **not** own branching or business logic. Put that in Lobster, acpx, or the calling code.

### Runtime shape

Canonical plugin/runtime entrypoint:

- `api.runtime.tasks.flow`
- `api.runtime.taskFlow` still exists as an alias, but `api.runtime.tasks.flow` is the canonical shape

Binding:

- `api.runtime.tasks.flow.fromToolContext(ctx)` — when you already have trusted tool context with `sessionKey`
- `api.runtime.tasks.flow.bindSession({ sessionKey, requesterOrigin })` — when your binding layer already resolved the session and delivery context

### Managed-flow lifecycle

1. `createManaged(...)` — create the flow
2. `runTask(...)` — link and launch a child task
3. `setWaiting(...)` — block on a person or external system
4. `resume(...)` — continue when external input arrives
5. `finish(...)` or `fail(...)` — terminal states
6. `requestCancel(...)` or `cancel(...)` — stop the flow (cancel also terminates linked child tasks)

### Example shape

```ts
const taskFlow = api.runtime.tasks.flow.fromToolContext(ctx);

const created = taskFlow.createManaged({
  controllerId: "my-plugin/inbox-triage",
  goal: "triage inbox",
  currentStep: "classify",
  stateJson: {
    businessThreads: [],
    personalItems: [],
    eodSummary: [],
  },
});

const classify = taskFlow.runTask({
  flowId: created.flowId,
  runtime: "acp",
  childSessionKey: "agent:main:subagent:classifier",
  runId: "inbox-classify-1",
  task: "Classify inbox messages",
  status: "running",
  startedAt: Date.now(),
  lastEventAt: Date.now(),
});

if (!classify.created) {
  throw new Error(classify.reason);
}

const waiting = taskFlow.setWaiting({
  flowId: created.flowId,
  expectedRevision: created.revision,
  currentStep: "await_business_reply",
  stateJson: {
    businessThreads: ["slack:thread-1"],
    personalItems: [],
    eodSummary: [],
  },
  waitJson: {
    kind: "reply",
    channel: "slack",
    threadKey: "slack:thread-1",
  },
});

if (!waiting.applied) {
  throw new Error(waiting.code);
}

const resumed = taskFlow.resume({
  flowId: waiting.flow.flowId,
  expectedRevision: waiting.flow.revision,
  status: "running",
  currentStep: "finalize",
  stateJson: waiting.flow.stateJson,
});

if (!resumed.applied) {
  throw new Error(resumed.code);
}

taskFlow.finish({
  flowId: resumed.flow.flowId,
  expectedRevision: resumed.flow.revision,
  stateJson: resumed.flow.stateJson,
});
```

### Design constraints

- Use **managed** TaskFlows when your code owns the orchestration.
- One-task **mirrored** flows are created by core runtime for detached ACP/subagent work; this skill is mainly about managed flows.
- Treat `stateJson` as the persisted state bag. There is no separate `setFlowOutput` or `appendFlowOutput` API.
- Every mutating method after creation is revision-checked. Carry forward the latest `flow.revision` after each successful mutation.
- `runTask(...)` links the child task to the flow. Use it instead of manually creating detached tasks when you want parent orchestration.

### Operational pattern

- Store only the minimum state needed to resume.
- Put human-readable wait reasons in `blockedSummary` or structured wait metadata in `waitJson`.
- Use `getTaskSummary(flowId)` when the orchestrator needs a compact health view of child work.
- Use `requestCancel(...)` when a caller wants the flow to stop scheduling immediately.
- Use `cancel(...)` when you also want active linked child tasks cancelled.
- Keep conditionals **above** the runtime — use the flow runtime for state and task linkage; keep decisions in the authoring layer.

---

## 2. TaskFlow Inbox Triage

> Original skill: `taskflow-inbox-triage` 📥

A concrete example of how to think about TaskFlow without turning the core runtime into a DSL.

### Goal

Triage inbox items with one owner flow:

- **business** → post to Slack and wait for reply
- **personal** → notify the owner now
- **everything else** → keep for end-of-day summary

### Pattern

1. Create one flow for the inbox batch.
2. Run one detached task to classify new items.
3. Persist the routing state in `stateJson`.
4. Move to `waiting` only when an outside reply is required.
5. Resume the flow when classification or human input completes.
6. Finish when the batch has been routed.

### Suggested `stateJson` shape

```json
{
  "businessThreads": [],
  "personalItems": [],
  "eodSummary": []
}
```

Suggested `waitJson` when blocked on Slack:

```json
{
  "kind": "reply",
  "channel": "slack",
  "threadKey": "slack:thread-1"
}
```

### Minimal runtime calls

```ts
const taskFlow = api.runtime.tasks.flow.fromToolContext(ctx);

const created = taskFlow.createManaged({
  controllerId: "my-plugin/inbox-triage",
  goal: "triage inbox",
  currentStep: "classify",
  stateJson: {
    businessThreads: [],
    personalItems: [],
    eodSummary: [],
  },
});

const child = taskFlow.runTask({
  flowId: created.flowId,
  runtime: "acp",
  childSessionKey: "agent:main:subagent:classifier",
  task: "Classify inbox messages",
  status: "running",
  startedAt: Date.now(),
  lastEventAt: Date.now(),
});

if (!child.created) {
  throw new Error(child.reason);
}

const waiting = taskFlow.setWaiting({
  flowId: created.flowId,
  expectedRevision: created.revision,
  currentStep: "await_business_reply",
  stateJson: {
    businessThreads: ["slack:thread-1"],
    personalItems: [],
    eodSummary: [],
  },
  waitJson: {
    kind: "reply",
    channel: "slack",
    threadKey: "slack:thread-1",
  },
});

if (!waiting.applied) {
  throw new Error(waiting.code);
}

const resumed = taskFlow.resume({
  flowId: waiting.flow.flowId,
  expectedRevision: waiting.flow.revision,
  status: "running",
  currentStep: "route_items",
  stateJson: waiting.flow.stateJson,
});

if (!resumed.applied) {
  throw new Error(resumed.code);
}

taskFlow.finish({
  flowId: resumed.flow.flowId,
  expectedRevision: resumed.flow.revision,
  stateJson: resumed.flow.stateJson,
});
```

---

## 3. Browser Use

> Original skill: `browser-use` — Playwright-based browser automation

Use when the task requires navigating websites, interacting with web pages, filling forms, taking screenshots, or extracting information from web pages.

### What it does

Browser Use automates browser interactions via **Playwright**. It can:

- Navigate to URLs and interact with page elements
- Fill out and submit forms
- Take screenshots of pages or specific elements
- Extract structured data from web pages
- Run web tests and assertions
- Handle authentication flows on web apps

### When to use it

- Web testing or QA automation
- Automated form submission
- Scraping data from sites that require JavaScript
- Visual capture (screenshots / page thumbnails)
- Verifying UI state programmatically

### Key capabilities

| Task | Description |
|------|-------------|
| `navigate` | Open a URL in a controlled browser |
| `click` | Click buttons, links, and interactive elements |
| `fill` | Type into text inputs and forms |
| `screenshot` | Capture full-page or element-level screenshots |
| `extract` | Pull text or structured data from the DOM |
| `wait` | Wait for elements or network conditions |
| `evaluate` | Run JavaScript in the page context |

### Notes

- Requires a Playwright-compatible environment (Chromium/Firefox/WebKit).
- Prefer `web_fetch` for simple read-only page extraction (no JS); use Browser Use only when interaction or rendering is required.
- Sessions are ephemeral by default — do not rely on browser state across separate invocations unless the skill is configured for persistent sessions.

---

## 4. Healthcheck

> Original skill: `healthcheck` — host audit and OS hardening

Assess and harden the host running OpenClaw, aligned to a user-defined risk tolerance without breaking access.

### Core rules

- Recommend running with a state-of-the-art model (e.g., Opus 4.5, GPT 5.2+). Self-check the model; suggest switching if below that level — do not block execution.
- **Require explicit approval** before any state-changing action.
- Do not modify remote access settings without confirming how the user connects.
- Prefer reversible, staged changes with a rollback plan.
- Never claim OpenClaw changes the host firewall, SSH, or OS updates; it does not.
- Every set of user choices must be **numbered** so the user can reply with a single digit.

### Workflow (in order)

#### Step 0 — Model self-check (non-blocking)
Check the current model. Suggest switching if below state-of-the-art. Do not block.

#### Step 1 — Establish context (read-only)
Infer from the environment where possible. Determine:
1. OS and version; container vs host
2. Privilege level (root/admin vs user)
3. Access path (local, SSH, RDP, tailnet)
4. Network exposure (public IP, reverse proxy, tunnel)
5. OpenClaw gateway status and bind address
6. Backup system status
7. Deployment context
8. Disk encryption status (FileVault/LUKS/BitLocker)
9. OS automatic security updates status
10. Usage mode (local workstation vs headless/remote vs other)

Ask once for permission to run read-only checks. List follow-up info needed as unordered bullets.

#### Step 2 — Run OpenClaw security audits (read-only)
```bash
openclaw security audit --deep
```
Alternatives: `--json` (structured), `--fix` (apply safe defaults only — does NOT change host firewall/SSH/OS).

#### Step 3 — Check OpenClaw version/update status
```bash
openclaw update status
```

#### Step 4 — Determine risk tolerance
Offer suggested profiles (numbered):
1. Home/Workstation Balanced — most common
2. VPS Hardened — deny-by-default inbound, minimal ports, key-only SSH
3. Developer Convenience — more local services, explicit warnings
4. Custom — user-defined constraints

#### Step 5 — Produce a remediation plan
Include: target profile, current posture summary, gaps, step-by-step remediation with exact commands, access-preservation strategy, rollback, risks, least-privilege notes, credential hygiene.

Always show the plan **before** any changes.

#### Step 6 — Offer execution options
1. Do it for me (guided, step-by-step approvals)
2. Show plan only
3. Fix only critical issues
4. Export commands for later

#### Step 7 — Execute with confirmations
For each step: show exact command, explain impact and rollback, confirm access will remain available. Stop on unexpected output.

#### Step 8 — Verify and report
Re-check firewall status, listening ports, remote access, and re-run `openclaw security audit`. Deliver a final posture report.

### Required approvals (always)

- Firewall rule changes
- Opening/closing ports
- SSH/RDP configuration changes
- Installing/removing packages
- Enabling/disabling services
- User/group modifications
- Scheduling tasks or startup persistence
- Update policy changes
- Access to sensitive files or credentials

### Periodic checks & cron

After any audit/hardening pass, offer to schedule periodic audits:
```bash
openclaw cron add --name healthcheck:security-audit ...
openclaw cron add --name healthcheck:update-status ...
```
Check existing cron before creating: `openclaw cron list`. Use exact names above; update with `openclaw cron edit <id>` if found.

### Supported OpenClaw commands

```bash
openclaw security audit [--deep] [--fix] [--json]
openclaw status [--deep]
openclaw health --json
openclaw update status
openclaw cron add|list|runs|run
```

Do not invent CLI flags or imply OpenClaw enforces host firewall/SSH/OS policies.

### Memory writes

Only write to memory files when the user explicitly opts in and the session is a private/local workspace.
Append-only to `memory/YYYY-MM-DD.md` — never overwrite. Redact sensitive host details.

---

## 5. Billing Guard

> Original skill: `billing-guard`

Apply this skill whenever a request may:
- Use a paid API key
- Trigger provider billing
- Consume metered cloud/model usage
- Change billing settings, subscriptions, or quotas
- Choose a paid path when a local/auth path exists

### Rules

1. Default to **auth-first + local-first**.
2. Do **not** use billing or paid usage silently.
3. If billing may be touched, **pause and ask for explicit approval**.
4. Prefer in order:
   - Existing auth/session access
   - Local runtime / local model / local files
   - Already-approved provider path
   - New billed path only **after** approval

### Required response pattern

If billing may be required, say clearly:
- What action would touch billing
- Why it may cost money
- The cheapest local/auth alternative if one exists
- That **approval is required** before proceeding

### Examples

| Request | Action |
|---------|--------|
| Use OpenAI API with a new key | Requires approval |
| Run local Ollama instead | Allowed |
| Top up account / enable billing / upgrade plan | Requires approval |
| Use existing authenticated local session with no billing | Allowed |

### Current workspace standing instruction

- The owner is currently **negative on billing**.
- Do **not** touch billing or self-initiate paid usage.
- Any billing-related action requires explicit approval first.

---

## 6. Find Skills / ClawHub

> Original skills: `find-skills` + `clawhub`

Use when the user wants to discover, install, update, or publish agent skills.

### find-skills

Helps users discover and install skills when they:
- Ask "how do I do X?"
- Ask "find a skill for X"
- Ask "is there a skill that can…?"
- Express interest in extending agent capabilities

When triggered, search ClawHub or the local skill registry for matching skills and suggest installation.

### ClawHub CLI

Install the CLI first:

```bash
npm i -g clawhub
```

#### Auth (required for publish)
```bash
clawhub login
clawhub whoami
```

#### Search
```bash
clawhub search "postgres backups"
```

#### Install
```bash
clawhub install my-skill
clawhub install my-skill --version 1.2.3
```

#### Update
```bash
clawhub update my-skill
clawhub update my-skill --version 1.2.3
clawhub update --all
clawhub update my-skill --force
clawhub update --all --no-input --force
```

#### List installed skills
```bash
clawhub list
```

#### Publish
```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

### Notes

- Default registry: `https://clawhub.com` (override with `CLAWHUB_REGISTRY` or `--registry`)
- Default workdir: `cwd` (falls back to OpenClaw workspace); install dir: `./skills` (override with `--workdir` / `--dir` / `CLAWHUB_WORKDIR`)
- Update command hashes local files, resolves matching version, and upgrades to latest unless `--version` is set
- When billing guard is active, treat `clawhub install` with paid skills as requiring approval before proceeding

---

## Quick-reference matrix

| Sub-skill | Trigger keywords | Key action |
|-----------|-----------------|------------|
| TaskFlow | multi-step job, durable task, state, child task, wait, resume | Create managed flow, run child, set waiting, resume, finish |
| Inbox Triage | inbox, route, triage, classify, Slack reply | TaskFlow pattern with business/personal/eod buckets |
| Browser Use | browser, Playwright, form, screenshot, scrape, navigate | Playwright automation — click, fill, screenshot, extract |
| Healthcheck | audit, harden, firewall, SSH, cron, security, OS | Read-only audit → plan → approved changes → verify |
| Billing Guard | billing, API key, paid, subscription, quota, metered | Pause → disclose → offer local alt → require approval |
| Find Skills / ClawHub | find skill, install skill, publish skill, search skill | `clawhub search / install / update / publish` |
