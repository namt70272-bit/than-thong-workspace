# Upgrade Tasks

## 🔴 CRITICAL — Làm ngay

| # | Task | File liên quan | Rủi ro | Cần xác nhận? |
|---|---|---|---|---|
| 1 | Rotate/revoke Gemini API key | `scripts/test-gemini-key.py`, `scripts/create-n8n-cred.py`, `scripts/create-n8n-http-workflow.py`, `gemini-webhook.py` | Key bị lộ → unauthorized usage | ✅ Cần user làm trên dashboard |
| 2 | Rotate/revoke GCP service account key | `config/gcp-n8n-vertex-ai-key.json` | Full GCP project access | ✅ Cần user làm trên GCP Console |
| 3 | Xóa elevated exec wildcard | OpenClaw gateway config | Any webchat user = admin | ✅ Cần user xác nhận config change |
| 4 | Thêm _audit/ vào .gitignore | `.gitignore` | Report nhạy cảm có thể commit | ✅ Hỏi trước khi sửa file |
| 5 | Thêm runner/ vào .gitignore | `.gitignore` | OAuth token có thể commit | ✅ Hỏi trước khi sửa file |
| 6 | Thay hardcoded key bằng env var | scripts/*.py, gemini-webhook.py | Key lộ qua git | ✅ Cần user approve từng file |

## 🟡 HIGH — Sau bảo mật ổn

| # | Task | Mô tả |
|---|---|---|
| 7 | Tạo `.env.example` | Template với placeholder, không key thật |
| 8 | Tạo docker-compose.yml | Gom 4 container đang chạy |
| 9 | Xóa PostHog telemetry key | `reference-library/mem0/telemetry.py` |
| 10 | Tạo healthcheck script | `scripts/healthcheck.ps1` (mẫu, chưa chạy) |
| 11 | Tạo backup script | `scripts/backup.ps1` (mẫu, chưa chạy) |
| 12 | Fix n8n container | Debug restart loop hoặc xóa |
| 13 | Hạn chế quyền tool nguy hiểm | Thêm deny list cho exec/elevated |

## 🟢 MEDIUM — Tối ưu hệ thống

| # | Task | Mô tả |
|---|---|---|
| 14 | Sắp xếp thư mục | Gom file theo GĐ2 plan |
| 15 | Dọn langfuse image (1.37GB) | Image không dùng |
| 16 | Dọn Python cache | `__pycache__` trong scripts/ |
| 17 | Dọn runner diag logs | `runner/_diag/*.log` |
| 18 | Viết operating guide | Hoàn thiện doc |
| 19 | Tạo auto-audit workflow | GitHub Actions chạy audit định kỳ |

## 🔵 LOW — Tối ưu lâu dài

| # | Task | Mô tả |
|---|---|---|
| 20 | Mermaid diagrams | Export SVG từ workflow map |
| 21 | Dependency graph | Có madge output rồi, cần visualize |
| 22 | Dashboard local | Netdata/Grafana cho monitoring |
| 23 | Documentation nâng cao | Chi tiết từng module |
| 24 | Self-healing scripts | Phát hiện + tự fix lỗi phổ biến |

---

## Chi tiết từng task CRITICAL

### Task 1: Gemini API key
- **Mục tiêu:** Revoke key trên Google AI Studio, dùng key mới qua env var
- **File liên quan:** scripts/test-gemini-key.py, scripts/create-n8n-cred.py, scripts/create-n8n-http-workflow.py, scripts/test-gemini-openai-endpoint.py, gemini-webhook.py
- **Cách an toàn:** User vào https://aistudio.google.com/app/apikey → revoke key cũ → tạo key mới → tôi thay vào env var
- **Backup cần:** Có — git commit trước khi sửa

### Task 2: GCP service account key
- **Mục tiêu:** Revoke key trên GCP Console, xóa file JSON khỏi workspace
- **File liên quan:** config/gcp-n8n-vertex-ai-key.json
- **Cách an toàn:** User vào GCP Console → IAM → Service Accounts → Revoke key → tôi xóa file
- **Backup cần:** Có — copy key ra ngoài workspace trước khi xóa

### Task 3: Elevated exec wildcard
- **Mục tiêu:** Thay `"*"` bằng specific user ID hoặc `[]`
- **File liên quan:** OpenClaw gateway.yaml
- **Cách an toàn:** Đọc config → tạo bản sao → sửa → restart gateway
- **Backup cần:** Có — backup config trước khi sửa

### Task 6: Thay hardcoded → env var
- **Mục tiêu:** 5 scripts dùng `os.environ.get("GEMINI_API_KEY")` thay vì hardcode
- **Cách an toàn:** Tạo `.env` → thêm key → sửa từng file → test
- **Backup cần:** Có — git commit trước từng file
