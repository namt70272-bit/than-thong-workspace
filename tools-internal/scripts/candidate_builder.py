from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
CANDIDATES = ROOT / "expansion" / "candidates"
LOG = ROOT / "tools-internal" / "records" / "candidate-build-log.jsonl"

MAP = {
    "rules": CANDIDATES / "rules",
    "config": CANDIDATES / "config-templates",
    "example": CANDIDATES / "examples",
    "reference": CANDIDATES / "references",
    "script": CANDIDATES / "scripts",
    "util": CANDIDATES / "utils",
    "report": CANDIDATES / "reports",
}


def main() -> int:
    if len(sys.argv) != 4:
        print(json.dumps({
            "usage": "python candidate_builder.py <source-file> <kind> <target-name>",
            "kinds": list(MAP.keys())
        }, ensure_ascii=False, indent=2))
        return 0

    source = Path(sys.argv[1])
    kind = sys.argv[2]
    target_name = sys.argv[3]

    if kind not in MAP:
        print(json.dumps({"error": f"unknown kind: {kind}"}, ensure_ascii=False, indent=2))
        return 2
    if not source.exists() or not source.is_file():
        print(json.dumps({"error": "source file not found"}, ensure_ascii=False, indent=2))
        return 3

    dest_dir = MAP[kind]
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / target_name
    shutil.copy2(source, dest)

    record = {
        "source": str(source),
        "kind": kind,
        "target": str(dest),
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
