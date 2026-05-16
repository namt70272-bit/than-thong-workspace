from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"


def run_json(script: str, *args: str):
    proc = subprocess.run(["python", str(SCRIPTS / script), *args], text=True, encoding="utf-8", capture_output=True)
    out = proc.stdout
    if proc.returncode not in (0, 2):
        raise RuntimeError(proc.stderr or out)
    try:
        data = json.loads(out)
    except Exception:
        data = {"raw": out}
    data["_returncode"] = proc.returncode
    return data


def main() -> int:
    if len(sys.argv) < 3:
        print(json.dumps({
            "usage": "python billing_wrapper.py <task-text> <internal-script> [script-args...]"
        }, ensure_ascii=False, indent=2))
        return 0
    task = sys.argv[1]
    internal_script = sys.argv[2]
    args = sys.argv[3:]

    gate = run_json("billing_gate.py", task)
    if not gate.get("allowed"):
        print(json.dumps({"blocked": True, "gate": gate}, ensure_ascii=False, indent=2))
        return 2

    policy = json.loads((ROOT / "tools-internal" / "policy" / "billing.policy.json").read_text(encoding="utf-8-sig"))
    if internal_script not in policy.get("internalTrustedScripts", []):
        print(json.dumps({"blocked": True, "reason": "script-not-trusted", "script": internal_script}, ensure_ascii=False, indent=2))
        return 3

    out = subprocess.check_output(["python", str(SCRIPTS / internal_script), *args], text=True, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
