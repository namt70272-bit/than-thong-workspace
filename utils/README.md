# Utils Guide

## Purpose
Các file trong `utils/` không phải duplicate mù; mỗi file có vai trò riêng.

## Files

### `rate_limiter.py`
- Rate limiter đơn giản
- Token-bucket/thread-safe
- Dùng khi chỉ cần throttle local, nhẹ, ít phụ thuộc

### `rate_governor.py`
- Bản nâng cao
- Cross-process sync qua state file + lock
- Có billing guard + circuit breaker + logging
- Dùng cho orchestration/usage control nghiêm ngặt hơn

### `prompt_loader.py`
- Loader dạng object/singleton
- Load prompt YAML và format prompt
- Phù hợp khi cần một loader instance dùng lặp lại

### `prompt_utils.py`
- Utility functions
- Load/render prompt
- sanitize user content / LLM output / exception
- Phù hợp cho safety layer và xử lý text

## Rule of thumb
- Cần throttle nhẹ -> `rate_limiter.py`
- Cần governance/budget/cross-process -> `rate_governor.py`
- Cần object loader -> `prompt_loader.py`
- Cần sanitize + helper functions -> `prompt_utils.py`
