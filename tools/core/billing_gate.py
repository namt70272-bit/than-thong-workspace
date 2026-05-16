from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

WORKSPACE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
POLICY_PATH = WORKSPACE / "tools-internal" / "policy" / "billing.policy.json"
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8-sig"))

SAFE_INTERNAL_PHRASES = [
    "no billing", "billing rule", "billing gate", "billing policy",
    "billing wrapper", "billing audit", "under billing",
    "billing is negative", "avoid billing", "billing risk",
    "billing guard", "top gate", "top rule", "top wrapper",
    "thần thông", "than thong", "than_thong",
    "local only", "local-first", "local first", "internal only",
]


@dataclass
class GateResult:
    allowed: bool
    mode: str
    reason: str
    billingRisk: bool
    internetNeeded: bool
    localCapable: bool
    confidence: str
    matched: List[str]


def classify(text: str) -> GateResult:
    raw = (text or "").lower().strip()
    matched: List[str] = []

    # Check safe internal phrases first
    is_safe_internal = any(p in raw for p in SAFE_INTERNAL_PHRASES)

    paid = any(h in raw for h in POLICY["paidRiskHints"])
    internet = any(h in raw for h in POLICY["internetHints"])
    local = any(k in raw for k in ["local", "workspace", "file", "script", "candidate", "import", "cleanup", "inventory", "reference", "template", "windows", "win-"])

    # If "billing" only appears in safe context, neutralize false positive
    if is_safe_internal and paid:
        # Recheck after neutralizing billing as a keyword
        neutralized = raw
        for p in SAFE_INTERNAL_PHRASES:
            neutralized = neutralized.replace(p, "")
        paid = any(h in neutralized for h in POLICY["paidRiskHints"] if h != "billing")

    # Collect matches
    if paid:
        matched.append("paid-risk")
    if internet:
        matched.append("internet")

    if paid:
        return GateResult(False, "block", "Paid/provider/billing risk detected by policy. Stop and ask first.", True, internet, local, "high", sorted(set(matched)))

    if not raw:
        return GateResult(True, "allow", "Empty task classified as safe local context (default allow).", False, False, True, "medium", [])

    if is_safe_internal:
        matched.append("internal-trusted")
        return GateResult(True, "local-trusted", "Trusted internal/local task allowed by billing policy.", False, internet, True, "high", sorted(set(matched)))

    if internet and not local:
        return GateResult(True, "warn", "Internet may be required. Keep read-only and avoid all paid/provider paths.", False, True, False, "medium", sorted(set(matched)))

    return GateResult(True, "allow", "Local-first task allowed by billing rule.", False, internet, True, "high", sorted(set(matched)))


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python billing_gate.py <task-text>", "policy": str(POLICY_PATH)}, ensure_ascii=False, indent=2))
        return 0
    text = " ".join(sys.argv[1:])
    result = classify(text)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
