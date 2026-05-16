#!/usr/bin/env python3
"""Deep analysis of 2,434 reference files — extract knowledge by category"""
import os, sys, json, re
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REF = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\reference-library")

print("=" * 70)
print("DEEP ANALYSIS: 2,434 REFERENCE FILES")
print("=" * 70)

category_findings = {}

for cat in sorted(os.listdir(str(REF))):
    cat_path = REF / cat
    if not cat_path.is_dir():
        continue
    
    files = sorted(cat_path.rglob("*.py"))
    if not files:
        continue
    
    # Get file sizes
    sizes = sorted([(f.stat().st_size, f.name) for f in files], reverse=True)
    
    # Sample top 5 files for content analysis
    top_files = []
    for f in files:
        if len(top_files) >= 5:
            break
        if f.stat().st_size > 2000 and f.stat().st_size < 50000:
            top_files.append(f)
    
    # Extract key imports, classes, and functions from top files
    imports = Counter()
    classes = []
    functions = []
    key_topics = Counter()
    
    for f in top_files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            lines = content.split("\n")
            
            for line in lines[:200]:
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    imports[line.split()[1].split(".")[0]] += 1
                if line.startswith("class "):
                    classes.append(line.split("(")[0].split(":")[0].replace("class ", "").strip())
                if line.startswith("def "):
                    func = line.split("(")[0].replace("def ", "").strip()
                    if func != "__init__":
                        functions.append(func)
        except:
            pass
    
    # Determine key capabilities
    capabilities = set()
    for f in files:
        name = f.name.lower()
        if "train" in name: capabilities.add("Training")
        if "predict" in name or "infer" in name: capabilities.add("Inference")
        if "search" in name: capabilities.add("Search")
        if "embed" in name: capabilities.add("Embedding")
        if "download" in name or "fetch" in name or "crawl" in name: capabilities.add("Data Collection")
        if "backtest" in name or "backtest" in f.read_text(errors="replace", encoding="utf-8")[:2000].lower(): capabilities.add("Backtesting")
        if "api" in name or "server" in name: capabilities.add("API Server")
        if "agent" in name: capabilities.add("Agent")
        if "chat" in name or "llm" in name: capabilities.add("LLM")
        if "memory" in name: capabilities.add("Memory")
        if "vector" in name: capabilities.add("Vector Store")
    
    category_findings[cat] = {
        "file_count": len(files),
        "total_size_kb": sum(f.stat().st_size for f in files) // 1024,
        "top_imports": [k for k, v in imports.most_common(5)],
        "sample_classes": classes[:5],
        "sample_functions": functions[:5],
        "capabilities": sorted(capabilities),
        "top_files": [(name, sz // 1024) for sz, name in sizes[:5]],
    }

# === GENERATE REPORT ===
print("\n\n")

for cat, info in sorted(category_findings.items(), key=lambda x: -x[1]["file_count"]):
    print(f"{'─' * 60}")
    print(f"📁 {cat} ({info['file_count']} files, {info['total_size_kb']}KB)")
    print(f"{'─' * 60}")
    
    print(f"   CAPABILITIES: {', '.join(info['capabilities'][:8])}")
    if info["top_imports"]:
        print(f"   KEY IMPORTS: {', '.join(info['top_imports'])}")
    if info["sample_classes"]:
        print(f"   CLASSES: {', '.join(info['sample_classes'])}")
    if info["sample_functions"]:
        print(f"   FUNCTIONS: {', '.join(info['sample_functions'][:8])}")
    
    print(f"   TOP FILES:")
    for name, sz in info["top_files"][:3]:
        print(f"     [{sz}KB] {name}")
    print()

# === WRITE COMPREHENSIVE REPORT ===
REVIEW = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\review")
report_path = REVIEW / "REFERENCE-KNOWLEDGE-REPORT.md"
with open(str(report_path), "w", encoding="utf-8") as f:
    f.write("# 📚 REFERENCE KNOWLEDGE REPORT\n\n")
    f.write(f"> Generated from 2,434 files across 21 categories\n")
    f.write(f"> Date: 2026-05-14\n\n")
    
    total_kb = sum(info["total_size_kb"] for info in category_findings.values())
    f.write(f"**Total:** {sum(info['file_count'] for info in category_findings.values())} files, {total_kb}KB\n\n")
    
    f.write("## Category Index\n\n")
    for cat, info in sorted(category_findings.items(), key=lambda x: -x[1]["file_count"]):
        f.write(f"- [{cat}](#{cat.lower().replace('/', '-').replace('_', '-').replace(' ', '-')}): {info['file_count']} files, {', '.join(info['capabilities'][:5])}\n")
    
    f.write("\n---\n\n")
    
    for cat, info in sorted(category_findings.items(), key=lambda x: -x[1]["file_count"]):
        f.write(f"## {cat}\n\n")
        f.write(f"- **Files:** {info['file_count']} | **Size:** {info['total_size_kb']}KB\n")
        f.write(f"- **Capabilities:** {', '.join(info['capabilities'][:8])}\n")
        f.write(f"- **Key Imports:** {', '.join(info['top_imports'][:5])}\n")
        if info["sample_classes"]:
            f.write(f"- **Notable Classes:** `{'`, `'.join(info['sample_classes'][:5])}`\n")
        if info["sample_functions"]:
            f.write(f"- **Notable Functions:** `{'`, `'.join(info['sample_functions'][:8])}`\n")
        f.write(f"\n**Top Files:**\n")
        for name, sz in info["top_files"][:3]:
            f.write(f"- [{sz}KB] {name}\n")
        f.write("\n---\n\n")

print(f"Report saved: {report_path}")
print("DONE")
