#!/usr/bin/env python3
"""Test MCP Server on port 9877"""
import httpx, time, subprocess, sys, os

# Free port 9876 first
os.system("netstat -ano | findstr :9876 | findstr LISTEN")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 9876))
sock.close()
if result == 0:
    print("Port 9876 in use, freeing...")
    os.system("for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :9876 ^| findstr LISTEN') do taskkill /f /pid %a 2>nul")

time.sleep(1)

# Start server 
TOOLS = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
os.chdir(TOOLS)
proc = subprocess.Popen(
    ["python", "agent_mcp_server.py"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    cwd=TOOLS
)
time.sleep(4)

print("=== TEST 3: MCP SERVER ===")

try:
    # List tools
    r = httpx.post("http://127.0.0.1:9876/mcp", json={
        "jsonrpc": "2.0", "id": 1, "method": "tools/list"
    }, headers={"Accept": "application/json,text/event-stream"}, timeout=10)
    data = r.json()
    tools = data.get("result", {}).get("tools", [])
    print(f"Tools: {len(tools)}")
    for t in tools[:6]:
        print(f"  - {t['name']}")

    # Test system_status
    r2 = httpx.post("http://127.0.0.1:9876/mcp", json={
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "system_status", "arguments": {}}
    }, headers={"Accept": "application/json,text/event-stream"}, timeout=10)
    d2 = r2.json()
    content = d2.get("result", {}).get("content", [])
    first = content[0] if content else {}
    text = first.get("text", "")
    print(f"system_status: {text[:100]}")
    
    # Test list_skills
    r3 = httpx.post("http://127.0.0.1:9876/mcp", json={
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "list_skills", "arguments": {}}
    }, headers={"Accept": "application/json,text/event-stream"}, timeout=10)
    d3 = r3.json()
    c3 = d3.get("result", {}).get("content", [{}])
    t3 = c3[0].get("text", "")
    skills_count = t3.count('"') // 4  # rough count
    print(f"list_skills: {t3[:80]}...")

    print("MCP Server: OK")

except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:100]}")
finally:
    proc.kill()
    print("Server stopped.")
