from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-cleanup.json"

TEMP_PATTERNS = ["*.tmp", "*.bak", "*.old", "~*", "*.log"]
RISK_DIRS = [
    (r"C:\Users\ACER\AppData\Local\Temp", False),
    (r"C:\Windows\Temp", True),
]

def main() -> int:
    findings = []
    for d, admin in RISK_DIRS:
        p = Path(d)
        if not p.exists():
            continue
        count = 0
        size = 0
        for pattern in TEMP_PATTERNS:
            for f in p.glob(pattern):
                try:
                    sz = f.stat().st_size
                    count += 1
                    size += sz
                except:
                    pass
        findings.append({
            "dir": d,
            "fileCount": count,
            "sizeMB": round(size / (1024*1024), 2),
            "needsAdmin": admin,
        })
    OUT.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
