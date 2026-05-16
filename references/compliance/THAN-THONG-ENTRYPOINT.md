# Thần thông Entrypoint Policy

## Rule chính thức
Mọi mệnh lệnh local phải đi qua `thần thông` trước.
Mọi câu lệnh/câu tự nhiên đều được coi là input cho `thần thông` trước khi rẽ sang bất kỳ công cụ nội bộ nào khác.

## Billing / Quota safety
Bất kỳ thứ gì đi qua `thần thông` đều không được:
- dùng billing
- dùng quota trả phí
- top-up / credit / token trả phí
- gọi provider/API trả phí

Nếu có dấu hiệu này, `thần thông` phải chặn ngay ở cửa đầu tiên.

## Thứ tự xử lý
1. `thần thông` nhận raw request
2. `thần thông` gate billing/quota/local-first
3. `thần thông` route command phù hợp
4. `thần thông` thực thi local nếu làm được
5. Nếu `thần thông` không có command hoặc không xử lý được thì mới gọi script/tool nội bộ khác
6. Chỉ sau đó mới cân nhắc đường Internet / external

## Entrypoint chuẩn
- `python tools-internal\scripts\than_thong_console.py <lệnh>`
- `python tools-internal\scripts\than_thong_entry.py <lệnh>`
- `than-thong.cmd <lệnh>`

## Ví dụ
- `than-thong.cmd duplicate`
- `than-thong.cmd win-repair-printer suggest`
- `than-thong.cmd win-events suggest 24`

## Ý nghĩa
- Chuẩn hóa một cửa vào
- Giảm việc gọi tắt rời rạc vào từng script
- Giữ đúng local-first + auth-first + billing-safe
