from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
RECORDS = ROOT / "tools-internal" / "records"
OUT_JSON = RECORDS / "top-win-full-dashboard.json"
OUT_MD = RECORDS / "top-win-full-dashboard.md"

FILES = [
    "top-win-audit.json", "top-win-cleanup.json", "top-win-process-audit.json",
    "top-win-data-map.json", "top-win-env-audit.json", "top-win-svc-audit.json",
    "top-win-startup-audit.json", "top-win-disk-health.json",
    "top-win-tighten-report.json", "top-win-system-restore.json",
]
data = {}
for f in FILES:
    p = RECORDS / f
    if p.exists():
        try:
            data[f] = json.loads(p.read_text(encoding="utf-8"))
        except:
            data[f] = {"error": "parse-failed"}
    else:
        data[f] = None

OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# Top Win Full Dashboard", "", "## Record status"]
for f in FILES:
    d = data[f]
    status = "OK" if d else "MISSING"
    if isinstance(d, list):
        items = len(d)
    elif isinstance(d, dict):
        items = d.get("drives", d.get("suggestions", d.get("status", "ok")))
    else:
        items = ""
    lines.append(f"- {status}: {f} ({items})")
OUT_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT_JSON}")
print(f"Wrote {OUT_MD}")
