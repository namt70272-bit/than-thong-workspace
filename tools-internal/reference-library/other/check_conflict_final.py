#!/usr/bin/env python3
"""KIEM TRA XUNG DOT CHI TIET 156 file an toan voi E workspace"""
import zipfile, os, sys, json, re, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

G = r'G:\Ai'
E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
REVIEW = os.path.join(E, 'review', 'candidate')

# Skip list
SKIP_LIST = ['davinci-resolve', 'powershell-7.6', 'camoufox', 'graillon', 'vbcable', 'voicemeeter',
             'marktext', 'outline-apps', 'seelen-ui', 'win10-gaming', 'winhance', 'winutil', 'sophia',
             'whisper-bin-x64', 'whispergui', 'comtypes-1.4.16', 'gsnapwin64']
CONFLICT_FILES = ['FastCode.zip', 'OpenClaw.zip', 'OpenClaw-QWQ.zip', 'AtomicBot.zip', 'OpenViking.zip', 'AntiGravity-KỹNăngHay.zip']
BIG_SKIP = ['AI-Maestro.zip', 'ClawWork.zip', 'Dify-Plugin.zip', 'Hello-Agent.zip', 'n8n.zip']

zips_to_check = []
for f in os.listdir(G):
 if not f.endswith('.zip'): continue
 fn = f.lower()
 if any(s in fn for s in SKIP_LIST): continue
 if f in CONFLICT_FILES or any(b in fn for b in ['ai-maestro', 'clawwork', 'dify-plugin', 'hello-agent']): continue
 if fn == 'n8n.zip': continue
 zips_to_check.append(f)

# === Index E workspace ===
e_file_index = {}   # basename -> set(rel_paths)
e_skill_names = set()
e_config_port = {}
e_dependency_names = set()
e_dir_structure = set()
e_python_imports_all = set()
e_typescript_exports = set()

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        lname = f.lower()
        if lname not in e_file_index: e_file_index[lname] = set()
        e_file_index[lname].add(os.path.join(rel, f).lower())
    for d in dirs:
        lname = d.lower()
        e_dir_structure.add(lname)

# Skills
skdir = os.path.join(E, 'skills')
if os.path.exists(skdir):
    for s in os.listdir(skdir):
        if os.path.isdir(os.path.join(skdir, s)): e_skill_names.add(s.lower())

# Read config files for port numbers
for root, dirs, files in os.walk(E):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env', '.conf', '.js', '.tsx']: continue
        try:
            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read(20000)
                for m in re.finditer(r'(?:port|PORT|listen|LISTEN)\s*[:=]\s*(\d{3,5})', content):
                    e_config_port[int(m.group(1))] = e_config_port.get(int(m.group(1)), 0) + 1
                
                # Find imports/packages
                for m in re.finditer(r'import\s+(\w+)', content):
                    if m.group(1).lower() not in ['os', 'sys', 're', 'json', 'math', 'time', 'pathlib', 'typing']:
                        e_python_imports_all.add(m.group(1).lower())
        except: pass

# Read package.json from various places
for root, dirs, files in os.walk(E):
    for f in files:
        if f == 'package.json' and 'node_module' not in root.lower():
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                    pkg = json.load(fh)
                    for key in ['dependencies', 'devDependencies', 'peerDependencies']:
                        if key in pkg:
                            for dep in pkg[key]:
                                e_dependency_names.add(dep.lower())
            except: pass

port_pat = re.compile(r'(?:port|PORT|listen|LISTEN)\s*[:=]\s*(\d{3,5})')

# === Scan each safe zip ===
print("=" * 80)
print("KIEM TRA CHI TIET: XUNG DOT PORT / DEPENDENCY / SKILL PATH")
print("=" * 80)

results = {
    'XUNG_DOT': [],
    'CAN_KIEM_TRA': [],
    'AN_TOAN': []
}

