#!/usr/bin/env python3
"""LOC DANH SACH CHI LAY NHUNG FILE MOI HOAN TOAN (khong trung gi)"""
import zipfile, os, sys, json, re, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

G = r'G:\Ai'
E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'

def sig(content):
    return hashlib.md5(content[:600].encode()).hexdigest()[:12]

# === E index ===
e_file_index = {}
e_skill_names = set()
e_readme_sigs = set()

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        lname = f.lower()
        if lname not in e_file_index:
            e_file_index[lname] = set()
        e_file_index[lname].add(os.path.join(rel, f).lower())

skdir = os.path.join(E, 'skills')
if os.path.exists(skdir):
    for s in os.listdir(skdir):
        if os.path.isdir(os.path.join(skdir, s)):
            e_skill_names.add(s.lower())

for root, dirs, files in os.walk(E):
    for f in files:
        if f.lower() == 'readme.md':
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                    e_readme_sigs.add(sig(fh.read(600)))
            except: pass

# === Skip these ===
SKIP_LIST = [
    'davinci-resolve', 'powershell-7.6', 'camoufox', 'graillon', 'vbcable', 'voicemeeter',
    'marktext', 'outline-apps', 'seelen-ui', 'win10-gaming', 'winhance', 'winutil', 'sophia',
    'whisper-bin-x64', 'whispergui', 'comtypes-1.4.16', 'gsnapwin64',
]

zips = sorted([f for f in os.listdir(G) if f.endswith('.zip')])

# === Already extracted / from n8n ===
already_done = ['n8n.zip', 'n8n-ServerChan.zip', 'n8n-workflow-automation-1.0.0.zip', 'Cognee-n8n.zip']

final_safe = []
final_conflict = []
final_skip = []
final_minor = []

for fname in zips:
    fname_lower = fname.lower()
    
    # Skip non-useful
    if any(s in fname_lower for s in SKIP_LIST):
        final_skip.append((fname, 'không liên quan (driver/audio/video)'))
        continue
    
    fpath = os.path.join(G, fname)
    sz = os.path.getsize(fpath) / 1048576
    
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            names = z.namelist()
            
            # -- Check real conflicts --
            has_skill_conflict = False
            has_readme_conflict = False
            
            for n in names:
                if 'skill.md' in n.lower():
                    parts = n.split('/')
                    for i, p in enumerate(parts):
                        if p == 'skills' and i+1 < len(parts):
                            sname = parts[i+1].lower()
                            if sname in e_skill_names:
                                has_skill_conflict = True
                                break
                    if has_skill_conflict: break
            
            if not has_skill_conflict:
                for n in names:
                    if n.lower().endswith('readme.md'):
                        try:
                            c = z.read(n).decode('utf-8', errors='replace')
                            s = sig(c)
                            if s in e_readme_sigs:
                                has_readme_conflict = True
                        except: pass
            
            # Categorize
            if has_skill_conflict:
                # Show which skills
                conflict_skills = []
                for n in names:
                    if 'skill.md' in n.lower():
                        parts = n.split('/')
                        for i, p in enumerate(parts):
                            if p == 'skills' and i+1 < len(parts):
                                sname = parts[i+1].lower()
                                if sname in e_skill_names:
                                    conflict_skills.append(parts[i+1])
                final_conflict.append((fname, sz, len(names), conflict_skills, 'TRÙNG SKILL'))
            elif has_readme_conflict and len(names) <= 10:
                # Small file, only README dup → likely same project
                final_conflict.append((fname, sz, len(names), [], 'TRÙNG README (cùng project?)'))
            elif sz > 100:
                final_minor.append((fname, sz, len(names), 'QUÁ LỚN (>100MB)'))
            elif names == 0 or len(names) <= 2:
                final_minor.append((fname, sz, len(names), 'RỖNG / QUÁ NHỎ'))
            else:
                # Count code
                ts_cnt = len([n for n in names if n.endswith('.ts') and 'node_module' not in n.lower()])
                py_cnt = len([n for n in names if n.endswith('.py') and 'node_module' not in n.lower()])
                skill_cnt = len([n for n in names if 'skill.md' in n.lower()])
                final_safe.append((fname, sz, len(names), ts_cnt, py_cnt, skill_cnt))
                
    except Exception as ex:
        final_minor.append((fname, sz, 0, f'LỖI DOC: {str(ex)[:30]}'))

