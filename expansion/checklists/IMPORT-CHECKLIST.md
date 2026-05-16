# IMPORT CHECKLIST

## Trước khi lấy bất cứ thứ gì từ nguồn ngoài
- [ ] Đã inventory file/thư mục và dung lượng
- [ ] Đã đọc README/docs/config mẫu trước
- [ ] Đã xác định đây là docs/template/rule hay executable/service
- [ ] Không có `.db`, `.sqlite`, `.cache`, `dist`, `build`, `node_modules`, runtime state
- [ ] Không có `.env`, credentials, secrets, tokens cần nhập vào hệ
- [ ] Không đè skill/config/runtime đang chạy
- [ ] Không mở port, không tạo service, không migration
- [ ] Có thể trích thành file tối thiểu thay vì copy nguyên repo

## Trước khi nhập vào runtime thật
- [ ] Đã có candidate tối thiểu
- [ ] Đã test cô lập
- [ ] Có rollback
- [ ] Chủ Nhân đã duyệt nếu thay đổi có tác động hệ thống
