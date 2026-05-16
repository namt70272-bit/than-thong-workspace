# A0 — Tự động hóa

## Đã xác nhận an toàn tuyệt đối để lấy trước

### 1) Lobster
**Chỉ lấy:**
- `README.md`
- `VISION.md`
- cấu trúc ý tưởng từ `src/parser.ts`, `src/runtime.ts` chỉ để đọc logic

**Không lấy:**
- CLI thực thi
- resume state thật
- package/runtime code để chạy ngay

**Giá trị:**
- workflow DSL pattern
- cách tách parser / runtime / resume
- mô hình pipeline có thể áp vào TaskFlow hiện có

### 2) TựĐộng-NghiênCứuSâu
**Chỉ lấy:**
- workflow mô tả
- prompt/pipeline nếu có

**Không lấy:**
- script tự chạy
- service / cron / state cũ

### 3) Cognee-n8n
**Chỉ lấy:**
- integration pattern mô tả

**Không lấy:**
- n8n runtime

## Kết luận
Mảng này A0 chủ yếu là lấy pattern workflow rồi chuyển thành template nhỏ cho hệ hiện tại.
