#!/usr/bin/env python
"""
FastMCP Server + Agent Integration
Agent co the goi tools qua MCP protocol
Chay: python agent_mcp_server.py
"""

try:
    from fastmcp import FastMCP
except ImportError:
    print("pip install fastmcp first")
    import sys; sys.exit(1)

import json, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from datetime import datetime

# Load .env at startup
_env_loaded = False
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                if _k.strip() and _v.strip() and _k not in os.environ:
                    os.environ[_k.strip()] = _v.strip()
                    _env_loaded = True

import os
os.environ.setdefault("FASTMCP_PORT", "9876")
mcp = FastMCP("OpenClaw Agent Tools")

# ===== TOOLS =====

@mcp.tool()
def list_tools():
    """List available tools in tools-internal"""
    tools_dir = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
    scripts_dir = os.path.join(tools_dir, "scripts")
    extracted_dir = os.path.join(tools_dir, "extracted-scripts")
    
    result = {"scripts": [], "extracted_groups": {}}
    
    for f in sorted(os.listdir(scripts_dir)):
        if f.endswith('.py'):
            sz = os.path.getsize(os.path.join(scripts_dir, f)) // 1024
            result["scripts"].append({"name": f, "size_kb": sz})
    
    if os.path.exists(extracted_dir):
        for d in sorted(os.listdir(extracted_dir)):
            dd = os.path.join(extracted_dir, d)
            if os.path.isdir(dd):
                files = [f for f in os.listdir(dd) if f.endswith('.py')]
                result["extracted_groups"][d] = len(files)
    
    return result

@mcp.tool()
def read_skill(name: str):
    """Read a skill's SKILL.md content by skill name"""
    skills_dir = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills"
    skill_path = os.path.join(skills_dir, name, "SKILL.md")
    if os.path.exists(skill_path):
        with open(skill_path, encoding='utf-8') as f:
            return f.read()
    # Try case-insensitive
    for d in os.listdir(skills_dir):
        if d.lower() == name.lower():
            sp = os.path.join(skills_dir, d, "SKILL.md")
            if os.path.exists(sp):
                with open(sp, encoding='utf-8') as f:
                    return f.read()
    return {"error": f"Skill '{name}' not found"}

@mcp.tool()
def run_script(script_name: str, args: str = ""):
    """Run a script from tools-internal/scripts/ and return output"""
    scripts_dir = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\scripts"
    fp = os.path.join(scripts_dir, script_name)
    if not os.path.exists(fp):
        return {"error": f"Script '{script_name}' not found"}
    try:
        result = subprocess.run(
            ["python", fp, *args.split()],
            capture_output=True, text=True, timeout=30
        )
        return {"stdout": result.stdout[:5000], "stderr": result.stderr[:2000], "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Script timed out"}

@mcp.tool()
def list_skills():
    """List all available skills in the system"""
    skills_dir = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills"
    skills = sorted([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])
    return {"skills": skills, "count": len(skills)}

@mcp.tool()
def memory_store(user_id: str, session_id: str, content: str):
    """Store a memory for an agent user"""
    sys.path.insert(0, os.path.dirname(__file__))
    from agent_memory import add_memory
    return add_memory(user_id, session_id, content)

@mcp.tool()
def memory_search(user_id: str, query: str, limit: int = 5):
    """Search stored memories by relevance"""
    sys.path.insert(0, os.path.dirname(__file__))
    from agent_memory import search_memory
    return search_memory(user_id, query, limit)

@mcp.tool()
def web_search(query: str, limit: int = 5):
    """Search the web for information"""
    sys.path.insert(0, os.path.dirname(__file__))
    from agent_search import web_search as ws
    return ws(query, limit)

@mcp.tool()
def fetch_page(url: str):
    """Fetch a web page and return its text content"""
    sys.path.insert(0, os.path.dirname(__file__))
    from agent_search import fetch_url
    return fetch_url(url)

@mcp.tool()
def system_status():
    """Get current system status information"""
    return {
        "time": datetime.now().isoformat(),
        "python": sys.version,
        "platform": sys.platform,
    }

@mcp.tool()
def search_tools(query: str):
    """Search scripts in tools-internal by keyword"""
    tools_dir = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
    results = []
    for root, dirs, files in os.walk(tools_dir):
        for f in files:
            if not f.endswith('.py'): continue
            if query.lower() in f.lower():
                rel = os.path.relpath(os.path.join(root, f), tools_dir)
                sz = os.path.getsize(os.path.join(root, f)) // 1024
                results.append({"path": rel, "size_kb": sz})
    return {"query": query, "results": results[:20], "total": len(results)}

if __name__ == "__main__":
    import asyncio
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("Starting FastMCP Agent Tools Server (port 9876)")
    print("Tools: list_tools, read_skill, run_script, list_skills, system_status, search_tools, memory_store, memory_search, web_search, fetch_page")
    print("Connect: any MCP client -> http://localhost:9876/mcp")
    asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9876))
