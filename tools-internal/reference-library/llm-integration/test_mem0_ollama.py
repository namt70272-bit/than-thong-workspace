#!/usr/bin/env python
"""Test mem0 with Ollama local LLM + HuggingFace local embedding"""
import os
os.environ['OPENAI_API_KEY'] = ''  # not needed
os.environ['FIRECRAWL_API_KEY'] = 'fc-ded302299ff34cfe9c09ff862f7786ef'

# Start Ollama if not running
import subprocess
try:
    subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
except:
    print("Starting Ollama...")
    subprocess.Popen(["ollama", "serve"], shell=True)
    import time; time.sleep(3)

from mem0 import Memory
config = {
    'version': 'v1.1',
    'llm': {
        'provider': 'ollama',
        'config': {
            'model': 'qwen2.5-coder:7b',
            'ollama_base_url': 'http://localhost:11434',
        }
    },
    'embedder': {
        'provider': 'huggingface',
        'config': {'model': 'sentence-transformers/all-MiniLM-L6-v2'}
    },
    'vector_store': {
        'provider': 'qdrant',
        'config': {
            'on_disk': True,
            'path': 'E:/KY-DATA/OpenClaw/runtime-mirror/.openclaw/workspace/tools-internal/agent-memory'
        }
    },
}

print("Initializing mem0 with Ollama + HuggingFace...")
mem = Memory.from_config(config)

mem.add("Hom nay da nang cap he thong voi FastMCP, FireCrawl, mem0", user_id="chu_nhan")
mem.add("Dang dung Ollama qwen2.5-coder lam LLM local, khong can OpenAI", user_id="chu_nhan")
mem.add("Co 25 skills moi, 3300 scripts, MCP server port 9876", user_id="chu_nhan")

all_m = mem.get_all(user_id="chu_nhan")
print(f"Stored: {len(all_m)} memories")

results = mem.search("nang cap he thong", user_id="chu_nhan")
print(f"Search: {len(results)} results")
for r in results[:3]:
    score = r.get("score", 0)
    mem_text = r.get("memory", "")[:70]
    print(f"  [{score:.3f}] {mem_text}")

print("\nMEM0 FULL MODE: OK (khong can OpenAI quota!)")
