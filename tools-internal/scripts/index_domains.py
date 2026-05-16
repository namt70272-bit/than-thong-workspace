from pathlib import Path

ROOT = Path(r"E:\KY-DATA\OpenClaw\mang-he-thong")
for domain in sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name[0:2].isdigit()]):
    print(domain.name)
    for child in sorted([c for c in domain.iterdir() if c.is_dir()]):
        print(f"  - {child.name}")
