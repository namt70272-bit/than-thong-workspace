# .gitignore Proposal

## Thêm các dòng sau vào `.gitignore`

### Nhóm 1: Secret & Credentials
```
# Secrets & credentials
.env
.env.*
!.env.example
*.key
*.pem
*-key.json
credentials*.json
service-account*.json
oauth*.json
token*
```

**Giải thích:** Bảo vệ mọi file secret không bị commit lên GitHub. Hiện tại `config/gcp-n8n-vertex-ai-key.json` đang không được gitignore → nguy cơ lộ GCP private key.

---

### Nhóm 2: Audit reports
```
# Audit reports
_audit/
_audit/**/*
!_audit/*.md
```

**Giải thích:** Audit report chứa Gitleaks findings + Trivy scan có thể lộ secret pattern. Chỉ giữ .md files.

---

### Nhóm 3: Runner credentials
```
# GitHub runner
runner/
.runner/
```

**Giải thích:** `runner/.credentials` chứa OAuth token. `runner/_diag/` chứa log có credential config. Hiện tại runner/ đã được push lên GitHub.

---

### Nhóm 4: Browser profile
```
# Browser profiles
browser-profile/
chrome-profile/
user-data-dir/
**/User Data/
**/Default/
```

**Giải thích:** Nếu có browser profile cho automation, không được commit (chứa cookies, session).

---

### Nhóm 5: Logs & Cache
```
# Logs & cache
**/__pycache__/
*.pyc
*.pyo
.pytest_cache/
**/_diag/
**/*.log
logs/
cache/
tmp/
temp/
downloads/
```

**Giải thích:** Runner diagnostic logs (runner/_diag/) chứa thông tin credential. Các file log khác không cần backup.

---

### Nhóm 6: Data
```
# Data
data/**
!data/**/*.md
n8n-db*.sqlite
*.db
*.sqlite
*.sqlite3
```

**Giải thích:** Database files không nên commit.

---

## Đề xuất `.gitignore` đầy đủ

```gitignore
# === OpenClaw Workspace ===

# Secrets & credentials
.env
.env.*
!.env.example
*.key
*.pem
*-key.json
credentials*.json
service-account*.json
oauth*.json
token*

# Audit reports
_audit/
_audit/**/*
!_audit/*.md

# GitHub runner
runner/
.runner/

# Browser profiles
browser-profile/
chrome-profile/
user-data-dir/

# Logs & cache
__pycache__/
*.pyc
*.pyo
.pytest_cache/
logs/
cache/
tmp/
temp/
downloads/
**/_diag/
**/*.log

# Data
data/**
!data/**/*.md
*.db
*.sqlite
*.sqlite3

# OS files
Thumbs.db
.DS_Store
```

## Rủi ro
- Các pattern quá rộng có thể bỏ sót file cần commit (ví dụ `data/` chứa markdown docs)
- Cần kiểm tra git status sau khi apply để không mất file quan trọng

**Không tự sửa .gitignore — chờ xác nhận.**
