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
OUT = ROOT / "tools-internal" / "records" / "win-event-diagnosis.json"


def run_pwsh(script: str, timeout: int = 40) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            stderr=subprocess.STDOUT,
        )
        return True, out.strip()
    except subprocess.CalledProcessError as e:
        return False, (e.output or str(e)).strip()
    except Exception as e:
        return False, str(e)


def fetch_events(hours: int = 24) -> dict:
    scripts = {
        "printservice": (
            "$start=(Get-Date).AddHours(-%d); "
            "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PrintService/Operational'; StartTime=$start} -ErrorAction SilentlyContinue | "
            "Select-Object -First 30 TimeCreated, Id, LevelDisplayName, ProviderName, Message | ConvertTo-Json -Compress"
        ) % hours,
        "system_pnp": (
            "$start=(Get-Date).AddHours(-%d); "
            "Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=$start} -ErrorAction SilentlyContinue | "
            "Where-Object { $_.ProviderName -match 'Kernel-PnP|UserPnp|Service Control Manager|Print' -or $_.Message -match 'printer|EPSON|USB|spooler' } | "
            "Select-Object -First 40 TimeCreated, Id, LevelDisplayName, ProviderName, Message | ConvertTo-Json -Compress"
        ) % hours,
    }
    result = {}
    for key, script in scripts.items():
        ok, out = run_pwsh(script)
        if not ok or not out:
            result[key] = []
            continue
        try:
            data = json.loads(out)
            if isinstance(data, dict):
                result[key] = [data]
            elif isinstance(data, list):
                result[key] = data
            else:
                result[key] = []
        except Exception:
            result[key] = []
    return result


def summarize(events: dict) -> dict:
    print_events = events.get("printservice", [])
    sys_events = events.get("system_pnp", [])

    warnings = [e for e in print_events + sys_events if (e.get("LevelDisplayName") or "") in {"Warning", "Error"}]
    printer_mentions = [e for e in print_events + sys_events if "EPSON" in (e.get("Message") or "").upper() or "PRINTER" in (e.get("Message") or "").upper()]
    usb_mentions = [e for e in sys_events if "USB" in (e.get("Message") or "").upper()]
    spooler_mentions = [e for e in sys_events if "SPOOLER" in (e.get("Message") or "").upper() or e.get("ProviderName") == "Service Control Manager"]

    findings = []
    if warnings:
        findings.append(f"Có {len(warnings)} event mức Warning/Error trong 24h gần đây.")
    if printer_mentions:
        findings.append(f"Có {len(printer_mentions)} event liên quan printer/EPSON.")
    if usb_mentions:
        findings.append(f"Có {len(usb_mentions)} event liên quan USB/PnP.")
    if spooler_mentions:
        findings.append(f"Có {len(spooler_mentions)} event liên quan Spooler/Service Control.")
    if not findings:
        findings.append("Chưa thấy event nổi bật liên quan printer/PnP/Spooler trong cửa sổ thời gian đã quét.")

    return {
        "warningCount": len(warnings),
        "printerEventCount": len(printer_mentions),
        "usbEventCount": len(usb_mentions),
        "spoolerEventCount": len(spooler_mentions),
        "findings": findings,
        "sampleWarnings": warnings[:5],
    }


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "audit"
    hours = 24
    if len(sys.argv) > 2:
        try:
            hours = int(sys.argv[2])
        except ValueError:
            hours = 24

    events = fetch_events(hours)
    diagnosis = summarize(events)
    result = {
        "mode": mode,
        "hours": hours,
        "events": events,
        "diagnosis": diagnosis,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if mode == "audit":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if mode == "suggest":
        print("=== WINDOWS EVENT CORRELATION ===")
        for item in diagnosis["findings"]:
            print(f"- {item}")
        return 0

    print(json.dumps({"error": f"unsupported mode: {mode}"}, ensure_ascii=False))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
