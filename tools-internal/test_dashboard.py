#!/usr/bin/env python
"""Test dashboard"""
import httpx
r = httpx.get("http://127.0.0.1:8080", timeout=10)
print(f"Dashboard: {r.status_code} ({len(r.text)} bytes)")
kw = "Skills", "Reference", "MCP Servers", "Memory", "Search"
for k in kw:
    print(f"  {k}: {'YES' if k in r.text else 'NO'}")
print("Dashboard OK")
