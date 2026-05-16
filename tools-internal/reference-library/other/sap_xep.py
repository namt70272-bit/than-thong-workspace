#!/usr/bin/env python3
"""Sap xep 156 file vao cac thu muc phu hop, copy vao E"""
import zipfile, os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

G = r'G:\Ai'
E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'
CANDIDATE = os.path.join(E, 'review', 'candidate')

# === Classification map: filename (without .zip) -> subfolder ===
CLASSIFICATION = {
    # AGENT-FRAMEWORK
    'AgentScope': 'agent-framework',
    'Spring-AI': 'agent-framework',
    'VũTrụAgent': 'agent-framework',
    'LangChain': 'agent-framework',
    'Agent-BộQuảnTrị': 'agent-framework',
    'KỹNăngAgentKhoaHọc': 'agent-framework',
    'TạoKỹNăngAgent': 'agent-framework',
    'ThiếtKếHệThốngAgent': 'agent-framework',
    
    # AGENT-TOOL
    'Agency-Agent': 'agent-tool',
    'Agency-Agent-TQ': 'agent-tool',
    'Agent-VươnTới': 'agent-tool',
    'Agent-Captcha': 'agent-tool',
    'Agent365-CôngCụDev': 'agent-tool',
    'AI-CặpĐôi': 'agent-tool',
    'AI-TiếpThị': 'agent-tool',
    'AI cục bộ': 'agent-tool',
    'CLI2KỹNăng': 'agent-tool',
    'CLI-BấtCứ': 'agent-tool',
    'Kode-Agent': 'agent-tool',
    'HexStrike-AI': 'agent-tool',
    'GRIT': 'agent-tool',
    'CICADA': 'agent-tool',
    'NadirClaw': 'agent-tool',
    'ĐaAgent-KhoThôngMinh': 'agent-tool',
    'XâyAppVớiAgentAI': 'agent-tool',
    'TạoPromptAgentAI': 'agent-tool',
    'TựĐộng-NghiênCứuSâu': 'agent-tool',
    'SystemPrompt-MôHình-AITools': 'agent-tool',
    'MẫuCloneWeb-AI': 'agent-tool',
    'LậpKếHoạchVớiTệp': 'agent-tool',
    'Persona-BảoVệ': 'agent-tool',
    'Salacia-BảoVệ': 'agent-tool',
    'KỹNăng-ĐóngBăng': 'agent-tool',
    'TiệnÍch-TuânThủ': 'agent-tool',
    'desktop-control-1.0.0': 'agent-tool',
    'self-improving-agent-3.0.16': 'agent-tool',
    'BảoTrìMáyChủ-KỹNăng': 'agent-tool',
    'Prompt-LặpLại-V2': 'agent-tool',
    'Hermit': 'agent-tool',
    'ÝTưởng-ThànhSảnPhẩm': 'agent-tool',
    'GBrain': 'agent-tool',
    
    # SKILL COLLECTIONS
    'Paperclip': 'skill-collection',
    'Paperclip-DevModule': 'skill-collection',
    'TốiThiểuToken-KỹNăng': 'skill-collection',
    'KỹNăng-ĐóngBăng': 'skill-collection',
    'PowerPlatform-KỹNăng': 'skill-collection',
    '96-KỹNăng': 'skill-collection',
    '996-KỹNăng': 'skill-collection',
    '724-VănPhòng': 'skill-collection',
    
    # MEMORY
    'mem0': 'memory',
    'memU': 'memory',
    'memUBot': 'memory',
    'MemPalace': 'memory',
    'Memorix': 'memory',
    'BộNhớAI-Tuyển': 'memory',
    'Obsidian-LLM-Wiki': 'memory',
    'Obsidian-CầuKho': 'memory',
    'Gemini-LangGraph-KhởiĐầu': 'memory',
    'GBrain': 'memory',
    
    # SEARCH-BROWSER
    'FireCrawl': 'search-browser',
    'Browser-Dùng': 'search-browser',
    'Browser-DùngDesktop': 'search-browser',
    'NanoBrowser': 'search-browser',
    'Spy-TìmKiếm': 'search-browser',
    'Tavily-SinhKey': 'search-browser',
    
    # MCP
    'FastMCP': 'mcp',
    'Toonify-MCP': 'mcp',
    'MCP-MáyChủ-Tuyển': 'mcp',
    'MCP-TrungTâm': 'mcp',
    
    # API-GATEWAY
    'API-Mới': 'api-gateway',
    'Chat2API': 'api-gateway',
    'DeepSeek-API-MiễnPhí': 'api-gateway',
    'CLI-ProxyAPI': 'api-gateway',
    'FastAPI-MẫuFullStack': 'api-gateway',
    'BộAPIBackend': 'api-gateway',
    'api-gateway-1.0.84': 'api-gateway',
    'GPT-MãMở': 'api-gateway',
    'COAI': 'api-gateway',
    
    # GIT-DEVOPS
    'GitNexus': 'git-devops',
    'Gitea-Mirror': 'git-devops',
    'Git-Cliff': 'git-devops',
    'Terraform-Spec-Test': 'git-devops',
    'VS-SDK-TestFX': 'git-devops',
    
    # CLAW ECOSYSTEM
    'Claw-Code': 'claw-ecosystem',
    'Claw-Mesh': 'claw-ecosystem',
    'Claw-Rice': 'claw-ecosystem',
    'ClawHub': 'claw-ecosystem',
    'ClawTeam': 'claw-ecosystem',
    'Clawdinators': 'claw-ecosystem',
    'Caclawphony': 'claw-ecosystem',
    
    # CLAUDE ECOSYSTEM
    'Claude-BạchTuộc': 'claude',
    'Claude-BạnCode': 'claude',
    'Claude-GameStudio': 'claude',
    'Claude-SiêuBộNhớ': 'claude',
    'ClaudeCode-Tuyển': 'claude',
    'ClaudeKỹNăng-Tuyển': 'claude',
    'ScanAI-ClaudeCode-KỹNăng': 'claude',
    'CC-ChuyểnMạch': 'claude',
    'CC-Cổng': 'claude',
    
    # N8N
    'n8n-workflow-automation-1.0.0': 'n8n',
    'n8n-ServerChan': 'n8n',
    'Cognee-n8n': 'n8n',
    
    # OPENCLAW PLUGINS
    'OpenClaw-AI': 'openclaw-plugins',
    'OpenClaw-Ansible': 'openclaw-plugins',
    'OpenClaw-ChatBộNhớ': 'openclaw-plugins',
    'OpenClaw-DựÁn': 'openclaw-plugins',
    'OpenClaw-QuảnLý': 'openclaw-plugins',
    'OpenClaw-SiêuBộNhớ': 'openclaw-plugins',
    'OpenClaw-WeChat': 'openclaw-plugins',
    'OpenClawKỹNăng-Tuyển': 'openclaw-plugins',
    'Nix-OpenClaw': 'openclaw-plugins',
    'MemOS-Cloud-OpenClaw-Plugin': 'openclaw-plugins',
    'OpenCLI': 'openclaw-plugins',
    'OpenMythos': 'openclaw-plugins',
    'OpenSrc': 'openclaw-plugins',
    'Open-R1': 'openclaw-plugins',
    
    # OTHER
    'OpenCode': 'other',
    'Shannon': 'other',
    'Spark': 'other',
    'Vibe-Kanban': 'other',
    'Fincept-Terminal': 'other',
    'Hudi': 'other',
    'YepAnywhere': 'other',
    'Concept-Imprint': 'other',
    'VidPipe': 'other',
    'Paperclip': 'other',
    'Iffy': 'other',
    'L1B3RT4S': 'other',
    'MWA': 'other',
    'MSDL': 'other',
    'Multipass': 'other',
    'Jake-ĐoLường': 'other',
    'PhânTíchMạngXãHội': 'other',
    'QuảnTrịSite': 'other',
    'ShNote': 'other',
    'Anki-SoạnThảo': 'other',
    'AntFarm': 'other',
    'BibiGPT-XARTGPT': 'other',
    'ChatVôHạn': 'other',
    'Hitomi-Downloader-master': 'other',
    'TàiLiệu': 'other',
    'TốiƯuHệThốngNgười': 'other',
    'TựCodeToànPhần': 'other',
    'PC-TinhChỉnh': 'other',
    'Frontend-SDK': 'other',
    'acpx-ThưViện': 'other',
    'MỹChốngMỹ': 'other',
    'CộngĐồng': 'other',
    'Mạng': 'other',
    'Tavily-SinhKey': 'other',
    'VPN-Tuyển': 'other',
    'Voice-CộngĐồng-QuyTrình': 'other',
    'Windows-Terminal': 'other',
    'WinForge': 'other',
    'x-cmd': 'other',
    'Kuku-Shell': 'other',
    'api-gateway-1.0.84': 'other',
    'caldav-calendar-1.0.1': 'other',
    'gmail-1.0.6': 'other',
    'imap-smtp-email-0.0.13': 'other',
    'multi-search-engine-2.1.3': 'other',
}

