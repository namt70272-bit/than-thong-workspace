from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"
OUT = ROOT / "tools-internal" / "records" / "bypass-risk-audit.json"

required_mentions = {
    "ops_console.py": ["preflight_runner.py"],
    "billing_wrapper.py": ["billing_gate.py"],
    "import_orchestrator.py": ["import_validator.py", "deep_validator.py", "sync_executor.py", "rollback_manifest.py"],
}

results = []
for script, needles in required_mentions.items():
    p = SCRIPTS / script
    text = p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""
    missing = [n for n in needles if n not in text]
    results.append({
        "script": script,
        "ok": len(missing) == 0,
        "missing": missing,
    })

OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
