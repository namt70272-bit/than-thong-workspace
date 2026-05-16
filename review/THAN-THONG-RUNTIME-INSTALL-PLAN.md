# Than-thong Runtime Install Plan

## Mục tiêu
Đưa `than-thong-guard` từ skeleton thành plugin guard cài được trong OpenClaw local runtime.

## Đã có
- `runtime-guard/than-thong-guard/index.ts`
- `runtime-guard/than-thong-guard/openclaw.plugin.json`
- `runtime-guard/than-thong-guard/package.json`
- internal hooks:
  - `hooks/than-thong-bootstrap`
  - `hooks/than-thong-command-guard`

## Cách gắn vào runtime (dự kiến)
### 1. Plugin guard
- discover plugin từ path local
- hoặc pin qua `plugins.entries.than-thong-guard`
- mục tiêu: cho runtime load `before_tool_call` hook từ plugin này

### 2. Internal hooks
- enable internal hooks
- enable:
  - `than-thong-bootstrap`
  - `than-thong-command-guard`

## Lý do chưa patch config ngay
- cần tránh sửa config mù khi chưa tra field schema path chính xác bằng control-plane/config tool phù hợp
- bước tiếp nên là lookup exact config path/hook enable path rồi mới patch

## Mục tiêu patch sau khi xác nhận path
- load workspace hook directories
- enable internal hooks entries
- đăng ký local plugin path cho `than-thong-guard`

## Kết luận
Mặt file/plugin skeleton đã sẵn sàng. Việc còn lại là gắn đúng vào config/runtime của OpenClaw một cách chính xác và an toàn.
