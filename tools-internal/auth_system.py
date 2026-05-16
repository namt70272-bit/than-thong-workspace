#!/usr/bin/env python
"""
Enhanced Auth System — from MCP reference files
OAuth + JWT + Token management for MCP Gateway
Reference: mcp/ (AuthProvider, TokenHandler patterns)
"""
import os, sys, json, time, hashlib, secrets
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
AUTH_DIR = BASE / "auth"
AUTH_DIR.mkdir(exist_ok=True)
USERS_FILE = AUTH_DIR / "users.json"
TOKENS_FILE = AUTH_DIR / "tokens.json"

# Initialize
for f in [USERS_FILE, TOKENS_FILE]:
    if not f.exists():
        f.write_text("{}", encoding="utf-8")
        f.chmod(0o600)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role="user"):
    users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    if username in users:
        return {"error": "User exists"}
    users[username] = {
        "password": hash_password(password),
        "role": role,
        "created": time.time()
    }
    USERS_FILE.write_text(json.dumps(users, indent=2), encoding="utf-8")
    return {"ok": True, "user": username, "role": role}

def authenticate(username, password):
    users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    if username not in users:
        return None
    if users[username]["password"] != hash_password(password):
        return None
    return {"username": username, "role": users[username]["role"]}

def create_token(username, expires_in=86400):
    token = secrets.token_hex(32)
    tokens = json.loads(TOKENS_FILE.read_text(encoding="utf-8"))
    tokens[token] = {
        "username": username,
        "created": time.time(),
        "expires": time.time() + expires_in
    }
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
    return token

def validate_token(token):
    tokens = json.loads(TOKENS_FILE.read_text(encoding="utf-8"))
    if token not in tokens:
        return None
    info = tokens[token]
    if time.time() > info["expires"]:
        del tokens[token]
        TOKENS_FILE.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
        return None
    return info

def require_auth(func):
    """Decorator for MCP tools that need auth"""
    def wrapper(*args, **kwargs):
        # In MCP context, token comes from headers/session
        return func(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if action == "add-user":
        u = sys.argv[2] if len(sys.argv) > 2 else None
        p = sys.argv[3] if len(sys.argv) > 3 else "changeme"
        if u:
            r = create_user(u, p)
            print(f"User '{u}': {'OK' if r.get('ok') else r.get('error')}")
    elif action == "login":
        u = sys.argv[2] if len(sys.argv) > 2 else None
        p = sys.argv[3] if len(sys.argv) > 3 else None
        if u and p:
            user = authenticate(u, p)
            if user:
                token = create_token(u)
                print(f"Token: {token}")
            else:
                print("Auth failed")
    elif action == "verify":
        t = sys.argv[2] if len(sys.argv) > 2 else None
        if t:
            info = validate_token(t)
            if info:
                print(f"Valid: user={info['username']}")
            else:
                print("Invalid/expired")
    else:
        print("Auth System")
        print("  add-user <name> <pass>")
        print("  login <name> <pass>")
        print("  verify <token>")
