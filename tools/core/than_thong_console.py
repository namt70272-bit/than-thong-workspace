#!/usr/bin/env python3
"""Thần thông console — cổng vào chính cho điều hành nội bộ"""
import sys, os
from pathlib import Path

# Dynamically locate workspace
ws = Path.cwd()
for _ in range(3):
    if (ws / "AGENTS.md").exists() or (ws / "MEMORY.md").exists():
        break
    ws = ws.parent

# Add scripts to path
scripts_dir = ws / "tools-internal" / "scripts"
if scripts_dir.exists():
    sys.path.insert(0, str(scripts_dir))

# Run ops_console directly (no subprocess overhead)
import ops_console
sys.exit(ops_console.main())
