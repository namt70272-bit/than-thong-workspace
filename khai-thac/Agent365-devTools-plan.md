# Kế hoạch khai thác: Agent365-devTools-main.zip

**Nguồn:** `G:\đã xong\Agent365-devTools-main.zip`  
**Ngày lập:** 2026-05-11  
**Nguyên tắc:** Không bê nguyên, không chép đè, không phá runtime đang chạy.

---

## 1. Sơ đồ cấu trúc (3 tầng)

```
Agent365-devTools-main/
├── .claude/
│   ├── agents/          ← 8 sub-agent prompts (architecture-reviewer, code-reviewer, pr-code-reviewer, prd-writer, prd-task-generator, task-implementer, pr-comment-resolver, test-coverage-reviewer)
│   └── skills/
│       ├── review-pr/   ← SKILL.md + review-pr.py (dùng gh CLI + Claude Code)
│       └── review-staged/ ← SKILL.md only (không có script Python)
├── .github/
│   ├── workflows/       ← 6 GitHub Actions YML (auto-triage, ci, daily-report, dependency-review, escalate-stale, update-team-workload)
│   └── copilot-instructions.md ← chuẩn code review cho .NET C#
├── autoTriage/
│   ├── cli/             ← triage_issue.py, daily_report.py, escalation_check.py
│   ├── config/          ← prompts.yaml (toàn bộ prompt LLM), team-members.json
│   ├── models/          ← ado_models.py, issue_classification.py, team_config.py
│   ├── services/        ← llm_service.py, intake_service.py, github_service.py, copilot_service.py, escalation_service.py, daily_report_service.py, teams_service.py, config_parser.py, prompt_loader.py
│   ├── utils/           ← sanitise.py (xịn hơn bản hiện tại)
│   ├── tests/           ← đầy đủ unit/integration tests
│   └── requirements.txt
├── Feedback/            ← 11 file phân tích chất lượng code, security audit, architecture review (chỉ đọc)
├── CLAUDE.md            ← hướng dẫn cho Claude Code làm việc với .NET CLI
├── src/                 ← .NET 8 C# CLI source (không liên quan hệ Python đang chạy)
└── docs/
```

---

## 2. Gắn nhãn từng vùng

