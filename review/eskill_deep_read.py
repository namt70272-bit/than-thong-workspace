import os, re, json, textwrap
from collections import defaultdict, Counter

ROOT = r"E:\skill"
WORKSPACE = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
WORKSPACE_SKILLS = os.path.join(WORKSPACE, "skills")
OUT = os.path.join(WORKSPACE, "review", "ESKILL-DEEP-READ.md")

TOP_SOURCE_MAP = {
    "02-Microsoft-Azure": ("Cloud/DevOps", "Azure"),
    "03-OpenAI": ("AI/ML", "OpenAI"),
    "10-Bao-Mat-Trail-of-Bits": ("Security", "Trail of Bits"),
    "15-Xac-Thuc-Auth0": ("Security", "Auth/OAuth"),
    "18-Hugging-Face": ("AI/ML", "HuggingFace"),
    "19-Netlify": ("Cloud/DevOps", "Netlify"),
    "32-Vercel-Nextjs": ("Cloud/DevOps", "Vercel"),
}

GROUP_SUBGROUP_ORDER = {
    "AI/ML": ["Claude Skills", "OpenAI", "HuggingFace", "Gemini", "FireCrawl", "LLM Tools", "Other AI/ML"],
    "Security": ["Auth/OAuth", "Security Audit", "Trail of Bits", "Better-Auth", "Other Security"],
    "Cloud/DevOps": ["Azure", "Terraform", "Vercel", "Netlify", "Docker", "Other Cloud/DevOps"],
}

HIGH_TRUST_SOURCES = {
    "01-Claude-Chinh-Thuc",
    "02-Microsoft-Azure",
    "03-OpenAI",
    "10-Bao-Mat-Trail-of-Bits",
    "15-Xac-Thuc-Auth0",
    "18-Hugging-Face",
    "19-Netlify",
    "32-Vercel-Nextjs",
}

STRONG_IMPORT_HINTS = {
    "deploy", "deployment", "auth", "oauth", "oidc", "jwt", "security", "audit", "threat", "vulnerability",
    "azure", "terraform", "docker", "container", "netlify", "vercel", "openai", "hugging", "gemini",
    "firecrawl", "llm", "rag", "embedding", "vector", "training", "fine", "fine-tune", "finetune", "monitoring",
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str) -> str:
    return normalize(text).replace(" ", "-")


def parse_frontmatter(text: str):
    fm = {}
    body = text
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
        if m:
            raw, body = m.group(1), m.group(2)
            for line in raw.splitlines():
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                fm[k.strip().lower()] = v.strip().strip('"')
    return fm, body


def clean_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = re.sub(r"^>+\s*", "", text, flags=re.M)
    text = re.sub(r"^[-*]\s+", "", text, flags=re.M)
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def first_sentences(text: str, n=2):
    text = clean_markdown(text)
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    picked = []
    for part in parts:
        part = part.strip()
        if len(part) < 20:
            continue
        picked.append(part)
        if len(picked) >= n:
            break
    if not picked and parts:
        picked = [parts[0].strip()]
    return " ".join(picked).strip()


def extract_description_and_summary(text: str, fm: dict):
    desc = fm.get("description", "").strip()
    fm_name = fm.get("name", "").strip()
    _, body = parse_frontmatter(text)
    raw_lines = body.splitlines()
    paras = []
    cur = []
    for line in raw_lines:
        if not line.strip():
            if cur:
                paras.append(" ".join(cur).strip())
                cur = []
            continue
        s = line.strip()
        if s.startswith("#"):
            if cur:
                paras.append(" ".join(cur).strip())
                cur = []
            paras.append(s)
            continue
        cur.append(s)
    if cur:
        paras.append(" ".join(cur).strip())

    summary_candidates = []
    for i, p in enumerate(paras):
        pl = p.lower()
        if pl.startswith("##") and any(k in pl for k in ["overview", "when to use", "purpose", "workflow", "what this skill", "what it", "use this skill"]):
            for q in paras[i+1:i+4]:
                if q.startswith("#"):
                    continue
                summary_candidates.append(q)
        elif not p.startswith("#"):
            summary_candidates.append(p)
    summary = ""
    for cand in summary_candidates:
        s = first_sentences(cand, 2)
        if len(s) >= 40:
            if normalize(s) != normalize(desc):
                summary = s
                break
    if not desc:
        for cand in summary_candidates:
            s = first_sentences(cand, 1)
            if s:
                desc = s
                break
    if not summary:
        summary = desc or fm_name or "Không rõ từ nội dung."
    return desc[:360], summary[:420]


def phrase_in(text, phrases):
    return any(p in text for p in phrases)


def token_hit(tokens, wanted):
    return any(t in tokens for t in wanted)


