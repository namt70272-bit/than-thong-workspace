# Engram folder map — pre-import review

Source: `G:\da xong\engram-memory-community-main`

## Sơ đồ nhanh

- `.engram/` ⚠️ runtime state mẫu
  - `graph.kuzu`
  - `hash_index.pkl`
  - `hot_tier.json`
- `config/` ⚠️ cấu hình tích hợp OpenClaw
  - `openclaw-config.json`
  - `docker-compose.yml`
- `plugin/` 🔥 plugin OpenClaw chính
  - `index.js`
  - `openclaw.plugin.json`
  - `package.json`
- `scripts/` 🔥 script cài đặt / memory ops / MCP helper
- `src/` 🔥 lõi recall engine + `index.ts`
- `docker/` 🔥 service stack all-in-one / fastembed / mcp
- `skills/openclaw/` ⚠️ skill + plugin bản phụ
- `openclaw.plugin.json` / `plugin.py` ⚠️ entry ở root
- `docs/` ✅ tài liệu kiến trúc / giới hạn / integration
- `bridge/` 🟡 bridge/CLI phụ trợ
- `context/` 🟡 context tools phụ trợ
- `packages/mcp-server-node/` 🟡 Node MCP server riêng
- `sdks/` ✅ SDK mẫu, ít rủi ro
- `vendor/graphify/` ⚠️ code vendored, cần check license + upstream
- `benchmarks/`, `examples/`, `assets/`, `.claude/`, `bin/` ✅ phụ trợ

## Chỗ phải soi kỹ nhất trước khi import

1. `.engram/`
   - Không bê thẳng vào production như data thật.
   - Xem như sample/local state cho repo này.

2. `plugin/` + root `openclaw.plugin.json` + `plugin.py`
   - Đây là bề mặt tích hợp trực tiếp với OpenClaw.
   - Phải check hook, tool registration, command path, plugin format.

3. `scripts/install-plugin.sh`
   - Có thể ghi vào config/plugin path cũ.
   - Không chạy thẳng trước khi review xong.

4. `config/openclaw-config.json`
   - Cần so với config OpenClaw hiện tại ở E để tránh đè `memory-core`.

5. `docker/` + `docker-compose.yml`
   - Xem nó giả định port nào (`6333`, `11435`, `8585`) và service nào đã có sẵn.

6. `src/recall/*`
   - Đây là lõi thật: hot tier, graph, hasher, recall engine.
   - Cần xác nhận logic có đáng dùng và không phải demo-only.

7. `vendor/graphify/`
   - Cần check đây là vendor nguyên bản hay fork sửa tay, và có dependency gì kéo theo.

## Thứ tự đọc kỹ trước khi copy sang E

1. `README.md`
2. `README-community.md`
3. `docs/OPENCLAW_INTEGRATION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/LIMITATIONS.md`
6. `config/openclaw-config.json`
7. `plugin/openclaw.plugin.json`
8. `plugin/index.js`
9. `scripts/install-plugin.sh`
10. `src/index.ts`
11. `src/recall/*`
12. `docker/all-in-one/*`
13. `vendor/graphify/*`
14. `.engram/*`

## Kết luận hiện tại

Có thể khai thác được, nhưng chưa nên bê sang E để dùng ngay.
Đúng quy trình là: đọc kỹ nhóm file nóng ở trên, rồi mới copy repo sang E ở chế độ review candidate.
