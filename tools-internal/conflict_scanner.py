#!/usr/bin/env python3
"""Toàn diện conflict scanner — port, file, import, process, skill, version"""
import os, sys, json, socket, subprocess, re
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
WORKSPACE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = TOOLS / "scripts"
ROOT = TOOLS  # current dir
SKILLS = WORKSPACE / "skills"

print("=" * 70)
print("CONFLICT SCANNER — FULL SYSTEM AUDIT")
print("=" * 70)

findings = {"lỗi": [], "cảnh_báo": [], "ok": []}

def add(kind, msg):
    findings[kind].append(msg)

# ============================
# 1. PORT CONFLICTS
# ============================
print("\n1. PORT CONFLICTS")
known_ports = {
    8080: "Dashboard", 9001: "Gateway",
    9876: "System", 9877: "Memory", 9878: "Search", 9879: "LLM",
    9880: "RAG", 9881: "Enhanced",
    11434: "Ollama"
}

# Check which ports are actually in use
import subprocess
try:
    r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=10)
    listening_ports = set()
    for line in r.stdout.splitlines():
        if "LISTENING" in line:
            parts = line.strip().split()
            for p in parts:
                if ":" in p:
                    port_str = p.split(":")[-1]
                    if port_str.isdigit():
                        listening_ports.add(int(port_str))
    
    for port in sorted(known_ports.keys()):
        service = known_ports[port]
        in_use = port in listening_ports
        if in_use:
            print(f"  ✅ {service:15s} :{port} — dang chay")
        else:
            print(f"  ⚠️  {service:15s} :{port} — CHUA CHAY")
    print(f"\n  Tong ports listening: {len(listening_ports)}")
    
except Exception as e:
    print(f"  LOI scan port: {e}")

# ============================
# 2. STDLIB FILE SHADOWING
# ============================
print("\n2. STD LIBRARY SHADOWING")
stdlibs = {"abc","ast","base64","collections","colorsys","contextlib","copy","csv",
           "dataclasses","datetime","decimal","dis","enum","functools","glob","hashlib",
           "html","http","importlib","inspect","io","itertools","json","logging","math",
           "multiprocessing","operator","os","pathlib","pickle","platform","pprint",
           "random","re","secrets","shutil","signal","socket","sqlite3","statistics",
           "string","struct","subprocess","sys","tempfile","textwrap","threading","time",
           "traceback","types","typing","unittest","urllib","uuid","warnings","weakref",
           "xml","zipfile","profile","cProfile","redis","requests"}

all_py_files = list(TOOLS.rglob("*.py"))
shadow_files = []
for f in all_py_files:
    name = f.stem.lower()
    if name in stdlibs and not name.startswith("_") and "reference-library" not in str(f):
        shadow_files.append(f)

if shadow_files:
    for f in shadow_files:
        add("lỗi", f"STDLIB SHADOW: {f.relative_to(TOOLS)} shadows '{f.stem}'")
        print(f"  ❌ {f.relative_to(TOOLS)}")
else:
    print("  ✅ Khong co file shadowing stdlib")

# ============================
# 3. SKILL NAME CONFLICTS
# ============================
print("\n3. SKILL NAME CONFLICTS")
skill_dirs = [d.name.lower() for d in SKILLS.iterdir() if d.is_dir()]
dupes = [d for d in set(skill_dirs) if skill_dirs.count(d) > 1]
if dupes:
    for d in dupes:
        add("cảnh_báo", f"SKILL TRUNG: '{d}' xuat hien {skill_dirs.count(d)} lan")
        print(f"  ⚠️  {d}: {skill_dirs.count(d)} lan")
else:
    print("  ✅ Khong co skill trung ten")

