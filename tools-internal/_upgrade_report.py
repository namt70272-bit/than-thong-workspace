#!/usr/bin/env python3
"""Scan reference-library for high-value scripts -> upgrade report"""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REF = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\reference-library'

print("=== SCANNING REFERENCE LIBRARY ===")
print()

all_files = []
for root, dirs, files in os.walk(REF):
    for f in files:
        if f.endswith('.py'):
            rel = os.path.relpath(os.path.join(root, f), REF)
            sz = os.path.getsize(os.path.join(root, f))
            cat = root.replace(REF, '').strip('\\/')
            all_files.append({'path': rel, 'size_b': sz, 'category': cat})

print(f"Total files: {len(all_files)}")
print()

# Find high-value scripts (large + has main() entry point)
high_value = []
for item in all_files:
    fp = os.path.join(REF, item['path'])
    try:
        c = open(fp, 'rb').read().decode('utf-8', errors='replace')
        has_main = 'if __name__' in c
        has_class = 'class ' in c
        score = 0
        if has_main: score += 2
        if has_class: score += 1
        if item['size_b'] > 10000: score += 1
        item['score'] = score
        item['has_main'] = has_main
        item['has_class'] = has_class
        high_value.append(item)
    except:
        item['score'] = 0
        high_value.append(item)

high_value.sort(key=lambda x: -x['score'])

# Generate upgrade recommendations from the best scripts
print("=" * 65)
print("NANG CAP HE THONG — KHUYEN NGHI TU REFERENCE LIBRARY")
print("=" * 65)

# Group by category
from collections import Counter
cat_count = Counter(item['category'] for item in all_files)

print(f"\n1. THU VIEN THAM KHAO ({len(all_files)} files, {len(cat_count)} nhom)")
print()
for cat, cnt in cat_count.most_common():
    print(f"   {cat:25s}: {cnt:4d} files")

print()
print("2. CAPABILITIES CO THE TICH HOP VAO HE THONG")
print()

# Framework capabilities
frameworks = {
    'spark': {
        'files': 727 + 18,
        'capability': 'Xu ly du lieu lon (DataFrame, SQL, streaming)',
        'integration': 'Dung Spark scripts de xu ly batch data, ETL pipeline',
        'effort': 'Cao (can Spark runtime)'
    },
    'mcp': {
        'files': 221,
        'capability': 'MCP protocol — goi tools tu xa qua HTTP/SSE',
        'integration': 'DA CO: agent_mcp_server.py (port 9876)',
        'effort': 'Thap (da co san)'
    },
    'langchain': {
        'files': 120,
        'capability': 'Chain LLM calls, agent orchestration, RAG pipeline',
        'integration': 'Xay RAG pipeline cho agent: doc -> chunk -> embed -> search',
        'effort': 'Trung binh (can embedder)'
    },
    'firecrawl': {
        'files': 56,
        'capability': 'Web crawling + search API',
        'integration': 'DA CO: agent_search.py (+ FireCrawl API key)',
        'effort': 'Thap (da co key)'
    },
    'finance/quant': {
        'files': 58 + 40,
        'capability': 'Phan tich tai chinh, backtest, portfolio optimization',
        'integration': 'Backtest chien luoc giao dich, phan tich thi truong',
        'effort': 'Trung binh (can API data)'
    },
    'mem0/memory': {
        'files': 44 + 9,
        'capability': 'AI memory layer — nho hoi thoai, vector search',
        'integration': 'DA CO: agent_memory.py (JSON fallback)',
        'effort': 'Thap (da co)'
    },
    'web-scraping': {
        'files': 118,
        'capability': 'Crawl website, download content',
        'integration': 'Them FireCrawl + Spy-Search de agent co the doc web',
        'effort': 'Thap' 
    },
    'api-server': {
        'files': 29,
        'capability': 'FastAPI server, OAuth proxy, auth backend',
        'integration': 'Dung FastAPI scripts lam API Gateway cho agent',
        'effort': 'Trung binh'
    },
    'torch/ml': {
        'files': 23 + 20,
        'capability': 'Deep learning inference, local ML models',
        'integration': 'Chay model local qua Ollama (da co qwen2.5-coder)',
        'effort': 'Thap (Ollama da co)'
    },
}

for key, info in sorted(frameworks.items(), key=lambda x: -x[1]['files']):
    print(f"   [{key:20s}] {info['capability']}")
    print(f"   Files: {info['files']:4d} | Tich hop: {info['integration']}")
    print(f"   Effort: {info['effort']}")
    print()

# Top 20 scripts worth learning from
print("3. TOP 20 SCRIPTS GIA TRI CAO NHAT (tham khao chinh)")
print()
top = [item for item in high_value if item['score'] >= 3 and item['size_b'] > 5000][:20]
for i, item in enumerate(top):
    kb = item['size_b'] // 1024
    main_flag = '+' if item['has_main'] else ' '
    cls_flag = '+' if item['has_class'] else ' '
    print(f"   {i+1:2d}. [{kb:4d}KB] {item['path']:55s} [M:{main_flag} C:{cls_flag}]")

# Final recommendations
print()
print("=" * 65) 
print("4. KHUYEN NGHI NANG CAP NGAY")
print("=" * 65)
print("""
MUC DO THAP (lam ngay):
  - Tich hop FireCrawl vao agent_mcp_server (DA CO)
  - Mem0 JSON fallback agent_memory (DA CO)
  - FastMCP server 12 tools (DA CO)
  - Ollama qwen2.5-coder local LLM (DA CO)

MUC DO TRUNG BINH:
  - Xay RAG pipeline: doc -> chunk -> embed -> search
    (dung langchain reference + HuggingFace embedder)
  - Xay API Gateway tu FastAPI scripts
    (dung fastapi/ + api_server.py)
  - Tich hop finance analysis
    (dung finance/quant/ scripts)

MUC DO CAO:
  - Spark data processing pipeline
    (can Spark runtime, 727 files)
  - MCP multi-agent orchestration
    (can nhieu MCP server chay dong thoi)

NHUNG GI DA CO SAN (khong can lam them):
  ✅ 25 skills moi
  ✅ FastMCP 3.2.4 + 12 tools
  ✅ FireCrawl search (web)
  ✅ mem0 memory (JSON fallback)
  ✅ Ollama + qwen2.5-coder
  ✅ 2.411 files tham khao da sap xep
  ✅ 21 category reference library
""")
print(f"Index: reference-library/_index.json")
print("DONE")
