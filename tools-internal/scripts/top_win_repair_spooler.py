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
OUT = ROOT / "tools-internal" / "records" / "top-win-repair-spooler.json"


def run_pwsh(script: str, timeout: int = 20) -> tuple[bool, str]:
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


def get_dependent_services() -> list[dict]:
    ok, out = run_pwsh(
        "Get-Service Spooler -DependentServices | Select-Object Name,DisplayName,Status | ConvertTo-Json -Compress"
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


def get_recent_spooler_events(hours: int = 24) -> list[dict]:
    script = (
        "$start=(Get-Date).AddHours(-%d); "
        "Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=$start} -ErrorAction SilentlyContinue | "
        "Where-Object { $_.ProviderName -match 'Service Control Manager|Print|Spooler' } | "
        "Select-Object -First 20 TimeCreated, ProviderName, Id, LevelDisplayName, Message | ConvertTo-Json -Compress"
    ) % hours
    ok, out = run_pwsh(script, timeout=30)
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


def build_diagnosis(spooler: dict, deps: list[dict], events: list[dict]) -> dict:
    status = spooler.get("StatusName")
    start_type = spooler.get("StartTypeName")
    symptoms: list[str] = []
    actions: list[str] = []
    handoff: list[str] = []

    if status != "Running":
        symptoms.append(f"Print Spooler đang ở trạng thái {status or 'unknown'}.")
        actions.append("Cần restart Print Spooler và kiểm tra lại printer list / queue.")
        handoff.append("Restart-Service Spooler -Force")
    else:
        actions.append("Print Spooler đang chạy bình thường ở thời điểm audit.")

    if start_type != "Automatic":
        symptoms.append(f"Spooler StartType hiện là {start_type or 'unknown'}, không phải Automatic.")
        actions.append("Nên đặt Spooler về Automatic để tránh mất printer object sau reboot.")
        handoff.append("Set-Service -Name Spooler -StartupType Automatic")

    if deps:
        actions.append(f"Có {len(deps)} dependent service(s) gắn với Spooler; cần lưu ý trước khi restart ở môi trường nhạy cảm.")

    if events:
        actions.append("Đã thu thập event liên quan Spooler/Print để correlation thêm nếu sự cố tái diễn.")

    if not symptoms:
        symptoms.append("Không thấy lỗi Spooler rõ ràng ở thời điểm audit.")

    return {
        "status": status,
        "startType": start_type,
        "dependentServiceCount": len(deps),
        "eventCount": len(events),
        "symptoms": symptoms,
        "suggestedActions": actions,
        "adminHandoffCommands": handoff,
    }


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "audit"
    spooler = get_spooler()
    deps = get_dependent_services()
    events = get_recent_spooler_events()
    diagnosis = build_diagnosis(spooler, deps, events)

    result = {
        "mode": mode,
        "spooler": spooler,
        "dependentServices": deps,
        "events": events,
        "diagnosis": diagnosis,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if mode == "audit":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if mode == "suggest":
        print("=== WIN SPOOLER REPAIR SUGGEST ===")
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
