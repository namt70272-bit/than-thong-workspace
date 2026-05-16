from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
RECORDS = ROOT / "tools-internal" / "records"


def main() -> int:
    if len(sys.argv) < 3:
        print(json.dumps({"usage": "python record_writer.py <record-type> <json-payload>"}, ensure_ascii=False, indent=2))
        return 0
    record_type = sys.argv[1]
    payload = json.loads(sys.argv[2])
    payload["recordType"] = record_type
    payload["createdAt"] = datetime.now().isoformat()
    out = RECORDS / f"{record_type}.jsonl"
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
