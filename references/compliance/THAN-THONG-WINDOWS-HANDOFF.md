# Thần thông Windows Admin Handoff

## Mục tiêu
Khi `thần thông` chạm admin boundary trên Windows, không dừng mơ hồ mà phải bàn giao ngắn, rõ, đúng lệnh.

## Khi nào kích hoạt handoff
- Restart/stop/start service
- Add/remove printer
- Driver registration
- Firewall / network adapter changes
- Scheduled task mức system
- Registry/system policy nhạy cảm
- Cài/gỡ package mức máy

## Output chuẩn
Mỗi handoff nên có đúng 4 phần:
1. Vấn đề
2. Vì sao cần admin
3. Lệnh cần chạy
4. Output cần dán lại

## Mẫu
### Vấn đề
Printer object bị mất nhưng USB device còn hiện diện.

### Vì sao cần admin
Cần restart Print Spooler và đăng ký lại printer object, đây là thao tác service/driver layer của Windows.

### Lệnh cần chạy
```powershell
Restart-Service Spooler -Force
Add-Printer -Name "EPSON L1250 Series" -DriverName "EPSON L1250 Series" -PortName "USB001"
Get-Printer | ft Name,PortName,DriverName,PrinterStatus
```

### Output cần dán lại
- toàn bộ output terminal
- lỗi nếu có

## Rule vận hành
- Ưu tiên 1 handoff gọn thay vì nhiều lệnh rời
- Chỉ sinh lệnh khi đã chẩn đoán đủ tốt
- Nếu có rollback, phải ghi ngay dưới lệnh chính
- Sau khi user dán output, `thần thông` phải tiếp tục từ trạng thái mới thay vì lặp lại từ đầu
