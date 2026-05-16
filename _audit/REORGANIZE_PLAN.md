# Reorganization Plan: openclaw-system/

**Date:** 2026-05-16
**Status:** Plan only — no files moved
**Target root:** `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\openclaw-system\`

---

## Proposed Target Structure

```
openclaw-system/
├── apps/               # Agent core, browser, gateway, local services
├── configs/            # openclaw/, mcp/, browser/, docker/, env-templates/
├── tools/              # browser-use, playwright, local-scripts, scanners
├── workflows/          # web-browsing, file-management, research, content, daily
├── memory/             # rules, notes, system-map, long-term
├── data/               # input, output, cache, downloads, logs
├── docs/               # system docs
├── scripts/            # start, stop, audit, backup, healthcheck
└── _audit/             # audit reports
```

---

## 1. `apps/` — Agent Core, Browser, Gateway, Local Services

**Purpose:** Runtime application code — agents, plugins, gateway, MCP servers, local services that actively run.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `tools-internal/agent_mcp_server.py` | `openclaw-system/apps/mcp/agent_mcp_server.py` | MCP server |
| `tools-internal/mcp_client.py` | `openclaw-system/apps/mcp/mcp_client.py` | MCP client |
| `tools-internal/mcp_ecosystem.py` | `openclaw-system/apps/mcp/mcp_ecosystem.py` | MCP ecosystem |
| `tools-internal/mcp_enhanced_server.py` | `openclaw-system/apps/mcp/mcp_enhanced_server.py` | MCP enhanced |
| `tools-internal/mcp_llm_server.py` | `openclaw-system/apps/mcp/mcp_llm_server.py` | MCP LLM server |
| `tools-internal/mcp_memory_server.py` | `openclaw-system/apps/mcp/mcp_memory_server.py` | MCP memory server |
| `tools-internal/mcp_rag_server.py` | `openclaw-system/apps/mcp/mcp_rag_server.py` | MCP RAG server |
| `tools-internal/mcp_search_server.py` | `openclaw-system/apps/mcp/mcp_search_server.py` | MCP search server |
| `tools-internal/rag_engine.py` | `openclaw-system/apps/rag/rag_engine.py` | RAG engine |
| `tools-internal/agent_memory.py` | `openclaw-system/apps/agent/agent_memory.py` | Agent memory |
| `tools-internal/agent_search.py` | `openclaw-system/apps/agent/agent_search.py` | Agent search |
| `tools-internal/agent-memory/` | `openclaw-system/apps/agent/agent-memory/` | Agent memory store |
| `tools-internal/agent-memory-v2/` | `openclaw-system/apps/agent/agent-memory-v2/` | Agent memory v2 |
| `tools-internal/agent-search/` | `openclaw-system/apps/agent/agent-search/` | Agent search store |
| `tools-internal/service_discovery.py` | `openclaw-system/apps/services/service_discovery.py` | Service discovery |
| `tools-internal/api_gateway.py` | `openclaw-system/apps/gateway/api_gateway.py` | API gateway |
| `tools-internal/dashboard_web.py` | `openclaw-system/apps/dashboard/dashboard_web.py` | Web dashboard |
| `tools-internal/test_dashboard.py` | `openclaw-system/apps/dashboard/test_dashboard.py` | Dashboard test |
| `tools-internal/test_gateway.py` | `openclaw-system/apps/gateway/test_gateway.py` | Gateway test |
| `runtime-guard/than-thong-guard/` | `openclaw-system/apps/guards/than-thong-guard/` | Runtime guard |
| `tools-internal/start_mcp.bat` | `openclaw-system/apps/mcp/start_mcp.bat` | MCP startup script |
| `tools-internal/start_mcp_ecosystem.ps1` | `openclaw-system/apps/mcp/start_mcp_ecosystem.ps1` | MCP ecosystem start |

**Files that should NOT go here:**
- Config files (.env, .json policy files) → `configs/`
- Pure scripts/utilities (`.py` helpers without runtime component) → `tools/` or `scripts/`
- Reference documentation → `docs/` or `references/`
- Build/packaging code → stays in `packaging/` or separate
- Third-party extracted libraries → `tools/`

**Risks:**
- MCP servers have hardcoded relative paths (e.g., to `tools-internal/rag-data/`). Moving them would break internal references unless symlinks or env vars are updated.
- The `__pycache__/` dirs must be excluded from moves (re-generated).
- Runtime objects like `.lock`, `.vault.*` files have fixed paths; need env-var overrides.

**Safe order:**
1. Create `apps/mcp/`, `apps/agent/`, `apps/services/`, `apps/gateway/`, `apps/dashboard/`, `apps/guards/`
2. Copy MCP server files first (no cross-dependencies)
3. Copy agent memory/search files
4. Copy gateway/dashboard
5. Copy runtime guard
6. Update any internal import paths
7. Delete originals only after verification

---

## 2. `configs/` — OpenClaw, MCP, Browser, Docker, Env Templates

**Purpose:** All configuration files — environment, policy, constraints, templates.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `config/.env.rate-limit` | `openclaw-system/configs/env/.env.rate-limit` | Rate limit env |
| `config/.rate_limit_state.json` | `openclaw-system/configs/state/.rate_limit_state.json` | State file |
| `config/gcp-n8n-vertex-ai-key.json` | `openclaw-system/configs/secrets/gcp-n8n-vertex-ai-key.json` | GCP key |
| `config/prompts-template.yaml` | `openclaw-system/configs/prompts/prompts-template.yaml` | Prompt templates |
| `config/prompt-templates/` | `openclaw-system/configs/prompts/` | Prompt templates |
| `config/policy-templates/` | `openclaw-system/configs/policies/` | Policy templates |
| `config/rate-limit.ps1` | `openclaw-system/configs/scripts/rate-limit.ps1` | Rate limit setup |
| `.env` (if exists at root) | `openclaw-system/configs/env/.env` | Root env |
| `than-thong.spec` | `openclaw-system/configs/spec/than-thong.spec` | Spec file |
| `packaging/than-thong.spec` | `openclaw-system/configs/spec/packaging-than-thong.spec` | Packaging spec |
| `tools-internal/.env` | `openclaw-system/configs/env/.tools-internal.env` | Internal tools env |
| `tools-internal/.vault.json` | `openclaw-system/configs/secrets/.vault.json` | Vault config |
| `tools-internal/.vault.lock` | `openclaw-system/configs/secrets/.vault.lock` | Vault lock |
| `tools-internal/.vault_key` | `openclaw-system/configs/secrets/.vault_key` | Vault key |
| `tools-internal/policy/` | `openclaw-system/configs/policies/` | Billing/top policies |
| `tools-internal/README.md` | `openclaw-system/configs/docs/internal-README.md` | Or keep in tools dir |
| `tools-internal/registry.json` | `openclaw-system/configs/registry.json` | Internal tool registry |
| `.gitignore` | `openclaw-system/configs/git/.gitignore` | Git ignore |

**Files that should NOT go here:**
- Actual apps/services → `apps/`
- Scripts that execute actions → `scripts/`
- Generated/cache data → `data/`

**Risks:**
- `.vault.json`, `.vault.lock`, `.vault_key` are read by vault.py at fixed relative paths; must update vault.py load paths.
- `than-thong.spec` at root is referenced by `than-thong.cmd` — needs path update.

**Safe order:**
1. Create `configs/env/`, `configs/secrets/`, `configs/prompts/`, `configs/policies/`, `configs/spec/`
2. Copy env files (no active references)
3. Copy policy files
4. Copy prompt/spec files
5. Update vault.py and than-thong.cmd paths
6. Delete originals after verification

---

## 3. `tools/` — Browser-Use, Playwright, Local Scripts, Scanners

**Purpose:** Executable tools, utilities, scanners, and automation scripts used by the agent.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `scripts/browser.py` | `openclaw-system/tools/browser/browser.py` | Browser tool |
| `scripts/gpu-monitor.ps1` | `openclaw-system/tools/monitoring/gpu-monitor.ps1` | GPU monitor |
| `scripts/play_song.py` | `openclaw-system/tools/media/play_song.py` | Media player |
| `scripts/model_usage.py` | `openclaw-system/tools/analytics/model_usage.py` | Model usage |
| `scripts/test-gemini-api.py` | `openclaw-system/tools/test/gemini-api.py` | Test scripts |
| `scripts/test-gemini-key.py` | `openclaw-system/tools/test/gemini-key.py` | Test scripts |
| `scripts/test-gemini-openai-endpoint.py` | `openclaw-system/tools/test/gemini-openai.py` | Test |
| `scripts/test-vertex-ai-key.py` | `openclaw-system/tools/test/vertex-ai-key.py` | Test |
| `scripts/create-n8n-cred.py` | `openclaw-system/tools/n8n/create-cred.py` | n8n tools |
| `scripts/create-n8n-http-workflow.py` | `openclaw-system/tools/n8n/create-http-workflow.py` | n8n tools |
| `scripts/create-n8n-workflow.py` | `openclaw-system/tools/n8n/create-workflow.py` | n8n tools |
| `scripts/uninstall-apps.cmd` | `openclaw-system/tools/win/uninstall-apps.cmd` | Windows tools |
| `scripts/uninstall-apps.ps1` | `openclaw-system/tools/win/uninstall-apps.ps1` | Windows tools |
| `scripts/tmux/` | `openclaw-system/tools/tmux/` | Tmux helpers |
| `scripts/video/` | `openclaw-system/tools/video/` | Video tools |
| `scripts/whisper/` | `openclaw-system/tools/whisper/` | Whisper tools |
| `scripts/README.md` | `openclaw-system/tools/README.md` | Tool docs |
| `cleanup_voice.py` | `openclaw-system/tools/media/cleanup_voice.py` | Voice cleanup |
| `gemini-webhook.py` | `openclaw-system/tools/webhook/gemini-webhook.py` | Webhook |
| `run_tests.py` | `openclaw-system/tools/test/run_tests.py` | Test runner |

**Internal scripts (scanners, checkers, utilities):**

| Current Path | Target Path | Notes |
|---|---|---|
| `tools-internal/scripts/` (all .py/.ps1/.cmd) | `openclaw-system/tools/scripts/` | Core internal tools |
| `tools-internal/_*.py` files | `openclaw-system/tools/lib/` | Internal library modules |
| `tools-internal/__main__.py` | `openclaw-system/tools/lib/__main__.py` | Entry point |
| `tools-internal/_config.py` | `openclaw-system/tools/lib/_config.py` | Config helper |
| `tools-internal/_pyhelper.py` | `openclaw-system/tools/lib/_pyhelper.py` | Python helper |
| `tools-internal/protect/` | `openclaw-system/tools/security/` | Security scripts |
| `tools-internal/extracted-scripts/` | `openclaw-system/tools/extracted/` | Extracted 3rd-party |

**Files that should NOT go here:**
- Runtime apps/servers → `apps/`
- RAG/ML data → `data/`
- System startup/stop scripts → `scripts/`

**Risks:**
- `tools-internal/scripts/` files reference each other via relative imports (e.g., `from _config import...`). Moving them changes the import graph.
- `than_thong_console.py` and friends are invoked by `than-thong.cmd` at the root.
- `start_mcp.bat` and `start_mcp_ecosystem.ps1` might reference relative paths.

**Safe order:**
1. Create `tools/scripts/`, `tools/lib/`, `tools/browser/`, etc.
2. Move library modules first (`_*.py`)
3. Move scripts that depend on libs
4. Move standalone scripts
5. Update `than-thong.cmd` paths
6. Verify imports work, then delete originals

---

## 4. `workflows/` — Web Browsing, File Management, Research, Content, Daily

**Purpose:** Lobster workflow files, n8n workflow definitions, automation templates.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `examples/inbox-triage.lobster` | `openclaw-system/workflows/lobster/inbox-triage.lobster` | Lobster workflow |
| `examples/pr-intake.lobster` | `openclaw-system/workflows/lobster/pr-intake.lobster` | Lobster workflow |
| `examples/content-workflows/` | `openclaw-system/workflows/content/` | Content examples |
| `examples/automation/` | `openclaw-system/workflows/automation/` | Automation examples |
| `examples/code-review/` | `openclaw-system/workflows/code-review/` | Code review examples |
| `examples/document-templates/` | `openclaw-system/workflows/templates/` | Document templates |
| `expansion/imports/workflow-templates/` | `openclaw-system/workflows/templates/` | Workflow templates |

**Files that should NOT go here:**
- Reference/readme docs → `docs/`
- Report files → keep in `_audit/` or `docs/`

**Risks:**
- Low risk — these are mostly templates and examples. No active runtime depends on these paths.
- Lobster files may be referenced by agent setup configs.

**Safe order:**
1. Create `workflows/lobster/`, `workflows/content/`, `workflows/templates/`
2. Copy all lobster and example files
3. Copy workflow templates
4. Any time, low impact

---

## 5. `memory/` — Rules, Notes, System Map, Long-Term

**Purpose:** Curated memory, rules, system documentation, knowledge base. NOT daily logs (those stay under workspace root `memory/` or go into `data/`).

**Note:** The current `memory/` directory at workspace root contains daily memory snapshots and is already well-structured. This folder would hold *curated* system memory: rules, system maps, long-term reference.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| References from `references/` that are system-internal knowledge | `openclaw-system/memory/rules/` | Curated rules |
| New curated system-map files (to be created) | `openclaw-system/memory/system-map/` | System topology |
| `MEMORY.md` | `openclaw-system/memory/long-term/MEMORY.md` | Long-term memory |
| Refactored rules from `references/compliance/` | `openclaw-system/memory/rules/` | THAN-THONG-RULE.md etc |

**Files that should NOT go here:**
- Daily `memory/YYYY-MM-DD.md` files → keep at root `memory/`
- Third-party reference docs → `docs/`
- Raw audit data → `_audit/`

**Risks:**
- `MEMORY.md` is loaded by the agent at startup via AGENTS.md reference. Moving it requires updating AGENTS.md.
- The existing `memory/` directory name conflict: root-level `memory/` is for daily notes; this new `memory/` is curated. Might cause confusion.

**Safe order:**
1. Create `memory/rules/`, `memory/system-map/`, `memory/long-term/`
2. Copy curated references
3. Update AGENTS.md if MEMORY.md path changes
4. Keep daily memory at root — do NOT move it

---

## 6. `data/` — Input, Output, Cache, Downloads, Logs

**Purpose:** Runtime data, cache files, logs, SQLite databases, vector stores, uploaded/downloaded files.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `n8n-db2.sqlite` | `openclaw-system/data/db/n8n-db2.sqlite` | n8n SQLite DB |
| `tools-internal/rag-data/` | `openclaw-system/data/rag/` | RAG index + vectors |
| `tools-internal/records/` | `openclaw-system/data/records/` | Run records, logs |
| `tools-internal/reference-library/` | `openclaw-system/data/reference-library/` | Reference library data |
| `tools-internal/auth/` | `openclaw-system/data/auth/` | Auth token storage |
| `report/*.jsonl` | `openclaw-system/data/analytics/` | Analytics data |
| `reports/rate-limit-2026-05-12.jsonl` | `openclaw-system/data/analytics/rate-limit.jsonl` | Rate limit log |
| `reports/engram-file-manifest-2026-05-11.json` | `openclaw-system/data/manifests/engram-manifest.json` | Manifest |
| `reports/voicebox-api-spec.json` | `openclaw-system/data/api-specs/voicebox-api-spec.json` | API spec |
| `reports/automation-stack.json` | `openclaw-system/data/analytics/automation-stack.json` | Automation stack |
| `reports/*.jsonl` | `openclaw-system/data/analytics/` | Various JSONL data |
| `runner/_diag/*.log` | `openclaw-system/data/logs/runner/` | Runner logs |
| `%TMPDIR%` contents (JITI cache) | `openclaw-system/data/cache/jiti/` | JITI cache |

**Files that should NOT go here:**
- Application code → `apps/`
- Configuration → `configs/`
- Active scripts → `scripts/` or `tools/`
- Reports (markdown) → `docs/` or `_audit/`

**Risks:**
- `tools-internal/records/` is written to by multiple internal tools. Moving it requires updating all writer scripts.
- `n8n-db2.sqlite` is actively used by n8n; path change would break n8n config.
- `rag-data/` is loaded by `rag_engine.py` at runtime; must update load paths.
- `tools-internal/auth/tokens.json` and `users.json` are read by auth_system.py.

**Safe order:**
1. Create `data/rag/`, `data/records/`, `data/auth/`, `data/db/`, `data/logs/`, `data/cache/`, `data/reference-library/`
2. Copy static data first (reference-library)
3. Copy records (after checking no writer is actively running)
4. Copy auth data (security-sensitive — handle carefully)
5. Copy RAG data
6. Copy SQLite DB
7. Update all writer/reader scripts in `tools/`
8. Delete originals only after full verification

---

## 7. `docs/` — System Documentation

**Purpose:** All documentation, references, guides, reports (markdown). Mirrors/excludes `references/` for curated system docs.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `references/` (all subdirs) | `openclaw-system/docs/references/` | All reference docs |
| `reports/` (markdown files only) | `openclaw-system/docs/reports/` | Markdown reports |
| `reports/README.md` | `openclaw-system/docs/reports/README.md` | Reports index |
| `docs/` (any existing) | merge with target | |
| `QUICK-START.md` | `openclaw-system/docs/QUICK-START.md` | Quick start |
| `README.md` | `openclaw-system/docs/README.md` | Main readme |
| `CHANGES.md` | `openclaw-system/docs/CHANGES.md` | Changelog |
| `AUTOMATION.md` | `openclaw-system/docs/automation/AUTOMATION.md` | Automation |
| `DATA-STORE.md` | `openclaw-system/docs/DATA-STORE.md` | Data store docs |
| `DIRECTORY-MAP.md` | `openclaw-system/docs/DIRECTORY-MAP.md` | Directory map |
| `REFERENCE-INDEX.md` | `openclaw-system/docs/REFERENCE-INDEX.md` | Reference index |
| `SKILL-REGISTRY.md` | `openclaw-system/docs/skills/SKILL-REGISTRY.md` | Skill registry |
| `WORKSPACE.md` | `openclaw-system/docs/WORKSPACE.md` | Workspace docs |
| `AGENTS.md` | `openclaw-system/docs/AGENTS.md` | Agents guide |
| `SOUL.md` | `openclaw-system/docs/SOUL.md` | Soul doc |
| `TOOLS.md` | `openclaw-system/docs/TOOLS.md` | Tools guide |
| `USER.md` | `openclaw-system/docs/USER.md` | User guide |
| `IDENTITY.md` | `openclaw-system/docs/IDENTITY.md` | Identity |
| `progress.md` | `openclaw-system/docs/progress.md` | Progress |
| `task_plan.md` | `openclaw-system/docs/task_plan.md` | Task plan |
| `findings.md` | `openclaw-system/docs/findings.md` | Findings |
| `HEARTBEAT.md` | `openclaw-system/docs/HEARTBEAT.md` | Heartbeat config |
| `dot2-*.md` (all integration docs) | `openclaw-system/docs/integrations/` | Integration docs |
| `THAN-THONG-DEFAULT-BEHAVIOR.md` | `openclaw-system/docs/rules/than-thong-behavior.md` | Behavior doc |
| `expansion/README.md` | `openclaw-system/docs/expansion/README.md` | Expansion docs |
| `expansion/domains/` | `openclaw-system/docs/domains/` | Domain docs |
| `expansion/plans/` | `openclaw-system/docs/plans/` | Plans |
| `expansion/inventory/` | `openclaw-system/docs/inventory/` | Inventory docs |
| `skills/README.md` | `openclaw-system/docs/skills/README.md` | Skills index |
| `skills/SKILL-REGISTRY.md` | `openclaw-system/docs/skills/SKILL-REGISTRY.md` | Skill registry |
| `references/awesome-skills-catalog/` | `openclaw-system/docs/catalogs/awesome-skills-catalog/` | Skills catalog |

**Files that should NOT go here:**
- Code/scripts → `tools/` or `apps/`
- Config files → `configs/`
- Raw data → `data/`
- Active audit runs → `_audit/`

**Risks:**
- `than-thong.cmd` references `than-thong.spec` at root; spec moves to `configs/`.
- `AGENTS.md` is loaded by OpenClaw at startup; moving it requires updating config.
- `TOOLS.md`, `SOUL.md`, `USER.md`, `MEMORY.md` are loaded by AGENTS.md as project context. Moving them breaks the startup chain.
- `skills/` is where OpenClaw reads skills from — those SKILL.md files should stay in `skills/`.

**Critical constraint: DO NOT move `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `MEMORY.md` — these are loaded by OpenClaw at agent startup from hardcoded paths.**
- `skills/` directories must remain in `skills/` (OpenClaw loads skills from `~/.openclaw/workspace/skills/<name>/SKILL.md`).

**Safe order:**
1. Create `docs/references/`, `docs/reports/`, `docs/automation/`, etc.
2. Copy reference docs (read-only, no active path deps)
3. Copy reports
4. Copy integration docs (dot-2-*.md)
5. Copy expansion docs
6. Copy domain/plan docs
7. Verify no startup files were moved
8. Delete originals

---

## 8. `scripts/` — Start, Stop, Audit, Backup, Healthcheck

**Purpose:** Entry points for agent lifecycle — startup, shutdown, backup, healthcheck, daily maintenance.

**Files to move here:**

| Current Path | Target Path | Notes |
|---|---|---|
| `than-thong.cmd` | `openclaw-system/scripts/than-thong.cmd` | Main entry point |
| `tools-internal/scripts/watchdog_log.ps1` | `openclaw-system/scripts/health/watchdog_log.ps1` | Watchdog |
| `tools-internal/scripts/rollback.cmd` | `openclaw-system/scripts/maintenance/rollback.cmd` | Rollback |
| `managed-hooks/than-thong-startup/` | `openclaw-system/scripts/startup/than-thong-startup/` | Startup hook |
| `managed-hooks/than-thong-shutdown-guard/` | `openclaw-system/scripts/shutdown/than-thong-shutdown/` | Shutdown hook |
| `managed-hooks/than-thong-stop-logger/` | `openclaw-system/scripts/shutdown/than-thong-stop-logger/` | Stop logger |
| `managed-hooks/than-thong-oh-sync.ps1` | `openclaw-system/scripts/sync/oh-sync.ps1` | Sync script |
| `hooks/` (legacy hooks) | `openclaw-system/scripts/legacy-hooks/` | Legacy hooks |
| `packaging/build.bat` | `openclaw-system/scripts/build/build.bat` | Build script |
| `packaging/build.py` | `openclaw-system/scripts/build/build.py` | Build script |

**Files that should NOT go here:**
- Internal tool library scripts → `tools/`
- Config/spec files → `configs/`

**Risks:**
- `than-thong.cmd` at root is invoked by name. Moving it requires updating PATH or Alias.
- Hooks are installed by OpenClaw from `managed-hooks/<name>` directory; moving them breaks hook loading unless config is updated.
- `than-thong.cmd` references `than-thong.spec` at root.

**Safe order:**
1. Create `scripts/startup/`, `scripts/shutdown/`, `scripts/health/`, `scripts/sync/`, `scripts/build/`
2. Copy `than-thong.cmd` last (update internal spec path first)
3. Update PATH/alias for `than-thong.cmd`
4. Update hook config paths
5. Delete originals

---

## 9. `_audit/` — Audit Reports (stays in place or symlinked)

**Purpose:** Audit/tree/findings/reports from the workspace audit tool.

**Current status:** Already exists at `_audit/` at workspace root.

**Recommendation:** Keep `_audit/` where it is, or create a symlink at `openclaw-system/_audit/`. These are live working files for ongoing audits and should remain accessible.

**Files to keep:**
- `_audit/tree.txt` — directory tree
- `_audit/files.csv` — file inventory
- `_audit/important-files.csv` — important files
- `_audit/madge-*` — dependency graphs
- `_audit/docker-*` — Docker audit
- `_audit/process-summary.csv` — process summary
- `_audit/listening-ports.txt`
- `_audit/WORKFLOW_MAP.md`
- `_audit/openclaw-repomix.md`
- `_audit/REORGANIZE_PLAN.md` — this file

---

## Items NOT Covered by the Proposed Structure

The following items don't cleanly fit into the 9 folders and need special consideration:

### Root Docs (AGENTS.md, SOUL.md, etc.)
**Constraint:** These are loaded by OpenClaw at startup. **DO NOT MOVE.** They must stay at workspace root.

### `skills/` Directory
**Constraint:** OpenClaw scans `skills/<name>/SKILL.md` at startup. **DO NOT MOVE.** Keep at workspace root.

### `memory/` (Daily Memory)
Recommend keeping at workspace root. It's separate from the curated `openclaw-system/memory/`.

### `.github/` — CI/CD Workflows
Keep at root. GitHub Actions requires `.github/workflows/` at repo root.

### `packaging/` — Build/Package System
Could go to `openclaw-system/tools/build/` or stay as root dir. Low priority.

### `runner/` — GitHub Actions Runner
System service — keep at root. It's a standalone runner installation, not workspace code.

### `tests/` and `.pytest_cache` / `.ruff_cache`
Tests could go to `openclaw-system/tools/test/` or stay. Caches are auto-generated.

### `tmp/`
Temp files — should be cleaned, not reorganized.

### `models/` — Python ML Models
Could go to `openclaw-system/apps/models/` or `openclaw-system/tools/models/`.

### `archive/`
Archived/deprecated files — could go under `data/archive/`.

### `review/` and `khai-thac/`
Review system for skills — could go to `openclaw-system/tools/review/`.

---

## Summary of Safe Move Order

Recommended execution order (least risky first):

1. **`_audit/`** — Already in place, no-op
2. **`docs/`** — Copy-only, no code path dependencies
3. **`workflows/`** — Template files, no active references
4. **`configs/`** — Copy + update spec/vault paths
5. **`data/`** — Copy + update writer/reader paths (critical)
6. **`tools/`** — Copy + update import paths, cmd file (critical)
7. **`apps/`** — Copy + update internal paths (critical)
8. **`scripts/`** — Move last, after all path updates are verified
9. **Root config updates** — Update `than-thong.cmd`, AGENTS.md if needed

**Total original directories to reorganize:** ~25 top-level dirs → compressed into 8 folders
**Files not to move (~stay at root):** `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `MEMORY.md`, `IDENTITY.md`, `skills/`, `.github/`, `memory/`, `runner/`, `.gitignore`, `pyproject.toml`, `package.json` files, auto-generated caches
