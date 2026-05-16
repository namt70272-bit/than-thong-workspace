from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "local-knowledge-qa.json"


def score(text: str, query: str) -> int:
    q = query.lower().split()
    t = text.lower()
    return sum(1 for token in q if token in t)


def search_docs(query: str) -> list[dict]:
    hits = []
    for path in ROOT.rglob("*.md"):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        s = score(content + "\n" + str(path), query)
        if s > 0:
            preview = "\n".join(content.splitlines()[:8])
            hits.append({"path": str(path.relative_to(ROOT)), "score": s, "preview": preview})
    hits.sort(key=lambda x: (-x["score"], x["path"]))
    return hits[:10]


def main() -> int:
    query = " ".join(sys.argv[1:]).strip()
    result = {"query": query, "hits": search_docs(query)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
