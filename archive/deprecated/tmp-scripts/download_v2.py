import csv
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

CSV_PATH = Path(r"E:\skill\_skill-index.csv")
DEST_ROOT = Path(r"E:\skill")
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
GITHUB_RAW = re.compile(
    r"^https?://raw\.githubusercontent\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/(?P<branch>[^/]+)/(?P<filepath>.+)$",
    re.IGNORECASE,
)


def safe_name(name: str) -> str:
    s = name.replace("/", "__").replace(" ", "-")
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


def download_zip(url: str, temp_dir: Path) -> Path | None:
    """Download a zip file from URL to temp_dir, return path or None."""
    dest = temp_dir / "archive.zip"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        if resp.status != 200 and resp.status != 302:
            return None
        dest.write_bytes(data)
        return dest
    except Exception as e:
        return None


def extract_zip(zip_path: Path, extract_to: Path):
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(str(extract_to))


def download_single_file(url: str, dest_dir: Path):
    """Download a single raw file from GitHub."""
    m = GITHUB_RAW.match(url)
    if not m:
        return False
    ensure_clean_dir(dest_dir)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        filename = Path(m.group("filepath")).name
        (dest_dir / filename).write_bytes(data)
        return True
    except Exception:
        return False


def find_skill_dir(extract_root: Path, subpath: str | None) -> Path | None:
    """
    After extracting a zip, the archive has a top-level folder like `repo-branch/`.
    Find the requested subpath within it.
    """
    top_dirs = list(extract_root.iterdir())
    if not top_dirs:
        return None
    base = top_dirs[0]  # Should be the repo root folder
    if not subpath:
        return base
    candidate = base / subpath
    if candidate.exists():
        return candidate
    return None


def resolve_owner_repo(owner: str, repo: str, branch: str | None):
    """Get the default branch name via git ls-remote HEAD symbolic ref."""
    if branch:
        return branch
    try:
        url = f"https://github.com/{owner}/{repo}.git"
        r = subprocess.run(
            ["git", "ls-remote", "--symref", url, "HEAD"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                m = re.search(r"ref: refs/heads/(\S+)\s+HEAD", line)
                if m:
                    return m.group(1)
    except Exception:
        pass
    return "main"  # fallback


def download_skill_from_github(row: dict) -> dict:
    url = row["Url"].strip()
    m = GITHUB_RE.match(url)
    if not m:
        return None  # not a github url

    owner = m.group("owner")
    repo = m.group("repo")
    branch = m.group("branch")
    subpath = m.group("subpath")
    is_blob = "/blob/" in url

    # Resolve branch if not specified
    actual_branch = resolve_owner_repo(owner, repo, branch)

    # If it's a single file from blob, try raw download
    if is_blob and subpath and subpath.lower().endswith(".md"):
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{actual_branch}/{subpath}"
        dest_base = CATEGORY_DIRS[row["Category"]]
        dest_dir = dest_base / safe_name(row["SkillName"])
        ensure_clean_dir(dest_dir)
        try:
            req = urllib.request.Request(raw_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            filename = Path(subpath).name
            (dest_dir / filename).write_bytes(data)
            return {"status": "downloaded", "reason": "raw-file", "dest": str(dest_dir)}
        except Exception as e:
            write_placeholder(dest_dir, url, f"Failed to download raw file: {e}", row)
            return {"status": "placeholder", "reason": f"raw-dl-fail: {e}", "dest": str(dest_dir)}

    # Use archive zip
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{actual_branch}.zip"
    with tempfile.TemporaryDirectory(prefix="skill_dl_") as tmp:
        tmp_path = Path(tmp)
        zip_path = download_zip(zip_url, tmp_path)
        if not zip_path:
            # Try main as fallback
            zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
            zip_path = download_zip(zip_url, tmp_path)
        if not zip_path:
            # Try master
            zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
            zip_path = download_zip(zip_url, tmp_path)
        if not zip_path:
            dest_base = CATEGORY_DIRS[row["Category"]]
            dest_dir = dest_base / safe_name(row["SkillName"])
            write_placeholder(dest_dir, url, f"Failed to download archive for {owner}/{repo}", row)
            return {"status": "placeholder", "reason": "zip-dl-fail", "dest": str(dest_dir)}

        extract_to = tmp_path / "extracted"
        extract_to.mkdir()
        extract_zip(zip_path, extract_to)

        src = find_skill_dir(extract_to, subpath)
        if not src or not src.exists():
            dest_base = CATEGORY_DIRS[row["Category"]]
            dest_dir = dest_base / safe_name(row["SkillName"])
            write_placeholder(dest_dir, url, f"Subpath '{subpath}' not found in archive for {owner}/{repo}", row)
            return {"status": "placeholder", "reason": "subpath-missing", "dest": str(dest_dir)}

        dest_base = CATEGORY_DIRS[row["Category"]]
        dest_dir = dest_base / safe_name(row["SkillName"])
        ensure_clean_dir(dest_dir)

        # Copy all files from src to dest_dir
        for item in src.iterdir():
            if item.is_dir():
                shutil.copytree(item, dest_dir / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_dir / item.name)

        return {"status": "downloaded", "reason": "archive", "dest": str(dest_dir)}


def main():
    rows = load_rows()
    results = []

    for row in rows:
        dest_base = CATEGORY_DIRS[row["Category"]]
        dest_dir = dest_base / safe_name(row["SkillName"])

        # Skip if already downloaded (not placeholder)
        if dest_dir.exists() and any(dest_dir.iterdir()):
            only_source = list(dest_dir.iterdir()) == [dest_dir / "SOURCE.txt"]
            if not only_source:
                results.append({
                    "status": "downloaded",
                    "reason": "existing",
                    "dest": str(dest_dir),
                    "skill": row["SkillName"],
                    "category": row["Category"],
                    "url": row["Url"],
                })
                print(f"[downloaded-skip] {row['Category']} :: {row['SkillName']}", flush=True)
                continue

        url = row["Url"].strip()
        m = GITHUB_RE.match(url)

        if not m:
            dest_dir.mkdir(parents=True, exist_ok=True)
            write_placeholder(dest_dir, url, "Non-GitHub URL", row)
            result = {"status": "placeholder", "reason": "non-github", "dest": str(dest_dir)}
        else:
            result = download_skill_from_github(row)
            if result is None:
                dest_dir.mkdir(parents=True, exist_ok=True)
                write_placeholder(dest_dir, url, "Non-GitHub URL (fallthrough)", row)
                result = {"status": "placeholder", "reason": "non-github", "dest": str(dest_dir)}

        result.update({"skill": row["SkillName"], "category": row["Category"], "url": row["Url"]})
        results.append(result)
        print(f"[{result['status']}] {row['Category']} :: {row['SkillName']} :: {result['reason']}", flush=True)

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
        *[f"- {cat}: {counts[cat]['downloaded']}/{counts[cat]['total']} downloaded, {counts[cat]['placeholder']} placeholders" for cat in TARGET_CATEGORIES],
    ]
    if unavailable:
        log_lines.append("- Unavailable/placeholders:")
        log_lines.extend([f"  * {u['category']} :: {u['skill']} :: {u['reason']} :: {u['url']}" for u in unavailable])
    log_lines.append("")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")

    summary = {"counts": counts, "unavailable": unavailable}
    print("=== SUMMARY_JSON ===", flush=True)
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
