#!/usr/bin/env python3
"""Doc sau n8n.zip - chon loc tinh hoa"""
import zipfile, os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

G = r'G:\Ai'
n8n_zip = os.path.join(G, 'n8n.zip')

with zipfile.ZipFile(n8n_zip, 'r') as z:
    names = z.namelist()
    
    print("="*60)
    print("DOC SAU n8n.zip - CHON LOC TINH HOA")
    print("="*60)
    
    # === 1) AI-Workflow-Builder ===
    print("\n[1] AI WORKFLOW BUILDER (457 files)")
    builder_files = [n for n in names if 'ai-workflow-builder.ee' in n]
    # Check READMEs
    readmes = [n for n in builder_files if 'readme' in n.lower() or n.endswith('.md')]
    for r in readmes:
        print(f"  - {r}")
    
    # Source files
    src_files = [n for n in builder_files if '/src/' in n and n.endswith('.ts')]
    print(f"  TypeScript sources: {len(src_files)}")
    for s in src_files:
        print(f"    {s}")
    
    # === 2) Nodes-Langchain ===
    print(f"\n[2] NODES-LANGCHAIN (749 files)")
    lc_dir = 'n8n-master/packages/@n8n/nodes-langchain/nodes/'
    lc_nodes = [n for n in names if n.startswith(lc_dir) and n.endswith('.node.ts')]
    for n in lc_nodes[:40]:
        name = n.replace(lc_dir, '').split('/')[0]
        print(f"  - {name}/")
    if len(lc_nodes) > 40:
        print(f"  ... and {len(lc_nodes)-40} more")
    
    # === 3) AI templates ===
    print(f"\n[3] AI WORKFLOW TEMPLATES")
    templates = [n for n in names if 'templates/ai' in n.lower() and n.endswith('.json')]
    for t in templates:
        print(f"  - {t}")
    
    # === 4) n8n-workflow-generator skill ===
    print(f"\n[4] WORKFLOW GENERATOR SKILL")
    gen_files = [n for n in names if '.claude/skills/n8n-workflow-generator' in n]
    for g in gen_files:
        print(f"  - {g}")
    
    # === 5) n8n-code-creator skill ===
    print(f"\n[5] CODE CREATOR SKILL")
    code_creator = [n for n in names if '.claude/skills/n8n-code-creator' in n]
    for c in code_creator[:20]:
        print(f"  - {c}")
    if len(code_creator) > 20:
        print(f"  ... and {len(code_creator)-20} more")
    
    # === 6) Workflow SDK ===
    print(f"\n[6] WORKFLOW SDK (212 files)")
    sdk_src = [n for n in names if 'workflow-sdk/src' in n and n.endswith('.ts')]
    for s in sdk_src:
        print(f"  - {s}")
    
    # === 7) Task Runner ===
    print(f"\n[7] TASK RUNNER (43 files)")
    tr_src = [n for n in names if 'task-runner/src' in n and n.endswith('.ts')]
    for t in tr_src:
        print(f"  - {t}")
    
    # === 8) Claude Skills (full) ===
    print(f"\n[8] CLAUDE SKILLS INCLUDED")
    skills = set()
    for n in names:
        if '.claude/skills/' in n:
            parts = n.split('/')
            if len(parts) >= 4:
                skills.add(parts[3])
    for s in sorted(skills):
        print(f"  - {s}/")
    
# De xuat cu the
print("\n" + "="*60)
print("DE XUAT TRICH LOC TINH HOA")
print("="*60)

print("""
NEN LAY (khong conflict):
  - skills/n8n-workflow-generator/ -> skill thiet ke workflow AI
  - skills/n8n-code-creator/ -> skill tao node code
  - templates/ai-workflows/*.json -> workflow mau (basic-ai-chatbot...)
  - node-langchain/ -> tham khao cach implement AI node cho n8n
  - workflow-sdk/ -> SDK code cho n8n workflow
  - Cac README.md -> tai lieu tham khao

KHONG LAY:
  - Toan bo Docker/*containers/testing -> runtime env, khong can
  - editor-ui/ (2000 files) -> frontend, khong lien quan
  - node_modules/ -> dependencies, se pull lai khi build
  - test/ -> test spec, khong can cho production

DE XUAT TAO FILE MOI:
  1. skills/n8n-flow-builder.mjs -> tu AI workflow builder
  2. references/n8n-nodes-ai-guide.md -> tu langchain nodes doc
  3. templates/n8n-ai-workflows/ -> workflow JSON mau
  4. docs/n8n-task-runner.md -> tu task runner code
""")
