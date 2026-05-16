# 👁️ THẦN THÔNG — KẾ HOẠCH NHẬP G:\Ai VÀO E WORKSPACE

> Soạn: 2026-05-14 11:36 GMT+7
> Trạng thái: **SẴN SÀNG THỰC THI**
> Tool import: `tools-internal/than_thong_import_wave.py`

---

## Nguyên tắc vận hành

- **Mỗi bước đều qua thần thông gate** trước
- **Backup** trước mọi thao tác ghi đè
- **Rollback manifest** để hoàn tác bất kỳ lúc nào
- **Không copy bulk** — chỉ extract tinh hoa (SKILL.md, script .py, config)
- **File trùng hoàn toàn** → bỏ qua
- **File >100MB** → bỏ qua đợt này

---

## 6 GIAI ĐOẠN THỰC THI

### 🥇 GIAI ĐOẠN 1: Skills & Agent Tools
**Nội dung:** 36 files từ `agent-tool/`  
**Hành động:** `extract-skills` → `register-skills`  
**Công cụ:** `than_thong_import_wave.py execute skills-agent-tools`  
**Rủi ro:** Thấp — chỉ thêm skills mới, bỏ qua nếu trùng tên

| File | Dung lượng | Ghi chú |
|------|-----------|---------|
| AI cục bộ | 8.1MB | Skill collection |
| CLI-BấtCứ | 6.6MB | Any CLI → Skill |
| ĐaAgent-KhoThôngMinh | 2.3MB | Multi-agent |
| HexStrike-AI | 2.0MB | AI tool |
| Agent365-CôngCụDev | 1.1MB | Tools dev |
| NadirClaw | 1.8MB | Claw skill |
| Kode-Agent | 1.2MB | Agent framework |
| MẫuCloneWeb-AI | 1.0MB | Web clone |
| TựĐộng-NghiênCứuSâu | 985KB | Deep research |
| Agency-Agent (-TQ) | 873KB ×2 | Agent agency |
| ... + 25 files nhỏ | <500KB mỗi file | Skills lẻ |

### 🥈 GIAI ĐOẠN 2: OpenClaw Plugins & Claw Ecosystem
**Nội dung:** 21 files từ `openclaw-plugins/` + `claw-ecosystem/`  
**Hành động:** `extract-skills` → `extract-scripts` → backup trước  
**Công cụ:** `than_thong_import_wave.py execute openclaw-plugins`  
**Rủi ro:** Trung bình — có thể ghi đè file E nếu trùng tên

| File | Dung lượng | Ghi chú |
|------|-----------|---------|
| Caclawphony | 30MB | Claw music |
| Clawdinators | 12MB | Claw tools |
| ClawTeam | 8.7MB | Claw team |
| Claw-Code | 5.1MB | Claw coding |
| ClawHub | 4.1MB | Claw hub |
| Claw-Mesh | 466KB | Claw mesh |
| Claw-Rice | 48KB | Claw rice |
| OpenClaw-AI | 867KB | AI plugin |
| OpenClaw-QuảnLý | 1.1MB | Management |
| OpenCLI | 348KB | CLI tool |
| Nix-OpenClaw | 1.4MB | Nix config |
| MemOS-Cloud-Plugin | 20KB | Cloud plugin |
| ... + 8 plugins nhỏ | | WeChat, DựÁn, Ansible... |

### 🥉 GIAI ĐOẠN 3: API Gateway & MCP
**Nội dung:** 12 files từ `api-gateway/` + `mcp/`  
**Hành động:** `extract-scripts` → `validate` (check port trước)  
**Công cụ:** `than_thong_import_wave.py execute api-mcp`  
**Rủi ro:** Trung bình — cần kiểm tra port conflict

| File | Dung lượng | Ghi chú |
|------|-----------|---------|
| GPT-MãMở | 31.5MB | GPT OSS |
| FastMCP | 8.5MB | MCP framework |
| COAI | 6.4MB | CO AI |
| Chat2API | 5.1MB | Chat API |
| API-Mới | 3.0MB | New API |
| DeepSeek-API-MiễnPhí | 2.3MB | DeepSeek free API |
| CLI-ProxyAPI | 1.4MB | CLI proxy |
| FastAPI-MẫuFullStack | 823KB | Fullstack template |
| BộAPIBackend | 57KB | Backend kit |
| MCP-MáyChủ-Tuyển | 21KB | MCP server |
| Toonify-MCP | 117KB | Toonify |
| MCP-TrungTâm | 0KB | Docs |

### 4️⃣ GIAI ĐOẠN 4: Memory & Browser Tools
**Nội dung:** 15 files từ `memory/` + `search-browser/`  
**Hành động:** `extract-scripts` → `validate` (extract selective)  
**Công cụ:** `than_thong_import_wave.py execute memory-browser`  
**Rủi ro:** Cao — file lớn (FireCrawl 31MB, mem0 20MB, BộNhớAI 30MB)

