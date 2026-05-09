# OpenClaw Infrastructure Audit — 2026-05-09 22:45 GMT+7

Scope: local OpenClaw installation and runtime areas on C: and E:. Secrets/tokens were intentionally redacted or not copied into this report.

## Executive summary

- OpenClaw is installed on C: via npm at `C:\Users\ACER\AppData\Roaming\npm\node_modules\openclaw`.
- Installed package version is `2026.5.2`; update available according to `openclaw status`: npm `2026.5.7`.
- Gateway is running locally on `127.0.0.1:18789`, reachable over WebSocket/HTTP loopback.
- Windows Scheduled Task `OpenClaw Gateway` launches `C:\Users\ACER\.openclaw\gateway.cmd`, which points runtime home to E:.
- Current active workspace is `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`.
- Migration from C runtime to E runtime is partially complete: active gateway launcher uses E runtime, but C still holds important legacy/runtime directories and launcher stubs.
- Telegram is enabled and healthy; Discord is disabled.
- Heartbeat is disabled. Cron list via live scheduler returned zero jobs, though old cron job/run files still exist under C runtime.
- Security audit found 0 critical, 2 warnings, 1 info.

## Architecture reference

OpenClaw uses one long-lived Gateway that owns messaging surfaces and serves WebSocket clients, web UI, automations, and nodes. Default gateway bind is local loopback on port `18789`. Canvas/A2UI are served by the same gateway HTTP server under `/__openclaw__/canvas/` and `/__openclaw__/a2ui/`.

## C: layout

### Code install

- `C:\Users\ACER\AppData\Roaming\npm\openclaw.ps1`
- `C:\Users\ACER\AppData\Roaming\npm\openclaw.cmd`
- `C:\Users\ACER\AppData\Roaming\npm\node_modules\openclaw`

Package metadata:

- name: `openclaw`
- version: `2026.5.2`
- CLI bin: `openclaw.mjs`
- main code dirs: `assets`, `dist`, `docs`, `node_modules`, `patches`, `scripts`, `skills`

### Legacy/default runtime root

`C:\Users\ACER\.openclaw` still contains substantial runtime state:

- Config files: `openclaw.json`, backups, last-good config
- Gateway launcher: `gateway.cmd`
- Agents/session state: `agents\main\agent`, `agents\main\sessions`
- Runtime data: `canvas`, `credentials`, `cron`, `devices`, `flows`, `identity`, `memory`, `tasks`, `telegram`, `workspace`
- Extensions/plugins: `extensions`, `plugins`
- Queues/logs: `delivery-queue`, `logs`, `locks`
- Other: `qqbot`, `subagents`, local `node_modules`

Notable C-only extension/plugin directories seen:

- `agntdata-x`
- `doc-to-pdf`
- `engram`
- `scan-document`
- `telegram-ui`
- `web-search-plus-plugin.disabled`

## E: layout

Root: `E:\KY-DATA\OpenClaw`

Major directories:

- `runtime-mirror` — target runtime root
- `code-mirror` — mirrored OpenClaw package/code
- `backups`, `reports`, `projects`, `scripts`, `tools`, `memory-system`, `models-local`, etc.

Migration docs present:

- `README-MIGRATION.md`
- `MIGRATION-MANIFEST.md`
- `CODE-MIRROR-README.md`

### E runtime

Active/current workspace observed:

- `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`

Runtime root contains:

- `.openclaw\agents`
- `.openclaw\canvas`
- `.openclaw\devices`
- `.openclaw\identity`
- `.openclaw\logs`
- `.openclaw\tasks`
- `.openclaw\tui`
- `.openclaw\workspace`
- `.openclaw\openclaw.json`
- `.openclaw\openclaw.json.last-good`

### E code mirror

- Code root: `E:\KY-DATA\OpenClaw\code-mirror\npm\node_modules\openclaw`
- Package version: `2026.5.2`
- Native E launcher: `E:\KY-DATA\OpenClaw\openclaw-e-native.ps1`
- Native E gateway launcher: `E:\KY-DATA\OpenClaw\gateway-e-native.cmd`

## Launchers and service path

Windows Scheduled Task:

- Task: `OpenClaw Gateway`
- Action: `C:\Users\ACER\.openclaw\gateway.cmd`
- State shown by Task Scheduler: `Ready`
- `openclaw status` also verified listener running with PID `12600` on port `18789`.

Gateway launcher content summary:

- Sets `OPENCLAW_HOME=E:\KY-DATA\OpenClaw\runtime-mirror`
- Sets `OPENCLAW_WORKSPACE=E:\KY-DATA\OpenClaw\runtime-mirror\workspace`
- Starts C-installed OpenClaw code: `C:\Users\ACER\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`

Important discrepancy:

- Launcher sets `OPENCLAW_WORKSPACE=E:\KY-DATA\OpenClaw\runtime-mirror\workspace`.
- Actual active injected workspace is `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`.
- This should be reviewed before hardening or final migration.

Available launchers:

