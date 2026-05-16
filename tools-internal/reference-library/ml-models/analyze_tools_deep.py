#!/usr/bin/env python3
"""Khoi phan tich sau: tim script gia tri cao, phan loai cu the"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
all_py = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_') and not f.startswith('_ext')]

# === Tim file co chuc nang dac biet ===
patterns = {
    'File Explorer/Manager': ['walk', 'listdir', 'scandir', 'glob', 'file_manager'],
    'Download/Upload Tool': ['download_file', 'upload', 'wget', 'aria2'],
    'OCR/Text Extraction': ['ocr', 'pytesseract', 'tesseract', 'textract'],
    'Database Client': ['sqlite', 'mysql', 'postgres', 'mongodb', 'redis_client'],
    'Email Handler': ['smtp', 'imap', 'send_email', 'mail'],
    'Web Scraper': ['scraper', 'crawl', 'extract_url', 'fetch_page'],
    'Data Converter': ['convert', 'json2csv', 'csv2json', 'xml2dict', 'to_csv'],
    'Report Generator': ['report', 'generate_report', 'dashboard'],
    'Config Reader': ['read_config', 'config_parser', 'yaml_loader'],
    'Network Scanner': ['port_scan', 'network', 'sniff', 'ping'],
    'Auth/Encryption': ['encrypt', 'decrypt', 'hash', 'jwt', 'token'],
    'Chat Bot': ['chat', 'bot', 'respond', 'conversation'],
    'Code Generator': ['code_gen', 'generate_code', 'scaffold'],
    'Schedule/Timer': ['schedule', 'cron', 'timer', 'delay'],
    'Log Analyzer': ['log_parser', 'analyze_log', 'log_reader'],
    'Translation': ['translate', 'translation', 'lang_detect'],
    'Compression': ['compress', 'zip', 'tar', 'gzip', 'unzip'],
    'Notification': ['notify', 'alert', 'send_sms', 'push'],
    'Test Runner': ['test', 'unittest', 'pytest', 'benchmark'],
    'Template Engine': ['template', 'jinja', 'mako', 'render'],
}

all_scripts = {}
total = 0

for f in all_py:
    try:
        content = open(os.path.join(TOOLS, f), 'rb').read().decode('utf-8', errors='replace')
        clower = content.lower()
        matches = []
        for cat, keywords in patterns.items():
            for kw in keywords:
                if kw in clower:
                    matches.append(cat)
                    break
        if matches:
            total += 1
            all_scripts[f] = matches
    except:
        pass

print("=" * 65)
print("KHO PHAN TICH SAU: NANG LUC CU THE")
print("=" * 65)

# Group by category
from collections import Counter
cat_count = Counter()
for f, cats in all_scripts.items():
    for c in cats:
        cat_count[c] += 1

print(f"\nTong {total} script co chuc nang ro rang:\n")
for cat, count in cat_count.most_common(30):
    examples = [f for f, cats in all_scripts.items() if cat in cats][:3]
    print(f"  {cat:25s}: {count:3d} scripts")
    for ex in examples:
        sz = os.path.getsize(os.path.join(TOOLS, ex)) // 1024
        print(f"    - {ex:50s} [{sz}KB]")

print()
print("=" * 65)
print("TOP 50 SCRIPTS GIA TRI CAO NHAT (theo kich thuoc + chuc nang)")
print("=" * 65)

# Score: script gia tri = medium-large size + multiple categories
scored = []
for f, cats in all_scripts.items():
    sz = os.path.getsize(os.path.join(TOOLS, f))
    if sz < 5000: continue  # skip tiny files
    score = len(cats) * 100 + (sz // 1024)
    scored.append((score, f, sz, cats))

scored.sort(key=lambda x: -x[0])

print(f"\n{'#':>3} {'Script':45s} {'KB':>6} {'Chuc nang':30s}")
print(f"{'---':>3} {'-'*45:45s} {'-'*6:>6} {'-'*30:30s}")
for i, (score, f, sz, cats) in enumerate(scored[:50]):
    sz_kb = sz // 1024
    main_cat = cats[0] if cats else ''
    print(f"{i+1:3d} {f:45s} {sz_kb:6d} {main_cat:30s}")

print()
print("=" * 65)
print("FILE CO TIEM NANG TICH HOP TRUC TIEP (server, cli, api)")
print("=" * 65)

server_like = [f for f in all_py if any(kw in open(os.path.join(TOOLS,f),'rb').read().decode('utf-8',errors='replace')[:3000].lower() for kw in ['fastapi','flask','uvicorn','sanic','aiohttp.web','server.run','app.run','start_server'])]
cli_like = [f for f in all_py if 'if __name__' in open(os.path.join(TOOLS,f),'rb').read().decode('utf-8',errors='replace')[:2000]]

print(f"\n  Server-type scripts: {len(server_like)}")
for f in server_like[:10]:
    sz = os.path.getsize(os.path.join(TOOLS, f)) // 1024
    print(f"    {f:45s} [{sz}KB]")
print(f"\n  CLI-capable scripts: {len(cli_like)}")
for f in cli_like[:10]:
    sz = os.path.getsize(os.path.join(TOOLS, f)) // 1024
    print(f"    {f:45s} [{sz}KB]")

print()
print("=" * 65)
print("HOAN TAT")
print("=" * 65)
