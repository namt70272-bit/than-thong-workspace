#!/usr/bin/env python
"""mem0 + Ollama local - final test"""
import os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ['OPENAI_API_KEY'] = ''
os.environ['FIRECRAWL_API_KEY'] = 'fc-ded302299ff34cfe9c09ff862f7786ef'

fresh = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\agent-memory-v2'
if os.path.exists(fresh): shutil.rmtree(fresh)

print("Initializing mem0 + Ollama + HuggingFace...")
sys.stdout.flush()

from mem0 import Memory
config = {
    'version': 'v1.1',
    'llm': {
        'provider': 'ollama',
        'config': {'model': 'qwen2.5-coder:7b', 'ollama_base_url': 'http://localhost:11434'}
    },
    'embedder': {
        'provider': 'huggingface',
        'config': {'model': 'sentence-transformers/all-MiniLM-L6-v2'}
    },
    'vector_store': {
        'provider': 'qdrant',
        'config': {'on_disk': True, 'path': fresh}
    },
}

mem = Memory.from_config(config)
print("Init OK. Storing memories...")
sys.stdout.flush()

mem.add("Hom nay nang cap he thong FastMCP FireCrawl mem0", user_id="chu_nhan")
mem.add("Dung Ollama qwen2.5-coder lam LLM local hoan toan", user_id="chu_nhan")
mem.add("25 skills moi 3300 scripts MCP server port 9876", user_id="chu_nhan")

all_mem = mem.get_all(user_id="chu_nhan")
print("Stored: " + str(len(all_mem)) + " memories")
sys.stdout.flush()

results = mem.search("nang cap he thong", user_id="chu_nhan")
print("Search: " + str(len(results)) + " results")
for r in results[:3]:
    score = r.get("score", 0)
    mem_text = r.get("memory", "")[:60]
    print("  [" + f"{score:.3f}" + "] " + mem_text)

print()
print("MEM0 + OLLAMA FULL MODE: OK (khong can OpenAI!)")
