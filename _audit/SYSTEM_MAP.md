# SYSTEM MAP — OpenClaw Runtime Environment

**Generated:** 2026-05-16  
**Host:** DESKTOP-2R6S7IU (Windows 11 10.0.26200 x64)  
**Workspace Root:** `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`

---

## 1. Overview

OpenClaw is an AI agent runtime that runs locally on Windows. It provides a persistent agent session with tools, skills, memory, and infrastructure to automate tasks, manage workflows, and interact with Docker containers, LLMs (via Ollama), GitHub Actions runners, and n8n automation pipelines.

**What it does:**
- Runs a conversational AI agent (currently DeepSeek V4 Flash) with tool-calling support
- Maintains workspace identity, memory (daily notes + consolidation), and skill registry
- Orchestrates Docker containers for vector DB (Qdrant), proxy (Tinyproxy), automation (n8n), log viewer (Dozzle), container management (Portainer), and image processing (Python worker)
- Provides local-only tooling ("thần thông" / "top" system) for workspace management without billing risk
- Runs a self-hosted GitHub Actions runner for CI/CD workflows
- Hosts a local Ollama instance for LLM inference

---

## 2. Directory Structure Map

```
E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\
├── .github/workflows/       12 GitHub Actions workflow YAML files
├── .learnings/              Error and learning records
├── .openclaw/               Runtime workspace state
├── _audit/                  Audit data files (tree, docker, ports, processes)
├── archive/                 Deprecated content retained for reference
│   └── deprecated/tmp-scripts/  Old download scripts (Python + PowerShell)
├── config/                  YAML templates, rate-limiter state, GCP key
│   └── prompt-templates/    "Thần thông" prompt database files
├── examples/                .lobster workflow examples
├── expansion/               Import pipeline for reference knowledge
│   ├── candidates/          Reference knowledge candidates (80+ files)
│   ├── checklists/          Import checklist
│   ├── domains/             16 domain definitions
│   ├── import-map/          Import map
│   ├── inventory/           Master index + storage policy
│   ├── plans/               Upgrade plans
│   ├── queue/               Import queue
│   ├── rollback/            Rollback rules
│   └── sync/                Sync rules
├── hooks/                   Than-thong bootstrap + command guard hooks
├── khai-thac/               External source mining notes
├── managed-hooks/           Active managed hooks (bootstrap, command-guard, compact-guard, message-filter, shutdown-guard, startup, stop-logger)
├── memory/                  Daily logs + consolidated memories + index
├── models/                  Python classification + team config models
├── packaging/               Than-thong desktop packaging (tray, engine, router, etc.)
├── references/              Imported knowledge organized by domain
│   ├── agent-mesh/          Clawmesh, CCswitch
│   ├── agent-patterns/      Claude, OpenAI, Minimax, Hello Agent
│   ├── api-integration/     Auth0, Google Workspace, Resend, Azure, Venice
│   ├── automation/          n8n docs, lobster patterns, billing-wave1
│   ├── awesome-skills-catalog/  1100+ skill catalog (from VoltAgent)
│   ├── cli-patterns/        OpenCLI patterns
│   ├── code-management/     Coderabbit, OpenCode
│   ├── compliance/          Than-thong/top/billing rules, Trail of Bits
│   ├── content-management/  Community marketing
│   ├── device-control/      Browser, Expo, Fal.ai
│   ├── documentation/       Docs patterns
│   ├── himalaya/            Email client config
│   ├── infrastructure/      Cloudflare, Firebase, Netlify
│   ├── memory-knowledge/    HuggingFace, Notion, Vector DBs, DuckDB
│   ├── model-usage/         CodexBar CLI
│   ├── retrieval/           Brave, Spy patterns
│   ├── system-admin/        Redis, Sentry, Datadog, MongoDB
│   ├── work-management/     Clawteam, community productivity
│   └── workspace-governance/ Optimization reports (Vietnamese)
├── reports/                 18+ generated reports + automation stack JSON
├── review/                  Skill/ESKILL review pipeline
├── runner/                  Self-hosted GitHub Actions runner binary
│   ├── bin/                 Runner executables + check scripts
│   └── _work/               Workspace checkout + _actions cache
├── runtime-guard/           Than-thong guard plugin (TypeScript → JS)
├── scripts/                 Utility scripts (model usage, n8n, browser, audio, GPU monitor)
├── skills/                  ~40 formal skill definitions
├── tests/                   Python test suite
├── tools-internal/          Internal tooling (import, validate, sync, rollback)
│   ├── agent-memory-v2/     Agent memory metadata
│   ├── auth/                Token/user store (currently empty)
│   ├── extracted-scripts/   Extracted knowledge (gov data APIs, finance, MCP, claw-code)
│   └── scripts/             Operational scripts (40+ Python tools)
├── utils/                   Python helpers (rate_limiter, prompt_utils)
└── Root .md files           20+ root docs (AGENTS.md, SOUL.md, TOOLS.md, etc.)
```

