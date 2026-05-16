# Agent Rules Proposal

## Rules đề xuất cho OpenClaw Agent

### Nhóm 1: File Safety

| Rule | Mô tả |
|---|---|
| **R1** | Trước khi xóa file → hỏi user |
| **R2** | Trước khi di chuyển/rename file → hỏi user |
| **R3** | Trước khi sửa file đang chạy (config, service) → backup trước |
| **R4** | Không sửa file trong `.git` nếu chưa commit |
| **R5** | Không sửa file có chứa secret (API key, token) nếu chưa có env var |

### Nhóm 2: Security

| Rule | Mô tả |
|---|---|
| **R6** | Không in API key/token/password/private key ra màn hình |
| **R7** | Nếu thấy secret → che dạng: `sk-****abcd` |
| **R8** | Không upload `_audit/` lên cloud |
| **R9** | Không đọc `runner/.credentials` trừ khi cần debug |
| **R10** | Không dùng profile Chrome cá nhân cho automation |

### Nhóm 3: External Actions

| Rule | Mô tả |
|---|---|
| **R11** | Trước khi gửi email → hỏi user |
| **R12** | Trước khi đăng bài lên mạng xã hội → hỏi user |
| **R13** | Trước khi thanh toán/mua hàng → hỏi user |
| **R14** | Trước khi push GitHub → hỏi user (nếu không phải auto-backup) |
| **R15** | Trước khi revoke/rotate key → hướng dẫn user tự làm |

### Nhóm 4: Browser Automation

| Rule | Mô tả |
|---|---|
| **R16** | Browser automation phải dùng profile riêng: `OpenClaw-Agent` |
| **R17** | Mặc định headless mode |
| **R18** | Không auto-fill credentials trên site lạ |
| **R19** | Timeout tối đa 30s mỗi page load |
| **R20** | Không download file nếu user chưa xác nhận |

### Nhóm 5: Tool Permissions

| Rule | Mô tả |
|---|---|
| **R21** | Tool nguy hiểm (exec, elevated, delete) phải có allow list |
| **R22** | Chỉ dùng allow list cho script quan trọng |
| **R23** | MCP tools phải được kiểm tra trước khi cho phép |
| **R24** | web_search, web_fetch chỉ dùng khi thực sự cần |

### Nhóm 6: Maintenance

| Rule | Mô tả |
|---|---|
| **R25** | Sau mỗi lần nâng cấp → chạy healthcheck |
| **R26** | Audit lại hệ thống mỗi tháng |
| **R27** | Backup memory trước khi shutdown |
| **R28** | Ghi daily note cuối mỗi session |

---

## Cách implement

### Option A: Ghi vào AGENTS.md (dễ nhất)
Thêm các rule vào `AGENTS.md` dưới dạng markdown. Agent tự đọc và tuân theo.

### Option B: Tạo file rules riêng
Tạo `configs/agent-rules.yaml` — machine readable, có thể check bằng script.

### Option C: OpenClaw plugin
Tạo plugin runtime guard kiểm tra rule trước mỗi action (giống than-thong-guard).

**Không tự implement — chờ xác nhận cách nào.**
