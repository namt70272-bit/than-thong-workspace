# IMPORT MAP — Từ 16 mảng vào hệ thật

Mục tiêu: nhập A0 vào hệ hiện tại theo đích cuối rõ ràng, không nhầm chỗ, không tạo 2 nguồn sự thật.

## Đích cuối trong workspace
- `references/` — docs kiến trúc, guideline, capability maps, ontology summary
- `examples/` — workflow templates, planning templates, sample structures
- `config/` — config templates, prompt templates, non-live reference configs
- `utils/` — utility snippets nhỏ, không side-effect
- `scripts/` — script tái sử dụng, chỉ khi đã qua review kỹ
- `reports/` — báo cáo tổng hợp, so sánh, risk analysis

## Mapping theo mảng

### 01 Quản lý agent
- role patterns -> `references/agent-patterns/`
- orchestration notes -> `references/agent-architecture/`
- sample layouts -> `examples/agent-layouts/`

### 02 Quản lý công việc
- planning/workflow templates -> `examples/work-management/`
- team process notes -> `references/work-management/`

### 03 Tự động hóa
- workflow templates -> `examples/automation/`
- DSL/pipeline notes -> `references/automation/`

### 04 Tổ chức tri thức / memory
- ontology summaries -> `references/memory-knowledge/`
- vault templates -> `examples/knowledge-structures/`

### 05 Quản lý code
- review/release patterns -> `references/code-management/`
- sample review templates -> `examples/code-review/`

### 06 Quản trị hệ thống
- checklists -> `references/system-admin/`
- deploy philosophy -> `references/deploy-guides/`

### 07 Tích hợp API
- route/auth templates -> `examples/api-contracts/`
- integration notes -> `references/api-integration/`

### 08 Hệ thống tra cứu
- capability maps -> `references/retrieval/`
- query templates -> `examples/retrieval/`

### 09 Mạng agent
- mesh/handoff docs -> `references/agent-mesh/`

### 10 Tài liệu tổ chức
- doc frameworks -> `references/documentation/`
- planning templates -> `examples/documentation/`

### 11 Cấu hình / tuân thủ
- rule packs -> `config/policy-templates/`
- prompt templates -> `config/prompt-templates/`
- persona/compliance refs -> `references/compliance/`

### 12 Hệ thống CLI
- CLI UX notes -> `references/cli-patterns/`
- sample command specs -> `examples/cli-specs/`

### 13 Quản lý tài liệu
- document templates -> `examples/document-templates/`
- structure notes -> `references/document-management/`

### 14 Quản lý nội dung
- content process notes -> `references/content-management/`
- workflow templates -> `examples/content-workflows/`

### 15 Điều khiển thiết bị / browser
- boundary/control notes -> `references/device-control/`

### 16 Hạ tầng / deploy / platform
- infra philosophy/RFC -> `references/infrastructure/`
- deploy templates -> `examples/infrastructure/`

## Quy tắc
- Không nhập thẳng từ `E:\KY-DATA\OpenClaw\mang-he-thong\`
- Phải qua `expansion/candidates/` trước
- Chỉ khi candidate ổn mới copy/patch vào đích cuối
