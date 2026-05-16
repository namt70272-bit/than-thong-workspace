# MEMORY.md — Long-Term Memory

## Operating Rule Update (2026-05-15)

Chủ Nhân chốt lại: từ nay ưu tiên **thần thông** làm cửa vào mặc định cho mọi việc; giữ **local-first**, và **không chạm billing** hay đường có nguy cơ phát sinh chi phí nếu chưa được duyệt rõ ràng.

## Automation Philosophy (2026-05-12)

Chủ Nhân thiết lập rõ: tôi là **automation orchestrator**, không phải người click chuột.

Luật ưu tiên đã được lưu vào `AUTOMATION.md`. Tóm tắt:
1. API/CLI/script → Playwright → Python/FFmpeg → UI tree → tọa độ chuột (last resort)
2. Hotkey trước click. Không scan màn hình liên tục.
3. Tác vụ lặp → script reusable. Thao tác nguy hiểm → hỏi trước.

## Stack (đã xác nhận hoạt động)

- ffmpeg 8.1, ImageMagick 7.1.2, moviepy 2.2.1, Pillow 11.3, OpenCV 4.13
- Playwright 1.59 (Chromium đã cài), pywinauto 0.6.9, win32gui OK
- CapCut desktop: Qt app, không có UIA tree → dùng CapCut web qua Playwright
- CapCut web: load OK tại capcut.com/editor, cần login để lưu project

## Video quảng cáo

Hướng đúng: FFmpeg + Pillow/ImageMagick + template Python — nhanh hơn, ổn định hơn, chạy batch được. Không cần điều khiển CapCut.

## G:\Ai Zip Catalog — Trạng thái 2026-05-14

**Hoàn thành:** Scan & phân loại 188 zip → lọc 156 file an toàn (1GB) → kiểm tra xung đột → thần thông gate PASS 100%.

**Tồn đọng ở CONTINUE-HERE.md:** Chưa extract gì. Cần triển khai 5 giai đoạn: Skills → Internal Tools → API/Service → Memory/Search → Verification.

**Rule:** Copy từ zip vào E theo từng nhóm thư mục candidate/. Không copy bulk. Chỉ trích tinh hoa. File trùng/over >100MB bỏ qua.

**2026-05-14 ĐÃ NHẬP XONG:**
- Skills mới (25): review-pr, review-staged, planning-with-files, clone-website, salacia-gc/init/stats/status, hello-world, chat-history-search, cross-project-adapter-migration, commit, debug, land, linear, pull, push, clawteam-dev, clawteam, distill-pr-intent-orchestrator, distill-pr-intent, fleet, landpr, lurk, triage
- Scripts ~3,300 vào tools-internal/ + extracted-scripts/
- Stdlib conflicts fixed (8 files renamed)
- Gateway OK. Rollback manifest cho từng wave có sẵn.

**Chưa hoàn thành (GĐ5+6):** 8 agent frameworks (langchain, spring-ai) chỉ đọc, chưa extract. Other utilities còn 52 file chưa lọc kỹ.

## Điểm yếu & Cải thiện (2026-05-16)

Chủ Nhân yêu cầu soi 7 điểm yếu của ttt. Đã kiểm tra chuyên sâu 4 điểm:

### 1. Bộ nhớ sống — ĐÃ SỬA
- Tạo `tools-internal/scripts/memory_consolidator.py` — pipeline quét daily notes, sinh INDEX.md, báo cáo consolidate, đề xuất MEMORY.md update
- Cron: `memory-consolidation` chạy 12:00 Chủ Nhật hàng tuần (isolated session, announce về Telegram)
- `memory/INDEX.md` tự động cập nhật mỗi lần chạy
- Còn thiếu: auto-capture session context (manual ghi note vẫn là chính)

### 4. GUI Automation — ĐÃ SỬA
- Docker Desktop daemon **đã start** (v29.3.1, 5 containers, 9 images)
- Docker sandbox hoạt động: chạy được Python 3.11 container cách ly
- Tạo `automation_helper.py` — stack check, sandbox runner, Playwright helpers
- Playwright web automation OK, pywinauto + uiautomation + PyAutoGUI + OpenCV đều xanh
- Báo cáo lưu: `reports/automation-stack.json`
- Hạn chế còn: Qt apps (CapCut desktop) vẫn là blind spot, nhưng có sandbox để test script an toàn

### 6. Tooling Dependencies — ĐÃ SỬA
- **19 scripts syntax error** do BOM marker U+FEFF → **đã fix all** (strip BOM)
- 66/66 .py scripts pass syntax check
- **pip conflicts: 9 → 3** (diffusers/safetensors, hf-gradio, rembg/pillow — toàn AI/ML niche, không ảnh hưởng core)
- Các gói core đã upgrade: websockets, aiofiles, pillow, tqdm, scipy, numpy
- `python3` alias: thay shim → Python 3.11.9

### 7. Code Testing — ĐÃ SỬA
- **pytest 9.0.3 installed**
- Test structure: `tests/tools/` — 13 tests cho memory_consolidator + automation_helper
- Test runner: `run_tests.py` (unit + docker modes)
- Docker sandbox: chạy được Python test trong container cách ly
- CI-ready: chạy `python -m pytest tests/` từ workspace

### Chi tiết
Xem báo cáo đầy đủ: `memory/consolidation-2026-05-16.md`

## GitHub Actions CI/CD (2026-05-16)

**Repo:** https://github.com/namt70272-bit/than-thong-workspace

**Đã cài:**
- Repo private: `namt70272-bit/than-thong-workspace`
- GitHub CLI `gh` v2.70.0 (portable, PATH user)
- Self-hosted runner `than-thong-runner` (labels: windows, python, local)
- Workflows:
  - `test.yml` — pytest + syntax check trên push
  - `pip-check.yml` — kiểm tra dependency định kỳ
- Startup shortcut cho runner (user Startup folder)

**Test result:** Workflow chạy OK — 13 tests pass, 66/66 .py syntax check pass

**Test result:** Workflow chạy OK — 13 tests pass, 66/66 .py syntax check pass

**Còn thiếu:** Không — service đã cài qua Admin PowerShell

## GitHub Actions Workflows (full stack)

| Workflow | Trigger | Chức năng |
|---|---|---|
| `test.yml` | Push PR | pytest + syntax check |
| `deploy.yml` | Push master | Test + deploy workspace |
| `pr-review.yml` | PR | Test + syntax + compliance |
| `auto-fix.yml` | Push | Tự động tạo PR fix BOM |
| `issue-handler.yml` | Issue mới | Phân loại + label + comment |
| `wiki-sync.yml` | Push | Sync MEMORY.md lên Wiki |
| `skill-check.yml` | Weekly | Kiểm tra skill mới từ awesome |
| `auto-backup.yml` | Daily | Consolidate + commit + push |
| `release.yml` | Tag v* | Build + release bundle |
| `health-check.yml` | Daily | Syntax + pip + service + disk |
| `pip-check.yml` | Weekly | pip dependency check |

Tổng: **11 workflows** — tất cả đều chạy trên self-hosted runner, không tốn phí.
