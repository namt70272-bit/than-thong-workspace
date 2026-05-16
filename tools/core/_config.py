#!/usr/bin/env python3
"""Central config for thần thông tools — single source of truth for paths"""
import sys
from pathlib import Path

# Detect workspace root dynamically
# Tự phát hiện: nếu chạy từ workspace thì dùng CWD
_POSSIBLE_ROOTS = [
    Path.cwd(),
    Path(__file__).resolve().parent.parent.parent,  # scripts/../../ = workspace
    Path(__file__).resolve().parent.parent,          # tools-internal/
]

# Find the actual workspace by looking for signature files
for root in _POSSIBLE_ROOTS:
    if (root / "AGENTS.md").exists() or (root / "MEMORY.md").exists():
        WORKSPACE = root
        break
    # One level up
    parent = root.parent
    if (parent / "AGENTS.md").exists():
        WORKSPACE = parent
        break
else:
    # Fallback to hardcoded
    WORKSPACE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")

TOOLS_INTERNAL = WORKSPACE / "tools-internal"
SCRIPTS = TOOLS_INTERNAL / "scripts"
RECORDS = TOOLS_INTERNAL / "records"
SKILLS = WORKSPACE / "skills"
POLICY = TOOLS_INTERNAL / "policy"
CANDIDATE = WORKSPACE / "review" / "candidate"

# Map reverse aliases
ROOT = WORKSPACE  # legacy alias
