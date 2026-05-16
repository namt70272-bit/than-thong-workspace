# DATA-STORE.md — Nguyên tắc lưu trữ dữ liệu

**Mọi dữ liệu tập trung ở Ổ E:** `E:\KY-DATA\OpenClaw\runtime-mirror`

## Cấu trúc

| Đường dẫn | Gì ở đây |
|-----------|----------|
| `E:\...\.openclaw\workspace\` | File làm việc (AGENTS.md, SOUL.md, MEMORY.md, TOOLS.md, skills, scripts, config, utils, references...) |
| `E:\...\.openclaw\memory\` | Nhật ký ngày và bộ nhớ dài hạn |
| `E:\...\.openclaw\media\` | Ảnh, file upload, media assets |
| `E:\...\.openclaw\canvas\` | Web UI files (hosted embeds) |
| `E:\...\.openclaw\plugins\` | Plugin skills |
| `E:\...\.openclaw\logs\` | Logs cũ |
| `E:\...\.tmp\openclaw\` | Logs runtime (trong ngày) |
| `E:\...\.openclaw\openclaw.json` | **Config chính** (đồng bộ từ C: khi cần) |

## Nguyên tắc

1. **Ổ C chỉ chứa app** (node, npm, code-mirror) — không lưu dữ liệu mới vào C:
2. **File rác** (backup, clobbered, rejected, last-good) phát sinh từ gateway — dọn định kỳ
3. **Workspace** và **memory** chỉ thao tác trên E: — không tạo file làm việc mới trên C:
4. **Config** (`openclaw.json`) gateway đọc từ C: nhưng bản sao luôn có ở E: — sync khi restart
5. Nếu có file tạm sinh ra ở đâu đó ngoài E: (ví dụ `C:\...\.openclaw\`), kiểm tra và dời về E: hoặc xoá

## Drive Letter

- Ổ OpenClaw luôn được gán **E:** — cố định, không đổi kể cả cắm vào máy khác
- Volume label: **OPENCLAW** (lưu trên đĩa, tồn tại vĩnh viễn)
- Script duy trì: `E:\KY-DATA\OpenClaw\fix-drive.bat` (chạy Admin)
- Nếu máy mới gán sai letter → chạy fix-drive.bat

## Giữ sạch

- Junk files (`*.bak*`, `*.clobbered*`, `*.rejected*`, `*.last-good`, `*.old*`) → xoá
- Temp scripts (`_*.py`, `_*.sh`, `_*.ps1`) → xoá sau khi dùng xong
- Không để file rác tích tụ quá 1 ngày