| Vùng | Nhãn | Hành động |
|------|------|-----------|
| `.claude/agents/*.md` | **docs/prompts** | ✅ Trích nội dung, không copy nguyên |
| `.claude/skills/review-pr/` | **executable** | ✅ Đọc kỹ, port logic sang SKILL.md của ta |
| `.claude/skills/review-staged/` | **docs** | ✅ Đọc kỹ |
| `.github/copilot-instructions.md` | **docs/chuẩn** | ✅ Trích làm tài liệu tham khảo |
| `.github/workflows/` | **GitHub-specific** | ⚠️ Không dùng trực tiếp (cần GitHub Actions) |
| `autoTriage/utils/sanitise.py` | **executable** | ✅ Nâng cấp bản hiện tại |
| `autoTriage/services/llm_service.py` | **executable** | ✅ Trích RateLimiter cải tiến + call_llm pattern |
| `autoTriage/services/intake_service.py` | **executable** | ✅ Tham khảo pipeline classify |
| `autoTriage/config/prompts.yaml` | **config mẫu** | ✅ Port các prompt hữu ích |
| `autoTriage/models/` | **executable** | ✅ Tham khảo data models |
| `autoTriage/tests/` | **tests** | 📌 Tham khảo test pattern |
| `autoTriage/services/github_service.py` | **external-dep** | ❌ Gắn chặt GitHub API |
| `autoTriage/services/teams_service.py` | **external-dep** | ❌ MS Teams webhook |
| `autoTriage/services/copilot_service.py` | **external-dep** | ❌ GitHub Copilot API |
| `src/` (.NET C#) | **không liên quan** | ❌ Bỏ qua hoàn toàn |
| `Feedback/` | **docs phân tích** | 📌 Đọc tham khảo nếu cần |

---

## 3. Vùng nguy cơ cao

| Rủi ro | Mô tả |
|--------|-------|
| **Trùng utils** | `utils/sanitise.py` (repo) vs `utils/prompt_utils.py` + `utils/rate_limiter.py` (hiện tại) — nội dung KHÁC NHAU, không thể merge mù |
| **Trùng RateLimiter** | Bản trong `llm_service.py` có thêm env var `LLM_MAX_CALLS_PER_MINUTE` và logging — bản hiện tại đơn giản hơn |
| **Trùng sanitize** | `sanitise.py` có regex redact credential trong exception, bản hiện tại (`prompt_utils.py`) không có |
| **Prompt YAML** | `prompts.yaml` của repo dùng `{variable}` syntax — giống bản hiện tại (`render_prompt`) — an toàn để port |
| **Không có review-code skill** | Repo có `.claude/skills/review-pr/` dùng `gh` CLI và Claude Code — ta có `skills/review-code/` nhưng khác hoàn toàn |
| **GitHub Actions** | Workflows gắn chặt `GITHUB_TOKEN`, `AZURE_OPENAI_*` — không dùng được trong OpenClaw |

---

## 4. Danh sách thực sự nên lấy

### A. Nâng cấp `utils/sanitise.py` (file mới tách biệt)
- Regex redact Bearer token, api_key, password trong exception message
- `sanitise_user_content` có XML escape (bản hiện tại thiếu)
- Constants `MAX_ISSUE_TITLE_LENGTH`, `MAX_ISSUE_BODY_LENGTH`

### B. Nâng cấp `utils/rate_limiter.py`
- Thêm env var `LLM_MAX_CALLS_PER_MINUTE` override
- Thêm logging khi bị throttle
- Module-level singleton pattern

### C. Port `autoTriage/config/prompts.yaml` → `config/prompts-template.yaml`
- Chỉ lấy các prompt: `classify_issue_*`, `select_assignee_*`, `copilot_fixable_*`, `summary_*`
- Bỏ: `daily_digest_*`, `weekly_planning_*`, `daily_report_*` (GitHub-specific)
- Đặt tại `workspace/config/prompts-template.yaml` (candidate, chưa nối runtime)

### D. Trích `.claude/agents/` → `workspace/agents-reference/`
- `code-reviewer.md` — hướng dẫn review code cụ thể, có anti-pattern list
- `architecture-reviewer.md` — workflow review kiến trúc chuẩn
- `pr-code-reviewer.md` — 14 anti-pattern C# cụ thể (tham khảo cho review skill)
- **Không** đặt vào `.claude/agents/` của OpenClaw, chỉ lưu làm reference

### E. Tham khảo `autoTriage/models/issue_classification.py`
- Data class `IssueClassification`, `TriageRationale`
- Pattern `to_dict()`, `to_summary()` — có thể dùng cho skill review-code

---

## 5. Không nên lấy

| File/Thư mục | Lý do |
|---|---|
| `autoTriage/services/github_service.py` | Gắn chặt PyGithub, GitHub API |
| `autoTriage/services/teams_service.py` | MS Teams webhook |
| `autoTriage/services/copilot_service.py` | GitHub Copilot API |
| `autoTriage/services/escalation_service.py` | Phụ thuộc GitHub + Teams |
| `.github/workflows/` | Cần GitHub Actions runner |
| `src/` | .NET C#, không liên quan |
| `autoTriage/tests/` | Test gắn chặt GitHub mocks |
| `Feedback/` | Chỉ đọc tham khảo, không import |

---

## 6. Cách nhập tối thiểu vào E (thứ tự)

```
Bước 1: Tạo thư mục candidate (CHƯA nối runtime)
  workspace/khai-thac/candidate/
    ├── utils/
    │   ├── sanitise_v2.py        ← nâng cấp từ sanitise.py + prompt_utils.py
    │   └── rate_limiter_v2.py    ← nâng cấp từ rate_limiter.py
    ├── config/
    │   └── prompts-template.yaml ← chỉ port các prompt cần thiết
    └── agents-reference/
        ├── code-reviewer.md
        ├── architecture-reviewer.md
        └── pr-code-reviewer.md

Bước 2: Kiểm tra diff từng file
  - So sánh sanitise_v2 vs prompt_utils.py hiện tại → xác định hàm nào gộp/thay
  - So sánh rate_limiter_v2 vs rate_limiter.py hiện tại → xác định upgrade point

Bước 3: Cập nhật hệ thật (nếu ổn)
  - Gộp sanitise_v2 vào utils/prompt_utils.py HOẶC tách thành utils/sanitise.py mới
  - Update rate_limiter.py tại chỗ (backward compatible)
  - Đặt prompts-template.yaml vào workspace/config/ (không nối tự động)

Bước 4: Cập nhật TOOLS.md
  - Ghi lại nguồn gốc, version, ngày lấy
```

---

## 7. Rủi ro nếu nối thẳng

| Hành động | Rủi ro |
|---|---|
| Copy `sanitise.py` đè `prompt_utils.py` | Mất hàm `load_prompts`, `render_prompt`, `sanitize_llm_output` đang dùng |
| Copy nguyên `llm_service.py` | Phụ thuộc `openai`, `models.team_config`, `constants` không tồn tại |
| Copy nguyên `intake_service.py` | Phụ thuộc toàn bộ stack GitHub + Teams + Copilot |
| Đặt `.claude/agents/` vào OpenClaw | Agents này dành cho Claude Code (Cursor/claude.ai), không phải OpenClaw agent system |
| Import `prompts.yaml` trực tiếp vào runtime | Các prompt `daily_digest`, `weekly_planning` sẽ gây lỗi nếu thiếu biến |

---

## 8. Quyết định tiếp theo (cần xác nhận)

- [ ] **Có muốn nâng cấp `utils/sanitise` (bổ sung redact credential)?**
- [ ] **Có muốn nâng cấp `rate_limiter` (thêm env override + logging)?**
- [ ] **Có muốn port prompts template (cho review-code skill hoặc skill khác)?**
- [ ] **Có muốn lưu agents reference để dùng khi viết skill mới?**
- [ ] **Có muốn đọc thêm `Feedback/` để xem phân tích chất lượng code?**

---

*File này là kết quả bước Inventory + Chọn lọc theo skill khai-thac. Chưa có file nào được copy vào runtime.*
