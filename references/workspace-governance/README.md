# Workspace Governance / Historical Operational Docs

Thư mục này chứa các tài liệu vận hành, tái cấu trúc, và báo cáo lịch sử đã được dời khỏi root để tránh trùng nguồn sự thật ở top-level workspace.

## Giữ ở root
Các file nên ở root vì là điểm vào chính:
- README.md
- WORKSPACE.md
- DIRECTORY-MAP.md
- QUICK-START.md
- REFERENCE-INDEX.md
- SKILL-REGISTRY.md
- CHANGES.md
- AGENTS.md / SOUL.md / USER.md / TOOLS.md / HEARTBEAT.md / DATA-STORE.md / IDENTITY.md / MEMORY.md

## Dời khỏi root
Các file mang tính historical/report/restructure nên nằm ở đây để root gọn:
- optimization reports
- restructure plans/completion notes
- summary snapshots
- completion notes

## Quy tắc
- Root chỉ giữ landing + canonical guides
- Tài liệu historical/secondary chuyển vào `references/workspace-governance/`
- Nếu hai file cùng nói về cùng một chủ đề, chọn 1 file canonical ở root và chuyển file còn lại vào đây
