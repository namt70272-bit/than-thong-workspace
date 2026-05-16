from pathlib import Path
import subprocess
import sys

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"

raise SystemExit(subprocess.call(["python", str(SCRIPTS / "billing_gate.py"), *sys.argv[1:]]))
