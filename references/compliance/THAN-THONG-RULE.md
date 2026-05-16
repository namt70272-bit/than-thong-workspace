# THẦN THÔNG RULE

## Tên luật chính thức
**thần thông**

## Quan hệ với tên cũ
- `thần thông` là tên chính thức
- `top` và `billing` là alias legacy để tương thích
- mọi tài liệu mới nên gọi lớp điều hành này là `thần thông`

## Mục tiêu
`thần thông` là lớp điều hành nội bộ local-first của workspace:
- route tác vụ nội bộ
- gate rủi ro provider/billing
- validate candidate
- sync một chiều
- rollback
- dashboard/audit
- quản lý Windows-side

## Luật cứng
- nội bộ/local-first trước
- tránh provider/billing tuyệt đối nếu chưa được duyệt
- Internet chỉ read-only khi thật sự cần
- mọi tác vụ nội bộ nên đi qua `thần thông` entrypoints trước
