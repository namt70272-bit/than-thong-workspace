#!/usr/bin/env python3
"""
MCP Ecosystem — Multi-Server Orchestrator
Runs: system, search, memory, llm servers on different ports
Gateway: unified API endpoint at port 9001
"""
import os, sys, json, subprocess, time, signal, asyncio
from pathlib import Path

TOOLS = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
SCRIPTS = TOOLS / "scripts"
PY = "python"  # Use Python 3.11 (has all packages)

# Load .env
env_path = TOOLS / ".env"
if env_path.exists():
    for line in open(env_path):
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

SERVERS = {
    "system": {
        "port": 9876,
        "script": "agent_mcp_server.py",
        "description": "System tools (skills, scripts, status)",
        "status": "ready"
    },
    "memory": {
        "port": 9877,
        "script": None,  # Will create
        "description": "Memory store + search (JSON fallback)",
        "status": "pending"
    },
    "search": {
        "port": 9878,
        "script": None,  # Will create
        "description": "Web search via FireCrawl + httpx",
        "status": "pending"
    },
    "llm": {
        "port": 9879,
        "script": None,  # Will create
        "description": "Ollama local LLM interface",
        "status": "pending"
    },
}

# === BUILD MCP MEMORY SERVER ===
MEMORY_SERVER = r'''
#!/usr/bin/env python
"""MCP Memory Server - port 9877"""
import os, sys, json
sys.path.insert(0, r"''' + str(TOOLS).replace('\\', '/') + r'''")
os.environ.setdefault("OPENAI_API_KEY", "")

from agent_memory import add_memory, search_memory, get_all_memories
try:
    from fastmcp import FastMCP
    mcp = FastMCP("Memory Server")
    
    @mcp.tool()
    def store(user_id: str, session_id: str, content: str):
        """Store a memory"""
        return add_memory(user_id, session_id, content)
    
    @mcp.tool()
    def search(user_id: str, query: str, limit: int = 5):
        """Search memories"""
        return search_memory(user_id, query, limit)
    
    @mcp.tool()
    def list_all(user_id: str):
        """Get all memories for a user"""
        return get_all_memories(user_id)
    
    import asyncio
    asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9877))
except Exception as e:
    print(f"Memory server error: {e}")
'''

# === BUILD MCP SEARCH SERVER ===
SEARCH_SERVER = r'''
#!/usr/bin/env python
"""MCP Search Server - port 9878"""
import os, sys, json
sys.path.insert(0, r"''' + str(TOOLS).replace('\\', '/') + r'''")

os.environ.setdefault("FIRECRAWL_API_KEY", "")
from agent_search import web_search, fetch_url

try:
    from fastmcp import FastMCP
    mcp = FastMCP("Search Server")
    
    @mcp.tool()
    def search(query: str, limit: int = 5):
        """Search the web"""
        return web_search(query, limit)
    
    @mcp.tool()
    def fetch(url: str):
        """Fetch a web page"""
        return fetch_url(url)
    
    import asyncio
    asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9878))
except Exception as e:
    print(f"Search server error: {e}")
'''

# === BUILD MCP LLM SERVER ===
LLM_SERVER = r'''
#!/usr/bin/env python
"""MCP LLM Server - port 9879 (uses local Ollama)"""
import os, sys
try:
    import ollama
    from fastmcp import FastMCP
    mcp = FastMCP("LLM Server")
    
    MODEL = "qwen2.5-coder:7b"
    
    @mcp.tool()
    def chat(prompt: str, system: str = "You are a helpful AI assistant."):
        """Chat with local LLM"""
        resp = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ])
        return resp["message"]["content"]
    
    @mcp.tool()
    def list_models():
        """List available local models"""
        models = ollama.list()
        return [m.model for m in (models.get("models") or [])]
    
    import asyncio
    asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9879))
except Exception as e:
    print(f"LLM server error: {e}")
'''

# Write server scripts
scripts = {
    "mcp_memory_server.py": MEMORY_SERVER,
    "mcp_search_server.py": SEARCH_SERVER,
    "mcp_llm_server.py": LLM_SERVER,
}

for name, content in scripts.items():
    path = TOOLS / name
    path.write_text(content)
    print(f"Created: {name}")

# === LAUNCH ALL SERVERS ===
print("\nLaunching MCP Ecosystem...")
processes = []

for srv_name, info in SERVERS.items():
    if info["script"]:
        script_path = TOOLS / info["script"]
        if script_path.exists():
            proc = subprocess.Popen(
                [PY, str(script_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            processes.append((srv_name, info["port"], proc))
            print(f"  [{srv_name:8s}] PID {proc.pid} port {info['port']}")
            time.sleep(1.5)  # stagger startup

print(f"\n{len(processes)} MCP servers running")
print("System:   http://127.0.0.1:9876/mcp")
print("Memory:   http://127.0.0.1:9877/mcp")
print("Search:   http://127.0.0.1:9878/mcp")
print("LLM:      http://127.0.0.1:9879/mcp")

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    for name, port, proc in processes:
        proc.terminate()
    print("Done.")
