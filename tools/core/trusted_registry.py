from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
POLICY_PATH = ROOT / "tools-internal" / "policy" / "billing.policy.json"
OUT = ROOT / "tools-internal" / "records" / "trusted-registry.json"
policy = json.loads(POLICY_PATH.read_text(encoding="utf-8-sig"))
trusted = [{"script": s, "trusted": True} for s in policy["internalTrustedScripts"]]
OUT.write_text(json.dumps(trusted, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
