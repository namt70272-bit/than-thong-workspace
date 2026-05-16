# KẾ HOẠCH NÂNG CẤP HỆ THỐNG TỪ E:\SKILL

**Ngày:** 2026-05-13  
**Nguyên tắc:** Chỉ nâng cấp thứ đã có, không thêm mới tràn lan.  
**Pipeline:** Gate → đọc SKILL.md → so sánh với hiện tại → kiểm tra xung đột → import candidate → validate → sync → rollback

---

## CÁC BƯỚC KIỂM TRA XUNG ĐỘT

Trước khi import bất kỳ skill nào, kiểm tra:
1. **Trùng tên** — skill đã có trong `workspace/skills/` chưa?
2. **Trùng chức năng** — skill mới có làm việc skill cũ đang làm không?
3. **Trùng dependency** — có yêu cầu CLI/package khác với hệ hiện tại không?
4. **Trùng port/service** — có mở port/service mới không?
5. **Allowed-tools** — có yêu cầu tool mà hệ không có không?
6. **Billing risk** — có API key/service tính phí không?

---

## ƯU TIÊN — Xem skill nào nâng cấp được thứ đã có

### 🥇 1. security (hiện có) ← 10-Bao-Mat-Trail-of-Bits (74 skills)
**Hiện tại:** `workspace/skills/security/` — 1 SKILL.md, quản lý 1Password CLI  
**E:\skill có:** Trail of Bits — 74 skills bảo mật chuyên sâu  
**Nâng cấp:** Có thể thêm security audit patterns, vulnerability scanning, OWASP  
**Xung đột:** Không — security skill hiện tại rất nhỏ, không đụng nhau  
**Cách làm:** Đọc top 10 skills từ Trail of Bits → chọn 3-5 cái phù hợp → import vào `references/compliance/`  
**Rủi ro:** Thấp — mostly docs và rule patterns

### 🥈 2. automation (hiện có) ← 03-Tu-dong-hoa (754 skills) + 46-n8n (7 skills)
**Hiện tại:** `workspace/skills/automation/` — TaskFlow, cron, Browser Use  
**E:\skill có:** 754 kỹ năng automation + 7 n8n skills  
**Nâng cấp:** Pipeline patterns, deployment workflow, CI/CD templates  
**Xung đột:** Có thể trùng với TaskFlow concepts, cần lọc  
**Cách làm:** Đọc mẫu, lấy workflow pattern, không import nguyên

### 🥉 3. code-development (hiện có) ← 01-Claude (137 skills) + 05-code (1,461 skills)
**Hiện tại:** `workspace/skills/code-development/` — GitNexus, code review  
**E:\skill có:** Angular, React, TypeScript, Python, Go, Rust patterns  
**Nâng cấp:** Thêm code review guidelines, framework patterns  
**Xung đột:** Không nếu chỉ lấy pattern, không lấy runtime  
**Cách làm:** Lọc theo ngôn ngữ lập trình, chỉ import reference

### 4. notes-knowledge (hiện có) ← 29-Notion (4 skills) + 12-Google-Workspace (95 skills)
**Hiện tại:** `workspace/skills/notes-knowledge/` — Notion, Obsidian, Apple Notes  
**E:\skill có:** Notion API, Google Workspace (Gmail, Drive, Calendar, Docs)  
**Nâng cấp:** Thêm Google Workspace integration patterns  
**Xung đột:** Không — workspace skills chỉ là API wrappers  
**Rủi ro:** Rất thấp

### 5. web-search (hiện có) ← 24-Brave (11 skills)
**Hiện tại:** `workspace/skills/web-search/` — blogwatcher, Gemini CLI, web search  
**E:\skill có:** Brave Search API, search patterns  
**Nâng cấp:** Có thể thêm Brave search capability  
**Xung đột:** Không — skill search hiện tại không dùng Brave  
**Rủi ro:** Cần API key (billing check!)

### 6. communication (hiện có) ← 12-Google-Workspace (95 skills)
**Hiện tại:** `workspace/skills/communication/` — Email, Discord, Slack  
**E:\skill có:** Gmail, Google Calendar, Google Drive, Google Docs  
**Nâng cấp:** Thêm Google integration patterns  
**Xung đột:** Không — communication skill hiện tại dùng Himalaya, không dùng Google API  
**Cách làm:** Đọc mẫu → import reference

### 7. media-video (hiện có) ← 14-fal-ai (16 skills)
**Hiện tại:** `workspace/skills/media-video/` — ffmpeg, camera  
**E:\skill có:** fal.ai media generation (image, video, audio)  
**Nâng cấp:** AI media generation patterns  
**Xung đột:** Không  
**Rủi ro:** fal.ai có API key (billing check!)

### 8. review-code (hiện có) ← 38-CodeRabbit (2 skills)
**Hiện tại:** `workspace/skills/review-code/` — local AI code review  
**E:\skill có:** CodeRabbit AI review  
**Nâng cấp:** Code review workflow patterns  
**Xung đột:** Không — review-code skill rất nhỏ  
**Rủi ro:** Thấp

### 9. utilities (hiện có) ← 04 + 05 + 06 + 08 (product management)
**Hiện tại:** `workspace/skills/utilities/` — weather, Trello, GitHub CLI  
**E:\skill có:** Product management, marketing, startup skills  
**Nâng cấp:** Có thể thêm product management patterns  
**Xung đột:** Không — utilities rất linh hoạt

### 10. than-thong (hiện có) — KHÔNG nâng cấp từ E:\skill
**Lý do:** than-thong là lớp điều hành nội bộ tự xây, không có skill ngoài nào tương đương.

---

## SKILL KHÔNG CÓ TRONG HỆ — NÊN ĐỂ SAU

Các skill trong E:\skill chưa có trong hệ hiện tại:
- Flutter (09) — không dùng Flutter
- WordPress (16) — không dùng WordPress
- Apollo GraphQL (17) — không dùng GraphQL server
- Hugging Face (18) — có thể tham khảo sau
- Coinbase (25), Binance (30) — crypto, không cần
- GSAP Animation (27) — animation, không cần
- Datadog (28) — monitoring, đã có sentry
- Figma (34) — design, có thể tham khảo
- DuckDB (35) — embedded DB
- Vector Databases (40) — có thể tham khảo cho memory

Những cái này không nên import vội — chưa có mảng tương ứng, dễ gây rối.

---

## KẾ HOẠCH THỰC HIỆN

### Bước 1: Nâng cấp security (dễ nhất, giá trị cao)
1. Đọc 10-Bao-Mat-Trail-of-Bits → chọn 3-5 security skills
2. Kiểm tra xung đột với security skill hiện tại
3. Import vào `references/compliance/` qua pipeline thần thông

### Bước 2: Nâng cấp automation
1. Đọc mẫu automation skills từ E:\skill
2. Lọc workflow patterns
3. Import vào `references/automation/`

### Bước 3-10: Làm dần các mảng còn lại

---

## XUNG ĐỘT CẦN TRÁNH

| Nguy cơ | Skill từ E:\skill | Skill hiện tại | Hậu quả |
|---|---|---|---|
| Trùng tên | Nếu import trực tiếp vào skills/ | skills/security/ | Overwrite |
| Trùng allowed-tools | Yêu cầu tool không có | Bash, Read, Write... | Skill chạy sai |
| Billing | Cần API key mới | Không có key | Lỗi runtime |
| Service/Port | Yêu cầu chạy service nền | Không có | Skill treo |
