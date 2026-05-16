#!/usr/bin/env python3
"""
Mem0 Memory integration for OpenClaw agent
Local storage (SQLite) - no external server needed
"""
import os, json
from datetime import datetime

MEMORY_DIR = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\agent-memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

try:
    from mem0 import Memory
    # Local-only config: SQLite store, no embedding server needed
    config = {
        "version": "v1.1",
        "graph_store": {"config": {"model": "gpt-4o-mini"}},
        "llm": {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
        "embedder": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
        "vector_store": {
            "provider": "qdrant",
            "config": {"on_disk": True, "path": MEMORY_DIR, "hnsw_config": {"m": 16, "ef_construct": 100}}
        },
    }
    memory = Memory.from_config(config)
    MEM0_AVAILABLE = True
except Exception as e:
    memory = None
    MEM0_AVAILABLE = False
    _init_error = str(e)

def add_memory(user_id: str, session_id: str, content: str):
    """Store a memory entry"""
    if not MEM0_AVAILABLE:
        return _fallback_store(user_id, session_id, content)
    try:
        result = memory.add(content, user_id=user_id, session_id=session_id)
        return {"status": "stored", "id": str(result)}
    except Exception as e:
        return _fallback_store(user_id, session_id, content)

def search_memory(user_id: str, query: str, limit: int = 5):
    """Search memories by relevance"""
    if not MEM0_AVAILABLE:
        return _fallback_search(user_id, query, limit)
    try:
        results = memory.search(query, user_id=user_id, limit=limit)
        return {"results": results}
    except Exception as e:
        return _fallback_search(user_id, query, limit)

def get_all_memories(user_id: str):
    """Get all memories for a user"""
    if not MEM0_AVAILABLE:
        return _fallback_get_all(user_id)
    try:
        results = memory.get_all(user_id=user_id)
        return {"memories": results}
    except Exception as e:
        return _fallback_get_all(user_id)

def _fallback_store(user_id, session_id, content):
    """Fallback: store in JSON file when mem0 not available"""
    fpath = os.path.join(MEMORY_DIR, f"{user_id}.json")
    entries = []
    if os.path.exists(fpath):
        with open(fpath, encoding='utf-8') as f:
            entries = json.load(f)
    entries.append({
        "content": content,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    })
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    return {"status": "stored_fallback", "total_entries": len(entries)}

def _fallback_search(user_id, query, limit):
    """Fallback: simple text search"""
    fpath = os.path.join(MEMORY_DIR, f"{user_id}.json")
    if not os.path.exists(fpath):
        return {"results": []}
    with open(fpath, encoding='utf-8') as f:
        entries = json.load(f)
    q = query.lower()
    matches = [e for e in entries if q in e['content'].lower()]
    return {"results": matches[:limit], "total": len(matches)}

def _fallback_get_all(user_id):
    fpath = os.path.join(MEMORY_DIR, f"{user_id}.json")
    if not os.path.exists(fpath):
        return {"memories": []}
    with open(fpath, encoding='utf-8') as f:
        return {"memories": json.load(f)}

if __name__ == "__main__":
    print("Agent Memory Module")
    print(f"  mem0ai: {'AVAILABLE' if MEM0_AVAILABLE else 'UNAVAILABLE (fallback active)'}")
    print(f"  Storage: {MEMORY_DIR}")
    
    # Quick test
    r = add_memory("test_user", "test_session", "Hello from test")
    print(f"  Test store: {r}")
    if r.get('status') != 'stored_fallback':
        r2 = get_all_memories("test_user")
        print(f"  Test read: {len(r2.get('memories', []))} entries")
