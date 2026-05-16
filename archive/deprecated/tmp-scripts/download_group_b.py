"""Download Group B Community skills into E:\skill category folders."""
import csv, os, sys, subprocess, tempfile, shutil, uuid, json, time, stat
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone, timedelta

INDEX = r'E:\skill\_skill-index.csv'
TEMP_ROOT = r'E:\skill\_tmp_group_b'
CATEGORY_MAP = {
    'Specialized Domains': r'E:\skill\43-Cong-Dong-Chuyen-Nganh-Dac-Thu',
    'Marketing': r'E:\skill\44-Cong-Dong-Tiep-Thi-Mang-Xa-Hoi',
    'Context Engineering': r'E:\skill\45-Cong-Dong-Ky-Thuat-Ngu-Canh',
    'n8n Automation': r'E:\skill\46-Cong-Dong-n8n-Tu-Dong-Hoa',
}

TZ = timezone(timedelta(hours=7))
timestamp = datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S %z')

def safe_name(s):
    x = s.strip()
    x = x.replace('http://','').replace('https://','')
    for ch in '\\/:*?"<>|': x = x.replace(ch, '__')
    x = x.replace(' ', '-')
    x = ''.join(c if c.isalnum() or c in '._-' else '_' for c in x)
    x = x.strip(' ._-')
    if not x: x = 'unnamed-skill'
    if len(x) > 120: x = x[:120].strip(' ._-')
    return x

def ensure_clean_dir(p):
    if os.path.exists(p):
        for root, dirs, files in os.walk(p, topdown=False):
            for name in files:
                fp = os.path.join(root, name)
                try:
                    os.chmod(fp, stat.S_IWRITE)
                except:
                    pass
        shutil.rmtree(p, ignore_errors=True)
    os.makedirs(p, exist_ok=True)

def write_source(dest, name, category, url, desc, status, reason):
    os.makedirs(dest, exist_ok=True)
    txt = f"""Skill: {name}
Category: {category}
Source: {url}
Status: {status}
Reason: {reason}
Description: {desc}
DownloadedAt: {datetime.now(TZ).isoformat()}
"""
    with open(os.path.join(dest, 'SOURCE.txt'), 'w', encoding='utf-8') as f:
        f.write(txt)

def copy_dir_contents(src, dest):
    ensure_clean_dir(dest)
    for item in os.listdir(src):
        if item == '.git':
            continue
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
        else:
            shutil.copy2(s, d)

def run_git(args, cwd=None, timeout=180):
    env = os.environ.copy()
    env['GIT_TERMINAL_PROMPT'] = '0'
    try:
        proc = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        out = proc.stdout + proc.stderr
        return proc.returncode, out
    except subprocess.TimeoutExpired:
        return 124, 'git command timed out'
    except Exception as e:
        return -1, str(e)

def parse_github(url):
    try:
        u = urlparse(url)
    except:
        return None
    if u.hostname and u.hostname.lower() != 'github.com':
        return None
    parts = [p for p in u.path.strip('/').split('/') if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].replace('.git', '')
    info = {
        'owner': owner,
        'repo': repo,
        'repo_url': f'https://github.com/{owner}/{repo}.git',
        'kind': 'repo',
        'ref': None,
        'subpath': None,
        'raw_url': None,
    }
    if len(parts) >= 5 and parts[2] in ('tree', 'blob'):
        info['kind'] = parts[2]
        info['ref'] = parts[3]
        info['subpath'] = '/'.join(parts[4:])
        if parts[2] == 'blob':
            info['raw_url'] = f'https://raw.githubusercontent.com/{owner}/{repo}/{parts[3]}/' + info['subpath']
    return info

def check_github_exists(gh):
    """Check if GitHub repo exists via API. Returns True if exists/pub, False if 404/private."""
    import urllib.request
    api = f'https://api.github.com/repos/{gh["owner"]}/{gh["repo"]}'
    try:
        req = urllib.request.Request(api)
        req.add_header('User-Agent', 'OpenClaw-Downloader/1.0')
        resp = urllib.request.urlopen(req, timeout=20)
        return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        return True  # assume exists on other errors (rate limit etc)
    except:
        return None  # indeterminate

