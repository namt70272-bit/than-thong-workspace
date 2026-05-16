# STORAGE POLICY — E: ONLY

## Nguyên tắc cứng
- Mọi dữ liệu làm việc, review, candidate, import, docs trích lọc đều nằm trên ổ `E:`
- Ổ `C:` chỉ là app/runtime/npm/node/code-mirror, không tạo dữ liệu làm việc mới ở đó
- Nguồn ngoài như `G:` chỉ là nơi đọc/rà soát, không phải nơi tích hợp trực tiếp

## Áp dụng cho chương trình mở rộng
- Hồ sơ mảng: `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\expansion\domains\`
- Import an toàn: `...\expansion\imports\`
- Review/candidate: `...\review\`
- Tạm thời: `...\tmp-staging\`

## Cấm
- Không copy nguyên repo ngoài vào workspace đang chạy
- Không tạo cache/build/node_modules/dist trong khu mở rộng
- Không giữ state DB/vector cũ từ nguồn ngoài
