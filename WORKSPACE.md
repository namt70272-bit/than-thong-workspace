# OpenClaw Workspace Guide

**Version:** 2.1  
**Audited:** 2026-05-12  
**Location:** `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`

## Mục đích

Đây là workspace cục bộ cho OpenClaw: chứa identity, memory, skills, utilities, scripts, references, reports, và tài liệu điều hướng.

## Cấu trúc thực tế hiện tại

```text
workspace/
├── .git/              Git metadata
├── .openclaw/         Runtime workspace state
├── archive/           Nội dung deprecated giữ lại để tham chiếu
├── config/            YAML/config templates
├── examples/          Workflow examples (.lobster)
├── khai-thac/         Ghi chú khai thác nguồn ngoài
├── memory/            Nhật ký theo ngày + hướng dẫn memory
├── references/        Tài liệu tham chiếu nhập vào
├── reports/           Báo cáo audit / analysis đã sinh
├── scripts/           Script chạy trực tiếp
├── skills/            Formal skills + tooling cho skills
├── utils/             Python helper dùng lại
└── *.md               Tài liệu gốc ở root
```

## Các file root quan trọng

- `AGENTS.md` — luật vận hành workspace
- `SOUL.md` — persona / vibe
- `IDENTITY.md` — tên và marker nhận diện
- `USER.md` — preference của chủ nhân
- `TOOLS.md` — ghi chú local setup
- `README.md` — landing page ngắn
- `DIRECTORY-MAP.md` — bản đồ thư mục
- `SKILL-REGISTRY.md` — registry skills
- `REFERENCE-INDEX.md` — index references
- `CHANGES.md` — change log
- `HEARTBEAT.md` — checklist heartbeat

## Những gì đang có thật

### Skills
- `skills/billing-guard/`
- `skills/khai-thac/`
- `skills/review-code/`
- `skills/skill-creator/` *(tooling, không phải formal skill)*

### Utils
- `utils/prompt_utils.py`
- `utils/rate_limiter.py`

### Scripts
- `scripts/browser.py`
- `scripts/model_usage.py`
- `scripts/play_song.py`
- `scripts/tmux/`
- `scripts/video/`
- `scripts/whisper/`

### References
- `references/1password/`
- `references/himalaya/`
- `references/model-usage/`
- `references/awesome-skills-catalog/`

### Reports
Các báo cáo lịch sử đang nằm trong `reports/`, gồm audit hạ tầng OpenClaw, engram extraction, canonicalization, import planning.

## Điều hướng nhanh

### Muốn hiểu workspace
1. `README.md`
2. `DIRECTORY-MAP.md`
3. `SKILL-REGISTRY.md`
4. `REFERENCE-INDEX.md`

### Muốn dùng skill
1. `skills/README.md`
2. `skills/<skill-name>/SKILL.md`

### Muốn tìm tool chạy được
1. `scripts/README.md`
2. `utils/README.md`
3. `TOOLS.md`

### Muốn xem lịch sử / continuity
1. `memory/README.md`
2. `memory/*.md`
3. `reports/*.md`

## Ghi chú audit 2026-05-12

- File này đã được sửa để phản ánh **cấu trúc thực tế**, không còn liệt kê các path chưa tồn tại như `MEMORY.md`, `references/QUICK-REF.md`, `memory/INDEX.md`, `templates/`, hay `archives/`.
- Inventory thực tế tại thời điểm audit: **118 files**, **43 folders**, khoảng **655 KB** toàn workspace; nếu loại `.git` và `__pycache__` còn **78 files**, **24 folders**, khoảng **507 KB**.
- Dung lượng lớn nhất nằm ở `references/awesome-skills-catalog/README.md`.

## Quy ước bảo trì

- Tài liệu phải phản ánh cấu trúc đang tồn tại, không mô tả wish-list như thể đã có sẵn.
- Tooling cho skills phải ghi rõ là tooling, tránh bị hiểu nhầm là formal skill.
- Nội dung deprecated giữ trong `archive/`, không xóa vội.
- Nếu thêm folder lớn mới, cập nhật `DIRECTORY-MAP.md`, `README.md`, và file index liên quan.

## Trạng thái hiện tại

- Tổ chức: gọn, có chủ đích
- Billing posture: auth-first + local-first
- Security posture: chưa thấy secret thật nằm trong workspace; có script dùng API cần guard rõ
- Tài liệu: khá nhiều, nhưng cần tiếp tục giữ đồng bộ với trạng thái thật
