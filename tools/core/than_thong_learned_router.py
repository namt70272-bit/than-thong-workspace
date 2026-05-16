#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
STORE = ROOT / "tools-internal" / "records" / "than-thong-learned-routes.json"


def load_store() -> dict:
    if not STORE.exists():
        return {"notes": "Seed file for future unsupported-route learning.", "unsupportedExamples": [], "manualMappings": {}}
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except Exception:
        return {"notes": "fallback", "unsupportedExamples": [], "manualMappings": {}}


def save_store(data: dict) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def match(text: str) -> dict | None:
    data = load_store()
    norm = text.strip().lower()
    mapping = data.get("manualMappings", {})
    for key, value in mapping.items():
        if key.strip().lower() in norm:
            return value
    return None


def remember_unsupported(text: str) -> None:
    data = load_store()
    examples = data.setdefault("unsupportedExamples", [])
    if text not in examples:
        examples.append(text)
    save_store(data)


def add_manual_mapping(pattern: str, command: str, args: list[str] | None = None) -> None:
    data = load_store()
    mapping = data.setdefault("manualMappings", {})
    mapping[pattern] = {"command": command, "args": args or []}
    save_store(data)
