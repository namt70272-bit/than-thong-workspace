from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
CAND = ROOT / "expansion" / "candidates"
OUT = ROOT / "tools-internal" / "records" / "drift-check.json"

records = []
for p in CAND.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(CAND)
    # candidate path tail should appear somewhere under workspace targets
    matches = list(ROOT.rglob(rel.name))
    records.append({
        "candidate": str(rel),
        "matchesInWorkspace": [str(m.relative_to(ROOT)) for m in matches if m != p],
        "drift": len(matches) == 0,
    })
OUT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
