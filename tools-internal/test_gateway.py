#!/usr/bin/env python
"""Test all 5 servers"""
import httpx, json, sys

print("=== FINAL TEST: MCP Ecosystem + Gateway ===\n")

results = {}

# 1) Health check
try:
    r = httpx.get("http://127.0.0.1:9001/health", timeout=5)
    data = r.json()
    print(f"Gateway Health: {data.get('gateway')}")
    for s, info in data.get("servers", {}).items():
        print(f"  {s}: {info.get('status')}")
    results["gateway"] = "OK"
except Exception as e:
    print(f"Gateway: {type(e).__name__}")
    results["gateway"] = str(e)[:30]

# 2) List servers
try:
    r = httpx.get("http://127.0.0.1:9001/servers", timeout=10)
    data = r.json()
    for s, info in data.items():
        if isinstance(info, dict):
            cnt = info.get("count", 0)
            tools = info.get("tools", [])
            print(f"  {s}: {cnt} tools {tools[:3]}")
    results["servers"] = "OK"
except Exception as e:
    print(f"Servers: {type(e).__name__}")
    results["servers"] = str(e)[:30]

# 3) Unified routing
try:
    r = httpx.post("http://127.0.0.1:9001/unified", 
        json={"query": "what is openclaw", "user_id": "test"},
        timeout=30)
    data = r.json()
    print(f"Unified route: {data.get('routed_to')}")
    results["unified"] = "OK"
except Exception as e:
    print(f"Unified: {type(e).__name__}")
    results["unified"] = str(e)[:30]

# 4) System tools
try:
    r = httpx.post("http://127.0.0.1:9001/system/list_tools", json={}, timeout=10)
    print(f"System tools: {r.status_code}")
    results["system"] = "OK"
except Exception as e:
    print(f"System: {type(e).__name__}")
    results["system"] = str(e)[:30]

print(f"\nResults: {results}")
print("ALL TESTS COMPLETE")
