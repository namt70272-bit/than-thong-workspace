# KIẾN TRÚC HỆ THỐNG n8n — VẬN HÀNH TOÀN DIỆN

**Ngày:** 2026-05-13  
**Nguyên tắc:** Local-first, dữ liệu trên E:, billing tối thiểu  
**Nền tảng:** n8n Docker + PostgreSQL + Redis + MinIO + Ollama + FFmpeg

---

## 1. TỔNG QUAN KIẾN TRÚC

```
                     ┌─────────────────────────────────┐
                     │         n8n ORCHESTRATOR        │
                     │  (http://localhost:5678)        │
                     └──┬──────┬──────┬──────┬──────┬──┘
                        │      │      │      │      │
              ┌─────────┘  ┌───┘   ┌──┘   ┌──┘   └──────────┐
              ▼            ▼       ▼      ▼                  ▼
        ┌──────────┐ ┌────────┐ ┌──────┐ ┌──────┐ ┌──────────────┐
        │ CONTENT  │ │ CUSTOMER│ │ CARE │ │REPORT│ │  OPERATIONS  │
        │ PIPELINE │ │   CRM   │ │ ENGINE│ │ ENGINE│ │   SCHEDULER  │
        └────┬─────┘ └───┬────┘ └──┬───┘ └──┬───┘ └──────┬───────┘
             │           │         │        │            │
             ▼           ▼         ▼        ▼            ▼
        ┌──────────────────────────────────────────────────────┐
        │              INFRASTRUCTURE LAYER                    │
        │  PostgreSQL(5432) Redis(6379) MinIO(9000) Ollama    │
        │  Qdrant(6333) video-worker FFmpeg                   │
        └──────────────────────────────────────────────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   E:\DATA    │
                   └──────────────┘
```

---

## 2. CHI TIẾT 6 NHÁNH WORKFLOW

### 2a) CONTENT PIPELINE — Tạo nội dung

```
Webhook (ảnh/video/text từ người dùng)
  │
  ▼
Lưu file gốc vào MinIO (bucket: raw-content)
  │
  ▼
AI Vision (Ollama minicpm-v) → phân tích ảnh
  │
  ▼
LLM (Ollama qwen2.5) → viết kịch bản, caption, prompt
  │
  ▼
TTS (sherpa-onnx local) → tạo voice
  │
  ▼
video-worker (FFmpeg) → ghép video + voice + text + loop
  │
  ▼
Xuất MP4 → MinIO (bucket: finished-content)
  │
  ▼
Gửi link / thông báo
```

