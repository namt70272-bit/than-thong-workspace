from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
RECORDS = ROOT / "tools-internal" / "records"
OUT = RECORDS / "compliance-audit.json"

checks = {
    "billingRuleExists": (ROOT / "references" / "compliance" / "BILLING-RULE.md").exists(),
    "billingSkillExists": (ROOT / "skills" / "billing" / "SKILL.md").exists(),
    "billingPolicyExists": (ROOT / "tools-internal" / "policy" / "billing.policy.json").exists(),
    "opsConsoleExists": (ROOT / "tools-internal" / "scripts" / "ops_console.py").exists(),
    "preflightExists": (ROOT / "tools-internal" / "scripts" / "preflight_runner.py").exists(),
    "importOrchestratorExists": (ROOT / "tools-internal" / "scripts" / "import_orchestrator.py").exists(),
}
OUT.write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
