from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "local-search-index.json"

EXTS = {".md", ".py", ".txt", ".json"}


def build_index() -> dict:
    files = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in EXTS:
            try:
                rel = path.relative_to(ROOT)
            except Exception:
                rel = path
            files.append(str(rel))
    return {"count": len(files), "files": sorted(files)[:2000]}


def main() -> int:
    result = build_index()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Indexed {result['count']} local files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
