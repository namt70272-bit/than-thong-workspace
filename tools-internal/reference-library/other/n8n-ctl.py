#!/usr/bin/env python3
"""
n8n Controller — quan ly n8n workflow qua API.
Dung requests (xu ly XSRF cookie tu dong).

Cach dung:
  python n8n-ctl.py login <email> <pwd>      # Login + save session
  python n8n-ctl.py status                    # Xem workflows
  python n8n-ctl.py activate <id>             # Activate workflow
  python n8n-ctl.py deactivate <id>           # Deactivate
  python n8n-ctl.py import <file.json>        # Import workflow
  python n8n-ctl.py restart                   # Restart docker container
  python n8n-ctl.py setup <email> <pwd>       # Owner setup (lan dau)
"""
import sys, os, json, time, subprocess, pickle
import requests
from urllib.parse import unquote

N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")
N8N_CONTAINER = os.environ.get("N8N_CONTAINER", "n8n")
SESSION_FILE = os.path.expanduser("~/.n8n-session.pkl")

def fix_stdio():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except: pass
fix_stdio()

def make_requests():
    s = requests.Session()
    # Load saved session if exists
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'rb') as f:
                saved = pickle.load(f)
            s.cookies.update(saved.get('cookies', {}))
        except: pass
    return s

def save_session(s):
    # Also hit the editor to get CSRF token
    s.get(N8N_URL + '/', timeout=5)
    # Build header with xsrf
    xsrf = ''
    if 'XSRF-TOKEN' in s.cookies:
        xsrf = unquote(s.cookies['XSRF-TOKEN'])
    n8n_auth = s.cookies.get('n8n-auth', '')
    if xsrf:
        s.headers['X-XSRF-TOKEN'] = xsrf
    elif n8n_auth:
        s.headers['X-XSRF-TOKEN'] = n8n_auth
    # Save
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump({'cookies': dict(s.cookies)}, f)
    return xsrf or n8n_auth or 'no-token'

def api(s, method, path, data=None):
    url = N8N_URL + path
    try:
        r = s.request(method, url, json=data, timeout=10)
        return r.status_code, r.json() if r.text and 'application/json' in r.headers.get('Content-Type','') else r.text
    except Exception as e:
        return 0, str(e)

def cmd_login(args):
    email, pwd = args[0], args[1]
    s = requests.Session()
    # First call to get CSRF
    s.get(N8N_URL + '/', timeout=5)
    # Login
    r = s.post(N8N_URL + '/rest/login', json={
        'emailOrLdapLoginId': email, 'password': pwd
    }, timeout=5)
    if r.status_code == 200:
        save_session(s)
        print(f'[OK] Login: {email}')
    else:
        print(f'[ERR] Login: {r.status_code} {r.text[:200]}')

def cmd_status(args):
    s = make_requests()
    save_session(s)
    code, data = api(s, 'GET', '/rest/workflows')
    if code != 200:
        print(f'[ERR] {code} {data}')
        return
    wfs = data.get('data', [])
    print(f'[LIST] Workflows ({len(wfs)}):')
    for w in wfs:
        icon = '[ON]' if w.get('active') else '[OFF]'
        print(f'  {icon} {w["id"][:8]}... {w.get("name","?")} active={w.get("active")}')

def cmd_activate(args):
    wf_id = args[0]
    s = make_requests()
    save_session(s)
    code, data = api(s, 'PATCH', f'/rest/workflows/{wf_id}', {'active': True})
    if code == 200:
        print(f'[OK] Activated {wf_id[:8]}...')
        # Publish
        subprocess.run([
            'docker', 'exec', N8N_CONTAINER, 'sh', '-c',
            f'cd /home/node/.n8n && n8n publish:workflow --id={wf_id}'
        ], capture_output=True, text=True)
        print('[PUB] Published. Restart n8n:')
        print(f'   docker restart {N8N_CONTAINER}')
    else:
        print(f'[ERR] {code} {data}')

def cmd_deactivate(args):
    wf_id = args[0]
    s = make_requests()
    save_session(s)
    code, data = api(s, 'PATCH', f'/rest/workflows/{wf_id}', {'active': False})
    if code == 200:
        print(f'[OK] Deactivated {wf_id[:8]}...')
    else:
        print(f'[ERR] {code} {data}')

def cmd_import(args):
    path = args[0]
    subprocess.run(['docker', 'cp', path, f'{N8N_CONTAINER}:/tmp/wf_import.json'],
                   capture_output=True)
    r = subprocess.run([
        'docker', 'exec', N8N_CONTAINER, 'sh', '-c',
        'cd /home/node/.n8n && n8n import:workflow --input=/tmp/wf_import.json'
    ], capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(f'[ERR] {r.stderr}')

def cmd_restart(args):
    print('[RST] Restarting n8n...')
    r = subprocess.run(['docker', 'restart', N8N_CONTAINER], capture_output=True, text=True)
    if r.returncode == 0:
        print('[OK] Waiting 15s...')
        time.sleep(15)
        check = subprocess.run(['docker', 'logs', N8N_CONTAINER, '--tail', '3'],
                               capture_output=True, text=True)
        if 'Editor is now accessible' in check.stdout:
            print('[OK] n8n ready')
        else:
            print(check.stdout)
    else:
        print(f'[ERR] {r.stderr}')

def cmd_setup(args):
    email, pwd = args[0], args[1]
    r = requests.post(N8N_URL + '/rest/owner/setup', json={
        'firstName': 'Admin', 'lastName': 'n8n',
        'email': email, 'password': pwd
    }, timeout=5)
    if r.status_code == 200:
        print(f'[OK] Owner setup: {email}')
    else:
        print(f'[ERR] {r.status_code} {r.text[:200]}')

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    args = sys.argv[2:]
    cmds = {
        'login': cmd_login, 'status': cmd_status,
        'activate': cmd_activate, 'deactivate': cmd_deactivate,
        'import': cmd_import, 'restart': cmd_restart, 'setup': cmd_setup,
    }
    fn = cmds.get(cmd)
    if not fn:
        print(f'[ERR] Unknown command: {cmd}')
        print(__doc__)
        return
    fn(args)

if __name__ == '__main__':
    main()
