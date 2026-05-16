from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"
RECORDS = ROOT / "tools-internal" / "records"


def run(name: str, *args: str):
    cmd = ["python", str(SCRIPTS / name), *args]
    out = subprocess.check_output(cmd, text=True, encoding="utf-8").strip()
    try:
        return json.loads(out)
    except Exception:
        return out


def main() -> int:
    if len(sys.argv) != 5:
        print(json.dumps({"usage": "python import_orchestrator.py <source-file> <kind> <candidate-name> <dest-file>"}, ensure_ascii=False, indent=2))
        return 0
    source, kind, candidate_name, dest = sys.argv[1:5]
    build = run("candidate_builder.py", source, kind, candidate_name)
    candidate_path = Path(build["target"])
    validate = run("import_validator.py", str(candidate_path.parent))
    deep = run("deep_validator.py", str(candidate_path))
    dest_path = Path(dest)
    backup_was_created = None
    if dest_path.exists():
        backup = Path(str(dest_path) + ".bak")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest_path, backup)
        backup_was_created = str(backup)
    sync = run("sync_executor.py", build["target"], dest)
    rollback = run("rollback_manifest.py", dest)
    # real_rollback manifest path => kept for later manual use, skip auto-call
    record = {
        "source": source,
        "candidate": build,
        "validate": validate,
        "deep": deep,
        "backup": backup_was_created,
        "sync": sync,
        "rollback": rollback,
    }
    with (RECORDS / "import-orchestrator.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if validate.get("ok") and deep.get("ok") else 5


if __name__ == "__main__":
    raise SystemExit(main())
