# Script Proposals

## scripts/healthcheck.ps1
- **Mục đích:** Kiểm tra toàn bộ service (Docker, Ollama, Qdrant, runner, gateway)
- **Nội dung đề xuất:** Check từng container bằng docker ps, gọi health endpoints, báo kết quả
- **Rủi ro:** Thấp — chỉ đọc, không ghi
- **Khi nào chạy:** Hàng ngày, hoặc trước khi upgrade

## scripts/audit.ps1
- **Mục đích:** Chạy audit tự động (giống audit đã làm)
- **Nội dung đề xuất:** tree + files.csv + docker ps + ports + security scan
- **Rủi ro:** Thấp — chỉ đọc, không ghi
- **Khi nào chạy:** Hàng tuần, hoặc trước upgrade lớn

## scripts/backup.ps1
- **Mục đích:** Git commit + push + consolidate memory
- **Nội dung đề xuất:** git add -A, git commit, git push, python memory_consolidator.py
- **Rủi ro:** Trung bình — có thể push lỗi nếu workspace dirty
- **Khi nào chạy:** Hàng ngày, hoặc trước khi upgrade

## scripts/doctor.ps1
- **Mục đích:** Chẩn đoán lỗi phổ biến
- **Nội dung đề xuất:** Kiểm tra port conflicts, Docker service, git status, pip check, syntax check
- **Rủi ro:** Thấp — chỉ đọc
- **Khi nào chạy:** Khi có lỗi

## scripts/start.ps1
- **Mục đích:** Khởi động toàn bộ hệ thống
- **Nội dung đề xuất:** Docker start containers, ensure Ollama running, verify ports
- **Rủi ro:** Thấp — start service là an toàn
- **Khi nào chạy:** Khi boot máy, hoặc sau stop

## scripts/stop.ps1
- **Mục đích:** Dừng toàn bộ hệ thống an toàn
- **Nội dung đề xuất:** Memory consolidate, git commit, docker stop
- **Rủi ro:** Trung bình — có thể mất dữ liệu session chưa lưu
- **Khi nào chạy:** Trước shutdown máy
