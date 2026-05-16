from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
RECORDS = ROOT / "tools-internal" / "records" / "rollback-log.jsonl"


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python real_rollback.py <manifest-json> [mode:delete|restore]", "modes": ["delete", "restore"]}, ensure_ascii=False, indent=2))
        return 0

    manifest = Path(sys.argv[1])
    if not manifest.exists():
        print(json.dumps({"error": "manifest-not-found", "path": str(manifest)}, ensure_ascii=False, indent=2))
        return 2

    mode = sys.argv[2] if len(sys.argv) > 2 else "restore"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    acted = []

    for f in data.get("files", []):
        p = Path(f)
        if mode == "delete" and p.exists() and p.is_file():
            p.unlink()
            acted.append({"action": "deleted", "file": str(p)})
            RECORDS.parent.mkdir(parents=True, exist_ok=True)
            with RECORDS.open("a", encoding="utf-8") as log:
                log.write(json.dumps({"action": "deleted", "file": str(p)}, ensure_ascii=False) + "\n")
        elif mode == "restore":
            backup = Path(str(p) + ".bak")
            if backup.exists():
                shutil.copy2(backup, p)
                acted.append({"action": "restored", "file": str(p)})
                with RECORDS.open("a", encoding="utf-8") as log:
                    log.write(json.dumps({"action": "restored", "file": str(p)}, ensure_ascii=False) + "\n")
            elif p.exists() and p.is_file():
                # no backup but file exists - offer delete
                acted.append({"action": "skip-no-backup", "file": str(p)})
            else:
                acted.append({"action": "skip-not-found", "file": str(p)})

    print(json.dumps({"mode": mode, "acted": acted}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
