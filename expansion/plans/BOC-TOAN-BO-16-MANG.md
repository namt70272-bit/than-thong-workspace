# KẾ HOẠCH BÓC TÁCH TOÀN BỘ 16 MẢNG

**Ngày:** 2026-05-13  
**Nguyên tắc:** Local-first, qua thần thông gate, mảng nào theo mảng đó, không lẫn.  
**Pipeline:** Source zip → đọc → chắt lọc → candidate → validate → deep-validate → sync → rollback

---

## CẤU TRÚC MỖI MẢNG (điền dần)

### 01 — Quản lý agent
| Level | Làm gì | Source | Candidate | Đích cuối |
|---|---|---|---|---|
| L0 | ✅ A0 tóm tắt | Hello-Agent, AgentScope, Agent365 | `than-thong-wave2-agent-a0-summary.md` | `references/agent-patterns/` |
| L2 | Bóc role patterns + multi-agent layout | Hello-Agent/README, AgentScope/docs | `Imports-du-kien/` | `references/agent-patterns/` |
| L3 | Trích orchestration concepts | AgentScope architecture | `Imports-du-kien/` | `references/agent-architecture/` |
| L4 | Tạo sample agent layout | Hello-Agent co-creation projects | `Imports-du-kien/` | `examples/agent-layouts/` |

**Source zip:** Hello-Agent.zip, AgentScope.zip, Agent365-CôngCụDev.zip

### 02 — Quản lý công việc
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | ClawTeam, LậpKếHoạch | `references/work-management/` |
| L2 | Trích team workflow | ClawTeam README + SKILL + workflows refs | `references/work-management/` |
| L3 | Tạo planning template | LậpKếHoạch content | `examples/work-management/` |

### 03 — Tự động hóa
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | Lobster, TựĐộng, Cognee-n8n | `references/automation/` |
| L2 | Trích workflow DSL pattern | Lobster README + src concepts | `references/automation/` |
| L3 | Tạo pipeline mẫu | TựĐộng-NghiênCứuSâu workflow | `examples/automation/` |
| L4 | Trích n8n integration pattern | Cognee-n8n | `references/automation/` |

### 04 — Tổ chức tri thức / memory
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | Claw-Mesh, Obsidian, MemPalace | `references/memory-knowledge/` |
| L2 | Trích ontology mesh | Claw-Mesh README + QUICKSTART + SKILL | `references/agent-mesh/` |
| L3 | Trích vault structure | Obsidian-LLM-Wiki yaml examples | `examples/knowledge-structures/` |
| L4 | Trích conceptual memory model | MemPalace, Memorix | `references/memory-knowledge/` |

### 05 — Quản lý code
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | OpenCode, GitNexus, Git-Cliff | `references/code-management/` |
| L2 | Trích review workflow | OpenCode workspace concept | `references/code-management/` |
| L3 | Trích changelog/release pattern | Git-Cliff README | `examples/code-review/` |

### 06 — Quản trị hệ thống
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | BảoTrì, QuảnTrịSite, Nix | `references/system-admin/` |
| L2 | Trích checklist maintenance | BảoTrìMáyChủ SKILL + servers schema | `references/system-admin/` |
| L3 | Trích site admin flow | QuảnTrịSite manifest | `references/system-admin/` |
| L4 | Trích deploy philosophy | Nix-OpenClaw docs/RFC | `references/infrastructure/` |

### 07 — Tích hợp API
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | API-Mới, FastAPI, Chat2API | `references/api-integration/` |
| L2 | Trích route structure | FastAPI-MẫuFullStack folder layout | `examples/api-contracts/` |
| L3 | Trích auth flow pattern | Chat2API proxy pattern | `references/api-integration/` |
| L4 | Trích endpoint schema | API-Mới, BộAPIBackend | `examples/api-contracts/` |

### 08 — Hệ thống tra cứu
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | Spy-TìmKiếm, Tavily, FireCrawl | `references/retrieval/` |
| L2 | Trích query pipeline | Spy-TìmKiếm config example + docs | `references/retrieval/` |
| L3 | Trích capability map | FireCrawl README capabilities | `references/retrieval/` |
| L4 | Trích search patterns | ScanAI pipeline | `examples/retrieval/` |

### 09 — Mạng agent
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | Claw-Mesh, CC-ChuyểnMạch | `references/agent-mesh/` |
| L2 | Bóc ontology graph | Claw-Mesh ontology jsonl | `Imports-du-kien/` |
| L3 | Trích session manager idea | CC-ChuyểnMạch session-manager.md | `references/agent-mesh/` |

