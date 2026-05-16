from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-svc-audit.json"

WATCH_SERVICES = [
    "wuauserv",  # Windows Update
    "BITS",      # Background Intelligent Transfer
    "SysMain",   # SysMain (Superfetch)
    "WSearch",   # Windows Search
    "DiagTrack", # Connected User Experiences and Telemetry
    "DPS",       # Diagnostic Policy Service
    "Spooler",   # Print Spooler
    "Themes",
    "AppXSvc",
    "MapsBroker",
    "XblAuthManager",
    "XblGameSave",
    "XboxNetApiSvc",
    "XboxGipSvc",
]

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True, encoding="utf-8", timeout=15
        )
        return out.strip()
    except:
        return "?"

def main() -> int:
    results = {}
    for svc in WATCH_SERVICES:
        status = run_pwsh(f"Get-Service -Name {svc} -EA 0 | Select-Object Status,StartType,Name | ConvertTo-Json -Compress")
        if status and status != "?":
            try:
                results[svc] = json.loads(status)
            except:
                results[svc] = {"status": "unknown"}
        else:
            results[svc] = {"status": "not-found"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
