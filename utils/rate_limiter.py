"""
RateLimiter - Token-bucket rate limiter (adapted from autoTriage + Agent365-devTools)
Dùng được local, không cần external deps.

Env override: LLM_MAX_CALLS_PER_MINUTE (int) — thay đổi giới hạn mà không sửa code.
"""
import os
import time
import logging
import threading
from typing import List

logger = logging.getLogger(__name__)

_DEFAULT_MAX_CALLS = 60
_env_val = os.environ.get("LLM_MAX_CALLS_PER_MINUTE")
if _env_val is not None:
    try:
        _DEFAULT_MAX_CALLS = int(_env_val)
    except (TypeError, ValueError):
        logger.warning(
            "LLM_MAX_CALLS_PER_MINUTE=%r không hợp lệ, dùng mặc định %d",
            _env_val, _DEFAULT_MAX_CALLS,
        )


class RateLimiter:
    """Thread-safe token-bucket rate limiter.

    Tracks call timestamps over a rolling window and blocks when limit exceeded.
    Threading.Lock guards _calls for concurrent access (e.g. Azure Functions).
    """

    def __init__(self, max_calls_per_minute: int | None = None):
        if max_calls_per_minute is None:
            max_calls_per_minute = _DEFAULT_MAX_CALLS
            # Re-read env at constructor level so dynamic overrides work
            _env_live = os.environ.get("LLM_MAX_CALLS_PER_MINUTE")
            if _env_live is not None:
                try:
                    max_calls_per_minute = int(_env_live)
                except (TypeError, ValueError):
                    pass
        self._max_calls = int(max_calls_per_minute)
        self._calls: List[float] = []
        self._lock = threading.Lock()

    def wait_if_needed(self) -> None:
        """Block until a call is allowed under the rate limit."""
        with self._lock:
            now = time.monotonic()
            cutoff = now - 60.0
            self._calls = [t for t in self._calls if t > cutoff]
            if len(self._calls) >= self._max_calls:
                wait = max(0.0, self._calls[0] - cutoff)
                if wait > 0:
                    logger.info(
                        "Rate limit %d/%d — chờ %.1fs",
                        len(self._calls), self._max_calls, wait,
                    )
                    time.sleep(wait)
                self._calls = [t for t in self._calls if t > time.monotonic() - 60.0]
            self._calls.append(time.monotonic())

    def remaining(self) -> int:
        """Return remaining calls allowed in current window."""
        with self._lock:
            now = time.monotonic()
            cutoff = now - 60.0
            self._calls = [t for t in self._calls if t > cutoff]
            return max(0, self._max_calls - len(self._calls))

    def reset(self) -> None:
        """Clear all tracked calls."""
        with self._lock:
            self._calls.clear()