def classify(source, rel_path, skill_name, description):
    parts = rel_path.split(os.sep)
    parts_wo_source = parts[1:] if len(parts) > 1 else parts
    tail_norm = normalize(" ".join(parts_wo_source[-4:] + [skill_name]))
    source_norm = normalize(source)
    focus = normalize(" ".join([source] + parts_wo_source[-4:] + [skill_name]))
    tokens = set(focus.split())
    tail_tokens = set(tail_norm.split())

    if source in TOP_SOURCE_MAP:
        return TOP_SOURCE_MAP[source]

    if source == "01-Claude-Chinh-Thuc":
        if "gemini" in tail_tokens:
            return ("AI/ML", "Gemini")
        if "firecrawl" in tail_tokens:
            return ("AI/ML", "FireCrawl")
        if phrase_in(tail_norm, ["better auth"]) or ("better" in tail_tokens and "auth" in tail_tokens):
            return ("Security", "Better-Auth")
        if "hashicorp" in tail_tokens or "terraform" in tail_tokens:
            return ("Cloud/DevOps", "Terraform")
        if "azure" in tail_tokens:
            return ("Cloud/DevOps", "Azure")
        if token_hit(tail_tokens, {"security", "audit", "threat", "vulnerability"}):
            return ("Security", "Security Audit")
        if token_hit(tail_tokens, {"anthropic", "anthropics", "claude"}):
            return ("AI/ML", "Claude Skills")
        if token_hit(tail_tokens, {"llm", "embedding", "vector", "rag", "inference", "finetune", "tokenizer", "prompt"}):
            return ("AI/ML", "LLM Tools")
        return None

    # Security-first for strong exact patterns in path/name only
    if phrase_in(source_norm + " " + tail_norm, ["trail of bits", "trail-of-bits"]):
        return ("Security", "Trail of Bits")
    if phrase_in(tail_norm, ["better auth"]) or ("better" in tail_tokens and "auth" in tail_tokens):
        return ("Security", "Better-Auth")
    if token_hit(tail_tokens, {"auth0", "oauth", "oidc", "jwt", "passkey", "session", "sso", "entra", "msal", "authentication"}):
        return ("Security", "Auth/OAuth")
    if token_hit(tail_tokens, {"security", "audit", "vuln", "vulnerability", "pentest", "forensics", "hardening", "threat", "malware", "rbac", "secret"}):
        return ("Security", "Security Audit")

    # Cloud/DevOps
    if token_hit(tail_tokens, {"azure", "aks", "bicep", "arm", "keyvault"}):
        return ("Cloud/DevOps", "Azure")
    if token_hit(tail_tokens, {"terraform", "hashicorp", "tfstate", "provider"}):
        return ("Cloud/DevOps", "Terraform")
    if token_hit(tail_tokens, {"vercel"}) or source == "32-Vercel-Nextjs":
        return ("Cloud/DevOps", "Vercel")
    if token_hit(tail_tokens, {"netlify"}):
        return ("Cloud/DevOps", "Netlify")
    if token_hit(tail_tokens, {"docker", "container", "containers", "kubernetes", "kubectl", "helm", "devcontainer", "podman"}):
        return ("Cloud/DevOps", "Docker")

    # AI/ML
    if token_hit(tail_tokens, {"openai", "chatgpt", "gpt", "responses"}) or source == "03-OpenAI":
        return ("AI/ML", "OpenAI")
    if phrase_in(tail_norm, ["hugging face", "hugging-face"]) or token_hit(tail_tokens, {"hugging", "hf", "transformers", "trl"}) or source == "18-Hugging-Face":
        return ("AI/ML", "HuggingFace")
    if token_hit(tail_tokens, {"gemini", "vertex"}):
        return ("AI/ML", "Gemini")
    if token_hit(tail_tokens, {"firecrawl"}):
        return ("AI/ML", "FireCrawl")
    if source in {"40-Vector-Databases", "11-Venice-AI", "14-fal-ai", "23-MiniMax"} or token_hit(tail_tokens, {"llm", "embedding", "vector", "rag", "inference", "finetune", "tokenizer", "prompt", "agentic"}):
        return ("AI/ML", "LLM Tools")
    return None


def import_recommendation(source, in_system, skill_name, description, subgroup):
    if in_system:
        return "Không — đã có"
    blob = normalize(" ".join([skill_name, description, subgroup]))
    hits = sum(1 for h in STRONG_IMPORT_HINTS if h in blob)
    if source in HIGH_TRUST_SOURCES and hits >= 1:
        return "Có — ưu tiên cao"
    if source in HIGH_TRUST_SOURCES:
        return "Có — đáng nhập"
    if hits >= 2:
        return "Có — cân nhắc"
    return "Cân nhắc"


def escape_md(text: str) -> str:
    text = text.replace("|", "\\|")
    return text.replace("\n", " ").strip()


workspace_entries = []
try:
    workspace_entries = os.listdir(WORKSPACE_SKILLS)
except FileNotFoundError:
    workspace_entries = []
workspace_norm = {slugify(x): x for x in workspace_entries}

