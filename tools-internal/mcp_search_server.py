#!/usr/bin/env python
"""MCP Search Server — port 9878"""
import os, sys
sys.path.insert(0, r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
os.environ["FIRECRAWL_API_KEY"] = "fc-ded302299ff34cfe9c09ff862f7786ef"

# Import directly from tools-internal root
import importlib.util
spec = importlib.util.spec_from_file_location(
    "agent_search",
    r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\reference-library\firecrawl\agent_search.py"
)
agent_search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_search)
web_search = agent_search.web_search
fetch_url = agent_search.fetch_url

from fastmcp import FastMCP
import asyncio

mcp = FastMCP("Search Server")

@mcp.tool()
def search(query: str, limit: int = 5):
    """Search the web for information"""
    return web_search(query, limit)

@mcp.tool()
def fetch(url: str):
    """Fetch a web page content"""
    return fetch_url(url)

asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9878))
