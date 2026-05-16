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

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-repair-audio.json"


def run_pwsh(script: str, timeout: int = 25) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", script], text=True, encoding="utf-8", errors="replace", timeout=timeout, stderr=subprocess.STDOUT)
        return True, out.strip()
    except subprocess.CalledProcessError as e:
        return False, (e.output or str(e)).strip()
    except Exception as e:
        return False, str(e)


def get_audio_services() -> list[dict]:
    ok, out = run_pwsh("Get-Service Audiosrv, AudioEndpointBuilder -ErrorAction SilentlyContinue | Select-Object Name,Status,StartType | ConvertTo-Json -Compress")
    if not ok or not out:
        return []
    try:
        data = json.loads(out)
        return data if isinstance(data, list) else [data]
    except Exception:
        return []


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "suggest"
    services = get_audio_services()
    result = {
        "mode": mode,
        "services": services,
        "suggestedActions": [
            "Kiểm tra Windows Audio và AudioEndpointBuilder còn Running không.",
            "Nếu audio mất hoàn toàn, cần handoff admin để restart service hoặc rescan thiết bị."
        ],
        "adminHandoffCommands": [
            "Restart-Service Audiosrv -Force",
            "Restart-Service AudioEndpointBuilder -Force"
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== WIN AUDIO REPAIR SUGGEST ===")
    print(f"- Audio services checked: {len(services)}")
    for item in result["suggestedActions"]:
        print(f"- Action: {item}")
    print("- Admin handoff commands:")
    for cmd in result["adminHandoffCommands"]:
        print(f"  {cmd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
