#!/usr/bin/env python
"""MCP Memory Server — port 9877"""
import os, sys, json
BASE = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
sys.path.insert(0, BASE)

# Simple JSON file memory (no qdrant dependency)
MEMORY_DIR = os.path.join(BASE, "agent-memory")
os.makedirs(MEMORY_DIR, exist_ok=True)
from datetime import datetime

def _store(user_id: str, session_id: str, content: str):
    fpath = os.path.join(MEMORY_DIR, f"{user_id}.json")
    entries = []
    if os.path.exists(fpath):
        with open(fpath, encoding="utf-8") as f:
            entries = json.load(f)
    entries.append({
        "content": content,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    })
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    return {"stored": True, "total": len(entries)}

def _search(user_id: str, query: str, limit: int = 5):
    fpath = os.path.join(MEMORY_DIR, f"{user_id}.json")
    if not os.path.exists(fpath):
        return {"results": []}
    with open(fpath, encoding="utf-8") as f:
        entries = json.load(f)
    q = query.lower()
    matches = [e for e in entries if q in e["content"].lower()]
    return {"results": matches[:limit], "total": len(matches)}

from fastmcp import FastMCP
import asyncio

mcp = FastMCP("Memory Server")

@mcp.tool()
def store(user_id: str, session_id: str, content: str):
    """Store a memory entry"""
    return _store(user_id, session_id, content)

@mcp.tool()
def search(user_id: str, query: str, limit: int = 5):
    """Search stored memories by text"""
    return _search(user_id, query, limit)

@mcp.tool()
def list_all(user_id: str):
    """Get all memories for a user"""
    fpath = os.path.join(MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(fpath):
        with open(fpath, encoding="utf-8") as f:
            return json.load(f)
    return []

asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9877))
