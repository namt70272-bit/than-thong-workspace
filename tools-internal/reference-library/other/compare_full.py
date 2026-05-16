#!/usr/bin/env python3
"""SO SANH G:\Ai vs E: - CHI TIET tung muc: trung / khong trung"""
import zipfile, os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

G = r'G:\Ai'
E = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace'

# === B1. Index everything in E ===
# Files
e_file_index = {}  # basename.lower() -> set of rel paths
e_dir_index = set()
e_readme_content = {}  # dedup by MD5 of first 500 chars
e_skill_names = set()
e_skill_dir_names = set()
e_imports = set()  # python imports found
e_unique_files = set()  # paths that are truly unique

for root, dirs, files in os.walk(E):
    rel = os.path.relpath(root, E)
    for f in files:
        lname = f.lower()
        if lname not in e_file_index:
            e_file_index[lname] = set()
        e_file_index[lname].add(os.path.join(rel, f).lower())
        e_unique_files.add(os.path.join(rel, f).lower())
    for d in dirs:
        e_dir_index.add(d.lower())
        if 'skills' in rel:
            e_skill_dir_names.add(d.lower())

# Skill names
skdir = os.path.join(E, 'skills')
if os.path.exists(skdir):
    for s in os.listdir(skdir):
        if os.path.isdir(os.path.join(skdir, s)):
            e_skill_names.add(s.lower())

# Ports in E configs
e_ports = set()
port_pat = re.compile(r'port\s*[:=]\s*(\d+)', re.IGNORECASE)
for root, dirs, files in os.walk(E):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.py', '.ts', '.json', '.yaml', '.yml', '.env', '.conf']: continue
        try:
            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                for m in port_pat.finditer(fh.read()):
                    p = int(m.group(1))
                    if 3000 <= p <= 9999: e_ports.add(p)
        except: pass

# README hashes
def sig(content):
    """Signature of README focus"""
    import hashlib
    return hashlib.md5(content[:600].encode()).hexdigest()[:12]

for root, dirs, files in os.walk(E):
    for f in files:
        if f.lower() == 'readme.md':
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='replace') as fh:
                    content = fh.read(600)
                    s = sig(content)
                    e_readme_content[s] = True
            except: pass

# === B2. Classify each G:\Ai zip ===
skip_non_useful = ['davinci-resolve', 'powershell-7.6', 'camoufox', 'graillon', 'vbcable', 'voicemeeter',
                   'marktext', 'outline-apps', 'seelen-ui', 'win10-gaming', 'winhance', 'winutil', 'sophia',
                   'whisper-bin-x64', 'whispergui', 'comtypes-1.4.16', 'gsnapwin64']

zips = sorted([f for f in os.listdir(G) if f.endswith('.zip')])

