from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-startup-audit.json"

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True, encoding="utf-8", timeout=20
        )
        lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
        return lines
    except:
        return []

def main() -> int:
    startup = run_pwsh("Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location, User | ConvertTo-Json -Compress")
    scheduled = run_pwsh("Get-ScheduledTask -TaskPath '\\' -EA 0 | Select-Object TaskName, TaskPath, State | ConvertTo-Json -Compress | Select-Object -First 50")
    result = {
        "startupPrograms": startup if startup else [],
        "scheduledTasks": scheduled if scheduled else [],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
