#!/usr/bin/env python3
"""Load .env file and vault for all agent modules"""
import os, sys, importlib.util

BASE = os.path.dirname(__file__)
loaded = []

# Try vault first
vault_path = os.path.join(BASE, "vault.py")
vault_json = os.path.join(BASE, ".vault.json")
if os.path.exists(vault_json):
    try:
        spec = importlib.util.spec_from_file_location("vault", vault_path)
        vault = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vault)
        secrets = vault.vault_get()
        if secrets:
            for k, v in secrets.items():
                os.environ.setdefault(k, v)
                loaded.append(k)
    except Exception as e:
        print(f"Vault load failed: {e}", file=sys.stderr)

# Fallback to .env
env_path = os.path.join(BASE, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"").strip()
            if key and val and key not in os.environ:
                os.environ[key] = val
                if key not in loaded:
                    loaded.append(key)

# Default port
if "FASTMCP_PORT" not in os.environ:
    os.environ["FASTMCP_PORT"] = "9876"

if __name__ == "__main__":
    print("Loaded env keys:", loaded)
    print("OPENAI_API_KEY:", "set" if os.environ.get("OPENAI_API_KEY") else "missing")
    print("FIRECRAWL_API_KEY:", "set" if os.environ.get("FIRECRAWL_API_KEY") else "missing")
