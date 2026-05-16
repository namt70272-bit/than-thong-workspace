# Lobster: OpenClaw-Native Workflow DSL

> Nguồn: G:\Ai\Lobster.zip  
> Trích xuất: thần thông, mảng 03 - Tự động hóa  
> Ngày: 2026-05-13

## Khái niệm
Lobster là workflow shell cho OpenClaw: workflow typed (JSON-first), pipeline, job, và approval gates.

## Vấn đề nó giải quyết
- LLM phải lập kế hoạch lại mỗi bước → tốn token
- Không có deterministic workflow
- Không có checkpoint approval
- Không resume được khi gián đoạn

## Lợi ích
- Chạy deterministic (không cần LLM re-plan mỗi bước)
- Dừng tại checkpoint, hỏi trước khi có side-effect
- Resume chính xác chỗ cũ
- Nhớ đã xử lý gì rồi

## Cách dùng
```
node bin/lobster.js "workflows.run --name github.pr.monitor --args-json '{\"repo\":\"openclaw/openclaw\",\"pr\":1152}'"
```

## Value cho hệ thống
Mẫu workflow deterministic có thể áp vào:
- pipeline import của thần thông
- TaskFlow pattern
- cron job có approval gate
