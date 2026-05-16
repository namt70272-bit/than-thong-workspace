#!/usr/bin/env python
"""
Vault - Encrypted API key storage
Replaces plaintext .env with encrypted storage
"""
import os, sys, json, base64
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOOLS = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
VAULT_FILE = TOOLS / ".vault.json"
ENV_FILE = TOOLS / ".env"
KEY_FILE = TOOLS / ".vault_key"
LOCK_FILE = TOOLS / ".vault.lock"

# Simple XOR-based encryption (not military grade, but stops casual reading)
# For production: use cryptography.fernet instead
def _xor_encrypt(data: str, key: str) -> str:
    result = []
    for i, c in enumerate(data):
        result.append(chr(ord(c) ^ ord(key[i % len(key)])))
    return "".join(result)

def _get_or_create_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_text().strip()
    import uuid
    key = str(uuid.uuid4()) + str(uuid.uuid4())
    KEY_FILE.write_text(key)
    KEY_FILE.chmod(0o600)  # owner read/write only
    return key

def vault_init():
    """Convert .env to encrypted vault"""
    if not ENV_FILE.exists():
        print("No .env file found")
        return
    
    print("Initializing vault from .env...")
    key = _get_or_create_key()
    
    secrets = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                secrets[k.strip()] = v.strip()
    
    encrypted = {}
    for k, v in secrets.items():
        encrypted[k] = _xor_encrypt(v, key + k)
    
    vault = {
        "version": 1,
        "keys": list(secrets.keys()),
        "encrypted": encrypted,
        "created": __import__("datetime").datetime.now().isoformat()
    }
    
    VAULT_FILE.write_text(json.dumps(vault, indent=2))
    VAULT_FILE.chmod(0o600)
    
    # Overwrite original .env with placeholder
    ENV_FILE.write_text("# Keys moved to vault. Use vault_get() to access.\n")
    ENV_FILE.chmod(0o600)
    
    LOCK_FILE.write_text("locked")
    
    print(f"Vault initialized: {len(secrets)} keys encrypted")
    print(f"Original .env overwritten with placeholder")
    print(f"Key stored in: {KEY_FILE}")

def vault_get(key_name=None):
    """Get a key from the vault. If key_name is None, return all."""
    if not VAULT_FILE.exists():
        return None if key_name else {}
    
    key = KEY_FILE.read_text().strip() if KEY_FILE.exists() else ""
    vault = json.loads(VAULT_FILE.read_text())
    
    if key_name:
        if key_name in vault["encrypted"]:
            return _xor_encrypt(vault["encrypted"][key_name], key + key_name)
        return None
    
    result = {}
    for k in vault["keys"]:
        result[k] = _xor_encrypt(vault["encrypted"][k], key + k)
    return result

def vault_list():
    """List stored keys without revealing values"""
    if not VAULT_FILE.exists():
        print("Vault not initialized")
        return
    vault = json.loads(VAULT_FILE.read_text())
    print(f"Vault v{vault['version']} - {len(vault['keys'])} keys")
    for k in vault["keys"]:
        val = vault_get(k)
        print(f"  {k}: {val[:8]}...{val[-4:]}" if val else f"  {k}: (error)")

def vault_load_env():
    """Load vault keys into environment"""
    secrets = vault_get()
    if secrets:
        for k, v in secrets.items():
            os.environ[k] = v
        print(f"Loaded {len(secrets)} keys into environment")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if action == "init":
        vault_init()
    elif action == "list":
        vault_list()
    elif action == "get":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        val = vault_get(name)
        if val and name:
            print(f"{name}={val[:8]}...{val[-4:]}")
        elif val:
            for k, v in val.items():
                print(f"{k}={v[:8]}...{v[-4:]}")
    elif action == "load":
        vault_load_env()
    else:
        print("Vault - Encrypted API key storage")
        print()
        print("Commands:")
        print("  init  - Encrypt .env into vault")
        print("  list  - Show stored keys")
        print("  get   - Show a key (masked)")
        print("  load  - Load keys into environment")
