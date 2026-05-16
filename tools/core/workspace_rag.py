#!/usr/bin/env python3
"""
workspace_rag.py — Local RAG search cho toàn bộ workspace

Index daily notes + MEMORY.md + script docs → Qdrant
Search bằng ngôn ngữ tự nhiên

Usage:
  python workspace_rag.py --index      # Index tất cả tài liệu
  python workspace_rag.py --query "..." # Tìm kiếm
  python workspace_rag.py --ask "..."   # Hỏi đáp (search + LLM)
"""

import os, sys, json, hashlib, re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get(
    "OPENCLAW_WORKSPACE",
    r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
))

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION = "workspace-knowledge"
OLLAMA_HOST = "http://localhost:11434"
EMBED_MODEL = "bge-m3:latest"
LLM_MODEL = "qwen2.5-coder:7b"


def safeprint(*args):
    text = " ".join(str(a) for a in args)
    try: print(text, flush=True)
    except UnicodeEncodeError: print(text.encode("ascii", "replace").decode("ascii"), flush=True)


def get_embedding(text):
    import urllib.request, json as j
    data = j.dumps({"model": EMBED_MODEL, "prompt": text[:8000]}).encode()
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/embeddings", data=data,
                                 headers={"Content-Type": "application/json"})
    resp = j.loads(urllib.request.urlopen(req).read())
    return resp.get("embedding", [])


def ask_llm(prompt):
    import urllib.request, json as j
    data = j.dumps({"model": LLM_MODEL, "prompt": prompt, "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 1024}}).encode()
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/generate", data=data,
                                 headers={"Content-Type": "application/json"})
    resp = j.loads(urllib.request.urlopen(req).read())
    return resp.get("response", "")


# ── Index ────────────────────────────────────────────────────────────

def collect_documents():
    """Thu thập tất cả text từ workspace."""
    docs = []
    suffixes = {".py", ".md", ".txt", ".yml", ".yaml", ".json", ".ps1", ".cmd"}

    # 1. Daily notes
    for f in sorted((WORKSPACE / "memory").glob("*.md")):
        if f.name in ("README.md", "INDEX.md") or f.name.startswith("consolidation"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            docs.append({"path": str(f.relative_to(WORKSPACE)), "content": content[:20000],
                         "type": "daily-note"})
        except: pass

    # 2. MEMORY.md
    mem = WORKSPACE / "MEMORY.md"
    if mem.exists():
        docs.append({"path": "MEMORY.md", "content": mem.read_text(encoding="utf-8", errors="replace")[:20000],
                     "type": "long-term-memory"})

    # 3. Core scripts
    for f in sorted((WORKSPACE / "tools-internal" / "scripts").glob("*.py")):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            docs.append({"path": str(f.relative_to(WORKSPACE)), "content": content[:20000],
                         "type": "script"})
        except: pass

    # 4. Workflow YAMLs
    for f in sorted((WORKSPACE / ".github" / "workflows").glob("*.yml")):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            docs.append({"path": str(f.relative_to(WORKSPACE)), "content": content[:20000],
                         "type": "workflow"})
        except: pass

    # 5. Run tests
    rt = WORKSPACE / "run_tests.py"
    if rt.exists():
        docs.append({"path": "run_tests.py", "content": rt.read_text(encoding="utf-8", errors="replace")[:20000],
                     "type": "script"})

    safeprint(f"Collected {len(docs)} documents")
    return docs


def index_documents(docs):
    """Index documents vào Qdrant."""
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import Distance, VectorParams

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # Create collection if not exists
    try:
        client.get_collection(COLLECTION)
        safeprint(f"Collection '{COLLECTION}' already exists")
    except:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
        safeprint(f"Created collection '{COLLECTION}'")

    # Index each doc
    indexed = 0
    for doc in docs:
        doc_id = hashlib.md5(doc["path"].encode()).hexdigest()

        # Skip if already exists
        try:
            existing = client.query_points(collection_name=COLLECTION, query=[], filter=models.Filter(
                must=[models.FieldCondition(key="_id", match=models.MatchValue(value=doc_id))]
            ), limit=1)
            if existing.points:
                continue
        except: pass

        # Get embedding
        vec = get_embedding(doc["path"] + "\n" + doc["content"][:2000])
        if not vec:
            continue

        # Store
        client.upsert(
            collection_name=COLLECTION,
            points=[models.PointStruct(
                id=doc_id,
                vector=vec,
                payload={"path": doc["path"], "type": doc["type"],
                         "content_preview": doc["content"][:1000]}
            )]
        )
        indexed += 1
        if indexed % 5 == 0:
            safeprint(f"  Indexed {indexed}/{len(docs)}...")

    safeprint(f"Done: {indexed} new docs indexed")


# ── Search ────────────────────────────────────────────────────────────

def search(query, limit=5):
    """Search Qdrant."""
    from qdrant_client import QdrantClient

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    try:
        client.get_collection(COLLECTION)
    except:
        safeprint("Collection not found. Run --index first")
        return []

    vec = get_embedding(query)
    if not vec:
        safeprint("Failed to get embedding")
        return []

    from qdrant_client.http import models
    results = client.query_points(
        collection_name=COLLECTION,
        query=vec,
        limit=limit
    )

    hits = []
    for r in results.points:
        hits.append({
            "path": r.payload.get("path", ""),
            "type": r.payload.get("type", ""),
            "score": r.score,
            "preview": r.payload.get("content_preview", "")[:500]
        })
    return hits


# ── Ask ───────────────────────────────────────────────────────────────

def ask(question):
    """Search + answer using local LLM."""
    safeprint(f"Searching for: {question}")
    hits = search(question, limit=5)

    if not hits:
        safeprint("No relevant documents found.")
        return "Không tìm thấy thông tin liên quan."

    context = "\n\n".join([f"[{h['path']}] ({h['score']:.2f})\n{h['preview']}" for h in hits])

    prompt = f"""Dựa trên các tài liệu sau, trả lời câu hỏi.

Tài liệu:
{context[:6000]}

Câu hỏi: {question}

Trả lời ngắn gọn, chính xác, bằng tiếng Việt. Nếu không có thông tin thì nói không biết."""

    safeprint("Generating answer with local LLM...")
    answer = ask_llm(prompt)
    return answer


# ── Main ──────────────────────────────────────────────────────────────

def main():
    args = set(sys.argv[1:])

    if "--index" in args:
        docs = collect_documents()
        index_documents(docs)

    elif "--query" in args:
        idx = sys.argv.index("--query")
        q = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        if not q:
            safeprint("Usage: --query \"your search query\"")
            return
        results = search(q)
        safeprint(f"\nResults for: {q}")
        safeprint("=" * 50)
        for r in results:
            safeprint(f"\n[{r['type']}] {r['path']} (score: {r['score']:.3f})")
            safeprint(f"  {r['preview'][:200]}")

    elif "--ask" in args:
        idx = sys.argv.index("--ask")
        q = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        if not q:
            safeprint("Usage: --ask \"your question\"")
            return
        answer = ask(q)
        safeprint(f"\nQuestion: {q}")
        safeprint(f"Answer: {answer}")

    else:
        safeprint("Usage:")
        safeprint("  workspace_rag.py --index         Index all documents")
        safeprint("  workspace_rag.py --query \"...\"   Search documents")
        safeprint("  workspace_rag.py --ask \"...\"     Q&A with context")


if __name__ == "__main__":
    main()