# === Do the copy ===
SKIP_LIST = ['davinci-resolve', 'powershell-7.6', 'camoufox', 'graillon', 'vbcable', 'voicemeeter',
             'marktext', 'outline-apps', 'seelen-ui', 'win10-gaming', 'winhance', 'winutil', 'sophia',
             'whisper-bin-x64', 'whispergui', 'comtypes-1.4.16', 'gsnapwin64']
CONFLICT_FILES = ['FastCode.zip', 'OpenClaw.zip', 'OpenClaw-QWQ.zip', 'AtomicBot.zip', 'OpenViking.zip', 'AntiGravity-KỹNăngHay.zip']
BIG_ZIPS = ['AI-Maestro.zip', 'ClawWork.zip', 'Dify-Plugin.zip', 'Hello-Agent.zip', 'n8n.zip']

copied = 0
skipped = 0
not_found = 0
unknown = []
total_size = 0

for fname in os.listdir(G):
    if not fname.endswith('.zip'): continue
    fn = fname.lower()
    
    # Skip filters
    if any(s in fn for s in SKIP_LIST): 
        skipped += 1; continue
    if fname in CONFLICT_FILES: 
        skipped += 1; continue
    if any(b in fn for b in ['ai-maestro', 'clawwork', 'dify-plugin', 'hello-agent']) or fn == 'n8n.zip':
        skipped += 1; continue
    if fname.endswith('.zip') and fn.replace('.zip','').strip() == '':
        skipped += 1; continue
    
    # Find classification
    base = fname.replace('.zip', '')
    folder = CLASSIFICATION.get(base)
    
    if not folder:
        # Try fuzzy match
        for key, val in CLASSIFICATION.items():
            if key.lower() in base.lower() or base.lower() in key.lower():
                folder = val
                break
    
    if not folder:
        unknown.append(fname)
        continue
    
    src = os.path.join(G, fname)
    dst = os.path.join(CANDIDATE, folder, fname)
    sz = os.path.getsize(src)
    
    shutil.copy2(src, dst)
    copied += 1
    total_size += sz

# === Report ===
print("=" * 80)
print(f"DA SAP XEP {copied} FILE VAO {len(os.listdir(CANDIDATE))} THU MUC")
print("=" * 80)
print()

total_mb = total_size / 1048576
print(f"Tong dung luong: {total_mb:.0f} MB")
print()

# Show each folder
for folder in sorted(os.listdir(CANDIDATE)):
    fdir = os.path.join(CANDIDATE, folder)
    if not os.path.isdir(fdir): continue
    files = [f for f in os.listdir(fdir) if f.endswith('.zip')]
    if not files: continue
    folder_sz = sum(os.path.getsize(os.path.join(fdir, f)) for f in files)
    print(f"  📁 {folder}/ ({len(files)} files, {folder_sz/1048576:.0f} MB)")
    for f in sorted(files):
        fsz = os.path.getsize(os.path.join(fdir, f)) / 1024
        print(f"      [{fsz:7.0f}KB] {f.replace('.zip','')}")
    print()

if unknown:
    print(f"\n⚠️ KHONG PHAN LOAI DUOC ({len(unknown)} files):")
    for f in unknown:
        print(f"  - {f}")

print(f"\nSkipped (trung/lon/skip): {skipped}")
print("HOAN THANH.")
