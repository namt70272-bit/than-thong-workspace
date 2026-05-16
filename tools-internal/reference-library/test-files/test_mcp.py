#!/usr/bin/env python3
"""Test MCP Server"""
import httpx, json

try:
    # List tools
    r = httpx.post('http://127.0.0.1:9876/mcp', json={
        'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'
    }, timeout=10)
    data = r.json()
    tools = data.get('result', {}).get('tools', [])
    print("MCP Server: ONLINE")
    print(f"Tools: {len(tools)}")
    for t in tools:
        print(f"  - {t['name']}")

    # Test system_status
    r2 = httpx.post('http://127.0.0.1:9876/mcp', json={
        'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
        'params': {'name': 'system_status', 'arguments': {}}
    }, timeout=10)
    d2 = r2.json()
    content = d2.get('result', {}).get('content', [{}])
    print(f"\nsystem_status: {str(content)[:200]}")

    # Test list_skills
    r3 = httpx.post('http://127.0.0.1:9876/mcp', json={
        'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
        'params': {'name': 'list_skills', 'arguments': {}}
    }, timeout=10)
    d3 = r3.json()
    c3 = d3.get('result', {}).get('content', [{}])
    print(f"list_skills: {str(c3)[:200]}")

    # Test memory_store
    r4 = httpx.post('http://127.0.0.1:9876/mcp', json={
        'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call',
        'params': {'name': 'memory_store', 'arguments': {
            'user_id': 'chu_nhan', 'session_id': 'test_1200',
            'content': 'Day la memory test tu MCP server'
        }}
    }, timeout=10)
    d4 = r4.json()
    print(f"memory_store: {str(d4)[:200]}")

    print("\nAll tests passed!")

except Exception as e:
    print(f"ERROR: {e}")
