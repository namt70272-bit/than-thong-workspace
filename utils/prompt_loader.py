# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Ported from Agent365-devTools (autoTriage/services/prompt_loader.py)
# — simplified, no path search, uses singleton pattern.

"""
Prompt Loader — load & format AI prompts từ YAML.
Singleton pattern tránh reload nhiều lần.

Cách dùng:
  loader = PromptLoader("config/prompts-template.yaml")
  prompt = loader.get("classify_issue_system")
  formatted = loader.format("classify_issue_user", title="...", body="...")
"""
import logging
from pathlib import Path
from typing import Optional

import yaml

logger = logging.getLogger(__name__)


class PromptLoader:
    """Load and format AI prompts from YAML with singleton convenience."""

    _instance: Optional["PromptLoader"] = None
    _prompts: dict[str, str] = {}

    def __new__(cls, path: str | None = None):
        """Singleton: chỉ tạo mới nếu chưa có instance hoặc path khác."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._prompts = {}  # reset per-instance
        return cls._instance

    def __init__(self, path: str | None = None):
        """Khởi tạo loader từ file YAML.

        Args:
            path: Đường dẫn đến file prompts YAML.
                  Nếu None, không load (dùng cache hoặc reload sau).
        """
        if path is not None:
            self._path = path
            if not self._prompts:
                self._load(path)

    def _load(self, path: str) -> None:
        """Load prompts từ file YAML."""
        p = Path(path)
        if not p.exists():
            logger.warning("Prompt file not found: %s", path)
            self._prompts = {}
            return
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            self._prompts = {k: str(v) for k, v in data.items() if isinstance(v, str)}
            logger.info("Loaded %d prompts from %s", len(self._prompts), path)
        except Exception as e:
            logger.error("Failed to load prompts from %s: %s", path, e)
            self._prompts = {}

    def get(self, name: str, default: str = "") -> str:
        """Lấy prompt theo tên."""
        return self._prompts.get(name, default)

    def format(self, name: str, default: str = "", **kwargs) -> str:
        """Lấy prompt và format với variables.

        Args:
            name: Tên prompt.
            default: Giá trị mặc định.
            **kwargs: Variables dạng {key} cần thay thế.

        Returns:
            Prompt đã format, hoặc default nếu không tìm thấy.
            Nếu thiếu variable → log warning và trả về raw prompt.
        """
        prompt = self.get(name, default)
        if not prompt:
            return default
        try:
            return prompt.format(**kwargs)
        except KeyError as e:
            logger.warning("Missing variable %s in prompt '%s'", e, name)
            return prompt

    def reload(self, path: str | None = None) -> None:
        """Force reload từ file."""
        self._load(path or self._path)


def get_prompt_loader(path: str | None = None) -> PromptLoader:
    """Convenience: get singleton PromptLoader instance."""
    return PromptLoader(path)
