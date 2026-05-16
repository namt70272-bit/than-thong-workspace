from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"


def run_py(name: str, *args: str):
    cmd = ["python", str(SCRIPTS / name), *args]
    out = subprocess.check_output(cmd, text=True, encoding="utf-8")
    return json.loads(out)


DEFAULT_TEXT = "system health check local first preflight"

def main() -> int:
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_TEXT
    gate = run_py("billing_gate.py", text)
    route = run_py("task_router.py", text)
    result = {"gate": gate, "route": route}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if gate.get("allowed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
