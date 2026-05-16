from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
LOG = ROOT / "tools-internal" / "records" / "sync-log.jsonl"


def main() -> int:
    if len(sys.argv) != 3:
        print(json.dumps({"usage": "python sync_executor.py <source-file> <dest-file>"}, ensure_ascii=False, indent=2))
        return 0
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    if not src.exists() or not src.is_file():
        print(json.dumps({"error": "source missing"}, ensure_ascii=False, indent=2))
        return 2
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    rec = {"source": str(src), "dest": str(dst), "mode": "one-way"}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
