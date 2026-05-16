#!/usr/bin/env python
"""
Service Discovery — MCP ecosystem tự động dò tìm servers
Phát hiện server nào đang chạy, tool gì, trạng thái thế nào
"""
import os, sys, json, httpx, socket, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")

# Known MCP server definitions
MCP_DEFS = {
    "System": {"port": 9876, "script": "agent_mcp_server.py", "desc": "System tools (skills, scripts, status)"},
    "Memory": {"port": 9877, "script": "mcp_memory_server.py", "desc": "JSON memory store"},
    "Search": {"port": 9878, "script": "mcp_search_server.py", "desc": "Web search + fetch"},
    "LLM": {"port": 9879, "script": "mcp_llm_server.py", "desc": "Ollama local LLM"},
    "RAG": {"port": 9880, "script": "mcp_rag_server.py", "desc": "Document search (4,400 chunks)"},
    "Gateway": {"port": 9001, "script": "api_gateway.py", "desc": "Unified API endpoint"},
    "Dashboard": {"port": 8080, "script": "dashboard_web.py", "desc": "Web UI dashboard"},
}

def check_port(port, timeout=2):
    """Check if a port is listening"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex(("127.0.0.1", port))
    sock.close()
    return result == 0

def discover():
    """Discover all running MCP services"""
    results = {}
    for name, info in MCP_DEFS.items():
        online = check_port(info["port"])
        results[name] = {
            "port": info["port"],
            "online": online,
            "status": "UP" if online else "DOWN",
            "script": info["script"],
            "description": info["desc"],
            "url": f"http://127.0.0.1:{info['port']}/mcp" if name != "Gateway" and name != "Dashboard" else f"http://127.0.0.1:{info['port']}"
        }
        
        if online and name not in ("Gateway", "Dashboard"):
            # Try to get tool list
            try:
                r = httpx.post(f"http://127.0.0.1:{info['port']}/mcp", json={
                    "jsonrpc": "2.0", "id": "disc", "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "discovery", "version": "1"}}
                }, headers={"Accept": "application/json,text/event-stream"}, timeout=3)
                results[name]["init_ok"] = r.status_code == 200
            except:
                results[name]["init_ok"] = False
    
    return results

def register():
    """Register discovery results for other services to read"""
    results = discover()
    reg_path = TOOLS / "registry.json"
    reg_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return results

def summary():
    """Print a summary table"""
    results = register()
    
    print("=" * 65)
    print("MCP ECOSYSTEM — SERVICE DISCOVERY")
    print("=" * 65)
    
    online = sum(1 for r in results.values() if r["online"])
    print(f"\n{online}/{len(results)} services online\n")
    
    for name, info in sorted(results.items(), key=lambda x: x[1]["port"]):
        status_icon = "ONLINE" if info["online"] else "OFFLINE"
        print(f"  [{status_icon}] {name:10s} :{info['port']:<5d} {info['description']}")
    
    print()
    
    if results.get("Gateway", {}).get("online"):
        print(f"  Gateway: http://127.0.0.1:9001")
        print(f"  Dashboard: http://127.0.0.1:8080")
    
    return results

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "summary"
    
    if action == "discover":
        results = discover()
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif action == "register":
        register()
        print("Registry written to tools-internal/registry.json")
    elif action == "check":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        if name and name in MCP_DEFS:
            info = MCP_DEFS[name]
            online = check_port(info["port"])
            print(f"{name} on port {info['port']}: {'ONLINE' if online else 'OFFLINE'}")
        else:
            for n, i in MCP_DEFS.items():
                online = check_port(i["port"])
                print(f"  {n:12s} :{i['port']:<5d} {'UP' if online else 'DOWN'}")
    else:
        summary()
