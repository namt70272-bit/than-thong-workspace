#!/usr/bin/env python
"""Full system audit — what thần thông CAN and CANNOT do"""
import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
E = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
T = Path(str(E) + "/tools-internal")
SCR = Path(str(T) + "/scripts")

print("=" * 70)
print("THAN THONG — FULL CAPABILITY REPORT")
print("=" * 70)

# === 1. THAN THONG SCRIPTS ===
scripts_dir = os.path.join(str(T), "scripts")
console_cmds = [
    ("preflight", "preflight_runner.py", "Check gate + route before ops"),
    ("inventory", "workspace_inventory.py", "Index workspace files"),
    ("domains", "index_domains.py", "Index workspace domains"),
    ("junk", "find_junk.py", "Find junk files"),
    ("duplicate", "duplicate_checker.py", "Scan duplicate files"),
    ("canonical", "canonical_checker.py", "Check single source of truth"),
    ("track", "domain_tracker.py", "Track 16 domain progress"),
    ("drift", "drift_checker.py", "Check candidate vs workspace drift"),
    ("waves", "wave_manager.py", "Manage import waves"),
    ("dashboard", "ops_dashboard.py", "System dashboard"),
    ("scan-G", "top_scan_G_source.py", "Scan G:\\Ai source zips"),
    ("daily", "than_thong_daily.py", "Daily maintenance"),
    ("win-audit", "top_win_audit.py", "Windows audit"),
    ("win-cleanup", "top_win_cleanup.py", "Windows cleanup"),
    ("win-process", "top_win_process_audit.py", "Process monitoring"),
    ("win-data", "top_win_data_map.py", "Windows data mapping"),
    ("win-dashboard", "top_win_dashboard.py", "Windows dashboard"),
    ("win-env", "top_win_env_audit.py", "Environment variables"),
    ("win-svc", "top_win_svc_audit.py", "Windows services"),
    ("win-startup", "top_win_startup_audit.py", "Startup programs"),
    ("win-disk", "top_win_disk_health.py", "Disk health"),
    ("win-restore", "top_win_system_restore.py", "System restore points"),
    ("win-tighten", "top_win_tighten.py", "Security recommendations"),
    ("win-full", "top_win_full_dashboard.py", "Full Windows dashboard"),
]
print(f"\n1. THAN THONG CONSOLE: {len(console_cmds)} commands")
for cmd, script, desc in console_cmds:
    status = "OK" if os.path.exists(os.path.join(scripts_dir, script)) else "MISSING"
    print(f"   [{status}] {cmd:15s} → {desc}")

# === 2. MCP ECOSYSTEM ===
mcp_servers = [
    ("System", 9876, "agent_mcp_server.py", "System/skills/scripts tools"),
    ("Memory", 9877, "mcp_memory_server.py", "JSON memory store"),
    ("Search", 9878, "mcp_search_server.py", "Web search + fetch"),
    ("LLM", 9879, "mcp_llm_server.py", "Ollama local LLM"),
    ("Gateway", 9001, "api_gateway.py", "Unified API endpoint"),
]
print(f"\n2. MCP ECOSYSTEM: {len(mcp_servers)} servers")
for name, port, script, desc in mcp_servers:
    exists = "OK" if os.path.exists(os.path.join(str(T), script)) else "MISSING"
    online = subprocess.run(["python", "-c", f"import socket; s=socket.socket(); s.settimeout(2); print(s.connect_ex(('127.0.0.1',{port})))"], capture_output=True, text=True, timeout=5).stdout.strip()
    status = "ONLINE" if online == "0" else "OFFLINE"
    print(f"   [{status}] {name:8s} :{port} → {desc} ({exists})")

# === 3. INSTALLED PACKAGES ===
print(f"\n3. PYTHON PACKAGES (Python 3.11)")
r = subprocess.run(["python", "-m", "pip", "list", "--format=columns"], capture_output=True, text=True, timeout=10)
lines = r.stdout.strip().split("\n")[2:]  # skip headers
pkgs = {}
for line in lines:
    parts = line.split()
    if len(parts) >= 2:
        pkgs[parts[0]] = parts[1]

key_pkgs = ["fastmcp", "mem0ai", "firecrawl-py", "fastapi", "uvicorn", "ollama", "openai", "httpx", "pydantic", "qdrant-client", "sentence-transformers", "sqlalchemy"]
for p in key_pkgs:
    ver = pkgs.get(p, "NOT INSTALLED")
    print(f"   {p:25s} v{ver}")

# === 4. SKILLS ===
skills_dir = os.path.join(str(E), "skills")
skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
print(f"\n4. SKILLS: {len(skills)} total")
from collections import Counter
skill_origins = Counter()
for s in skills:
    reg = os.path.join(skills_dir, s, "SKILL.md")
    if os.path.exists(reg):
        skill_origins["has_skill_md"] += 1
    else:
        skill_origins["no_skill_md"] += 1
print(f"   Has SKILL.md: {skill_origins['has_skill_md']}")
print(f"   No SKILL.md:  {skill_origins['no_skill_md']}")

