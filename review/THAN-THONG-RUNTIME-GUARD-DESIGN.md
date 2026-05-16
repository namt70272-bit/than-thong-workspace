# Thần thông Runtime Guard Design

## Mục tiêu
Đưa `thần thông` từ lớp workspace policy/supervisor lên lớp runtime guard của OpenClaw để giảm trôi mạnh hơn.

## Hook phù hợp nhất
### 1. Plugin hook: `before_tool_call`
Dùng để:
- chặn tool có nguy cơ billing/quota/provider trả phí
- chặn tool external nếu chưa được policy cho phép
- tạo lớp preflight trước khi tool thật chạy

Đây là điểm móc mạnh nhất vì nó nằm ngay **trước execution của tool**.

### 2. Internal hooks
Các event nên tận dụng:
- `agent:bootstrap` — nhắc/ghim default behavior khi bootstrap session
- `message:received` — có thể annotate/log inbound intent
- `command:new` / `command:reset` — tái khẳng định guard sau reset/new

## Kiến trúc đề xuất
Inbound request
-> OpenClaw runtime
-> Than-thong runtime guard (plugin hook)
-> nếu safe/local/offline thì cho tiếp
-> nếu billing/quota/external risk thì block ngay
-> workspace supervisor xử lý route local

## 2 lớp guard
### Guard A — Runtime tool guard
- nơi: plugin hook `before_tool_call`
- nhiệm vụ:
  - block `web_search`, `web_fetch`, image/music/video generation, external messaging path nếu policy cấm
  - block paid-provider path theo rule thần thông
  - log tool attempt bị chặn

### Guard B — Bootstrap/session guard
- nơi: internal hooks
- nhiệm vụ:
  - nhắc/thêm note vào bootstrap context
  - bảo đảm session mới/reset vẫn bám policy thần thông-first

## Deliverables
### Plugin guard
- `runtime-guard/than-thong-guard/`
  - `HOOK.md` hoặc plugin manifest/spec
  - `handler.ts` hoặc plugin entry
  - policy map cho blocked tools

### Internal hook pack
- `hooks/than-thong-bootstrap/`
- `hooks/than-thong-command-guard/`

## Tool policy gợi ý ban đầu
### Chặn mặc định
- `web_search`
- `web_fetch`
- `image_generate`
- `music_generate`
- `video_generate`
- mọi tool dẫn tới provider trả phí / external network khi không có allow cụ thể

### Cho phép local-first
- `read`, `write`, `edit`, `apply_patch`
- `exec` (vẫn qua policy riêng)
- `process`
- `memory_*`
- `session_status`
- `sessions_*`
- `cron` (nếu chỉ local reminder/workflow nội bộ)

## Giai đoạn thực thi
### Phase 1
- tạo internal hook bootstrap guard
- tạo plugin guard skeleton cho `before_tool_call`

### Phase 2
- nối policy blocked-tools
- log vi phạm vào workspace record

### Phase 3
- cân nhắc tích hợp config/plugin load thực tế

## Kết luận
Nếu muốn giảm trôi mạnh hơn, không thể chỉ dựa vào AGENTS.md/TOOLS.md.
Cần lớp runtime guard bám vào hook của OpenClaw, và đây là hướng khả thi nhất đã xác định được từ docs local.
