#!/usr/bin/env python3
"""Phan tich 3300+ tools scripts — capacity analysis"""
import os, sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
EXTRACTED = os.path.join(TOOLS, 'extracted-scripts')

all_py = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_')]

print("=" * 70)
print("PHAN TICH NANG LUC: 3300+ TOOLS SCRIPTS")
print("=" * 70)

# 1) Source distribution
extracted_files = sum(len(files) for _, _, files in os.walk(EXTRACTED)) if os.path.exists(EXTRACTED) else 0
print(f"\n1. NGUON GOC")
print(f"   tools-internal/ root:       {len(all_py)} .py files")
print(f"   tools-internal/scripts/:    {len([f for f in os.listdir(os.path.join(TOOLS,'scripts')) if f.endswith('.py')])} .py files")
print(f"   tools-internal/extracted/:  {extracted_files} .py files (organized)")
print()

# 2) File size distribution
def size_cat(sz):
    if sz < 1024: return "tiny"
    if sz < 5120: return "small"
    if sz < 20480: return "medium"
    if sz < 102400: return "large"
    return "xlarge"

size_dist = Counter()
for f in all_py:
    sz = os.path.getsize(os.path.join(TOOLS, f))
    size_dist[size_cat(sz)] += 1
print("2. PHAN BO KICH THUOC")
for cat in ['tiny', 'small', 'medium', 'large', 'xlarge']:
    print(f"   {cat:8s}: {size_dist.get(cat, 0)} files")
print()

# 3) Import analysis (all files)
print("3. PHAN TICH IMPORT (lay domain tu import statements)")
domain_patterns = {
    'AI/ML Inference':       ['transformers', 'torch', 'tensorflow', 'onnx', 'llama_cpp', 'vllm'],
    'Web API/Server':        ['fastapi', 'flask', 'django', 'uvicorn', 'starlette', 'aiohttp', 'sanic', 'web'],
    'Web Scraping':          ['requests', 'httpx', 'urllib3', 'scrapy', 'selenium', 'playwright', 'beautifulsoup', 'bs4', 'lxml'],
    'Database':              ['sqlalchemy', 'sqlite3', 'psycopg2', 'pymongo', 'redis', 'mysql'],
    'File Processing':       ['pdfplumber', 'pypdf2', 'pdf', 'pandas', 'openpyxl', 'xlrd', 'docx', 'pillow', 'pil'],
    'Image/Video':           ['opencv', 'cv2', 'ffmpeg', 'moviepy', 'pillow', 'pil', 'numpy'],
    'System/OS':             ['psutil', 'shutil', 'subprocess', 'platform', 'win32', 'pywin', 'comtypes'],
    'Cryptography':          ['cryptography', 'hashlib', 'hmac', 'jwt', 'oauth', 'bcrypt'],
    'Memory/Search':         ['chromadb', 'faiss', 'elasticsearch', 'pinecone', 'milvus', 'weaviate', 'qdrant'],
    'Messaging/Social':      ['telegram', 'discord', 'slack', 'twitter', 'whatsapp', 'email'],
    'Git/DevOps':            ['gitpython', 'github', 'gitlab', 'docker', 'kubernetes', 'ansible'],
    'Speech/Audio':          ['whisper', 'speech_recognition', 'pyaudio', 'tts', 'stt'],
    'LangChain/LangGraph':   ['langchain', 'langgraph', 'langserve'],
    'Claude/OpenAI':         ['anthropic', 'openai', 'claude', 'bedrock'],
    'CLI/Terminal':          ['click', 'typer', 'argparse', 'rich', 'prompt_toolkit', 'questionary'],
    'Config/Data':           ['yaml', 'toml', 'json', 'configparser', 'dotenv'],
}

# Scan ALL files (it's worth taking the time)
domain_count = Counter()
for f in all_py:
    try:
        content = open(os.path.join(TOOLS, f), 'rb').read().decode('utf-8', errors='replace')[:5000].lower()
        for domain, keywords in domain_patterns.items():
            for kw in keywords:
                if kw in content:
                    domain_count[domain] += 1
                    break  # count once per domain per file
    except: pass

# Also count multi-domain files
print()
print("   Files theo domain:")
for domain, count in domain_count.most_common(20):
    pct = count * 100 // len(all_py)
    bar = '#' * (pct // 5)
    print(f"   {domain:25s}: {count:5d} files ({pct:2d}%) {bar}")
print()

# 4) Class and function analysis (quick scan)
print("4. CAC THANH PHAN CHUC NANG CHINH")
func_patterns = {
    'async def': 'async handler',
    'def main(': 'main entry',
    'class ': 'class',
    'def handle(': 'handler',
    'def process(': 'processor',
    'def generate(': 'generator',
    'def parse(': 'parser',
    'def search(': 'search',
    'def embed(': 'embedding',
    'def query(': 'query',
    'def train(': 'training',
    'def download(': 'download',
    'def upload(': 'upload',
}

func_counts = Counter()
for f in all_py[:1000]:
    try:
        content = open(os.path.join(TOOLS, f), 'rb').read().decode('utf-8', errors='replace')
        for pattern, label in func_patterns.items():
            if pattern in content:
                func_counts[label] += 1
    except: pass

for label, count in func_counts.most_common(15):
    print(f"   {label:20s}: {count} files")
print()

# 5) Identify actual tools/utilities (files with 'main()' or CLI entry)
print("5. FILE CO CLI ENTRY POINT (co the chay truc tiep)")
cli_files = []
for f in all_py:
    try:
        content = open(os.path.join(TOOLS, f), 'rb').read().decode('utf-8', errors='replace')[:3000]
        if 'if __name__ ==' in content or 'def main(' in content or 'typer' in content or 'click' in content.lower() or 'argparse' in content:
            cli_files.append(f)
    except: pass

print(f"   {len(cli_files)} files co entry point")
# Show key CLI tools
cli_by_cat = {
    'memory': [], 'search': [], 'server': [], 'download': [],
    'convert': [], 'analyze': [], 'embed': [], 'chat': []
}
for f in cli_files:
    for cat in cli_by_cat:
        if cat in f.lower():
            cli_by_cat[cat].append(f)
for cat, files in cli_by_cat.items():
    if files:
        print(f"   {cat:15s}: {len(files)} files (vd: {files[0]})")

print()
print("=" * 70)
print("HOAN TAT PHAN TICH")
print("=" * 70)
