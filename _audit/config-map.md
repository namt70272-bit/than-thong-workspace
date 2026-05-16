# Config Map

## OpenClaw Config Files

| File | Path | Purpose | Has Secret? | Action |
|---|---|---|---|---|
| OpenClaw config | `E:\KY-DATA\OpenClaw\runtime-mirror\config\*` | Main gateway config | YES (tokens) | Keep, protect |
| .gitignore | `workspace\.gitignore` | Git exclusion rules | No | Keep |
| pyproject.toml | `workspace\pyproject.toml` | Ruff/Python settings | No | Keep |
| AGENTS.md | `workspace\AGENTS.md` | Agent behavior rules | No | Keep |
| SOUL.md | `workspace\SOUL.md` | Agent personality | No | Keep |
| TOOLS.md | `workspace\TOOLS.md` | Tool notes | Partial (paths) | Keep |
| USER.md | `workspace\USER.md` | User profile | No | Keep |
| MEMORY.md | `workspace\MEMORY.md` | Long-term memory | No | Keep |

## GitHub/CI Config

| File | Path | Purpose | Has Secret? | Action |
|---|---|---|---|---|
| * .yml | `.github/workflows/*` | 12 CI/CD workflows | YES (some have GH_TOKEN) | Can template token refs |
| .runner | `runner\.runner` | Runner registration | Partial | Keep |
| .credentials | `runner\.credentials` | Runner auth token | **YES** (OAuth token) | **PROTECT - DO NOT COMMIT** |
| .credentials_rsaparams | `runner\.credentials_rsaparams` | RSA keys | **YES** | **PROTECT** |

## Docker Config

| File | Path | Purpose | Has Secret? | Action |
|---|---|---|---|---|
| N/A (no docker-compose.yml) | - | Containers run via `docker run` | No | Consider docker-compose for reproducibility |

## Tool/Script Config

| File | Path | Purpose | Has Secret? | Action |
|---|---|---|---|---|
| than_thong_blocklist.py | `tools-internal/scripts/` | Blocked domains list | No | Keep |
| billing.policy.json | `tools-internal/policy/` | Billing rules | No | Keep |
| memory_consolidator.py | `tools-internal/scripts/` | Memory pipeline | No | Keep |
| workspace_rag.py | `tools-internal/scripts/` | RAG search | No (path config) | Keep |

## Dangerous Secrets Found

| Location | Risk | Action |
|---|---|---|
| `runner\.credentials` | OAuth token for GitHub runner | **Already in .gitignore? Check!** |
| `runner\.credentials_rsaparams` | RSA keys for runner | **Already in .gitignore? Check!** |
| GitHub classic PAT (stored in gh keyring) | Full repo access | Stored in Windows Credential Manager - safe |

## Config Recommendations

1. **Create env templates**: Extract hardcoded paths/tokens to `.env.template`
2. **Docker Compose**: Create `docker-compose.yml` for the 4 Docker services
3. **Gitignore check**: Ensure `runner/` is in `.gitignore` (contains credentials)
4. **Centralize config**: Move config-like values from script files into separate config