# Define categories with priority
HIGH_PRIORITY = [
    'n8n', 'cognee',
    'TaoKyNangAgent', 'TaoKỹNăngAgent', 'agent-skill-creator',
    'CLI2KyNang', 'CLI2KỹNăng', 'cli2skill',
    'KyNang-DongBang', 'KỹNăng-ĐóngBăng', 'skill-freeze',
    'Persona-BaoVe', 'Persona-BảoVệ', 'persona-protect',
    'Salacia-BaoVe', 'Salacia-BảoVệ',
    'MCP-TrungTam', 'MCP-TrungTâm', 'mcp-hub',
    'desktop-control', 
    'YTruong-ThanhSanPham', 'ÝTưởng-ThànhSảnPhẩm', 'idea-to-product',
    'NadirClaw', 'Lobster', 'GBrain', 'Memorix', 'MemPalace', 'MemU', 'memU', 'mem0',
    'FastCode', 'AgentScope', 'Agent365-CongCuDev', 'Agent365-CôngCụDev',
    'Claude-GameStudio', 'Claude-BachTuoc', 'Claude-BạchTuộc', 'claude-octopus',
    'Claude-BanCode', 'Claude-BạnCode', 'claude-code-buddy',
    'Claude-SieuBoNho', 'Claude-SiêuBộNhớ', 'claude-supermemory',
    'CC-ChuyenMach', 'CC-ChuyểnMạch', 'cc-switch',
    'FastMCP', 'FireCrawl', 'Spy-TimKiem', 'Spy-TìmKiếm', 'spy-search',
    'Gemini-LangGraph-KhoiDau', 'Gemini-LangGraph-KhởiĐầu',
    'Browser-Dung', 'Browser-Dùng', 'browser-use',
    'TienIch-TuanThu', 'TiệnÍch-TuânThủ', 'compliance-utility',
    'TaoPromptAgentAI', 'ThietKeHeThongAgent', 'ThiếtKếHệThốngAgent',
    'TuDong-NghienCuuSau', 'TựĐộng-NghiênCứuSâu', 'auto-research',
    'LapKeHoachVoiTep', 'LậpKếHoạchVớiTệp', 'planning-with-files',
    'MauCloneWeb-AI', 'MẫuCloneWeb-AI',
    'CICADA', 'Hermit', 'Claw-Code', 'Claw-Mesh', 'Claw-Rice',
    'OpenCLI', 'Multipass', 'OpenClaw-QuanLy', 'OpenClaw-QuảnLý',
    'OpenClaw-SieuBoNho','OpenClaw-SiêuBộNhớ','OpenClaw-ChatBoNho','OpenClaw-ChatBộNhớ',
    'OpenClaw-DuAn','OpenClaw-DựÁn','Nix-OpenClaw','OpenClaw-Ansible',
    'OpenClaw-WeChat','caldav-calendar','gmail-1.0.6','imap-smtp-email','multi-search-engine',
    'Trust', 'tai-viet',
]

MEDIUM_PRIORITY = [
    'AI-Maestro', 'Spring-AI', 'Hello-Agent', 'LangChain', 'Agent-BoQuanTri', 'Agent-BộQuảnTrị',
    'VuTruAgent', 'VũTrụAgent', 'AgentUniverse',
    'KyNangAgentKhoaHoc', 'KỹNăngAgentKhoaHọc', 'scientific-agent-skills',
    'Chat2API', 'DeepSeek-API-MienPhi', 'DeepSeek-API-MiễnPhí', 'CLI-ProxyAPI',
    'API-Moi', 'API-Mới', 'new-api',
    'GitNexus', 'Gitea-Mirror', 'Git-Cliff',
    'OpenCode', 'Shannon', 'Spark', 'Vibe-Kanban',
    'AntiGravity-KyNangHay', 'AntiGravity-KỹNăngHay',
    'ToiThieuToken-KyNang', 'TốiThiểuToken-KỹNăng', 'token-minimizer',
    'Fincept-Terminal', 'Caclawphony', 'Hudi', 
    'DaAgent-KhoThongMinh', 'ĐaAgent-KhoThongMinh',
    'AI cuc bo', 'AI cục bộ', 'Agency-Agent', 'Agent-Captcha', 'Agent-VuonToi', 'Agent-VươnTới',
    'AI-CapDoi', 'AI-CặpĐôi', 'AI-TiepThi', 'AI-TiếpThị',
    'FastAPI-MauFullStack', 'FastAPI-MẫuFullStack',
    'OpenClawKyNang-Tuyen', 'OpenClawKỹNăng-Tuyển',
    'ClaudeCode-Tuyen', 'ClaudeCode-Tuyển',
    'MemOS-Cloud-OpenClaw-Plugin', 'SystemPrompt-MoHinh-AITools', 'SystemPrompt-MôHình-AITools',
    'Toonify-MCP', 'MCP-MayChu-Tuyen', 'MCP-MáyChủ-Tuyển',
    'Obsidian-LLM-Wiki', 'Obsidian-CauKho', 'Obsidian-CầuKho',
    'OpenClaw-AI', 'OpenClaw',
    'AtomicBot', 'ClawTeam', 'Clawdinators',
    'GRIT', 'HexStrike-AI', 'Kode-Agent',
    'BoNhoAI-Tuyen', 'BộNhớAI-Tuyển',
    'MemUBot', 'memUBot',
    'NanoBrowser', 'Browser-DungDesktop', 'Browser-DùngDesktop',
    'Paperclip', 'Iffy', 'Trust', 'L1B3RT4S', 'MWA',
    'WinForge', 'caldav', 'gmail', 'imap', 'multi-search',
    'ClawHub', 'OpenClaw', 'OpenClaw-QWQ', 
    'Agentscope', 'Agent365-CongCuDev',
]

