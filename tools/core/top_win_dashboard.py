from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
RECORDS = ROOT / "tools-internal" / "records"
OUT_JSON = RECORDS / "top-win-dashboard.json"
OUT_MD = RECORDS / "top-win-dashboard.md"

FILES = ["top-win-audit.json", "top-win-cleanup.json", "top-win-process-audit.json", "top-win-data-map.json"]
data = {}
for f in FILES:
    p = RECORDS / f
    if p.exists():
        data[f] = json.loads(p.read_text(encoding="utf-8"))
    else:
        data[f] = None

OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# Top Win Dashboard", ""]
for f, d in data.items():
    lines.append(f"- {'OK' if d else 'MISSING'}: {f}")
OUT_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT_JSON}")
print(f"Wrote {OUT_MD}")
