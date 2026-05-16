# Kế hoạch nâng cấp OpenClaw

**Ngày:** 2026-05-16 20:43 GMT+7
**Nguồn:** Tổng hợp từ MASTER_SUMMARY, SECURITY_CHECKLIST, UPGRADE_CONTEXT, UPGRADE_ROADMAP, UPGRADE_TASKS, REORGANIZE_PLAN

---

## 1. Tình trạng hiện tại

Hệ thống OpenClaw là một **AI orchestrator platform** chạy local kết nối GitHub CI/CD:

| Thành phần | Chi tiết |
|---|---|
| **Agent core** | DeepSeek V4 Flash (cloud) + thần thông gate |
| **Local LLM** | Ollama (3 models: bge-m3, gemma3:1b, qwen2.5-coder:7b) |
| **Vector DB** | Qdrant v1.18.0 (Docker, 89 documents indexed) |
| **CI/CD** | GitHub Actions + self-hosted Windows runner (12 workflows) |
| **Docker** | 6 containers (5 running), 9 images (~6GB) |
| **Scripts** | 66+ Python scripts trong tools-internal/ |
| **Tests** | pytest 9.0.3, 13 unit tests |
| **Tổng quan** | 8,638 files, 382 directories, 1.4 GB |

**Độ ổn định:** 🟡 Trung bình
**Độ rối:** 🟡 Trung bình

---

## 2. Vấn đề nghiêm trọng nhất

| # | Vấn đề | Mức | Hậu quả |
|---|---|---|---|
| 1 | **Gemini API key hardcode** trong 4 scripts | 🔴 CRITICAL | Key lộ → unauthorized usage, billing risk |
| 2 | **GCP service account private key** trong workspace | 🔴 CRITICAL | Full GCP project access nếu bị lộ |
| 3 | **Elevated exec wildcard** trên webchat (`"*"`) | 🔴 CRITICAL | Ai vào webchat cũng có quyền admin |
| 4 | **Runner credentials (.credentials)** trong workspace | 🟡 MEDIUM | OAuth token lộ nếu commit git |
| 5 | **Cấu trúc thư mục lẫn lộn** | 🟡 MEDIUM | scripts/, tools-internal/ trộn tool + test + ref |
| 6 | **n8n container restart loop** | 🟡 MEDIUM | Chiếm 2.27GB image không dùng được |
| 7 | **PostHog telemetry key** trong reference-library | 🟡 MEDIUM | Phone-home nếu code được import |
| 8 | **Không docker-compose.yml** | 🟢 LOW | Services chạy thủ công, không reproducible |
| 9 | **Unpinned npm plugin spec** | 🟡 MEDIUM | Supply-chain risk |

### Rủi ro tổng thể

**Rủi ro lớn nhất: Secret trong source code** — 2 CRITICAL exposure (Gemini key + GCP key) và elevated exec wildcard cần xử lý ngay lập tức.

---

## 3. Mục tiêu nâng cấp

1. **🔴 Bảo mật** — Xóa secret khỏi source code, dùng env var, xóa elevated wildcard
2. **🟡 Cấu trúc** — Gom tool/config/workflow vào thư mục chuẩn (openclaw-system/)
3. **🟡 Vận hành** — Healthcheck + backup + audit script
4. **🟢 Tài liệu** — Operating guide, system map đầy đủ
5. **🟢 Docker** — docker-compose.yml, dọn image không dùng

**Nguyên tắc:** Local-first, auth-first, không billing. Mọi thay đổi đều phải backup git trước.

---

## 4. Kiến trúc đề xuất

### Cấu trúc thư mục mục tiêu

```
openclaw-system/          # Thư mục chính
├── apps/                 # Agent core, gateway, MCP servers, dashboard
├── configs/              # env, mcp, browser, docker, policies, prompts
├── tools/                # browser-use, local-scripts, scanners, test tools
├── workflows/            # Lobster, n8n templates
├── memory/               # Rules, system-map, long-term (curated)
├── data/                 # RAG, db, records, cache, logs, reference-library
├── docs/                 # System docs, references, reports, catalogs
└── scripts/              # start, stop, audit, backup, healthcheck
```

### Các file KHÔNG được di chuyển