def classify_zip(fname):
    fname_lower = fname.lower()
    for skip in skip_non_useful:
        if skip in fname_lower: return 'SKIP'
    # N8N
    if any(x in fname_lower for x in ['n8n', 'cognee']): return 'N8N'
    # OpenClaw ecosystem
    if 'openclaw' in fname_lower or 'openclaw' in fname_lower: return 'OPENCLAW'
    if 'atomicbot' in fname_lower: return 'OPENCLAW'
    if any(x in fname_lower for x in ['clawdinators', 'clawteam', 'claw-code', 'claw-mesh', 'claw-rice', 'clawhub']): return 'CLAW'
    # Agent frameworks
    if any(x in fname_lower for x in ['agent-universe', 'vutruagent', 'vũtrụagent']): return 'AGENT-FRAMEWORK'
    if any(x in fname_lower for x in ['ai-maestro']): return 'AGENT-FRAMEWORK'
    if any(x in fname_lower for x in ['spring-ai']): return 'AGENT-FRAMEWORK'
    if any(x in fname_lower for x in ['hello-agent']): return 'AGENT-FRAMEWORK'
    if any(x in fname_lower for x in ['agentscope']): return 'AGENT-FRAMEWORK'
    if any(x in fname_lower for x in ['langchain']): return 'AGENT-FRAMEWORK'
    if any(x in fname_lower for x in ['agent-bo', 'agent-bộ']): return 'AGENT-FRAMEWORK'
    # Agent tools
    if any(x in fname_lower for x in ['taokynang', 'tạokỹnăng', 'cli2ky', 'cli2kỹ', 'persona-b', 'salacia-b',
                                       'ky-nang-dong', 'kỹ-năng-đóng', 'tienich-t', 'tiệnÍch-t',
                                       'fastcode', 'agent365-c', 'agent-captcha', 'agent-vuon', 'agent-vươn',
                                       'maucloneweb', 'mẫucloneweb', 'systemprompt', 'system-prompt',
                                       'self-improving-agent', 'lapkehoach', 'lậpkếhoạch']): return 'AGENT-TOOL'
    # Claude ecosystem
    if any(x in fname_lower for x in ['claude-', 'claudeky', 'claudecode-', 'cc-chuyen', 'cc-chuyển']): return 'CLAUDE'
    # MCP
    if any(x in fname_lower for x in ['mcp-', 'fastmcp', 'toonify']): return 'MCP'
    # Memory
    if any(x in fname_lower for x in ['mem0', 'memu', 'memubot', 'mempalace', 'memorix', 'memos-', 'bonhoai', 'bộnhớai']): return 'MEMORY'
    # Search/Browser
    if any(x in fname_lower for x in ['firecrawl', 'spy-tim', 'spy-tìm', 'browser-d', 'nanobrowser']): return 'SEARCH-BROWSER'
    # API / Gateway
    if any(x in fname_lower for x in ['api-moi', 'api-mới', 'api-tuyen', 'chat2api', 'deepseek-api',
                                       'cli-proxy', 'fastapi-m', 'boapi', 'bộapi']): return 'API-GATEWAY'
    # Skill collections
    if any(x in fname_lower for x in ['antigravity', 'toithieutoken', 'tốithiểutoken', 'designdm', 'claudecode-tuyen',
                                       'openclawky', 'kynangagentkhoa']): return 'SKILL-COL'
    # Misc agent
    if any(x in fname_lower for x in ['agency-agent', 'hexstrike', 'kode-agent', 'ai-cap', 'ai-cặp', 'ai-tiep', 'ai-tiếp',
                                       'ai-cuc', 'ai-cục', 'xayapp', 'xâyapp', 'daagent', 'đaagent',
                                       'grit', 'nairclaw', 'nadirclaw', 'lobster', 'gbrain', 'hermit', 'cicada',
                                       'trust', 'opencli', 'multipass', 'nix-', 'gemini-lang', 'obsidian-llm',
                                       'obsidian-cau', 'tritoe', 'trithong', 'tritue', 'ytruong', 'ýtưởng',
                                       'desktop-control', 'mcp-hub', 'mcp-trung', 'cadlaw', 'caldav', 'gmail-1', 'imap-smtp',
                                       'multi-search', 'planning-with-files', 'auto-research', 'tudong-nghien',
                                       'tựđộng-nghiên', 'thietkehethong', 'thiếtkếhệthống', 'taoprompt', 'tạoprompt',
                                       'bibigpt', 'tai-lieu', 'tàiliệu']): return 'AGENT-TOOL'
    # Other dev tools
    if any(x in fname_lower for x in ['gitnexus', 'gitea', 'git-cliff', 'opencode', 'shannon',
                                       'spark', 'vibe-kanban', 'fincept', 'caclawphony', 'hudi',
                                       'gitnexus', 'paperclip', 'iffy', 'l1b3rt4s', 'mwa', 'winforge',
                                       'tuy-chinh', 'tùychỉnh', 'pc-tinh', 'concept-imprint', 'winforge',
                                       'x-cmd', 'multipass', 'frontend-s', 'open-r1', 'openmythos',
                                       'opensrc', 'openviking', 'vidpipe', 'whispergui', 'yepanywhere',
                                       'jacob', 'jacobo', 'jake-', 'phang', 'phántíchmạng', 'quantri', 'quảntrịsite',
                                       'shnote', 'tanhh', 'tôiquy', 'taiquy', 'taoiweb', 'taoiwep',
                                       'vs-sdk', 'voice-cong', 'terraform', 'tavily']): return 'OTHER-DEV'
    # Not useful
    if any(x in fname_lower for x in ['724-van', '996-ky', 'caldav', 'anki', 'anthill', 'anthill', 'antfarm',
                                       'chatonu', 'congdong', 'cộngđồng', 'gpt-giao', 'gpt-mamo', 'gpt-mãmở',
                                       'hitomi']): return 'MINOR'
    
    return 'UNCATEGORIZED'

