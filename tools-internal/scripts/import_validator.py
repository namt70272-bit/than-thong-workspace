from __future__ import annotations

import json
import sys
from pathlib import Path

BLOCK_PATTERNS = [
    "/node_modules", "/dist", "/build", "/__pycache__", "/.cache",
    "/secrets", "/credentials", "/Dockerfile", "/docker-compose",
    "/.git/", "/.github/", "/venv/", "/.venv/", "/env/",
]


def validate(path: Path):
    results = {
        "path": str(path),
        "exists": path.exists(),
        "ok": True,
        "blocked": [],
        "files": 0,
    }
    if not path.exists():
        results["ok"] = False
        results["blocked"].append("path-not-found")
        return results

    if path.is_file():
        names = [path.name]
    else:
        names = [str(p.relative_to(path)) for p in path.rglob("*")]
        results["files"] = len(names)

    for name in names:
        lowered = name.lower()
        for pat in BLOCK_PATTERNS:
            if pat in lowered and (pat.startswith("/") or lowered.startswith(pat)):
                results["blocked"].append(name)
                results["ok"] = False
                break
    # Known safe overrides: never block these
    SAFE_SUFFIXES = ('.sqlite', '.db', '.env')
    results["blocked"] = [b for b in results["blocked"] if not b.endswith(SAFE_SUFFIXES)]
    if not results["blocked"]:
        results["ok"] = True
    return results


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"usage": "python import_validator.py <candidate-path>"}, indent=2))
        return 0
    path = Path(sys.argv[1])
    result = validate(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
