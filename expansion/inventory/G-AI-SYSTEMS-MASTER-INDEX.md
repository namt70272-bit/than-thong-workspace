# G:\Ai — Master Index for Safe Expansion

Nguyên tắc: chỉ dùng làm nguồn rà soát/trích lọc. Không nhập nguyên repo vào hệ đang chạy.

## Nguồn
- Đường dẫn: `G:\Ai`
- Mục tiêu: mở rộng hệ thống theo 16 mảng, ưu tiên A0 (không rủi ro)
- Quy ước lưu trữ: mọi dữ liệu làm việc/candidate/import đều nằm trên ổ `E:`

## Phân tầng rủi ro
- `A0` — Không rủi ro: docs, rules, prompt, ontology, config mẫu, workflow mẫu
- `A1` — Rủi ro thấp có kiểm soát: chỉ xem xét qua package/sandbox sau
- `B` — Chặn: service, DB, migration, source app lớn, port, runtime override

## 16 mảng
1. Quản lý agent
2. Quản lý công việc
3. Tự động hóa
4. Tổ chức tri thức / memory
5. Quản lý code
6. Quản trị hệ thống
7. Tích hợp API
8. Hệ thống tra cứu
9. Mạng agent
10. Tài liệu tổ chức
11. Cấu hình / tuân thủ
12. Hệ thống CLI
13. Quản lý tài liệu
14. Quản lý nội dung
15. Điều khiển thiết bị / browser
16. Hạ tầng / deploy / platform

## Quy tắc đồng bộ
- Không tạo dữ liệu làm việc mới trên `C:`
- Không import state/cache/build vào `E:`
- Chỉ trích các phần tối thiểu vào `E:\...\workspace\expansion\imports\...`
- Mỗi import phải có nguồn và lý do chọn
