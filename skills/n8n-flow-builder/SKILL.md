---
name: n8n-flow-builder
description: Thiet ke, phan tich va toi uu workflow n8n tu mo ta tu nhien. Su dung kien thuc tu AI Workflow Builder chinh thuc cua n8n.
---

# n8n Flow Builder

## Tổng quan

Skill này giúp thiết kế workflow n8n chuyên nghiệp dựa trên kiến trúc AI Workflow Builder của n8n.

## Quy trình thiết kế

### 1. Phân tích yêu cầu
- Xác định trigger (Webhook, Cron, Polling)
- Xác định input/output
- Xác định pattern (chatbot, ETL, notification, form)

### 2. Kiến trúc workflow
- Workflow Config node đầu tiên (API URLs, thresholds, constants)
- Trigger → Config → Processing → Output
- Dùng `=$("Workflow Config").first().json.apiUrl` để tham chiếu

### 3. Chọn pattern phù hợp

| Pattern | Khi nào dùng |
|---------|-------------|
| Chatbot | Cần conversation với LLM |
| Webhook | API callback, nhận data từ ngoài |
| Cron | Chạy định kỳ (báo cáo, sync) |
| Form | Thu thập input từ user |
| Data transformation | ETL, mapping, enrich |

### 4. Best practices
- **Idempotency**: Mỗi workflow chạy lại không gây side effect
- **Error handling**: Retry policy + failure notification
- **Logging**: Ghi log mỗi step quan trọng
- **Human-in-the-loop**: Review queue cho action nguy hiểm
- **Configuration node**: Một node Set() đầu workflow cho constants

### 5. Validation
- Webhook responseMode=onReceived cho simple API
- Code node: check module imports, async handling
- HTTP Request node: verify auth, response parsing
- Connections: kiểm tra output format match input expectation

## Templates mẫu

Xem `review/candidate/n8n-tinh-hoa/`:
- `04-ai-chatbot-template.json` — Chatbot AI
- `14-data-transformation.json` — ETL
- `14-http-api-call.json` — API integration

## References

Chi tiết tại `review/candidate/n8n-tinh-hoa/`:
- `01` → Tổng quan skill
- `02` → Agent prompt
- `03` → Best practices
- `07-12` → Node guides, expression, branching
- `13` → HTTP/If/Set node deep dives
- `15` → Code patterns & schema
