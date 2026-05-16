#!/usr/bin/env python
"""Test mem0 with local HuggingFace embedding"""
import os
os.environ['OPENAI_API_KEY'] = ''
os.environ['FIRECRAWL_API_KEY'] = 'fc-ded302299ff34cfe9c09ff862f7786ef'

from mem0 import Memory
config = {
    'version': 'v1.1',
    'llm': {'provider': 'openai', 'config': {'model': 'gpt-4o-mini'}},
    'embedder': {'provider': 'huggingface', 'config': {'model': 'sentence-transformers/all-MiniLM-L6-v2'}},
    'vector_store': {
        'provider': 'qdrant',
        'config': {'on_disk': True, 'path': 'E:/KY-DATA/OpenClaw/runtime-mirror/.openclaw/workspace/tools-internal/agent-memory'}
    },
}

print("Initializing mem0 with local embedding...")
mem = Memory.from_config(config)

mem.add("Hom nay toi da nang cap he thong voi FastMCP va FireCrawl", user_id="chu_nhan")
mem.add("API key OpenAI da het quota, dang dung local embedding", user_id="chu_nhan")

all_m = mem.get_all(user_id="chu_nhan")
print(f"mem0: {len(all_m)} memories stored")

results = mem.search("nang cap he thong", user_id="chu_nhan")
print(f"Search: {len(results)} results")
for r in results[:2]:
    score = r.get("score", 0)
    mem_text = r.get("memory", "")[:60]
    print(f"  Score: {score:.3f} | {mem_text}")

print("\nMEM0 HOAT DONG KHONG CAN OPENAI QUOTA!")
