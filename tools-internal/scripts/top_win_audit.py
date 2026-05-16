from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-audit.json"

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True, encoding="utf-8", timeout=30
        )
        return out.strip()
    except Exception as e:
        return str(e)

def main() -> int:
    result = {
        "os": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "hostname": platform.node(),
        "drives": {},
        "envVars": ["OPENCLAW_HOME", "PATH", "TEMP"],
    }
    for d in "CDEFG":
        drive = f"{d}:"
        free = run_pwsh(f"$dr=Get-PSDrive -Name {d} -EA 0; if($dr){{[math]::Round($dr.Free/1GB,2)}}else{{'?'}}")
        used = run_pwsh(f"$dr=Get-PSDrive -Name {d} -EA 0; if($dr){{[math]::Round($dr.Used/1GB,2)}}else{{'?'}}")
        total = run_pwsh(f"$dr=Get-PSDrive -Name {d} -EA 0; if($dr){{[math]::Round(($dr.Free+$dr.Used)/1GB,2)}}else{{'?'}}")
        result["drives"][drive] = {"freeGB": free, "usedGB": used, "totalGB": total}
    result["envVars"] = {
        v: run_pwsh(f"echo ${v}") for v in result["envVars"]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
