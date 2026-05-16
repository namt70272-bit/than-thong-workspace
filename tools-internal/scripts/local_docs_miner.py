from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "local-docs-miner.json"


def mine_docs() -> dict:
    docs = []
    for path in ROOT.rglob("*.md"):
        try:
            rel = path.relative_to(ROOT)
            first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:3]
        except Exception:
            continue
        docs.append({"path": str(rel), "preview": first})
    return {"count": len(docs), "docs": docs[:500]}


def main() -> int:
    result = mine_docs()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Mined {result['count']} markdown docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
