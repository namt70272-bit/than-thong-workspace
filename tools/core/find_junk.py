from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
patterns = ["*.bak*", "_*.py", "_*.ps1", "*.old*", "*.tmp*"]

found = []
for pattern in patterns:
    found.extend(ROOT.glob(pattern))

for p in sorted(set(found)):
    print(str(p) if found else "No junk found.")

