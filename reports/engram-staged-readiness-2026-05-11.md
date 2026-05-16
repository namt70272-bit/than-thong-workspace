# Engram staged readiness — 2026-05-11

## Kết luận ngắn
Engram **đã đủ để bước sang staged integration**.
Nó **chưa phải bản hoàn chỉnh production-final**.

## Hiện tại đã có gì
- Nhánh tối thiểu đã trích tại `E:\KY-DATA\OpenClaw\projects\engram-candidate`
- Nhánh test cô lập đã vá tại `E:\KY-DATA\OpenClaw\projects\engram-isolated-test`
- Bundle staged để chuẩn bị nối OpenClaw tại `E:\KY-DATA\OpenClaw\projects\engram-openclaw-staged`

## Những gì đã xác nhận pass
- Import recall engine: pass
- Cài dependency local cho nhánh test: pass
- Tự bootstrap Qdrant collection đúng schema: pass
- Store/search trong isolated engine: pass
- Store/search qua `engine\plugin.py`: pass
- Preflight staged bundle với Qdrant + FastEmbed: pass

## Những lỗi đã vá
1. Copy thiếu source `src\recall` trong nhánh test
2. Store báo success giả dù Qdrant chưa ghi thật
3. Collection mới không tự tạo đúng schema `dense + bm25`
4. Plugin thiếu env điều khiển `ENGRAM_DATA_DIR`, graph, consolidation
5. Fallback Python path chưa hợp Windows
6. Preflight probe dùng endpoint Qdrant không phù hợp môi trường hiện tại

## Hiện tại có thể áp dụng chưa?
### Có, nhưng chỉ ở mức staged / controlled rollout
Nghĩa là:
- dùng runtime staging hoặc runtime phụ
- collection riêng
- data dir riêng
- graph tắt ở vòng đầu
- chưa bật thẳng vào runtime chính đang phục vụ

## Đây đã là bản nâng cấp hoàn chỉnh chưa?
Chưa.

Nó mới là **bản nâng cấp khả dụng để đưa vào giai đoạn áp dụng thử**.
Để gọi là hoàn chỉnh, còn thiếu:
- wiring thật với OpenClaw plugin loader trong staging runtime
- test hook auto-recall / auto-capture end-to-end trong session thật
- test restart persistence
- test concurrent calls
- quyết định chiến lược migration từ state/collection cũ
- rollback switch rõ ràng trước khi bật trên runtime chính

## Bundle sẵn để đi tiếp
- `E:\KY-DATA\OpenClaw\projects\engram-openclaw-staged\README.md`
- `E:\KY-DATA\OpenClaw\projects\engram-openclaw-staged\STAGED-CHECKLIST.md`
- `E:\KY-DATA\OpenClaw\projects\engram-openclaw-staged\openclaw-staging-config-snippet.json`
- `E:\KY-DATA\OpenClaw\projects\engram-openclaw-staged\env.staging.example.ps1`
- `E:\KY-DATA\OpenClaw\projects\engram-openclaw-staged\preflight.ps1`

## Khuyến nghị
Đi tiếp theo thứ tự:
1. tạo runtime/plugin staging riêng
2. gắn bundle staged vào đó
3. test memory hooks thật
4. xác nhận rollback
5. rồi mới cân nhắc bật vào runtime chính
