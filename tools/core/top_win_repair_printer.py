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
OUT = ROOT / "tools-internal" / "records" / "top-win-repair-printer.json"


def run_pwsh(script: str, timeout: int = 25) -> tuple[bool, str]:
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True,
            encoding="utf-8",
            timeout=timeout,
            stderr=subprocess.STDOUT,
        )
        return True, out.strip()
    except subprocess.CalledProcessError as e:
        return False, (e.output or str(e)).strip()
    except Exception as e:
        return False, str(e)


def get_printers() -> list[dict]:
    ok, out = run_pwsh(
        "Get-Printer | Select-Object Name,DriverName,PortName,PrinterStatus,Default | ConvertTo-Json -Compress"
    )
    if not ok or not out:
        return []
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def get_usb_epson_devices() -> list[dict]:
    ok, out = run_pwsh(
        "Get-PnpDevice -PresentOnly | Where-Object { $_.FriendlyName -match 'EPSON|L1250' -or $_.InstanceId -match 'EPSON|L1250' } | "
        "Select-Object Class,Status,FriendlyName,InstanceId | ConvertTo-Json -Compress"
    )
    if not ok or not out:
        return []
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def get_spooler() -> dict:
    ok, out = run_pwsh(
        "Get-Service Spooler | Select-Object @{Name='StatusName';Expression={$_.Status.ToString()}}, @{Name='StartTypeName';Expression={$_.StartType.ToString()}}, Name, DisplayName | ConvertTo-Json -Compress"
    )
    if not ok or not out:
        return {"status": "unknown", "detail": out}
    try:
        return json.loads(out)
    except Exception:
        return {"status": "unknown", "detail": out}


def get_drivers() -> list[dict]:
    ok, out = run_pwsh(
        "Get-PrinterDriver | Where-Object { $_.Name -match 'EPSON|L1250' } | Select-Object Name,Manufacturer | ConvertTo-Json -Compress"
    )
    if not ok or not out:
        return []
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def build_diagnosis(printers: list[dict], devices: list[dict], spooler: dict, drivers: list[dict]) -> dict:
    epson_printers = [p for p in printers if "EPSON" in (p.get("Name") or "").upper() or "L1250" in (p.get("Name") or "").upper()]
    usb_devices = [d for d in devices if (d.get("Class") or "").upper() in {"USB", "USBDEVICE", "PRINTER"}]
    has_driver = any("EPSON" in (d.get("Name") or "").upper() or "L1250" in (d.get("Name") or "").upper() for d in drivers)
    spooler_running = (spooler.get("StatusName") == "Running")

    symptoms: list[str] = []
    actions: list[str] = []
    handoff: list[str] = []

    if not spooler_running:
        symptoms.append("Print Spooler không ở trạng thái Running.")
        actions.append("Cần restart Spooler và kiểm tra lại danh sách printer.")
        handoff.append("Restart-Service Spooler -Force")

    if usb_devices and not epson_printers:
        symptoms.append("Thiết bị Epson còn hiện diện ở lớp USB/PnP nhưng printer object đã mất khỏi Windows.")
        if has_driver:
            actions.append("Có thể add lại printer USB bằng driver Epson hiện có trên cổng USB001.")
            handoff.append('Add-Printer -Name "EPSON L1250 Series" -DriverName "EPSON L1250 Series" -PortName "USB001"')
        else:
            actions.append("Thiếu driver Epson đăng ký trong Windows; cần cài/khôi phục driver trước.")

    if epson_printers:
        actions.append("Printer Epson đang hiện diện; có thể đặt bản USB làm mặc định để tránh nhầm queue mạng.")
        handoff.append('(Get-CimInstance Win32_Printer | ? Name -eq "EPSON L1250 Series") | Invoke-CimMethod -MethodName SetDefaultPrinter')

    if not symptoms:
        symptoms.append("Không thấy lỗi đăng ký printer rõ ràng ở thời điểm audit.")
        actions.append("Nếu vẫn lỗi khi in, kiểm tra queue, test print, và event log PrintService.")

    return {
        "epsonPrinterCount": len(epson_printers),
        "usbDeviceCount": len(usb_devices),
        "hasEpsonDriver": has_driver,
        "spoolerRunning": spooler_running,
        "symptoms": symptoms,
        "suggestedActions": actions,
        "adminHandoffCommands": handoff,
    }


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "audit"
    printers = get_printers()
    devices = get_usb_epson_devices()
    spooler = get_spooler()
    drivers = get_drivers()
    diagnosis = build_diagnosis(printers, devices, spooler, drivers)

    result = {
        "mode": mode,
        "printers": printers,
        "epsonDevices": devices,
        "spooler": spooler,
        "drivers": drivers,
        "diagnosis": diagnosis,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if mode == "audit":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if mode == "suggest":
        print("=== WIN PRINTER REPAIR SUGGEST ===")
        for item in diagnosis["symptoms"]:
            print(f"- Symptom: {item}")
        for item in diagnosis["suggestedActions"]:
            print(f"- Action: {item}")
        if diagnosis["adminHandoffCommands"]:
            print("- Admin handoff commands:")
            for cmd in diagnosis["adminHandoffCommands"]:
                print(f"  {cmd}")
        return 0

    print(json.dumps({"error": f"unsupported mode: {mode}"}, ensure_ascii=False))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