for fname in sorted(zips_to_check):
    fpath = os.path.join(G, fname)
    sz_mb = os.path.getsize(fpath) / 1048576
    display = fname.replace('.zip', '')
    
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            names = z.namelist()
            
            conflicts = []
            
            # 1) Check skill path conflicts
            for n in names:
                if n.lower() == 'skill.md' or n.lower().endswith('/skill.md') and 'node_module' not in n.lower():
                    parts = n.split('/')
                    for i, p in enumerate(parts):
                        if p == 'skills' and i+1 < len(parts):
                            sname = parts[i+1].lower()
                            if sname in e_skill_names:
                                conflicts.append(f"SKILL_PATH: skills/{parts[i+1]} da ton tai")
                
                # Check for /tools/ or /tools-internal/ paths
                if any(x in n.lower() for x in ['/tools/', '/tools-internal/', '/scripts/']) and 'node_module' not in n.lower():
                    base = os.path.basename(n).lower()
                    if base in e_file_index and not base.endswith('.md'):
                        conflicts.append(f"TOOL_PATH: {n} (trung ten file trong tools/)")
            
            # 2) Check ports used inside zip files
            zip_ports = set()
            for n in names[:200]:  # limit to keep speed
                ext = os.path.splitext(n)[1].lower()
                if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env', '.js']: continue
                try:
                    content = z.read(n).decode('utf-8', errors='replace')
                    for m in port_pat.finditer(content):
                        p = int(m.group(1))
                        if 3000 <= p <= 9999:
                            zip_ports.add(p)
                except: pass
            
            if zip_ports:
                for p in sorted(zip_ports):
                    if p in e_config_port:
                        conflicts.append(f"PORT {p} (dung trong E: {e_config_port[p]} lan)")
            
            # 3) Check dependency names
            zip_deps = set()
            for n in names:
                if n.endswith('package.json'):
                    try:
                        content = z.read(n).decode('utf-8', errors='replace')
                        pkg = json.loads(content)
                        for key in ['dependencies', 'devDependencies', 'peerDependencies']:
                            if key in pkg:
                                for dep in pkg[key]:
                                    zip_deps.add(dep.lower())
                    except: pass
                if n.endswith('requirements.txt') or n.endswith('pyproject.toml'):
                    try:
                        content = z.read(n).decode('utf-8', errors='replace')
                        for m in re.finditer(r'^([a-zA-Z][\w-]+)', content, re.MULTILINE):
                            dep = m.group(1).lower().strip()
                            if dep not in ['python', 'pip']:
                                zip_deps.add(dep)
                    except: pass
            
            dep_conflicts = zip_deps & e_dependency_names
            if dep_conflicts:
                conflicts.append(f"DEP: {', '.join(sorted(dep_conflicts)[:10])}")
            
            # 4) Check for same top-level directory names
            zip_top_dirs = set()
            for n in names:
                parts = n.split('/')
                if len(parts) > 1 and parts[0]:
                    zip_top_dirs.add(parts[0].lower())
            
            dir_collisions = zip_top_dirs & e_dir_structure
            if dir_collisions:
                real_collisions = [d for d in dir_collisions if d not in ['.gitignore', '.github', 'docs', 'examples', 'tests', 'scripts']]
                if real_collisions:
                    conflicts.append(f"DIR: {', '.join(sorted(real_collisions)[:5])}")
            
            # Summary
            if not conflicts:
                results['AN_TOAN'].append((fname, sz_mb, len(names)))
                status = "✅ AN TOAN"
            elif len(conflicts) <= 2:
                results['CAN_KIEM_TRA'].append((fname, sz_mb, len(names), conflicts))
                status = "⚡ CAN KIEM"
            else:
                results['XUNG_DOT'].append((fname, sz_mb, len(names), conflicts))
                status = "⚠️ XUNG DOT"
            
            print(f"\n[{status}] {display}")
            print(f"  {sz_mb:.1f}MB | {len(names)} files")
            if conflicts:
                for c in conflicts[:3]:
                    print(f"  → {c}")
                if len(conflicts) > 3:
                    print(f"  → ... va {len(conflicts)-3} nua")
            
    except Exception as ex:
        print(f"\n[❌ LOI] {display}")
        print(f"  {sz_mb:.1f}MB | Khong doc duoc: {ex}")