| File | Dung lượng | Ghi chú |
|------|-----------|---------|
| BộNhớAI-Tuyển | 30MB | Memory collection |
| FireCrawl | 31MB | Web crawl |
| Spy-TìmKiếm | 15MB | Search |
| mem0 | 20MB | Memory layer |
| memU | 12MB | Memory utility |
| memUBot | 8.3MB | Memory bot |
| Browser-Dùng | 1.7MB | Browser tool |
| Memorix | 1.5MB | Memory |
| Obsidian-LLM-Wiki | 1.2MB | Wiki |
| MemPalace | 759KB | Memory palace |
| GBrain | 755KB | Brain memory |
| NanoBrowser | 465KB | Browser |
| Gemini-LangGraph | 348KB | LangGraph |
| Obsidian-CầuKho | 194KB | Bridge |
| Browser-DùngDesktop | 135KB | Desktop browse |

### 5️⃣ GIAI ĐOẠN 5: Agent Frameworks (READ-ONLY)
**Nội dung:** 8 files từ `agent-framework/`  
**Hành động:** `read-only` — đọc tham khảo, không copy  
**Công cụ:** Thủ công — không dùng import_wave  
**Rủi ro:** Thấp — chỉ đọc

| File | Dung lượng | Ghi chú |
|------|-----------|---------|
| Spring-AI | 60.3MB | Spring AI |
| VũTrụAgent (AgentUniverse) | 51.9MB | Agent universe |
| KỹNăngAgentKhoaHọc | 28.6MB | 134 skills |
| LangChain | 17.3MB | LangChain |
| TạoKỹNăngAgent | 15.8MB | Skill creator |
| Agent-BộQuảnTrị | 17.0MB | Gov toolkit |
| ThiếtKếHệThốngAgent | 9.9MB | System design |
| AgentScope | 6.5MB | Agent scope |

### 6️⃣ GIAI ĐOẠN 6: Other Utilities (FILTERED)
**Nội dung:** 55 files từ `other/`  
**Hành động:** `extract-scripts` — **lọc thêm trước khi làm**  
**Công cụ:** `than_thong_import_wave.py execute other-utilities`  
**Rủi ro:** Cao — 489MB. Chỉ lấy file <5MB. Bỏ qua codebase lớn.

**Sẽ bỏ qua (quá lớn, không liên quan):**
- OpenCode (84MB), Shannon (67MB), Spark (66MB), Vibe-Kanban (61MB)
- MỹChốngMỹ (32MB), TàiLiệu (30MB), Hudi (24MB), Fincept-Terminal (19MB)
- AntFarm (15MB), Concept-Imprint (13MB), PhânTíchMạngXH (12MB)

**Sẽ lấy (file nhỏ, có ích):**
- acpx-ThưViện, YepAnywhere, Tavily-SinhKey, Lobster, Iffy
- Desktop tools: PC-TinhChỉnh, ShNote, VidPipe, Frontend-SDK, Cursor-TrợGiúp
- Scripts nhỏ: x-cmd, api-gateway-1.0.84, multi-search-engine
- Services: caldav-calendar, gmail, imap-smtp-email, VPN-Tuyển
- Skills/Collections nhỏ: DesignMD-Tuyển, Paperclip, PowerPlatform-KỹNăng

---

## LỆNH THỰC THI

```powershell
# Xem kế hoạch
python tools-internal\than_thong_import_wave.py plan

# Thực thi từng giai đoạn
python tools-internal\than_thong_import_wave.py execute skills-agent-tools
python tools-internal\than_thong_import_wave.py execute openclaw-plugins
python tools-internal\than_thong_import_wave.py execute api-mcp
python tools-internal\than_thong_import_wave.py execute memory-browser
python tools-internal\than_thong_import_wave.py execute other-utilities

# Hoàn tác nếu lỗi
python tools-internal\than_thong_import_wave.py rollback skills-agent-tools
python tools-internal\than_thong_import_wave.py rollback <wave_name>

# Kiểm tra sau mỗi bước
python tools-internal\scripts\than_thong_console.py preflight
python tools-internal\scripts\than_thong_console.py dashboard
```

---

## THỜI GIAN DỰ KIẾN

| Giai đoạn | Thời gian | Ghi chú |
|-----------|:---------:|---------|
| GĐ1: Skills & Agent Tools | ~3-5 phút | Extract nhanh, file nhỏ |
| GĐ2: OpenClaw Plugins | ~2-3 phút | File vừa, cần backup |
| GĐ3: API Gateway & MCP | ~3-5 phút | Cần đọc port config |
| GĐ4: Memory & Browser | ~5-8 phút | File lớn, extract selective |
| GĐ5: Frameworks (read) | ~2 phút | Chỉ đọc |
| GĐ6: Other (filtered) | ~5-10 phút | Lọc thêm trước |
| **Tổng** | **~20-35 phút** | |

---

## ROLLBACK

Nếu có vấn đề sau khi import:
```powershell
# Rollback từng wave
python tools-internal\than_thong_import_wave.py rollback skills-agent-tools

# Kiểm tra dashboard
python tools-internal\scripts\than_thong_console.py dashboard
```

Mỗi wave có manifest riêng trong `tools-internal/records/rollback-<wave>.json`.

---

*Kế hoạch được thần thông gate phê duyệt. Sẵn sàng thực thi khi Chủ Nhân OK.*
