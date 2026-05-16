# BÁO CÁO TOÀN CẢNH — THẦN THÔNG

**Ngày:** 2026-05-13  
**Tình trạng:** Hoạt động  
**Alias tương thích:** `top`, `billing`

---

## 1) THẦN THÔNG LÀ GÌ?

Thần thông là **lớp điều hành nội bộ** của OpenClaw workspace.  
Nó không phải một script — nó là một **hệ thống công cụ + luật + quy trình** để:

- **Gate** — mọi tác vụ đều được kiểm tra rủi ro billing/provider trước
- **Route** — tác vụ nội bộ được tự động chuyển đến công cụ phù hợp
- **Import** — đưa dữ liệu an toàn từ staging vào runtime qua nhiều lớp kiểm tra
- **Sync** — đồng bộ một chiều có log
- **Rollback** — gỡ import sai có backup
- **Dashboard** — tổng quan workspace + Windows
- **Windows Ops** — quản lý máy tính Windows-side
- **Audit** — kiểm tra compliance, duplicate, canonical, drift
- **Cleanup** — dọn rác, junk, file tạm

---

## 2) THẦN THÔNG CÓ GÌ?

### 2a) Luật và skill

| Thành phần | Vị trí |
|---|---|
| Luật chính | `references/compliance/THAN-THONG-RULE.md` |
| Skill chính | `skills/than-thong/SKILL.md` |
| Policy machine-readable | `tools-internal/policy/billing.policy.json` |

### 2b) 3 entrypoint chính

| Lệnh | Chức năng |
|---|---|
| `than_thong_gate.py` | Kiểm tra billing risk trước mọi tác vụ. Trả về allow/block/warn |
| `than_thong_wrapper.py` | Chạy trusted internal script sau khi qua gate |
| `than_thong_console.py` | Console điều hành nội bộ. Có subcommand cho mọi việc |

### 2c) Công cụ lõi (37 scripts)

#### Gate / Route (4)
- `billing_gate.py` — gate chính (engine)
- `preflight_runner.py` — gate + route trong một cổng
- `task_router.py` — route tác vụ tới tool phù hợp
- `billing_wrapper.py` — wrapper trusted script

#### Import pipeline (6)
- `candidate_builder.py` — xây candidate từ staging
- `import_validator.py` — kiểm tra candidate nhanh
- `deep_validator.py` — kiểm tra sâu: secret, network, blocked path
- `sync_executor.py` — sync một chiều có log
- `import_orchestrator.py` — build + validate + deep-validate + backup + sync + rollback + record
- `rollback_manifest.py` — sinh manifest

#### Rollback thực tế (1)
- `real_rollback.py` — delete hoặc restore từ `.bak`

#### Kiểm tra / Audit (6)
- `domain_tracker.py` — theo dõi 16 mảng
- `duplicate_checker.py` — scan trùng nội dung
- `canonical_checker.py` — phát hiện nhiều nguồn sự thật
- `drift_checker.py` — so staging/candidate/runtime
- `compliance_audit.py` — kiểm diện luật thần thông
- `bypass_risk_audit.py` — phát hiện script bỏ qua gate

#### Quản lý tổng thể (4)
- `wave_manager.py` — quản lý 4 wave nhập
- `trusted_registry.py` — đăng ký script trusted
- `workspace_inventory.py` — quét toàn bộ workspace
- `ops_dashboard.py` — dashboard trạng thái record

#### Bảo trì (2)
- `auto_maintain.py` — chạy loạt audit định kỳ
- `find_junk.py` — scan file rác
- `index_domains.py` — cấu trúc 16 mảng

#### Templates (3)
- `templates/IMPORT-RECORD.md`
- `templates/A0-EXTRACTION.md`
- `tools-internal/templates/SYNC-RECORD.md`

### 2d) Windows-side (11 tools)

| Tool | Chức năng |
|---|---|
| `top_win_audit.py` | Quét OS, ổ đĩa, biến môi trường |
| `top_win_env_audit.py` | Kiểm tra biến môi trường |
| `top_win_svc_audit.py` | Service Windows |
| `top_win_startup_audit.py` | Startup + scheduled task |
| `top_win_process_audit.py` | Process quan trọng |
| `top_win_disk_health.py` | Sức khỏe ổ đĩa |
| `top_win_cleanup.py` | Tìm temp/junk toàn ổ |
| `top_win_data_map.py` | Dữ liệu trên các ổ |
| `top_win_system_restore.py` | Điểm khôi phục Windows |
| `top_win_tighten.py` | Gợi ý siết chặt |
| `top_win_dashboard.py` | Dashboard tổng quan |
| `top_win_full_dashboard.py` | Dashboard đầy đủ |

