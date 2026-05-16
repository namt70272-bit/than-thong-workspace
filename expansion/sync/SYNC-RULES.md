# SYNC RULES — Đồng bộ an toàn

## Luồng đồng bộ chuẩn
1. `E:\KY-DATA\OpenClaw\mang-he-thong\...` = khu staging ngoài runtime
2. `workspace/expansion/candidates/...` = candidate đã chắt lọc
3. đích cuối trong `workspace/...` = chỉ nhận bản tối thiểu đã duyệt

## Không được làm
- Không copy nguyên repo vào workspace
- Không sync tự động 2 chiều
- Không để file staging trở thành nguồn sự thật runtime
- Không nhập DB/cache/build/node_modules/dist/state
- Không đưa `.env`, token, secrets, credentials vào candidate nếu chưa có lý do rõ ràng

## Đồng bộ 1 chiều
- staging ngoài -> candidate trong workspace
- candidate -> đích cuối
- không làm chiều ngược lại trừ khi cập nhật hồ sơ thủ công

## Quy tắc đặt tên
- Ở staging: tiếng Việt để dễ nhìn
- Ở candidate/đích cuối: ưu tiên tiếng Anh, rõ chức năng

## Kiểm tra trước khi sync
- [ ] file là docs/template/rules/snippet an toàn
- [ ] không có side-effect khi tồn tại trong workspace
- [ ] không trùng tên file đích đang dùng
- [ ] có thư mục đích rõ ràng theo IMPORT-MAP
- [ ] có ghi nguồn và lý do chọn

## Kiểm tra sau khi sync
- [ ] đọc lại file đã vào đúng chỗ
- [ ] không đè nhầm file cũ
- [ ] root workspace không phát sinh file rác
- [ ] cập nhật queue/rollback log
