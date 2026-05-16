#!/usr/bin/env python3
"""Set API keys and configure modules"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OPENAI_KEY = "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"
FIRECRAWL_KEY = "fc-ded302299ff34cfe9c09ff862f7786ef"

# Set env for this process
os.environ["OPENAI_API_KEY"] = OPENAI_KEY
os.environ["FIRECRAWL_API_KEY"] = FIRECRAWL_KEY

# Save .env file
env_path = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\.env"
from datetime import datetime
with open(env_path, "w") as f:
    f.write("# Agent API Keys\n")
    f.write("# Set: " + datetime.now().isoformat() + "\n")
    f.write("OPENAI_API_KEY=" + OPENAI_KEY + "\n")
    f.write("FIRECRAWL_API_KEY=" + FIRECRAWL_KEY + "\n")
print("1. Keys saved to .env")

# Test OpenAI
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    models = client.models.list()
    print("2. OpenAI API: OK (" + str(len(list(models))) + " models available)")
except Exception as e:
    print("2. OpenAI API: ERROR - " + str(e)[:80])

# Test mem0 with key
try:
    os.environ["OPENAI_API_KEY"] = OPENAI_KEY
    from mem0 import Memory
    config = {
        "version": "v1.1",
        "llm": {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
        "embedder": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
        "vector_store": {
            "provider": "qdrant",
            "config": {"on_disk": True, "path": os.path.join(os.path.dirname(env_path), "agent-memory")}
        },
    }
    memory = Memory.from_config(config)
    r = memory.add("Test memory entry", user_id="test", session_id="setup")
    m = memory.get_all(user_id="test")
    print("3. mem0 Full: OK (" + str(len(m)) + " memories stored)")
except Exception as e:
    print("3. mem0 Full: FALLBACK (" + str(e)[:100] + ")")

# Test FireCrawl
try:
    from firecrawl import FirecrawlApp
    fc = FirecrawlApp(api_key=FIRECRAWL_KEY)
    r = fc.search(query="test", params={"count": 1})
    print("4. FireCrawl: OK")
except Exception as e:
    print("4. FireCrawl: ERROR - " + str(e)[:100])

# Reload modules
sys.path.insert(0, r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")

# Re-import memory module
import importlib
import agent_memory
importlib.reload(agent_memory)
print("5. agent_memory: mem0=" + ("YES" if agent_memory.MEM0_AVAILABLE else "NO"))

import agent_search
importlib.reload(agent_search)
print("6. agent_search: FireCrawl=" + ("YES" if agent_search.FIRECRAWL_AVAILABLE else "NO"))

print()
print("All configured. Ready.")
