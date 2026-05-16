#!/usr/bin/env python3
"""Kiem tra xung dot tung file trong G:\Ai voi E workspace"""
import zipfile, os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
G = r'G:\Ai'

# === Lay danh sach file & skill trong E ===
e_files = set()
e_skills = set()
e_configs = set()
e_scripts = set()
e_ports = set()
e_top_dirs = set()

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        e_files.add(f.lower())
        e_files.add(os.path.join(rel, f).lower())
        if 'skill' in rel.lower():
            e_skills.add(f.split('.')[0].lower())
    for d in dirs:
        full = os.path.relpath(os.path.join(root, d), E)
        if full != '.':
            e_top_dirs.add(d.lower())
            e_top_dirs.add(full.lower())

# Skill names from skills/ dir
skills_dir = os.path.join(E, 'skills')
if os.path.exists(skills_dir):
    for s in os.listdir(skills_dir):
        if os.path.isdir(os.path.join(skills_dir, s)):
            e_skills.add(s.lower())

e_port_patterns = [r'port\s*[:=]\s*(\d+)', r'listen\s*(\d+)', r'PORT\s*=\s*(\d+)']
e_ports_found = set()
for root, dirs, files in os.walk(E):
    for f in files:
        if not f.endswith(('.py', '.ts', '.json', '.yaml', '.yml', '.env', '.conf')):
            continue
        try:
            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            for pat in e_port_patterns:
                matches = re.findall(pat, content, re.IGNORECASE)
                for m in matches:
                    p = int(m)
                    if 3000 <= p <= 9999:
                        e_ports_found.add(p)
        except:
            pass

print("=" * 70)
print("KIEM TRA XUNG DOT CHI TIET")
print("=" * 70)

# === Cac file CAN KIEM TRA ===
targets = [
    # Uu tien so 1
    ('Agent365-CongCuDev.zip', 'dev-tools', None),
    ('FastCode.zip', 'code-skills', None),
    ('CLI2KyNang.zip', 'cli2skill', None),
    ('Lobster.zip', 'lobster-workflow', None),
    ('GBrain.zip', 'gbrain-memory', None),
    ('KyNang-DongBang.zip', 'skill-freeze', None),
    ('Persona-BaoVe.zip', 'persona-protect', None),
    ('Salacia-BaoVe.zip', 'salacia', None),
    ('TaoKyNangAgent.zip', 'create-agent-skill', None),
    ('Desktop-Control.zip', 'desktop-control', None),
    ('YTruong-ThanhSanPham.zip', 'idea-to-product', None),
    ('NadirClaw.zip', 'nadirclaw', None),
    ('TienIch-TuanThu.zip', 'compliance-utility', None),
    ('MCP-TrungTam.zip', 'mcp-hub', None),
    ('Claude-Octopus.zip', 'claude-octopus', None),
    ('Claude-Code-Buddy.zip', 'claude-code-buddy', None),
    ('Claude-Supermemory.zip', 'claude-supermemory', None),
    ('Claude-GameStudio.zip', 'game-studio', None),
    ('CC-Switch.zip', 'cc-switch', None),
    ('FastMCP.zip', 'fastmcp', None),
    ('Mem0.zip', 'mem0', None),
    ('FireCrawl.zip', 'firecrawl', None),
    ('MemPalace.zip', 'mempalace', None),
    ('Memorix.zip', 'memorix', None),
    ('MemU.zip', 'memu', None),
]

# Map Vietnamese names -> actual zip names (approximate)
viet_name_map = {
    'TaoKyNangAgent': 'TaoKỹNăngAgent',
    'YTruong-ThanhSanPham': 'ÝTưởng-ThànhSảnPhẩm',
    'KyNang-DongBang': 'KỹNăng-ĐóngBăng',
    'TienIch-TuanThu': 'TiệnÍch-TuânThủ',
}

def find_zip(name):
    """Find actual zip in G: with fuzzy match"""
    actuals = [f for f in os.listdir(G) if f.endswith('.zip') and f.lower().startswith(name.lower())]
    if actuals:
        return actuals[0]
    # Try more fuzzy
    for f in os.listdir(G):
        if f.endswith('.zip') and name.lower() in f.lower():
            return f
    return None