---

## 3. Docker Containers

### Running Containers (6)

| Container | Image | Status | Ports | Purpose |
|-----------|-------|--------|-------|---------|
| **qdrant** | qdrant/qdrant:latest | Up 20 min | 6333-6334 | Vector database for embeddings/semantic search |
| **openclaw-tinyproxy** | vimagick/tinyproxy:latest | Up 2h | 1080→8888 | HTTP proxy for outbound traffic |
| **n8n-pro** | n8nio/n8n:latest | Restarting (49s ago) | n/a | Workflow automation (currently restarting) |
| **dozzle** | amir20/dozzle:latest | Up 2h | 8888→8080 | Realtime Docker log viewer |
| **portainer** | portainer/portainer-ce:latest | Up 2h | 9000 | Docker container management UI |
| **image-python-worker** | 099b4b70198b (custom) | Exited(255) 2h ago | 8000 | Image processing Python worker |

**Note:** n8n was started 6h ago and has been restarting. image-python-worker exited with code 255.

### Available Images (11 total)

- qdrant/qdrant:latest (275MB)
- n8nio/n8n:latest (2.27GB — largest)
- portainer/portainer-ce:latest (242MB)
- amir20/dozzle:latest (89.4MB)
- vimagick/tinyproxy:latest (9.32MB — smallest)
- alpine:latest (13.1MB)
- python:3.11-slim (188MB)
- postgres:16-alpine (396MB)
- n8n-pipeline-python-worker:latest (1.34GB)
- ghcr.io/langfuse/langfuse:latest (1.37GB)
- custom image 099b4b70198b (for image-python-worker)

### Docker Networks

| Network | Driver | Scope |
|---------|--------|-------|
| bridge | bridge | local (default) |
| host | host | local |
| none | null | local |
| openclaw-proxy | bridge | local |

### Docker Volumes

- `3140644b5045b91cb824c8398b4092eb0e0eb80954051b8d7038faa67e1bf6656` (anonymous, local driver)
- `n8n_data` (named, local driver)

---

## 4. Port Map

### Notable Listening Ports

| Port | Service | PID | Notes |
|------|---------|-----|-------|
| 80 | HTTP | 4 | Windows HTTP stack |
| 8000 | image-python-worker | 19888 | Python worker (container, exited) |
| 8080 | n8n-internal | 14864 | n8n web UI (127.0.0.1 only) |
| 8888 | dozzle | 19888 | Docker log viewer |
| 9000 | portainer | 19888 | Docker management UI |
| 6333 | qdrant gRPC | 19888 | Vector DB gRPC |
| 6334 | qdrant HTTP | 19888 | Vector DB REST |
| 1080 | tinyproxy | 19888 | HTTP proxy (mapped) |
| 11434 | Ollama | 26600 | Local LLM inference |
| 7680 | Windows Update | 19428 | Delivery Optimization |
| 15100-15101 | Ollama API | 12048 | Ollama endpoints |
| 49664-49673 | Ephemeral RPC | various | Windows dynamic ports |
| 1801, 2103, 2105, 2107 | MSMQ | 6868 | Message Queuing |
| 135, 445 | RPC/SMB | 1804/4 | Windows core services |
| 902 | VMWare | 7148 | VMWare Workstation |
| 912 | VMWare | 7148 | VMWare WS web |
| 9001 | n8n webhook | 17816 | (127.0.0.1 only) |
| 9876-9880 | Python workers | 15884-16928 | Multiple Python processes |
| 10089 | Unknown | 20456 | (127.0.0.1 only) |
| 18789 | Unknown | 24252 | (127.0.0.1 only) |
| 60894 | Unknown | 21400 | (127.0.0.1 only) |
| 64332 | Unknown | 12676 | (127.0.0.1 only) |
| 24642 | Unknown | 19772 | (127.0.0.1 only) |

