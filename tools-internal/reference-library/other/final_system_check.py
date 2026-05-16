#!/usr/bin/env python3
"""Final system check after import"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
SKILLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills'

all_py = [f for f in os.listdir(TOOLS) if f.endswith('.py')]
scripts_py = [f for f in os.listdir(os.path.join(TOOLS, 'scripts')) if f.endswith('.py')]
extracted = os.path.join(TOOLS, 'extracted-scripts')
ext_py = sum(len(files) for _, _, files in os.walk(extracted)) if os.path.exists(extracted) else 0

print("=== FINAL SYSTEM CHECK ===")
print()
print(f"tools-internal/:       {len(all_py)} .py files")
print(f"  scripts/:            {len(scripts_py)} .py files")
print(f"  extracted-scripts/:  {ext_py} .py files (organized)")

skill_dirs = [d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))]
print(f"skills/:               {len(skill_dirs)} skill directories")

# Stdlib conflicts
stdlib = set("abc,ast,base64,collections,colorsys,contextlib,copy,csv,dataclasses,datetime,decimal,dis,enum,functools,glob,hashlib,html,http,importlib,inspect,io,itertools,json,logging,math,multiprocessing,operator,os,pathlib,pickle,platform,pprint,random,re,secrets,shutil,signal,socket,sqlite3,statistics,string,struct,subprocess,sys,tempfile,textwrap,threading,time,traceback,types,typing,unittest,urllib,uuid,warnings,weakref,xml,zipfile".split(","))
conflicts = [f for f in all_py if os.path.splitext(f)[0].lower() in stdlib and not f.startswith("_")]
print(f"Stdlib conflicts:     {'NONE' if not conflicts else str(conflicts)}")

# Port checks
port_pat = re.compile(r'(?:port|PORT)\s*[:=]\s*(\d{3,5})')
critical_ports = {5678, 8000, 8080, 3000, 5000, 5173, 11434}
found = {}
for f in all_py:
    if f.startswith("_"): continue
    try:
        c = open(os.path.join(TOOLS, f), "rb").read().decode("utf-8", errors="replace")[:10000]
        for m in port_pat.finditer(c):
            p = int(m.group(1))
            if p in critical_ports:
                if p not in found: found[p] = []
                found[p].append(f)
    except: pass

if found:
    print(f"Port conflicts:      {sum(len(v) for v in found.values())} files reference system ports")
    for p in sorted(found.keys()):
        print(f"  Port {p}: {', '.join(found[p][:3])}")
else:
    print(f"Port conflicts:      NONE")

# Registry check
reg = os.path.join(SKILLS, "SKILL-REGISTRY.md")
if os.path.exists(reg):
    with open(reg) as f:
        reg_content = f.read()
    lines = [l.strip() for l in reg_content.splitlines() if l.strip().startswith("- `")]
    print(f"SKILL-REGISTRY:      {len(lines)} registered skills")

print()
print("=== CHECK COMPLETE ===")
