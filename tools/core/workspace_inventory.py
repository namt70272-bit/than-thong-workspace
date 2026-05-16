from pathlib import Path
import json

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "workspace-inventory.json"

skip_dirs = {".git", "node_modules", "dist", "build", "__pycache__"}
items = []
for p in ROOT.rglob("*"):
    if any(part in skip_dirs for part in p.parts):
        continue
    items.append({
        "path": str(p.relative_to(ROOT)),
        "type": "dir" if p.is_dir() else "file",
        "size": p.stat().st_size if p.is_file() else 0,
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