# ============================
# 4. IMPORT RESOLUTION TEST
# ============================
print("\n4. IMPORT RESOLUTION TEST (top tools)")
test_imports = [
    ("fastapi", False), ("fastmcp", False), ("firecrawl", False),
    ("sentence_transformers", False), ("numpy", False), ("httpx", False),
    ("ollama", False), ("openai", False), ("pydantic", False),
    ("uvicorn", False), ("starlette", False), ("qdrant_client", True),
    ("mem0", True), ("transformers", False), ("torch", True),
    ("sqlalchemy", False), ("redis", True),
]

for pkg, optional in test_imports:
    try:
        mod = __import__(pkg)
        ver = getattr(mod, "__version__", "?") 
        print(f"  ✅ {pkg:25s} v{ver}")
    except ImportError as e:
        label = "⚠️  " if optional else "❌ "
        msg = f"{label} {pkg}: {str(e)[:60]}"
        print(f"  {msg}")
        if not optional:
            add("cảnh_báo", f"THIEU PACKAGE: {pkg}")

# ============================
# 5. DUPLICATE FILE PATHS (tools-internal vs scripts)
# ============================
print("\n5. FILE NAME CONFLICTS (tools-internal vs scripts)")
scripts_files = {f.name for f in SCRIPTS.iterdir() if f.suffix == ".py"}
root_files = {f.name for f in TOOLS.iterdir() if f.suffix == ".py" and f.parent == TOOLS}
common = scripts_files & root_files
if common:
    for f in sorted(common):
        add("cảnh_báo", f"FILE TRUNG: '{f}' o ca root va scripts/")
        print(f"  ⚠️  {f}")
else:
    print("  ✅ Khong co file trung ten giua root va scripts/")

# ============================
# 6. MCP SERVER DUPLICATE PROCESSES
# ============================
print("\n6. PROCESS DUPLICATE CHECK")
try:
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"], 
                       capture_output=True, text=True, timeout=10)
    py_count = len([l for l in r.stdout.splitlines() if "python" in l.lower()])
    print(f"  Python processes: {py_count}")
    
    # Check for duplicate MCP servers
    r2 = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=10)
    port_counts = Counter()
    for line in r2.stdout.splitlines():
        for p in known_ports:
            if f":{p} " in line and "LISTENING" in line:
                port_counts[p] += 1
    
    for port, count in port_counts.items():
        if count > 1:
            add("cảnh_báo", f"PORT {port} ({known_ports.get(port,'?')}) co {count} process")
            print(f"  ⚠️  Port {port}: {count} process (can duplicate!)")
except Exception as e:
    print(f"  LOI process scan: {e}")

# ============================
# 7. ENV/VAULT STATUS
# ============================
print("\n7. API KEY STATUS")
env_file = TOOLS / ".env"
vault_file = TOOLS / ".vault.json"
backup_file = TOOLS / ".env.backup"

if vault_file.exists():
    vault = json.loads(vault_file.read_text(encoding="utf-8"))
    print(f"  ✅ Vault: {len(vault['keys'])} keys encrypted")
elif env_file.exists():
    keys = sum(1 for l in env_file.read_text().splitlines() if "=" in l and not l.startswith("#"))
    print(f"  ⚠️  .env plaintext: {keys} keys (nen dung vault)")
    add("cảnh_báo", ".env plaintext — nen dung vault")
else:
    print(f"  ⚠️  Khong co API key storage")
    add("cảnh_báo", "Thieu API key storage")

if backup_file.exists():
    print(f"  ⚠️  .env.backup ton tai — nen xoa sau khi xac nhan vault OK")
    add("cảnh_báo", ".env.backup van ton tai")

# ============================
# 8. SUMMARY
# ============================
print("\n" + "=" * 70)
print("KET QUA CONFLICT SCAN")
print("=" * 70)

print(f"\n  ❌ LOI:    {len(findings['lỗi'])}")
for f in findings["lỗi"]:
    print(f"     - {f}")

print(f"\n  ⚠️  CANH BAO: {len(findings['cảnh_báo'])}")
for f in findings["cảnh_báo"]:
    print(f"     - {f}")

print(f"\n  ✅ OK:     {len(findings['ok'])}")
print()
print("SCAN COMPLETE")
