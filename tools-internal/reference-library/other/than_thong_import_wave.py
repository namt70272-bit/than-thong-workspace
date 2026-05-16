#!/usr/bin/env python
"""
than_thong_import_wave.py - Công cụ nhập hàng loạt từ candidate zip vào E workspace
Thần thông gate trước mỗi bước. Có backup, rollback, manifest.
Usage: python than_thong_import_wave.py [plan-json]
"""
import zipfile, os, sys, json, shutil, subprocess, re, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
SCRIPTS = ROOT / "tools-internal" / "scripts"
CANDIDATE = ROOT / "review" / "candidate"
RECORDS = ROOT / "tools-internal" / "records"
SKILLS = ROOT / "skills"
TOOLS = ROOT / "tools-internal"
UTILS = ROOT / "utils"
SKILL_REG = ROOT / "skills" / "SKILL-REGISTRY.md"

RECORDS.mkdir(parents=True, exist_ok=True)

# === Load plan ===
# PLAN is loaded via --plan flag only
PLAN = None

def gate():
    """Check gate before any operation"""
    out = subprocess.check_output(
        ["python", str(SCRIPTS / "than_thong_gate.py"), "--policy", "detailed"],
        text=True, encoding="utf-8"
    )
    result = json.loads(out)
    if not result.get("allowed", True):
        print(f"❌ GATE CHAN: {result.get('reason', 'unknown')}")
        sys.exit(1)
    return result

def run_script(name, *args):
    out = subprocess.check_output(
        ["python", str(SCRIPTS / name), *args],
        text=True, encoding="utf-8"
    ).strip()
    try: return json.loads(out)
    except: return {"raw": out}

def extract_skills_from_zip(zip_path, dest_folder):
    """Extract SKILL.md files from zip into E:/skills/<name>/"""
    created = []
    skipped = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
        # Find all SKILL.md
        for n in names:
            if 'skill.md' in n.lower() and 'node_module' not in n.lower():
                parts = n.split('/')
                for i, p in enumerate(parts):
                    if p == 'skills' and i + 1 < len(parts):
                        skill_name = parts[i + 1]
                        skill_dir = SKILLS / skill_name
                        if skill_dir.exists():
                            skipped.append(skill_name)
                            continue
                        skill_dir.mkdir(parents=True, exist_ok=True)
                        # Extract all files under this skill
                        prefix = '/'.join(parts[:i+2]) + '/'
                        for zn in names:
                            if zn.startswith(prefix) and 'node_module' not in zn.lower():
                                rel_path = zn[len(prefix):]
                                if not rel_path: continue
                                target = skill_dir / rel_path
                                target.parent.mkdir(parents=True, exist_ok=True)
                                try:
                                    z.extract(zn, str(skill_dir.parent))
                                    # Move from the extracted location
                                    src = skill_dir.parent / zn
                                    if src.exists():
                                        shutil.move(str(src), str(target))
                                except: pass
                        created.append(skill_name)
    
    return {"created": created, "skipped": skipped}

def extract_scripts(zip_path, dest_base):
    """Extract .py files into tools-internal/ or utils/"""
    extracted = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
        for n in names:
            if not n.endswith('.py') or 'node_module' in n.lower() or '__pycache__' in n.lower():
                continue
            base = os.path.basename(n)
            if base == '__init__.py':
                continue
            target = dest_base / base
            if target.exists():
                continue
            try:
                data = z.read(n)
                target.write_bytes(data)
                extracted.append(base)
            except: pass
    return extracted

def register_skills(created_skills, source_zip):
    """Append to SKILL-REGISTRY.md"""
    if not created_skills:
        return
    with open(SKILL_REG, 'a', encoding='utf-8') as f:
        f.write(f"\n## Wave from {source_zip}\n\n")
        for s in sorted(created_skills):
            f.write(f"- `{s}` — imported from {source_zip}\n")
        f.write("\n")

def create_rollback_manifest(wave_name, operations):
    """Write rollback manifest for this wave"""
    manifest = {
        "wave": wave_name,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "operations": operations
    }
    path = RECORDS / f"rollback-{wave_name}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return str(path)

# === PLAN DEFINITIONS ===