def check_zip_conflicts(fname, label):
    fpath = os.path.join(G, fname)
    if not os.path.exists(fpath):
        return {'file': fname, 'label': label, 'error': 'NOT_FOUND'}
    
    sz_mb = os.path.getsize(fpath) / 1048576
    if sz_mb > 40:
        return {'file': fname, 'label': label, 'error': 'TOO_LARGE', 'size_mb': sz_mb}
    
    result = {
        'file': fname,
        'label': label,
        'size_mb': round(sz_mb, 1),
        'duplicate_files': [],
        'duplicate_skills': [],
        'port_conflicts': [],
        'config_conflicts': [],
        'status': 'OK'
    }
    
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            names = z.namelist()
            result['total_files'] = len(names)
            
            # Check file name conflicts
            for n in names:
                base = os.path.basename(n)
                if base.lower() in e_files:
                    result['duplicate_files'].append(n)
                
                # Check SKILL.md files
                if 'skill.md' in n.lower():
                    skill_name = n.split('/')[-2].lower() if '/' in n else ''
                    if skill_name in e_skills:
                        result['duplicate_skills'].append(skill_name)
            
            # Check port conflicts
            for n in names:
                ext = os.path.splitext(n)[1].lower()
                if ext in ['.py', '.ts', '.json', '.yaml', '.yml', '.env', '.conf']:
                    try:
                        content = z.read(n).decode('utf-8', errors='replace')
                        for pat in e_port_patterns:
                            matches = re.findall(pat, content, re.IGNORECASE)
                            for m in matches:
                                p = int(m)
                                if 3000 <= p <= 9999 and p in e_ports_found:
                                    result['port_conflicts'].append((n, p))
                    except:
                        pass
            
            # Check package.json / pyproject.toml deps conflicts
            pkg_files = [n for n in names if n.endswith('package.json')]
            for p in pkg_files:
                try:
                    content = z.read(p).decode('utf-8', errors='replace')
                    pkg = json.loads(content)
                    deps = list(pkg.get('dependencies', {}).keys()) + list(pkg.get('devDependencies', {}).keys())
                    result['config_conflicts'].extend(deps[:20])
                except:
                    pass
            
    except Exception as ex:
        result['error'] = str(ex)
    
    return result

# Run checks
for name, label, _ in targets:
    # Find actual filename
    actual = find_zip(label)
    if not actual:
        # Try from name
        if name in viet_name_map:
            actual = viet_name_map[name] + '.zip' if not viet_name_map[name].endswith('.zip') else viet_name_map[name]
        if not actual:
            # Just use name directly
            actual = name if name.endswith('.zip') else name + '.zip'
    
    result = check_zip_conflicts(actual, label)
    
    if result.get('error') == 'NOT_FOUND':
        print(f"[SKIP] {label} - not found in G:\\Ai")
        continue
    if result.get('error') == 'TOO_LARGE':
        print(f"[SKIP] {label} - too large ({result['size_mb']:.0f}MB) - need manual")
        continue
    
    conflicts = []
    if result['duplicate_files']:
        conflicts.append(f"trung file({len(result['duplicate_files'])})")
    if result['duplicate_skills']:
        conflicts.append(f"trung skill({result['duplicate_skills']})")
    if result['port_conflicts']:
        conflicts.append(f"xung dot port({len(result['port_conflicts'])})")
    if result['config_conflicts']:
        conflicts.append(f"config({len(result['config_conflicts'])} deps)")
    
    status = "✅ AN TOAN" if not conflicts else f"⚠️ {', '.join(conflicts)}"
    
    print(f"[{status}] {label}")
    print(f"  File: {result['file']} ({result['size_mb']}MB, {result.get('total_files',0)} files)")
    if result['duplicate_files']:
        print(f"  - Trung file: {result['duplicate_files'][:5]}")
    if result['duplicate_skills']:
        print(f"  - Trung skill: {result['duplicate_skills']}")
    if result['port_conflicts']:
        for fname, port in result['port_conflicts'][:3]:
            print(f"  - Port {port} conflict in {fname}")
    print()

# === Also check config conflicts
print("\n[PORT] Cac port dang dung trong E:")
ports_sorted = sorted(e_ports_found)
print(f"  {[p for p in ports_sorted if 3000 <= p <= 9999][:20]}")
print(f"  (and more...)")

print("\n[SKILLS] Cac skill hien co trong E:")
print(f"  {sorted(e_skills)}")
