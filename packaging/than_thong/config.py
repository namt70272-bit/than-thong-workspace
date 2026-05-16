"""Configuration manager — JSON-based, auto-save."""
import json, os
from pathlib import Path

APP_DIR = Path(os.environ.get("APPDATA", Path.home())) / "than-thong"
CONFIG_PATH = APP_DIR / "config.json"
LOG_DIR = APP_DIR / "logs"

DEFAULTS = {
    "auto_start": False,
    "start_minimized": True,
    "enable_service": False,
    "enable_notifications": True,
    "enable_hotkeys": True,
    "hotkey": "ctrl+alt+t",
    "blocked_tools": [
        "web_search", "web_fetch",
        "image_generate", "music_generate", "video_generate"
    ],
    "local_first": True,
    "no_billing": True,
    "theme": "dark",
    "log_level": "INFO",
    "log_retention_days": 30,
    "workspace_dir": str(Path.cwd()),
}


class Config:
    def __init__(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self._data = {}
        self.load()

    def load(self):
        if CONFIG_PATH.exists():
            try:
                raw = CONFIG_PATH.read_text(encoding="utf-8")
                self._data = json.loads(raw)
            except (json.JSONDecodeError, OSError):
                self._data = {}
        for k, v in DEFAULTS.items():
            self._data.setdefault(k, v)
        self.save()

    def save(self):
        CONFIG_PATH.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    @property
    def data(self):
        return dict(self._data)

    @property
    def log_path(self):
        return LOG_DIR / "than-thong.log"

    @property
    def blocked_tools(self):
        return set(self._data.get("blocked_tools", DEFAULTS["blocked_tools"]))


config = Config()
