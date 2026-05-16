# Upgrade Context

## 1. Hệ thống hiện tại đang như thế nào?

OpenClaw là AI orchestrator chạy local + GitHub CI/CD, gồm:
- **Agent core**: DeepSeek V4 Flash + thần thông gate
- **Local LLM**: Ollama (3 models: bge-m3, gemma3:1b, qwen2.5-coder:7b)
- **Vector DB**: Qdrant v1.18.0 (89 documents indexed)
- **CI/CD**: GitHub Actions + self-hosted Windows runner (12 workflows)
- **Docker**: 6 containers (5 running), 9 images (~6GB)
- **Scripts**: 66+ Python scripts trong tools-internal/
- **Tests**: pytest 9.0.3, 13 unit tests

## 2. Vấn đề lớn nhất hiện tại

1. **Secret trong source code** — Gemini key + GCP private key trong file cleartext
2. **Elevated exec wildcard** — webchat có thể exec admin không cần duyệt
3. **Cấu trúc thư mục lẫn** — scripts/, tools-internal/ trộn tool core + test + reference
4. **n8n container restart loop** — service chết, chiếm 2.27GB image
5. **Runner credentials trong workspace** — `.credentials` file chứa OAuth token

## 3. Rủi ro bảo mật nghiêm trọng

| # | Rủi ro | Mức | File liên quan |
|---|---|---|---|
| 1 | Gemini API key lộ trong 4 scripts | 🔴 CRITICAL | scripts/test-gemini-key.py + 3 files |
| 2 | GCP service account private key | 🔴 CRITICAL | config/gcp-n8n-vertex-ai-key.json |
| 3 | Elevated exec wildcard webchat | 🔴 CRITICAL | openclaw config |
| 4 | PostHog telemetry API key | 🟡 MEDIUM | reference-library/mem0/telemetry.py |
| 5 | Runner credential files | 🟡 MEDIUM | runner/.credentials, runner/_diag/*.log |

## 4. Điểm rối trong cấu trúc thư mục

| Vấn đề | Mô tả |
|---|---|
| `scripts/` gốc | Chứa test scripts lẫn secret song song với `tools-internal/scripts/` |
| `tools-internal/` quá to | 65 scripts + extracted code + reference library |
| `extracted-scripts/` | Hàng ngàn file từ G:\Ai zip — cần lọc |
| `runner/` trong workspace | Chứa credentials, diag logs — không nên trong workspace |
| `memory/` | 10 files, nhưng lẫn với session transcripts dài |
| Không có `config/` riêng cho MCP/tool/browser | Cấu hình rải rác |

## 5. Điểm rối trong Docker/local service

| Vấn đề | Mô tả |
|---|---|
| n8n restart loop | Container chết liên tục, chiếm 2.27GB |
| Không docker-compose.yml | Services chạy bằng `docker run` thủ công |
| Langfuse image không dùng | 1.37GB image không có container |
| Thiếu restart policy | Qdrant, dozzle, portainer chạy manual |

## 6. Điểm rối trong workflow

Hiện có 12 GitHub Actions workflows — khá đầy đủ. Vấn đề:
- Thiếu workflow tự động audit định kỳ
- Thiếu workflow rollback khi deploy lỗi
- auto-work-review chỉ chạy trên PR, không chạy trên push

## 7. Điểm rối trong config/env/tool/MCP

| Vấn đề | Mô tả |
|---|---|
| Không `.env.example` | Không có template cho env vars |
| Secret hardcode trong script | 5+ file chứa key trực tiếp |
| Không MCP config chuẩn hóa | Không có file mcp_config.json riêng |
| Config rải rác | tools-internal/policy/, config/, scripts/ |

## 8. Những phần không nên đụng vào ngay

- **OpenClaw gateway config** — đang chạy ổn định
- **GitHub Actions workflows** — 12 workflows đang hoạt động
- **Ollama models** — 3 models đã download, không cần đụng
- **Qdrant + indexed documents** — 89 documents đã index
- **Core thần thông scripts** — hệ thống gate đang hoạt động

## 9. Những phần có thể cải thiện an toàn

| Có thể làm ngay | Cần hỏi trước |
|---|---|
| Tạo .env.example | Xóa file chứa secret |
| Tạo gitignore proposal | Sửa source code hardcoded |
| Tạo script mẫu chưa chạy | Di chuyển file |
| Tạo doc bổ sung | Sửa config thật |
| Tạo plan | Dọn Docker |

## 10. Mục tiêu nâng cấp đề xuất

1. **Bảo mật** — Xóa secret khỏi source, dùng env var
2. **Cấu trúc** — Gom tool/config/workflow vào folder chuẩn
3. **Vận hành** — Healthcheck + backup + audit script
4. **Tài liệu** — Operating guide, system map đầy đủ
5. **Docker** — docker-compose.yml, dọn image không dùng
