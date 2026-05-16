#!/usr/bin/env python3
"""Organize 2.411 files into extracted-scripts/ by source + function"""
import os, shutil, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
SCRIPTS = os.path.join(TOOLS, 'scripts')
EXTRACTED = os.path.join(TOOLS, 'extracted-scripts')
REFERENCE = os.path.join(TOOLS, 'reference-library')

# === SCAN ALL FILES ===
all_py = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_') and not f.startswith('_ext')]
print(f"Scanning {len(all_py)} files...")

# === BUILD CATEGORIES ===
# Keywords in filename -> category
FILENAME_RULES = {
    'finance/quant': ['financial', 'portfolio', 'equity', 'hedge', 'bond', 'stock', 'crypto',
                      'backtest', 'zipline', 'vectorbt', 'databento', 'capital', 'trade',
                      'quant', 'risk', 'volatility', 'leverage', 'margin', 'future', 'option',
                      'qlib', 'finrl', 'skfolio', 'fincept', 'btp_', 'algorithm', 'factor',
                      'market', 'fiscal', 'treasury', 'comtrade', 'bea_', 'bnr_'],
    'ml-models': ['classifier', 'regression', 'kmeans', 'pca', 'svm', 'random_forest',
                  'gradient_boost', 'lsh', 'lda', 'gaussian_mixture', 'isotonic',
                  'als_example', 'decision_tree', 'neural', 'deep', 'transformer_',
                  'tokenizer', 'embedding', 'modeling', 'routed_'],
    'spark-data': ['spark', 'rdd', 'dataframe', 'groupby', 'pyspark', 'hive',
                   'kafka', 'streaming', 'wordcount', 'partition', 'sql_',
                   'pipeline', 'avro', 'parquet'],
    'api-server': ['api_server', 'fastapi', 'uvicorn', 'oauth_proxy', 'backend',
                   'worker', 'proxy', 'config_server', 'starlette'],
    'web-scraping': ['scraper', 'crawl', 'downloader', 'fetch', 'spider'],
    'data-sources': ['gov_api', 'gov_data', 'bea_data', 'bnr_data', 'faostat',
                     'un_comtrade', 'nasa_gibs', 'canada_gov', 'swiss_gov', 'french',
                     'datagov', 'hdx_data', 'openafrica', 'spain_data', 'fiscal',
                     'ilostat', 'akshare_', 'dataportal'],
    'llm-integration': ['langchain', 'langgraph', 'langserve', 'llm_judge', 'rag',
                        'embedder', 'reranker', 'vector_store', 'prompt',
                        'openai', 'anthropic', 'claude', 'ollama'],
    'memory': ['memory', 'mem0', 'memu', 'embeddings', 'longmemeval',
               'convomem', 'locomo', 'membench'],
    'docs-processing': ['pdf_', 'docx_', 'md_parse', 'chunker', 'html_parser',
                        'markdown', 'ocr', 'textract'],
    'utils': ['utils', 'helper', 'util', 'common', 'base_', 'config',
              'logger', 'logging', 'format', 'validate'],
}

# Also scan file content for deeper categorization
CONTENT_RULES = {
    'finance': ['from qlib', 'from finrl', 'from skfolio', 'import talib', 'backtest', 'zipline'],
    'langchain': ['from langchain', 'from langgraph', 'from langserve'],
    'fastapi': ['from fastapi', 'import fastapi', 'from uvicorn'],
    'firecrawl': ['from firecrawl', 'import firecrawl'],
    'mem0': ['from mem0', 'import mem0'],
    'openai': ['from openai', 'import openai'],
    'mcp': ['from mcp', 'import mcp', 'from fastmcp'],
    'spark': ['from pyspark', 'import pyspark'],
    'torch': ['import torch', 'from torch'],
    'transformers': ['from transformers', 'import transformers'],
}

categories = {}
for f in all_py:
    # Try filename first
    matched = False
    for cat, kws in FILENAME_RULES.items():
        if any(kw in f.lower() for kw in kws):
            categories.setdefault(cat, []).append(f)
            matched = True
            break
    if matched:
        continue
    
    # Try content analysis
    try:
        c = open(os.path.join(TOOLS, f), 'rb').read(5000).decode('utf-8', errors='replace')
        for cat, kws in CONTENT_RULES.items():
            if any(kw in c.lower() for kw in kws):
                categories.setdefault(cat, []).append(f)
                matched = True
                break
    except: pass
    
    if not matched:
        if f.startswith('test_'):
            categories.setdefault('test-files', []).append(f)
        else:
            categories.setdefault('other', []).append(f)

# === MOVE FILES ===
os.makedirs(REFERENCE, exist_ok=True)
total_moved = 0

for cat in sorted(categories.keys()):
    cat_dir = os.path.join(REFERENCE, cat)
    os.makedirs(cat_dir, exist_ok=True)
    
    for f in categories[cat]:
        src = os.path.join(TOOLS, f)
        if not os.path.exists(src):
            continue
        dst = os.path.join(cat_dir, f)
        # Skip if already in extracted-scripts
        if os.path.exists(os.path.join(EXTRACTED, cat, f)):
            continue
        if not os.path.exists(dst):
            shutil.move(src, dst)
            total_moved += 1

# === REPORT ===
print(f"\n=== ORGANIZATION COMPLETE ===")
print(f"Total moved: {total_moved} files into {len(categories)} categories")
print(f"\nCategory breakdown:")

for cat in sorted(categories.keys()):
    count = len(categories[cat])
    dir_path = os.path.join(REFERENCE, cat)
    actual = len([f for f in os.listdir(dir_path) if f.endswith('.py')])
    print(f"  {cat:25s}: {count:4d} files -> {actual} in reference-library/{cat}/")

remaining = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_') and not f.startswith('_ext')]
print(f"\nRemaining in tools-internal/: {len(remaining)} .py files")

# Save index
index = {}
for cat, files in sorted(categories.items()):
    index[cat] = sorted(files)
idx_path = os.path.join(REFERENCE, '_index.json')
with open(idx_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f"Index saved: {idx_path}")
print("\nDONE")
