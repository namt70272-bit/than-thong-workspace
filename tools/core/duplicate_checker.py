from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "duplicate-check.json"
SCAN_DIRS = [ROOT / "references", ROOT / "examples", ROOT / "config"]

seen = {}
dups = []
for base in SCAN_DIRS:
    if not base.exists():
        continue
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        try:
            data = p.read_bytes()
        except Exception:
            continue
        h = hashlib.sha256(data).hexdigest()
        rel = str(p.relative_to(ROOT))
        if h in seen:
            dups.append({"original": seen[h], "duplicate": rel})
        else:
            seen[h] = rel

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(dups, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