- `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `MEMORY.md`, `IDENTITY.md` — OpenClaw startup chain
- `skills/` — OpenClaw quét thư mục này để load SKILL.md
- `memory/` (daily notes) — Giữ nguyên tại root
- `.github/` — GitHub Actions yêu cầu tại repo root
- `runner/` — Self-hosted runner, giữ nguyên

---

## 5. Việc cần làm ngay (5 items)

### 🔴 Item 1: Xử lý Gemini API key lộ
- **Lý do:** Key hardcode trong 4 scripts (test-gemini-key.py, create-n8n-cred.py, create-n8n-http-workflow.py, test-gemini-openai-endpoint.py)
- **Hành động:** User revoke key trên Google AI Studio → tạo key mới → thay bằng env var
- **Backup cần:** Git commit trước khi sửa
- **File liên quan:** scripts/test-gemini-key.py, scripts/create-n8n-cred.py, scripts/create-n8n-http-workflow.py, scripts/test-gemini-openai-endpoint.py, gemini-webhook.py

### 🔴 Item 2: Xử lý GCP service account key
- **Lý do:** Full GCP private key trong config/gcp-n8n-vertex-ai-key.json
- **Hành động:** User revoke key trên GCP Console → copy backup ra ngoài → xóa file khỏi workspace
- **Backup cần:** Copy ra ngoài workspace trước khi xóa
- **File liên quan:** config/gcp-n8n-vertex-ai-key.json

### 🔴 Item 3: Xóa elevated exec wildcard
- **Lý do:** `tools.elevated.allowFrom.webchat: ["*"]` — bất kỳ ai vào webchat cũng có quyền admin
- **Hành động:** Đọc config hiện tại → backup → sửa thành `[]` hoặc specific user ID → restart gateway
- **Backup cần:** Backup gateway config trước khi sửa
- **File liên quan:** OpenClaw gateway.yaml (chưa xác định vị trí chính xác)

### 🟡 Item 4: Bảo vệ runner credentials khỏi git
- **Lý do:** runner/.credentials + runner/_diag/*.log chứa OAuth config
- **Hành động:** Thêm runner/ vào .gitignore (kiểm tra đã có chưa)
- **Backup cần:** Hỏi trước khi sửa .gitignore
- **File liên quan:** .gitignore

### 🟡 Item 5: Thêm _audit/ vào .gitignore
- **Lý do:** Report nhạy cảm có thể commit lên git
- **Hành động:** Thêm _audit/ vào .gitignore
- **Backup cần:** Hỏi trước khi sửa .gitignore

---

## 6. Việc cần tôi xác nhận (5 items)

> **Hướng dẫn:** Trả lời từng item bằng **Có/Không/Tôi sẽ tự làm**. Nếu trả lời, tôi sẽ thực hiện các bước an toàn theo đúng kế hoạch.

### Item A: Xác nhận revoke Gemini API key
- Bạn vào https://aistudio.google.com/app/apikey → revoke key cũ → tạo key mới
- **Cần bạn:** Thực hiện thao tác trên dashboard Google
- **Sau đó:** Tôi thay hardcoded key → env var trong 5 scripts

### Item B: Xác nhận revoke GCP service account key
- Bạn vào GCP Console → IAM → Service Accounts → Revoke key
- **Cần bạn:** Thực hiện thao tác trên GCP Console
- **Sau đó:** Tôi backup key ra ngoài workspace → xóa file JSON

### Item C: Xác nhận thay đổi OpenClaw gateway config
- Tôi sẽ đọc gateway config hiện tại → tạo bản sao → đề xuất thay đổi
- **Cần bạn:** Xem xét đề xuất → xác nhận → tôi sửa → restart gateway

### Item D: Xác nhận sửa .gitignore
- Tôi sẽ đọc .gitignore hiện tại → đề xuất thêm pattern
- **Cần bạn:** Xem xét → xác nhận → tôi sửa file

### Item E: Xác nhận hướng tổ chức lại thư mục
- Tôi sẽ đề xuất lộ trình di chuyển file từng bước
- **Cần bạn:** Xác nhận target structure → OK để bắt đầu

---

## 7. Việc không được tự động làm (5 items)

### ❌ Không tự rotate key
- Gemini key và GCP key phải do user revoke/tạo mới trên dashboard
- Tôi không có quyền truy cập Google AI Studio hay GCP Console
- Tôi chỉ sửa source code sau khi có key mới

### ❌ Không tự xóa file chưa backup
- Không xóa file chứa secret nếu chưa backup ra ngoài workspace
- Không xóa file nếu chưa git commit trạng thái hiện tại
- Không xóa file nếu chưa có xác nhận của user

### ❌ Không tự động di chuyển file hàng loạt
- Mọi file move đều phải theo lộ trình: copy → verify path → update imports → delete original
- Không move file có active runtime dependency (AGENTS.md, SKILL.md, MEMORY.md, than-thong.cmd)
- Không move runner/, .github/, skills/, memory/ (daily)

### ❌ Không tự sửa config production chưa backup
- Gateway config, than-thong.cmd, AGENTS.md — backup trước mọi thay đổi
- Tạo bản sao (.backup) trước khi sửa

### ❌ Không tự dọn Docker container/image
- n8n container restart loop cần debug → không xóa vội
- Langfuse image (1.37GB) cần xác nhận không dùng → mới xóa
- Không docker rm/docker rmi khi chưa hỏi

---

## 8. Cấu trúc thư mục đề xuất

### Thư mục hiện tại → Mục tiêu

| Hiện tại | Mục tiêu | Ghi chú |
|---|---|---|
| `scripts/*.py` (test, n8n, tools) | `openclaw-system/tools/test/`, `tools/n8n/`, `tools/browser/`, v.v. | Gom theo domain |
| `tools-internal/scripts/` (65 files) | `openclaw-system/tools/scripts/` | Core toolchain |
| `tools-internal/reference-library/` | `openclaw-system/data/reference-library/` | Reference data |
| `tools-internal/rag-data/` | `openclaw-system/data/rag/` | RAG data |
| `tools-internal/mcp_*.py` | `openclaw-system/apps/mcp/` | MCP servers |
| `config/`, `tools-internal/.env` | `openclaw-system/configs/env/`, `configs/secrets/` | Config files |
| `examples/` | `openclaw-system/workflows/` | Workflow templates |
| `reports/` (markdown) | `openclaw-system/docs/reports/` | Reports |
| `references/` | `openclaw-system/docs/references/` | Reference docs |
| `than-thong.cmd` | `openclaw-system/scripts/than-thong.cmd` | Entry point |

### Giữ nguyên tại root

- `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `MEMORY.md`, `IDENTITY.md`
- `skills/`
- `memory/` (daily notes)
- `.github/`
- `runner/`
- `_audit/`

### Lộ trình di chuyển an toàn

1. **docs/** → Copy-only, không code dependency
2. **workflows/** → Template files, không active reference
3. **configs/** → Copy + update spec/vault paths
4. **data/** → Copy + update writer/reader paths (critical)
5. **tools/** → Copy + update import paths (critical)
6. **apps/** → Copy + update internal paths (critical)
7. **scripts/** → Move cuối, sau khi path updates verified
8. **Root config updates** → than-thong.cmd path fix, AGENTS.md nếu cần

---

## 9. Config/env đề xuất

### `.env.example` template

```bash
# === API Keys (thay giá trị thật của bạn) ===
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# === GCP (dùng Workload Identity nếu có) ===
# GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\secure\key.json

# === Rate Limiting ===
LLM_MAX_CALLS_PER_MINUTE=30

# === Docker ===
COMPOSE_PROJECT_NAME=openclaw

# === Ollama ===
OLLAMA_HOST=http://localhost:11434

# === Qdrant ===
QDRANT_HOST=http://localhost:6333

# === Agent ===
AGENT_LOG_LEVEL=INFO
THAN_THONG_MODE=strict
```

### File config cần tạo

| File | Mục đích |
|---|---|
| `.env.example` | Template env vars, không key thật |
| `docker-compose.yml` | Gom qdrant + portainer + dozzle + tinyproxy |
| `mcp_config.json.example` | MCP server config template |
| `tool_config.yaml.example` | Tool config template |
| `.gitignore` (cập nhật) | Thêm runner/, _audit/, configs/secrets/ |

---

## 10. Workflow vận hành đề xuất

### Script lifecycle

| Script | Mục đích | Khi chạy |
|---|---|---|
| `start.ps1` | Khởi động Docker + Ollama + gateway | Mỗi khi boot |
| `stop.ps1` | Dừng an toàn (graceful shutdown) | Trước khi tắt máy |
| `healthcheck.ps1` | Kiểm tra toàn bộ service | Mỗi heartbeat / cron |
| `audit.ps1` | Audit bảo mật + cấu trúc → _audit/ | Hàng ngày / weekly |
| `backup.ps1` | Git commit + push + backup memory | Cuối ngày |
| `doctor.ps1` | Chẩn đoán lỗi phổ biến + gợi ý fix | Khi có lỗi |

### CI/CD bổ sung

| Workflow | Mục đích |
|---|---|
| Auto-audit | GitHub Actions chạy audit định kỳ |
| Rollback | Workflow rollback khi deploy lỗi |
| PR audit | Audit tự động trên mọi PR |

### Port quản lý

| Port | Service | Mở? |
|---|---|---|
| 6333-6334 | Qdrant API | Local only ✅ |
| 11434 | Ollama API | Local only ✅ |
| 8888 | Dozzle logs | Local only ✅ |
| 9000 | Portainer | Auth required ✅ |
| 1080 | Tinyproxy | MEDIUM risk ⚠️ |

---

## 11. Rule an toàn cho agent

### ⚠️ Quy tắc vận hành

1. **Không tự động xóa/thay đổi file production** — Luôn backup git trước
2. **Không tự động rotate key** — User làm trên dashboard, tôi chỉ sửa code
3. **Không sửa .gitignore khi chưa hỏi** — File quan trọng cho security
4. **Không move file khi chưa verify import paths** — Tránh break runtime
5. **Không docker rm/docker rimi khi chưa xác nhận** — Dễ mất data
6. **Không expose service ra internet** — Portainer/Dozzle/Qdrant local only
7. **Không push secret lên GitHub** — Kiểm tra .gitignore trước mọi commit

### ✅ Quy tắc nên làm

1. **Mọi thay đổi file → git commit trước**
2. **Mọi file mới → kiểm tra không chứa secret**
3. **Mọi import path update → test trước khi delete original**
4. **Mọi config change → backup + đề xuất → user OK → apply**
5. **Audit định kỳ → ghi vào _audit/**

### 📋 Checklist trước mọi thao tác nguy hiểm

- [ ] Đã git commit/stash trạng thái hiện tại?
- [ ] Đã backup file sẽ sửa?
- [ ] Đã xác nhận với user?
- [ ] Đã kiểm tra dependency (import path, relative path)?
- [ ] Có rollback plan không?

---

## 12. Kế hoạch thực hiện từng bước (5 giai đoạn)

### Giai đoạn 1: 🔴 Cấp cứu bảo mật (1-2 ngày)

| Bước | Task | Ai làm | Trạng thái |
|---|---|---|---|
| 1.1 | User revoke Gemini API key trên AI Studio | User | ⏳ Chờ |
| 1.2 | User revoke GCP key trên GCP Console | User | ⏳ Chờ |
| 1.3 | Xóa elevated exec wildcard — backup + sửa config | Agent (sau khi user OK) | ⏳ Chờ |
| 1.4 | Thay hardcoded Gemini key → env var (5 scripts) | Agent (sau khi có key mới) | ⏳ Chờ |
| 1.5 | Backup GCP key ra ngoài → xóa khỏi workspace | Agent (sau khi user revoke) | ⏳ Chờ |
| 1.6 | Thêm _audit/ + runner/ vào .gitignore | Agent (sau khi user OK) | ⏳ Chờ |
| 1.7 | Xóa PostHog telemetry key khỏi telemetry.py | Agent | ⏳ Chờ |

### Giai đoạn 2: 🟡 Chuẩn hóa cấu trúc thư mục (2-3 ngày)

| Bước | Task | Chi tiết |
|---|---|---|
| 2.1 | Tạo cấu trúc openclaw-system/ | Tạo 8 thư mục con |
| 2.2 | Move docs/ (copy-only) | References, reports, docs |
| 2.3 | Move workflows/ | Lobster, n8n templates |
| 2.4 | Move configs/ | env, secrets, policies, prompts |
| 2.5 | Move data/ | RAG, db, records, cache |
| 2.6 | Move tools/ | Scripts + update import paths |
| 2.7 | Move apps/ | MCP servers + update paths |
| 2.8 | Move scripts/ | than-thong.cmd + hooks |
| 2.9 | Update root configs | than-thong.cmd path, alias |

**Nguyên tắc:** Copy → verify → update paths → delete original. Từng bước một.

### Giai đoạn 3: 🟡 Chuẩn hóa config/env (song song GĐ2, 1-2 ngày)

| Bước | Task | Chi tiết |
|---|---|---|
| 3.1 | Tạo `.env.example` | Template sạch, không key thật |
| 3.2 | Tạo config template MCP | mcp_config.json.example |
| 3.3 | Tạo config template tool | tool_config.yaml.example |
| 3.4 | Thay hardcoded → env var | Áp dụng cho scripts có key |
| 3.5 | Gom config vào configs/ | Tách khỏi tools-internal/ |
| 3.6 | Kiểm tra .gitignore | Đảm bảo đủ pattern |

### Giai đoạn 4: 🟡 Chuẩn hóa workflow vận hành (2-3 ngày)

| Bước | Task | Chi tiết |
|---|---|---|
| 4.1 | Tạo start.ps1 | Mẫu, chưa chạy |
| 4.2 | Tạo stop.ps1 | Mẫu, chưa chạy |
| 4.3 | Tạo healthcheck.ps1 | Mẫu, chưa chạy |
| 4.4 | Tạo audit.ps1 | Mẫu, chưa chạy |
| 4.5 | Tạo backup.ps1 | Mẫu, chưa chạy |
| 4.6 | Tạo doctor.ps1 | Mẫu, chưa chạy |

### Giai đoạn 5: 🟢 Tối ưu nâng cao (1 tuần)

| Bước | Task | Chi tiết |
|---|---|---|
| 5.1 | Docker cleanup | Dọn langfuse (1.37GB), fix/debug n8n |
| 5.2 | Dependency cleanup | extracted-scripts/ dọn, cache dọn |
| 5.3 | Log cleanup | runner/_diag/, __pycache__ |
| 5.4 | Auto-audit cron | GitHub Actions audit định kỳ |
| 5.5 | Documentation | Operating guide, system map |
| 5.6 | Tạo docker-compose.yml | Gom 4 container đang chạy |

**Tổng thời gian ước tính:** 1-2 tuần nếu làm liên tục.

---

## 13. Checklist trước khi sửa thật

### Trước mỗi thao tác

- [ ] **Git status** — đã commit/stash mọi thay đổi?
- [ ] **Backup** — đã copy file sắp sửa ra ngoài?
- [ ] **Xác nhận** — user đã OK cho thao tác này?
- [ ] **Dependency check** — import paths, relative paths, config references?
- [ ] **Rollback plan** — biết cách undo nếu sai?

### Trước Giai đoạn 1 (bảo mật)

- [ ] User đã revoke Gemini key? (cần link AI Studio)
- [ ] User đã revoke GCP key? (cần link GCP Console)
- [ ] Đã xác định gateway config location?
- [ ] Đã git commit workspace hiện tại?
- [ ] Đã backup scripts có secret ra ngoài?

### Trước Giai đoạn 2 (cấu trúc thư mục)

- [ ] Đã có target structure được user xác nhận?
- [ ] Đã xác định file nào KHÔNG được move? (AGENTS.md, skills/, runner/)
- [ ] Đã liệt kê toàn bộ import path cần update?
- [ ] Đã tạo openclaw-system/ skeleton?
- [ ] Có script để kiểm tra import path không bị hỏng?

### Trước Giai đoạn 3 (config/env)

- [ ] Đã xác định toàn bộ file cần thay hardcoded key?
- [ ] Đã tạo .env.example?
- [ ] Đã kiểm tra .gitignore exclude đúng pattern?
- [ ] User đã approve config template?

### Trước Giai đoạn 4 (workflow)

- [ ] Đã thống nhất script naming convention?
- [ ] Scripts chỉ là mẫu (template), chưa chạy?

### Trước Giai đoạn 5 (tối ưu)

- [ ] Đã xác nhận langfuse image không dùng?
- [ ] Đã xác nhận n8n có sửa hay dọn?
- [ ] extracted-scripts/ còn cần không?

---

## 14. Checklist sau khi sửa thật

### Sau mỗi thao tác

- [ ] **Verify file mới** — nội dung đúng, không chứa secret?
- [ ] **Test import** — script chạy được không?
- [ ] **Git diff** — kiểm tra thay đổi có an toàn?
- [ ] **Commit** — message rõ ràng, mô tả thay đổi?

### Sau Giai đoạn 1 (bảo mật)

- [ ] Không còn Gemini API key hardcode trong scripts/
- [ ] config/gcp-n8n-vertex-ai-key.json đã xóa khỏi workspace
- [ ] gateway config đã sửa, elevated wildcard không còn
- [ ] .gitignore đã cập nhật (runner/, _audit/)
- [ ] PostHog key đã xóa
- [ ] git commit ghi lại toàn bộ thay đổi

### Sau Giai đoạn 2 (cấu trúc thư mục)

- [ ] openclaw-system/ có đủ 8 thư mục con
- [ ] Mọi file đã move đúng target
- [ ] Import paths đã update, không còn reference path cũ
- [ ] than-thong.cmd path đã update
- [ ] AGENTS.md, SOUL.md, skills/, runner/ không bị move
- [ ] git commit ghi lại toàn bộ thay đổi

### Sau Giai đoạn 3 (config/env)

- [ ] .env.example tồn tại với placeholder key
- [ ] Mọi script dùng `os.environ.get()` thay vì hardcode
- [ ] .gitignore bảo vệ đủ pattern
- [ ] Config templates đã tạo

### Sau Giai đoạn 4 (workflow)

- [ ] Scripts lifecycle đã tạo (start, stop, healthcheck, audit, backup, doctor)
- [ ] Là mẫu (chưa chạy)

### Sau Giai đoạn 5 (tối ưu)

- [ ] Docker image không dùng đã dọn
- [ ] Cache/log đã dọn
- [ ] Operating guide hoàn thiện
- [ ] Auto-audit cron đã setup
- [ ] docker-compose.yml hoạt động

---

## 15. Kết luận

### Tình trạng hiện tại
Hệ thống OpenClaw đang hoạt động ổn định ở mức trung bình với 3 **vấn đề CRITICAL** cần xử lý ngay:
1. Secret trong source code (Gemini + GCP key)
2. Elevated exec wildcard
3. Runner credentials trong workspace

### Ưu tiên tuyệt đối
**Bảo mật trước — tổ chức sau.** Không làm gì khác cho đến khi secret được xử lý và elevated wildcard bị vô hiệu hóa.

### Lộ trình tổng thể

```
Tuần 1: 🔴 Cấp cứu bảo mật (Giai đoạn 1)
Tuần 1-2: 🟡 Chuẩn hóa cấu trúc + config (Giai đoạn 2-3)
Tuần 2: 🟡 Workflow vận hành (Giai đoạn 4)
Tuần 2-3: 🟢 Tối ưu nâng cao (Giai đoạn 5)
```

### Những việc CHỜ USER trả lời

1. ✅ Revoke Gemini API key trên AI Studio
2. ✅ Revoke GCP key trên GCP Console
3. ✅ Xác nhận sửa gateway config
4. ✅ Xác nhận sửa .gitignore
5. ✅ Xác nhận target structure openclaw-system/

### Câu hỏi cho user

> "Em đã tổng hợp toàn bộ audit vào UPGRADE_MASTER_PLAN.md. Anh/chị xem qua và cho em biết:
> 1. Đã revoke Gemini key chưa?
> 2. Đã revoke GCP key chưa?
> 3. Có đồng ý em xem xét gateway config không?
> 4. Có đồng ý em update .gitignore không?
> 5. Cấu trúc openclaw-system/ có ổn không?"

---

*Kế hoạch này được tạo từ tổng hợp 6 file audit: MASTER_SUMMARY, SECURITY_CHECKLIST, UPGRADE_CONTEXT, UPGRADE_ROADMAP, UPGRADE_TASKS, REORGANIZE_PLAN.*
*Không có file nào bị sửa đổi trong quá trình tạo kế hoạch này.*
