#!/usr/bin/env python3
"""Kiem tra xung dot chi tiet tung file - DUNG TEN"""
import os, zipfile, re, json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
G = r'G:\Ai'

# === Existing workspace inventory ===
e_files = set()
e_skills = {}
e_skill_files = set()
e_ports = set()

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        lname = f.lower()
        e_files.add(lname)
        e_files.add(os.path.join(rel, f).lower())
    for d in dirs:
        lname = d.lower()
        e_files.add(lname)

# Skill names / SKILL.md paths
skills_dir = os.path.join(E, 'skills')
if os.path.exists(skills_dir):
    for s in os.listdir(skills_dir):
        sd = os.path.join(skills_dir, s)
        if os.path.isdir(sd):
            e_skills[s.lower()] = sd
            for sf in os.listdir(sd):
                if sf.lower() == 'skill.md':
                    e_skill_files.add(f'{s.lower()}/skill.md')
                    e_skill_files.add(f'skills/{s.lower()}/skill.md')

# Ports in E
port_pat = re.compile(r'port\s*[:=]\s*(\d+)', re.IGNORECASE)
for root, dirs, files in os.walk(E):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env', '.conf', '.js']: continue
        try:
            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                for m in port_pat.finditer(fh.read()):
                    p = int(m.group(1))
                    if 3000 <= p <= 9999: e_ports.add(p)
        except: pass

# === MAP LABEL -> EXACT ZIP NAME ===
target_map = {
    'agent365-dev-tools': ['Agent365-CôngCụDev.zip', 'Agent365-CôngCụDev'],
    'fast-code':           ['FastCode.zip', 'FastCode'],
    'cli2skill':           ['CLI2KỹNăng.zip', 'CLI2KỹNăng'],
    'lobster':             ['Lobster.zip', 'Lobster'],
    'gbrain':              ['GBrain.zip', 'GBrain'],
    'skill-freeze':        ['KỹNăng-ĐóngBăng.zip', 'KỹNăng-ĐóngBăng'],
    'persona-protect':     ['Persona-BảoVệ.zip', 'Persona-BảoVệ'],
    'salacia':             ['Salacia-BảoVệ.zip', 'Salacia-BảoVệ'],
    'create-agent-skill':  ['TạoKỹNăngAgent.zip', 'TạoKỹNăngAgent'],
    'desktop-control':     ['desktop-control-1.0.0.zip', 'desktop-control-1.0.0'],
    'idea-to-product':     ['ÝTưởng-ThànhSảnPhẩm.zip', 'ÝTưởng-ThànhSảnPhẩm'],
    'nadirclaw':           ['NadirClaw.zip', 'NadirClaw'],
    'compliance-utility':  ['TiệnÍch-TuânThủ.zip', 'TiệnÍch-TuânThủ'],
    'mcp-hub':             ['MCP-TrungTâm.zip', 'MCP-TrungTâm'],
    'claude-octopus':      ['Claude-BạchTuộc.zip', 'Claude-BạchTuộc'],
    'claude-code-buddy':   ['Claude-BạnCode.zip', 'Claude-BạnCode'],
    'claude-supermemory':  ['Claude-SiêuBộNhớ.zip', 'Claude-SiêuBộNhớ'],
    'game-studio':         ['Claude-GameStudio.zip', 'Claude-GameStudio'],
    'cc-switch':           ['CC-ChuyểnMạch.zip', 'CC-ChuyểnMạch'],
    'fastmcp':             ['FastMCP.zip', 'FastMCP'],
    'mem0':                ['mem0.zip', 'mem0'],
    'firecrawl':           ['FireCrawl.zip', 'FireCrawl'],
    'mempalace':           ['MemPalace.zip', 'MemPalace'],
    'memorix':             ['Memorix.zip', 'Memorix'],
    'memu':                ['memU.zip', 'memU'],
    'agentscope':          ['AgentScope.zip', 'AgentScope'],
    'agent-boquantri':     ['Agent-BộQuảnTrị.zip', 'Agent-BộQuảnTrị'],
    'n8n-skill':           ['n8n-workflow-automation-1.0.0.zip', 'n8n-workflow-automation'],
    'desktop-browser-use': ['Browser-Dùng.zip', 'Browser-Dùng'],
    'spy-search':          ['Spy-TìmKiếm.zip', 'Spy-TìmKiếm'],
    'idea-plan':           ['LậpKếHoạchVớiTệp.zip', 'LậpKếHoạchVớiTệp'],
    'tao-prompt-ai':       ['TạoPromptAgentAI.zip', 'TạoPromptAgentAI'],
    'system-design':       ['ThiếtKếHệThốngAgent.zip', 'ThiếtKếHệThốngAgent'],
    'auto-research':       ['TựĐộng-NghiênCứuSâu.zip', 'TựĐộng-NghiênCứuSâu'],
    'agentscope':          ['AgentScope.zip', 'AgentScope'],
    'cicada':              ['CICADA.zip', 'CICADA'],
    'hermit':              ['Hermit.zip', 'Hermit'],
    'claw-rice':           ['Claw-Rice.zip', 'Claw-Rice'],
    'taiviet-security':    ['Trust.zip', 'Trust'],
    'openclaw-wechat':     ['OpenClaw-WeChat.zip', 'OpenClaw-WeChat'],
    'nix-openclaw':        ['Nix-OpenClaw.zip', 'Nix-OpenClaw'],
    'opencli':             ['OpenCLI.zip', 'OpenCLI'],
    'multipass':           ['Multipass.zip', 'Multipass'],
    'claw-mesh':           ['Claw-Mesh.zip', 'Claw-Mesh'],
    'mau-clone-web':       ['MẫuCloneWeb-AI.zip', 'MẫuCloneWeb-AI'],
    'bibigpt':             ['BibiGPT-XARTGPT.zip', 'BibiGPT-XARTGPT'],
    'memubot':             ['memUBot.zip', 'memUBot'],
    'caldav':              ['caldav-calendar-1.0.1.zip', 'caldav'],
    'gmail':               ['gmail-1.0.6.zip', 'gmail'],
    'imap-smtp':           ['imap-smtp-email-0.0.13.zip', 'imap-smtp'],
    'multi-search':        ['multi-search-engine-2.1.3.zip', 'multi-search'],
    'openclaw-manager':    ['OpenClaw-QuảnLý.zip', 'OpenClaw-QuảnLý'],
    'openclaw-supermem':   ['OpenClaw-SiêuBộNhớ.zip', 'OpenClaw-SiêuBộNhớ'],
    'openclaw-chat-mem':   ['OpenClaw-ChatBộNhớ.zip', 'OpenClaw-ChatBộNhớ'],
    'openclaw-project':    ['OpenClaw-DựÁn.zip', 'OpenClaw-DựÁn'],
    'gemini-langraph':     ['Gemini-LangGraph-KhởiĐầu.zip', 'Gemini-LangGraph'],
    'obsidian-llm-wiki':   ['Obsidian-LLM-Wiki.zip', 'Obsidian-LLM-Wiki'],
}