records = []
seen = {}
for dp, dns, fns in os.walk(ROOT):
    if "SKILL.md" not in fns:
        continue
    rel_dir = os.path.relpath(dp, ROOT)
    rel_parts = rel_dir.split(os.sep)
    if any(part.startswith("_") for part in rel_parts):
        continue
    path = os.path.join(dp, "SKILL.md")
    rel = os.path.relpath(path, ROOT)
    source = rel.split(os.sep)[0]
    try:
        text = open(path, "r", encoding="utf-8").read()
    except UnicodeDecodeError:
        text = open(path, "r", encoding="utf-8", errors="ignore").read()
    fm, _ = parse_frontmatter(text)
    folder_name = os.path.basename(os.path.dirname(path))
    skill_name = fm.get("name", "").strip() or folder_name
    description, summary = extract_description_and_summary(text, fm)
    classification = classify(source, rel, skill_name, description)
    if not classification:
        continue
    group, subgroup = classification
    dedupe_key = (source, group, subgroup, slugify(skill_name))
    row = {
        "group": group,
        "subgroup": subgroup,
        "skill": skill_name,
        "description": description or "(không có description rõ ràng)",
        "capability": summary or description or "(không tóm tắt được)",
        "source": source,
        "rel": rel,
    }
    if dedupe_key in seen:
        prev = seen[dedupe_key]
        if len(rel) < len(prev["rel"]):
            seen[dedupe_key] = row
        continue
    seen[dedupe_key] = row

for row in seen.values():
    folder_slug = slugify(os.path.basename(os.path.dirname(os.path.join(ROOT, row["rel"]))))
    skill_slug = slugify(row["skill"])
    in_system = "Có" if (folder_slug in workspace_norm or skill_slug in workspace_norm) else "Không"
    row["in_system"] = in_system
    row["recommendation"] = import_recommendation(row["source"], in_system == "Có", row["skill"], row["description"], row["subgroup"])
    records.append(row)

# stable sort
records.sort(key=lambda r: (r["group"], r["subgroup"], r["source"], r["skill"], r["rel"]))

# counts
by_group = Counter(r["group"] for r in records)
by_subgroup = Counter((r["group"], r["subgroup"]) for r in records)
new_count = sum(1 for r in records if r["in_system"] == "Không")
priority_now = sum(1 for r in records if r["recommendation"] == "Có — ưu tiên cao")
worth_import = sum(1 for r in records if r["recommendation"].startswith("Có"))

lines = []
lines.append("# Đọc sâu 700 Skills AI/ML + Security + Cloud\n")
lines.append(f"_Quét toàn bộ `E:\\skill` bằng `os.walk`, đọc nội dung từng `SKILL.md`, lọc theo từ khóa trong tên/đường dẫn, rồi so với `os.listdir(workspace/skills)`._\n")
lines.append("_Lưu ý lọc dữ liệu: bỏ qua các thư mục cache/tạm bắt đầu bằng `_` (ví dụ `_repo_cache`, `_cache_repos`) và gộp các bản sao trùng `source + subgroup + skill` để kết quả gần với tập skill thực dùng được._\n")

for group in ["AI/ML", "Security", "Cloud/DevOps"]:
    items = [r for r in records if r["group"] == group]
    lines.append(f"## Nhóm: {group} ({len(items)} skills)\n")
    for subgroup in GROUP_SUBGROUP_ORDER[group]:
        subitems = [r for r in items if r["subgroup"] == subgroup]
        if not subitems:
            continue
        lines.append(f"### {subgroup}\n")
        lines.append("| Skill | Mô tả | Có trong hệ thống? | Đáng nhập? |")
        lines.append("|---|---|---|---|")
        for r in subitems:
            desc = f"{r['description']} Làm được: {r['capability']} Nguồn: `{r['source']}`"
            lines.append(
                f"| {escape_md(r['skill'])} | {escape_md(desc[:520])} | {r['in_system']} | {escape_md(r['recommendation'])} |"
            )
        lines.append("")

lines.append("## Tổng kết\n")
lines.append(f"- Tổng số skill được giữ lại sau khi đọc sâu và phân loại: **{len(records)}**")
lines.append(f"- AI/ML: **{by_group['AI/ML']}** | Security: **{by_group['Security']}** | Cloud/DevOps: **{by_group['Cloud/DevOps']}**")
lines.append(f"- Bao nhiêu skill mới so với `workspace/skills`: **{new_count}**")
lines.append(f"- Bao nhiêu skill đáng nhập ngay (`Có — ưu tiên cao`): **{priority_now}**")
lines.append(f"- Bao nhiêu skill đáng nhập tổng thể (`Có ...`): **{worth_import}**")

priority_examples = [r for r in records if r['recommendation'] == 'Có — ưu tiên cao'][:25]
if priority_examples:
    lines.append("- Ưu tiên nhập trước:")
    for r in priority_examples:
        lines.append(f"  - `{r['skill']}` — {r['group']} / {r['subgroup']} — nguồn `{r['source']}`")
else:
    lines.append("- Ưu tiên nhập trước: chưa có skill nào vượt ngưỡng ưu tiên cao theo heuristic.")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines).strip() + "\n")

stats = {
    "total_records": len(records),
    "by_group": dict(by_group),
    "by_subgroup": {f"{g}::{s}": c for (g,s), c in sorted(by_subgroup.items())},
    "new_count": new_count,
    "priority_now": priority_now,
    "worth_import": worth_import,
    "output": OUT,
}
print(json.dumps(stats, ensure_ascii=False, indent=2))
