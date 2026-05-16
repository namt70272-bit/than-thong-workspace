# A0 — Hạ tầng / deploy / platform

## Đã xác nhận an toàn tuyệt đối để lấy trước

### 1) Nix-OpenClaw
**Chỉ lấy:**
- `README.md`
- `docs/agent-first.md`
- `docs/golden-paths.md`
- `docs/plugins-maintainers.md`
- `docs/rfc/*`

**Không lấy:**
- `flake.nix`
- `flake.lock`
- CI/workflow apply

### 2) Clawdinators
**Chỉ lấy:**
- `README.md`
- `AGENTS.md`
- mô hình `generic layer` vs `specific layer`

**Không lấy:**
- deployment configs
- secrets paths
- cloud apply steps

### 3) Terraform-Spec-Test / OpenClaw-Ansible
**Chỉ lấy:**
- docs/template structure

**Không lấy:**
- apply scripts

## Kết luận
A0 mảng này chỉ nên lấy triết lý deploy, layer hóa, và guideline maintainers.
