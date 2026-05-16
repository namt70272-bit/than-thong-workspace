from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT_RECORDS = ROOT / "tools-internal" / "records" / "top-win-tighten.json"
OUT_REPORT = ROOT / "tools-internal" / "records" / "top-win-tighten-report.json"

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script],
            text=True, encoding="utf-8", timeout=30
        )
        return out.strip()
    except Exception as e:
        return str(e)

def suggest_svc_changes(services: dict) -> list:
    suggestions = []
    recommendations = {
        "DiagTrack": {"recommend": "Disabled", "reason": "Telemetry service, safe to disable"},
        "XblAuthManager": {"recommend": "Disabled", "reason": "Xbox auth, not needed on non-gaming"},
        "XblGameSave": {"recommend": "Disabled", "reason": "Xbox save, not needed"},
        "XboxNetApiSvc": {"recommend": "Disabled", "reason": "Xbox networking, not needed"},
        "XboxGipSvc": {"recommend": "Disabled", "reason": "Xbox accessories, not needed"},
        "WSearch": {"recommend": "Manual", "reason": "Windows Search indexing, disable if use Everything"},
        "MapsBroker": {"recommend": "Disabled", "reason": "Downloaded maps manager"},
    }
    for svc, info in services.items():
        if isinstance(info, dict) and info.get("status") == "Running":
            if svc in recommendations:
                suggestions.append({
                    "service": svc,
                    "current": "Running",
                    "recommend": recommendations[svc]["recommend"],
                    "reason": recommendations[svc]["reason"],
                })
    return suggestions

def suggest_env_fixes(env_audit: dict) -> list:
    fixes = []
    for var, info in env_audit.items():
        if "not-set" in info.get("issues", []):
            fixes.append({"variable": var, "issue": "not-set", "suggest": "Consider setting this variable"})
    return fixes

def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "audit"
    result = {"mode": mode, "suggestions": [], "note": "Read-only audit unless --apply passed"}

    # Load existing audits
    rec_dir = OUT_RECORDS.parent
    svc_file = rec_dir / "top-win-svc-audit.json"
    env_file = rec_dir / "top-win-env-audit.json"

    svcs = {}
    envs = {}
    if svc_file.exists():
        svcs = json.loads(svc_file.read_text(encoding="utf-8"))
    if env_file.exists():
        envs = json.loads(env_file.read_text(encoding="utf-8"))

    result["suggestions"] = suggest_svc_changes(svcs) + suggest_env_fixes(envs)
    OUT_REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
