#!/usr/bin/env python3.13
"""Test Python 3.13 compatibility"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ['OPENAI_API_KEY'] = "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"
os.environ['FIRECRAWL_API_KEY'] = "fc-ded302299ff34cfe9c09ff862f7786ef"

print("1. fastmcp:", end=" ")
import fastmcp
print(fastmcp.__version__)

print("2. FireCrawl:", end=" ")
from firecrawl import FirecrawlApp
fc = FirecrawlApp()
r = fc.search("OpenClaw AI")
print("OK")
for item in (r.data or [])[:2]:
    print(f"   - {item.title}: {getattr(item, 'url', 'N/A')}")

print("3. mem0:", end=" ")
from mem0 import Memory
config = {
    "version": "v1.1",
    "llm": {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
    "embedder": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
}
mem = Memory.from_config(config)
mem.add("Hello from Python 3.13", user_id="test", session_id="init")
all_m = mem.get_all(user_id="test")
print(f"OK ({len(all_m)} memories)")

print("4. MCP server:", end=" ")
compile(open("E:/KY-DATA/OpenClaw/runtime-mirror/.openclaw/workspace/tools-internal/agent_mcp_server.py", "rb").read(), "mcp", "exec")
print("OK")

print("\nAll tests PASSED on Python 3.13")
