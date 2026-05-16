---
name: billing
description: Luật vận hành cứng cho local-first/internal-first. Dùng skill này như cổng quyết định trước mọi tác vụ: ưu tiên tool nội bộ, chặn mọi đường có nguy cơ billing, chỉ cho phép Internet read-only khi thật sự cần và vẫn phải tránh provider trả phí.
---

# Billing

## Vai trò
Đây là skill gốc để thực thi luật `billing` của workspace.

Mọi tác vụ phải đi qua nguyên tắc này trước:
1. Ưu tiên công cụ nội bộ / local-first
2. Ưu tiên file, script, template, workflow, docs trên E:
3. Nếu có thể làm bằng nội bộ thì **phải** làm bằng nội bộ
4. Nếu có nguy cơ phát sinh billing -> **dừng, báo, không tự chạy**
5. Chỉ ngoại lệ cho Internet read-only khi thật sự cần, và vẫn phải tránh mọi đường dẫn trả phí

## Bộ công cụ gắn kèm
Dùng các script trong `tools-internal/scripts/` trước khi làm việc:
- `billing_gate.py` -> gate chính trước tác vụ
- `task_router.py` -> chọn công cụ nội bộ phù hợp
- `import_validator.py` -> kiểm candidate trước khi nhập
- `candidate_builder.py` -> đưa file an toàn vào candidate layer
- `sync_executor.py` -> sync one-way candidate -> đích cuối
- `rollback_manifest.py` -> tạo manifest rollback
- `duplicate_checker.py` -> scan duplicate
- `canonical_checker.py` -> phát hiện nhiều nguồn sự thật
- `domain_tracker.py` -> theo dõi 16 mảng
- `workspace_inventory.py` -> inventory workspace
- `find_junk.py` -> scan junk
- `index_domains.py` -> index mảng
- `ops_dashboard.py` -> tổng hợp tình trạng hệ thống nội bộ

## Rule of engagement
Trước khi ra quyết định thực thi, tự hỏi:
- Việc này có làm bằng nội bộ được không?
- Có cần Internet không?
- Có nguy cơ billing không?
- Có tool nội bộ nào gánh được không?

Nếu câu trả lời là:
- **nội bộ được** -> dùng tool nội bộ
- **cần Internet** -> chỉ đọc/kiểm tra, tránh provider trả phí
- **có nguy cơ billing** -> chặn và báo

## Kết quả mong muốn
Skill này biến luật `billing` thành cổng điều phối mặc định cho toàn bộ công việc trong workspace.
