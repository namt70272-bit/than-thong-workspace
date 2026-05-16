#!/usr/bin/env python3
"""Top console — legacy alias, redirects to thần thông"""
import sys
from pathlib import Path

ws = Path.cwd()
for _ in range(3):
    if (ws / "AGENTS.md").exists():
        break
    ws = ws.parent

scripts_dir = ws / "tools-internal" / "scripts"
sys.path.insert(0, str(scripts_dir))

print("👁️  Redirecting to thần thông console...", file=sys.stderr)
import ops_console
sys.exit(ops_console.main())