# === Final Summary ===
print("\n" + "=" * 80)
print("TONG KET")
print("=" * 80)
print(f"\n✅ AN TOAN tuyet doi: {len(results['AN_TOAN'])} files")
print(f"⚡ Can kiem tra nhe: {len(results['CAN_KIEM_TRA'])} files")
print(f"⚠️ XUNG DOT: {len(results['XUNG_DOT'])} files")

if results['CAN_KIEM_TRA']:
    print("\n--- CAN KIEM TRA ---")
    for fname, sz, cnt, conflicts in results['CAN_KIEM_TRA']:
        print(f"  {fname.replace('.zip','')} [{sz:.1f}MB] {conflicts}")

if results['XUNG_DOT']:
    print("\n--- XUNG DOT ---")
    for fname, sz, cnt, conflicts in results['XUNG_DOT']:
        print(f"  {fname.replace('.zip','')} [{sz:.1f}MB]")
        for c in conflicts[:5]:
            print(f"    → {c}")

# === Plan storage structure ===
print("\n" + "=" * 80)
print("KHONG GIAN LUU TRU DE XUAT")
print("=" * 80)

storage_plan = {
    'skills/': 'Skills và Agent Skills',
    'tools-internal/': 'Scripts nội bộ',
    'review/candidate/': 'Khu vực chứa file zip gốc đã kiểm tra',
    'references/awesome-skills-catalog/': 'Danh mục skills tham khảo',
    'utils/': 'Utils và tools nhỏ',
}

print("""
Cau truc de xuat cho E workspace:

E:\\KY-DATA\\OpenClaw\\runtime-mirror\\.openclaw\\workspace\\
├── review/candidate/         ← File zip goc (da kiem tra)
│   ├── agent-framework/      ← AgentScope, Spring-AI, VũTrụAgent...
│   ├── agent-tool/           ← TạoKỹNăngAgent, CLI2KỹNăng, CICADA...
│   ├── skill-collection/     ← KỹNăngAgentKhoaHọc, Paperclip...
│   ├── memory/               ← mem0, memU, MemPalace...
│   ├── search-browser/       ← FireCrawl, Browser-Dùng...
│   ├── mcp/                  ← FastMCP, Toonify-MCP...
│   ├── api-gateway/          ← Chat2API, DeepSeek-API, API-Mới...
│   ├── git-devops/           ← GitNexus, Git-Cliff...
│   └── other/                ← Còn lại
│
├── skills/                   ← Skills se trich xuat
│   ├── agent-scope/
│   ├── agent-governance/
│   ├── cicada/
│   ├── ... (skills tham khao)
│   └── n8n-flow-builder/    ← Đa co san
│
├── tools-internal/           ← Scripts nội bộ
│   ├── extract_skills.py     ← Trich skill tu zip
│   └── import_candidate.py   ← Copy file ve
│
└── utils/                    ← Utility nho
""")

# Write full report
with open(os.path.join(E, 'review', 'G-Ai-conflict-check.md'), 'w', encoding='utf-8') as f:
    f.write("# Kiem tra xung dot 156 file voi E workspace\n\n")
    f.write(f"✅ AN TOAN: {len(results['AN_TOAN'])}\n")
    f.write(f"⚡ CAN KIEM: {len(results['CAN_KIEM_TRA'])}\n")
    f.write(f"⚠️ XUNG DOT: {len(results['XUNG_DOT'])}\n\n")
    
    for cat, items in [('AN_TOAN', results['AN_TOAN']), ('CAN_KIEM_TRA', results['CAN_KIEM_TRA']), ('XUNG_DOT', results['XUNG_DOT'])]:
        f.write(f"## {cat}\n\n")
        for item in items:
            fname = item[0].replace('.zip', '')
            sz = item[1]
            cnt = item[2]
            if cat == 'AN_TOAN':
                f.write(f"- {fname} [{sz:.1f}MB, {cnt} files]\n")
            else:
                conflicts = item[3]
                f.write(f"- {fname} [{sz:.1f}MB, {cnt} files]: {'; '.join(conflicts[:5])}\n")
    
    f.write(f"\n---\nGenerated: 2026-05-14\n")

print("\nBao cao tai: review/G-Ai-conflict-check.md")
print("HOAN THANH.")
