from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\mang-he-thong")
OUT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\records\domain-tracker.json")

rows = []
for domain in sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit()]):
    row = {
        "domain": domain.name,
        "has_source": (domain / "00-Nguon").exists(),
        "has_a0": (domain / "01-Chac-loc-A0").exists(),
        "has_a1": (domain / "02-Can-nhac-A1").exists(),
        "has_b": (domain / "03-Chan-rui-ro-B").exists(),
        "has_imports": (domain / "04-Imports-du-kien").exists(),
        "has_notes": (domain / "05-Ghi-chu").exists(),
        "a0_files": len(list((domain / "01-Chac-loc-A0").glob("*"))) if (domain / "01-Chac-loc-A0").exists() else 0,
    }
    rows.append(row)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
