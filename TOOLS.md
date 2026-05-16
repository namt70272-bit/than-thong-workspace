# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### Thần thông rule (local-first)

- Luật vận hành chính thức hiện tại tên: **thần thông**
- `top` và `billing` vẫn giữ như alias legacy để tương thích ngược
- Mọi công việc phải ưu tiên nội bộ / local-first
- Không được làm phát sinh billing cho model/API/provider/dịch vụ trả phí
- Nếu có nguy cơ chạm billing → phải báo trước, không tự chạy
- Ngoại lệ duy nhất: tác vụ cần Internet để đọc/kiểm tra bên ngoài, nhưng vẫn phải tránh đường dẫn có billing nếu có thể

### Internal tools (local-only)

- `tools-internal/` — Bộ công cụ nội bộ để xử lý inventory, cleanup, import tracking, A0 extraction, sync record, duplicate/junk scan, workspace indexing mà không đụng billing
- `tools-internal/scripts/than_thong_gate.py` — cổng chính mới cho luật `thần thông`
- `tools-internal/scripts/than_thong_wrapper.py` — wrapper chính mới cho trusted internal flow
- `tools-internal/scripts/than_thong_console.py` — console điều hành chính mới
- `tools-internal/scripts/top_gate.py` — alias legacy của `top`
- `tools-internal/scripts/top_wrapper.py` — alias legacy của `top`
- `tools-internal/scripts/top_console.py` — alias legacy của `top`
- `tools-internal/scripts/billing_gate.py` — alias legacy của gate cũ để tương thích
- `tools-internal/scripts/task_router.py` — router ưu tiên tool nội bộ theo luật top
- `tools-internal/scripts/preflight_runner.py` — cổng vào chuẩn gate + route
- `tools-internal/scripts/import_validator.py` — validator candidate trước khi nhập hệ
- `tools-internal/scripts/deep_validator.py` — validator sâu: secret/network/blocked path
- `tools-internal/scripts/candidate_builder.py` — builder candidate layer
- `tools-internal/scripts/sync_executor.py` — sync one-way local
- `tools-internal/scripts/rollback_manifest.py` — manifest rollback
- `tools-internal/scripts/real_rollback.py` — rollback thực tế delete/restore
- `tools-internal/scripts/import_orchestrator.py` — build + validate + sync + rollback
- `tools-internal/scripts/domain_tracker.py` — tracker 16 mảng
- `tools-internal/scripts/duplicate_checker.py` — scan duplicate
- `tools-internal/scripts/canonical_checker.py` — check nhiều nguồn sự thật
- `tools-internal/scripts/drift_checker.py` — check lệch candidate/workspace
- `tools-internal/scripts/wave_manager.py` — quản lý các wave nhập
- `tools-internal/scripts/ops_dashboard.py` — dashboard trạng thái công cụ nội bộ
- `tools-internal/scripts/ops_console.py` — console điều hành nội bộ
- `tools-internal/scripts/trusted_registry.py` — registry script trusted theo policy
- `tools-internal/scripts/compliance_audit.py` — audit tuân thủ lớp top
- `tools-internal/scripts/auto_maintain.py` — chạy bảo trì nội bộ định kỳ bằng local tools
- `tools-internal/scripts/top_win_audit.py` — quét ổ đĩa, OS, biến môi trường Windows
- `tools-internal/scripts/top_win_env_audit.py` — kiểm tra biến môi trường
- `tools-internal/scripts/top_win_svc_audit.py` — kiểm tra service Windows
- `tools-internal/scripts/top_win_startup_audit.py` — chương trình khởi động cùng Windows
- `tools-internal/scripts/top_win_process_audit.py` — theo dõi process quan trọng
- `tools-internal/scripts/top_win_disk_health.py` — sức khỏe ổ đĩa
- `tools-internal/scripts/top_win_system_restore.py` — điểm khôi phục Windows
- `tools-internal/scripts/top_win_cleanup.py` — tìm temp/junk toàn máy Windows
- `tools-internal/scripts/top_win_tighten.py` — gợi ý siết chặt service/env
- `tools-internal/scripts/top_win_data_map.py` — kho dữ liệu trên các ổ
- `tools-internal/scripts/top_win_dashboard.py` — dashboard tổng quan Windows
- `tools-internal/scripts/top_win_full_dashboard.py` — dashboard đầy đủ Windows-side
- `references/compliance/THAN-THONG-RULE.md` — Luật thần thông/local-first chính thức
- `references/compliance/TOP-RULE.md` — alias legacy
- `references/compliance/BILLING-RULE.md` — alias legacy

