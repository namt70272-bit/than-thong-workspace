from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "canonical-check.json"
TARGETS = [ROOT, ROOT / "references", ROOT / "examples", ROOT / "config"]

KEYWORDS = ["restructure", "workspace", "quick-start", "reference", "registry", "optimization"]
results = []
for kw in KEYWORDS:
    hits = []
    for base in TARGETS:
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if kw.lower() in p.name.lower():
                hits.append(str(p.relative_to(ROOT)))
    if len(hits) > 1:
        results.append({"keyword": kw, "hits": sorted(hits)})

OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