# === B3. For each zip check duplicates ===
print("=" * 100)
print("SO SANH G:\\Ai vs E WORKSPACE")
print("=" * 100)

results = {}
cat_results = {}
final_text = "# SO SANH G:\\Ai vs E WORKSPACE\n\n"

# Process by category
for fname in zips:
    cat = classify_zip(fname)
    if cat not in cat_results: cat_results[cat] = []
    cat_results[cat].append(fname)

categories_order = ['AGENT-FRAMEWORK', 'AGENT-TOOL', 'OPENCLAW', 'CLAW', 'CLAUDE', 'N8N', 'MCP',
                    'MEMORY', 'SEARCH-BROWSER', 'API-GATEWAY', 'SKILL-COL', 'OTHER-DEV', 'MINOR', 'SKIP', 'UNCATEGORIZED']

for cat in categories_order:
    items = cat_results.get(cat, [])
    if not items: continue
    if cat == 'SKIP':
        print(f"\n## BO QUA ({len(items)} files)")
        final_text += f"\n## BỎ QUA — driver/audio/video không liên quan\n"
        for fname in items:
            sz = os.path.getsize(os.path.join(G, fname)) / 1048576
            print(f"   {fname} ({sz:.0f}MB)")
        continue
    
    print(f"\n## {cat} ({len(items)} files)")
    final_text += f"\n## {cat}\n\n"
    
    header = f"{'File':45s} {'Size':>8s} {'Files':>6s} {'Trùng?':>10s} {'Chi tiết'}"
    print(header)
    print("-" * 100)
    final_text += f"| {'File':45s} | {'MB':>8s} | {'Files':>6s} | {'Trùng?':>10s} | {'Chi tiết'} |\n"
    final_text += f"|{'-'*47}|{'-'*10}|{'-'*8}|{'-'*12}|{'-'*50}|\n"
    
    for fname in sorted(items):
        fpath = os.path.join(G, fname)
        if not os.path.exists(fpath): continue
        sz = os.path.getsize(fpath) / 1048576
        display_name = fname.replace('.zip', '')
        
        try:
            with zipfile.ZipFile(fpath, 'r') as z:
                names = z.namelist()
                
                # Check duplicates
                dup_basenames = set()
                dup_fullpaths = set()
                dup_skills = set()
                dup_readme_sigs = []
                dup_packages = []
                
                for n in names:
                    base = os.path.basename(n).lower()
                    if base in e_file_index:
                        dup_basenames.add(base)
                    if n.lower() in e_unique_files:
                        dup_fullpaths.add(n.lower())
                    
                    if 'skill.md' in n.lower():
                        parts = n.split('/')
                        for i, p in enumerate(parts):
                            if p == 'skills' and i+1 < len(parts):
                                sname = parts[i+1].lower()
                                if sname in e_skill_names:
                                    dup_skills.add(parts[i+1])
                    
                    if n.lower().endswith('readme.md'):
                        try:
                            content = z.read(n).decode('utf-8', errors='replace')
                            s = sig(content)
                            if s in e_readme_content:
                                dup_readme_sigs.append(n)
                        except: pass
                    
                    if n.lower().endswith('package.json'):
                        try:
                            content = z.read(n).decode('utf-8', errors='replace')
                            pkg = json.loads(content)
                            if 'name' in pkg:
                                dup_packages.append(pkg['name'])
                        except: pass
                
                # Determine dup severity
                skill_dup = len(dup_skills)
                content_dup = len(dup_readme_sigs) + len(dup_packages)
                file_dup = len(dup_basenames) + len(dup_fullpaths)
                
                # Real conflict = skill name or README content dup
                if skill_dup > 0:
                    dup_label = "⚠️ SKILL"
                    dup_detail = f"Trùng skill: {', '.join(dup_skills)[:40]}"
                elif content_dup > 0:
                    dup_label = "⚠️ README"
                    dup_detail = f"Trùng {content_dup} README/package"
                elif file_dup > 5:
                    dup_label = "~ phần"
                    dup_detail = f"Trùng {file_dup-5} tên file chung"
                else:
                    dup_label = "✅ MỚI"
                    dup_detail = f"Không trùng ({file_dup} tên chung)"
                
                # Count code by type
                ts_cnt = len([n for n in names if n.endswith('.ts') and 'node_module' not in n.lower()])
                py_cnt = len([n for n in names if n.endswith('.py') and 'node_module' not in n.lower()])
                skill_cnt = len([n for n in names if 'skill.md' in n.lower()])
                
                code_note = ''
                if ts_cnt: code_note += f' {ts_cnt}.ts'
                if py_cnt: code_note += f' {py_cnt}.py'
                if skill_cnt: code_note += f' {skill_cnt}skill'
                
                detail = f'{code_note} | {dup_detail}'
                
        except Exception as ex:
            names = 0
            dup_label = "❌ LỖI"
            detail = str(ex)[:50]
        
        line = f"{display_name:45s} {sz:8.1f} {len(names) if names else 0:6d} {dup_label:>10s} {detail}"
        print(line)
        
        md_line = f"| {display_name:45s} | {sz:8.1f} | {len(names) if names else 0:6d} | {dup_label:>10s} | {detail} |\n"
        final_text += md_line
    print()

# === Write report ===
with open(os.path.join(E, 'review', 'G-Ai-vs-E-comparison.md'), 'w', encoding='utf-8') as f:
    f.write(final_text)

print("=" * 100)
print("HOAN THANH. Bao cao: review/G-Ai-vs-E-comparison.md")
print("=" * 100)
