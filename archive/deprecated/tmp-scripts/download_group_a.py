import csv
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

CSV_PATH = Path(r"E:\skill\_skill-index.csv")
DEST_ROOT = Path(r"E:\skill")
TMP_ROOT = DEST_ROOT / "_tmp_group_a"
LOG_PATH = DEST_ROOT / "_download_log.txt"
CATEGORY_DIRS = {
    "Development and Testing": DEST_ROOT / "41-Cong-Dong-Phat-Trien-Kiem-Thu",
    "Productivity and Collaboration": DEST_ROOT / "42-Cong-Dong-Nang-Suat-Cong-Tac",
}
TARGET_CATEGORIES = tuple(CATEGORY_DIRS.keys())

GITHUB_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:/(?:tree|blob)/(?P<branch>[^/]+)/(?P<subpath>.+))?/?$",
    re.IGNORECASE,
)


def safe_name(name: str) -> str:
    s = name.replace("/", "__")
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-._")
    return s or "skill"


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if r["Category"] in TARGET_CATEGORIES]


def ensure_clean_dir(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_placeholder(dest_dir: Path, url: str, reason: str, row: dict):
    ensure_clean_dir(dest_dir)
    (dest_dir / "SOURCE.txt").write_text(
        f"Skill: {row['SkillName']}\nCategory: {row['Category']}\nURL: {url}\nReason: {reason}\n",
        encoding="utf-8",
    )


def run_git(args, cwd=None, timeout=300):
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result


def clone_repo(owner: str, repo: str, branch: str | None):
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    key = f"{owner}__{repo}__{branch or 'default'}"
    target = TMP_ROOT / key
    if target.exists() and (target / ".git").exists() and any(x.name != '.git' for x in target.iterdir()):
        return target, None
    if target.exists():
        shutil.rmtree(target)
    url = f"https://github.com/{owner}/{repo}.git"
    args = ["clone", "--quiet", "--depth", "1", "--single-branch", "--no-tags"]
    if branch:
        args += ["--branch", branch]
    args += [url, str(target)]
    try:
        res = run_git(args)
    except subprocess.TimeoutExpired:
        res = None
    if res and res.returncode == 0:
        return target, None
    if branch:
        if target.exists():
            shutil.rmtree(target)
        try:
            res2 = run_git(["clone", "--quiet", "--depth", "1", "--single-branch", "--no-tags", url, str(target)])
        except subprocess.TimeoutExpired:
            res2 = None
        if res2 and res2.returncode == 0:
            return target, None
        msg1 = (res.stderr if res else "git clone timed out") if res is not None else "git clone timed out"
        msg2 = (res2.stderr if res2 else "fallback clone timed out") if 'res2' in locals() else ""
        return None, (msg1 or "") + "\n" + (msg2 or "")
    return None, (res.stderr if res else "git clone timed out") or "git clone failed"


def copy_dir(src: Path, dest: Path):
    ensure_clean_dir(dest)
    for item in src.iterdir():
        if item.name == ".git":
            continue
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def copy_file(src: Path, dest_dir: Path):
    ensure_clean_dir(dest_dir)
    shutil.copy2(src, dest_dir / src.name)


def resolve_source(repo_root: Path, subpath: str | None, is_blob: bool):
    if not subpath:
        return repo_root, "dir"
    p = repo_root / Path(subpath)
    if is_blob:
        if p.name.lower() == "skill.md" and p.parent.exists():
            return p.parent, "dir"
        return p, "file"
    return p, "dir"


def process_row(row: dict):
    url = row["Url"].strip()
    dest_base = CATEGORY_DIRS[row["Category"]]
    dest_base.mkdir(parents=True, exist_ok=True)
    dest_dir = dest_base / safe_name(row["SkillName"])

    if dest_dir.exists() and any(dest_dir.iterdir()):
        only_source = [p.name for p in dest_dir.iterdir()] == ['SOURCE.txt']
        if not only_source:
            return {"status": "downloaded", "reason": "existing", "dest": str(dest_dir)}

    m = GITHUB_RE.match(url)
    if not m:
        write_placeholder(dest_dir, url, "Non-GitHub or registry-only source; manual retrieval required.", row)
        return {"status": "placeholder", "reason": "non-github", "dest": str(dest_dir)}

    owner = m.group("owner")
    repo = m.group("repo")
    branch = m.group("branch")
    subpath = m.group("subpath")
    is_blob = "/blob/" in url

    repo_root, clone_err = clone_repo(owner, repo, branch)
    if not repo_root:
        write_placeholder(dest_dir, url, f"Unavailable/private/clone failed: {clone_err.strip()}", row)
        return {"status": "placeholder", "reason": "clone-failed", "dest": str(dest_dir)}

    src, kind = resolve_source(repo_root, subpath, is_blob)
    if not src.exists():
        write_placeholder(dest_dir, url, f"Referenced path not found in cloned repo: {subpath}", row)
        return {"status": "placeholder", "reason": "path-missing", "dest": str(dest_dir)}

    if kind == "dir":
        copy_dir(src, dest_dir)
    else:
        copy_file(src, dest_dir)
    return {"status": "downloaded", "reason": kind, "dest": str(dest_dir)}


def main():
    rows = load_rows()
    results = []
    for row in rows:
        result = process_row(row)
        result.update({"skill": row["SkillName"], "category": row["Category"], "url": row["Url"]})
        results.append(result)
        print(f"[{result['status']}] {row['Category']} :: {row['SkillName']}", flush=True)

    counts = {cat: {"downloaded": 0, "placeholder": 0, "total": 0} for cat in TARGET_CATEGORIES}
    unavailable = []
    for r in results:
        counts[r["category"]]["total"] += 1
        counts[r["category"]][r["status"]] += 1
        if r["status"] != "downloaded":
            unavailable.append({"category": r["category"], "skill": r["skill"], "url": r["url"], "reason": r["reason"]})

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines = [
        f"[{timestamp}] GROUP A download summary",
        *(f"- {cat}: {counts[cat]['downloaded']}/{counts[cat]['total']} downloaded, {counts[cat]['placeholder']} placeholders" for cat in TARGET_CATEGORIES),
    ]
    if unavailable:
        log_lines.append("- Unavailable/placeholders:")
        log_lines.extend([f"  * {u['category']} :: {u['skill']} :: {u['reason']} :: {u['url']}" for u in unavailable])
    log_lines.append("")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")

    summary = {"counts": counts, "unavailable": unavailable, "results": results}
    print("SUMMARY_JSON=" + json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
