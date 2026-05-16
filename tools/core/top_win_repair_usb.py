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
OUT = ROOT / "tools-internal" / "records" / "top-win-repair-usb.json"


def run_pwsh(script: str, timeout: int = 25) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", script], text=True, encoding="utf-8", errors="replace", timeout=timeout, stderr=subprocess.STDOUT)
        return True, out.strip()
    except subprocess.CalledProcessError as e:
        return False, (e.output or str(e)).strip()
    except Exception as e:
        return False, str(e)


def get_usb_devices() -> list[dict]:
    ok, out = run_pwsh("Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'USB' } | Select-Object -First 30 Class,Status,FriendlyName,InstanceId | ConvertTo-Json -Compress")
    if not ok or not out:
        return []
    try:
        data = json.loads(out)
        return data if isinstance(data, list) else [data]
    except Exception:
        return []


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "suggest"
    devices = get_usb_devices()
    result = {
        "mode": mode,
        "deviceCount": len(devices),
        "sampleDevices": devices[:10],
        "suggestedActions": [
            "Kiểm tra thiết bị USB hiện diện/biến mất ở lớp PnP.",
            "Nếu thiết bị quan trọng biến mất, cần handoff admin để rescan/rebind driver."
        ],
        "adminHandoffCommands": [
            "pnputil /scan-devices"
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== WIN USB REPAIR SUGGEST ===")
    print(f"- USB devices sampled: {len(devices)}")
    for item in result["suggestedActions"]:
        print(f"- Action: {item}")
    print("- Admin handoff commands:")
    for cmd in result["adminHandoffCommands"]:
        print(f"  {cmd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