### 10 — Tài liệu tổ chức
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | TàiLiệu, XâyApp, MẫuClone | `references/documentation/` |
| L2 | Trích doc framework | TàiLiệu docs/plan/index | `references/documentation/` |
| L3 | Trích methodology | XâyAppVớiAgentAI, YTưởngThànhSảnPhẩm | `references/documentation/` |
| L4 | Trích planning template | MẫuCloneWeb-AI structure | `examples/documentation/` |

### 11 — Cấu hình / tuân thủ
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | SystemPrompt, Prompt-LặpLại | `references/compliance/` |
| L2 | Bóc prompt database | SystemPrompt-MôHình toàn bộ Prompt.txt | `config/prompt-templates/` |
| L3 | Tạo prompt pack (Anthropic, Cursor, Devin, Windsurf...) | SystemPrompt từng tool | `config/prompt-templates/` |
| L4 | Trích prompt engineering guide | Prompt-LặpLại README + runbook | `references/compliance/` |

### 12 — Hệ thống CLI
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | OpenCLI, CLI-ProxyAPI, x-cmd | `references/cli-patterns/` |
| L2 | Trích command UX pattern | OpenCLI help/command structure | `references/cli-patterns/` |
| L3 | Trích CLI contract ideas | CLI-ProxyAPI | `examples/cli-specs/` |

### 13 — Quản lý tài liệu
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | MarkText, DesignMD, Concept-Imprint | `references/document-management/` |
| L2 | Trích doc template structure | MarkText docs | `examples/document-templates/` |
| L3 | Trích design system template | Concept-Imprint, acpx-ThưViện | `references/document-management/` |

### 14 — Quản lý nội dung
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | OpenClaw-QuảnLý, DựÁn, CộngĐồng | `references/content-management/` |
| L2 | Trích content workflow | Voice-CộngĐồng-QuyTrình docs | `examples/content-workflows/` |

### 15 — Điều khiển thiết bị / browser
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | Browser-Dùng, desktop-control | `references/device-control/` |
| L2 | Trích boundary pattern | Browser-Dùng docs | `references/device-control/` |

### 16 — Hạ tầng / deploy / platform
| Level | Làm gì | Source | Đích cuối |
|---|---|---|---|
| L0 | ✅ A0 | Clawdinators, Nix-OpenClaw, Terraform | `references/infrastructure/` |
| L2 | Trích RFC architecture | Nix-OpenClaw docs/rfc/* | `references/infrastructure/` |
| L3 | Trích deploy philosophy | Clawdinators generic/specific layer | `references/infrastructure/` |
| L4 | Trích infra template | Terraform-Spec-Test, Ansible | `examples/infrastructure/` |

---

## THỨ TỰ ƯU TIÊN (theo giá trị nhất → dễ nhất)

| Ưu tiên | Mảng | Lý do |
|---|---|---|
| 🔴 1 | **11** Cấu hình / tuân thủ | Prompt database sẵn sàng để bóc |
| 🔴 2 | **04** Tổ chức tri thức | Ontology mesh + vault structure |
| 🟡 3 | **01** Quản lý agent | Agent patterns cụ thể |
| 🟡 4 | **03** Tự động hóa | Workflow DSL + pipeline |
| 🟡 5 | **10** Tài liệu tổ chức | Doc framework + methodology |
| 🟢 6 | **07** Tích hợp API | Route + auth patterns |
| 🟢 7 | **08** Hệ thống tra cứu | Query pipeline + capabilities |
| 🟢 8 | **16** Hạ tầng / deploy | RFC + deploy philosophy |
| 🔵 9-16 | Còn lại | Làm dần theo thời gian |

---

## QUY TRÌNH MỖI LẦN BÓC

Cho mỗi source zip:

```
1. Mở zip, đọc nội dung
2. Chắt lọc phần an toàn (docs/templates/rules)
3. Ghi A0-EXTRACTION record
4. Tạo candidate file vào staging (04-Imports-du-kien)
5. Thần thông gate -> import_orchestrator -> validate -> deep-validate -> sync -> rollback
```

## KHÔNG LÀM
- Không copy nguyên zip vào workspace
- Không nhập code runtime/service/docker/db
- Không cài package từ source
- Không import vào skills/ trực tiếp
- Không phá cấu trúc mảng — mảng nào ở mảng đó
