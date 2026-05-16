#!/usr/bin/env python
"""Web UI Dashboard - port 8080"""
import os, sys, json, httpx
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
TOOLS = ROOT / "tools-internal"
SKILLS = ROOT / "skills"
REF = TOOLS / "reference-library"

app = FastAPI(title="OpenClaw Dashboard")

MCP_SERVERS = {
    "system": ("System", "http://127.0.0.1:9876/mcp"),
    "memory": ("Memory", "http://127.0.0.1:9877/mcp"),
    "search": ("Search", "http://127.0.0.1:9878/mcp"),
    "llm": ("LLM", "http://127.0.0.1:9879/mcp"),
}

CSS = (
    "*{margin:0;padding:0;box-sizing:border-box}"
    "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px}"
    ".container{max-width:1200px;margin:0 auto}"
    "h1{color:#58a6ff;font-size:24px;margin-bottom:20px}"
    "h2{color:#8b949e;font-size:16px;margin:15px 0 10px;text-transform:uppercase}"
    ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-bottom:20px}"
    ".card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:15px}"
    ".card h3{color:#58a6ff;font-size:14px;margin-bottom:8px}"
    ".card .value{font-size:28px;font-weight:bold}"
    ".status{display:inline-block;padding:2px 8px;border-radius:12px;font-size:12px;margin-left:8px}"
    ".up{background:#1b4a2b;color:#3fb950}"
    ".down{background:#4a1b1b;color:#f85149}"
    ".server-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-bottom:20px}"
    ".server{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px}"
    ".server h4{color:#58a6ff;font-size:13px}"
    ".server .port{color:#8b949e;font-size:11px}"
    "pre{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:10px;font-size:12px;overflow-x:auto;max-height:400px}"
    ".search-box{display:flex;gap:10px;margin-bottom:15px}"
    ".search-box input{flex:1;padding:10px;background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#c9d1d9;font-size:14px}"
    ".search-box button{padding:10px 20px;background:#238636;color:#fff;border:none;border-radius:6px;cursor:pointer}"
    ".footer{color:#8b949e;font-size:12px;margin-top:30px;text-align:center}"
)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    try:
        skills = len([d for d in os.listdir(str(SKILLS)) if os.path.isdir(Path(str(SKILLS), d))]) if SKILLS.exists() else 0
        ref_scripts = sum(len(files) for _, _, files in os.walk(str(REF))) if REF.exists() else 0
        
        servers_html = ""
        for key, (name, url) in MCP_SERVERS.items():
            port = url.split(":")[2].split("/")[0]
            try:
                async with httpx.AsyncClient(timeout=2) as client:
                    r = await client.post(url, json={"jsonrpc":"2.0","id":"ping","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"dash","version":"1"}}}, headers={"Accept":"application/json,text/event-stream"})
                servers_html += f'<div class="server"><h4>{name} <span class="status up">UP</span></h4><div class="port">Port {port}</div></div>'
            except:
                servers_html += f'<div class="server"><h4>{name} <span class="status down">DOWN</span></h4><div class="port">Port {port}</div></div>'
        
        mem_dir = TOOLS / "agent-memory"
        memory_html = "<p>No memories yet</p>"
        if mem_dir.exists():
            total = 0
            users = 0
            for f in list(mem_dir.glob("*.json")):
                users += 1
                try: total += len(json.loads(f.read_text(encoding="utf-8")))
                except: pass
            memory_html = f"<p>{users} users, {total} entries</p>"
        
        env_path = TOOLS / ".env"
        api_keys = 0
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if "=" in line and not line.startswith("#"):
                    api_keys += 1
        
        timestamp = __import__("datetime").datetime.now().strftime("%H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html><head><title>OpenClaw Dashboard</title><style>{CSS}</style></head>
<body><div class="container">
<h1>&#128065; OpenClaw Dashboard</h1>
<div class="grid">
<div class="card"><h3>Skills</h3><div class="value">{skills}</div></div>
<div class="card"><h3>Reference Scripts</h3><div class="value">{ref_scripts}</div></div>
<div class="card"><h3>Console Commands</h3><div class="value">24</div></div>
<div class="card"><h3>API Keys</h3><div class="value">{api_keys}</div></div>
</div>
<h2>MCP Servers</h2>
<div class="server-grid">{servers_html}</div>
<h2>Memory</h2><div class="card">{memory_html}</div>
<h2>Search</h2>
<div class="search-box">
<input type="text" id="searchQuery" placeholder="Search web...">
<button onclick="searchWeb()">Search</button>
</div>
<div class="card"><pre id="searchResult">Enter query to search</pre></div>
<div class="footer">Gateway: <a href="http://127.0.0.1:9001">localhost:9001</a> | {timestamp}</div>
</div>
<script>
async function searchWeb() {{
    const q=document.getElementById('searchQuery').value;
    document.getElementById('searchResult').textContent='Searching...';
    try {{
        const r=await fetch('/api/search',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{query:q}})}});
        const d=await r.json();
        document.getElementById('searchResult').textContent=JSON.stringify(d,null,2);
    }} catch(e) {{
        document.getElementById('searchResult').textContent='Error: '+e;
    }}
}}
</script>
</body></html>"""
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error</h1><pre>{e}</pre>", status_code=500)

@app.post("/api/search")
async def api_search(request: Request):
    body = await request.json()
    query = body.get("query", "")
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(MCP_SERVERS["system"][1], json={
                "jsonrpc":"2.0","id":"s","method":"tools/call",
                "params":{"name":"web_search","arguments":{"query":query,"limit":3}}
            }, headers={"Accept":"application/json,text/event-stream"})
            return r.json()
    except Exception as e:
        return {"error": str(e)[:100]}

if __name__ == "__main__":
    print("Dashboard: http://127.0.0.1:8080")
    uvicorn.run(app, host="127.0.0.1", port=8080)
