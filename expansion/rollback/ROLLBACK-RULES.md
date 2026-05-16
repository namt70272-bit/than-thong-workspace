# ROLLBACK RULES

## Mục tiêu
Nếu nhập candidate sai chỗ hoặc không còn cần, có thể gỡ sạch mà không làm bẩn runtime.

## Quy tắc
- Mỗi đợt nhập phải có 1 record trong `queue/IMPORT-QUEUE.md`
- Nếu sửa file có sẵn, phải backup trước vào `archive/` hoặc tạo patch log
- Ưu tiên thêm file mới hơn là sửa file lõi
- Không xóa file lõi nếu chưa có xác nhận

## Checklist rollback
- [ ] biết chính xác file nào đã thêm
- [ ] biết file nào đã sửa
- [ ] có bản trước khi sửa
- [ ] biết thư mục đích cuối
- [ ] đã cập nhật log rollback

## Chiến lược an toàn nhất
1. Thêm file mới vào `references/`, `examples/`, `config/` trước
2. Chỉ sửa file hiện có khi thật cần
3. Nếu candidate không đạt, xóa candidate trước, không đụng đích cuối
