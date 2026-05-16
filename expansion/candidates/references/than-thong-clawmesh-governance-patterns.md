# Claw-Mesh / Claw-Grid: Distributed Agent Governance Patterns

> Nguồn: G:\Ai\Claw-Mesh.zip  
> Trích xuất: thần thông, mảng 04 - Tổ chức tri thức  
> Ngày: 2026-05-13

## 1. CPC Governance Model (3-tier)
```
Constitutional Layer → Immutable rules (resource limits, safety boundaries)
Policy Layer → Configurable policies (model routing, cost caps, trust thresholds)
Control Layer → Runtime enforcement (sentinel monitoring, circuit breakers, auto-healing)
```

## 2. 4-Layer Architecture
| Layer | Name | Technology |
|---|---|---|
| L1 | Command | Agent orchestration, task decomposition, routing |
| L2 | Node | Multi-node, 14 agent roles, CPC governance |
| L3 | Data | PostgreSQL aggregation, Signal, Mesh SDN |
| L4 | Execution | Container agents, parallel dispatch, trust scoring |

## 3. Agent Role Structure (14 roles)
Lưu tại `governance/roles/`, các vai trò được định nghĩa với handoff protocols và failure domains.

## 4. Governance Components
- `governance/` — roles, policies, runbooks, SLOs
- `sentinel/` — Python monitoring scripts
- `spec/ts-governance/` — TypeScript formal spec (future)
- `fsc/` — Full Self Coding worker daemon

## 5. Ontology Graph (error → fix)
Từ `.mem/ontology/graph.jsonl`:
- Entities: error_type, fix_type, error, fix
- Relations: fixes (with confidence scoring 0.85-0.93)
- Memory of known patterns: OOM → increase memory, connection refused → restart service

## 6. Tech Stack
- Runtime: Bun/TypeScript + Python sentinel
- Messaging: Redis 7 Streams
- DB: PostgreSQL (signals), DuckDB (analytics)
- Network: NetBird mesh SDN + SSH fallback
- Models: MiniMax/Doubao (workers), Claude (orchestration only)
- Agents: Docker <200MB per agent
