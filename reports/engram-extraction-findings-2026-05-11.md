# Engram extraction findings — 2026-05-11 02:06 GMT+7

## Short map
- `docs/` — architecture, limits, OpenClaw integration
- `config/` — sample OpenClaw + compose config
- `plugin/` — newer OpenClaw plugin entry (`index.js`)
- `src/` — recall logic / plugin TS source
- `scripts/` — Python store/search/setup helpers
- `docker/` — all-in-one container + services
- `skills/openclaw/` — alternate OpenClaw packaging
- `.engram/` — persisted local state (quarantine)
- `vendor/graphify/` — vendored graph tool

## High-risk areas
1. `.engram/` — stateful cache/index/graph, không nhập thẳng.
2. `plugin/` + `src/index.ts` — đụng trực tiếp plugin hooks OpenClaw.
3. `scripts/install-plugin.sh` + `scripts/setup.sh` — script cài đặt/ghi config, Linux-first.
4. `config/openclaw-config.json` — có thể giẫm lên memory backend hiện tại.
5. Cloud path trong `plugin/index.js` — phải bỏ qua vì không đụng billing.

## Useful signals found
- Qdrant `6333` đang có mặt.
- FastEmbed `11435` đang có mặt và trả healthy.
- MCP/HTTP `8585` chưa lên.
- Repo có ít nhất 3 lớp tích hợp khác nhau: root plugin, `plugin/`, và `skills/openclaw/`.
- Plugin mới (`plugin/index.js`) có local-only mode nếu không set `apiKey`.

## What is worth extracting
### A. Documentation / rules
- `docs/OPENCLAW_INTEGRATION.md`
- `docs/ARCHITECTURE.md`
- `docs/LIMITATIONS.md`

### B. Minimal plugin surface to study further
- `plugin/index.js`
- `plugin/openclaw.plugin.json`

### C. Core local-memory logic worth reviewing before any use
- `src/index.ts`
- `src/recall/*`
- `plugin.py`
- `scripts/memory_store.py`
- `scripts/memory_search.py`
- `docker/all-in-one/*`

## What should NOT be imported into active E
- `.engram/*`
- `package-lock.json`, SDK lockfiles, egg-info
- `benchmarks/`, `examples/`, `assets/`, `.claude/`
- `vendor/graphify/*` unless graph feature becomes a real need
- `scripts/setup.sh` / `install-plugin.sh` as executable installers

## Minimal import strategy for E
1. Do **not** copy repo whole.
2. Create a candidate area in E, e.g. `E:\KY-DATA\OpenClaw\projects\engram-candidate\`.
3. Put only:
   - selected docs
   - one chosen plugin implementation (`plugin/` path preferred over duplicates)
   - selected recall logic files if truly needed
4. Keep `.engram/` and vendor code out of the candidate initially.
5. Adapt config as a patch, not a full replacement.

## Risks if wired directly right now
- overwrite/duplicate plugin surfaces
- replace current memory behavior unexpectedly
- drag in cloud/billing path by mistake
- import stale runtime state from `.engram/`
- run Linux/bash install steps that do not fit current Windows/OpenClaw layout
