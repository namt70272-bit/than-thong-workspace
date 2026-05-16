"""Engine — core lifecycle manager."""
import threading, time, json, os
from pathlib import Path
from than_thong.config import config
from than_thong.logger import log
from than_thong.gate import check_tool
from than_thong.router import route


class ThanThongEngine:
    """Core engine quản lý vòng đời thần thông."""

    def __init__(self):
        self._running = False
        self._thread = None
        self._stats = {
            "started_at": None,
            "blocked": 0,
            "passed": 0,
            "errors": 0,
            "commands_run": 0,
        }
        self._lock = threading.Lock()

    def start(self):
        if self._running:
            return
        self._running = True
        self._stats["started_at"] = time.time()
        log.info("Than-thong engine started")
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        log.info("Than-thong engine stopped")

    @property
    def is_running(self):
        return self._running

    @property
    def stats(self):
        with self._lock:
            return dict(self._stats)

    def record_block(self):
        with self._lock:
            self._stats["blocked"] += 1

    def record_pass(self):
        with self._lock:
            self._stats["passed"] += 1

    def record_error(self):
        with self._lock:
            self._stats["errors"] += 1

    def run_command(self, command: str, *args) -> dict:
        self._stats["commands_run"] += 1
        tool_check = f"cmd:{command}"
        if not check_tool(tool_check):
            self.record_block()
            return {"success": False, "blocked": True}
        self.record_pass()
        return route(command, *args)

    def _loop(self):
        """Background loop (future: periodic health check, log rotation...)."""
        while self._running:
            time.sleep(60)

    def get_status(self) -> dict:
        uptime = time.time() - self._stats["started_at"] if self._stats["started_at"] else 0
        return {
            "engine": "dang_chay" if self._running else "da_dung",
            "thoi_gian_chay_giay": int(uptime),
            "thong_ke": self.stats,
            "cau_hinh": config.data,
        }


engine = ThanThongEngine()
