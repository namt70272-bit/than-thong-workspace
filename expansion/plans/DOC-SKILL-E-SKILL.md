# KẾ HOẠCH ĐỌC & KHAI THÁC E:\SKILL

**Tổng quan:** 35,175 files, 3,142 SKILL.md, 46 thư mục, ~640MB  
**Mục tiêu:** Đọc → phân loại → chọn lọc → import an toàn qua thần thông  
**Nguyên tắc:** Không copy nguyên repo vào workspace. Qua gate/validate/sync/rollback.

---

## Phase 1 — Đọc hết các thư mục nhỏ (<=10 SKILL.md)

**19 thư mục, ~130 SKILL.md — nhanh, dễ đọc hết**

| Ưu tiên | Thư mục | SKILL.md | Nội dung |
|---|---|---|---|
| 1 | 24-Brave | 11 | Brave search API, browser |
| 2 | 25-Coinbase | 9 | Crypto/blockchain |
| 3 | 26-Cloudflare | 8 | Cloudflare workers, AI, R2 |
| 4 | 31-MongoDB | 7 | MongoDB database |
| 5 | 33-Browserbase | 7 | Browser automation |
| 6 | 34-Figma | 6 | Design/Figma API |
| 7 | 35-DuckDB | 6 | Embedded analytics DB |
| 8 | 36-Chat-Luong-Web | 6 | Web quality (Addy Osmani) |
| 9 | 37-Resend | 5 | Email API |
| 10 | 30-Binance | 6 | Binance trading API |
| 11 | 29-Notion | 4 | Notion API |
| 12 | 27-GSAP | 8 | Animation library |
| 13 | 32-Vercel-Nextjs | 3 | Vercel/NextJS deploy |
| 14 | 38-CodeRabbit | 2 | AI code review |
| 15 | 39-Redis | 1 | Redis cache |
| 16 | 46-n8n | 7 | n8n automation |
| 17 | 45-Ky-Thuat-Ngu-Canh | 13 | Community kỹ thuật |
| 18 | 28-Datadog | 24 | Datadog monitoring |
| 19 | 40-Vector-Databases | 26 | Vector DB comparison |

**Thời gian:** ~130 SKILL.md = đọc được trong 1-2 session

---

## Phase 2 — Đọc Official Skills (1-20)

**~800 SKILL.md, cần chia nhỏ theo session**

| Session | Thư mục | SKILL.md | Focus |
|---|---|---|---|
| 2a | 01-Claude-Chinh-Thuc | 137 | Claude official skills |
| 2b | 02-Microsoft-Azure | 132 | Azure + AI Foundry |
| 2c | 12-Google-Workspace | 95 | Gmail, Drive, Admin |
| 2d | 10-Bao-Mat-Trail-of-Bits | 74 | Security audit skills |
| 2e | 05-Quan-Ly-San-Pham-Pawel | 65 | Product management |
| 2f | 08-Khoi-Nghiep-Garry-Tan | 51 | Startup/entrepreneur |
| 2g | 04-Quan-Ly-San-Pham-Dean | 47 | Product management |
| 2h | 06-Tiep-Thi-Corey-Haines | 41 | Marketing |
| 2i | 03-OpenAI | 37 | OpenAI API skills |
| 2j | 19-Netlify | 39 | Netlify deploy + AI |
| 2k | 09-Flutter | 29 | Flutter mobile dev |
| 2l | 16-WordPress | 28 | WordPress dev |
| 2m | 17-Apollo-GraphQL | 27 | GraphQL |
| 2n | 18-Hugging-Face | 28 | Hugging Face Hub |
| 2o | 20-Firebase | 27 | Firebase |
| 2p | 15-Auth0 | 25 | Auth0 auth |
| 2q | 07-Sentry | 30 | Sentry error tracking |
| 2r | 11-Venice-AI | 20 | Venice AI API |
| 2s | 14-fal-ai | 16 | fal AI media |
| 2t | 22-Expo | 24 | React Native Expo |

**Thời gian:** ~800 skills, 2-3 session, mỗi session ~40 skills

---

## Phase 3 — Community skills (21, 23, 41-44)

**~1,900 SKILL.md — cần lọc theo chất lượng**

| Thư mục | SKILL.md | Cách xử lý |
|---|---|---|
| 41-Phat-Trien-Kiem-Thu | 1,031 | Chọn top 10% (có review, active) |
| 43-Chuyen-Nganh | 715 | Chọn theo domain cần |
| 44-Tiep-Thi-Mang-Xa-Hoi | 117 | Lọc marketing/social |
| 42-Nang-Suat-Cong-Tac | 90 | Lọc productivity |
| 21-Quang-Cao-Kim-Barrett | 24 | Marketing ads |
| 23-MiniMax | 34 | MiniMax AI |

---

## Phase 4 — Dọn cache

| Thư mục | Dung lượng | Hành động |
|---|---|---|
| `_repo_cache` | 72.8 MB | Xóa (cache git repos) |
| `_cache_repos` | 14.2 MB | Xóa |
| `_cache_repos_probe` | 3.9 MB | Xóa |
| `_tmp_*` | 0 MB | Xóa |

**Tổng cache:** ~91 MB, ~6,400 files — không ảnh hưởng gì nếu xóa.

---

## Phase 5 — Import thử (sau khi đọc)

Chọn những skill có giá trị cao nhất để import qua pipeline thần thông:
- Không copy nguyên thư mục vào `workspace/skills/`
- Chỉ import SKILL.md đã chọn vào `references/`
- Gate → validate → deep-validate → sync → rollback

---

## Tóm tắt thời gian

| Phase | Nội dung | Thời gian ước tính |
|---|---|---|
| 1 | Đọc ~130 SKILL.md nhỏ | 1 session |
| 2 | Đọc ~800 official skills | 2-3 sessions |
| 3 | Lọc community skills | 1-2 sessions |
| 4 | Dọn cache | 5 phút |
| 5 | Import chọn lọc | Theo nhu cầu |

**Tổng:** ~4-6 sessions để đọc + phân loại hết E:\skill.
