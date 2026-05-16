# Thời hạn sử dụng - Unified Rate Governor

## 1. THỜI HẠN KỸ THUẬT (KHÔNG GIỚI HẠN)

- **Code Python thuần** → chạy mãi mãi
- **0 dependencies** → không lỗi thời
- **File-lock cross-process** → không cần service restart
- **Auto-recovery khi file corrupt** → tự lành
- **Chi phí: 0 đồng** (local, không cloud)

## 2. THỜI HẠN VẬN HÀNH THEO CẤU HÌNH

### Rate limit: 30 calls/min
- Mỗi phút có 30 slot, reset sau 60s
- Nếu dùng hết → đợi ~60s có slot mới
- Nếu dùng 5 calls/phút → chạy 6 giờ liên tục
- Nếu dùng 1 call/phút → chạy 30 phút liên tục

### Billing budget: chưa set → không giới hạn
- Set `LLM_DAILY_BUDGET_CENTS=500` = $5/ngày
- `live` mode → block khi hết budget
- `dry-run` mode → chỉ log, không block

### Circuit breaker: 5 failures → 60s cooldown
- Tự mở circuit breaker
- Sau 60s → half-open → thử lại
- OK thì close, fail tiếp thì mở lại

### State file: persist giữa các lần chạy
- `config/.rate_limit_state.json`
- Xóa file → tự tạo lại mặc định

## 3. THỜI HẠN THEO USE CASE

### A. Phát triển (DEV)
- 30 calls/min, budget unlimited
- **CHẠY MÃI MÃI**

### B. Production (PROD) $5/ngày
- 30 calls/min, $5/day
- LLM costs ~$0.005/call (DeepSeek)
- → 1000 calls/ngày (~33 phút chạy)

### C. Budget $0 (free tier)
- 30 calls/min, $0
- → Chỉ local models (Ollama)

### D. Unmetered local
- 30 calls/min, 0 cost
- **CHẠY MÃI MÃI**

## 4. THỜI GIAN TRIỂN KHAI

### Đã làm xong (hôm nay):
- 11:18 - Set LLM_MAX_CALLS_PER_MINUTE=30
- 11:20 - Fix rate_limiter constructor env read
- 11:26 - Viết RateGovernor (file-based sync)
- 11:28 - Viết GovernorWithBilling (billing guard)
- 11:29 - Test all pass

### Sắp tới (tuần này):
- Tích hợp Governor vào scripts hiện tại
- Config model fallbacks trong OpenClaw config
- Tạo dashboard reports

### Bảo trì: không cần định kỳ
- State file tự cleanup (prune bucket mỗi 60s)
- Log rotated daily

## 5. TÓM TẮT

| Thành phần | Thời hạn | Phụ thuộc |
|---|---|---|
| Rate Governor | VĨNH VIỄN | Python stdlib |
| Rate limit (30/m) | Reset mỗi 60s | State file |
| Circuit breaker | Cooldown 60s | Tự phục hồi |
| Billing budget | Reset hàng ngày | State file |
| State file | Mãi mãi | Disk (0 bytes) |
| Logs | Xoay ngày | Disk |

**PHẠM VI SỬ DỤNG: KHÔNG GIỚI HẠN**
**YÊU CẦU: 0 đồng, 0 dependencies, local-first**
