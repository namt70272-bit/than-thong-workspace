from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
RECORDS = ROOT / "tools-internal" / "records"
OUT_JSON = RECORDS / "ops-dashboard.json"
OUT_MD = RECORDS / "ops-dashboard.md"

files = [
    "workspace-inventory.json",
    "domains-index.txt",
    "junk-scan.txt",
    "domain-tracker.json",
    "duplicate-check.json",
    "canonical-check.json",
]
status = {}
for f in files:
    p = RECORDS / f
    status[f] = p.exists()

payload = {"records": status}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

lines = ["# Ops Dashboard", "", "## Record status"]
for name, ok in status.items():
    lines.append(f"- {'OK' if ok else 'MISSING'}: {name}")
OUT_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT_JSON}")
print(f"Wrote {OUT_MD}")
