# 📋 NOTE NỐI VIỆC — DỰ ÁN KHAI THÁC G:\Ai

> **Tạo lúc:** 2026-05-14 11:34 GMT+7
> **Reset tại đây.** Đọc file này trước, nếu có thì đọc review/G-Ai-inventory.md và G-Ai-vs-E-comparison.md.

---

## 🎯 TRẠNG THÁI TỔNG QUAN

**Công việc đã hoàn thành:**

| Hạng mục | Trạng thái |
|----------|:--------:|
| Scan inventory 188 file G:\Ai | ✅ Done |
| So sánh G:\Ai vs E workspace | ✅ Done |
| Lọc 156 file an toàn (không trùng) | ✅ Done |
| Kiểm tra xung đột chi tiết (port/skill/path/dependency) | ✅ Done |
| Thần thông gate kiểm tra lần cuối (164 file, PASS 100%) | ✅ Done |
| Phân loại & copy vào review/candidate/ 14 thư mục | ✅ Done |
| Nấu file này — nối việc | ✅ Done |

**Công việc CÒN LẠI — chưa động đến:**

| Giai đoạn | Chi tiết | Ưu tiên |
|-----------|----------|:-------:|
| **GĐ1: Triển khai Skills** | Extract + register skills từ zip vào E:\skills\ | ⭐⭐⭐ |
| **GĐ2: Nội bộ Tools** | Chép script/tool hữu ích vào tools-internal/ | ⭐⭐ |
| **GĐ3: API/Service** | Tích hợp MCP, API Gateway, n8n workflows | ⭐⭐ |
| **GĐ4: Memory/Search** | Setup mem0, FireCrawl, Browser-Dùng | ⭐ |
| **GĐ5: Kiểm chứng** | Test từng thứ chạy được | ⭐⭐ |

---

## 📂 CẤU TRÚC CANDIDATE — 164 FILE, ~1GB