print("=" * 80)
print("KIEM TRA XUNG DOT CHI TIET - MOI FILE MOT DANH GIA")
print("=" * 80)
print()

results = {'safe': [], 'warn': [], 'fail': []}

for label, (fname, desc) in target_map.items():
    fpath = os.path.join(G, fname)
    if not os.path.exists(fpath):
        print(f"[EMPTY] {label} - file not found: {fname}")
        continue
    
    sz_mb = os.path.getsize(fpath) / 1048576
    
    issues = []
    dup_files = []
    dup_skills = []
    ports = []
    
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            names = z.namelist()
            
            for n in names:
                base = os.path.basename(n).lower()
                if base in e_files or n.lower() in e_files:
                    dup_files.append(n)
                
                if 'skill.md' in n.lower():
                    # Check if we have this skill name
                    parts = n.split('/')
                    idx = parts.index('skills') if 'skills' in parts else -1
                    if idx >= 0 and idx + 1 < len(parts):
                        sname = parts[idx + 1].lower()
                        if sname in e_skills:
                            dup_skills.append(sname)
            
            # Port scan
            for n in names:
                ext = os.path.splitext(n)[1].lower()
                if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env']: continue
                try:
                    content = z.read(n).decode('utf-8', errors='replace')
                    for m in port_pat.finditer(content):
                        p = int(m.group(1))
                        if 3000 <= p <= 9999 and p in e_ports:
                            ports.append((n.split('/')[-1], p))
                except: pass
            
    except Exception as ex:
        results['fail'].append((label, fname, str(ex)))
        print(f"[ERR] {label} - cannot read: {ex}")
        continue
    
    if dup_files: issues.append(f"TRUNG FILE({len(dup_files)})")
    if dup_skills: issues.append(f"TRUNG SKILL({dup_skills})")
    if ports: issues.append(f"PORT({ports})")
    
    # Size risk
    if sz_mb > 30:
        issues.append(f"LON({sz_mb:.0f}MB)")
    
    if not issues:
        results['safe'].append((label, fname, sz_mb, len(names)))
        icon = "✅"
        cat = "AN TOAN"
    elif len(dup_files) > 3 or 'SKILL' in str(issues) or ports:
        results['warn'].append((label, fname, issues))
        icon = "⚠️"
        cat = "CAN KIEM TRA"
    else:
        results['safe'].append((label, fname, sz_mb, len(names)))
        icon = "✅"
        cat = "AN TOAN (trung file nho)"
    
    print(f"[{icon}] {label}")
    print(f"  File: {fname} ({sz_mb:.1f}MB, {len(names)} files)")
    if dup_files:
        print(f"  - Trung file: {dup_files[:6]}")
        if len(dup_files) > 6: print(f"    ... va {len(dup_files)-6} file nua")
    if dup_skills:
        print(f"  - Trung skill: {dup_skills}")
    if ports:
        print(f"  - Port conflict: {ports}")
    print()

# ==== SUMMARY ====
print("=" * 80)
print("TOM TAT")
print("=" * 80)
print(f"\n✅ AN TOAN ({len(results['safe'])} file): co the lay")
for label, fname, sz, cnt in results['safe']:
    print(f"  - {label} ({sz:.1f}MB, {cnt} files)")

print(f"\n⚠️ CAN KIEM TRA ({len(results['warn'])} file): co xung dot nho")
for label, fname, issues in results['warn']:
    print(f"  - {label}: {issues}")

print(f"\n❌ LOI ({len(results['fail'])} file): khong doc duoc")
for label, fname, err in results['fail']:
    print(f"  - {label} ({err})")
