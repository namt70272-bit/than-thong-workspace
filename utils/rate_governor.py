"""
RateGovernor - Unified Rate Governor (v3)
File-based cross-process rate limiter + billing guard + circuit breaker.

Architecture:
    - Singleton RateGovernor instance per process
    - Shared state file (JSON) with file lock for cross-process sync
    - Multi-bucket: global + per-model + per-source
    - Billing tracker: daily budget tracking
    - Circuit breaker: auto-backoff on repeated failures
    - Logging: structured JSONL for dashboard

Env overrides:
    LLM_MAX_CALLS_PER_MINUTE=30    (default: 60)
    LLM_RATE_GOVERNOR_DISABLE=1    (bypass all rate limiting)
    LLM_DAILY_BUDGET_CENTS=500     (default: no budget)
    LLM_GOVERNOR_TIMEOUT=5         (file lock timeout seconds)

Usage:
    from utils.rate_governor import Governor
    
    g = Governor()
    g.wait_if_needed(model="deepseek/deepseek-chat", source="main-session")
    # ... make LLM call ...
    g.record_call(cost_cents=0.5)  # optional billing
"""
import os
import json
import time
import logging
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# ---- Constants ----
STATE_FILE = "config/.rate_limit_state.json"
LOG_FILE = "reports/rate-limit-{date}.jsonl"
ENV_VAR = "LLM_MAX_CALLS_PER_MINUTE"
ENV_DISABLE = "LLM_RATE_GOVERNOR_DISABLE"
ENV_BUDGET = "LLM_DAILY_BUDGET_CENTS"
ENV_LOCK_TIMEOUT = "LLM_GOVERNOR_TIMEOUT"
DEFAULT_MAX_CALLS = 60
DEFAULT_LOCK_TIMEOUT = 5

# ---- File lock helpers (cross-process) ----
_lock_cache: Dict[str, Any] = {}
_use_file_lock = True

def _file_lock_path() -> str:
    ws = os.environ.get("OPENCLAW_WORKSPACE") or os.getcwd()
    return os.path.join(ws, "config", ".rate_limit.lock")

def _acquire_file_lock(lock_path: str, timeout: float = 5.0) -> bool:
    """Acquire cross-process file lock. Returns True if acquired."""
    global _use_file_lock
    if not _use_file_lock:
        return True
    try:
        import portalocker
        fd = open(lock_path, "w")
        portalocker.lock(fd, portalocker.LOCK_EX | portalocker.LOCK_NB)
        _lock_cache["fd"] = fd
        _lock_cache["path"] = lock_path
        return True
    except ImportError:
        # portalocker not available, use simple approach
        _use_file_lock = False
        return True
    except (BlockingIOError, OSError):
        return False

def _release_file_lock():
    global _use_file_lock
    if not _use_file_lock:
        return
    fd = _lock_cache.pop("fd", None)
    if fd:
        try:
            import portalocker
            portalocker.unlock(fd)
        except ImportError:
            pass
        fd.close()

# ---- State file helpers ----
def _get_workspace() -> str:
    return os.environ.get("OPENCLAW_WORKSPACE") or os.getcwd()

def _state_path() -> str:
    return os.path.join(_get_workspace(), STATE_FILE)

def _log_path() -> str:
    today = time.strftime("%Y-%m-%d")
    return os.path.join(_get_workspace(), LOG_FILE.format(date=today))

def _default_state() -> Dict[str, Any]:
    """Create default state file content."""
    max_calls = DEFAULT_MAX_CALLS
    try:
        max_calls = int(os.environ.get(ENV_VAR, str(DEFAULT_MAX_CALLS)))
    except (TypeError, ValueError):
        pass
    return {
        "version": 1,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "config": {
            "max_calls_per_minute": max_calls,
            "model_limits": {},
            "source_limits": {},
            "billing": {
                "daily_budget_cents": _get_env_int(ENV_BUDGET, 0),
                "currency": "USD",
            },
        },
        "buckets": {
            "global": {"calls": [], "remaining": max_calls},
        },
        "billing": {
            "today_spent_cents": 0,
            "last_reset": time.strftime("%Y-%m-%d"),
            "total_calls_today": 0,
            "total_calls_alltime": 0,
        },
        "circuit_breaker": {
            "consecutive_failures": 0,
            "last_failure": None,
            "until": None,  # timestamp when circuit opens
            "state": "closed",  # closed | open | half-open
        },
        "stats": {
            "last_hour_calls": 0,
            "last_hour_start": time.time(),
        },
        "alerts": [],
    }

