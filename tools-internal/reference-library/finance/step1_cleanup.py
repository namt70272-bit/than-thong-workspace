#!/usr/bin/env python3
"""Buoc 1: Don tools-internal — xoa rac, sap xep scripts."""
import os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
EXTRACTED = os.path.join(TOOLS, 'extracted-scripts')
TRASH = os.path.join(TOOLS, '_trash')

all_py = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_') and not f.startswith('_ext')]

print("=" * 60)
print("BUOC 1: DON TOOLS-INTERNAL")
print("=" * 60)
print(f"\nTong so .py files: {len(all_py)}")
print()

# === 1A: Xoa test_*.py nho (<5KB, ko co class, ko co if __name__) ===
deleted = set()
for f in all_py:
    if not f.startswith('test_') and not f.endswith('_test.py'):
        continue
    fp = os.path.join(TOOLS, f)
    sz = os.path.getsize(fp)
    if sz > 5120:
        continue  # keep larger test files
    try:
        content = open(fp, 'rb').read().decode('utf-8', errors='replace')
        # Keep if has class or entry point or meaningful logic
        if 'class ' in content or 'if __name__' in content or 'def ' in content:
            continue
    except:
        pass
    os.remove(fp)
    deleted.add(f)

print(f"1A. Xoa test_*.py nho vo dung: {len(deleted)} files")
for f in deleted[:20]:
    print(f"    [DELETE] {f}")
if len(deleted) > 20:
    print(f"    ... va {len(deleted)-20} files nua")
print()

# === 1B: Gom scripts cung nhom vao extracted-scripts/ ===
# Phat hien nhom tu ten file
groups = {
    'finance': ['financial', 'portfolio', 'equity', 'hedge', 'bond', 'stock', 'crypto',
                'backtest', 'zipline', 'vectorbt', 'databento', 'capital', 'trade',
                'algorithm', 'quant', 'risk', 'volatility', 'leverage'],
    'spark': ['spark', 'rdd', 'dataframe', 'groupby', 'pyspark', 'sql_', 'hive',
              'kafka', 'streaming', 'wordcount'],
    'sklearn-ml': ['classifier', 'regression', 'kmeans', 'pca', 'svm', 'random_forest',
                   'gradient_boost', 'lsh', 'lda', 'gaussian_mixture', 'isotonic'],
    'api-gov': ['gov_api', 'gov_data', 'bea_data', 'bnr_data', 'faostat',
                'un_comtrade', 'nasa_gibs', 'canada_gov', 'swiss_gov', 'french_gov',
                'datagov', 'hdx_data', 'openafrica', 'spain_data', 'fiscal_data'],
    'langchain-llm': ['langchain', 'langgraph', 'langserve', 'llm_judge', 'rag',
                      'embedder', 'reranker', 'vector_store', 'prompt'],
    'memory': ['memory', 'mem0', 'memu', 'embeddings', 'vector'],
    'server-api': ['api_server', 'fastapi', 'uvicorn', 'oauth_proxy', 'backend',
                   'worker', 'proxy'],
    'test-utils': ['test_data', 'test_config', 'test_settings'],
}

moved = 0
for group_name, keywords in groups.items():
    group_dir = os.path.join(EXTRACTED, group_name)
    os.makedirs(group_dir, exist_ok=True)
    for f in all_py:
        if f in deleted:
            continue
        # Check file still exists (may have been deleted in 1A)
        src = os.path.join(TOOLS, f)
        if not os.path.exists(src):
            continue
        if any(kw in f.lower() for kw in keywords):
            dst = os.path.join(group_dir, f)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                moved += 1

print(f"1B. Gom vao extracted-scripts/ : {moved} files")
for d in sorted(os.listdir(EXTRACTED)):
    dd = os.path.join(EXTRACTED, d)
    if os.path.isdir(dd):
        cnt = len([f for f in os.listdir(dd) if f.endswith('.py')])
        if cnt > 0:
            print(f"    extracted-scripts/{d}/ : {cnt} files")
print()

# === 1C: Thong ke con lai ===
remaining = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_') and not f.startswith('_ext')]
print(f"1C. Con lai trong tools-internal/ root: {len(remaining)} .py files")
print()

print("=" * 60)
print("HOAN TAT BUOC 1")
print("=" * 60)