# === Print ===
print("=" * 80)
print(f"DANH SÁCH LỌC: G:\\Ai → Có thể lấy vào hệ thống")
print("=" * 80)

print(f"\n{'=' * 80}")
print(f"✅ CÓ THỂ LẤY ({len(final_safe)} files)")
print(f"{'=' * 80}")
for fname, sz, cnt, ts, py, sk in sorted(final_safe, key=lambda x: x[1]):
    code = ''
    if ts: code += f' {ts}.ts'
    if py: code += f' {py}.py'
    if sk: code += f' {sk}skill'
    print(f"  [{sz:6.1f}MB] {fname.replace('.zip',''):45s} [{cnt:5d} files{code}]")

print(f"\n{'=' * 80}")
print(f"❌ KHÔNG LẤY VÌ TRÙNG ({len(final_conflict)} files)")
print(f"{'=' * 80}")
for fname, sz, cnt, conflicts, reason in sorted(final_conflict, key=lambda x: x[1]):
    conflict_str = f" ({', '.join(conflicts[:3])})" if conflicts else ''
    print(f"  [{sz:6.1f}MB] {fname.replace('.zip',''):45s} {reason}{conflict_str}")

print(f"\n{'=' * 80}")
print(f"⏩ BỎ QUA ({len(final_skip)+len(final_minor)} files)")
print(f"{'=' * 80}")
for fname, reason in final_skip:
    print(f"  SKIP {fname.replace('.zip',''):45s} {reason}")
for fname, sz, cnt, reason in final_minor:
    print(f"  [{sz:6.1f}MB] {fname.replace('.zip',''):45s} {reason}")

# === SAVE ===
with open(os.path.join(E, 'review', 'G-Ai-loc-safe.md'), 'w', encoding='utf-8') as f:
    f.write("# G:\\Ai — Danh sách có thể lấy vào hệ thống\n\n")
    f.write(f"**Tổng:** {len(final_safe)} file có thể lấy, {len(final_conflict)} file trùng (bỏ), {len(final_skip)+len(final_minor)} file bỏ qua\n\n")
    
    f.write(f"## ✅ CÓ THỂ LẤY ({len(final_safe)} files)\n\n")
    f.write("| File | MB | Files | .ts | .py | Skills |\n|------|----|-------|-----|-----|--------|\n")
    for fname, sz, cnt, ts, py, sk in sorted(final_safe, key=lambda x: x[1]):
        f.write(f"| {fname.replace('.zip','')} | {sz:.1f} | {cnt} | {ts} | {py} | {sk} |\n")
    
    f.write(f"\n## ❌ KHÔNG LẤY — trùng ({len(final_conflict)} files)\n\n")
    for fname, sz, cnt, conflicts, reason in sorted(final_conflict, key=lambda x: x[1]):
        conflict_str = f" ({', '.join(conflicts[:3])})" if conflicts else ''
        f.write(f"- {fname.replace('.zip','')} [{sz:.1f}MB] {reason}{conflict_str}\n")
    
    f.write(f"\n## ⏩ BỎ QUA ({len(final_skip)+len(final_minor)} files)\n\n")
    for fname, reason in final_skip:
        f.write(f"- {fname.replace('.zip','')} — {reason}\n")
    for fname, sz, cnt, reason in final_minor:
        f.write(f"- {fname.replace('.zip','')} [{sz:.1f}MB] — {reason}\n")

print(f"\n\nLưu tại: review/G-Ai-loc-safe.md")
print("HOÀN THÀNH.")
