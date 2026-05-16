# A0 — Tổ chức tri thức / memory

## Đã xác nhận an toàn tuyệt đối để lấy trước

### 1) Claw-Mesh
**Chỉ lấy:**
- `README.md`
- `QUICKSTART.md`
- `SKILL.md`
- ontology / kiến trúc mesh ở mức tài liệu

**Không lấy:**
- API/server/runtime code
- workflow phân tán thực thi

**Giá trị:**
- mô hình mesh nhiều agent
- phân tầng governance + data + execution
- ý tưởng tách node role

### 2) Obsidian-LLM-Wiki
**Chỉ lấy:**
- `README.md`
- `vault-mind.example.yaml`
- cấu trúc vault/wiki

**Không lấy:**
- `.env.domestic.example` để dùng thật
- script setup
- MCP/server config

**Giá trị:**
- cách tổ chức kho tri thức
- schema YAML cho tri thức/vault

### 3) MemPalace / Memorix
**Chỉ lấy:**
- conceptual model, naming, structure

**Không lấy:**
- backend/state/migration

## Kết luận
A0 của mảng memory là lấy structure và ontology, chưa chạm backend memory nào.
