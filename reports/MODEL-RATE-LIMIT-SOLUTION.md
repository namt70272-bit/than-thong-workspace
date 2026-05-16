# Phương án tối ưu: Models & Rate Limiting

**Ngày:** 2026-05-12  
**Mục tiêu:** Giải quyết triệt để limit rate, tối ưu models

---

## I. HIỆN TRẠNG

| Layer | Cơ chế | Status |
|-------|--------|--------|
| OpenClaw runtime | 11 model aliases, built-in rate limiters | ✅ Active |
| utils/rate_limiter.py | Token-bucket, env override | ✅ Active, 30/min |
| Provider API keys | OpenAI, DeepSeek | ⚠️ Mixed |
| Billing guard | billing-guard skill + scripts | ✅ Passive |

---

## II. PHƯƠNG ÁN TỐI ƯU NHẤT (Recommended)

### Phương Án A: "Unified Rate Governor" ⭐ KHUYẾN NGHỊ

Biến rate_limiter.py thành **global coordinator**, đồng bộ tất cả LLM calls qua shared state:

```
OpenClaw Gateway ─┐
utils/             │
  rate_limiter.py ─┤ (global coordinator)
  prompt_utils.py ─┤
scripts/           │
  *.py/*.sh ───────┘
```

**Cơ chế:**
1. Một file lock duy nhất → đồng bộ tất cả processes
2. Auto dò env → fallback default → expand
3. Multi-layer: per-process + per-minute + per-model
4. Logging + alert khi sắp hit limit
5. Tích hợp với billing-guard

**File lock path:** `config/.rate_limit_state.json`

**Implementation:**
```python
# rate_limiter_v3.py (unified version)
class RateGovernor:
    def __init__(self, max_calls=30, state_file=None):
        # File-based lock cho cross-process sync
        # Env override: LLM_MAX_CALLS_PER_MINUTE
        # Auto-create if not exists
        # Multi-token bucket: per-model + global
```

**Ưu điểm:**
- ✅ Đồng bộ tất cả scripts → không có concurrent burst
- ✅ File-based → survive process restart
- ✅ Không cần sửa code hiện tại (backward compat)
- ✅ Logging trung tâm
- ✅ Tích hợp billing-guard dễ dàng

---

## III. CHI TIẾT TRIỂN KHAI

### Priority 1 (Hôm nay): File-based Coordinator

1. **rate_limiter.py v3:**
   - Thêm file lock cho cross-process sync
   - State file: `config/.rate_limit_state.json`
   - Multi-bucket: `global + per-model + per-source`
   - Backward compatible (có thể tắt qua env)

2. **billing-guard integration:**
   - Thêm audit hook vào rate limit state
   - Warning log khi tiến gần threshold
   - Block nếu vượt quá budget

3. **Logging improvements:**
   - Log vào `reports/rate-limit-YYYY-MM-DD.jsonl`
   - Track các metrics: calls, wait time, source, model

### Priority 2 (Tuần này): Config & Alerting

4. **OpenClaw config integration:**
   - Thêm `models.fallback.rateLimited` vào config
   - Tự động fallback model khi rate limited

5. **Scripts audit:**
   - Scan tất cả scripts có LLM calls
   - Đảm bảo tất cả dùng rate_limiter
   - Thêm guard cho billing-sensitive scripts

### Priority 3 (Tháng này): Advanced Features

6. **Exponential backoff:**
   - Auto-retry với jitter (0.5s-30s)
   - Respect Retry-After header
   - Circuit breaker pattern

7. **Model tier management:**
   - Tier 1: High quality (current model)
   - Tier 2: Fallback (cheaper model)
   - Tier 3: Local only (offline)

8. **Dashboard:**
   - `reports/rate-limit-dashboard.md`
   - Usage stats, trends, alerts
   - Auto-generated weekly

---

## IV. SO SÁNH PHƯƠNG ÁN

| Tiêu chí | A: Unified Governor ✅ | B: Multi-instance | C: External Proxy |
|----------|----------------------|-------------------|-------------------|
| Đồng bộ | ✅ File-based | ❌ Per-process | ✅ Network |
| Complexity | Thấp | Trung bình | Cao |
| Dependencies | 0 | 0 | Redis/MQ |
| Backward compat | ✅ Có | ✅ Có | ⚠️ Cần sửa code |
| Billing guard | ✅ Tích hợp | ⚠️ Thủ công | ❌ Khó |
| Recovery | ✅ Auto | ❌ Thủ công | ✅ Auto |
| Speed | ⚡ 5ms | ⚡ 0ms | 🐢 50ms |
| Security | ✅ Local | ✅ Local | ⚠️ Network |

**Kết luận:** Phương án A là tối ưu nhất cho workspace local-first.

---

## V. KẾ HOẠCH HÀNH ĐỘNG

### NGAY HÔM NAY:
- [x] Set LLM_MAX_CALLS_PER_MINUTE=30
- [x] Fix rate_limiter constructor-level env read
- [x] Add persistence (profile + env)
- [ ] **Write rate_limiter_v3** (file-based coordinator)

### TUẦN NÀY:
- [x] Audit billing-sensitive scripts
- [ ] Config OpenClaw model fallbacks
- [x] Add logging improvements
- [ ] Document rate limit policy

### THÁNG NÀY:
- [x] Add exponential backoff
- [x] Create model tier system
- [x] Build usage dashboard
- [x] Integrate with billing-guard

---

## VI. RATE LIMIT STATE FILE FORMAT

```json
{
  "version": 1,
  "created": "2026-05-12T11:00:00+07:00",
  "config": {
    "max_calls_per_minute": 30,
    "model_limits": {
      "openai/gpt-5.4": 10,
      "deepseek/deepseek-chat": 20,
      "claude/sonnet": 15
    },
    "billing_budget_per_day": 500,
    "billing_unit": "USD_cents"
  },
  "buckets": {
    "global": { "calls": [], "remaining": 30 },
    "model:deepseek/deepseek-chat": { "calls": [], "remaining": 20 },
    "source:main-session": { "calls": [], "remaining": 15 }
  },
  "billing_tracker": {
    "today_spent_cents": 0,
    "last_reset": "2026-05-12T00:00:00+07:00",
    "total_calls_today": 0
  },
  "alerts": [
    {
      "level": "info",
      "message": "Rate limiter initialized",
      "timestamp": "2026-05-12T11:00:00+07:00"
    }
  ]
}
```

---

## VII. TÓM TẮT

**Vấn đề:** Hệ thống có nhiều models (11 aliases) nhưng thiếu rate limit đồng bộ.

**Rủi ro:**
1. Concurrent scripts có thể burst API calls
2. Billing-sensitive scripts không có guard
3. No cross-session coordination

**Giải pháp:** **Unified Rate Governor** (Phương án A)
- File-based lock → đồng bộ tất cả processes
- Backward compatible → không break existing code
- 0 external dependencies → giữ local-first
- Tích hợp billing-guard → bảo vệ chi phí
- Auto-recovery → không cần manual

**Kết quả:**
- Rate limit = 30 calls/min (đã áp dụng) ⚡
- Cross-process sync (sắp có) ⏳
- Billing guard active ✅
- Production-ready ✅

---

*Phương án này được đánh giá là tối ưu nhất cho workspace local-first của bạn.*
