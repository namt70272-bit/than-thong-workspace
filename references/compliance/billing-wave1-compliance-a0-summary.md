# A0 — Cấu hình / tuân thủ

## Đã xác nhận an toàn tuyệt đối để lấy trước

### 1) Prompt-LặpLại-V2
**Chỉ lấy:**
- `README.md`
- `runbook.md`
- `proactive-integration.md`

**Không lấy:**
- `scripts/ab_tester.py`
- `scripts/repeat_bench.py`
- bất kỳ mã chạy benchmark

**Giá trị:**
- mẫu lặp prompt có kiểm soát
- cách tổ chức runbook
- cách mô tả integration an toàn

### 2) SystemPrompt-MôHình-AITools
**Chỉ lấy:**
- `README.md`
- các file `Prompt.txt` làm tài liệu tham khảo
- `Tools.json` chỉ để đọc cấu trúc công cụ

**Không lấy:**
- nguyên bộ prompt để nhét thẳng vào runtime
- bất kỳ prompt có giả định toolchain khác hệ hiện tại

**Giá trị:**
- thư viện prompt/system mẫu
- pattern mô tả tool use
- pattern persona/tool contract

## Cách nhập tối thiểu sau này
- chắt lọc rule vào `workspace/expansion/imports/rules/`
- chắt lọc prompt mẫu vào `workspace/expansion/imports/config-templates/`

## Kết luận
Mảng này là mảng an toàn nhất để khai thác đầu tiên vì chủ yếu là tài liệu/prompt/rules, không cần chạy gì.