**Note:** Ports 7,9,13,17,19 are standard Windows echo/daytime/quote services (PID 5212).

---

## 5. Key Processes

| Process | PID | CPU(s) | Mem(MB) | Role |
|---------|-----|--------|---------|------|
| node | 24252 | 584.9 | 737.3 | **OpenClaw agent runtime** (highest CPU/mem) |
| ollama | 26600 | 21.3 | 158.7 | Local LLM server |
| ollama app | 12676 | 15.4 | 34.2 | Ollama desktop tray |
| Docker Desktop | 4808+6052+9464+24008 | 79.2 | 377.1 | Docker management suite |
| com.docker.backend | 19888+22860 | 60.2 | 234.0 | Docker backend + port proxy |
| docker-agent | 436 | 0.6 | 40.8 | Docker agent |
| python | 14864 | 13.6 | 14.4 | Python worker (n8n webhook?) |
| python | 15884 | 15.7 | 17.7 | Python worker |
| python | 15948 | 15.3 | 20.0 | Python worker |
| python | 16492 | 15.7 | 18.9 | Python worker |
| python | 16928 | 25.8 | 214.1 | Python worker (largest mem) |
| python | 17336 | 15.5 | 17.7 | Python worker |
| python | 17816 | 14.3 | 14.5 | Python worker |
| docker-sandbox | 12064 | 0 | 14.3 | Docker sandbox |
| docker.build | 19912 | 0.9 | 37.0 | Docker build process |

---

## 6. Configuration Files Found

### GitHub Workflows (12 total — see Section 7)

### Key Config Files

| File | Purpose |
|------|---------|
| `config/prompts-template.yaml` | 10 LLM prompt templates |
| `config/prompt-templates/*.md` | "Thần thông" prompt database |
| `config/.rate_limit_state.json` | Rate limiter state |
| `config/rate-limit.ps1` | Rate limit PowerShell script |
| `config/gcp-n8n-vertex-ai-key.json` | GCP service account key for Vertex AI |
| `expansion/README.md` | Import pipeline documentation |
| `expansion/checklists/IMPORT-CHECKLIST.md` | Import checklist |
| `expansion/queue/IMPORT-QUEUE.md` | Import queue |
| `expansion/import-map/IMPORT-MAP.md` | Import domain mapping |
| `expansion/sync/SYNC-RULES.md` | Sync rules |
| `expansion/rollback/ROLLBACK-RULES.md` | Rollback rules |
| `references/compliance/THAN-THONG-RULE.md` | "Thần thông" operating rules |
| `references/compliance/BILLING-RULE.md` | Billing guard rules |
| `references/compliance/THAN-THONG-SUPER-POLICY.md` | Super policy |
| `hooks/than-thong-bootstrap/` | Bootstrap hook (TypeScript) |
| `hooks/than-thong-command-guard/` | Command guard hook (TypeScript) |
| `managed-hooks/*/` | 7 active managed hooks (bootstrap, guard, message filter, etc.) |
| `runtime-guard/than-thong-guard/` | Runtime guard plugin (TypeScript → JS) |
| `packaging/than_thong/` | Desktop tray packaging (Python) |

---

## 7. Workflows Summary (12 GitHub Actions)

| Workflow File | Trigger | Purpose |
|---------------|---------|---------|
| `auto-backup.yml` | Push + dispatch | Auto-backup workspace |
| `auto-fix.yml` | PR + dispatch | Auto-fix lint/style issues |
| `auto-review.yml` | PR + dispatch | Full AI review: tests, ruff check, AI comment |
| `deploy.yml` | Push master + dispatch | Deploy: tests + syntax check + git pull |
| `health-check.yml` | Daily cron (7AM) + dispatch | Health: syntax checks, pip check, runner service |
| `issue-handler.yml` | Issues + dispatch | Issue triage automation |
| `pip-check.yml` | Push (pip files) + dispatch | Validate pip dependencies |
| `pr-review.yml` | PR + dispatch | PR review automation |
| `release.yml` | Release + dispatch | Release tagging |
| `skill-check.yml` | Push (skills) + dispatch | Validate skill definitions |
| `test.yml` | PR + push + dispatch | Run pytest suite |
| `wiki-sync.yml` | Push (wiki) + dispatch | Wiki sync |

**Notable:** All workflows use `self-hosted` runner (GitHub Actions Runner installed locally at `runner/bin/`).

---

## 8. Strengths

