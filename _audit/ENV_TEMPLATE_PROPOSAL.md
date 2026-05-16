# .env Template Proposal

## File: `.env.example`

```bash
# ============================================
# OpenClaw Environment Configuration Template
# ============================================
# Copy this file to .env and fill in your values.
# NEVER commit .env to version control!
# ============================================

# --- API Keys (Required) ---
# Get your Gemini API key: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Get your OpenAI API key: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# --- Google Cloud (Optional) ---
# Path to GCP service account JSON (outside workspace!)
# GOOGLE_APPLICATION_CREDENTIALS=C:\secrets\gcp-service-account.json

# --- PostHog (Optional) ---
# Disable telemetry by leaving this empty
# POSTHOG_API_KEY=

# --- OpenClaw Paths ---
OPENCLAW_HOME=./

# Data & storage paths
DATA_PATH=./data/
MEMORY_PATH=./memory/
LOG_PATH=./data/logs/
CACHE_PATH=./data/cache/

# --- Config Paths ---
OPENCLAW_CONFIG_PATH=./config/
MCP_CONFIG_PATH=./configs/mcp/
TOOLS_CONFIG_PATH=./configs/tools/

# --- Browser Profile ---
# Path to dedicated browser profile for automation
# Must be a separate profile, NOT the personal Chrome profile
BROWSER_PROFILE_PATH=./data/browser-profile/
BROWSER_HEADLESS=true

# --- Ollama (Local LLM) ---
OLLAMA_HOST=http://localhost:11434

# --- Qdrant (Vector DB) ---
QDRANT_HOST=localhost
QDRANT_PORT=6333

# --- Docker ---
DOCKER_HOST=
COMPOSE_FILE=./docker-compose.yml
```

## Nguyên tắc
1. **Không đưa key thật** vào `.env.example`
2. **Mọi secret** đều qua env var, không hardcode
3. **Path có thể thay đổi** tùy theo cấu trúc mới
4. **GCP key** phải ở ngoài workspace

## File cần tạo
- `.env.example` — template sạch
- `.env` — thật, có key (đã gitignored)

## Các key cần migrate từ hardcode → env var

| Key hiện tại | File nguồn | Env var mới |
|---|---|---|
| `AIzaSyC28WW_****` | 5 scripts trong scripts/ | `GEMINI_API_KEY` |
| `phc_hgJkUVJFYtmaJqrvf6CYN67TIQ8yhXAkWzUn` | reference-library/mem0/telemetry.py | `POSTHOG_API_KEY` |
| GCP private key | config/gcp-n8n-vertex-ai-key.json | `GOOGLE_APPLICATION_CREDENTIALS` |
| OpenAI keys (nếu có) | scripts/*.py | `OPENAI_API_KEY` |

**Không tự tạo .env — chờ xác nhận.**
