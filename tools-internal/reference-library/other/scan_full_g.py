#!/usr/bin/env python3
"""THAN-THONG: Doc het G:\Ai - liet ke tat ca - khong dong cham"""
import zipfile, os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

G = r'G:\Ai'
E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'

# === 1) Inventory E workspace ===
e_file_names = set()
e_dir_names = set()
e_skills = {}
e_skill_paths = set()

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        e_file_names.add(f.lower())
    for d in dirs:
        e_dir_names.add(d.lower())

skills_dir = os.path.join(E, 'skills')
if os.path.exists(skills_dir):
    for s in os.listdir(skills_dir):
        sd = os.path.join(skills_dir, s)
        if os.path.isdir(sd):
            e_skills[s.lower()] = True
            for sf in os.listdir(sd):
                if sf.lower() == 'skill.md':
                    e_skill_paths.add(f'skills/{s.lower()}/skill.md')

# === 2) Scan all zips in G ===
zips = sorted([f for f in os.listdir(G) if f.endswith('.zip') and os.path.isfile(os.path.join(G, f))])

print("=" * 80)
print(f"SO DO: G:\\Ai ({len(zips)} zip files)")
print("=" * 80)

# Group by prefix
groups = {}
skip_zips = ['gmail-1.0.6.zip', 'caldav-calendar-1.0.1.zip', 'imap-smtp-email-0.0.13.zip',
             'multi-search-engine-2.1.3.zip', 'api-gateway-1.0.84.zip', 'desktop-control-1.0.0.zip',
             'whispergui-v2.zip', 'comtypes-1.4.16.zip', 'whisper-bin-x64.zip',
             'davinci-resolve-20-3-2-9.zip', 'graillon-free-3.2.zip', 'vbcable_driver_pack45.zip',
             'voicemeetersetup_v1122.zip', 'powershell-7.6.0-win-x64.zip',
             'camoufox.zip', 'marktext.zip', 'outline-apps.zip', 'seelen-ui.zip',
             'win10-gamingfocus-xart.zip', 'winhance.zip', 'winutil-acgos.zip',
             'sophia-script-windows.zip', 'pc-tinhchinh.zip']
skip_zips_lower = [z.lower() for z in skip_zips]

for zfile in zips:
    zlower = zfile.lower()
    if zlower in skip_zips_lower:
        continue
    
    # Skip known non-useful
    if any(x in zlower for x in ['graillon', 'vbcable', 'voicemeeter', 'davinci', 'powershell',
                                   'win10-gaming', 'seelen', 'winhance', 'winutil', 'sophia',
                                   'aacpx', '__mac', '.dmg', 'camoufox', 'powertoys',
                                   'outline-apps', 'marktext', 'whisper']):
        continue
    
    # Categorize
    fname_plain = zfile.replace('.zip', '')
    if 'claude' in zlower or 'claw-' in zlower or 'clawteam' in zlower or 'clawdinators' in zlower:
        cat = 'CLAW ECOSYSTEM'
    elif 'agent' in zlower or 'ai-' in zlower or '-ai' in zlower and 'skill' not in zlower:
        cat = 'AGENT/AI'
    elif 'openclaw' in zlower:
        cat = 'OPENCLAW'
    elif 'skill' in zlower:
        cat = 'SKILL'
    elif 'memory' in zlower or 'mem' in zlower and 'memo' not in zlower:
        cat = 'MEMORY'
    elif 'n8n' in zlower or 'cognee' in zlower:
        cat = 'N8N'
    elif 'api' in zlower or 'gateway' in zlower:
        cat = 'API/TOOL'
    elif 'langchain' in zlower or 'langgraph' in zlower or 'gemini' in zlower:
        cat = 'LLM/FRAMEWORK'
    elif 'mcp' in zlower:
        cat = 'MCP'
    elif 'plugin' in zlower:
        cat = 'PLUGIN'
    elif 'firecrawl' in zlower or 'browser' in zlower or 'spy' in zlower:
        cat = 'SEARCH/BROWSER'
    elif 'git' in zlower:
        cat = 'GIT/DEVOPS'
    elif 'design' in zlower:
        cat = 'DESIGN'
    else:
        cat = 'OTHER'
    
    if cat not in groups:
        groups[cat] = []
    groups[cat].append(zfile)

