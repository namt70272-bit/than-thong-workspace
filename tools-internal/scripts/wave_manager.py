from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "wave-manager.json"

waves = {
    "wave1": [11, 10, 3, 4],
    "wave2": [1, 2, 6, 16],
    "wave3": [5, 7, 8, 12, 13, 14, 9],
    "wave4": [15],
}
status = {k: {"domains": v, "status": "planned"} for k, v in waves.items()}
OUT.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
