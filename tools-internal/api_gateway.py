#!/usr/bin/env python
"""
API Gateway — Unified entry point for MCP ecosystem
Port 9001. Routes: /system, /memory, /search, /llm
Also provides: /unified (orchestrate across all servers)
"""
import os, sys, json, httpx, asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="OpenClaw MCP Gateway", version="2.0.0")

SERVERS = {
    "rag": "http://127.0.0.1:9880/mcp",
    "system": "http://127.0.0.1:9876/mcp",
    "memory": "http://127.0.0.1:9877/mcp",
    "search": "http://127.0.0.1:9878/mcp",
    "llm": "http://127.0.0.1:9879/mcp",
}

async def call_mcp(url: str, method: str, params: dict = None):
    """Call an MCP server tool"""
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json={
            "jsonrpc": "2.0", "id": "gw-1", "method": method,
            "params": params or {}
        }, headers={"Accept": "application/json,text/event-stream"})
        return r.json()

@app.get("/")
async def root():
    return {
        "name": "OpenClaw MCP Gateway",
        "version": "2.0",
        "servers": list(SERVERS.keys()),
        "endpoints": {
            "GET /health": "Health check",
            "GET /servers": "List servers + tools",
            "POST /{server}/{tool}": "Call tool on specific server",
            "POST /unified": "Intelligent routing across all servers"
        }
    }

@app.get("/health")
async def health():
    results = {}
    for name, url in SERVERS.items():
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.post(url, json={
                    "jsonrpc": "2.0", "id": "ping", "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name":"gw","version":"1"}}
                }, headers={"Accept": "application/json,text/event-stream"})
                results[name] = {"status": "up", "port": url.split(":")[2].split("/")[0]}
        except:
            results[name] = {"status": "down"}
    
    return {"gateway": "healthy", "servers": results}

@app.get("/servers")
async def list_servers():
    """List all servers and their tools"""
    results = {}
    for name, url in SERVERS.items():
        try:
            data = await call_mcp(url, "tools/list")
            tools = data.get("result", {}).get("tools", [])
            results[name] = {
                "tools": [t["name"] for t in tools],
                "count": len(tools)
            }
        except Exception as e:
            results[name] = {"error": str(e)[:50]}
    return results

@app.post("/{server}/{tool}")
async def call_tool(server: str, tool: str, request: Request):
    """Call a tool on a specific MCP server"""
    if server not in SERVERS:
        return JSONResponse({"error": f"Unknown server: {server}"}, status_code=404)
    
    body = await request.json() if request.headers.get("content-type") else {}
    data = await call_mcp(SERVERS[server], "tools/call", {
        "name": tool, "arguments": body
    })
    content = data.get("result", {}).get("content", [])
    text = " ".join(c.get("text", "") for c in content) if content else str(data)
    return {"server": server, "tool": tool, "result": text[:2000]}

@app.post("/unified")
async def unified(request: Request):
    """Intelligent routing: auto-route query to the right server"""
    body = await request.json()
    query = body.get("query", "").lower()
    
    # Route intelligence
    if any(w in query for w in ["search", "find", "crawl", "fetch", "web", "google", "lookup"]):
        server, tool = "search", "search"
        params = {"query": body.get("query", ""), "limit": body.get("limit", 5)}
    elif any(w in query for w in ["remember", "store", "save", "memory", "forget"]):
        server, tool = "memory", "store"
        params = {"user_id": body.get("user_id", "default"), "session_id": body.get("session_id", "main"), "content": body.get("content", query)}
    elif any(w in query for w in ["recall", "search memory", "what did"]) or body.get("action") == "search_memory":
        server, tool = "memory", "search"
        params = {"user_id": body.get("user_id", "default"), "query": body.get("query", query), "limit": body.get("limit", 5)}
    elif any(w in query for w in ["chat", "ask", "talk", "generate", "write", "explain", "tell"]):
        server, tool = "llm", "chat"
        params = {"prompt": body.get("query", query)}
    elif any(w in query for w in ["knowledge", "rag", "document", "docs", "find", "search in", "look up", "what is", "explain"]):
        server, tool = "rag", "search"
        params = {"query": body.get("query", query), "top_k": body.get("limit", 5)}
    elif any(w in query for w in ["skill", "tool", "script", "system", "status"]):
        server, tool = "system", "list_tools"
        params = {}
    else:
        server, tool = "system", "system_status"
        params = {}
    
    data = await call_mcp(SERVERS[server], "tools/call", {"name": tool, "arguments": params})
    content = data.get("result", {}).get("content", [])
    text = " ".join(c.get("text", "") for c in content) if content else str(data)
    
    return {
        "routed_to": f"{server}/{tool}",
        "result": text[:2000],
        "servers": {s: {"url": u.split(":")[2].split("/")[0]} for s, u in SERVERS.items()}
    }

@app.post("/rag")
async def rag_search(request: Request):
    """Direct RAG search endpoint (bypasses MCP protocol)"""
    body = await request.json()
    query = body.get("query", "")
    top_k = body.get("top_k", 5)
    
    import importlib.util as ut
    spec = ut.spec_from_file_location("rag_engine", 
        os.path.join(os.path.dirname(__file__), "rag_engine.py"))
    rag = ut.module_from_spec(spec)
    spec.loader.exec_module(rag)  # This loads the model - slow first time
    
    store = rag.LocalVectorStore(os.path.join(os.path.dirname(__file__), "rag-data"))
    qvec = rag.embed([query])[0]
    results = store.search(qvec, top_k=top_k)
    return {"query": query, "results": results, "total": store.count()}

if __name__ == "__main__":
    print("MCP Gateway running on http://127.0.0.1:9001")
    print("Servers: rag(9880) system(9876) memory(9877) search(9878) llm(9879)")
    uvicorn.run(app, host="127.0.0.1", port=9001)
