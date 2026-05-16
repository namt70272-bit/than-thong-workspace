from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"

JOBS = [
    "workspace_inventory.py",
    "find_junk.py",
    "domain_tracker.py",
    "duplicate_checker.py",
    "canonical_checker.py",
    "drift_checker.py",
    "ops_dashboard.py",
    "compliance_audit.py",
    "bypass_risk_audit.py",
    "top_win_audit.py",
    "top_win_env_audit.py",
    "top_win_svc_audit.py",
    "top_win_startup_audit.py",
    "top_win_process_audit.py",
    "top_win_disk_health.py",
    "top_win_cleanup.py",
    "top_win_data_map.py",
    "top_win_system_restore.py",
    "top_win_dashboard.py",
    "top_win_full_dashboard.py",
]

log_path = ROOT / "tools-internal" / "records" / "auto-maintain-last-run.json"
results = {}
for job in JOBS:
    script = SCRIPTS / job
    if script.exists():
        r = subprocess.run(["python", str(script)], capture_output=True, text=True, timeout=60)
        results[job] = {"exit": r.returncode, "stderr": r.stderr[:200] if r.stderr else ""}
    else:
        results[job] = {"exit": -1, "stderr": "not-found"}
log_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print("Auto-maintain run complete.")
