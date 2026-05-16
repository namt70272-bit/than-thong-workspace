# Thần thông Offline AI Roadmap

## Mục tiêu
Tạo một **AI nội bộ offline, độc lập, local-first** cho `thần thông` để xử lý các vấn đề nội bộ mà không đụng billing, quota, hay provider trả phí.

## Tầm nhìn
`thần thông` không chỉ là command gateway, mà là:
- offline supervisor
- local diagnostic agent
- local remediation planner
- local knowledge miner
- local route learner

## 4 bước đáng làm ngay
### Bước 1 — Mở rộng route coverage
Thêm domain mới:
- `win-repair-usb`
- `win-repair-audio`
- `local-search`
- `docs-miner`

Mục tiêu:
- giảm `unsupported`
- tăng khả năng xử lý câu tự nhiên
- tăng giá trị thực chiến offline

### Bước 2 — Learned Route Engine
Thêm cơ chế học từ các request chưa route được:
- ghi vào `than-thong-learned-routes.json`
- cho phép thêm mapping thủ công
- ưu tiên route đã học trước khi fallback keyword thường

Mục tiêu:
- thần thông tự thích nghi dần với cách ra lệnh của Chủ Nhân

### Bước 3 — Offline AI Assistant
Tạo một AI nội bộ không gọi provider trả phí, dùng local heuristics + rule engine + registry + parser.

Tên đề xuất:
- `than_thong_offline_agent.py`

Năng lực chính:
- hiểu yêu cầu nội bộ dạng tự nhiên
- phân tích tình trạng hệ thống từ file/log/output local
- đề xuất hành động local-first
- sinh handoff admin khi cần
- tuyệt đối không đụng billing/quota

### Bước 4 — Nền policy xuyên suốt
Chuẩn hóa luật để dù đổi mode/model/session thì trong workspace này vẫn giữ:
- first gate = thần thông
- offline-first
- no-billing
- no-quota
- no-paid-provider

## Kiến trúc đề xuất
User/Agent Request
-> `than_thong_entry.py`
-> `than_thong_supervisor.py`
-> `than_thong_blocklist.py`
-> `than_thong_offline_agent.py`
-> route / learned route / registry
-> local executor

## Thành phần mới nên có
- `tools-internal/scripts/than_thong_offline_agent.py`
- `tools-internal/scripts/than_thong_learned_router.py`
- `tools-internal/scripts/top_win_repair_usb.py`
- `tools-internal/scripts/top_win_repair_audio.py`
- `tools-internal/scripts/local_search_index.py`
- `tools-internal/scripts/local_docs_miner.py`

## Ưu tiên triển khai
### Wave 1
- learned router
- offline agent skeleton
- usb repair
- audio repair

### Wave 2
- local search index
- docs miner
- richer diagnostics

### Wave 3
- self-improving route suggestions
- capability scoring
- offline knowledge summaries

## Nguyên tắc bất biến
- Không dùng billing
- Không dùng quota trả phí
- Không gọi provider/model trả phí
- Chỉ local/offline/internal trước
- Khi không làm được thì trả lời rõ là không có route local an toàn

## Kết luận
Đây là hướng đúng để biến `thần thông` thành **siêu gateway + AI nội bộ offline** thay vì chỉ là router command.
