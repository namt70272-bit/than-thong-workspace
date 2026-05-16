# A0 — Hệ thống tra cứu

## Đã xác nhận an toàn tuyệt đối để lấy trước

### 1) Spy-TìmKiếm
**Chỉ lấy:**
- `README.md`
- `ROADMAP.md`
- `config.example.json`
- docs mô tả query modes

**Không lấy:**
- Dockerfile
- docker-compose
- `main.py`
- `run.sh`

### 2) Tavily-SinhKey
**Chỉ lấy:**
- `README.md`
- `config.example.py`
- docs ảnh/flow chỉ để hiểu quy trình

**Không lấy:**
- `main.py`
- solver scripts
- proxy runtime
- `.env.example` cho proxy

### 3) FireCrawl
**Chỉ lấy:**
- README/capabilities/docs

**Không lấy:**
- service/runtime code

## Kết luận
A0 của mảng tra cứu là đọc capability map và query patterns; không động vào key generation hay crawler runtime.
