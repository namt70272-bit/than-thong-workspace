# Thần Thông Super Policy

## Mục tiêu
Biến `thần thông` thành cổng local-first mặc định, offline-first, no-billing, no-quota cho toàn bộ workflow nội bộ trong workspace.

## Luật cứng
1. Mọi lệnh phải đi qua `thần thông` trước.
2. `thần thông` là nơi nhận raw request đầu tiên.
3. `thần thông` phải ưu tiên route tới năng lực local/offline trước.
4. Bất kỳ thứ gì đi qua `thần thông` đều không được:
   - dùng billing
   - dùng quota trả phí
   - gọi provider/API trả phí
   - top-up / credit / token trả phí
5. Nếu request có dấu hiệu chạm các vùng trên, `thần thông` phải chặn ngay.
6. Chỉ khi `thần thông` xác nhận không có route local an toàn thì mới cho phép xét đến lớp nội bộ khác.
7. Chỉ khi đã qua các lớp trên mới cân nhắc external/internet, và vẫn phải tránh billing/quota.

## Mục tiêu kỹ thuật
- Gate đầu tiên
- Router đầu tiên
- Executor local đầu tiên
- Supervisor của offline toolchain
- Bộ nhớ route học dần

## Thành phần
- `than_thong_supervisor.py` — lớp điều phối đầu tiên
- `than_thong_router.py` — route câu tự nhiên sang năng lực local
- `than_thong_offline_registry.py` — registry năng lực offline/local
- `than_thong_blocklist.py` — tập luật chặn billing/quota/external-risk
- `than_thong_entry.py` — cửa vào chuẩn

## Rule vận hành
- Unknown request → cố route local trước
- Nếu không route được → trả `unsupported` có lý do
- Không được tự ý chuyển sang API/model trả phí
- Không được dùng quota trả phí để “giải quyết nhanh”

## Phạm vi áp dụng
- Workspace hiện tại
- Mọi flow local vận hành bởi agent trong workspace
- Là nền để sau này siết tiếp ở bootstrap/session layer
