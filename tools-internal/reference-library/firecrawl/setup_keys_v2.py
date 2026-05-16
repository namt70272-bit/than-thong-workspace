#!/usr/bin/env python3
"""Re-run setup with keys"""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OPENAI_KEY = "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"
FIRECRAWL_KEY = "fc-ded302299ff34cfe9c09ff862f7786ef"

os.environ["OPENAI_API_KEY"] = OPENAI_KEY
os.environ["FIRECRAWL_API_KEY"] = FIRECRAWL_KEY

# Save .env
env_path = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\.env"
with open(env_path, "w") as f:
    f.write("OPENAI_API_KEY=" + OPENAI_KEY + "\n")
    f.write("FIRECRAWL_API_KEY=" + FIRECRAWL_KEY + "\n")
print("1. Keys saved to .env")

# Test OpenAI API call
import openai
client = openai.OpenAI(api_key=OPENAI_KEY)
models = list(client.models.list())
print("2. OpenAI API: OK (" + str(len(models)) + " models)")

# Test FireCrawl
try:
    from firecrawl import FirecrawlApp
    fc = FirecrawlApp(api_key=FIRECRAWL_KEY)
    r = fc.search(query="OpenClaw AI agent", params={"count": 2})
    results = r.get("results") or r.get("data") or []
    print("3. FireCrawl: OK (" + str(len(results)) + " results)")
except Exception as e:
    print("3. FireCrawl: ERROR - " + str(type(e).__name__) + ": " + str(e)[:100])

# Test mem0 with OpenAI key (skip qdrant, use simple config)
try:
    from mem0 import Memory
    config = {
        "version": "v1.1",
        "llm": {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
        "embedder": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
        "vector_store": {
            "provider": "qdrant",
            "config": {"on_disk": True, "path": r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\agent-memory"}
        },
    }
    memory = Memory.from_config(config)
    r = memory.add("Test memory", user_id="setup", session_id="init")
    all_m = memory.get_all(user_id="setup")
    print("4. mem0 Full: OK (" + str(len(all_m)) + " memories)")
except Exception as e:
    print("4. mem0 Full: " + str(type(e).__name__) + " - fallback to JSON")
    # Simple JSON fallback test
    mem_dir = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\agent-memory"
    os.makedirs(mem_dir, exist_ok=True)
    fpath = os.path.join(mem_dir, "setup.json")
    with open(fpath, "w") as f:
        json.dump([{"content": "Test memory", "timestamp": "now"}], f)
    print("   JSON fallback: OK")

# Final: update agent modules
sys.path.insert(0, r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")

# Reload memory module to pick up key
import importlib, agent_memory, agent_search
importlib.reload(agent_memory)
importlib.reload(agent_search)
print("5. agent_memory: mem0=" + ("YES" if agent_memory.MEM0_AVAILABLE else "NO(fallback)"))
print("6. agent_search: FireCrawl=" + ("YES" if agent_search.FIRECRAWL_AVAILABLE else "NO(fallback)"))

print("\nDone.")