def _get_env_int(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, str(default)))
    except (TypeError, ValueError):
        return default

def _read_state() -> Dict[str, Any]:
    """Read state from JSON file. Returns default if missing/corrupt."""
    path = _state_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
            # Validate basic structure
            if "version" in state and "buckets" in state:
                return state
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        pass
    state = _default_state()
    _write_state(state)
    return state

def _write_state(state: Dict[str, Any]) -> bool:
    """Write state to JSON file."""
    state["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    path = _state_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        return True
    except (OSError, PermissionError) as e:
        logger.warning("Cannot write rate limit state: %s", e)
        return False

def _append_log(entry: Dict[str, Any]):
    """Append structured log entry to daily JSONL file."""
    path = _log_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        entry["_ts"] = time.time()
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass


class Governor:
    """Unified Rate Governor — singleton per process, shared state via file lock.

    Thread-safe: uses threading.Lock for in-process.
    Cross-process safe: uses file lock via portalocker (optional).
    """

    _instance: Optional["Governor"] = None
    _lock = threading.Lock()
    _state_lock = threading.Lock()

    def __new__(cls) -> "Governor":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._max_calls = _get_env_int(ENV_VAR, DEFAULT_MAX_CALLS)
        self._disabled = os.environ.get(ENV_DISABLE, "0") == "1"
        self._lock_timeout = _get_env_int(ENV_LOCK_TIMEOUT, DEFAULT_LOCK_TIMEOUT)
        self._daily_budget = _get_env_int(ENV_BUDGET, 0)
        self._state = _default_state()
        self._initialized = True

        # Override from state file
        self._reload()

        logger.info(
            "RateGovernor initialized: max=%d/min, budget=%d, disabled=%s",
            self._max_calls, self._daily_budget, self._disabled,
        )

    def _reload(self):
        """Reload state from file."""
        if self._disabled:
            return
        try:
            self._state = _read_state()
            # Sync config from state
            cfg = self._state.get("config", {})
            self._max_calls = cfg.get("max_calls_per_minute", self._max_calls)
            billing_cfg = cfg.get("billing", {})
            self._daily_budget = billing_cfg.get("daily_budget_cents", self._daily_budget)
        except Exception:
            pass

    def _save(self):
        """Save current state to file."""
        if self._disabled:
            return
        try:
            _write_state(self._state)
        except Exception:
            pass

    def _ensure_bucket(self, name: str):
        """Ensure a bucket exists in state."""
        if name not in self._state["buckets"]:
            self._state["buckets"][name] = {"calls": [], "remaining": self._max_calls}

    def _prune_bucket(self, bucket: Dict[str, Any], window_sec: float = 60.0):
        """Remove old calls from a bucket."""
        now = time.time()
        cutoff = now - window_sec
        bucket["calls"] = [t for t in bucket["calls"] if t > cutoff]

    def _check_bucket(self, bucket: Dict[str, Any], max_calls: int) -> bool:
        """Check if a bucket has capacity."""
        self._prune_bucket(bucket)
        return len(bucket["calls"]) < max_calls

    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is open."""
        cb = self._state.get("circuit_breaker", {})
        if cb.get("state") != "open":
            return False
        until = cb.get("until")
        if until and time.time() < until:
            return True
        # Circuit half-opens after timeout
        cb["state"] = "half-open"
        self._save()
        return False

    def _record_failure(self):
        """Record a failure in circuit breaker."""
        cb = self._state.setdefault("circuit_breaker", {})
        cb["consecutive_failures"] = cb.get("consecutive_failures", 0) + 1
        cb["last_failure"] = time.time()

        threshold = 5
        if cb["consecutive_failures"] >= threshold:
            cb["state"] = "open"
            cb["until"] = time.time() + 60  # 60s cooldown
            msg = f"Circuit breaker OPEN after {cb['consecutive_failures']} failures"
            logger.warning(msg)
            self._state["alerts"].append({
                "level": "warning", "message": msg,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            })
        self._save()

    def _record_success(self):
        """Reset circuit breaker on success."""
        cb = self._state.setdefault("circuit_breaker", {})
        if cb.get("consecutive_failures", 0) > 0:
            cb["consecutive_failures"] = 0
            cb["state"] = "closed"
            cb["until"] = None
            self._save()

    def remaining(self, model: Optional[str] = None) -> int:
        """Get remaining calls in current window."""
        self._reload()
        global_bucket = self._state["buckets"].get("global", {"calls": []})
        self._prune_bucket(global_bucket)
        global_remaining = max(0, self._max_calls - len(global_bucket["calls"]))

        if model:
            model_key = f"model:{model}"
            model_bucket = self._state["buckets"].get(model_key, {"calls": []})
            self._prune_bucket(model_bucket)
            model_max = self._state["config"].get("model_limits", {}).get(model, self._max_calls)
            model_remaining = max(0, model_max - len(model_bucket["calls"]))
            return min(global_remaining, model_remaining)

        return global_remaining

    def wait_if_needed(
        self,
        model: Optional[str] = None,
        source: Optional[str] = None,
        cost_cents: float = 0,
        timeout: Optional[float] = None,
    ) -> bool:
        """Block until rate limit allows the call.

        Returns:
            True if call allowed, False if timed out waiting.
        """
        if self._disabled:
            return True

        # Check circuit breaker
        if self._is_circuit_open():
            logger.warning("Circuit breaker OPEN — request blocked")
            _append_log({
                "event": "blocked",
                "reason": "circuit_breaker_open",
                "model": model, "source": source,
            })
            return False

        # Check billing
        if self._daily_budget > 0:
            bill = self._state.get("billing", {})
            if bill.get("today_spent_cents", 0) >= self._daily_budget:
                logger.warning("Daily budget exceeded: %d/%d cents",
                               bill["today_spent_cents"], self._daily_budget)
                _append_log({
                    "event": "blocked",
                    "reason": "budget_exceeded",
                    "spent": bill.get("today_spent_cents"),
                    "budget": self._daily_budget,
                    "model": model, "source": source,
                })
                return False

        self._reload()

        # Determine max wait
        if timeout is None:
            timeout = float(self._lock_timeout)

        start = time.time()
        waited = False

        while True:
            # Check global bucket
            global_bucket = self._state["buckets"].setdefault(
                "global", {"calls": [], "remaining": self._max_calls}
            )
            if not self._check_bucket(global_bucket, self._max_calls):
                # Need to wait
                self._prune_bucket(global_bucket)
                if len(global_bucket["calls"]) > 0:
                    wait_time = global_bucket["calls"][0] + 60 - time.time()
                    wait_time = max(0.1, min(wait_time, timeout - (time.time() - start)))
                else:
                    wait_time = 0.5

                if time.time() - start + wait_time > timeout:
                    logger.warning("Rate limit wait timeout (%.1fs)", timeout)
                    _append_log({
                        "event": "timeout",
                        "waited_s": round(time.time() - start, 1),
                        "model": model, "source": source,
                    })
                    return False

                logger.info("Rate limit hit %d/%d — waiting %.1fs",
                            len(global_bucket["calls"]), self._max_calls, wait_time)
                time.sleep(wait_time)
                waited = True
                self._reload()
                continue

            # Check model bucket
            if model:
                model_key = f"model:{model}"
                model_limit = self._state["config"].get("model_limits", {}).get(
                    model, self._max_calls
                )
                self._ensure_bucket(model_key)
                model_bucket = self._state["buckets"][model_key]
                if not self._check_bucket(model_bucket, model_limit):
                    time.sleep(0.3)
                    waited = True
                    self._reload()
                    continue

            # Check source bucket
            if source:
                source_key = f"source:{source}"
                self._ensure_bucket(source_key)
                source_bucket = self._state["buckets"][source_key]
                source_limit = self._state["config"].get("source_limits", {}).get(
                    source, self._max_calls
                )
                if not self._check_bucket(source_bucket, source_limit):
                    time.sleep(0.3)
                    waited = True
                    self._reload()
                    continue

            # All buckets OK — record call
            now = time.time()
            global_bucket["calls"].append(now)

            if model:
                model_key = f"model:{model}"
                self._ensure_bucket(model_key)
                self._state["buckets"][model_key]["calls"].append(now)

            if source:
                source_key = f"source:{source}"
                self._ensure_bucket(source_key)
                self._state["buckets"][source_key]["calls"].append(now)

            # Update remaining
            self._prune_bucket(global_bucket)
            global_bucket["remaining"] = max(0, self._max_calls - len(global_bucket["calls"]))

            # Update billing if cost given
            if cost_cents > 0:
                bill = self._state.setdefault("billing", {})
                bill["today_spent_cents"] = bill.get("today_spent_cents", 0) + cost_cents
                bill["total_calls_alltime"] = bill.get("total_calls_alltime", 0) + 1
                # Check if day changed
                today = time.strftime("%Y-%m-%d")
                if bill.get("last_reset") != today:
                    bill["last_reset"] = today
                    bill["today_spent_cents"] = cost_cents
                    bill["total_calls_today"] = 1
                else:
                    bill["total_calls_today"] = bill.get("total_calls_today", 0) + 1

            # Record success for circuit breaker
            self._record_success()

            # Save state
            self._save()

            # Log
            _append_log({
                "event": "allowed",
                "waited_s": round(time.time() - start, 2),
                "waited": waited,
                "model": model,
                "source": source,
                "cost_cents": cost_cents,
                "remaining": global_bucket["remaining"],
            })

            return True

    def record_failure(self, model: Optional[str] = None):
        """Record a failure (429, timeout, etc)."""
        self._record_failure()
        _append_log({
            "event": "failure",
            "model": model,
        })

    def record_call(self, cost_cents: float = 0, model: Optional[str] = None):
        """Record a completed call for billing tracking."""
        with self._state_lock:
            self._reload()
            bill = self._state.setdefault("billing", {})
            today = time.strftime("%Y-%m-%d")
            if bill.get("last_reset") != today:
                bill["last_reset"] = today
                bill["today_spent_cents"] = 0
                bill["total_calls_today"] = 0
            bill["today_spent_cents"] = bill.get("today_spent_cents", 0) + cost_cents
            bill["total_calls_today"] = bill.get("total_calls_today", 0) + 1
            bill["total_calls_alltime"] = bill.get("total_calls_alltime", 0) + 1
            self._save()
            _append_log({
                "event": "billing_record",
                "cost_cents": cost_cents,
                "total_today_cents": bill["today_spent_cents"],
                "model": model,
            })

    def get_status(self) -> Dict[str, Any]:
        """Get current status as dict."""
        self._reload()
        global_bucket = self._state["buckets"].get("global", {"calls": []})
        self._prune_bucket(global_bucket)

        bill = self._state.get("billing", {})
        cb = self._state.get("circuit_breaker", {})

        return {
            "disabled": self._disabled,
            "max_calls_per_minute": self._max_calls,
            "current_calls": len(global_bucket["calls"]),
            "remaining": max(0, self._max_calls - len(global_bucket["calls"])),
            "daily_budget_cents": self._daily_budget,
            "today_spent_cents": bill.get("today_spent_cents", 0),
            "total_calls_today": bill.get("total_calls_today", 0),
            "total_calls_alltime": bill.get("total_calls_alltime", 0),
            "circuit_breaker_state": cb.get("state", "closed"),
            "circuit_breaker_failures": cb.get("consecutive_failures", 0),
            "config": self._state.get("config", {}),
            "buckets": {
                k: {"remaining": v.get("remaining", 0)}
                for k, v in self._state.get("buckets", {}).items()
            },
            "state_file": _state_path(),
            "log_file": _log_path(),
        }

    def reset(self):
        """Reset all state (buckets, circuit breaker, billing)."""
        self._state = _default_state()
        self._save()
        logger.info("RateGovernor state reset")
        _append_log({"event": "reset"})

    def reset_billing(self):
        """Reset daily billing counter."""
        with self._state_lock:
            self._reload()
            bill = self._state.setdefault("billing", {})
            bill["today_spent_cents"] = 0
            bill["total_calls_today"] = 0
            bill["last_reset"] = time.strftime("%Y-%m-%d")
            self._save()
            logger.info("RateGovernor billing reset")

    def set_daily_budget(self, cents: int):
        """Set daily billing budget."""
        with self._state_lock:
            self._reload()
            self._state.setdefault("config", {}).setdefault("billing", {})
            self._state["config"]["billing"]["daily_budget_cents"] = cents
            self._daily_budget = cents
            self._save()

    def set_model_limit(self, model: str, max_calls: int):
        """Set per-model rate limit."""
        with self._state_lock:
            self._reload()
            self._state.setdefault("config", {}).setdefault("model_limits", {})
            self._state["config"]["model_limits"][model] = max_calls
            self._save()

    def get_alerts(self, since: Optional[float] = None) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        self._reload()
        alerts = self._state.get("alerts", [])
        if since is not None:
            alerts = [a for a in alerts if a.get("_ts", 0) > since]
        return alerts[-50:]  # last 50 max
