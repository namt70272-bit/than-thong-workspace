from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
POLICY = json.loads((ROOT / "tools-internal" / "policy" / "billing.policy.json").read_text(encoding="utf-8-sig"))
SECRET_PATTERNS = [r"sk-[A-Za-z0-9]+", r"Bearer\s+[A-Za-z0-9\-_\.]+", r"api[_-]?key", r"password\s*=", r"token\s*="]


def scan(path: Path):
    findings = []
    MAX_FILES = 500  # safety limit
    count = 0
    blacklist = {"__pycache__", "node_modules", ".git", ".venv", "venv"}
    for p in path.rglob("*") if path.is_dir() else [path]:
        if not p.is_file():
            continue
        # Skip blacklisted dirs
        if any(b in p.parts for b in blacklist):
            continue
        # Skip large files
        if p.stat().st_size > 100_000:
            continue
        count += 1
        if count > MAX_FILES:
            findings.append({"type": "limit", "file": f"...({count} files scanned, stopped at {MAX_FILES})"})
            break
        rel = str(p.relative_to(path if path.is_dir() else p.parent))
        text = ""
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        lower = text.lower()
        for pat in POLICY.get("blockedPathHints", []):
            if pat in rel.lower():
                findings.append({"type": "blocked-path", "file": rel, "hint": pat})
        for pat in POLICY.get("networkCodeHints", []):
            if pat.lower() in lower:
                findings.append({"type": "network-hint", "file": rel, "hint": pat})
        for pat in SECRET_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                findings.append({"type": "secret-hint", "file": rel, "hint": pat})
    findings.append({"type": "info", "file": f"{count} files scanned"})
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"usage": "python deep_validator.py <path>"}, ensure_ascii=False, indent=2))
        return 0
    p = Path(sys.argv[1])
    findings = scan(p)
    result = {"path": str(p), "ok": len(findings) == 0, "findings": findings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 4


if __name__ == "__main__":
    raise SystemExit(main())
