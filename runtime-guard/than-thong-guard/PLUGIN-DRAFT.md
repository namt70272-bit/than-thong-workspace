# than-thong-guard (draft)

## Mục tiêu
Plugin/runtime guard cho OpenClaw dùng hook `before_tool_call` để chặn các tool path trái với policy thần thông.

## Hook mục tiêu
- `before_tool_call`

## Policy ban đầu
### Block mặc định
- `web_search`
- `web_fetch`
- `image_generate`
- `music_generate`
- `video_generate`

### Allow mặc định
- `read`, `write`, `edit`, `apply_patch`
- `exec`, `process`
- `memory_search`, `memory_get`
- `session_status`, `sessions_*`
- `cron` (nội bộ/local workflow)

## Hành vi
- nếu toolName thuộc blocklist -> trả `block: true`
- blockReason ghi rõ: thần thông runtime guard / billing-quota-external risk
- log ra workspace record để audit nội bộ

## Giai đoạn hiện tại
- mới là skeleton thiết kế + draft
- bước sau: tạo plugin entry TypeScript theo SDK `definePluginEntry` và đăng ký `api.on('before_tool_call', ...)`
