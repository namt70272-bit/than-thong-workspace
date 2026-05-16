#!/usr/bin/env python3
import os
TOOLS = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
EX = os.path.join(TOOLS, 'extracted-scripts')
for d in sorted(os.listdir(EX)):
    dd = os.path.join(EX, d)
    if not os.path.isdir(dd): continue
    fs = [f for f in os.listdir(dd) if f.endswith('.py')]
    sz = sum(os.path.getsize(os.path.join(dd,f))//1024 for f in fs)
    print(f'{d:25s} {len(fs):3d} scripts ~{sz:5d}KB')
# Also check key files in root
root_py = [f for f in os.listdir(TOOLS) if f.endswith('.py') and not f.startswith('_')]
# Find the real gems
gems = ['api_server.py', 'chat.py', 'web_server.py', 'search_engine.py', 'memory.py', 'crawler.py', 'agent_factory.py']
for g in gems:
    fp = os.path.join(TOOLS, g)
    if os.path.exists(fp):
        print(f'  FOUND: {g} ({os.path.getsize(fp)//1024}KB)')
