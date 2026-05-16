from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "G-source-scan.json"
G_SOURCE = Path(r"G:\Ai")

BLOCKED_HINTS = [
    ".env", "node_modules", "dist", "build", "__pycache__",
    ".db", ".sqlite", ".cache", "docker-compose", "Dockerfile",
    "migration", "migrations", "secrets", "credentials", ".pem"
]

def main() -> int:
    if not G_SOURCE.exists():
        print(json.dumps({"error": "G:\\Ai not found"}, ensure_ascii=False, indent=2))
        return 0

    # Count files by type
    total = 0
    blocked = []
    large_files = []

    for p in G_SOURCE.rglob("*"):
        if not p.is_file():
            continue
        total += 1
        rel = str(p.relative_to(G_SOURCE)).lower()
        for h in BLOCKED_HINTS:
            if h in rel:
                blocked.append(rel)
                break
        size_mb = p.stat().st_size / (1024*1024)
        if size_mb > 100:
            large_files.append({"file": str(rel), "sizeMB": round(size_mb, 1)})

    # Count by extension
    ext_count = {}
    for p in G_SOURCE.rglob("*"):
        if p.is_file():
            ext = p.suffix.lower() or "(no-ext)"
            ext_count[ext] = ext_count.get(ext, 0) + 1

    result = {
        "totalFiles": total,
        "blockedCount": len(blocked),
        "blockedExamples": blocked[:30],
        "largeFiles": sorted(large_files, key=lambda x: x["sizeMB"], reverse=True)[:20],
        "extensions": dict(sorted(ext_count.items(), key=lambda x: -x[1])),
        "note": "G:\\Ai has blocked-pattern content. Manual review needed before any import.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
