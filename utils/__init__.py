"""
utils package - Unified workspace utilities.

Auto-loads:
  - Rate Governor (file-based cross-process rate limiter)
  - Billing guard integration
  - Rate limiter (backward compatible)

Usage:
    from utils import governor  # Governor singleton
    governor.wait_if_needed(model="deepseek/deepseek-chat", source="script")
    
    # Or for raw access:
    from utils.rate_governor import Governor
    from utils.governor_billing import GovernorWithBilling
    from utils.rate_limiter import RateLimiter  # old API, still works
"""
import os

# Ensure rate limit env var — setd-efault preserves manual overrides
os.environ.setdefault("LLM_MAX_CALLS_PER_MINUTE", "30")
os.environ.setdefault("OPENCLAW_WORKSPACE", os.getcwd())

# Lazy singleton — only imported when actually used
_governor = None

def _get_governor():
    global _governor
    if _governor is None:
        from .rate_governor import Governor
        _governor = Governor()
    return _governor

def governor():
    """Get the global Governor singleton."""
    return _get_governor()

def get_status():
    """Quick status of the global Governor."""
    g = _get_governor()
    s = g.get_status()
    return {
        "rate": f"{s['remaining']}/{s['max_calls_per_minute']} calls/min",
        "circuit_breaker": s["circuit_breaker_state"],
        "today_calls": s["total_calls_today"],
        "budget_spent": f"{s['today_spent_cents']} cents",
        "state_file": s["state_file"],
        "log_file": s["log_file"],
    }

__all__ = ["governor", "get_status", "Governor", "GovernorWithBilling"]