### 2e) 16 mảng staging

Nằm tại: `E:\KY-DATA\OpenClaw\mang-he-thong\`

| # | Mảng | A0 |
|---|---|---|
| 01 | Quản lý agent | ✅ |
| 02 | Quản lý công việc | ✅ |
| 03 | Tự động hóa | ✅ |
| 04 | Tổ chức tri thức / memory | ✅ |
| 05 | Quản lý code | ✅ |
| 06 | Quản trị hệ thống | ✅ |
| 07 | Tích hợp API | ✅ |
| 08 | Hệ thống tra cứu | ✅ |
| 09 | Mạng agent | ✅ |
| 10 | Tài liệu tổ chức | ✅ |
| 11 | Cấu hình / tuân thủ | ✅ |
| 12 | Hệ thống CLI | ✅ |
| 13 | Quản lý tài liệu | ✅ |
| 14 | Quản lý nội dung | ✅ |
| 15 | Điều khiển thiết bị / browser | ✅ |
| 16 | Hạ tầng / deploy / platform | ✅ |

### 2f) Records đã sinh (28 records)

Inventory workspace, domain tracker, duplicate check, canonical check, drift check, compliance audit, bypass risk audit, wave plan, sync log, candidate log, rollback manifests, win-audit, win-env, win-svc, win-startup, win-disk, win-data, win-full-dashboard, dashboard...

---

## 3) THẦN THÔNG HOẠT ĐỘNG THẾ NÀO?

### Luồng cơ bản cho mọi tác vụ

```
Người dùng nói: "thần thông kiểm tra service Windows"

1. than_thong_gate.py
   ├── Đọc policy (billing.policy.json)
   ├── Phân tích task text:
   │   - Có paid risk không? → "kiểm tra service" → không
   │   - Có Internet cần không? → không
   │   - Có dấu hiệu internal trusted? → "thần thông" + "Windows" → có
   └── Kết luận: ALLOW (local-trusted)

2. than_thong_wrapper.py (nếu cần)
   ├── Gate pass
   ├── Chỉ chạy script trusted (trong policy)
   └── Thực thi

3. than_thong_console.py win-svc
   ├── Gate pass
   ├── Route → top_win_svc_audit.py
   ├── Chạy → quét service
   └── Ghi record → top-win-svc-audit.json

4. Người dùng nhận kết quả
```

### Luồng import (cho dữ liệu mới)

```
Staging ngoài → candidate_builder → import_validator → deep_validator 
→ backup file cũ → sync_executor → rollback_manifest → record_writer
```

### Luồng bảo trì

```
auto_maintain.py
├── workspace_inventory.py
├── find_junk.py
├── domain_tracker.py
├── duplicate_checker.py
├── canonical_checker.py
├── drift_checker.py
├── ops_dashboard.py
└── compliance_audit.py
```

---

## 4) NGUYÊN TẮC

| Nguyên tắc | Mô tả |
|---|---|
| Local-first | Làm bằng nội bộ trước |
| Anti-billing | Không tự ý gây phát sinh chi phí |
| Internet read-only | Chỉ cho đọc, tránh provider trả phí |
| Gate trước | Mọi việc phải qua kiểm tra trước |
| Audit sau | Mọi việc đều có record |
| Rollback | Import sai có thể gỡ |

---

## 5) THỐNG KÊ

| Khoản | Số lượng |
|---|---|
| Script tổng | 37 |
| Entrypoint thần thông | 3 |
| Windows-side tools | 12 |
| Templates | 3 |
| Records đã sinh | 28 |
| 16 mảng đã A0 | 16/16 |
| Alias legacy | top, billing |

---

## 6) TÓM TẮT MỘT CÂU

**Thần thông là quản gia toàn máy cho OpenClaw: local-first, gate billing, import an toàn, dọn Windows, audit toàn bộ.**
