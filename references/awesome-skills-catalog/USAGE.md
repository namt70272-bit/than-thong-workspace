# Awesome Agent Skills - How to Use

**Version:** 1.0  
**Updated:** 2026-05-12  
**License:** MIT  

## 🚀 Quick Start (2 phút)

### 1. Mở INDEX.md
```
references/awesome-skills-catalog/INDEX.md
```
- Xem danh sách 30+ công ty
- Xem các category chính (Web, API, ML/AI, Security, etc.)
- Hiểu cách tổ chức

### 2. Tìm Skill Cần
```
references/awesome-skills-catalog/README.md
```
- Ctrl+F tìm kiếm theo:
  - Tên công ty (Google, Stripe, Cloudflare, etc.)
  - Chủ đề (React, TensorFlow, Terraform, etc.)
  - Tên skill

### 3. Review Skill Repository
- Click link → đi tới repo skill thực tế
- Đọc `README.md` hoặc `SKILL.md` của skill đó
- Hiểu yêu cầu, cách dùng, ví dụ

### 4. Test Isolated
- Đừng dùng thẳng vào production
- Test skill đó ở branch/environment tách biệt trước
- Verify nó hoạt động với setup của bạn

### 5. Integrate vào Agent
- Khi đã test OK → add vào config/agent chính
- Update TOOLS.md nếu cần track custom configs

---

## 📖 Sử Dụng Chi Tiết

### Scenario 1: Tìm Skill Xử Lý Document

**Problem:** Mình cần skill để create/edit PDF

**Steps:**
1. Mở `README.md`
2. Ctrl+F: "anthropics"
3. Tìm: `anthropics/pdf` 
   ```
   - **[anthropics/pdf](https://officialskills.sh/anthropics/skills/pdf)** 
     - Extract text, create PDFs, and handle forms
   ```
4. Click link → đi tới https://officialskills.sh/anthropics/skills/pdf
5. Read docs → nếu phù hợp → test → integrate

### Scenario 2: Khám Phá Security Best Practices

**Problem:** Mình muốn biết security skills có sẵn

**Steps:**
1. Mở `INDEX.md`
2. Tìm: "Security: Trail of Bits specialized"
3. Mở `README.md`
4. Ctrl+F: "Trail of Bits"
5. Xem tất cả 22 skills từ Trail of Bits
6. Browse qua, pick cái phù hợp

### Scenario 3: Add Skill Mới vào Awesome List

**Problem:** Mình có skill hay → muốn add vào Awesome list

**Steps:**
1. Đọc `CONTRIBUTING.md` → hiểu requirements
2. Verify skill của bạn:
   - ✅ Public repo
   - ✅ Có documentation (README/SKILL.md)
   - ✅ Đã có community adoption (không brand new)
3. Format entry:
   ```
   - **[author/skill-name](link-to-repo)** - Short description (≤10 words)
   ```
4. Submit PR tới https://github.com/VoltAgent/awesome-agent-skills

---

## 📊 Danh Mục Chính

### Official Skills (30+ công ty)

| Company | Skills | Examples |
|---------|--------|----------|
| Anthropic | 17 | docx, pptx, xlsx, pdf, web-artifacts |
| Google | Multiple | Gemini API, Vertex AI, Workspace CLI |
| Microsoft | 133+ | Azure SDK (40+), multiple languages |
| Stripe | - | Payment integrations |
| Cloudflare | - | Workers, KV, AI Gateway |
| Vercel | - | React, Next.js, Web Design |
| Trail of Bits | 22 | Security & auditing |
| Hugging Face | 13 | ML workflows |
| And 22+ more... | ~1100 total | - |

### Community Skills

- **Marketing:** Email, social media, content
- **Productivity:** Calendar, todo, notes management
- **Development:** Testing, CI/CD, code review
- **Context Engineering:** Data parsing, embeddings
- **AI & Data:** LLM integrations, data analysis
- **Other:** Niche tools, language-specific

---

## 🎯 Use Cases

### For Agent Developers
- 📖 **Learn:** Browse skills từ các company → learn patterns
- 🔍 **Find:** Tìm skill phù hợp thay vì build from scratch
- 🛠️ **Integrate:** Review → test → add vào agent

### For Framework Users (Claude, Copilot, etc.)
- 🚀 **Extend:** Find skills để extend agent capabilities
- 📚 **Reference:** Xem cách các công ty tổ chức skills
- 💡 **Inspiration:** Get ideas từ community

### For Contributors
- 📝 **Submit:** Add skill mới sau khi mature
- 🔗 **Link:** Share repo + docs → VoltAgent curates

---

## 🔗 Links & Resources

- **Awesome List Repo:** https://github.com/VoltAgent/awesome-agent-skills
- **Website:** https://officialskills.sh/ (300k+ monthly views)
- **VoltAgent Framework:** https://github.com/VoltAgent/voltagent
- **Discord Community:** https://s.voltagent.dev/discord
- **ClawhHub (OpenClaw skills):** https://clawhub.ai

---

## ⚠️ Important Notes

### ✅ DO

- ✅ Use this as **reference only** (không install mù)
- ✅ **Review** skill repo trước dùng
- ✅ **Test cô lập** trước integrate
- ✅ **Respect licenses** của mỗi skill
- ✅ **Check compatibility** với setup của bạn

### ❌ DON'T

- ❌ Không cài 1100 skills cùng lúc
- ❌ Không giả định skill nào cũng suitable cho bạn
- ❌ Không skip reviewing repo đó
- ❌ Không integrate mà không test
- ❌ Không coi danh sách này là production state

---

## 📞 Support & Feedback

- **For Awesome Skills List Issues:**
  - GitHub Issues: https://github.com/VoltAgent/awesome-agent-skills/issues
  - Check existing issues trước submit

- **For Individual Skill Help:**
  - Đi tới repo skill đó
  - Check docs + existing issues
  - Contact skill author/maintainer

- **For VoltAgent Framework Questions:**
  - Discord: https://s.voltagent.dev/discord
  - GitHub: https://github.com/VoltAgent/voltagent

---

## 📋 Checklist: Before Using a Skill

- [ ] Đã read skill's README/documentation
- [ ] Đã check requirements (dependencies, auth, etc.)
- [ ] Đã kiểm tra compatibility với agent framework
- [ ] Đã test ở isolated environment
- [ ] Đã review any security implications
- [ ] Đã understand license & usage restrictions
- [ ] Có fallback/rollback plan nếu cần

---

**Happy skill hunting!** 🚀

**Remember:** Quality over quantity. One well-tested skill beats 10 untested ones.

---

Created: 2026-05-12  
By: Khai thác protocol  
License: MIT (same as source)
