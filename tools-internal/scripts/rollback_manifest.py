from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUTDIR = ROOT / "tools-internal" / "records" / "rollback-manifests"


def main() -> int:
    files = sys.argv[1:]
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = OUTDIR / f"rollback-{ts}.json"
    payload = {
        "createdAt": ts,
        "files": files,
        "note": "Remove or restore these files if import wave must be rolled back.",
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
