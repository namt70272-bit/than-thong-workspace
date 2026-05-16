#!/usr/bin/env python
"""FINAL HARDENING — toàn diện kiểm tra + gia cố hệ thống"""
import os, sys, json, subprocess, socket, stat
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
WORKSPACE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = TOOLS / "scripts"
SKILLS = WORKSPACE / "skills"
PYTHON = "python"  # Python 3.11 — đã confirm

results = {"pass": [], "warn": [], "fail": [], "fixed": []}

def P(msg): print(f"  ✅ {msg}"); results["pass"].append(msg)
def W(msg): print(f"  ⚠️  {msg}"); results["warn"].append(msg)
def F(msg): print(f"  ❌ {msg}"); results["fail"].append(msg)
def X(msg): print(f"  🔧 {msg}"); results["fixed"].append(msg)

print("=" * 65)
print("FINAL HARDENING — KIEM TRA & GIA CO")
print("=" * 65)

# ============================
# 1. PORT CONFLICT CHECK
# ============================
print("\n1. PORT CONFLICT CHECK")
services = {8080: "Dashboard", 9001: "Gateway", 9876: "System", 9877: "Memory",
            9878: "Search", 9879: "LLM", 9880: "RAG", 9881: "Enhanced", 11434: "Ollama"}

try:
    r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=10)
    listening = set()
    for line in r.stdout.splitlines():
        if "LISTENING" in line:
            parts = line.strip().split()
            for p in parts:
                if ":" in p:
                    ps = p.split(":")[-1]
                    if ps.isdigit(): listening.add(int(ps))
    
    for port, name in services.items():
        if port in listening:
            P(f"{name} :{port}")
        else:
            W(f"{name} :{port} — offline (can start khi can)")
    
    # Check for duplicates
    for port in sorted(services.keys()):
        in_list = [l for l in r.stdout.splitlines() if f":{port} " in l and "LISTENING" in l]
        if len(in_list) > 1:
            F(f"PORT {port} — {len(in_list)} process cung luc (fix: kill one)")
except Exception as e:
    W(f"Port scan: {e}")

# ============================
# 2. COMPILE ALL KEY SCRIPTS
# ============================
print("\n2. COMPILATION CHECK")
key_scripts = [
    "agent_mcp_server.py", "mcp_memory_server.py", "mcp_search_server.py",
    "mcp_llm_server.py", "mcp_rag_server.py", "mcp_enhanced_server.py",
    "api_gateway.py", "dashboard_web.py", "load_env.py", "vault.py",
    "service_discovery.py", "auth_system.py", "finance_module.py",
    "web_tools.py", "rag_engine.py",
]
for s in key_scripts:
    fp = TOOLS / s
    if fp.exists():
        try:
            compile(fp.read_bytes(), s, "exec")
            P(f"{s}")
        except SyntaxError as e:
            F(f"{s}: {e}")
    else:
        F(f"{s}: FILE NOT FOUND")

# Scripts/ directory
for f in sorted(SCRIPTS.glob("*.py")):
    try:
        compile(f.read_bytes(), f.name, "exec")
    except SyntaxError as e:
        F(f"scripts/{f.name}: {e}")

# ============================
# 3. IMPORT RESOLUTION
# ============================
print("\n3. IMPORT RESOLUTION")
packages = [
    ("fastapi", False), ("fastmcp", False), ("firecrawl", False),
    ("uvicorn", False), ("starlette", False), ("httpx", False),
    ("numpy", False), ("openai", False), ("pydantic", False),
    ("sentence_transformers", False), ("ollama", False),
    ("qdrant_client", True), ("mem0", True), ("transformers", True),
    ("torch", True), ("sqlalchemy", False),
]
for pkg, optional in packages:
    try:
        mod = __import__(pkg)
        ver = getattr(mod, "__version__", "ok")
        P(f"{pkg} v{ver}")
    except ImportError:
        if optional:
            W(f"{pkg} — optional, khong anh huong")
        else:
            F(f"{pkg} — THIEU (can: pip install {pkg})")

# ============================
# 4. VAULT + API KEYS
# ============================
print("\n4. API KEY SECURITY")
vault_file = TOOLS / ".vault.json"
key_file = TOOLS / ".vault_key"
env_file = TOOLS / ".env"
bak_file = TOOLS / ".env.backup"

if vault_file.exists():
    P("Vault: ton tai")
    vault_file.chmod(0o600)
    X("Vault permissions set to 600")
