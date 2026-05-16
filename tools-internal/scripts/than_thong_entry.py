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
KNOWN_COMMANDS = {
    "preflight", "inventory", "domains", "junk", "duplicate", "canonical", "track", "drift", "waves", "dashboard",
    "win-audit", "win-cleanup", "win-process", "win-data", "win-dashboard", "win-env", "win-svc", "win-startup",
    "win-disk", "win-restore", "win-tighten", "win-full", "win-repair-printer", "win-repair-spooler", "win-events",
    "scan-G", "daily"
}


def run_command(parts: list[str]) -> int:
    proc = subprocess.run(parts)
    return proc.returncode


def main() -> int:
    args = sys.argv[1:]
    if not args:
        return run_command([sys.executable, str(SCRIPTS / "than_thong_console.py")])

    first = args[0]
    if first in KNOWN_COMMANDS:
        raw = " ".join(args)
        return run_command([sys.executable, str(SCRIPTS / "than_thong_supervisor.py"), raw])

    raw = " ".join(args)
    return run_command([sys.executable, str(SCRIPTS / "than_thong_supervisor.py"), raw])


if __name__ == "__main__":
    raise SystemExit(main())
