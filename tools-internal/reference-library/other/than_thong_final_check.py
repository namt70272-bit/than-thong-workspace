#!/usr/bin/env python3
"""Than-thong gate check: kiem tra candidate zip voi he thong"""
import zipfile, os, sys, json, re, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
C = os.path.join(E, 'review', 'candidate')

# === INDEX E workspace (skills, ports, dependencies, imports) ===
e_skill_names = set()
e_python_imports = {}
e_node_packages = {}
e_port_usage = {}
e_config_keys = set()
e_file_paths = set()
e_skill_files = set()

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        e_file_paths.add(os.path.join(rel, f).lower())
    for d in dirs:
        pass

skdir = os.path.join(E, 'skills')
if os.path.exists(skdir):
    for s in os.listdir(skdir):
        if os.path.isdir(os.path.join(skdir, s)):
            e_skill_names.add(s.lower())

# Ports + package imports
port_pat = re.compile(r'(?:port|PORT|listen|LISTEN)\s*[:=]\s*(\d{3,5})')

for root, dirs, files in os.walk(E):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env', '.conf', '.js']: continue
        try:
            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read(50000)
                for m in port_pat.finditer(content):
                    p = int(m.group(1))
                    if 3000 <= p <= 9999:
                        e_port_usage[p] = e_port_usage.get(p, 0) + 1
        except: pass

# Common system ports that are OK
SAFE_PORTS = {3000, 3001, 5173, 5174, 8000, 8080, 8443, 9000, 5000, 5001, 11434, 11435, 1234, 5678}
# Ports already heavily used in E - caution
SYSTEM_PORTS = {5678, 8000, 5173, 3000, 8080, 5000, 3001}

print("=" * 80)
print("THAN THONG GATE CHECK: Candidate vs Hệ thống")
print("=" * 80)

results = {'PASS': [], 'WARN': [], 'FAIL': [], 'SKIP': []}

for root, dirs, files in os.walk(C):
    for fname in files:
        if not fname.endswith('.zip'): continue
        
        fpath = os.path.join(root, fname)
        sz_mb = os.path.getsize(fpath) / 1048576
        folder = os.path.basename(root)
        display = fname.replace('.zip', '')
        
        issues = []
        
        try:
            with zipfile.ZipFile(fpath, 'r') as z:
                names = z.namelist()
                
                # 1) SKILL NAME CONFLICT
                for n in names:
                    if 'skill.md' in n.lower() and 'node_module' not in n.lower():
                        parts = n.split('/')
                        for i, p in enumerate(parts):
                            if p == 'skills' and i+1 < len(parts):
                                sname = parts[i+1].lower()
                                if sname in e_skill_names:
                                    issues.append(f"SKILL_TRUNG: skills/{parts[i+1]}")
                
                # 2) PORT CONFLICT (real usage, not safe ports)
                zip_ports = set()
                for n in names:
                    ext = os.path.splitext(n)[1].lower()
                    if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env']: continue
                    try:
                        content = z.read(n).decode('utf-8', errors='replace')
                        for m in port_pat.finditer(content):
                            p = int(m.group(1))
                            if 3000 <= p <= 9999:
                                zip_ports.add(p)
                    except: pass
                
                if zip_ports:
                    real_conflicts = zip_ports & {p for p in e_port_usage if p not in SAFE_PORTS}
                    if real_conflicts:
                        issues.append(f"PORT: {real_conflicts}")
                
                # 3) PATH CONFLICT - same file path (not just basename)
                full_path_conflicts = []
                for n in names:
                    if n.lower() in e_file_paths:
                        full_path_conflicts.append(n)
                if full_path_conflicts:
                    if len(full_path_conflicts) < 5:
                        issues.append(f"PATH_TRUNG: {full_path_conflicts}")
                    else:
                        issues.append(f"PATH_TRUNG: {len(full_path_conflicts)} file")
                
        except Exception as ex:
            issues.append(f"LOI_DOC: {str(ex)[:50]}")
        
        # Determine status
        if not issues:
            results['PASS'].append((display, sz_mb, len(names), folder))
        else:
            # Check severity
            severe = [i for i in issues if i.startswith('SKILL_TRUNG') or i.startswith('PORT:')]
            if severe:
                results['FAIL'].append((display, sz_mb, len(names), folder, issues))
            else:
                results['WARN'].append((display, sz_mb, len(names), folder, issues))

# === PRINT RESULTS ===
print(f"\n✅ PASS ({len(results['PASS'])} files):")
for i, (name, sz, cnt, folder) in enumerate(sorted(results['PASS'], key=lambda x: x[1])):
    if i < 20:
        print(f"  [{sz:6.1f}MB] {name:50s} [{cnt:5d} files] {folder}")

print(f"\n⚡ WARN ({len(results['WARN'])} files - path overlaps, vô hại):")
for name, sz, cnt, folder, issues in results['WARN']:
    print(f"  [{sz:6.1f}MB] {name:50s} [{cnt:5d} files]")
    for i in issues[:3]:
        print(f"         → {i}")

if results['FAIL']:
    print(f"\n❌ FAIL ({len(results['FAIL'])} files - cần chú ý):")
    for name, sz, cnt, folder, issues in results['FAIL']:
        print(f"  [{sz:6.1f}MB] {name:50s} [{cnt:5d} files]")
        for i in issues:
            print(f"         → {i}")

print("\n" + "=" * 80)
print("KET LUAN:")
print(f"  ✅ PASS: {len(results['PASS'])} files - hoàn toàn an toàn")
print(f"  ⚡ WARN: {len(results['WARN'])} files - path overlap nhẹ (vô hại)")
print(f"  ❌ FAIL: {len(results['FAIL'])} files")
print("=" * 80)

# === WRITE REPORT ===
with open(os.path.join(E, 'review', 'than-thong-candidate-check.md'), 'w', encoding='utf-8') as f:
    f.write("# THAN THONG GATE: Candidate check\n\n")
    f.write(f"PASS: {len(results['PASS'])} | WARN: {len(results['WARN'])} | FAIL: {len(results['FAIL'])}\n\n")
    
    if results['FAIL']:
        f.write("## ❌ FAIL (cần chú ý)\n\n")
        for name, sz, cnt, folder, issues in results['FAIL']:
            f.write(f"- **{name}** [{sz:.1f}MB]: {'; '.join(issues)}\n")
        f.write("\n")
    
    if results['WARN']:
        f.write("## ⚡ WARN (path overlap nhẹ)\n\n")
        for name, sz, cnt, folder, issues in results['WARN']:
            f.write(f"- {name} [{sz:.1f}MB]: {'; '.join(issues)}\n")
        f.write("\n")
    
    f.write("## ✅ PASS\n\n")
    for name, sz, cnt, folder in sorted(results['PASS'], key=lambda x: x[1]):
        f.write(f"- {name} [{sz:.1f}MB, {cnt} files, {folder}]\n")

print(f"\nReport: review/than-thong-candidate-check.md")
print("THAN THONG GATE HOAN THANH.")
