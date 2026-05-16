# Báo cáo khai thác: openclaw source code (commit 6667cbf)

**Nguồn:** `G:\đã xong\openclaw-6667cbfcec517421d29e5c91601249b246f03dcb`  
**Loại:** Source code OpenClaw tại một commit cụ thể (newer hơn npm package)  
**Dung lượng:** ~12 MB, 14k files, 821 thư mục  
**Ngày phân tích:** 2026-05-11

---

## 1. Sơ đồ cấu trúc

```
openclaw-6667cbf/
├── src/            → 29 MB, 4.5K files — TypeScript source chính (quá lớn, bỏ qua)
├── docs/           → 11.4 MB, 512 files — documentation (tham khảo)
├── skills/         → 53 skills official (quan trọng)
│   ├── SKILL.md    → mỗi skill có 1 file
│   ├── scripts/    → extra tool scripts (model_usage, skill-creator, tmux, video-frames...)
│   └── references/ → tài liệu tham khảo đi kèm (1password, himalaya...)
├── extensions/     → 2.5 MB — extension implementations (tham khảo)
├── .agents/        → agent definitions
├── .pi/            → prompts + extensions
├── packages/       → SDK contracts
├── scripts/        → build/dev scripts
└── qa/ + test/     → test suites
```

---

## 2. Phân loại vùng

| Vùng | Nhãn | Mô tả |
|------|------|-------|
| `skills/*/SKILL.md` | **updated config** | 25 skills có update từ 8->423 bytes so với npm |
| `skills/*/scripts/` | **executable** | Python/bash/Node scripts — model_usage, skill-creator, tmux, video-frames |
| `skills/*/references/` | **docs** | Tài liệu hướng dẫn CLI config (1password, himalaya) |
| `skills/*/bin/` | **executable** | sherpa-onnx-tts (Node.js TTS bridge) |
| `skills/*/examples/` | **docs** | Lobster workflow examples (taskflow) |
| `skill-creator/scripts/` | **executable** | 4 Python scripts (init, package, validate skill) |
| `src/` | **source** | ❌ TypeScript code gốc — không cần vì dùng npm |
| `docs/` | **docs** | 📌 Tham khảo khi cần |
| `.github/workflows/` | **CI/CD** | ❌ GitHub Actions specific |
| `extensions/` | **source** | 📌 Tham khảo extension pattern |

---

## 3. Giá trị khai thác được

### A. Updated SKILL.md (đáng lấy nhất)

16 skills có update >100 bytes so với npm:

| Skill | Tăng | Nội dung mới |
|-------|------|-------------|
| `skill-creator` | +423 | Hướng dẫn dùng init_skill, package, validate scripts |
| `github` | +319 | Bổ sung workflow GitHub mới |
| `node-connect` | +260 | Thêm mobile pairing protocol |
| `taskflow` | +262 | Thêm Lobster workflow examples, config mới |
| `healthcheck` | +211 | Thêm audit checklist, SSH firewall checks |
| `gh-issues` | +237 | Thêm gh CLI workflow |
| `clawhub` | +179 | Skill install workflow |
| `weather` | +165 | Thêm forecast options |
| `things-mac` | +163 | macOS task management |
| `himalaya` | +127 | Email config updates |
| `taskflow-inbox-triage` | +127 | Inbox triage pattern |
| `xurl` | +126 | URL fetch options |
| `apple-notes` | +113 | macOS notes API |

⚠️ `coding-agent` (-1763) và `gifgrep` (-426) là **thu nhỏ**, không phải update.

### B. Extra scripts (25 files — KHÔNG có trong workspace)

| File | Loại | Công dụng |
|------|------|-----------|
| `skill-creator/scripts/init_skill.py` | Python | Tạo skill mới từ template |
| `skill-creator/scripts/package_skill.py` | Python | Đóng gói skill → .skill file |
| `skill-creator/scripts/quick_validate.py` | Python | Validate skill nhanh |
| `skill-creator/scripts/test_*.py` | Python | Tests cho skill-creator |
| `model-usage/scripts/model_usage.py` | Python | Thống kê chi phí LLM từ CodexBar logs |
| `model-usage/scripts/test_model_usage.py` | Python | Test |
| `openai-whisper-api/scripts/transcribe.sh` | Bash | Gọi Whisper API từ CLI |
| `sherpa-onnx-tts/bin/sherpa-onnx-tts` | Node.js | Bridge TTS daemon |
| `tmux/scripts/find-sessions.sh` | Bash | Liệt kê tmux sessions |
| `tmux/scripts/wait-for-text.sh` | Bash | Poll tmux pane cho text pattern |
| `video-frames/scripts/frame.sh` | Bash | Trích frame từ video (ffmpeg) |
| `taskflow/examples/inbox-triage.lobster` | Lobster | Mẫu inbox triage workflow |
| `taskflow/examples/pr-intake.lobster` | Lobster | Mẫu PR intake workflow |
| `1password/references/*.md` | Docs | CLI examples + get-started |
| `himalaya/references/*.md` | Docs | Email client config + MML |
| `model-usage/references/*.md` | Docs | CodexBar CLI commands |

