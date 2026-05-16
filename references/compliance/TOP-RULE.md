# TOP RULE

## Tên luật chính thức mới
**top**

## Quan hệ với tên cũ
- `top` là tên chính thức mới
- `billing` là tên legacy alias để tương thích ngược
- mọi tài liệu mới nên gọi lớp điều hành này là `top`

## Mục tiêu
`top` là lớp điều hành nội bộ local-first của workspace:
- route tác vụ nội bộ
- gate rủi ro provider/billing
- validate candidate
- sync một chiều
- rollback
- dashboard/audit

## Luật cứng
- nội bộ/local-first trước
- tránh provider/billing tuyệt đối nếu chưa được duyệt
- Internet chỉ read-only khi thật sự cần
- mọi tác vụ nội bộ nên đi qua `top_*` entrypoints trước
