# EXPANSION AREA

Khu này dùng để mở rộng hệ thống theo cách an toàn, có kiểm soát.

## Mục tiêu
- Không nhét thẳng repo/file ngoài vào runtime đang chạy
- Tách rõ: inventory, review, pattern extraction, candidate import
- Mọi nâng cấp đi qua quy trình: đọc -> chọn lọc -> dựng tối thiểu -> test cô lập -> mới cân nhắc nối thật

## Cấu trúc
- `inventory/` — danh mục nguồn ngoài, phân loại, risk map
- `domains/` — 16 mảng hệ thống, mỗi mảng một hồ sơ
- `plans/` — kế hoạch nâng cấp theo phase
- `checklists/` — checklist review/import/test
- `imports/safe-snippets/` — đoạn mã/quy tắc/config đã chắt lọc an toàn
- `imports/config-templates/` — config mẫu tối thiểu
- `imports/workflow-templates/` — workflow mẫu
- `imports/rules/` — policy/rule/prompt được trích riêng

## Quy ước
- Chỉ file đã chắt lọc mới được vào `imports/`
- Không để DB, cache, build, node_modules, dist, state cũ trong đây
- Không copy nguyên repo ngoài vào `workspace/`
- Mọi candidate phải ghi rõ nguồn và lý do chọn
