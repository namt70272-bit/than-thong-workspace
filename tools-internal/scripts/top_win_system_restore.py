from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-system-restore.json"

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True, encoding="utf-8", timeout=15
        )
        return out.strip()
    except Exception as e:
        return str(e)

def main() -> int:
    rp = run_pwsh("Get-ComputerRestorePoint -EA 0 | Select-Object Description, CreationTime, RestorePointType | ConvertTo-Json -Compress")
    result = {
        "restorePoints": rp if rp and rp != "[]" else "none or access-denied",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