# === 5. CAN DO ===
print(f"\n{'=' * 70}")
print("THAN THONG CO THE LAM:")
print(f"{'=' * 70}")
can_do = [
    ("QUAN LY WORKSPACE", [
        "Quet va index toan bo workspace (inventory)",
        "Phat hien file trung lap (duplicate)",
        "Kiem tra nguon su that (canonical)",
        "Phat hien lech candidate vs workspace (drift)",
        "Quan ly 16 mang cong viec (domain tracker)",
        "Quan ly wave nhap du lieu (wave manager)",
        "Kiem tra xung dot file candidate (import validator)",
        "Phan tich sau candidate (deep validator)",
        "Dong bo file candidate (sync executor)",
        "Rollback import (rollback manifest + real rollback)",
    ]),
    ("QUAN LY WINDOWS", [
        "Kiem tra suc khoe o dia (disk health)",
        "Quet moi truong Windows (env audit)",
        "Kiem tra services (service audit)",
        "Kiem tra startup programs",
        "Giam sat process (process audit)",
        "Don dep temp/junk (cleanup)",
        "Xem diem khoi phuc (system restore)",
        "Goi y siet chat bao mat (tighten)",
        "Full dashboard Windows (full dashboard)",
        "Ban do du lieu o dia (data map)",
    ]),
    ("MCP ECOSYSTEM", [
        "Goi tools qua MCP protocol (FastMCP 3.2.4)",
        "4 MCP server chuyen biet: System, Memory, Search, LLM",
        "API Gateway thong nhat port 9001",
        "Dinh tuyen thong minh (unified routing)",
        "Search web that (FireCrawl API)",
        "Chat voi LLM local (Ollama qwen2.5-coder:7b)",
        "Luu tru ky uc (JSON memory store)",
        "Doc/ghep skill SKILL.md",
        "Goi script tools-internal truc tiep",
    ]),
    ("AI & ML", [
        "Chat voi LLM local (Ollama, 4.7GB model)",
        "Search web (FireCrawl, 10 ket qua/query)",
        "AI memory (mem0 JSON fallback)",
        "128 OpenAI models (het quota)",
        "HuggingFace local embedding (all-MiniLM-L6-v2)",
        "LangChain/LangGraph scripts tham khao (120 file)",
    ]),
    ("DATA & SCRIPTS", [
        "2.434 file tham khao trong 21 category",
        "Finance/Quant scripts (98 file)",
        "Spark data processing scripts (727 file)",
        "Web scraping tools (118 file)",
        "FastAPI server scripts (29 file)",
        "Data sources API clients (17 file)",
    ]),
    ("CON SO", [
        "Skills: 56",
        "Scripts tham khao: 2.434",
        "Console commands: 24",
        "MCP servers: 5",
        "Python packages cai dat: 150+",
        "API keys cau hinh: 2 (OpenAI, FireCrawl)",
    ]),
]

for title, items in can_do:
    print(f"\n  🔹 {title}")
    for item in items:
        print(f"     ✅ {item}")

# === 6. CANNOT DO ===
print(f"\n{'=' * 70}")
print("THAN THONG KHONG THE LAM (hoac can them de lam):")
print(f"{'=' * 70}")
cannot_do = [
    ("THIEU DEPENDENCY", [
        "mem0 vector search full mode → can OpenAI co quota hoac fix qdrant+msvcrt",
        "FireCrawl search full mode → can `docket` package (chua co cho Python 3.14)",
        "MCP tool listing → FastMCP 3.x SSE protocol khong tuong thich HTTP POST",
        "Preflight runner → da fix nhung van phu thuoc python3 (3.14)",
        "Deep validator timeout → file qua nhieu, da fix limit 500",
    ]),
    ("CHUA CO TICH HOP", [
        "Tu dong khoi dong MCP servers khi reboot → can Windows service",
        "RAG pipeline (doc→chunk→embed→search) → can LangChain + vector store",
        "Multi-agent orchestration → can nhieu MCP agent phoi hop",
        "Vault/secret management → API keys trong .env plaintext",
        "Unit tests cho than thong scripts → 0% coverage",
        "CI/CD pipeline → khong co",
        "Web UI dashboard → chi co CLI",
        "Remote access → chi localhost",
    ]),
    ("GIOI HAN KY THUAT", [
        "Python 3.14 (python3) thieu package support (docket, grpcio wheel)",
        "Python 3.13 Windows Store thieu msvcrt module",
        "Chi Python 3.11 (python) chay duoc full packages",
        "3300 file extracted scripts time to organize nhung khong the xoa",
        "Hardcoded paths trong 20+ scripts (da fix 1 so)",
        "Shadow file van co the tai phat sinh khi extract zip moi",
        "Khong co permission/role system",
        "Khong co logging centralized",
    ]),
    ("TINH NANG CHUA XAY", [
        "Auto-sync G:\\Ai -> E workspace",
        "Smart diff giua candidate vs production",
        "Agent co the tu build skill moi tu scripts tham khao",
        "Web search history + cache",
        "Memory consolidation tu nhieu session",
        "Multi-modal (image/audio processing)",
        "API rate limiting cho MCP services",
        "Service discovery cho MCP ecosystem",
    ]),
]

for title, items in cannot_do:
    print(f"\n  ❌ {title}")
    for item in items:
        print(f"     ⚠️  {item}")

# === 7. SUMMARY ===
print(f"\n{'=' * 70}")
print("TONG QUAN")
print(f"{'=' * 70}")
print("""
THAN THONG MANH:
- Quan ly workspace day du (quét, so sanh, validate, rollback)
- Quan ly Windows toan dien (audit, cleanup, security)
- MCP ecosystem 5 server + API gateway
- Chat voi LLM local + search web + memory
- 2.434 file tham khao + 56 skills + 24 console commands

THAN THONG YEU:
- Phu thuoc Python 3.11 cho package day du
- Chua co auto-start, CI/CD, web UI
- Chua co RAG pipeline, multi-agent
- Mot so script chet do dependency

DE XUAT: 
- Dung Python 3.11 (python) cho MCP servers
- Python 3.14 (python3) cho thần thông tools nhe
- Tranh extract file vao tools-internal/ (da reference-library)
""")