def download_github_repo(gh, dest, name, cat, url, desc):
    tmp = os.path.join(TEMP_ROOT, str(uuid.uuid4()))
    try:
        exists = check_github_exists(gh)
        if exists is False:
            raise RuntimeError(f"GitHub repository unavailable/private (API 404): {gh['owner']}/{gh['repo']}")
        if exists is None:
            # API failed but repo might still be reachable via git — proceed
            pass

        if gh['kind'] == 'repo':
            rc, out = run_git(['clone', '--depth', '1', gh['repo_url'], tmp])
            if rc != 0:
                raise RuntimeError(f"git clone failed: {out}")
            copy_dir_contents(tmp, dest)
            write_source(dest, name, cat, url, desc, 'downloaded',
                        'shallow cloned repository; .git removed after copy')
            return True

        elif gh['kind'] == 'tree':
            rc, out = run_git([
                'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                '--branch', gh['ref'], gh['repo_url'], tmp
            ])
            if rc != 0:
                raise RuntimeError(f"git sparse clone failed: {out}")
            rc2, out2 = run_git(
                ['sparse-checkout', 'set', '--no-cone', gh['subpath']],
                cwd=tmp
            )
            if rc2 != 0:
                raise RuntimeError(f"sparse-checkout failed: {out2}")
            src = os.path.join(tmp, gh['subpath'].replace('/', os.sep))
            if not os.path.exists(src):
                raise RuntimeError(f"subfolder not found after sparse checkout: {gh['subpath']}")
            copy_dir_contents(src, dest)
            write_source(dest, name, cat, url, desc, 'downloaded',
                        f"sparse cloned subfolder {gh['subpath']} from {gh['owner']}/{gh['repo']}@{gh['ref']}; .git removed")
            return True

        elif gh['kind'] == 'blob':
            ensure_clean_dir(dest)
            import urllib.request
            filename = os.path.basename(gh['subpath'])
            target = os.path.join(dest, filename)
            urllib.request.urlretrieve(gh['raw_url'], target)
            write_source(dest, name, cat, url, desc, 'downloaded',
                        f"downloaded single file {gh['subpath']} from raw GitHub URL")
            return True

    except Exception as e:
        ensure_clean_dir(dest)
        write_source(dest, name, cat, url, desc, 'unavailable', str(e))
        return False
    finally:
        if os.path.exists(tmp):
            for root2, dirs2, files2 in os.walk(tmp, topdown=False):
                for fp in files2 + dirs2:
                    try: os.chmod(os.path.join(root2, fp), stat.S_IWRITE)
                    except: pass
            shutil.rmtree(tmp, ignore_errors=True)

def download_nongit(url, dest, name, cat, desc):
    try:
        import urllib.request
        ensure_clean_dir(dest)
        leaf = os.path.basename(urlparse(url).path)
        if not leaf:
            leaf = 'downloaded-skill'
        target = os.path.join(dest, leaf)
        urllib.request.urlretrieve(url, target)
        write_source(dest, name, cat, url, desc, 'downloaded',
                    'downloaded non-GitHub URL as single file')
        return True
    except Exception as e:
        ensure_clean_dir(dest)
        write_source(dest, name, cat, url, desc, 'unavailable', str(e))
        return False

def main():
    os.makedirs(TEMP_ROOT, exist_ok=True)
    for d in CATEGORY_MAP.values():
        os.makedirs(d, exist_ok=True)

    with open(INDEX, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r['Category'] in CATEGORY_MAP]

    results = []

    for row in rows:
        cat = row['Category']
        base = CATEGORY_MAP[cat]
        safe = safe_name(row['SkillName'])
        dest = os.path.join(base, safe)
        print(f"[{cat}] {row['SkillName']}", flush=True)

        gh = parse_github(row['Url'])
        if gh:
            ok = download_github_repo(gh, dest, row['SkillName'], cat, row['Url'], row['Description'])
        else:
            ok = download_nongit(row['Url'], dest, row['SkillName'], cat, row['Description'])

        # Read status from SOURCE.txt
        src_path = os.path.join(dest, 'SOURCE.txt')
        status = 'unknown'
        if os.path.exists(src_path):
            with open(src_path, encoding='utf-8') as f:
                content = f.read()
                for line in content.splitlines():
                    if line.startswith('Status:'):
                        status = line.split(':', 1)[1].strip()

        results.append({
            'category': cat,
            'skill_name': row['SkillName'],
            'url': row['Url'],
            'dest': dest,
            'ok': status == 'downloaded',
            'status': status,
        })

    # Print summary
    print("\n" + "="*60)
    print(f"GROUP B download: {timestamp}")
    print("="*60)
    totals = {}
    for cat_key in CATEGORY_MAP:
        cat_res = [r for r in results if r['category'] == cat_key]
        ok_count = sum(1 for r in cat_res if r['ok'])
        totals[cat_key] = {'downloaded': ok_count, 'unavailable': len(cat_res) - ok_count, 'total': len(cat_res)}
        print(f"  {cat_key}: downloaded={ok_count} unavailable={len(cat_res) - ok_count} total={len(cat_res)}")

    unavail = [r for r in results if not r['ok']]
    print(f"\nUnavailable items ({len(unavail)}):")
    for u in unavail:
        src_path = os.path.join(u['dest'], 'SOURCE.txt')
        reason = 'unknown'
        if os.path.exists(src_path):
            with open(src_path, encoding='utf-8') as f:
                for line in f:
                    if line.startswith('Reason:'):
                        reason = line.split(':', 1)[1].strip()
                        break
        print(f"  - [{u['category']}] {u['skill_name']} :: {u['url']} :: {reason}")

    # Write log
    log_path = r'E:\skill\_download_log.txt'
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n=== GROUP B download run: {timestamp} ===\n")
        for cat_key, t in totals.items():
            f.write(f"{cat_key} -> {CATEGORY_MAP[cat_key]} : downloaded={t['downloaded']} unavailable={t['unavailable']} total={t['total']}\n")
        f.write("Unavailable items:\n")
        if not unavail:
            f.write("  none\n")
        else:
            for u in unavail:
                src_path = os.path.join(u['dest'], 'SOURCE.txt')
                reason = 'unknown'
                if os.path.exists(src_path):
                    with open(src_path, encoding='utf-8') as f2:
                        for line in f2:
                            if line.startswith('Reason:'):
                                reason = line.split(':', 1)[1].strip()
                                break
                f.write(f"  - [{u['category']}] {u['skill_name']} :: {u['url']} :: {reason}\n")

    # Write summary JSON
    summary_path = r'E:\skill\_group_b_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nSummary written: {summary_path}")

if __name__ == '__main__':
    main()
