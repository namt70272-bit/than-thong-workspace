# Safe Change Plan

## Nhóm A — Có thể làm an toàn ngay (không cần hỏi)

| Task | Mô tả | Rủi ro |
|---|---|---|
| Tạo thêm file docs trong `_audit/` | Plan, proposal không ảnh hưởng gì | None |
| Tạo `.env.example` | Template sạch, không key thật | None |
| Tạo `.gitignore` proposal | Chỉ đề xuất, chưa sửa file thật | None |
| Đề xuất cấu trúc mới | Chỉ plan, chưa tạo folder | None |
| Đề xuất script mẫu | Chỉ nội dung, chưa tạo file | None |

## Nhóm B — Cần user xác nhận trước khi làm

| Task | Mô tả | Cần backup? |
|---|---|---|
| Sửa `.gitignore` thật | Thêm pattern cho runner/, _audit/ | ✅ Có |
| Sửa source code → env var | Thay hardcoded key bằng os.environ.get() | ✅ Có |
| Xóa file chứa secret | Xóa config/gcp-*.json, scripts/test-*.py | ✅ Có (git backup) |
| Tạo `.env` thật | File chứa key, phải cẩn thận | ✅ Có |
| Di chuyển file theo cấu trúc mới | Gom tools, config, data | ✅ Có |
| Dọn Docker image không dùng | Xóa langfuse, n8n | ✅ Có |
| Chỉnh OpenClaw config | Sửa gateway.yaml, sửa elevated | ✅ Có |
| Tạo script thật | healthcheck.ps1, backup.ps1 | ✅ Có |
| Tạo docker-compose.yml | Reproduce docker services | ✅ Có |

## Nhóm C — Không được tự động làm

| Task | Lý do |
|---|---|
| Revoke/rotate API key | Phải làm trên dashboard của Google/GitHub |
| Push GitHub (ngoài auto-backup) | Có thể push nhầm secret |
| Rewrite Git history | Mất commit history, phức tạp |
| Delete Docker volumes | Mất data Qdrant index |
| Delete database files | Không recover được |
| Delete browser profile | Mất session login |
| Xóa file không backup | Nếu chưa có git commit |
| Thay đổi tài khoản đang login | Mất quyền truy cập |
| Mở port ra internet | Rủi ro bảo mật |

## Quy trình thay đổi an toàn

```mermaid
flowchart TD
    A[Change proposal] --> B{Approval needed?}
    B -->|No (Group A)| C[Just do it]
    B -->|Yes (Group B)| D[Ask user]
    D -->|Approved| E[Backup first]
    E --> F[Make change]
    F --> G[Verify]
    G --> H[Update docs]
    D -->|Denied| I[Skip]
    C --> G
```

## Backup checklists

### Trước mỗi thay đổi Group B:
- [ ] `git status` — workspace sạch?
- [ ] `git add -A && git commit -m "backup before X"` 
- [ ] Nếu sửa config: backup file gốc sang `_audit/upgrade-backup/`
- [ ] Nếu xóa file: backup sang `_audit/upgrade-backup/`

### Sau mỗi thay đổi:
- [ ] Test chức năng cơ bản
- [ ] `python -m pytest tests/ -v` nếu liên quan Python
- [ ] Verify service còn chạy
- [ ] `git diff` để kiểm tra thay đổi
