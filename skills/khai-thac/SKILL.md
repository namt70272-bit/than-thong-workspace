---
name: khai-thac
description: Rà soát, bóc tách, và tái sử dụng nội dung từ thư mục/repo ngoài workspace mà không bê nguyên cây vào hệ đang chạy. Dùng khi cần đọc kỹ trước khi nhập về E, chỉ lấy phần cần thiết, tránh trùng lặp, chép đè, state bẩn, xung đột config, hoặc làm gãy hệ thống.
---

# Khai thác an toàn

## Luật cứng

- Không copy nguyên repo/thư mục vào E để dùng ngay.
- Không chép đè file đang dùng nếu chưa diff, backup, và xác định rõ mục đích.
- Không nhập runtime state, cache, DB, vector index, hoặc file sinh tự động vào production nếu chưa kiểm chứng.
- Ưu tiên **tạo file mới tối thiểu** từ nội dung đã chọn thay vì copy cả cụm.
- Mọi tích hợp phải đi theo thứ tự: **inventory → đọc → chọn lọc → dựng bản tối thiểu → test cô lập → mới cân nhắc nối vào hệ thật**.

## Quy trình chuẩn

### 1) Inventory trước

- Đếm file/thư mục và tổng dung lượng.
- Dựng sơ đồ thư mục 2-3 tầng.
- Gắn nhãn từng vùng:
  - docs
  - config
  - executable/plugin
  - runtime state/data
  - vendor
  - examples/assets

Nếu có file kiểu `.db`, `.sqlite`, `.pkl`, `.kuzu`, `.json` state, `.cache`, `dist`, `build`, `node_modules`, xem như vùng cần cách ly.

### 2) Đọc theo thứ tự nóng

Đọc trước các nhóm sau:
1. README / docs kiến trúc / limitations
2. config mẫu
3. plugin manifest / install script
4. entrypoint thực thi
5. lõi logic
6. vendor / generated / state

Chi tiết thứ tự đọc để ở `references/review-order.md`.

### 3) Chọn lọc nội dung cần lấy

Chỉ lấy 1 trong 3 kiểu sau:
1. **Ý tưởng/quy tắc** → chắt lọc thành file mới trong E
2. **Cấu hình mẫu** → chuyển thành patch tối thiểu cho config hiện tại
3. **Mã nguồn hữu ích** → chép từng file hoặc từng khối có chủ đích, không bê nguyên module nếu chưa cần

### 4) Dựng bản tối thiểu ở E

- Đặt vào thư mục review/candidate riêng, không nối thẳng vào runtime đang chạy.
- Nếu chỉ cần logic nhỏ, trích thành file mới thay vì mang cả repo.
- Nếu cần config, tạo diff/patch nhỏ nhất có thể.
- Nếu có state cũ đi kèm, bỏ ngoài candidate trừ khi chủ đích kiểm thử state đó.

### 5) Chặn lỗi chồng lấp

Trước khi đưa bất cứ gì vào E, luôn kiểm:
- có trùng tên file không
- có ghi đè config/tool/plugin đang chạy không
- có kéo theo port/service/dependency đã tồn tại không
- có đụng memory backend, auth, gateway, cron, plugin hooks không

### 6) Test cô lập trước khi nối thật

- Chạy đọc/inspect/test ở bản candidate.
- Chỉ khi ổn mới nối vào config/runtimes thật.
- Nếu có rủi ro restart, nói rõ trước.

## Câu lệnh chuẩn để gọi skill

- "Khai thác thư mục này theo chuẩn an toàn"
- "Dựng sơ đồ, đọc kỹ, chỉ lấy phần cần thiết"
- "Không bê nguyên repo, chỉ trích nội dung dùng được"
- "Làm candidate tối thiểu trước khi nhập vào E"

## Kết quả đầu ra bắt buộc

Luôn trả về:
- sơ đồ thư mục ngắn
- vùng nguy cơ cao
- danh sách file thực sự nên lấy
- danh sách file không nên lấy
- cách nhập tối thiểu vào E
- rủi ro nếu nối thẳng

## Không làm

- Không “bê sang rồi tính sau”.
- Không merge mù vào plugin/config đang chạy.
- Không coi dữ liệu mẫu đi kèm repo là dữ liệu production.
