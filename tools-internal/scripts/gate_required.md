# Gate Required Policy

## Cổng bắt buộc cho công việc nội bộ
- `preflight_runner.py` — cổng vào chuẩn trước mọi quyết định nội bộ
- `billing_wrapper.py` — wrapper chạy trusted internal script sau khi qua gate
- `import_orchestrator.py` — cổng bắt buộc cho mọi import candidate -> runtime
- `ops_console.py` — console điều hành chuẩn

## Quy tắc
- Không chạy script nội bộ trực tiếp nếu có wrapper tương ứng
- Import nội bộ phải đi qua `import_orchestrator.py`
- Kiểm tra policy phải đi qua `preflight_runner.py`
- Nếu một script chưa có trong trusted registry thì không được wrapper cho chạy
