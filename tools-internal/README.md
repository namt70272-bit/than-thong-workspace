# TOOLS-INTERNAL

Bộ công cụ nội bộ để gánh các công việc local-first mà không đụng billing.

## Mục tiêu
- xử lý inventory
- cleanup
- import tracking
- A0 extraction
- sync record
- duplicate/junk scan
- workspace indexing

## Nguyên tắc
- chỉ dùng local files/scripts
- không gọi dịch vụ trả phí
- không tạo dependency vào cloud/provider mới
- mọi dữ liệu lưu trên E:

## Thành phần
- `templates/` — mẫu record/template nội bộ
- `scripts/` — script nội bộ hỗ trợ quản trị
- `records/` — nhật ký thao tác nội bộ

## Core scripts under rule `billing`
- `scripts/billing_gate.py` — cổng kiểm tra local-first/billing risk trước tác vụ
- `scripts/task_router.py` — route tác vụ tới tool nội bộ phù hợp
- `scripts/preflight_runner.py` — chạy gate + route như cổng vào chuẩn
- `scripts/import_validator.py` — chặn candidate có env/db/build/cache/runtime risk
- `scripts/candidate_builder.py` — đưa file an toàn vào candidate layer có log
- `scripts/sync_executor.py` — sync one-way local
- `scripts/rollback_manifest.py` — tạo rollback manifest
- `scripts/import_orchestrator.py` — build + validate + sync + rollback trong một luồng
- `scripts/domain_tracker.py` — theo dõi tiến độ 16 mảng
- `scripts/duplicate_checker.py` — quét trùng nội dung trong vùng nhận
- `scripts/canonical_checker.py` — phát hiện nhiều nguồn sự thật
- `scripts/drift_checker.py` — kiểm tra lệch giữa candidate và workspace
- `scripts/wave_manager.py` — quản lý các wave nhập
- `scripts/ops_dashboard.py` — dashboard trạng thái record nội bộ
- `scripts/ops_console.py` — console điều hành nội bộ một lệnh
- `scripts/deep_validator.py` — kiểm nội dung sâu: secret hint, network hint, blocked path
- `scripts/trusted_registry.py` — registry script nội bộ trusted theo policy
- `scripts/real_rollback.py` — rollback delete/restore thực tế từ manifest/backup
- `scripts/workspace_inventory.py` — inventory workspace
- `scripts/find_junk.py` — scan junk nội bộ
- `scripts/index_domains.py` — index cấu trúc 16 mảng
- `scripts/record_writer.py` — ghi record JSONL chuẩn
