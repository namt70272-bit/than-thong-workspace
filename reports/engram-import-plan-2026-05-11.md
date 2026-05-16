# Engram review/import plan — 2026-05-11 01:53 GMT+7

## Scope snapshot
- Source: `G:\da xong\engram-memory-community-main`
- Size: ~1.31 MB
- Files: 174
- Dirs: 47

## Goal
Read and review the whole repo before copying anything into E for active use.

## Execution order

### Phase 1 — Inventory + freeze
1. Build a full file manifest.
2. Tag files by risk/type:
   - docs/config
   - runtime scripts
   - plugin/integration
   - docker/services
   - bundled state/data (`.engram/*`)
   - vendored code (`vendor/graphify/*`)
3. Treat `.engram/*` as sample/runtime state, not trusted production data.

### Phase 2 — Read all human-authored entry files first
Read in this order:
1. `README.md`
2. `README-community.md`
3. `docs/OPENCLAW_INTEGRATION.md`
4. `SKILL.md`
5. `IMPROVEMENTS.md`
6. `docs/ARCHITECTURE.md`
7. `docs/LIMITATIONS.md`
8. `docs/QUICK_START.md`
9. `bridge/README.md`
10. `context/README.md`
11. `vendor/graphify/README.md`
12. `vendor/graphify/UPSTREAM.md`

### Phase 3 — Review config and install surfaces
Must inspect before import:
1. `openclaw.plugin.json`
2. `plugin/openclaw.plugin.json`
3. `config/openclaw-config.json`
4. `scripts/install-plugin.sh`
5. `docker-compose.yml`
6. `config/docker-compose.yml`
7. `package.json`
8. `requirements.txt`
9. `bridge/pyproject.toml`
10. `packages/mcp-server-node/package.json`
11. `sdks/python/pyproject.toml`
12. `sdks/typescript/package.json`

### Phase 4 — Review executable code paths
Focus areas:
1. `plugin.py`
2. `src/index.ts`
3. `scripts/memory_store.py`
4. `scripts/memory_search.py`
5. `scripts/memory_*_wrapper.py`
6. `scripts/mcp_server.py`
7. `docker/all-in-one/*`
8. `docker/fastembed/*`
9. `docker/mcp/*`
10. `bridge/*.py`
11. `context/tools/*.py`
12. `packages/mcp-server-node/*`

### Phase 5 — Compatibility judgment for current OpenClaw
Check explicitly:
1. Does it require replacing current memory behavior or can it coexist?
2. Does it need Docker services on `6333`, `11435`, `8585`?
3. Does it introduce paid/cloud paths? (Cloud is optional; local-only preferred.)
4. Does it write into current OpenClaw config/plugins safely?
5. Does it rely on stale plugin conventions versus current OpenClaw 2026.5.2?

### Phase 6 — Safe import into E (only after review)
Target location recommendation:
- `E:\KY-DATA\OpenClaw\projects\engram-memory-community-main`

Import method:
1. Copy repo into E as a review candidate, not active plugin.
2. Do **not** enable plugin in active OpenClaw yet.
3. Strip or quarantine `.engram/` from imported copy unless we intentionally want its sample state.
4. Run isolated checks from the copied E version.
5. Only then decide whether to wire into active config.

## Current preliminary judgment
- Potentially useful: **yes**
- Best use path: **local-only memory/plugin experiment**
- Not ready for blind import: **correct**
- Biggest caution: it may overlap with current `memory-core`/active-memory behavior, and `.engram/*` should not be treated as trusted production state.
