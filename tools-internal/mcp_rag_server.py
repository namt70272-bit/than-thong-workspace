#!/usr/bin/env python
"""MCP RAG Server - port 9880"""
import os, sys, json, time
BASE = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
sys.path.insert(0, BASE)
DATA_DIR = os.path.join(BASE, "rag-data")

# Warm up the model
from sentence_transformers import SentenceTransformer
import numpy as np

print("Loading embedding model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print(f"Model loaded (384-dim vectors)")

# Load vector store
index_path = os.path.join(DATA_DIR, "index.json")
vectors_path = os.path.join(DATA_DIR, "vectors.npy")

chunks = json.loads(open(index_path, encoding="utf-8").read()) if os.path.exists(index_path) else []
vectors = np.load(vectors_path) if os.path.exists(vectors_path) else np.zeros((0, 384))
print(f"Loaded {len(chunks)} chunks, vectors shape: {vectors.shape}")

def search_rag(query, top_k=5):
    qvec = model.encode([query])[0]
    qnorm = qvec / np.linalg.norm(qvec)
    vnorm = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    scores = np.dot(vnorm, qnorm)
    top = np.argsort(scores)[-top_k:][::-1]
    results = []
    for idx in top:
        if scores[idx] > 0.1:
            results.append({
                "score": round(float(scores[idx]), 3),
                "text": chunks[idx]["full"][:500],
                "id": chunks[idx]["id"]
            })
    return results

# MCP Server
from fastmcp import FastMCP
import asyncio
mcp = FastMCP("RAG Server")

@mcp.tool()
def search(query: str, top_k: int = 5):
    """Search the RAG knowledge base"""
    start = time.time()
    results = search_rag(query, top_k)
    elapsed = time.time() - start
    return {
        "query": query,
        "results": results,
        "total_chunks": len(chunks),
        "time_seconds": round(elapsed, 2)
    }

@mcp.tool()
def status():
    """Get RAG system status"""
    return {
        "chunks": len(chunks),
        "dimensions": vectors.shape[1] if len(vectors) else 0,
        "model": "all-MiniLM-L6-v2"
    }

print("Starting RAG MCP Server on port 9880...")
asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9880))
