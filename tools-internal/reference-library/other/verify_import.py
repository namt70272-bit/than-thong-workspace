#!/usr/bin/env python3
"""Verify import success"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
SKILLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills'
SKILL_REG = os.path.join(SKILLS, 'SKILL-REGISTRY.md')

stdlibs = {'abc','ast','base64','collections','colorsys','contextlib','copy','csv','dataclasses',
           'datetime','decimal','dis','enum','functools','glob','hashlib','html','http','importlib',
           'inspect','io','itertools','json','logging','math','multiprocessing','operator','os',
           'pathlib','pickle','platform','pprint','random','re','secrets','shutil','signal','socket',
           'sqlite3','statistics','string','struct','subprocess','sys','tempfile','textwrap',
           'threading','time','traceback','types','typing','unittest','urllib','uuid','warnings',
           'weakref','xml','zipfile'}

print('=' * 60)
print('KIEM TRA SAU KHI NHAP:')
print('=' * 60)

# 1) Stdlib conflicts
conflicts = []
for f in os.listdir(TOOLS):
    name = os.path.splitext(f)[0].lower()
    if name in stdlibs and not name.startswith('_'):
        conflicts.append(f)

print(f'\n1. Xung dot stdlib: {"KHONG CO" if not conflicts else f"⚠️ {conflicts}"}')

# 2) Skills count
skill_dirs = [d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))]
print(f'2. Skills directory: {len(skill_dirs)} skills')

# 3) Tools count
tool_py = [f for f in os.listdir(TOOLS) if f.endswith('.py')]
tool_scripts = [f for f in os.listdir(os.path.join(TOOLS, 'scripts')) if f.endswith('.py')]
print(f'3. tools-internal/: {len(tool_py)} .py files')
print(f'   tools-internal/scripts/: {len(tool_scripts)} .py files')

# 4) SKILL-REGISTRY size
if os.path.exists(SKILL_REG):
    size = os.path.getsize(SKILL_REG)
    print(f'4. SKILL-REGISTRY.md: {size} bytes')

# 5) Rollback manifests
records = os.path.join(TOOLS, 'records')
if os.path.exists(records):
    manifests = [f for f in os.listdir(records) if f.startswith('rollback-')]
    waves = [f for f in os.listdir(records) if f.startswith('wave-')]
    print(f'5. Rollback manifests: {len(manifests)}')
    print(f'   Wave records: {len(waves)}')

# 6) Check key files exist
# from extract_skills
key_skills = ['review-pr', 'review-staged', 'salacia-gc', 'clone-website', 'chat-history-search',
              'clawteam', 'land', 'landpr', 'triage', 'fleet']
existing = [s for s in key_skills if os.path.isdir(os.path.join(SKILLS, s))]
print(f'6. Key skills da co: {len(existing)}/{len(key_skills)} — {", ".join(existing)}')

# 7) Total import size
total_bytes = 0
for f in tool_py:
    total_bytes += os.path.getsize(os.path.join(TOOLS, f))
print(f'7. Tong dung luong tools-internal: {total_bytes/1024:.0f} KB')

print('\n' + '=' * 60)
print('✅ KIEM TRA HOAN TAT')
print('=' * 60)