### C. Docs (tham khảo khi cần)

- 11.4 MB documentation cập nhật
- 2 thư mục docs mới: `.generated/` và `refactor/`

---

## 4. Kiểm tra trùng lặp với hệ thống

| Item | Trùng? | Mức độ |
|------|--------|--------|
| **SKILL.md** names | ✅ TRÙNG (đều có SKILL.md) | KHÔNG nguy hiểm — khác path |
| **Script tên file** | ✅ KHÔNG trùng | Không file `.py`, `.sh` nào trùng tên với workspace |
| **Utils** | ✅ KHÔNG trùng | `prompt_utils.py`, `rate_limiter.py` không có trong repo |
| **Skills đang ENABLED** | ✅ KHÔNG có | Config hiện tại: 53 skill entries đều DISABLED |
| **Config path** | ✅ KHÔNG trùng | File sẽ đặt ở `E:\KY-DATA\OpenClaw\projects\khai-thac-candidates\` riêng |
| **Tên biến env** | ✅ KHÔNG trùng | Không có env var nào overlap |

**Kết luận:** Không có rủi ro trùng lặp hay chồng lấn khi nhập các file này vào E.

---

## 5. Kế hoạch nhập vào ổ E

### 5a. Cấu trúc thư mục đích

```
E:\KY-DATA\OpenClaw\projects\khai-thac-candidates\openclaw-source\
├── skills-updated/
│   ├── node-connect.SKILL.md          ← bản mới nhất
│   ├── taskflow.SKILL.md
│   ├── healthcheck.SKILL.md
│   ├── skill-creator.SKILL.md
│   ├── weather.SKILL.md
│   └── [các skill update >100 bytes khác]
├── scripts/
│   ├── skill-creator/
│   │   ├── init_skill.py
│   │   ├── package_skill.py
│   │   ├── quick_validate.py
│   │   └── test_*.py
│   ├── model-usage/
│   │   ├── model_usage.py
│   │   └── test_model_usage.py
│   ├── whisper/transcribe.sh
│   ├── tmux/find-sessions.sh
│   ├── tmux/wait-for-text.sh
│   └── video/frame.sh
├── references/
│   ├── 1password/
│   ├── himalaya/
│   └── model-usage/
├── examples/
│   ├── inbox-triage.lobster
│   └── pr-intake.lobster
└── README-source.md
```

### 5b. Thứ tự thực hiện

```
Bước 1: Tạo thư mục đích
  mkdir -p E:\KY-DATA\OpenClaw\projects\khai-thac-candidates\openclaw-source

Bước 2: Copy SKILL.md mới nhất
  Copy các file SKILL.md từ source → skills-updated/
  Chỉ lấy 16 skill có update >100 bytes
  KHÔNG copy đè lên npm package hay workspace

Bước 3: Copy scripts
  Copy 25 extra files → scripts/ và references/ tương ứng
  Giữ nguyên cấu trúc thư mục con

Bước 4: Verify
  Chạy thử Python scripts (import test)
  Kiểm tra SKILL.md frontmatter parse được không

Bước 5: Ghi nhật ký
  Cập nhật TOOLS.md với nguồn gốc
  Ghi commit hash + ngày lấy
```

### 5c. Rủi ro nếu copy nguyên thư mục

| Hành động | Rủi ro |
|-----------|--------|
| Copy `skills/` vào `workspace/skills/` | Ghi đè khai-thac, billing-guard, review-code |
| Copy `src/` vào E | Lãng phí 29 MB, không dùng được |
| Copy `extensions/extension-name/` | Phụ thuộc TypeScript build, không dùng trực tiếp |
| Nối SKILL.md vào config đang chạy | Skill trong npm package đã được load tự động — khỏi cần |

---

## 6. Tóm tắt

| Mục | Số lượng | Công dụng |
|-----|----------|-----------|
| Updated SKILL.md | 16 files | Reference cho skill update |
| Python scripts | 6 files | Tạo/package skill, thống kê cost |
| Bash scripts | 4 files | Tmux, video frame, whisper |
| Node.js script | 1 file | TTS bridge |
| Docs references | 5 files | Hướng dẫn CLI config |
| Workflow examples | 2 files | Lobster mẫu |
| **Tổng cộng** | **~34 files, <300 KB** | **An toàn, không trùng lặp** |

---

*Báo cáo theo quy trình khai-thac: inventory → đọc → chọn lọc → dựng bản tối thiểu → kiểm tra trùng lặp.*