else:
    F("Vault: KHONG CO")

if key_file.exists():
    P("Vault key: ton tai")
    key_file.chmod(0o600)
    X("Vault key permissions set to 600")

if env_file.exists():
    env_text = env_file.read_text()
    if "sk-" in env_text or "fc-" in env_text:
        F(".env: van chua API keys plaintext")
    else:
        P(".env: placeholder safe")

if not bak_file.exists():
    P(".env.backup: da xoa")
else:
    W(".env.backup: con ton tai")

# ============================
# 5. STARTUP SCRIPT CHECK
# ============================
print("\n5. STARTUP AUTO-START")
startup_path = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
bat_file = startup_path / "MCP_Ecosystem.bat"

if bat_file.exists():
    content = bat_file.read_text()
    if "python" in content and "python3" not in content:
        P(f"Startup bat: {bat_file}")
    else:
        W("Startup bat: van con 'python3' — can fix")
else:
    W("Startup bat: KHONG CO — auto-start se khong chay")

# ============================
# 6. THAN THONG CONSOLE COMMANDS
# ============================
print("\n6. THAN THONG CONSOLE COMMANDS")
console = SCRIPTS / "than_thong_console.py"
if console.exists():
    try:
        r = subprocess.run([PYTHON, str(console)], capture_output=True, text=True, timeout=10)
        cmds = json.loads(r.stdout).get("commands", [])
        P(f"Console: {len(cmds)} commands available")
        # Test key commands
        for cmd in ["dashboard", "preflight", "duplicate", "inventory"]:
            try:
                r2 = subprocess.run([PYTHON, str(console), cmd], capture_output=True, text=True, timeout=15)
                if r2.returncode == 0: P(f"  {cmd}")
                else: W(f"  {cmd}: exit code {r2.returncode}")
            except: W(f"  {cmd}: timeout")
    except Exception as e:
        W(f"Console: {e}")

# ============================
# 7. SKILLS INTEGRITY
# ============================
print("\n7. SKILLS INTEGRITY")
skill_dirs = sorted([d for d in SKILLS.iterdir() if d.is_dir()])
has_skillmd = sum(1 for d in skill_dirs if (d/"SKILL.md").exists())
P(f"Skills: {len(skill_dirs)} total, {has_skillmd} co SKILL.md")
if len(skill_dirs) != has_skillmd:
    W(f"{len(skill_dirs) - has_skillmd} skills thieu SKILL.md")

# ============================
# 8. PERMISSIONS
# ============================
print("\n8. PERMISSIONS & SENSITIVE FILES")
sensitive = [".vault.json", ".vault_key", ".env"]
for fname in sensitive:
    fp = TOOLS / fname
    if fp.exists():
        try:
            perms = oct(fp.stat().st_mode)[-3:]
            if int(perms) > 600:
                fp.chmod(0o600)
                X(f"{fname}: permissions tightened to 600 (was {perms})")
            else:
                P(f"{fname}: permissions {perms}")
        except:
            W(f"{fname}: cannot check permissions")

# ============================
# 9. UNUSED/ORPHAN FILES
# ============================
print("\n9. ORPHAN CHECK")
reference = TOOLS / "reference-library"
if reference.exists():
    count = sum(1 for _ in reference.rglob("*.py"))
    P(f"Reference library: {count} files in 21 categories")

scripts_count = len([f for f in SCRIPTS.glob("*.py")])
P(f"Thần thông scripts: {scripts_count}")

# ============================
# SUMMARY
# ============================
print("\n" + "=" * 65)
print("HARDENING SUMMARY")
print("=" * 65)
print(f"\n  ✅ PASS:  {len(results['pass'])}")
print(f"  ⚠️  WARN:  {len(results['warn'])}")
print(f"  ❌ FAIL:  {len(results['fail'])}")
print(f"  🔧 FIXED: {len(results['fixed'])}")
print()

if results["warn"]:
    print("WARNINGS (khong nghiem trong):")
    for w in results["warn"]:
        print(f"  ⚠️  {w}")

if results["fail"]:
    print("\nFAILURES (can xu ly):")
    for f in results["fail"]:
        print(f"  ❌ {f}")

print(f"\nHe thong: {'ON DINH' if not results['fail'] else 'CAN SUA'}")
print(f"Thoi gian: {datetime.now().strftime('%H:%M:%S')}")
print("DONE")
