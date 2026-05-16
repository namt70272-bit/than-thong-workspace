#!/usr/bin/env python
"""Doc va phan loai 3.135 skills tu E:\skill"""
import os, sys, json, re
from pathlib import Path
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SKILL_DIR = Path(r"E:\skill")
EXISTING = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\skills")
REVIEW = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\review")

existing_names = {d.name.lower() for d in EXISTING.iterdir() if d.is_dir()}

print("=" * 65)
print("DOC 3.135 SKILLS — PHAN LOAI THEO THE LOAI")
print("=" * 65)

# === Domain classification patterns ===
DOMAINS = {
    "Cloud/DevOps": ["aws-", "azure-", "gcp-", "cloudflare", "vercel", "netlify", "docker", "kubernetes", "deploy", "terraform", "ansible", "heroku", "digitalocean"],
    "AI/ML": ["ai-", "ml-", "machine-learning", "deep-learning", "llm", "gpt", "claude", "openai", "hugging", "transformers", "model-", "training", "inference", "embedding", "rag", "vector"],
    "Web Dev": ["react", "vue", "angular", "nextjs", "nuxt", "svelte", "html", "css", "javascript", "typescript", "frontend", "backend", "nodejs", "deno", "bun"],
    "Mobile": ["flutter", "react-native", "swift", "kotlin", "android", "ios", "expo", "mobile"],
    "Database": ["sql", "nosql", "mongodb", "postgres", "mysql", "redis", "duckdb", "sqlite", "dynamodb", "cosmosdb", "aurora", "cassandra"],
    "API/GraphQL": ["api-", "rest", "graphql", "apollo", "grpc", "webhook", "endpoint"],
    "Security": ["security", "auth", "oauth", "jwt", "encrypt", "vulnerability", "pen-test", "trail-of-bits", "audit", "compliance", "privacy"],
    "Design/UI": ["figma", "gsap", "animation", "ui-", "ux-", "design-system", "accessibility", "responsive"],
    "Marketing/SEO": ["seo", "marketing", "ads", "analytics", "content", "email-", "social-media", "quang-cao", "tiep-thi"],
    "Finance/Crypto": ["finance", "crypto", "coinbase", "binance", "blockchain", "trading", "defi", "nft"],
    "Testing/QA": ["test-", "testing", "qa-", "playwright", "cypress", "jest", "pytest", "coverage"],
    "Product/PM": ["product", "project-management", "agile", "scrum", "roadmap", "jira", "notion"],
    "Community/Social": ["cong-dong", "discord", "slack", "telegram", "reddit", "community"],
    "Automation": ["n8n", "automation", "workflow", "zapier", "ci-cd", "github-actions", "pipeline"],
    "n8n": ["n8n-", "n8n_"],
    "Other": [],
}

skill_data = []  # {name, group, display_name, domain, desc}

for group_dir in sorted(SKILL_DIR.iterdir()):
    if not group_dir.is_dir() or group_dir.name.startswith("_"):
        continue
    
    for root, dirs, files in os.walk(str(group_dir)):
        for f in files:
            if f.lower() != "skill.md":
                continue
            
            skill_name = os.path.basename(root)
            if skill_name.lower() in existing_names:
                continue
            
            # Read content
            try:
                content = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
                lines = content.strip().split("\n")
                display_name = lines[0].replace("#", "").strip() if lines else skill_name
                # Get description (first non-empty line after title)
                desc = ""
                for line in lines[1:]:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("---"):
                        desc = line[:150]
                        break
                    if line.startswith("description:"):
                        desc = line.split(":",1)[1].strip()[:150]
                        break
            except:
                display_name = skill_name
                desc = ""
            
            # Classify domain
            domain = "Other"
            for dom, kws in DOMAINS.items():
                if any(kw in skill_name.lower() for kw in kws):
                    domain = dom
                    break
            if domain == "Other":
                # Try from group name
                gn = group_dir.name.lower()
                if "claude" in gn: domain = "AI/ML"
                elif "azure" in gn: domain = "Cloud/DevOps"
                elif "openai" in gn: domain = "AI/ML"
                elif "flutter" in gn: domain = "Mobile"
                elif "bao-mat" in gn: domain = "Security"
                elif "tiep-thi" in gn or "quang-cao" in gn: domain = "Marketing/SEO"
                elif "n8n" in gn: domain = "n8n"
            
            skill_data.append({
                "name": skill_name,
                "display": display_name,
                "group": group_dir.name,
                "domain": domain,
                "desc": desc[:200],
                "path": os.path.relpath(root, str(SKILL_DIR))
            })

