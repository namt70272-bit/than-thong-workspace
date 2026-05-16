from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
MEMORY = ROOT / "memory"
OUT = MEMORY / f"than-thong-{datetime.now().strftime('%Y-%m-%d')}.json"

def main() -> int:
    records_dir = ROOT / "tools-internal" / "records"
    day = datetime.now().strftime("%Y-%m-%d")
    summary = {
        "date": day,
        "records": {},
        "note": "Daily snapshot from than-thong auto-maintain",
    }
    for rec_file in ["workspace-inventory.json", "domain-tracker.json", "ops-dashboard.json",
                     "compliance-audit.json", "duplicate-check.json", "canonical-check.json",
                     "drift-check.json", "bypass-risk-audit.json"]:
        p = records_dir / rec_file
        if p.exists():
            try:
                summary["records"][rec_file] = "ok"
            except:
                summary["records"][rec_file] = "error"

    MEMORY.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
