#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "than-thong-offline-agent-last.json"

HEURISTICS = [
    ("printer", ["máy in", "printer", "epson", "in ấn", "print"]),
    ("spooler", ["spooler", "queue in", "hàng đợi in", "print service"]),
    ("usb", ["usb", "thiết bị usb", "cắm usb"]),
    ("audio", ["audio", "loa", "mic", "micro", "âm thanh"]),
    ("qa", ["hỏi", "tra cứu", "kiến thức local", "hỏi docs"]),
    ("docs", ["tài liệu", "docs", "markdown", "knowledge", "reference"]),
    ("search", ["tìm local", "tra local", "index", "search file"]),
    ("duplicate", ["duplicate", "trùng lặp", "trùng file"]),
    ("windows", ["windows", "hệ thống", "máy win"]),
]

SUGGESTIONS = {
    "printer": ["win-repair-printer", "suggest"],
    "spooler": ["win-repair-spooler", "suggest"],
    "usb": ["win-repair-usb", "suggest"],
    "audio": ["win-repair-audio", "suggest"],
    "docs": ["docs-miner"],
    "search": ["local-search"],
    "qa": ["local-qa"],
    "duplicate": ["duplicate"],
    "windows": ["win-full"],
}


def infer(text: str) -> dict:
    norm = text.lower()
    matches = []
    for label, keywords in HEURISTICS:
        if any(k in norm for k in keywords):
            matches.append(label)
    primary = matches[0] if matches else None
    suggestions = SUGGESTIONS.get(primary, []) if primary else []
    resolved = None
    if primary == "qa":
        resolved = {"command": "local-qa", "args": [text]}
    elif suggestions:
        resolved = {"command": suggestions[0], "args": suggestions[1:]}
    return {
        "input": text,
        "matchedDomains": matches,
        "primaryDomain": primary,
        "suggestedCommands": suggestions,
        "resolvedRoute": resolved,
        "mode": "offline-heuristic",
    }


def main() -> int:
    raw = " ".join(sys.argv[1:]).strip()
    result = infer(raw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
