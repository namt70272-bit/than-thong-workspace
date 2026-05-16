# Review order cho skill khai-thac

## Checklist đọc file

### A. Tài liệu gốc
1. `README.md`
2. README phụ (`README-community.md`, tương đương)
3. `docs/ARCHITECTURE.md`
4. `docs/LIMITATIONS.md`
5. `docs/*INTEGRATION*.md`

### B. Bề mặt tích hợp
1. `openclaw.plugin.json`
2. plugin manifest trong thư mục con (`plugin/openclaw.plugin.json`, `skills/*/openclaw.plugin.json`)
3. install scripts (`install*.sh`, `setup*.sh`)
4. config mẫu (`config/*.json`, `config/*.yml`, `docker-compose*.yml`)

### C. Bề mặt thực thi
1. entrypoint (`plugin.py`, `index.js`, `src/index.ts`, `server.py`)
2. scripts thao tác chính
3. docker entrypoints / service definitions

### D. Logic lõi
1. `src/**`
2. `packages/**/src/**`
3. `bridge/**`
4. `context/**`

### E. Vùng cần cách ly
1. `.engram/`, `.cache/`, `data/`, `dist/`, `build/`
2. `*.db`, `*.sqlite`, `*.kuzu`, `*.pkl`
3. vendor code

## Quy tắc chọn nội dung

- Chỉ trích phần phục vụ mục tiêu hiện tại.
- Nếu một file chỉ chứa 10% thứ cần, tạo file mới từ 10% đó.
- Nếu config mẫu khác config hiện tại, tạo patch tối thiểu thay vì thay nguyên file.
- Nếu repo có state cũ, mặc định bỏ qua khi import.

## Mẫu kết luận

- **Nên lấy:** file/khối logic, config tối thiểu, rule, docs hữu ích
- **Không nên lấy:** cache, runtime state, vendor thừa, dữ liệu mẫu, lockfiles không cần thiết
- **Cách đưa vào E:** candidate riêng → test → patch tối thiểu → verify
