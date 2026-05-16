# OpenClaw System — Master Summary

**Date:** 2026-05-16 20:30 GMT+7  
**Scope:** Full system audit: 8,638 files, 382 directories, 1.4 GB  
**Method:** Read-only scan. No files modified.

---

## 1. System Overview

Hệ thống OpenClaw hiện tại là một **AI orchestrator platform** chạy local, kết nối với GitHub CI/CD, có:

| Thành phần | Chi tiết |
|---|---|
| **Agent core** | DeepSeek V4 Flash (cloud), tự trị qua thần thông |
| **Local LLM** | Ollama (3 models: bge-m3, gemma3:1b, qwen2.5-coder:7b) |
| **Vector DB** | Qdrant v1.18.0 (Docker, 89 documents indexed) |
| **CI/CD** | GitHub Actions + self-hosted Windows runner |
| **Docker** | 6 containers (5 running), 9 images |
| **Services** | Portainer (UI), Dozzle (logs), Tinyproxy (proxy) |
| **Scripts** | 66+ Python scripts trong tools-internal/ |
| **Tests** | pytest 9.0.3, 13 unit tests |

## 2. Tools & Capabilities

| Tool | Status | Purpose |
|---|---|---|
| Ruff | ✅ Installed 0.15.13 | Python linter |
| Repomix | ✅ Ran | Codebase bundler (4,195 files → 9.8M tokens) |
| Madge | ✅ Ran | JS dependency graph |
| Trivy | ⏳ Pulling | Container/filesystem security scan |
| Gitleaks | ⏳ Pulling | Secret/token leak detection |
| Syft | ⏳ Pulling | SBOM generation |
| Grype | ⏳ Pulling | Vulnerability scanning |

## 3. Important Files & Folders

| Path | Type | Purpose |
|---|---|---|
| `tools-internal/scripts/` (65 files) | Core | Thần thông toolchain |
| `.github/workflows/` (12 files) | CI/CD | GitHub Actions pipelines |
| `runner/` | Runner | Self-hosted GitHub runner (has secrets!) |
| `memory/` (10 files) | Data | Daily notes + INDEX |
| `MEMORY.md` | Config | Long-term memory |
| `config/` | Config | OpenClaw + prompts |

## 4. Docker Landscape

| Container | Status | Ports | Purpose |
|---|---|---|---|
| **qdrant** | ✅ Running | 6333-6334 | Vector search |
| **portainer** | ✅ Running | 9000 | Docker UI |
| **dozzle** | ✅ Running | 8888 | Log viewer |
| **openclaw-tinyproxy** | ✅ Running | 1080 | HTTP proxy |
| **n8n-pro** | ❌ Restarting | — | Workflow automation (broken) |
| **image-python-worker** | ❌ Exited | — | ML worker |

## 5. Port Summary

| Port | Service | Risk |
|---|---|---|
| 6333-6334 | Qdrant API | LOW (local only) |
| 11434 | Ollama API | LOW (local only) |
| 8888 | Dozzle logs | LOW (local only) |
| 9000 | Portainer | LOW (needs auth) |
| 1080 | Tinyproxy | MEDIUM (outbound proxy) |
| 80 | Windows HTTP | LOW (system) |

## 6. Security Issues Found

### 🔴 CRITICAL
1. **Hardcoded Gemini API key** trong 4 scripts (`scripts/test-gemini-*.py`)
2. **GCP service account key** trong file JSON (`config/gcp-n8n-vertex-ai-key.json`)
3. **Runner credentials** trong `runner/.credentials` — cần .gitignore xác nhận

### 🟡 MEDIUM
1. PostHog telemetry key trong `reference-library/mem0/telemetry.py`
2. Runner diagnostics logs (~30 files) có thể chứa credential
3. Elevated exec từ webchat không chặn

### 🟢 LOW
1. Docker không có DB port mở
2. OpenClaw engine configs dùng token tự động (không hardcode)

## 7. Top 5 Things to Do Now

| # | Việc | Lý do |
|---|---|---|
| 1 | **Xóa/safe-clean** các file chứa API key thật | CRITICAL: Gemini key + GCP key trong cleartext |
| 2 | **Template hóa** secret ra `.env.template` | Tránh secret lộ qua git trong tương lai |
| 3 | **Kiểm tra .gitignore** có exclude `runner/` chưa | Runner credentials là OAuth token |
| 4 | **Fix n8n container** restart loop | Nếu không dùng, dọn dẹp image ~2.27GB |
| 5 | **Thêm docker-compose.yml** | Reproducible service setup |

## 8. What NOT to Do

- ❌ Không xóa file thủ công nếu chưa backup git
- ❌ Không expose Portainer/Dozzle ra internet
- ❌ Không tự động push secret lên GitHub
- ❌ Không chạy containers với `--privileged`
- ❌ Không hardcode token mới vào source code

## 9. Overall Assessment

**Độ ổn định:** 🟡 Trung bình—nhiều thành phần chạy tốt (agent, Docker, CI/CD) nhưng có secret lộ và n8n hỏng.

**Độ rối:** 🟡 Trung bình—cấu trúc tools-internal/ khá rõ ràng, nhưng scripts/ thư mục gốc lẫn tạp (test scripts chứa secret).

**Hướng tổ chức:** Gom các scripts test + config có secret vào thư mục riêng, tách biệt khỏi toolchain chính.

**Rủi ro lớn nhất:** **Secret trong source code** (Gemini key + GCP key) — ưu tiên số 1.
