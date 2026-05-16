#!/usr/bin/env python3
from __future__ import annotations

OFFLINE_REGISTRY = {
    "windows": [
        "win-audit", "win-cleanup", "win-process", "win-data", "win-dashboard", "win-env",
        "win-svc", "win-startup", "win-disk", "win-restore", "win-tighten", "win-full",
        "win-repair-printer", "win-repair-spooler", "win-repair-usb", "win-repair-audio", "win-events"
    ],
    "workspace": [
        "inventory", "domains", "junk", "duplicate", "canonical", "track", "drift", "waves", "dashboard",
        "local-search", "docs-miner", "local-qa"
    ],
    "source-intake": [
        "scan-G", "daily", "preflight"
    ],
}


def all_commands() -> list[str]:
    out = []
    for cmds in OFFLINE_REGISTRY.values():
        out.extend(cmds)
    return out
