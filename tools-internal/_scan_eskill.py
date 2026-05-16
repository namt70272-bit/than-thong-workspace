#!/usr/bin/env python3
"""Scan E:\skill vs existing system skills — find new ones"""
import os, sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SKILL_DIR = Path(r"E:\skill")
EXISTING_SKILLS = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills")

print("=" * 65)
print("SCAN E:\\skill — SO SANH VOI HE THONG")
print("=" * 65)

# Collect existing skill names (lowercase)
existing_names = set()
for d in EXISTING_SKILLS.iterdir():
    if d.is_dir():
        existing_names.add(d.name.lower())

print(f"\nSkills hien tai trong he thong: {len(existing_names)}")
print(f"  e.g.: {', '.join(sorted(list(existing_names))[:10])}...")

# Scan all SKILL.md files in E:\skill
new_skills = {}  # skill_name -> source_dir
total_found = 0

for group_dir in sorted(SKILL_DIR.iterdir()):
    if not group_dir.is_dir() or group_dir.name.startswith("_"):
        continue
    
    for root, dirs, files in os.walk(str(group_dir)):
        for f in files:
            if f.lower() == "skill.md":
                # The skill name is the directory containing SKILL.md
                skill_name = os.path.basename(root)
                
                # Read the SKILL.md to get the real name
                try:
                    content = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
                    lines = content.strip().split("\n")
                    name_line = lines[0].replace("#", "").strip() if lines else skill_name
                except:
                    name_line = skill_name
                
                if skill_name.lower() not in existing_names:
                    total_found += 1
                    new_skills.setdefault(group_dir.name, []).append({
                        "skill_name": skill_name,
                        "display_name": name_line,
                        "path": os.path.relpath(root, str(SKILL_DIR))
                    })

print(f"\nSkill MOI (chua co trong he thong): {total_found}")
print()

for group, skills in sorted(new_skills.items(), key=lambda x: -len(x[1])):
    print(f"\n{'─' * 50}")
    print(f"📁 {group} ({len(skills)} skills)")
    print(f"{'─' * 50}")
    for s in skills[:10]:
        print(f"  ✅ {s['skill_name']:40s} → {s['display_name'][:50]}")
    if len(skills) > 10:
        print(f"  ... va {len(skills)-10} skills nua")

print(f"\n\nTong cong: {total_found} skills MOI co the khai thac")
print(f"Trong {len(new_skills)} groups")
print()

# Save report
report_path = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\review") / "E-SKILL-NEW-DISCOVERY.md"
with open(str(report_path), "w", encoding="utf-8") as f:
    f.write(f"# Kham pha E:\\skill — Skills moi\n\n")
    f.write(f"**Tong cong: {total_found} skills moi tu {len(new_skills)} groups**\n\n")
    for group, skills in sorted(new_skills.items(), key=lambda x: -len(x[1])):
        f.write(f"## {group} ({len(skills)} skills)\n\n")
        for s in skills:
            f.write(f"- `{s['skill_name']}`: {s['display_name']}\n")
        f.write("\n")

print(f"Report: {report_path}")
print("DONE")
