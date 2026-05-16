# Thần thông Windows Upgrade Plan

## Mục tiêu
Nâng `thần thông` từ mức audit/chẩn đoán mạnh lên mức **diagnose + repair handoff** tốt hơn trên Windows, đặc biệt cho các lỗi service, printer, device registration.

## Hiện trạng quan sát
Các script hiện có mạnh ở mảng:
- audit tổng quan (`top_win_audit.py`)
- service snapshot (`top_win_svc_audit.py`)
- process/startup/env/disk/cleanup/data map
- dashboard tổng hợp qua `than_thong_console.py`

Điểm còn thiếu:
1. Chưa có command repair chuyên biệt cho Windows
2. Chưa có playbook riêng cho printer/audio/network/device
3. Chưa có lớp admin handoff rõ ràng khi bị chặn bởi quyền
4. Chưa có correlation engine cho Event Viewer + PnP + service
5. Chưa có capability matrix để biết tác vụ nào đọc được / sửa được / cần admin

## Đánh giá điểm yếu lớn
### 1) Admin boundary
- Không tự vượt qua được service control / driver registration / policy change
- Hiện chỉ chẩn đoán được, còn repair phải nhờ PowerShell admin/UI

### 2) Repair coverage còn mỏng
- Có scan nhưng thiếu lệnh sửa kiểu `win-repair-*`
- Ca printer vừa rồi là ví dụ rõ nhất

### 3) Thiếu peripheral playbooks
- Printer
- Audio
- USB device
- Bluetooth
- Camera/webcam

### 4) Thiếu event intelligence
- Chưa gom các nguồn log như:
  - PrintService
  - System / Service Control Manager
  - Kernel-PnP
  - UserPnp
- Kết quả là phát hiện dấu hiệu tốt nhưng kết luận còn thủ công

### 5) Handoff chưa mượt
- Khi cần admin, nên sinh ra đúng command + đúng lý do + bước tiếp theo
- Hiện flow này làm được bằng tay, chưa thành chuẩn của `thần thông`

### 6) Chưa có known-fix registry
- Chưa có DB nội bộ kiểu:
  - triệu chứng
  - nguyên nhân thường gặp
  - lệnh đọc
  - lệnh sửa không-admin
  - lệnh sửa admin

## Ước lượng capability hiện tại
### Không cần admin
- Read/audit: 85-90%
- Diagnose: 70-85%
- Repair: 40-60%

### Cần admin
- Diagnose: vẫn cao
- Repair: hiện phụ thuộc user handoff, chưa tự động hóa tốt

## Hướng nâng cấp ưu tiên
## Wave 1 — Admin handoff mode
Mục tiêu: gặp chỗ cần admin thì không bị khựng.

Cần thêm:
- module sinh handoff command chuẩn
- template output ngắn:
  - vấn đề gì
  - vì sao cần admin
  - chạy lệnh nào
  - dán output gì về lại
- mapping theo domain:
  - spooler/printer
  - services
  - network reset nhẹ
  - device rescan

Deliverables đề xuất:
- `tools-internal/scripts/win_admin_handoff.py`
- `references/compliance/THAN-THONG-WINDOWS-HANDOFF.md`

## Wave 2 — Windows repair pack
Mục tiêu: có các repair playbook nội bộ rõ ràng.

Command mới nên có:
- `win-repair-printer`
- `win-repair-audio`
- `win-repair-network-lite`
- `win-repair-usb-device`
- `win-repair-spooler`

Mỗi command nên có 3 mode:
- `audit`
- `suggest`
- `repair` (nếu không admin được thì sinh handoff)

Deliverables đề xuất:
- `tools-internal/scripts/top_win_repair_printer.py`
- `tools-internal/scripts/top_win_repair_spooler.py`
- `tools-internal/scripts/top_win_repair_usb.py`

## Wave 3 — Event log intelligence
Mục tiêu: tự nối các mảnh log thành chẩn đoán.

Nguồn log ưu tiên:
- `Microsoft-Windows-PrintService/Operational`
- `System`
- `Kernel-PnP`
- `UserPnp`
- `Service Control Manager`

Deliverables đề xuất:
- `tools-internal/scripts/win_event_correlator.py`
- `tools-internal/records/win-event-diagnosis.json`

## Wave 4 — Capability matrix + known fixes
Mục tiêu: biết rõ giới hạn và đường sửa.

Cần có:
- capability matrix cho từng domain Windows
- danh sách lỗi thường gặp + fix path
- score: đọc được / chẩn đoán được / sửa được / cần admin

Deliverables đề xuất:
- `references/compliance/THAN-THONG-WINDOWS-CAPABILITY-MATRIX.md`
- `references/compliance/THAN-THONG-WINDOWS-KNOWN-ISSUES.md`

## Đề xuất command routing mới
Nên mở rộng `ops_console.py` để có thêm command:
- `win-repair-printer`
- `win-repair-spooler`
- `win-repair-usb`
- `win-events`
- `win-handoff`

## Lộ trình làm thật
### Giai đoạn 1 (nhanh, giá trị cao)
1. Viết capability matrix
2. Viết admin handoff spec
3. Tạo printer repair playbook đầu tiên

### Giai đoạn 2
4. Thêm lệnh `win-repair-printer`
5. Thêm correlator log printer + PnP + service
6. Chuẩn hóa output `suggest next command`

### Giai đoạn 3
7. Mở sang audio / USB / network-lite
8. Gắn vào dashboard
9. Tạo known-fixes registry

## Khuyến nghị triển khai ngay
Bắt đầu bằng **printer domain** vì:
- vừa có case thật
- dễ kiểm chứng
- tác động rõ
- tạo mẫu cho các domain khác

## Việc nên làm ngay trong repo
1. Bổ sung command mới vào `ops_console.py`
2. Thêm script `top_win_repair_printer.py`
3. Thêm tài liệu capability + handoff
4. Chuẩn hóa format output cho ca cần admin

## Kết luận
`thần thông` hiện **mạnh ở audit và chẩn đoán**, nhưng với Windows vẫn thiếu lớp **repair orchestration**. Nâng cấp hoàn toàn khả thi, và hướng đi hiệu quả nhất là:

1. admin handoff
2. printer repair pack
3. event correlation
4. capability matrix