# === 3) Print grouped list ===
for cat in sorted(groups):
    items = groups[cat]
    total_mb = sum(os.path.getsize(os.path.join(G, f))/1048576 for f in items)
    print(f"\n{'=' * 60}")
    print(f"{cat} ({len(items)} files, {total_mb:.0f} MB)")
    print(f"{'=' * 60}")
    
    for zfile in sorted(items):
        fpath = os.path.join(G, zfile)
        sz_mb = os.path.getsize(fpath) / 1048576
        fname_plain = zfile.replace('.zip', '')
        
        try:
            with zipfile.ZipFile(fpath, 'r') as z:
                names = z.namelist()
                
                # Count types
                ts_cnt = len([n for n in names if n.endswith('.ts') and 'node_module' not in n.lower()])
                py_cnt = len([n for n in names if n.endswith('.py') and 'node_module' not in n.lower()])
                skill_cnt = len([n for n in names if 'skill.md' in n.lower() and 'node_module' not in n.lower()])
                
                # Read README or SKILL.md
                preview = ''
                for n in names:
                    if n.lower().endswith('readme.md') or n.lower().endswith('readme'):
                        try:
                            c = z.read(n).decode('utf-8', errors='replace')
                            preview = c.strip()[:120].replace('\n', ' ')
                            break
                        except: pass
                if not preview:
                    for n in names:
                        if 'skill.md' in n.lower():
                            try:
                                c = z.read(n).decode('utf-8', errors='replace')
                                preview = c.strip()[:120].replace('\n', ' ')
                                break
                            except: pass
                if not preview:
                    for n in names[:3]:
                        if n.endswith('.md'):
                            try:
                                c = z.read(n).decode('utf-8', errors='replace')
                                pr = c[:90].replace('|', '').replace('\n', ' ').strip()
                                if pr and len(pr) > 20:
                                    preview = pr
                                    break
                            except: pass
                
                # Check duplicate names
                dup_files = []
                dup_skills = []
                for n in names:
                    base = os.path.basename(n).lower()
                    if base in e_file_names or n.lower() in e_file_names:
                        dup_files.append(n)
                    if 'skill.md' in n.lower() and 'skills/' in n.lower() or '/skills/' in n.lower():
                        parts = n.split('/')
                        for i, p in enumerate(parts):
                            if p == 'skills' and i+1 < len(parts):
                                sname = parts[i+1].lower()
                                if sname in e_skills:
                                    dup_skills.append(parts[i+1])
                
                conflict_note = ''
                if dup_skills:
                    conflict_note = f' ⚠️ trung skill: {dup_skills[:3]}'
                elif len(dup_files) > 5:
                    conflict_note = f' ⚠️ trung {len(dup_files)} file'
                
                code_note = ''
                if ts_cnt > 0:
                    code_note += f' {ts_cnt}.ts'
                if py_cnt > 0:
                    code_note += f' {py_cnt}.py'
                if skill_cnt > 0:
                    code_note += f' {skill_cnt}skill'
                
                top_dirs = {}
                for n in names:
                    parts = n.split('/')
                    if len(parts) > 1:
                        top_dirs[parts[0]] = top_dirs.get(parts[0], 0) + 1
                top3 = sorted(top_dirs.items(), key=lambda x: -x[1])[:3]
                
                print(f"  [{sz_mb:6.1f}MB] {fname_plain}")
                print(f"         {len(names)} files{code_note}{conflict_note}")
                if top3:
                    print(f"         {[(d,c) for d,c in top3]}")
                if preview:
                    prv = preview[:100]
                    print(f"         {prv}")
                
        except Exception as ex:
            print(f"  [{sz_mb:6.1f}MB] {fname_plain}")
            print(f"         LOI DOC: {ex}")
        
        print()

# === 4) TOTAL ===
total_size = sum(os.path.getsize(os.path.join(G, f))/1048576 for f in zips)
total_checked = sum(os.path.getsize(os.path.join(G, f))/1048576 for f in zips 
                    if not any(x in f.lower() for x in ['davinci', 'graillon', 'vbcable', 'voicemeeter']))
print("=" * 80)
print(f"TONG: {len(zips)} files, {total_size:.0f} MB (bo qua driver/audio/video: ~{total_size-total_checked:.0f}MB)")
print(f"LIET KE XONG. KHONG DONG CHAM FILE NAO.")
print("=" * 80)