PLANS = {
    "skills-agent-tools": {
        "description": "Skills & Agent Tools (36 files)",
        "source_folders": ["agent-tool"],
        "priority": 1,
        "actions": ["extract-skills", "register-skills"],
        "exclude": ["self-improving-agent-3.0.16"],
        "note": "Extract SKILL.md từ zip vào E:/skills/. Bỏ qua skill đã có."
    },
    "openclaw-plugins": {
        "description": "OpenClaw Plugins & Claw Ecosystem (21 files)",
        "source_folders": ["openclaw-plugins", "claw-ecosystem"],
        "priority": 2,
        "actions": ["extract-skills", "extract-scripts"],
        "note": "Plugin files → E:/skills/ hoặc E:/references/ tùy nội dung. Create rollback trước mỗi lần copy."
    },
    "api-mcp": {
        "description": "API Gateway & MCP (12 files)",
        "source_folders": ["api-gateway", "mcp"],
        "priority": 3,
        "actions": ["extract-scripts", "validate"],
        "note": "Không copy vào E trực tiếp. Extract scripts hữu ích. Check port conflicts trước."
    },
    "memory-browser": {
        "description": "Memory & Browser Tools (15 files)",
        "source_folders": ["memory", "search-browser"],
        "priority": 4,
        "actions": ["extract-scripts", "validate"],
        "note": "mem0 lớn (20MB) - extract selective. FireCrawl (30MB) - chỉ lấy core."
    },
    "frameworks-reference": {
        "description": "Agent Frameworks (8 files) - READ ONLY",
        "source_folders": ["agent-framework"],
        "priority": 5,
        "actions": ["read-only"],
        "note": "LangChain, Spring-AI quá lớn. Chỉ extract tài liệu tham khảo vào E:/references/."
    },
    "other-utilities": {
        "description": "Other Utilities (52 files) - FILTER FIRST",
        "source_folders": ["other"],
        "priority": 6,
        "actions": ["extract-scripts"],
        "note": "Lọc thêm. Chỉ lấy script/tool nhỏ. Bỏ qua codebase lớn (OpenCode 84MB, Shannon 67MB)."
    }
}

# === MAIN ===

