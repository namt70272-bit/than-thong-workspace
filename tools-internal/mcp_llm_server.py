
#!/usr/bin/env python
"""MCP LLM Server - port 9879 (uses local Ollama)"""
import os, sys
try:
    import ollama
    from fastmcp import FastMCP
    mcp = FastMCP("LLM Server")
    
    MODEL = "qwen2.5-coder:7b"
    
    @mcp.tool()
    def chat(prompt: str, system: str = "You are a helpful AI assistant."):
        """Chat with local LLM"""
        resp = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ])
        return resp["message"]["content"]
    
    @mcp.tool()
    def list_models():
        """List available local models"""
        models = ollama.list()
        return [m.model for m in (models.get("models") or [])]
    
    import asyncio
    asyncio.run(mcp.run_http_async(host="127.0.0.1", port=9879))
except Exception as e:
    print(f"LLM server error: {e}")
