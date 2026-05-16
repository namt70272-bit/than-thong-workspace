from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-disk-health.json"

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
    drives = run_pwsh(
        "Get-PSDrive -PSProvider FileSystem | Select-Object Name, Root, Used, Free | ConvertTo-Json -Compress"
    )
    result = {"drives": []}
    if drives and drives != "?":
        try:
            result["drives"] = json.loads(drives)
        except:
            result["raw"] = drives
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
