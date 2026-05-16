#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = WORKSPACE / "tools-internal" / "scripts"
RECORD = WORKSPACE / "tools-internal" / "records" / "than-thong-supervisor-last.json"

sys.path.insert(0, str(SCRIPTS))
from than_thong_blocklist import inspect  # type: ignore
from than_thong_learned_router import match, remember_unsupported  # type: ignore


def run(parts: list[str]) -> int:
    proc = subprocess.run(parts)
    return proc.returncode


def run_offline_agent(raw: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "than_thong_offline_agent.py"), raw],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.stdout:
        try:
            return json.loads(proc.stdout)
        except Exception:
            return {"mode": "offline-heuristic", "error": proc.stdout}
    return {"mode": "offline-heuristic", "error": "no-output"}


def main() -> int:
    raw = " ".join(sys.argv[1:]).strip()
    check = inspect(raw)
    result = {"input": raw, "blockCheck": check}

    if check["blocked"]:
        result["status"] = "blocked"
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    offline = run_offline_agent(raw)
    result["offlineAgent"] = offline

    learned = match(raw)
    if learned:
        decision = {"status": "ok", **learned, "message": "Route từ learned router"}
    elif offline.get("resolvedRoute"):
        resolved = offline["resolvedRoute"]
        decision = {"status": "ok", "command": resolved["command"], "args": resolved.get("args", []), "message": "Route từ offline agent"}
    else:
        router = subprocess.run(
            [sys.executable, str(SCRIPTS / "than_thong_router.py"), raw],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        decision = {}
        if router.stdout:
            try:
                decision = json.loads(router.stdout)
            except Exception:
                decision = {"status": "unsupported", "message": router.stdout}
        else:
            decision = {"status": "unsupported", "message": "router-no-output"}

    result["routeDecision"] = decision
    status = decision.get("status")

    if status == "ok":
        command = decision["command"]
        args = decision.get("args", [])
        result["status"] = "executing"
        result["resolvedCommand"] = [command, *args]
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return run([sys.executable, str(SCRIPTS / "than_thong_console.py"), command, *args])

    result["status"] = status or "unsupported"
    if result["status"] != "ok":
        remember_unsupported(raw)
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
