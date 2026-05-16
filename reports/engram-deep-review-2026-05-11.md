# Engram deep review report — 2026-05-11

- Source: `G:\đã xong\engram-memory-community-main`
- Total files: **174**
- Total size: **1.31 MB**

## Classification summary

- aux: 36
- code: 38
- config: 2
- docs: 20
- integration: 7
- misc: 13
- runtime: 31
- state: 3
- vendor: 24

## Risk summary

- critical: 3
- high: 41
- medium: 62
- low: 68

## Top-level directory classification

- `.claude/` — 1 files · kinds={'aux': 1} · risks={'low': 1}
- `.engram/` — 3 files · kinds={'state': 3} · risks={'critical': 3}
- `.gitignore/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `IMPROVEMENTS.md/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `LICENSE/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `README-community.md/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `README.md/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `SKILL.md/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `assets/` — 2 files · kinds={'aux': 2} · risks={'low': 2}
- `benchmarks/` — 1 files · kinds={'aux': 1} · risks={'low': 1}
- `bin/` — 3 files · kinds={'aux': 3} · risks={'low': 3}
- `bridge/` — 15 files · kinds={'code': 15} · risks={'medium': 15}
- `config/` — 2 files · kinds={'config': 2} · risks={'high': 2}
- `context/` — 5 files · kinds={'code': 5} · risks={'medium': 5}
- `detect-arch.sh/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `docker/` — 16 files · kinds={'runtime': 16} · risks={'high': 16}
- `docker-compose.yml/` — 1 files · kinds={'misc': 1} · risks={'high': 1}
- `docs/` — 20 files · kinds={'docs': 20} · risks={'low': 20}
- `examples/` — 1 files · kinds={'aux': 1} · risks={'low': 1}
- `mcp/` — 1 files · kinds={'runtime': 1} · risks={'high': 1}
- `openclaw.plugin.json/` — 1 files · kinds={'integration': 1} · risks={'high': 1}
- `package-lock.json/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `package.json/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `packages/` — 8 files · kinds={'code': 8} · risks={'medium': 8}
- `plugin/` — 3 files · kinds={'integration': 3} · risks={'high': 3}
- `plugin.py/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `requirements.txt/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `scripts/` — 14 files · kinds={'runtime': 14} · risks={'high': 14}
- `sdks/` — 28 files · kinds={'aux': 28} · risks={'low': 28}
- `skills/` — 3 files · kinds={'integration': 3} · risks={'high': 3}
- `src/` — 10 files · kinds={'code': 10} · risks={'medium': 10}
- `tsconfig.json/` — 1 files · kinds={'misc': 1} · risks={'low': 1}
- `vendor/` — 24 files · kinds={'vendor': 24} · risks={'medium': 24}

## Critical / high-risk files or areas

- `.engram/graph.kuzu` — critical — state — runtime state/cache/index; stateful binary data
- `.engram/hash_index.pkl` — critical — state — runtime state/cache/index; stateful binary data
- `.engram/hot_tier.json` — critical — state — runtime state/cache/index
- `config/docker-compose.yml` — high — config — config surface; installer or orchestrator
- `config/openclaw-config.json` — high — config — config surface; installer or orchestrator
- `docker/all-in-one/Dockerfile` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/init.sh` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/fastembed/run` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/fastembed/type` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/init/type` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/init/up` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/mcp-server/dependencies.d/fastembed` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/mcp-server/dependencies.d/qdrant` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/mcp-server/run` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/mcp-server/type` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/qdrant/run` — high — runtime — runtime/install/entrypoint surface
- `docker/all-in-one/services.d/qdrant/type` — high — runtime — runtime/install/entrypoint surface
- `docker/fastembed/Dockerfile` — high — runtime — runtime/install/entrypoint surface
- `docker/fastembed/fastembed_service.py` — high — runtime — runtime/install/entrypoint surface
- `docker/mcp/Dockerfile` — high — runtime — runtime/install/entrypoint surface
- `docker/mcp/entrypoint.py` — high — runtime — runtime/install/entrypoint surface
- `docker-compose.yml` — high — misc — installer or orchestrator
- `mcp/server.py` — high — runtime — runtime/install/entrypoint surface
- `openclaw.plugin.json` — high — integration — plugin/integration surface
- `plugin/index.js` — high — integration — plugin/integration surface
- `plugin/openclaw.plugin.json` — high — integration — plugin/integration surface
- `plugin/package.json` — high — integration — plugin/integration surface
- `scripts/backfill_hash_index.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/engram_graph.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/export_memories_for_graph.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/fastembed_service.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/fastembed_setup.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/install-plugin.sh` — high — runtime — runtime/install/entrypoint surface; installer or orchestrator
- `scripts/mcp_server.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/memory_search.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/memory_search_wrapper.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/memory_store.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/memory_store_wrapper.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/migrate_collection.py` — high — runtime — runtime/install/entrypoint surface
- `scripts/setup-context.sh` — high — runtime — runtime/install/entrypoint surface
- `scripts/setup.sh` — high — runtime — runtime/install/entrypoint surface; installer or orchestrator
- `skills/openclaw/openclaw.plugin.json` — high — integration — plugin/integration surface
- `skills/openclaw/plugin.py` — high — integration — plugin/integration surface
- `skills/openclaw/SKILL.md` — high — integration — plugin/integration surface

## Candidate extraction classes

### Nên đọc và trích ý tưởng/quy tắc
- `README.md`
- `README-community.md`
- `docs/ARCHITECTURE.md`
- `docs/LIMITATIONS.md`
- `docs/OPENCLAW_INTEGRATION.md`
- `IMPROVEMENTS.md`
- `SKILL.md`

### Nên đọc kỹ nếu muốn tái dùng logic/plugin
- `plugin/index.js`
- `plugin/openclaw.plugin.json`
- `plugin/package.json`
- `src/index.ts`
- `src/recall/__init__.py`
- `src/recall/consolidation.py`
- `src/recall/graph_layer.py`
- `src/recall/hot_tier.py`
- `src/recall/matryoshka.py`
- `src/recall/models.py`
- `src/recall/multi_head_hasher.py`
- `src/recall/recall_engine.py`
- `src/recall/test_three_tiers.py`
- `scripts/memory_search.py`
- `scripts/memory_search_wrapper.py`
- `scripts/memory_store.py`
- `scripts/memory_store_wrapper.py`
- `docker/all-in-one/Dockerfile`
- `docker/all-in-one/init.sh`
- `docker/all-in-one/services.d/fastembed/run`
- `docker/all-in-one/services.d/fastembed/type`
- `docker/all-in-one/services.d/init/type`
- `docker/all-in-one/services.d/init/up`
- `docker/all-in-one/services.d/mcp-server/dependencies.d/fastembed`
- `docker/all-in-one/services.d/mcp-server/dependencies.d/qdrant`
- `docker/all-in-one/services.d/mcp-server/run`
- `docker/all-in-one/services.d/mcp-server/type`
- `docker/all-in-one/services.d/qdrant/run`
- `docker/all-in-one/services.d/qdrant/type`
- `config/openclaw-config.json`
- `skills/openclaw/openclaw.plugin.json`
- `skills/openclaw/plugin.py`
- `skills/openclaw/SKILL.md`

### Không nên nhập thẳng vào E
- `.claude/commands/graph.md`
- `.engram/graph.kuzu`
- `.engram/hash_index.pkl`
- `.engram/hot_tier.json`
- `assets/full-transparent.jpg`
- `assets/logo.svg`
- `benchmarks/longmemeval_bench.py`
- `examples/basic-usage.js`
- `package-lock.json`
- `packages/mcp-server-node/package-lock.json`
- `sdks/typescript/package-lock.json`
- `vendor/graphify/graphify/__init__.py`
- `vendor/graphify/graphify/__main__.py`
- `vendor/graphify/graphify/analyze.py`
- `vendor/graphify/graphify/benchmark.py`
- `vendor/graphify/graphify/build.py`
- `vendor/graphify/graphify/cache.py`
- `vendor/graphify/graphify/cluster.py`
- `vendor/graphify/graphify/detect.py`
- `vendor/graphify/graphify/export.py`
- `vendor/graphify/graphify/extract.py`
- `vendor/graphify/graphify/hooks.py`
- `vendor/graphify/graphify/ingest.py`
- `vendor/graphify/graphify/manifest.py`
- `vendor/graphify/graphify/report.py`
- `vendor/graphify/graphify/security.py`
- `vendor/graphify/graphify/serve.py`
- `vendor/graphify/graphify/transcribe.py`
- `vendor/graphify/graphify/validate.py`
- `vendor/graphify/graphify/watch.py`
- `vendor/graphify/graphify/wiki.py`
- `vendor/graphify/LICENSE`
- `vendor/graphify/pyproject.toml`
- `vendor/graphify/README.md`
- `vendor/graphify/UPSTREAM.md`

## Import strategy

1. Không copy nguyên repo.
2. Tạo candidate riêng trong E.
3. Chỉ trích docs + plugin path duy nhất + logic thật sự cần.
4. Bỏ `.engram/`, lockfiles, vendor, assets, examples khỏi candidate ban đầu.
5. Không chạy `setup.sh` hoặc `install-plugin.sh` trực tiếp trên máy đang chạy.
6. Nếu cần tích hợp, tạo patch config tối thiểu thay vì thay nguyên file.

## Notes from current environment

- Port `6333` có Qdrant trả lời.
- Port `11435` có FastEmbed trả lời healthy.
- Port `8585` chưa có MCP HTTP server.
- Repo chứa nhiều bề mặt tích hợp trùng chức năng (root/plugin/skills), cần chọn một đường duy nhất nếu tái dùng.