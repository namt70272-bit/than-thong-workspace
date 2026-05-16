#!/usr/bin/env python3
"""Load .env file for all agent modules"""
import os

env_path = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\.env"
loaded = []

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
                loaded.append(key)

# Always set defaults
if "FASTMCP_PORT" not in os.environ:
    os.environ["FASTMCP_PORT"] = "9876"

if __name__ == "__main__":
    print("Loaded env keys:", loaded)
    print("OPENAI_API_KEY:", "set" if os.environ.get("OPENAI_API_KEY") else "missing")
    print("FIRECRAWL_API_KEY:", "set" if os.environ.get("FIRECRAWL_API_KEY") else "missing")
