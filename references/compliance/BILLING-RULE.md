# BILLING RULE

## Tên luật
**billing**

## Mục tiêu
Mọi công việc phải ưu tiên xử lý bằng công cụ nội bộ/local-first. Không được làm phát sinh billing cho model, API, dịch vụ cloud, hay provider trả phí nếu chưa báo và được duyệt rõ ràng.

## Luật cứng
- Không dùng billing trong bất kỳ trường hợp nào nếu chưa được duyệt trước.
- Mọi công việc nội bộ phải được ưu tiên giải quyết bằng:
  - file local
  - script local
  - tool có sẵn trong OpenClaw
  - workflow local trong workspace
  - tài liệu local trên E:
- Chỉ ngoại lệ với các việc bản chất cần Internet để đọc/kiểm tra bên ngoài; khi đó vẫn phải tránh mọi đường dẫn có billing.
- Nếu có nguy cơ phát sinh billing cho model/API/provider: **dừng lại, báo rõ, không tự chạy**.

## Áp dụng
- Áp dụng cho toàn bộ tác vụ phân tích, tổ chức, sync, import, cleanup, indexing, templating, workflowing, documentation, local automation.
- Áp dụng cho mọi bước nâng cấp hệ thống hiện tại.

## Ưu tiên công cụ
1. Nội bộ / local script
2. OpenClaw built-in tools không chạm billing mới
3. File-based workflow / templates / docs
4. Internet read-only nếu thật cần
5. Bất kỳ đường trả phí nào -> phải báo trước

## Cấm
- Tự ý dùng API key mới
- Tự ý gọi dịch vụ có meter usage
- Tự ý cài/đăng nhập công cụ cloud có khả năng tính phí
- Tự ý chuyển tác vụ nội bộ sang model/provider trả phí

## Quy tắc quyết định
Nếu một việc có thể làm bằng nội bộ thì **phải làm bằng nội bộ**.
Nếu chưa rõ có chạm billing không thì **coi như có rủi ro billing** và phải báo.
