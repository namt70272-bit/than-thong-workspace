# Thần thông Windows Capability Matrix

## Thang đánh giá
- Đọc được: có thể lấy trạng thái / inventory / log
- Chẩn đoán được: có thể khoanh vùng nguyên nhân tương đối đáng tin
- Sửa không admin: sửa được bằng quyền thường
- Sửa cần admin: có đường sửa rõ nhưng cần elevated PowerShell/UI

| Domain | Đọc được | Chẩn đoán được | Sửa không admin | Sửa cần admin | Ghi chú |
|---|---:|---:|---:|---:|---|
| File/workspace | Cao | Cao | Cao | Thấp | Mạnh nhất hiện tại |
| Process quan sát | Cao | Trung bình-cao | Thấp | Trung bình | Kill process còn tùy quyền |
| Service trạng thái | Cao | Trung bình | Thấp | Cao | Restart/change startup thường cần admin |
| Printer queue | Trung bình-cao | Trung bình-cao | Trung bình | Cao | Queue có thể xử lý, registration thì khó |
| Printer driver/registration | Thấp-trung bình | Trung bình | Thấp | Cao | Điểm yếu hiện tại |
| USB/PnP detect | Trung bình | Trung bình | Thấp | Trung bình-cao | Thấy thiết bị nhưng repair còn yếu |
| Startup apps | Cao | Trung bình | Trung bình | Trung bình-cao | Tùy scope user/system |
| Env vars | Cao | Trung bình | Trung bình | Trung bình-cao | System env thường cần admin |
| Disk / cleanup | Cao | Cao | Trung bình | Trung bình-cao | Một số vùng bảo vệ bị chặn |
| Event log correlation | Thấp | Thấp-trung bình | Không áp dụng | Không áp dụng | Cần nâng cấp thêm |
| Network basic audit | Trung bình-cao | Trung bình | Thấp | Trung bình-cao | Reset adapter/firewall cần admin |
| Firewall / policy | Thấp | Trung bình | Thấp | Cao | Nằm sâu trong admin boundary |
| Driver/package layer | Thấp | Thấp-trung bình | Thấp | Cao | Cần playbook riêng |
| Audio/Bluetooth/camera | Thấp-trung bình | Thấp-trung bình | Thấp | Trung bình-cao | Chưa có module chuyên biệt |

## Kết luận ngắn
- Mạnh: audit, inventory, local analysis
- Khá: chẩn đoán nhiều lỗi user-level
- Yếu: repair system-level, driver, service control, printer registration
- Nâng cấp ưu tiên: handoff + repair playbooks + event correlation
