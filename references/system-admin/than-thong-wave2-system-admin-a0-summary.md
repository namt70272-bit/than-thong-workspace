# A0 — Quản trị hệ thống

## Đã xác nhận an toàn tuyệt đối để lấy trước

### 1) BảoTrìMáyChủ-KỹNăng
**Chỉ lấy:**
- `README.md`
- `SKILL.md`
- `servers.json` chỉ để xem schema

**Không lấy:**
- `check.sh`
- `cleanup.sh`
- `maintain-all.sh`

**Giá trị:**
- checklist server maintenance
- schema quản lý nhiều server

### 2) QuảnTrịSite
**Chỉ lấy:**
- `README.md`
- `flows/*/manifest.json`
- cấu trúc flow package

**Không lấy:**
- `clean.js`
- `flow.js`
- assets/function app thật

### 3) Nix-OpenClaw / Clawdinators
**Chỉ lấy:**
- `README.md`
- `docs/agent-first.md`
- `docs/golden-paths.md`
- `docs/rfc/*`
- `AGENTS.md`

**Không lấy:**
- `flake.nix` để apply thật
- workflow CI
- secrets/deploy steps

## Kết luận
A0 mảng này rất tốt để lấy triết lý deploy, checklist và separation of concerns; chưa động gì tới máy thật.
