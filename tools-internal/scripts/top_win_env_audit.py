from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-env-audit.json"

WATCH_VARS = [
    "OPENCLAW_HOME", "PATH", "TEMP", "TMP", "USERPROFILE",
    "APPDATA", "LOCALAPPDATA", "ProgramData",
    "OneDrive", "OneDriveCommercial",
]

def main() -> int:
    result = {}
    for v in WATCH_VARS:
        val = os.environ.get(v, "")
        issues = []
        if not val:
            issues.append("not-set")
        if v == "TEMP" and val and not os.path.isdir(val):
            issues.append("temp-dir-missing")
        if v == "TMP" and val and not os.path.isdir(val):
            issues.append("tmp-dir-missing")
        result[v] = {"value": val, "issues": issues}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
