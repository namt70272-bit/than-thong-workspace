#!/usr/bin/env python
"""MCP Client — connects to MCP servers via SSE"""
import httpx, json, asyncio, re

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session_id = None
        self.client = httpx.Client(timeout=30)
    
    def initialize(self):
        """Initialize session with MCP server"""
        r = self.client.post(f"{self.base_url}/mcp", json={
            "jsonrpc": "2.0", "id": "init-1", "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "openclaw-agent", "version": "1.0"}
            }
        }, headers={"Accept": "application/json,text/event-stream"})
        return r.json()
    
    def list_tools(self):
        r = self.client.post(f"{self.base_url}/mcp", json={
            "jsonrpc": "2.0", "id": "list-1", "method": "tools/list"
        }, headers={"Accept": "application/json,text/event-stream"})
        return r.json()
    
    def call_tool(self, name: str, args: dict = None):
        r = self.client.post(f"{self.base_url}/mcp", json={
            "jsonrpc": "2.0", "id": "call-1", "method": "tools/call",
            "params": {"name": name, "arguments": args or {}}
        }, headers={"Accept": "application/json,text/event-stream"})
        return r.json()

# Test all servers
servers = {
    "System": "http://127.0.0.1:9876",
    "Memory": "http://127.0.0.1:9877", 
    "Search": "http://127.0.0.1:9878",
    "LLM": "http://127.0.0.1:9879",
}

for name, url in servers.items():
    try:
        client = MCPClient(url)
        init = client.initialize()
        tools = client.list_tools()
        tool_list = tools.get("result", {}).get("tools", [])
        print(f"{name:8s} ({url:22s}): {len(tool_list)} tools | init: {init.get('result',{}).get('protocolVersion','?')}")
        if tool_list:
            for t in tool_list[:3]:
                print(f"          - {t['name']}")
    except Exception as e:
        print(f"{name:8s} ({url:22s}): {type(e).__name__}")