# === CLASSIFY GROUPS ===
group_domains = defaultdict(list)
for s in skill_data:
    group_domains[s["group"]].append(s["domain"])

# === PRINT BY DOMAIN ===
print(f"\nTong skills moi: {len(skill_data)}")
print()

domain_counts = Counter(s["domain"] for s in skill_data)
for dom, cnt in domain_counts.most_common():
    print(f"  {dom:25s}: {cnt:4d} skills")

# === PRINT DETAILED BY GROUP + DOMAIN ===
print(f"\n{'=' * 65}")
print("CHI TIET THEO NHOM + DOMAIN")
print("=" * 65)

for group, skills in sorted(group_domains.items(), key=lambda x: -len(x[1])):
    domain_dist = Counter(skills)
    top_dom = domain_dist.most_common(1)[0][0]
    print(f"\n📁 {group} ({len(skills)} skills)")
    for dom, cnt in domain_dist.most_common(3):
        bar = "█" * (cnt // 20)
        print(f"     {dom:20s}: {cnt:3d} {bar}")

# === TOP 50 MOST INTERESTING SKILLS ===
print(f"\n{'=' * 65}")
print("TOP 50 SKILLS DANG CHU Y NHAT")
print("=" * 65)

# Score: prefer skills with description, from important domains
priority_domains = {"AI/ML", "Security", "Cloud/DevOps", "Database", "API/GraphQL"}
scored = []
for s in skill_data:
    score = 0
    if s["domain"] in priority_domains: score += 3
    if len(s["desc"]) > 20: score += 2
    if s["name"] not in s["display"]: score += 1  # has custom display name
    scored.append((score, s))

scored.sort(key=lambda x: -x[0])

for i, (score, s) in enumerate(scored[:50]):
    print(f"\n  {i+1:2d}. [{s['domain']:15s}] {s['name']}")
    print(f"      {s['group']} | {s['display']}")
    if s["desc"]:
        print(f"      {s['desc'][:120]}")

# === WRITE REPORT ===
print(f"\n\nDang ghi bao cao...")

report_path = REVIEW / "ESKILL-COMPREHENSIVE-REPORT.md"
with open(str(report_path), "w", encoding="utf-8") as f:
    f.write(f"# 📚 Bao cao 3.135 Skills tu E:\\skill\n\n")
    f.write(f"**Tong cong: {len(skill_data)} skills moi, {len(domain_counts)} domains**\n\n")
    
    # Summary
    f.write("## Tong quan theo Domain\n\n")
    for dom, cnt in domain_counts.most_common():
        pct = cnt * 100 // len(skill_data)
        bar = "█" * (pct // 2)
        f.write(f"- {dom:25s}: {cnt:4d} skills ({pct}%) {bar}\n")
    
    f.write("\n---\n\n")
    
    # By Domain
    for dom in sorted(domain_counts.keys(), key=lambda d: -domain_counts[d]):
        skills_in_dom = [s for s in skill_data if s["domain"] == dom]
        if not skills_in_dom: continue
        f.write(f"## {dom} ({len(skills_in_dom)} skills)\n\n")
        f.write("| Skill | Group | Description |\n")
        f.write("|-------|-------|-------------|\n")
        for s in skills_in_dom[:50]:
            desc_clean = s["desc"].replace("|", "\\|")[:80]
            f.write(f"| `{s['name']}` | {s['group']} | {desc_clean} |\n")
        if len(skills_in_dom) > 50:
            f.write(f"| ... | ... | ({len(skills_in_dom)-50} skills nua trong {dom}) |\n")
        f.write("\n")
    
    f.write("\n---\n\n")
    f.write(f"*Generated: 2026-05-14 13:34*")

print(f"\n✅ Report: {report_path}")
print("DONE")