- C npm CLI: `C:\Users\ACER\AppData\Roaming\npm\openclaw.ps1`
- C gateway launcher: `C:\Users\ACER\.openclaw\gateway.cmd`
- E launcher using C code: `E:\KY-DATA\OpenClaw\openclaw-e.ps1`
- E gateway using C code: `E:\KY-DATA\OpenClaw\gateway-e.cmd`
- E-native launcher using E mirror code: `E:\KY-DATA\OpenClaw\openclaw-e-native.ps1`
- E-native gateway using E mirror code: `E:\KY-DATA\OpenClaw\gateway-e-native.cmd`

## Active status snapshot

From `openclaw status --deep`:

- OS: Windows 10.0.26200 x64
- Node: 24.14.1
- Dashboard: `http://127.0.0.1:18789/`
- Gateway: local loopback, reachable
- Tailscale exposure: off
- Gateway service: Scheduled Task installed; gateway listener detected on port 18789
- Node service: not installed
- Agents: 2
- Bootstrap file present: yes
- Sessions: 1 active
- Default model: `gpt-5.4`, current session using `gpt-5.5`
- Memory: enabled via `memory-core`; not checked by fast status
- Events: none
- Tasks: none
- Heartbeat: disabled for main and codex
- Telegram: enabled and OK

## Active config summary

Secrets are redacted.

Gateway:

- mode: `local`
- bind: `loopback`
- auth: token mode
- Control UI allowed origins: `localhost:18789`, `127.0.0.1:18789`

Channels:

- Telegram enabled
- Telegram DM policy allowlist
- Telegram allowed account: one allowlisted numeric ID
- Discord disabled

Agents:

- `main`: coding tool profile, elevated tools enabled with Telegram allowlist
- `codex`: ACP runtime, backend `acpx`, persistent mode, cwd currently points to `C:\Users\ACER\.openclaw\workspace`

Model providers/configured models:

- OpenAI via OpenAI-compatible/completions config; configured `gpt-4o-mini`
- OpenAI Codex via ChatGPT backend responses config; configured `gpt-5.4`
- DeepSeek: `deepseek-chat`, `deepseek-reasoner`, `deepseek-v4-flash`
- Ollama provider present at `http://localhost:11434/v1`, no models listed

Plugins:

- Allowed/enabled entries include Telegram, active-memory, agntdata-x, OpenAI, DeepSeek, Ollama, memory-core default.
- `agntdata-x` is stale/missing per security/config warning.
- `active-memory` is installed/enabled as plugin entry but its internal config says `enabled: false`.

## Automation state

- Live cron scheduler list returned zero jobs.
- `openclaw status` reports Tasks: none.
- Heartbeat disabled: `every: 0m`.
- C runtime still contains old cron files and old run history under `C:\Users\ACER\.openclaw\cron`.
- C runtime tasks database exists and is much larger than E runtime tasks DB, indicating old task history remains on C.

## Security audit

Result:

- 0 critical
- 2 warnings
- 1 info

Warnings:

1. Reverse proxy headers are not trusted.
   - Current gateway bind is loopback, so this is only relevant if you expose the Control UI through a reverse proxy.
   - Fix: keep local-only or configure `gateway.trustedProxies`.

2. Some configured models are below recommended tiers.
   - `openai/gpt-4o-mini` appears in fallbacks.
   - Fix: remove weak fallback for tool-enabled/untrusted-inbox usage, or keep only for low-risk tasks.

Info:

- Attack surface: open groups 0, allowlist groups 2.
- Elevated tools enabled.
- Webhooks disabled.
- Browser control enabled.
- Trust model is personal assistant / trusted operator boundary.

## Main risks / inconsistencies

1. Migration is not fully finalized.
   - C still holds active-looking state, extensions, backups, cron history, and task DB.
   - E is active for current workspace/runtime, but C is still the service entrypoint and code source.

2. Codex ACP cwd still points to C workspace.
   - `agents.list[1].runtime.acp.cwd = C:\Users\ACER\.openclaw\workspace`.
   - If E is intended to be primary, this should likely be changed to E workspace.

3. Workspace path mismatch.
   - Launcher sets `E:\KY-DATA\OpenClaw\runtime-mirror\workspace`.
   - Active workspace is `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`.

4. Stale plugin config.
   - `agntdata-x` referenced but plugin not found.
   - Remove stale allow/entry or reinstall plugin.

5. C and E config divergence.
   - C config has newer `meta.lastTouchedAt` and includes `engram` memory slot config.
   - E active config differs and appears to use `memory-core` default.
   - Need decide which config is canonical before further changes.

6. Update available.
   - Installed/mirrored package is `2026.5.2`; latest reported by status is `2026.5.7`.

7. Bootstrap incomplete.
   - Current workspace still has `BOOTSTRAP.md`.
   - Agent identity/user identity files are not finalized.

## Recommended next steps

1. Decide canonical target: C stub + E runtime/code, or C code + E runtime only.
2. Back up both configs and runtime folders before modifying.
3. Fix E runtime/workspace path consistency.
4. Move/update Codex ACP cwd to E if E is primary.
5. Remove stale `agntdata-x` config or restore the plugin.
6. Decide memory backend: `memory-core`, `engram`, or disabled; avoid split state.
7. Run `openclaw update` only after backup and config cleanup.
8. Complete bootstrap identity files and remove `BOOTSTRAP.md`.
9. After migration is stable, archive old C runtime state rather than deleting it immediately.
