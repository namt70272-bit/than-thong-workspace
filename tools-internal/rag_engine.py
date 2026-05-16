#!/usr/bin/env python
"""
RAG Engine — Document → Chunk → Embed → Search
Zero external dependencies: uses HuggingFace + numpy (no Qdrant)
"""
import os, sys, json, hashlib, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
DATA_DIR = BASE / "rag-data"
os.makedirs(str(DATA_DIR), exist_ok=True)

# === CHUNKER ===
def chunk_text(text, max_chars=500, overlap=50):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        # Try to break at sentence or paragraph
        if end < len(text):
            for sep in ['\n\n', '\n', '. ', '! ', '? ', ', ', ' ']:
                idx = text.rfind(sep, start + max_chars//2, end)
                if idx > 0:
                    end = idx + len(sep)
                    break
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end - overlap > start + 1 else end
    return chunks

# === EMBEDDING ===
_embedder = None
def get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _embedder

def embed(texts):
    """Embed list of texts -> numpy array"""
    model = get_embedder()
    return model.encode(texts, show_progress_bar=False)

# === VECTOR STORE (numpy-based, no Qdrant) ===
import numpy as np

class LocalVectorStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.path / "index.json"
        self.vectors_path = self.path / "vectors.npy"
        self.chunks = []
        self.vectors = np.zeros((0, 384))  # MiniLM produces 384-dim vectors
        self._load()
    
    def _load(self):
        if self.index_path.exists():
            self.chunks = json.loads(self.index_path.read_text(encoding="utf-8"))
        if self.vectors_path.exists():
            self.vectors = np.load(str(self.vectors_path))
    
    def _save(self):
        self.index_path.write_text(json.dumps(self.chunks, ensure_ascii=False), encoding="utf-8")
        np.save(str(self.vectors_path), self.vectors)
    
    def add(self, chunks, vectors):
        start = len(self.chunks)
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            self.chunks.append({"id": start + i, "text": chunk[:200], "full": chunk})
        new_vecs = np.array(vectors)
        self.vectors = np.vstack([self.vectors, new_vecs]) if len(self.vectors) else new_vecs
        self._save()
    
    def search(self, query_vec, top_k=5):
        if len(self.vectors) == 0:
            return []
        # Cosine similarity
        query_norm = query_vec / np.linalg.norm(query_vec)
        vecs_norm = self.vectors / np.linalg.norm(self.vectors, axis=1, keepdims=True)
        scores = np.dot(vecs_norm, query_norm)
        top_idx = np.argsort(scores)[-top_k:][::-1]
        results = []
        for idx in top_idx:
            if scores[idx] > 0.1:  # similarity threshold
                results.append({
                    "score": float(scores[idx]),
                    "text": self.chunks[idx]["full"][:500],
                    "id": self.chunks[idx]["id"]
                })
        return results
    
    def count(self):
        return len(self.chunks)

# === INGESTION PIPELINE ===
def ingest_file(filepath, source_name, store):
    """Ingest a single file into the vector store"""
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except:
        return 0
    if len(text) < 100:
        return 0
    chunks = chunk_text(text)
    if not chunks:
        return 0
    vectors = embed(chunks)
    store.add([f"[{source_name}] {c}" for c in chunks], vectors)
    return len(chunks)

def ingest_directory(dirpath, store, max_files=200):
    """Ingest all .md and .py files from a directory"""
    total = 0
    files = list(Path(dirpath).rglob("*.md")) + list(Path(dirpath).rglob("*.py"))
    for i, f in enumerate(files):
        if i >= max_files:
            break
        rel = str(f.relative_to(dirpath))[:80]
        chunks = ingest_file(str(f), rel, store)
        if chunks:
            total += chunks
    return total

# === CLI ===
if __name__ == "__main__":
    import time
    print("RAG Engine")
    print("=" * 50)
    
    store = LocalVectorStore(str(DATA_DIR))
    print(f"Current store: {store.count()} chunks")
    print()
    
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if action == "ingest":
        print("Ingesting reference library...")
        ref = BASE / "reference-library"
        if ref.exists():
            start = time.time()
            n = ingest_directory(str(ref), store, max_files=200)
            elapsed = time.time() - start
            print(f"  Ingested {n} chunks from {ref.name} ({elapsed:.1f}s)")
        
        print("Ingesting skills...")
        skills = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills")
        if skills.exists():
            start = time.time()
            n = ingest_directory(str(skills), store, max_files=100)
            elapsed = time.time() - start
            print(f"  Ingested {n} chunks from skills ({elapsed:.1f}s)")
        
        print(f"\nTotal: {store.count()} chunks in vector store")
    
    elif action == "search":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "thần thông tool"
        print(f"Searching: '{query}'")
        start = time.time()
        qvec = embed([query])[0]
        results = store.search(qvec, top_k=5)
        elapsed = time.time() - start
        print(f"Found {len(results)} results ({elapsed:.2f}s)")
        for r in results:
            print(f"\n  [{r['score']:.3f}] {r['text'][:120]}...")
    
    elif action == "mcp_test":
        # Test if MCP server is running
        import httpx
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "RAG pipeline"
        print(f"Test RAG search via MCP: '{query}'")
        qvec = embed([query])[0]
        results = store.search(qvec, top_k=3)
        print(f"Local results: {len(results)}")
        for r in results:
            print(f"  [{r['score']:.3f}] {r['text'][:80]}")
    
    else:
        print(f"Store: {store.count()} chunks")
        if store.count() > 0:
            print("Sample chunks:")
            for c in store.chunks[:3]:
                print(f"  - {c['text'][:80]}...")
        print()
        print("Commands:")
        print("  ingest  - In压 chunks from reference-library + skills")
        print("  search  - Search for similar chunks")
