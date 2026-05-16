---
name: top
description: Lớp điều hành local-first/internal-first của workspace. Dùng `top` như cổng vào chuẩn trước mọi tác vụ nội bộ: route, gate, validate, sync, rollback, dashboard, và chặn mọi đường có nguy cơ phát sinh billing/provider usage.
---

# Top

`top` là tên chính thức mới cho lớp điều hành nội bộ của workspace.

## Vai trò
- cổng vào mặc định trước mọi tác vụ nội bộ
- ưu tiên tool nội bộ/local-first
- chặn rủi ro phát sinh billing/provider usage
- chỉ cho Internet read-only khi thật sự cần

## Bộ công cụ gắn kèm

### Workspace / Core
- `top_gate.py`
- `top_wrapper.py`
- `top_console.py`
- `preflight_runner.py`
- `import_orchestrator.py`
- `ops_dashboard.py`

### Windows-side (top-win)

#### Quan sát và kiểm tra
- `top_win_audit.py` — quét ổ đĩa, OS, biến môi trường
- `top_win_env_audit.py` — kiểm tra biến môi trường
- `top_win_svc_audit.py` — kiểm tra service Windows
- `top_win_startup_audit.py` — chương trình khởi động cùng Windows
- `top_win_process_audit.py` — theo dõi process quan trọng
- `top_win_disk_health.py` — sức khỏe ổ đĩa
- `top_win_system_restore.py` — kiểm tra điểm khôi phục

#### Dọn dẹp và tối ưu
- `top_win_cleanup.py` — tìm temp/junk toàn máy
- `top_win_tighten.py` — gợi ý siết chặt (service/variable)

#### Kho dữ liệu
- `top_win_data_map.py` — kho dữ liệu trên các ổ

#### Dashboard
- `top_win_dashboard.py` — dashboard tổng quan Windows
- `top_win_full_dashboard.py` — dashboard đầy đủ Windows-side

Dùng qua:
- `top_console win-<tên>` (ví dụ: `top_console win-svc`, `top_console win-full`)
- Tất cả đều qua gate `top` trước

Và toàn bộ `tools-internal/scripts/`

## Tương thích ngược
- `billing` vẫn tồn tại như alias legacy
- mọi tài liệu mới nên ưu tiên dùng tên `top`

## Rule of engagement
1. Nếu làm được bằng nội bộ -> `top` phải gánh trước
2. Nếu cần Internet -> chỉ read-only, tránh đường trả phí
3. Nếu có nguy cơ phát sinh billing/provider cost -> chặn và báo
4. Tác vụ nội bộ nên đi qua `top_console.py` / `top_wrapper.py` / `preflight_runner.py`
