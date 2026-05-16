---
name: than-thong
description: Lớp điều hành local-first/internal-first của workspace. Dùng `thần thông` như cổng vào chuẩn trước mọi tác vụ nội bộ: route, gate, validate, sync, rollback, dashboard, và chặn mọi đường có nguy cơ phát sinh billing/provider usage.
---

# Thần Thông

`thần thông` là tên chính thức cho lớp điều hành nội bộ của workspace.

## Vai trò
- cổng vào mặc định trước mọi tác vụ nội bộ
- ưu tiên tool nội bộ/local-first
- chặn rủi ro phát sinh billing/provider usage
- chỉ cho Internet read-only khi thật sự cần
- quản lý Windows-side, dọn dẹp, audit, tối ưu

## Bộ công cụ gắn kèm
Dùng qua `thần thông` là tự động gọi:
- `than_thong_gate.py` → gate phân loại rủi ro
- `than_thong_wrapper.py` → wrapper cho script trusted
- `than_thong_console.py` → console điều hành
- và toàn bộ `tools-internal/scripts/`

## Tương thích ngược
- `top` và `billing` vẫn tồn tại làm alias legacy
- mọi tài liệu mới nên ưu tiên dùng tên `thần thông`

## Rule of engagement
1. Nếu làm được bằng nội bộ -> `thần thông` phải gánh trước
2. Nếu cần Internet -> chỉ read-only, tránh đường trả phí
3. Nếu có nguy cơ phát sinh billing/provider cost -> chặn và báo
4. Tác vụ nội bộ nên đi qua `than_thong_console.py` trước