### Default execution rule

- Từ nay mọi mệnh lệnh phải đi qua **thần thông trước**.
- `thần thông` là cửa vào mặc định để nhận lệnh, gate, route và thực thi local luôn nếu làm được.
- `than_thong_supervisor.py` là lớp supervisor mặc định của cửa vào này.
- Câu lệnh rõ ràng hay câu tự nhiên đều phải vào `thần thông` trước.
- Chỉ khi `thần thông` không có command phù hợp hoặc xác nhận không xử lý được thì mới gọi trực tiếp `tools-internal` khác.
- Bất kỳ thứ gì đi qua `thần thông` đều không được sử dụng billing, quota, top-up, credit, hay provider trả phí.
- Entry nhanh:
  - `python tools-internal\scripts\than_thong_console.py <lệnh>`
  - `python tools-internal\scripts\than_thong_entry.py <lệnh>`
  - `than-thong.cmd <lệnh>`
- Chỉ khi tác vụ thật sự cần Internet mới cân nhắc đường ngoài, và vẫn không được để phát sinh billing nếu chưa báo trước.

### Utilities (adapted from Agent365 autoTriage + Agent365-devTools)

- `utils/rate_limiter.py` — Token-bucket rate limiter cho LLM calls
  - v2 (2026-05-11): thêm env override `LLM_MAX_CALLS_PER_MINUTE`, logging khi throttle
  - Nguồn: `Agent365-devTools-main/autoTriage/services/llm_service.py` (RateLimiter class)
- `utils/prompt_utils.py` — Load prompt từ YAML + sanitize input/output
  - v2 (2026-05-11): thêm `sanitize_exception()` (redact Bearer/api_key/sk-), XML escape trong `sanitize_user_content()`, constants `MAX_TITLE_LENGTH`/`MAX_BODY_LENGTH`
  - Nguồn: `Agent365-devTools-main/autoTriage/utils/sanitise.py`
  - API cũ giữ nguyên: `load_prompts`, `render_prompt`, `sanitize_llm_output` không thay đổi

### Config

- `config/prompts-template.yaml` — 10 prompt templates cho LLM tasks
  - Nguồn: `Agent365-devTools-main/autoTriage/config/prompts.yaml` (port 2026-05-11)
  - Giữ: `classify_issue`, `summary`, `select_assignee`, `copilot_fixable`, `fix_suggestions`
  - Bỏ: `daily_digest`, `daily_report`, `weekly_planning` (GitHub Actions specific)
  - Dùng với: `load_prompts()` + `render_prompt()` từ `utils/prompt_utils.py`

### Skills (extracted and adapted)

- `skills/review-code/` — Code review skill (adapted from Claude review-pr)

### Scripts (extracted from OpenClaw source)

- `scripts/model_usage.py` — Phân tích LLM usage từ CodexBar logs (Agent365 autoTriage pattern)
- `scripts/tmux/find-sessions.sh` — Liệt kê tmux sessions
- `scripts/tmux/wait-for-text.sh` — Poll tmux pane cho text pattern
- `scripts/video/frame.sh` — Trích frame từ video (ffmpeg)
- `scripts/whisper/transcribe.sh` — Whisper API transcription

### Skill-Creator tools

- `skills/skill-creator/init_skill.py` — Tạo skill mới từ template
- `skills/skill-creator/package_skill.py` — Đóng gói skill → .skill file
- `skills/skill-creator/quick_validate.py` — Validate skill nhanh

### Examples

- `examples/inbox-triage.lobster` — Mẫu TaskFlow inbox triage workflow
- `examples/pr-intake.lobster` — Mẫu PR intake lane workflow

### References

- `references/1password/` — op CLI examples + get-started
- `references/himalaya/` — Email client config (Gmail, iCloud)
- `references/model-usage/` — CodexBar CLI commands
- `references/awesome-skills-catalog/` — VoltAgent Awesome Agent Skills (1100+ official + community skills)
  - **README.md** → Danh sách đầy đủ skills từ Anthropic, Google, Stripe, Cloudflare, Vercel, Trail of Bits, Hugging Face, v.v.
  - **CONTRIBUTING.md** → Hướng dẫn add skill mới (format, yêu cầu)
  - **INDEX.md** → Tóm tắt danh mục + cách dùng
  - **Use case:** Tìm skill tham khảo, khám phá best practices, add skills mới vào agent
  - **Updated:** 2026-05-12

---

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)
