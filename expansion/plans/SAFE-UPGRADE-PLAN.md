# SAFE UPGRADE PLAN

## Phase 0 — Dọn chỗ, chuẩn hóa khu mở rộng
- Tạo khu `expansion/`, `review/`, `tmp-staging/`
- Gom file test/tải xuống/media rời khỏi root workspace
- Giữ root chỉ cho file lõi và thư mục lõi

## Phase 1 — Inventory 16 mảng
- Mỗi mảng tạo 1 hồ sơ trong `domains/`
- Với từng mảng: mục tiêu, nguồn liên quan, phần A0/A1/B, rủi ro, cách khai thác tối thiểu

## Phase 2 — Trích A0
- Chỉ đọc và chắt lọc docs/rules/templates/ontology/config mẫu
- Không chạy service, không cài package, không import state

## Phase 3 — Candidate tối thiểu
- Dựng snippet/config/workflow nhỏ trong `imports/`
- Gắn nguồn, lý do chọn, cách dùng

## Phase 4 — Test cô lập
- Chỉ test trên candidate riêng
- Nếu có port/dependency/runtime change thì tách hẳn sandbox

## Phase 5 — Nối thật từng phần
- Chỉ nối patch nhỏ nhất
- Một lần một thay đổi
- Có rollback rõ ràng
