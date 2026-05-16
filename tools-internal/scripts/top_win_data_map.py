from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "top-win-data-map.json"

WATCH_PATHS = [
    ("C:\\Users\\ACER\\.openclaw", "C: runtime config"),
    ("C:\\Users\\ACER\\AppData\\Roaming\\npm", "npm global"),
    ("C:\\Users\\ACER\\AppData\\Local\\Temp", "user temp"),
    ("C:\\Windows\\Temp", "system temp (admin)"),
    ("E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw", "main OpenClaw workspace"),
    ("E:\\KY-DATA\\OpenClaw\\mang-he-thong", "16 mang staging"),
    ("E:\\KY-DATA\\OpenClaw\\code-mirror", "OpenClaw source code"),
    ("G:\\Ai", "external staging - FULL"),
    ("G:\\dang lam", "working in progress"),
]

def run_pwsh(script: str):
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", script], text=True, encoding="utf-8", timeout=15)
        return out.strip()
    except:
        return "?"

def main() -> int:
    results = []
    for path, note in WATCH_PATHS:
        p = Path(path)
        exists = p.exists()
        size_gb = "?"
        file_count = "?"
        if exists:
            sz = run_pwsh(f"if(Test-Path '{path}'){{(Get-ChildItem '{path}' -Recurse -EA 0 | Measure-Object -Property Length -Sum).Sum/1GB}}else{{'?'}}")
            cnt = run_pwsh(f"if(Test-Path '{path}'){{(Get-ChildItem '{path}' -Recurse -EA 0 -File).Count}}else{{'?'}}")
            size_gb = f"{float(sz):.2f}" if sz.replace(".","").isdigit() else "?"
            file_count = cnt
        results.append({
            "path": path,
            "exists": exists,
            "sizeGB": size_gb,
            "fileCount": file_count,
            "note": note,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