1. **Rich local infrastructure:** Docker-based services (vector DB, proxy, automation, monitoring) provide a complete local AI + automation stack.
2. **Local-first philosophy:** "Thần thông" rule ensures billing-safe operation; most tools work without internet.
3. **Extensive skill ecosystem:** ~40 formal skills covering analytics, automation, code, communication, security, smart-home, media, and more.
4. **Comprehensive reference library:** 80+ imported reference documents across 16 domains (agent patterns, API integration, compliance, infrastructure, etc.)
5. **Self-hosted CI/CD:** GitHub Actions runner enables local execution of 12 workflows without external cloud runners.
6. **Memory system:** Daily notes + consolidation + indexing provides session-to-session continuity.
7. **Hook architecture:** Boot-time and runtime hooks (bootstrap, command guard, message filter, shutdown guard) enable policy enforcement.
8. **Full import pipeline:** Build → validate → sync → rollback chain for safe knowledge import.
9. **Packaging:** Desktop tray application ("Thần thông") for Windows-native interaction.

---

## 9. Weaknesses / Messy Areas

1. **n8n in restarting state:** The n8n container (`n8n-pro`) is stuck in a restart loop — it started 6h ago and has been restarting at least once. This means automation workflows aren't running.
2. **image-python-worker exited:** Custom Python worker container exited with code 255 (likely config/startup error). Image processing capability is offline.
3. **High node.exe CPU:** The `node` process (OpenClaw runtime) uses 585 CPU seconds and 737MB RAM — likely needs optimization or indicates heavy model/agent load.
4. **Multiple anonymous Python workers:** 7 Python processes running with similar CPU profiles; unclear separation of concerns or cleanup strategy.
5. **Docker Desktop overhead:** 5 Docker Desktop processes consuming ~400MB RAM combined.
6. **Expansion pipeline incomplete:** `expansion/candidates/` contains 80+ reference candidates but import status is unclear (no completion tracking per candidate).
7. **Deprecated scripts in archive:** 8+ old download scripts in `archive/deprecated/` — unclear if fully superseded.
8. **Hooks in two locations:** Both `hooks/` and `managed-hooks/` contain similar hook definitions — likely migration incomplete.
9. **Large files:** `reports/voicebox-api-spec.json` (208KB), `review/ESKILL-DEEP-READ.md` (349KB), `expansion/candidates/references/than-thong-477-safe-skills-index.md` (606KB) — bloating workspace.
10. **Runner binary footprint:** GitHub Actions runner (`runner/bin/`) is a heavy artifact (~135MB+ for the checkout v4 action dist alone).
11. **auth/tokens.json and auth/users.json are empty:** Auth infrastructure exists but is unused.
12. **Ollama running on port 11434:** Potential concern if port is exposed; should ensure local-only binding.

---

## 10. Recommendations

### Immediate
1. **Fix n8n container:** Investigate why `n8n-pro` keeps restarting (likely config/environment issue). Check volumes and env vars.
2. **Diagnose image-python-worker:** Fix exit code 255 (check Dockerfile CMD, entry point script, or missing dependencies).
3. **Reduce node.exe overhead:** Profile the OpenClaw runtime for memory leaks or excessive CPU; consider if model loading can be deferred.
4. **Consolidate hook folders:** Migrate remaining `hooks/` content into `managed-hooks/` to avoid duplication.

### Short-term
5. **Clean up archive:** Assess which `archive/deprecated/` scripts can be safely removed vs. kept for reference.
6. **Prune large files:** Move the 600KB skills index and 350KB deep-read file out of workspace root or compress.
7. **Track import progress:** Add completion status to each candidate file in `expansion/candidates/`.
8. **Document Python workers:** Clarify ownership and purpose of the 7+ Python processes.
9. **Secure Ollama:** Ensure Ollama binds to 127.0.0.1 only; currently it also listens on 0.0.0.0:11434.

### Medium-term
10. **Docker image optimization:** n8n image is 2.27GB — consider multi-stage builds or Alpine variants.
11. **Auth hardening:** Populate or remove the empty `auth/` infrastructure.
12. **Runner cleanup:** The `_actions/checkout` directory can be cleaned; it's a vendored copy of the `actions/checkout@v4` GitHub Action.
13. **Monitor disk usage:** With multiple Docker images (total ~6.5GB+), runner artifacts, and node_modules patterns, disk space should be tracked.
14. **Backup strategy:** Ensure critical config (prompts, rules, hooks) is backed up separately from runtime state.