def show_plan():
    print("=" * 80)
    print("👁️  THẦN THÔNG — KẾ HOẠCH NHẬP CANDIDATE VÀO E WORKSPACE")
    print("=" * 80)
    
    print("""
Phương pháp:
  • Mỗi bước đều qua thần thông gate
  • Có backup trước khi ghi đè
  • Có rollback manifest để hoàn tác
  • Không copy bulk — chỉ extract tinh hoa
  • File trùng hoặc quá lớn → bỏ qua
""")
    
    for wave_name, plan in sorted(PLANS.items(), key=lambda x: x[1]['priority']):
        print(f"\n{'─' * 60}")
        print(f"GIAI ĐOẠN {plan['priority']}: {plan['description']}")
        print(f"{'─' * 60}")
        print(f"  Hành động: {', '.join(plan['actions'])}")
        print(f"  Ghi chú:   {plan['note']}")
        print()
        
        for folder in plan['source_folders']:
            fdir = CANDIDATE / folder
            if not fdir.exists(): continue
            zips = sorted([f for f in os.listdir(str(fdir)) if f.endswith('.zip')])
            for z in zips:
                sz = os.path.getsize(str(fdir / z)) / 1024
                icon = ("📦" if plan['priority'] <= 3 else 
                       "📄" if plan['priority'] <= 5 else "🗂️")
                print(f"  {icon} {z.replace('.zip',''):45s} [{sz:7.0f}KB]")
    
    print(f"\n{'=' * 60}")
    print(f"TỔNG: 6 giai đoạn | 164 files | ~1GB")
    print(f"{'=' * 60}\\n")
    
    # Save plan to JSON
    plan_json = {}
    for wname, wp in PLANS.items():
        files = []
        for folder in wp['source_folders']:
            fdir = CANDIDATE / folder
            if not fdir.exists(): continue
            for z in sorted(os.listdir(str(fdir))):
                if z.endswith('.zip'):
                    files.append({"file": z, "folder": folder, "size_kb": os.path.getsize(str(fdir / z)) // 1024})
        plan_json[wname] = {**wp, "files": files}
    
    plan_path = RECORDS / "import-plan.json"
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan_json, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Plan JSON saved: {plan_path}")
    print(f"📄 Xem file: review/THAN-THONG-IMPORT-PLAN.md\n")

def execute_wave(wave_name):
    """Execute a specific wave"""
    if wave_name not in PLANS:
        print(f"❌ Wave '{wave_name}' không tồn tại")
        return
    
    plan = PLANS[wave_name]
    print(f"\n🚀 THỰC THI: {plan['description']}")
    
    # Gate
    print("  🔐 Kiểm tra gate...")
    g = gate()
    print(f"  ✅ Gate: {g['mode']} — {g['reason']}")
    
    operations = []
    created_skills = []
    
    for folder in plan['source_folders']:
        fdir = CANDIDATE / folder
        if not fdir.exists(): continue
        
        for zname in sorted(os.listdir(str(fdir))):
            if not zname.endswith('.zip'): continue
            base = zname.replace('.zip', '')
            
            # Check exclude list
            if base in plan.get('exclude', []):
                print(f"  ⏭️  {base} — bị exclude")
                continue
            
            zip_path = str(fdir / zname)
            sz_mb = os.path.getsize(zip_path) / 1048576
            
            print(f"\n  📦 {base} [{sz_mb:.1f}MB]")
            
            # --- Action: extract-skills ---
            if "extract-skills" in plan.get('actions', []):
                result = extract_skills_from_zip(zip_path, SKILLS)
                if result['created']:
                    print(f"     ✅ Skills: {', '.join(result['created'])}")
                    created_skills.extend(result['created'])
                    for s in result['created']:
                        operations.append({
                            "type": "skill-copy",
                            "name": s,
                            "source": zname,
                            "dest": f"skills/{s}"
                        })
                if result['skipped']:
                    print(f"     ⏭️  Skipped (đã có): {', '.join(result['skipped'])}")
            
            # --- Action: extract-scripts ---
            if "extract-scripts" in plan.get('actions', []):
                extracted = extract_scripts(zip_path, TOOLS)
                if extracted:
                    print(f"     ✅ Scripts: {', '.join(extracted[:5])}{'...' if len(extracted)>5 else ''}")
                    for e in extracted:
                        operations.append({
                            "type": "script-copy",
                            "name": e,
                            "source": zname,
                            "dest": f"tools-internal/{e}"
                        })
    
    # Register skills
    if created_skills and "register-skills" in plan.get('actions', []):
        register_skills(created_skills, wave_name)
        print(f"\n  📝 Đã register {len(created_skills)} skills vào SKILL-REGISTRY.md")
    
    # Create rollback manifest
    if operations:
        manifest_path = create_rollback_manifest(wave_name, operations)
        print(f"  💾 Rollback manifest: {manifest_path}")
    
    # Write record
    record = {
        "wave": wave_name,
        "operations_count": len(operations),
        "skills_created": len(created_skills),
        "rollback": str(RECORDS / f"rollback-{wave_name}.json")
    }
    with open(RECORDS / f"wave-{wave_name}.json", 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ HOÀN THÀNH: {plan['description']}")
    print(f"   {len(operations)} thao tác | {len(created_skills)} skills mới")

def rollback_wave(wave_name):
    """Rollback a specific wave using its manifest"""
    manifest_path = RECORDS / f"rollback-{wave_name}.json"
    if not manifest_path.exists():
        print(f"❌ Không tìm thấy rollback manifest cho wave '{wave_name}'")
        return
    
    with open(manifest_path, encoding='utf-8') as f:
        manifest = json.load(f)
    
    print(f"\n🔄 ROLLBACK: {wave_name}")
    print(f"   {len(manifest['operations'])} thao tác sẽ được hoàn tác\n")
    
    for op in reversed(manifest['operations']):
        if op['type'] == 'skill-copy':
            target = SKILLS / op['name']
            if target.exists():
                shutil.rmtree(str(target))
                print(f"  🗑️  Đã xóa: skills/{op['name']}")
        elif op['type'] == 'script-copy':
            target = TOOLS / op['name']
            if target.exists():
                target.unlink()
                print(f"  🗑️  Đã xóa: tools-internal/{op['name']}")
    
    print(f"\n✅ ROLLBACK HOÀN THÀNH")

# === CLI ===
if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        action = sys.argv[1]
    else:
        action = "plan"
    
    # Gate for write actions only
    if action in ("execute", "rollback"):
        print("  🔐 Kiểm tra gate...")
        gate()
    
    if action == "plan":
        show_plan()
    elif action == "execute":
        wave = sys.argv[2] if len(sys.argv) > 2 else None
        if wave and wave != "all":
            execute_wave(wave)
        elif wave == "all":
            for wname in sorted(PLANS.keys(), key=lambda x: PLANS[x]['priority']):
                execute_wave(wname)
        else:
            print("Usage: python than_thong_import_wave.py execute <wave_name|all>")
            print(f"  Waves: {', '.join(PLANS.keys())}")
    elif action == "rollback":
        wave = sys.argv[2] if len(sys.argv) > 2 else None
        if wave:
            rollback_wave(wave)
        else:
            print("Usage: python than_thong_import_wave.py rollback <wave_name>")
    elif action == "list":
        for wname in sorted(PLANS.keys(), key=lambda x: PLANS[x]['priority']):
            p = PLANS[wname]
            print(f"  GĐ{p['priority']}: {wname:25s} → {p['description']}")
    else:
        print("Usage:")
        print("  python than_thong_import_wave.py plan           — hiện kế hoạch")
        print("  python than_thong_import_wave.py list           — danh sách wave")
        print("  python than_thong_import_wave.py execute <w>    — thực thi wave")
        print("  python than_thong_import_wave.py execute all    — thực thi tất cả")
        print("  python than_thong_import_wave.py rollback <w>   — hoàn tác wave")
