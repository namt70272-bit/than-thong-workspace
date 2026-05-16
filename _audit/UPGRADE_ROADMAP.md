# Upgrade Roadmap — 5 Giai đoạn

---

## Giai đoạn 1 — Cấp cứu bảo mật (Critical)

| Task | File liên quan | Mức |
|---|---|---|
| Rotate/revoke Gemini API key | 4 scripts trong `scripts/` | 🔴 |
| Rotate/revoke GCP service account | `config/gcp-n8n-vertex-ai-key.json` | 🔴 |
| Xóa elevated exec wildcard | OpenClaw gateway config | 🔴 |
| Xóa PostHog API key | `reference-library/mem0/telemetry.py` | 🟡 |
| Thêm `_audit/` + `runner/` vào `.gitignore` | `.gitignore` | 🟡 |
| Kiểm tra runner credential không bị git tracked | `.gitignore` | 🟡 |

**Nguyên tắc:** Không tự rotate key. Hướng dẫn user làm thủ công. Chỉ thay hardcoded → env var sau khi xác nhận.

---

## Giai đoạn 2 — Chuẩn hóa cấu trúc thư mục (High)

Mục tiêu chuyển từ cấu trúc phẳng hiện tại sang:

```
openclaw-system/
├─ apps/           → Agent core, gateway configs
├─ configs/        → MCP, browser, docker, env templates
├─ tools/          → browser-use, playwright, local-scripts
├─ workflows/      → workflow docs, templates
├─ memory/         → rules, notes, system-map, long-term
├─ data/           → input, output, cache, downloads, logs
├─ docs/           → system docs, maps
├─ scripts/        → start, stop, audit, backup, healthcheck
└─ _audit/         → audit reports
```

**Không tự chuyển file — chỉ lập kế hoạch.**

---

## Giai đoạn 3 — Chuẩn hóa config/env (High)

| Task | Mô tả |
|---|---|
| Tạo `.env.example` | Template sạch, không key thật |
| Tạo config template cho MCP | `mcp_config.json.example` |
| Tạo config template cho tool | `tool_config.yaml.example` |
| Thay hardcoded key → env var | 5+ scripts cần sửa |
| Gom config vào `configs/` | Tách khỏi tools-internal/ |
| Kiểm tra `.gitignore` bảo vệ đủ | Thêm pattern cho creds |

---

## Giai đoạn 4 — Chuẩn hóa workflow vận hành (Medium)

Tạo scripts mẫu (chưa chạy):

| Script | Mục đích |
|---|---|
| `start.ps1` | Khởi động Docker + Ollama + gateway |
| `stop.ps1` | Dừng an toàn |
| `healthcheck.ps1` | Kiểm tra toàn bộ service |
| `audit.ps1` | Chạy audit tự động → _audit/ |
| `backup.ps1` | Git commit + push + backup memory |
| `doctor.ps1` | Chẩn đoán lỗi phổ biến + gợi ý fix |

---

## Giai đoạn 5 — Tối ưu nâng cao (Low)

| Task | Mô tả |
|---|---|
| Docker cleanup | Dọn langfuse (1.37GB), n8n issue debug |
| Dependency cleanup | Dọn extracted-scripts/ không cần |
| Log/cache cleanup | runner/_diag/, __pycache__ |
| Browser profile isolation | Tạo profile riêng cho agent |
| Auto-audit cron | Chạy audit định kỳ qua GitHub Actions |
| Documentation | Operating guide, system map đầy đủ |

---

## Timeline đề xuất

```
GĐ1: Bảo mật          → LÀM NGAY (1-2 ngày)
GĐ2: Cấu trúc thư mục → Sau GĐ1 (2-3 ngày)
GĐ3: Config/env       → Song song GĐ2 (1-2 ngày)
GĐ4: Workflow scripts → Sau GĐ2 (2-3 ngày)
GĐ5: Tối ưu           → Cuối cùng (1 tuần)
```

**Tổng thời gian ước tính:** 1-2 tuần nếu làm liên tục.
