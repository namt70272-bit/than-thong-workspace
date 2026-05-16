from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-process-audit.json"
WATCH_NAMES = ["python", "node", "openclaw", "powershell", "cmd", "7z", "ffmpeg", "git", "ssh", "docker"]

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", script], text=True, encoding="utf-8", timeout=15)
        return out.strip().splitlines()
    except:
        return []

def main() -> int:
    results = {}
    for name in WATCH_NAMES:
        lines = run_pwsh(f"Get-Process -Name {name} -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, WorkingSet64 | ConvertTo-Json -Compress")
        if lines and lines[0]:
            results[name] = lines
        else:
            results[name] = []
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
