from __future__ import annotations

import json
import sys

ROUTES = {
    "preflight": "preflight_runner.py",
    "inventory": "workspace_inventory.py",
    "junk": "find_junk.py",
    "domains": "index_domains.py",
    "duplicate": "duplicate_checker.py",
    "canonical": "canonical_checker.py",
    "track": "domain_tracker.py",
    "candidate": "candidate_builder.py",
    "validate": "import_validator.py",
    "sync": "sync_executor.py",
    "rollback": "rollback_manifest.py",
    "dashboard": "ops_dashboard.py",
}

KEYWORDS = {
    "preflight": ["preflight", "pre-flight", "health check", "system check"],
    "inventory": ["inventory", "index workspace", "quét workspace", "kiểm kê"],
    "junk": ["junk", "rác", "cleanup", "clean"],
    "domains": ["domain", "mảng", "index mảng"],
    "duplicate": ["duplicate", "trùng", "overlap"],
    "canonical": ["canonical", "nguồn sự thật", "single source"],
    "track": ["tracker", "tiến độ", "track"],
    "candidate": ["candidate", "build candidate", "trích vào candidate"],
    "validate": ["validate", "kiểm candidate"],
    "sync": ["sync", "đồng bộ"],
    "rollback": ["rollback", "gỡ"],
    "dashboard": ["dashboard", "tổng quan", "ops"],
}


def route(text: str):
    raw = text.lower()
    for key, hints in KEYWORDS.items():
        if any(h in raw for h in hints):
            return {"route": key, "script": ROUTES[key]}
    return {"route": "unknown", "script": None}


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(json.dumps(route(text), ensure_ascii=False, indent=2))