**n8n nodes cần:**
- Webhook node (input)
- S3 node (MinIO, tương thích AWS S3)
- HTTP node (gọi Ollama API: http://host.docker.internal:11434)
- HTTP node (gọi video-worker)
- Email / HTTP node (output)

### 2b) CUSTOMER CRM — Quản lý khách

```
Webhook (khách mới đăng ký / liên hệ)
  │
  ▼
PostgreSQL → lưu vào bảng customers
  │
  ├── Gán tag (mới, tiềm năng, VIP, cũ)
  ├── Ghi lịch sử tương tác
  └── Tích điểm / xếp hạng
```

**Database schema (PostgreSQL):**
```sql
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(20),
  source VARCHAR(100),       -- FB, web, giới thiệu...
  tags TEXT[],                -- {mới, VIP, tiềm năng}
  loyalty_points INT DEFAULT 0,
  total_spent DECIMAL(12,2) DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE interactions (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  type VARCHAR(50),           -- email, call, chat, meeting
  content TEXT,
  sentiment VARCHAR(20),      -- positive, neutral, negative
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE reminders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  title VARCHAR(255),
  due_date TIMESTAMP,
  status VARCHAR(20) DEFAULT 'pending', -- pending, done, cancelled
  note TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 2c) CARE ENGINE — Chăm sóc khách

```
Schedule Trigger (hàng ngày 8:00)
  │
  ▼
PostgreSQL → query khách cần chăm sóc:
  ├── Sinh nhật trong tuần → gửi email chúc
  ├── Không tương tác > 30 ngày → email hỏi thăm
  ├── Khách VIP chưa liên hệ > 7 ngày → gọi/tin nhắn
  └── Đơn hàng gần đây → khảo sát hài lòng
  │
  ▼
LLM (Ollama) → viết nội dung cá nhân hóa
  │
  ▼
Gửi email / webhook thông báo
  │
  ▼
PostgreSQL → ghi log đã chăm sóc
```

### 2d) REPORT ENGINE — Báo cáo

```
Schedule Trigger (cuối ngày / cuối tuần / cuối tháng)
  │
  ▼
PostgreSQL → tổng hợp dữ liệu
  ├── Số khách mới / tuần
  ├── Doanh thu / tháng
  ├── Tỉ lệ hài lòng
  ├── Số content đã tạo
  └── Hiệu suất từng kênh
  │
  ▼
LLM (Ollama) → viết báo cáo tóm tắt bằng văn xuôi
  │
  ▼
Gửi email báo cáo
  └── Lưu báo cáo vào MinIO (bucket: reports)
```

### 2e) REMINDER — Nhắc lịch

```
Schedule Trigger (mỗi giờ kiểm tra)
  │
  ▼
PostgreSQL → query reminders sắp đến hạn
  │
  ▼
Với mỗi reminder:
  ├── Còn < 1 giờ → Gửi thông báo khẩn
  ├── Còn < 24 giờ → Gửi nhắc nhở
  └── Quá hạn → Đánh dấu quá hạn + thông báo
```

### 2f) OPERATIONS — Hỗ trợ vận hành

```
Webhook (yêu cầu hỗ trợ từ nhân viên / hệ thống)
  │
  ▼
Phân loại yêu cầu:
  ├── Kỹ thuật → tạo ticket
  ├── Khách hàng → chuyển CARE
  ├── Nội dung → chuyển CONTENT
  └── Báo cáo → chuyển REPORT
  │
  ▼
Ghi log + thông báo người phụ trách
```

---

## 3. INFRASTRUCTURE SETUP

### MinIO Buckets
```
raw-content/       → Ảnh/video/text người dùng upload
finished-content/  → Video/ảnh đã xử lý xong
reports/           → Báo cáo tự động
backups/           → Backup dữ liệu
templates/         → Mẫu video, template
```

### Ollama Models
```bash
ollama pull minicpm-v          # Vision (đang chạy)
ollama pull qwen2.5:7b         # LLM chính (đã có)
ollama run qwen2.5:7b          # Test
```

### PostgreSQL (ai-postgres có sẵn)
```bash
# Kết nối từ n8n container
Host: host.docker.internal
Port: 5432
Database: n8n (hoặc tạo mới: crm)
User/Pass: từ ai-postgres
```

### Redis (ai-redis có sẵn)
```bash
Host: host.docker.internal
Port: 6379
# Dùng cho queue + cache
```

---

## 4. THỨ TỰ TRIỂN KHAI

### Phase 1 — Nền tảng (làm ngay)
1. Tạo database + tables trong PostgreSQL
2. Tạo MinIO buckets
3. Kết nối n8n với PostgreSQL
4. Test webhook cơ bản

### Phase 2 — CRM (kế tiếp)
5. Webhook nhận khách mới → PostgreSQL
6. CRUD customers từ n8n
7. Gán tag + phân loại tự động

### Phase 3 — Content Pipeline
8. Upload → MinIO
9. Gọi Ollama Vision + LLM
10. video-worker xử lý

### Phase 4 — Care + Reminder
11. Schedule trigger chăm sóc
12. Email tự động
13. Nhắc lịch

### Phase 5 — Report
14. Tổng hợp dữ liệu
15. LLM viết báo cáo
16. Gửi email định kỳ

---

## 5. BẢNG TÓM TẮT

| Module | Trigger | Dữ liệu | Output |
|---|---|---|---|
| Content | Webhook | MinIO + Ollama | Video/MP4 |
| CRM | Webhook | PostgreSQL | Customer records |
| Care | Schedule (ngày) | PostgreSQL + Ollama | Email |
| Report | Schedule (tuần/tháng) | PostgreSQL + Ollama | Email + MinIO |
| Reminder | Schedule (giờ) | PostgreSQL | Notification |
| Operations | Webhook | PostgreSQL | Ticket + log |

---

## 6. LƯU Ý BILLING

- **Ollama**: Local, không billing ✅
- **PostgreSQL/Redis/MinIO**: Local, không billing ✅
- **FFmpeg/video-worker**: Local, không billing ✅
- **Email gửi đi**: Có thể cần SMTP (nếu dùng Gmail miễn phí)
- **TTS**: sherpa-onnx local, không billing ✅

**Nếu dùng API cloud (OpenAI/Anthropic/Runway): Cần báo trước và duyệt.**
