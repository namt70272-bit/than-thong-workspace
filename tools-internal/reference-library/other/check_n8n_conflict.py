#!/usr/bin/env python3
"""Kiểm tra xung đột khi nhập G:\Ai các file liên quan n8n vào E."""
import os, sys, zipfile, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
G = r'G:\Ai'

# 1) Files cần kiểm tra
targets = {
    'n8n.zip': 'n8n source code',
    'n8n-workflow-automation-1.0.0.zip': 'n8n workflow skill',
    'Cognee-n8n.zip': 'n8n community node - Cognee memory',
}

print("=" * 60)
print("KIEM TRA XUNG DOT: G:\\Ai -> E:\\ workspace")
print("=" * 60)

# 2) Kiểm tra file đã tồn tại
print("\n[1] File co ten trung trong workspace?")
findings = []
for fname in targets:
    fpath = os.path.join(G, fname)
    if not os.path.exists(fpath):
        print(f"  - {fname}: KHONG TON TAI trong G:\\Ai (bo qua)")
        continue
    
    # Check duplicates in E
    e_dupes = []
    for root, dirs, files in os.walk(E):
        for f in files:
            if f.lower() == fname.lower():
                e_dupes.append(os.path.relpath(os.path.join(root, f), E))
    
    if e_dupes:
        findings.append({"file": fname, "type": "duplicate_name", "detail": "Trung ten trong E"})
        print(f"  - {fname}: ⚠️ TRUNG TEN trong E:")
        for d in e_dupes:
            print(f"      {d}")
    else:
        print(f"  - {fname}: ✓ Khong trung ten")

# 3) Kiểm tra nội dung từng file
print("\n[2] Kiem tra noi dung file (có xung đột không):")

# Check n8n.zip
n8n_path = os.path.join(G, 'n8n.zip')
n8n_info = {"type": "source", "files": 0, "conflicts": []}
if os.path.exists(n8n_path):
    try:
        with zipfile.ZipFile(n8n_path, 'r') as z:
            names = z.namelist()
            n8n_info["files"] = len(names)
            # Check first-level dirs
            dirs = set()
            for n in names:
                parts = n.split('/')
                if len(parts) > 1:
                    dirs.add(parts[0])
            n8n_info["top_dirs"] = list(dirs)
            print(f"  - n8n.zip: {len(names)} files, thu muc goc: {sorted(dirs)[:10]}")
            
            # Check conflict with n8n Docker
            docker_conflicts = [
                n for n in names 
                if 'docker' in n.lower() or 'dockerfile' in n.lower()
            ]
            if docker_conflicts:
                print(f"    ⚠️ Co {len(docker_conflicts)} file Docker (co the conflict voi n8n dang chay)")
            
            # Check for n8n-nodes that overlap with current n8n
            node_names = [
                n for n in names 
                if n.startswith('n8n-master/packages/nodes-base/nodes/') and n.endswith('.node.json')
            ]
            print(f"    📦 {len(node_names)} node definitions")
            
    except Exception as e:
        print(f"  - n8n.zip: LOI doc: {e}")

# Check small files
for fname, desc in targets.items():
    if fname == 'n8n.zip':
        continue
    fpath = os.path.join(G, fname)
    if not os.path.exists(fpath):
        continue
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            names = z.namelist()
            print(f"  - {fname}: {len(names)} files, {desc}")
            
            # Check for script/executable files
            exts = set()
            for n in names:
                exts.add(os.path.splitext(n)[1].lower())
            risky_exts = [e for e in exts if e in ['.exe', '.bat', '.ps1', '.sh', '.py', '.js']]
            if risky_exts:
                print(f"    ⚠️ Co file thuc thi: {risky_exts}")
            
            # Check for config that might conflict
            config_files = [n for n in names if 'config' in n.lower() or '.env' in n.lower()]
            if config_files:
                print(f"    ⚠️ Co config file: {config_files[:5]}")
    except Exception as e:
        print(f"  - {fname}: LOI: {e}")

# 4) Kiểm tra port/dependency xung đột
print("\n[3] Kiem tra dependency xung dot:")
# Package.json check
for fname in targets:
    fpath = os.path.join(G, fname)
    if not os.path.exists(fpath):
        continue
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            wf_names = [n for n in z.namelist() if n.endswith('package.json')]
            for pkg in wf_names:
                try:
                    content = z.read(pkg).decode('utf-8')
                    pkg_data = json.loads(content)
                    deps = pkg_data.get('dependencies', {})
                    dev_deps = pkg_data.get('devDependencies', {})
                    all_deps = {**deps, **dev_deps}
                    if all_deps:
                        print(f"  - {fname} deps ({pkg}): {', '.join(all_deps.keys())[:200]}")
                except:
                    pass
    except:
        pass

# 5) Check n8n Docker state
print("\n[4] Kiem tra n8n Docker dang chay:")
import subprocess
r = subprocess.run(['docker', 'ps', '-a', '--filter', 'name=n8n', '--format', '{{.Names}} {{.Status}}'],
                   capture_output=True, text=True, timeout=5)
if r.stdout.strip():
    print(f"  - n8n container: {r.stdout.strip()}")
    print(f"  ⚠️ Canh bao: n8n.zip co the conflict neu copy node definition vao container")
else:
    print(f"  - n8n container: Khong chay")

# 6) Kết luận
print("\n" + "=" * 60)
print("KET LUAN")
print("=" * 60)

risks = []

# Duplicate risk
if any(f.get("type") == "duplicate_name" for f in findings):
    risks.append("- Ten file trung: co the ghi de neu copy truc tiep")

risks.append("- n8n.zip la source code (33MB) - khong nen copy nguyen vao E")
risks.append("- n8n-workflow-automation la skill doc - an toan, co the lay SKILL.md")
risks.append("- Cognee-n8n la community node - can build + cai vao n8n container")
risks.append("- n8n-container dang chay o version 2.20.7-exp.0 - source zipped co the la version khac")

print("\n* Xung dot nghiem trong:")
for r in risks:
    print(f"  {r}")

print("\n* De xuat:")
print("  1. n8n-workflow-automation: lay SKILL.md + _meta.json (3KB) - an toan")
print("  2. Cognee-n8n: lay TypeScript node code de tham khao (khong can build)")
print("  3. n8n.zip: KHONG COPY nguyen - chi mo xem co node/feature nao can")
print("  4. Tat ca luu vao E:/review/candidate/ truoc, khong no vao runtime")