Tất cả tại: **review/candidate/**

```
review/candidate/
├── agent-framework/    8 files → 207MB
│   ├── AgentScope.zip
│   ├── LangChain.zip
│   ├── Spring-AI.zip
│   ├── VũTrụAgent.zip (AgentUniverse)
│   ├── KỹNăngAgentKhoaHọc.zip (134 skills!)
│   ├── TạoKỹNăngAgent.zip
│   ├── ThiếtKếHệThốngAgent.zip
│   └── Agent-BộQuảnTrị.zip
│
├── agent-tool/        31 files →  29MB
│   ├── CLI-BấtCứ, CLI2KỹNăng, CICADA, GRIT,
│   ├── Agency-Agent, Agent-VươnTới, Agent-Captcha,
│   ├── Hermit, Kode-Agent, HexStrike-AI, NadirClaw, GBrain,
│   ├── AI-CặpĐôi, AI-TiếpThị, AI cục bộ,
│   ├── ĐaAgent-KhoThôngMinh, TựĐộng-NghiênCứuSâu,
│   ├── TạoPromptAgentAI, XâyAppVớiAgentAI,
│   ├── LậpKếHoạchVớiTệp, MẫuCloneWeb-AI,
│   ├── desktop-control, self-improving-agent,
│   ├── Persona-BảoVệ, Salacia-BảoVệ,
│   ├── KỹNăng-ĐóngBăng, TiệnÍch-TuânThủ,
│   ├── SystemPrompt-MôHình-AITools,
│   ├── Prompt-LặpLại-V2, BảoTrìMáyChủ-KỹNăng,
│   └── ÝTưởng-ThànhSảnPhẩm
│
├── skill-collection/   5 files →  30MB
│   ├── TốiThiểuToken-KỹNăng.zip (5.258 files)
│   ├── PowerPlatform-KỹNăng.zip
│   ├── 724-VănPhòng, 996-KỹNăng
│   └── KỹNăng-ĐóngBăng
│
├── memory/            10 files →  75MB
│   ├── mem0.zip, memU.zip, memUBot.zip
│   ├── MemPalace.zip, Memorix.zip, BộNhớAI-Tuyển.zip
│   ├── GBrain.zip, Obsidian-LLM-Wiki.zip, Obsidian-CầuKho.zip
│   └── Gemini-LangGraph-KhởiĐầu.zip
│
├── search-browser/     5 files →  48MB
│   ├── FireCrawl.zip (30.7MB)
│   ├── Browser-Dùng.zip, Browser-DùngDesktop.zip
│   ├── NanoBrowser.zip
│   └── Spy-TìmKiếm.zip
│
├── mcp/                4 files →   8MB
│   ├── FastMCP.zip
│   ├── Toonify-MCP.zip
│   └── MCP-MáyChủ-Tuyển.zip, MCP-TrungTâm.zip
│
├── api-gateway/        8 files →  49MB
│   ├── API-Mới, Chat2API, DeepSeek-API-MiễnPhí
│   ├── FastAPI-MẫuFullStack, CLI-ProxyAPI
│   ├── GPT-MãMở, COAI, BộAPIBackend
│
├── claude/             9 files →  20MB
│   ├── Claude-BạchTuộc (Octopus), Claude-BạnCode
│   ├── Claude-GameStudio, Claude-SiêuBộNhớ
│   ├── ClaudeCode-Tuyển, ClaudeKỹNăng-Tuyển
│   ├── CC-ChuyểnMạch, CC-Cổng
│   └── ScanAI-ClaudeCode-KỹNăng
│
├── claw-ecosystem/     7 files →  59MB
│   ├── Caclawphony, Claw-Code, Claw-Mesh, Claw-Rice
│   ├── ClawHub, ClawTeam, Clawdinators
│
├── openclaw-plugins/  14 files →   5MB
│   ├── 12 plugins OpenClaw (WeChat, DựÁn, Ansible, v.v.)
│   └── OpenCLI, OpenMythos, OpenSrc, Nix-OpenClaw
│
├── git-devops/         5 files →  28MB
│   ├── GitNexus.zip (3.155 files!)
│   ├── Gitea-Mirror.zip, Git-Cliff.zip
│   ├── Terraform-Spec-Test, VS-SDK-TestFX
│
├── n8n/                3 files →   0MB
│   ├── n8n-workflow-automation, n8n-ServerChan
│   └── Cognee-n8n
│
└── other/             55 files → 489MB
    ├── OpenCode.zip (84MB) — agent coding
    ├── Shannon.zip (67MB), Spark.zip (66MB)
    ├── Vibe-Kanban.zip (61MB), Spring-AI.zip (60MB)
    ├── Hudi.zip (24MB), Fincept-Terminal.zip (20MB)
    ├── TàiLiệu.zip (30MB), MỹChốngMỹ.zip (32MB)
    └── v.v.
```

---

## 🔜 KẾ HOẠCH CỤ THỂ — CÁC BƯỚC TIẾP THEO

### GIAI ĐOẠN 1: TRIỂN KHAI SKILLS (ưu tiên cao nhất)

**Tool có sẵn:** `tools-internal/scripts/import_orchestrator.py`

**Cách làm:**
1. Dùng `than_thong_console scan-G` để refresh
2. Với mỗi zip trong `agent-tool/` và `skill-collection/`:
   - Extract file SKILL.md và nội dung skills
   - Copy vào `E:\skills\<skill-name>\`
   - Register vào `skills/SKILL-REGISTRY.md`
3. Skill names đã biết trước từ scan — không cần đọc lại zip
4. File nào có skill trùng tên → extract selective (bỏ qua file trùng)

**File ưu tiên GĐ1:**
- `TạoKỹNăngAgent.zip` — tool tạo skill
- `CLI2KỹNăng.zip` — CLI → skill converter
- `KỹNăngAgentKhoaHọc.zip` — 134 skills tham khảo
- `CLI-BấtCứ.zip` — any CLI → skill
- `CICADA.zip` — constraint-driven agent design
- `desktop-control-1.0.0.zip` — desktop automation skill

### GIAI ĐOẠN 2: NỘI BỘ TOOLS & UTILITIES

Chép các script hữu ích từ zip vào `tools-internal/`:
- `Agent365-CôngCụDev.zip` → đã có rate_limiter.py, prompt_utils.py; xem còn gì mới
- `SystemPrompt-MôHình-AITools.zip` → system prompt management
- `BảoTrìMáyChủ-KỹNăng.zip` — server maintenance scripts
- `TựĐộng-NghiênCứuSâu.zip` — deep research automation

### GIAI ĐOẠN 3: API & SERVICE INTEGRATION

Nhóm `api-gateway/` và `mcp/`:
- `FastMCP.zip` — setup MCP python framework
- `Chat2API.zip` — chat→API wrapper
- `DeepSeek-API-MiễnPhí.zip` — free API proxy
- `FastAPI-MẫuFullStack.zip` — full stack template
- MCP từ `MCP-MáyChủ-Tuyển.zip`, `MCP-TrungTâm.zip`

### GIAI ĐOẠN 4: MEMORY & SEARCH

- `mem0.zip` (20.7MB) — AI memory layer
- `FireCrawl.zip` (30.7MB) — web crawling
- `Browser-Dùng.zip` — browser automation (thay Playwright)
- `Spy-TìmKiếm.zip` (15.3MB) — search engine tool

### GIAI ĐOẠN 5: KIỂM CHỨNG

Sau mỗi giai đoạn chạy:
```
than_thong_console preflight
than_thong_console dashboard
```

Và kiểm tra thủ công: gateway không báo lỗi khi restart.

---

## 📝 FILE LƯU HỒ SƠ

| File | Mô tả |
|------|-------|
| `review/G-Ai-inventory.md` | Full inventory 188 file G:\Ai |
| `review/G-Ai-vs-E-comparison.md` | So sánh G vs E |
| `review/G-Ai-loc-safe.md` | 156 file sạch (đã lọc) |
| `review/G-Ai-conflict-check.md` | Kiểm tra xung đột chi tiết |
| `review/than-thong-candidate-check.md` | Thần thông gate check (PASS 100%) |

---

## ⚠️ LƯU Ý QUAN TRỌNG KHI NỐI VIỆC

1. **Chưa extract file nào** — tất cả còn nguyên zip trong `review/candidate/`
2. **Không copy bulk** — chỉ extract phần mới, viết SKILL.md mới cho phù hợp hệ thống
3. **Luật thần thông** luôn active: local-first, không billing, gate trước mọi hành động
4. **File trùng** (FastCode, OpenClaw, OpenClaw-QWQ, AtomicBot, OpenViking, AntiGravity-KỹNăngHay) — **không lấy**
5. **File lớn >100MB** (AI-Maestro 300MB, ClawWork 524MB, Dify-Plugin 814MB, Hello-Agent 118MB) — **bỏ qua đợt này**
6. **Nếu cần thêm chi tiết** → đọc `review/than-thong-candidate-check.md` và `review/G-Ai-vs-E-comparison.md`
7. **Dùng thần thông cho mọi tác vụ** — `than_thong_console <lệnh>`

---

*End of note. System was last at 11:34 2026-05-14 GMT+7. All scans, checks, and classification done. Ready for extract phase.*
